import cv2
import os
import numpy as np
import sys

path = 'aaaaa.op'

def main():
    try:
        img = input_img(path)
    except (TypeError, ValueError) as e:
        print(e)
    else:
        print('seijo')
    finally:
        print('syu ryo')
    #print(img)



def input_img(path: str) -> np.ndarray:
    if os.path.isfile(path):
        img = cv2.imread(path)
        if not isinstance(img, np.ndarray):
            raise TypeError(f'\'{path}\' is not an image file')
        else:
            return img
    else:
        raise ValueError(f'Cannot access \'{path}\': No such file or directory')

if __name__ == '__main__':
    main()