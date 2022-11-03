import os

from tqdm import tqdm
from PIL import Image, ImageDraw


def censor():
    txt_list = os.listdir(input_txt_path)

    for label in txt_list if debug else tqdm(txt_list):

        if debug:
            print('=' * 100)
            print(label)
            print('-' * 100)

        img_name = f'{label[:-4]}.jpg'
        img = Image.open(f'{input_img_path}/{img_name}').convert('RGB')
        draw = ImageDraw.Draw(img, 'RGB')
        w, h = img.size
        f = float

        with open(f'{input_txt_path}/{label}', 'r') as txt:
            with open(f'{output_txt_path}/{label}', 'w') as txt_out:
                for lines in txt:

                    line = lines.split(' ')

                    if int(line[0]) in class_to_censor:
                        x1 = int((f(line[1]) - (f(line[3]) / 2)) * w)
                        y1 = int((f(line[2]) - (f(line[4]) / 2)) * h)
                        x2 = int((f(line[1]) + (f(line[3]) / 2)) * w)
                        y2 = int((f(line[2]) + (f(line[4]) / 2)) * h)

                        if debug:
                            print(line)
                            print(f'BBOX: {x1, y1, x2, y2}')

                        draw.rectangle(((x1, y1), (x2, y2)), fill=(0, 0, 0))

                    else:

                        if debug:
                            print(line)

                        txt_out.write(lines)
                if debug:
                    print('=' * 100)
                    print('\n')

        img.save(f'{output_img_path}/{img_name}', 'jpeg')


if __name__ == '__main__':

    debug = True

    class_to_censor = [0, 1]

    input_path = 'input_path'
    output_path = 'output_path_censor'
    input_img_path = f'{input_path}/images'
    input_txt_path = f'{input_path}/labels'
    output_img_path = f'{output_path}/images'
    output_txt_path = f'{output_path}/labels'
    os.makedirs(output_img_path, exist_ok=True)
    os.makedirs(output_txt_path, exist_ok=True)

    censor()
