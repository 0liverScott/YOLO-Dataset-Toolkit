import os
from tqdm import tqdm

def count():
    classes = {f'Class {v}': 0 for v in range(num_class)}
    for t in tqdm(os.listdir(txt_path)):
        with open(f'{txt_path}/{t}', 'r') as txt:
            for line in txt:
                classes[f'Class {line[0]}'] += 1
    for k, v in classes.items():
        print(f'{k}: {v}')


if __name__ == '__main__':
    path = 'input_path'
    txt_path = f'{path}/labels'
    num_class = 15  # Dataset Number of Classes
    count()
