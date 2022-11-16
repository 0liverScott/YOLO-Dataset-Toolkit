import os
import datetime

def result(dup):
    if dup:
        with open(f'dup_{date}.txt', 'w') as log:
            for file in dup:
                print(file)
                log.write(file)
        print(f'\n{len(dup)} file is dup.')
    else:
        print('There is no duplication')

def include_format():
    dup = list(set(path1_list) & set(path2_list))
    if dup:
        result(dup)

def without_format():
    path1_list2 = []
    path2_list2 = []
    for file in path1_list:
        path1_list2.append(file[:-4])
    for file in path2_list:
        path2_list2.append(file[:-4])
    dup = list(set(path1_list2) & set(path2_list2))
    if dup:
        result(dup)


if __name__ == '__main__':
    date = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    # Compare path1 and path2
    path1 = r'input_path/images'
    path2 = r'input_path/images'
    path1_list = os.listdir(path1)
    path2_list = os.listdir(path2)

    num = int(input("""1.Include format\n2.Without format\n"""))
    if num == 1:
        include_format()  # Doesn't pick filename is same but file format is different
    elif num == 2:
        without_format()  # No matter what is file format, pick a same filename.
    else:
        print('Wrong input.')
