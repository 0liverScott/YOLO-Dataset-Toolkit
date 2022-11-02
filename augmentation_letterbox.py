import os
import cv2
import numpy as np

from tqdm import tqdm
from PIL import Image, ImageOps

def xywh2xyxy(x, w=640, h=640, padw=0, padh=0):
    y = np.copy(x)
    y[0] = w * (x[0] - x[2] / 2) + padw  # top left x
    y[1] = h * (x[1] - x[3] / 2) + padh  # top left y
    y[2] = w * (x[0] + x[2] / 2) + padw  # bottom right x
    y[3] = h * (x[1] + x[3] / 2) + padh  # bottom right y
    return y

def xyxy2xywh(x, w=640, h=640):
    y = np.copy(x)
    y[0] = ((x[0] + x[2]) / 2) / w  # x center
    y[1] = ((x[1] + x[3]) / 2) / h  # y center
    y[2] = (x[2] - x[0]) / w  # width
    y[3] = (x[3] - x[1]) / h  # height
    return y

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, dw, dh, shape

def main():
    img_list = os.listdir(input_img_path)
    f = float
    for file in tqdm(img_list, desc='Resizing...'):
        im = ImageOps.exif_transpose(Image.open(f'{input_img_path}/{file}')).convert('RGB')
        im.thumbnail(photo_size)
        im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        im0, padw, padh, shape = letterbox(im, total_size, color=letter_color, auto=auto, stride=stride)
        cv2.imwrite(f'{output_img_path}/{file[:-4]}_letter.jpg', im0)

        with open(f'{input_txt_path}/{file[:-4]}.txt', 'r') as txt_org:
            with open(f'{output_txt_path}/{file[:-4]}_letter.txt', 'w') as txt:
                for line_org in txt_org:
                    line = line_org.split(' ')
                    cls = line[0]
                    xywh = [f(line[1]), f(line[2]), f(line[3]), f(line[4])]
                    bbox = xyxy2xywh(xywh2xyxy(xywh, w=shape[1], h=shape[0], padw=padw, padh=padh))
                    new_line = f"{cls} {' '.join(str(round(v, 6)) for v in bbox)}\n"
                    txt.write(new_line)


if __name__ == '__main__':
    photo_size = (256, 256)  # Resized photo size
    total_size = (640, 640)  # Letterbox + Resized photo size
    letter_color = (114, 114, 114)  # Set Letterbox color
    auto = False  # If you enable auto, total_size will set automatically by stride and photo_size
    stride = 32

    input_path = 'dataset_path'
    output_path = 'output_path'
    input_img_path = f'{input_path}/images'
    input_txt_path = f'{input_path}/labels'
    output_img_path = f'{output_path}/images'
    output_txt_path = f'{output_path}/labels'
    os.makedirs(output_img_path, exist_ok=True)
    os.makedirs(output_txt_path, exist_ok=True)

    main()
