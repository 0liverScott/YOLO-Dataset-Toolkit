import os

from tqdm import tqdm
from PIL import Image, ImageOps

def mirror():
    classes = {f'Class {v}': 0 for v in range(num_class)}
    target_classes = {f'Class {v}': 0 for v in range(num_class)}
    txt_list = os.listdir(input_txt_path)
    mirror_list = set([])

    for label in txt_list if debug else tqdm(txt_list, desc="Calculating..."):
        with open(f'{input_txt_path}/{label}', 'r') as txt:
            for lines in txt:  # Count Class
                line = lines.split(' ')
                classes[f'Class {line[0]}'] += 1
                if int(line[0]) in target_class:
                    mirror_list.add(label)

    for label in mirror_list if debug else tqdm(mirror_list, desc="Apply..."):

        if debug:
            print('=' * 100)
            print(label)
            print('-' * 100)

        img_name = f'{label[:-4]}.jpg'
        img = Image.open(f'{input_img_path}/{img_name}')
        imm = ImageOps.mirror(img).convert('RGB')  # Make mirror image
        imm.save(f'{output_img_path}/{img_name[:-4]}_mirror.jpg', 'jpeg')
        with open(f'{input_txt_path}/{label}', 'r') as txt:
            with open(f'{output_txt_path}/{label[:-4]}_mirror.txt', 'w') as txt_out:
                for lines in txt:
                    line = lines.split(' ')
                    line[1] = str((float(line[1]) - 0.5) * (-1) + 0.5)
                    txt_out.write(' '.join(v for v in line))
                    target_classes[f'Class {line[0]}'] += 1

                    if debug:
                        print(line)
                        print(f'{lines} -> {" ".join(v for v in line)}')
                if debug:
                    print('=' * 100)
                    print('\n')

    print(f'{"=" * 30}Result{"=" * 30}')
    print(f'\n<Class Added>')
    for k, v in target_classes.items():
        print(f'{k}: {v}')

    length = len(str(classes[max(classes, key=classes.get)] * 2))
    print(f'\n<Class Total>')
    for k, v in classes.items():
        print(f'{k}: {f"{v}".ljust(length)} -> {v + (target_classes[k])}')


if __name__ == '__main__':

    debug = False
    num_class = 3  # Put number of class for your dataset
    target_class = [0, 1]  # Put class numbers for apply augmentation
    input_path = 'input_path'
    output_path = 'output_path_mirror'
    input_img_path = f'{input_path}/images'
    input_txt_path = f'{input_path}/labels'
    output_img_path = f'{output_path}/images'
    output_txt_path = f'{output_path}/labels'
    os.makedirs(output_img_path, exist_ok=True)
    os.makedirs(output_txt_path, exist_ok=True)

    mirror()
