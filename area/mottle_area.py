import csv
import glob
import os
import tkinter
from tkinter import filedialog

import cv2
import numpy as np


# 葉全体の輪郭検出
def find_conts(path_img):
    img = cv2.imread(path_img)
    area = 0
    # グレースケール、二値化、反転
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY)[1]
    re_thresh = cv2.bitwise_not(thresh)

    # 輪郭検出
    conts = cv2.findContours(re_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    conts_list = list(filter(lambda x: cv2.contourArea(x) > 1000, conts))

    # 輪郭が1つ
    if len(conts_list) == 1:
        # 面積
        area = cv2.contourArea(conts_list[0])
        # 輪郭描画
        cv2.drawContours(img, conts_list, 0, color=(255,0,0), thickness=5)
    # 輪郭0
    elif len(conts_list) == 0:
        print('輪郭を検出できませんでした。')
        exit
    # それ以外
    else:
        area_list = []
        for i, cnt in enumerate(conts_list):
            area_list.append(cv2.contourArea(cnt))
        # 面積が最大のもの
        area = max(area_list)
        max_ind = area_list.index(area)
        cv2.drawContours(img, conts_list, max_ind, color=(255,0,0), thickness=5)
        
    return img, area, re_thresh    # 輪郭描画画像、葉全体面積


# 緑色部の面積測定
def measure_mottle(path_img, image, thresh):
    img_file = os.path.basename(path_img)
    img_name = os.path.splitext(img_file)[0]

    # 画像の読み込み
    img = cv2.imread(path_img)
    img_leaf = cv2.bitwise_and(img, img, mask=thresh)
    cv2.imwrite('leaf.jpeg', img_leaf)

    # HSV化
    img_hsv = cv2.cvtColor(img_leaf, cv2.COLOR_BGR2HSV_FULL)

    lower = np.array([55,0,0])          # HSV下限
    upper = np.array([135,255,255])     # HSV上限

    lower_lightGreen = np.array([65,0,0])
    upper_lightGreen = np.array([120, 255,255])

    lower_light = np.array([])
    upper_light = np.array([])

    # 範囲抽出
    bin_green = cv2.inRange(img_hsv, lower, upper)
    area = cv2.countNonZero(bin_green)
    

    # 緑色部の輪郭検出
    img_green = cv2.bitwise_and(img, img, mask=bin_green)
    green_name = img_name + '_green.jpeg'
    cv2.imwrite(green_name, img_green)
    conts = cv2.findContours(bin_green, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    cv2.drawContours(image, conts, -1, color=(0,0,255), thickness=3)
    
    return image, area    # 輪郭描画画像、緑面積

def calc(folder_path):
    
    files = glob.glob("./*JPG")
    res_dir = folder_path + '/Result'
    os.mkdir(res_dir)

    all_data = []
    column_title = ['葉ID', '全面積', '緑色部分面積', '斑面積', '斑入り率']
    all_data.append(column_title)
    
    for file in files:
        img_file = os.path.basename(file)
        img_name = os.path.splitext(img_file)[0]
        img, whole_area, thresh = find_conts(img_file)
        img, green_area = measure_mottle(img_file, img, thresh)
        mottle_area = whole_area - green_area
        if mottle_area < 0:
            mottle_area = str(mottle_area) + ' (Error)'
            green_area = str(green_area) + ' (Error)'
        
        if type(mottle_area) == str:
            ratio_mottle = '-'
        else:
            ratio_mottle = mottle_area / whole_area * 100

        data = [img_name, whole_area, green_area, mottle_area, ratio_mottle]
        all_data.append(data)
        result_name = img_name + '_area.JPG'
        result_file = res_dir + '/' + result_name
        cv2.imwrite(result_file, img)
    
    return all_data


def disp():
    global folder_path
    def btn_select_click():
        global folder_path
        folder_path = tkinter.filedialog.askdirectory()
        txt.delete(0, tkinter.END)
        txt.insert(tkinter.END, folder_path)

    def btn_enter_click():
        global folder_path
        os.chdir(folder_path)
        data = calc(folder_path)
        f = open('mottle_area.csv', 'w', newline='')
        writer = csv.writer(f)
        writer.writerows(data)
        f.close
        root.destroy()
        

    # 画面の作成
    root = tkinter.Tk()
    root.geometry('300x100')
    root.title('葉の斑面積測定')

    # フレームの作成
    main_frm = tkinter.Frame(root)
    main_frm.grid(column=0, row=0, sticky=tkinter.NSEW, padx=5, pady=5)

    #ラベル
    lbl = tkinter.Label(main_frm, text='画像フォルダ')

    # テキストボックス
    txt = tkinter.Entry(main_frm)

    # ボタン
    btn_select = tkinter.Button(main_frm, text='▼', command=btn_select_click)
    btn_enter = tkinter.Button(main_frm, text='実行', command=btn_enter_click)

    # 配置
    lbl.grid(column=0, row=0)
    txt.grid(column=1, row=0, sticky=tkinter.EW, padx=5)
    btn_select.grid(column=2, row=0)
    btn_enter.grid(column=1, row=1)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_frm.columnconfigure(1, weight=1)

    root.mainloop()

if __name__ == '__main__':
    disp()