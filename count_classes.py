import os
from tqdm import tqdm
from collections import defaultdict

def count():
    classes = defaultdict(int)
    nums = set()
    for t in tqdm(os.listdir(txt_path)):
        with open(f'{txt_path}/{t}', 'r') as txt:
            for line in txt:
                classes['Class ' f'{line[0].zfill(3)}'] += 1
                nums.add(int(line[0]))
    for n in range(max(nums)):
        if n not in nums:
            classes['Class ' f'{str(n).zfill(3)}'] = 0
    for k, v in sorted(classes.items()):
        print(f'{k}: {v}')


if __name__ == '__main__':
    path = 'input_path'
    txt_path = f'{path}/labels'

    count()
