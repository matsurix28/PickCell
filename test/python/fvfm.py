#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""Read Fv/Fm scale bar."""

import argparse
import itertools
import os
import re
import statistics
import sys

import cv2
import easyocr
import numpy as np


def main():
    input_path, output_path = args()
    fvfm = Fvfm()
    try:
        fvfm_list = fvfm.get(input_path, output_path)
    except (TypeError, ValueError) as e:
        print(e)
        sys.exit()

def test():
    #input_path, output_path = args()
    img = 'test/output/daen/bar.bmp'
    fvfm = Fvfm()
    try:
        fvfm_list = fvfm.get(img, './')
    except (TypeError, ValueError) as e:
        print(e)
        sys.exit()
    print(fvfm_list)

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-o', '--output', default='./')
    args = parser.parse_args()
    return args.input, args.output

class Fvfm:
    """Read Fv/Fm scale bar."""

    def __init__(self):
        self.__set_default()
        self.reader = easyocr.Reader(['en'])

    def __set_default(self):
        self.bin_thr = 230
        self.bar_area = 500

    def set_param(self,
                  bin_thr=230,
                  bar_area=500
                  ):
        self.bin_thr = bin_thr
        self.bar_area = bar_area

    def __read(self, img_path: str):
        text = self.reader.readtext(img_path)
        fvfm_list = []
        for value in text:
            if re.compile("0(\.|,)\d{2}$").match(value[1]):
                pos = (value[0][3][1] - value[0][0][1]) / 2 + value[0][0][1]
                fvfm_list.append([pos, float((value[1].replace(',', '.'))) * 1000])
        if len(fvfm_list) >= 2:
            fvfm_list.sort(key=lambda x: x[0])
            try:
                scale = self.__calculate(fvfm_list)
                return fvfm_list[0], scale
            except ValueError as e:
                raise
        else:
            raise ValueError('Cannot read Fv/Fm value.')

    def __calculate(self, fvfm_list):
        scale_list = []
        for pair in itertools.combinations(fvfm_list, 2):
            val_diff = np.abs(pair[0][1] - pair[1][1])
            pos_diff = np.abs(pair[1][0] - pair[0][0])
            scale = pos_diff / val_diff
            scale_list.append(scale)
        if len(scale_list) > 0:
            scale = statistics.median(scale_list)
            return scale
        else:
            raise ValueError('Cannot read Fv/Fm value.')
            
    def __get_area(self, img: np.ndarray):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, bin = cv2.threshold(gray, self.bin_thr, 255, cv2.THRESH_BINARY_INV)
        cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = list(filter(lambda x: cv2.contourArea(x) > self.bar_area, cnts))
        height = img.shape[0]
        bar = []
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            if self.__check_bar(h, w, height):
                bar = [x, y, h, w]
                break
        if bar == []:
            raise ValueError('No scale bar was detected.')
        else:
            return bar

    def __check_bar(self, height, width, img_height):
        ratio = height / width
        dominance = height / img_height
        if (ratio > 0.7) and (dominance > 0.8):
            return True
        else:
            return False

    def get(self, input_path: str, output_path=None):
        try:
            img = self.__input_img(input_path)
        except (TypeError, ValueError) as e:
            raise
        try:
            bar_area = self.__get_area(img)
        except (ValueError) as e:
            raise
        try:
            std_fvfm, scale = self.__read(input_path)
        except ValueError as e:
            raise
        try:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
            h,s,v = cv2.split(hsv)
            fvfm_list = self.__create_fvfm_list(std_fvfm, scale, bar_area, img)
        except ValueError as e:
            raise
        if output_path is not None:
            output = output_path + self.img_name + '_FvFmList.txt'
            f = open(output, 'w')
            for fvfm in fvfm_list:
                f.write(str(fvfm) + '\n')
            f.close()
        return fvfm_list

    def __create_fvfm_list(self, std_fvfm, scale, bar_area, img):
        top = bar_area[1]
        bottom = bar_area[1] + bar_area[2]
        center = int(bar_area[0] + (bar_area[3] / 2))
        upper_num = int((std_fvfm[0] - top) / scale)
        lower_num = int((bottom - std_fvfm[0]) / scale)
        fvfm_list = []
        for i in range(1, upper_num + 1):
            fvfm = std_fvfm[1] + i
            pos = int(std_fvfm[0] - (i * scale))
            value = img[pos, center]
            print(value)
            fvfm_list.append([value.tolist(), fvfm])
        for i in range(1, lower_num + 1):
            fvfm = std_fvfm[1] - i
            pos = int(std_fvfm[0] + (i * scale))
            value = img[pos, center]
            fvfm_list.append([value.tolist(), fvfm])
        if len(fvfm_list) > 0:
            fvfm_list.sort(key=lambda x: x[1], reverse=True)
            return fvfm_list
        else:
            raise ValueError('Cannot calculate Fv/Fm value.')

    def __input_img(self, path: str) -> np.ndarray:
        if os.path.isfile(path):
            img = cv2.imread(path)
            if not isinstance(img, np.ndarray):
                raise TypeError(f'\'{path}\' is not an image file')
            else:
                self.img_name = os.path.splitext(os.path.basename(path))[0]
                return img
        else:
            raise ValueError(f'Cannot access \'{path}\': No such file or directory')

if __name__ == '__main__':
    #main()
    test()
