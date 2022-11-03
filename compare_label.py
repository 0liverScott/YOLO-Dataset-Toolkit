import os
import cv2
import shutil
from tqdm import tqdm
from datetime import datetime
from PIL import Image, ImageDraw

def make_dirs(path):
    os.makedirs(f'{path}/labeled/images', exist_ok=True)
    os.makedirs(f'{path}/labeled/labels', exist_ok=True)
    os.makedirs(f'{path}/result/images', exist_ok=True)
    os.makedirs(f'{path}/result/labels', exist_ok=True)
    os.makedirs(f'{path}/original_images', exist_ok=True)
    if combine_image:
        os.makedirs(f'{path}/combined_images', exist_ok=True)

def draw_bbox(txt_list):
    for label in tqdm(txt_list, desc='Drawing BBOX...'):
        img_name = f'{label[:-4]}.jpg'
        img = cv2.imread(f'{label_img_path}/{img_name}')
        h, w = img.shape[:2]
        text_size = max(round((w + h) / 2 * 0.003), 2) / 2
        f = float
        with open(f'{label_txt_path}/{label}', 'r') as txt:
            for lines in txt:
                line = lines.split(' ')
                x1 = int((f(line[1]) - (f(line[3]) / 2)) * w)
                y1 = int((f(line[2]) - (f(line[4]) / 2)) * h)
                x2 = int((f(line[1]) + (f(line[3]) / 2)) * w)
                y2 = int((f(line[2]) + (f(line[4]) / 2)) * h)
                text_pos = (x1, y1 - 5)
                cv2.rectangle(img, (x1, y1), (x2, y2), colors[int(line[0])], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, classes[int(line[0])], text_pos, 1, text_size, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, classes[int(line[0])], text_pos, 1, text_size, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)
        cv2.imwrite(f'{output_path}/labeled/images/{img_name}', img)

def debug_label(a, b):
    print('-' * 120)
    print(f"|{str(a).strip().center(50)}{'|'.center(13)}{str(b).strip().center(50)}{'|'.center(12)}", end='')
    print(f"ERROR" if classes[int(a[0])] != classes[int(b[0])] else "")
    print('-' * 120)

def threshold(result_line, label_line):
    f = float
    result_line, label_line = result_line.split(' '), label_line.split(' ')
    x_center, y_center, width, height = f(result_line[1]), f(result_line[2]), f(result_line[3]), f(result_line[4])
    x_center_label, y_center_label = f(label_line[1]), f(label_line[2])

    if x_center - (width * threshold_x) <= x_center_label <= x_center + (width * threshold_x):
        if y_center - (height * threshold_y) <= y_center_label <= y_center + (height * threshold_y):
            return True
        else:
            return False
    else:
        return False

def compare(result, label, filename, error_class):
    break_more = False
    for liner in result:
        for linel in label:
            if threshold(liner, linel):  # Filter only same bbox
                if debug:
                    print(filename)
                    debug_label(liner, linel)
                if liner[0] != linel[0]:
                    error_class.append(filename)
                    break_more = True
                    break
        if break_more:
            break

def main():
    error_detect = []
    error_class = []

    start_time = datetime.now().strftime('%y%m%d_%H%M%S')

    for file in os.listdir(label_txt_path) if debug else tqdm(os.listdir(label_txt_path)):
        if os.path.isfile(f'{result_txt_path}/{file}'):
            with open(f'{result_txt_path}/{file}', 'r') as result_txt2:
                with open(f'{label_txt_path}/{file}', 'r') as label_txt2:
                    if len(list(enumerate(result_txt2))) != len(list(enumerate(label_txt2))):
                        error_detect.append(file)
                        continue
            with open(f'{result_txt_path}/{file}', 'r') as result_txt:
                with open(f'{label_txt_path}/{file}', 'r') as label_txt:
                    compare(result_txt, label_txt, file, error_class)
        else:
            error_detect.append(file)

    if output_log_txt:
        os.makedirs(f'{output_path}/logs', exist_ok=True)

    if error_detect:
        if output_log_txt:
            with open(f'{output_path}/logs/{start_time}_detect_error.txt', 'w') as log_detect_error:
                for file in error_detect:
                    log_detect_error.write(f"{file}\n")
        print(f'There are {len(error_detect)} error in detecting.'
              + f'Go check "{start_time}_detect_error.txt".' if output_log_txt else '')
    if error_class:
        if output_log_txt:
            with open(f'{output_path}/logs/{start_time}_class_error.txt', 'w') as log_class_error:
                for file in error_class:
                    log_class_error.write(f"{file}\n")
        print(f'There are {len(error_class)} error in result.'
              + f'Go check "{start_time}_class_error.txt".' if output_log_txt else '')

    error_all = error_detect + error_class

    make_dirs(output_path)
    draw_bbox(error_all)
    for file in tqdm(error_all, desc='Copying files...'):
        if os.path.isfile(f'{result_txt_path}/{file}'):
            shutil.copy2(f'{result_txt_path}/{file}', f'{output_path}/result/labels')
        shutil.copy2(f'{result_img_path}/{file[:-4]}.jpg', f'{output_path}/result/images')
        shutil.copy2(f'{label_txt_path}/{file}', f'{output_path}/labeled/labels')
        shutil.copy2(f'{label_img_path}/{file[:-4]}.jpg', f'{output_path}/original_images')
    if combine_image:
        for file in tqdm(error_all, desc='Combine images...'):
            img = f'{file[:-4]}.jpg'
            iml = Image.open(f'{output_path}/labeled/images/{img}')
            imr = Image.open(f'{output_path}/result/images/{img}')
            w, h = iml.size
            imc = Image.new('RGB', (2 * w, h), (0, 0, 0))
            imc.paste(imr, (0, 0))
            imc.paste(iml, (w, 0))
            imc.save(f'{output_path}/combined_images/{img}')


if __name__ == '__main__':

    # Detected result folder. Need to use save-txt and separate images, labels with each folder
    result_path = 'result_path'
    # Original dataset folder
    label_path = 'label_path'
    output_path = 'output_path_combine'

    # Make this equal to your model
    classes = ['Class 1', 'Class 2', 'Class 3']
    colors = [(0, 0, 222), (0, 222, 0), (0, 222, 222)]  # BGR

    # Threshold of bbox similarity
    threshold_x = 0.1
    threshold_y = 0.3

    output_log_txt = True
    combine_image = True  # Combine to one image label one and detect one
    debug = False

    result_txt_path = f'{result_path}/labels'
    result_img_path = f'{result_path}/images'
    label_txt_path = f'{label_path}/labels'
    label_img_path = f'{label_path}/images'

    main()
