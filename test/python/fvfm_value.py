import cv2
import easyocr
import re
import itertools
import statistics
import math

def main():
    img = cv2.imread('bar.bmp')
    bar = get_scale_area(img)
    fvfm, scale = yomitori('bar.bmp')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    fvfm_list = create_fvfmlist(fvfm[0], scale, bar, h)
    for f in fvfm_list:
        print(f)
    #aida = fvfm[0][0] - y
    #aida_kazu = int(aida / scale)
    #top = fvfm[0][1] + 1 * aida_kazu

    #aida_sita = y+ h -fvfm[0][0]
    #sita_kazu = int(aida_sita / scale)
    #bottom = fvfm[0][1] - 1 * sita_kazu

def create_fvfmlist(std_fvfm, scale, bar, img):
    top = bar[1]
    bottom = bar[1] + bar[2]
    center = int(bar[0] + (bar[3] / 2))
    upper_num = int((std_fvfm[0] - top) / scale)
    lower_num = int((bottom - std_fvfm[0]) / scale)
    fvfm_list = []
    for i in range(1, upper_num + 1):
        fvfm = std_fvfm[1] + i
        pos = int(std_fvfm[0] - (i * scale))
        value = img[pos, center]
        fvfm_list.append([value, fvfm])
    for i in range(1, lower_num + 1):
        fvfm = std_fvfm[1] - i
        pos = int(std_fvfm[0] + (i * scale))
        value = img[pos, center]
        fvfm_list.append([value, fvfm])
    return fvfm_list

def yomitori(img_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(img_path)
    fvfm_value = []
    for res in result:
        if re.compile("0(\.|,)\d{2}$").match(res[1]):
            pos = (res[0][3][1] - res[0][0][1]) / 2 + res[0][0][1]
            fvfm_value.append([pos, float((res[1].replace(',', '.'))) * 1000])
    if len(fvfm_value) >= 2:
        fvfm_value.sort(key=lambda x: x[0])
        scale = keisan(fvfm_value)
        print('first position', fvfm_value[0])
        print(scale)
        return fvfm_value, scale
    else:
        print('Yomitori Sippai')

def keisan(fvfm):
    value_list = []
    for pair in itertools.combinations(fvfm, 2):
        v1 = pair[0][1]
        v2 = pair[1][1]
        h1 = pair[0][0]
        h2 = pair[1][0]

        if h2 > h1:
            v_def = v1 - v2
            h_def = h2 - h1
            scale = h_def / v_def
            value_list.append(scale)
    scale = statistics.median(value_list)
    return scale

def get_scale_area(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY_INV)
    cnts_list, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_list = list(filter(lambda x: cv2.contourArea(x) > 500, cnts_list))
    img_height = img.shape[0]
    bar = []
    for cnts in cnts_list:
        x,y,w,h = cv2.boundingRect(cnts)
        print(y, h, img_height)
        if check_bar(h, w, img_height):
           bar = [x, y, h, w]
           break
    if bar == []:
        print('No Bar')
        exit
    return bar
    

def check_bar(h,w,ih):
    hi = h / w
    if hi > 0.7:
        tate = True
    else:
        tate = False
    img_hi = h / ih
    if img_hi > 0.8:
        img_tate = True
    else:
        img_tate = False
    if tate and img_tate:
        print('koreha bar')
        return True
    else:
        print('Kore ha Bar jane')
        return False

if __name__ == '__main__':
    main()
