import os
import cv2
import numpy as np

from tqdm import tqdm

def motion_blur(img, size=25):
    motion = np.zeros((size, size))
    motion[int((size - 1) / 2), :] = np.ones(size)
    motion = motion / size

    motion_output = cv2.filter2D(img, -1, motion)
    return motion_output

def main():
    img_list = os.listdir(input_img_path)
    for file in tqdm(img_list, desc='Resizing...'):
        im = cv2.imread(f'{input_img_path}/{file}')
        blur_size = round(im.shape[1] / (1000 / blur_threshold))
        im = motion_blur(im, size=blur_size)

        if show_img:
            cv2.imshow('motion', im)

            cv2.waitKey()
            cv2.destroyAllWindows()
        else:
            cv2.imwrite(f'{output_img_path}/{file[:-4]}_motion.jpg', im)

            with open(f'{input_txt_path}/{file[:-4]}.txt', 'r') as txt_org:
                with open(f'{output_txt_path}/{file[:-4]}_motion.txt', 'w') as txt:
                    for line_org in txt_org:
                        txt.write(line_org)


if __name__ == '__main__':

    blur_threshold = 25  # Set motion blur size 1 to 50
    show_img = False  # If show_img = True, just show result image, not to save

    input_path = 'input_path'
    output_path = 'output_path_motion'
    input_img_path = f'{input_path}/images'
    input_txt_path = f'{input_path}/labels'
    output_img_path = f'{output_path}/images'
    output_txt_path = f'{output_path}/labels'
    os.makedirs(output_img_path, exist_ok=True)
    os.makedirs(output_txt_path, exist_ok=True)

    main()
