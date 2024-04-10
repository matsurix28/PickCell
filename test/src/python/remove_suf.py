import collections
import glob
import os
import re

import cv2


def biggest_img(img_list):
    max_size = 0
    biggest = None
    for image in img_list:
        img = cv2.imread(image)
        size = img.size
        if size > max_size:
            max_size = size
            biggest = image
    return [biggest]

input_path = '.'
exts = ['jpg', 'jpeg', 'png', 'tiff', 'bmp']
exts = sum([[ext.lower(), ext.upper()] for ext in exts], [])

#files = ['1elgo-L.png', '3fgo-L.JPG', '2hf-F.png', '4gnshn-L.png', '1elgo-F.bmp', '3fgo-F.JPG', '4gnshn-F.png', '4gnshn-L.png', '5faiz-L']
files = []
for ext in exts:
    files += glob.glob(input_path + '/*.' + ext)
#print(files)
#for f in files:
#    name = os.path.splitext(f)[0]
#ff = [os.path.splitext(f)[0].rstrip('-L' '-F') for f in files]


ff = [re.sub('-(L|F)$', '', os.path.splitext(f)[0]) for f in files]
a = [k for k, v in collections.Counter(ff).items() if v > 1]

img_list = []

for name in a:
    print(name)
    l = glob.glob(input_path + '/' + name + '-L.*')
    f = glob.glob(input_path + '/' + name + '-F.*')
    #print(l)
    #print(f)
    if (len(l) == 0) or (len(f) == 0):
        #print('break')
        break
    if len(l) > 1:
        #print(l)
        l = biggest_img(l)
    if len(f) > 1:
        #print(f)
        f = biggest_img(f)
    img_list.append([name, l[0], f[0]])

print(img_list)
