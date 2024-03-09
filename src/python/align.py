#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-
"""Align the size and tilt of images with each other."""

import argparse
import os
import sys

import cv2
import detect
import numpy as np


def main():
    in1, in2, m1, m2, out = args()
    d = detect.Detect()
    try:
        name1 = get_name(in1)
        name2 = get_name(in2)
        if m1 == 'leaf':
            img1, cnt1 = d.extr_leaf(in1, out)
        elif m1 == 'green':
            img1, cnt1 = d.extr_green(in1, out)
        if m2 == 'leaf':
            img2, cnt2 = d.extr_leaf(in2, out)
        elif m2 == 'green':
            img2, cnt2 = d.extr_green(in2, out)
    except (TypeError, ValueError) as e:
        print(e)
        sys.exit()
    a = Align()
    try:
        img1, img2 = a.run(img1, img2, cnt1, cnt2)
        a.save(img1, name1, out)
        a.save(img2, name2, out)
    except ValueError as e:
        print(e)
        sys.exit()
    
def get_name(path):
    if os.path.isfile(path):
        img_name = os.path.splitext(os.path.basename(path))[0]
        return img_name
    else:
        raise ValueError(f'Cannot access \'{path}\': No such file or directory')

def args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in1', required=True)
    parser.add_argument('--in2', required=True)
    parser.add_argument('--m1', default='leaf', choices=['leaf', 'green'])
    parser.add_argument('--m2', default='leaf', choices=['leaf', 'green'])
    parser.add_argument('-o', '--output', default='./')
    args = parser.parse_args()
    return args.in1, args.in2, args.m1, args.m2, args.output

class Align:
    """Align the size and tilt of images with each other."""

    def __init__(self) -> None:
        pass
    
    def save(self, img, name, output_path):
        output = output_path + name + '_arranged.png'
        cv2.imwrite(output, img)


    def run(self, img1, img2, cnt1, cnt2):
        rotated1, center1, angle1 = self.__tilt(img1, cnt1)
        rotated2, center2, angle2 = self.__tilt(img2, cnt2)
        max_h1, max_w1 = self.__max_size(rotated1)
        max_h2, max_w2 = self.__max_size(rotated2)
        scale = max_h2 / max_h1
        rotated1 = cv2.resize(rotated1, dsize=None, fx=scale, fy=scale)
        _, img_cnts1 = self.__get_cnts(rotated1)
        _, img_cnts2 = self.__get_cnts(rotated2)
        size = [int(max_h2 * 1.2), int(max_w2 * 1.2)]
        try:
            best = self.__best_overlay(img_cnts1, img_cnts2, size)
        except ValueError as e:
            raise
        img1 = self.__rotate(img1, angle1, center1)
        img1 = cv2.resize(img1, dsize=None, fx=scale, fy=scale)
        img1 = cv2.resize(img1, dsize=None, fx=best[1], fy=1)
        img1 = self.__crop(img1, size, best[2])
        img2 = self.__rotate(img2, angle2, center2)
        img2 = self.__crop(img2, size)
        img_overlay = cv2.addWeighted(src1=img1, alpha=1, src2=img2, beta=0.3, gamma=0)
        #cv2.imwrite('test_res.png', img_overlay)
        return img1, img2, img_overlay
        

    def __tilt(self, img, cnts):
        center, _, angle = cv2.fitEllipse(cnts)
        bin = np.zeros(img.shape[:2], np.uint8)
        cv2.drawContours(bin, [cnts], -1, 255, -1)
        rotated = self.__rotate(bin, angle, center)
        return rotated, center, angle

    def __best_overlay(self, img1, img2, size):
        pos_range = int(size[1] / 10)
        img2 = self.__crop(img2, size)
        overlap = []
        for i in range(-20, 21, 1):
            fx = (100 + i) / 100
            resized = cv2.resize(img1, dsize=None, fx=fx, fy=1)
            for pos in range(-pos_range, pos_range, 1):
                img = self.__crop(resized, size, pos)
                if img.shape == img2.shape:
                    img_overlay = cv2.bitwise_and(img, img2)
                    white = np.sum(img_overlay)
                    overlap.append([white, fx, pos])
        if len(overlap) > 0:
            best = max(overlap, key=lambda x: x[0])
        else:
            raise ValueError('Cannot match same size.')
        return best

    def __get_cnts(self, img):
        cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        best_cnts = max(cnts, key=lambda x: cv2.contourArea(x))
        img_cnts = np.zeros(img.shape[:2], np.uint8)
        cv2.drawContours(img_cnts, [best_cnts], -1, 255, 5)
        return best_cnts, img_cnts


    def __max_size(self, img):
        height = (img == 255).sum(axis=0)
        max_height = height.max()
        width = (img == 255).sum(axis=1)
        max_width = width.max()
        return max_height, max_width
    
    def __crop(self, img, size, param=0):
        h, w = img.shape[:2]
        y, x = list(map(lambda x: int(x), size[:2]))
        crop = img[int(h / 2 - y / 2) : int(h / 2 + y / 2), int(w / 2 - x / 2 - param) : int(w / 2 + x / 2 -param)]
        return crop
    
    def __rotate(self, img, angle, center):
        h, w = img.shape[:2]
        corners = np.array([(0,0), (w,0), (w,h), (0,h)])
        radius = np.sqrt(max(np.sum((center - corners) ** 2, axis=1)))
        frame = int(2 * radius)
        trans = cv2.getRotationMatrix2D(center, angle - 90, 1)
        trans[0][2] += radius - center[0]
        trans[1][2] += radius - center[1]
        rotated = cv2.warpAffine(img, trans, (frame, frame))
        return rotated

if __name__ == '__main__':
    main()
