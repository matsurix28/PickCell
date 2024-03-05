#!/usr/bin/env python3.11
# -*- coding: utf-8 -*-

import argparse
import os
from multiprocessing import Pool

import cv2
import numpy as np


def main():
    p = Pickcell()
    img1 = cv2.imread('test/output/daen/1_arranged.png')
    img2 = cv2.imread('test/output/daen/6_arranged.png')
    fvfm = [[[  0,  74, 255], 831.0],[[  0,  64, 255], 832.0],[[  0,  53, 255], 833.0],[[  0,  43, 255], 834.0],[[  0,  33, 255], 835.0],[[  0,  21, 255], 836.0],[[  0,  11, 255], 837.0],[[  0,   1, 255], 838.0],[[  0,  95, 255], 829.0],[[  0, 105, 255], 828.0],[[  0, 117, 255], 827.0],[[  0, 127, 255], 826.0],[[  0, 136, 255], 825.0],[[  0, 148, 255], 824.0],[[  0, 158, 255], 823.0],[[  0, 168, 255], 822.0],[[  0, 179, 255], 821.0],[[  0, 189, 255], 820.0],[[  0, 199, 255], 819.0],[[  0, 210, 255], 818.0],[[  0, 220, 255], 817.0],[[  0, 231, 255], 816.0],[[  0, 241, 255], 815.0],[[  0, 251, 255], 814.0],[[  0, 255, 241], 813.0],[[  0, 255, 221], 812.0],[[  0, 255, 201], 811.0],[[  0, 255, 179], 810.0],[[  0, 255, 159], 809.0],[[  0, 255, 139], 808.0],[[  0, 255, 116], 807.0],[[  0, 255,  96], 806.0],[[  0, 255,  74], 805.0],[[  0, 255,  54], 804.0],[[  0, 255,  34], 803.0],[[  0, 255,  11], 802.0],[[  9, 255,   4], 801.0],[[ 28, 255,  14], 800.0],[[ 51, 255,  26], 799.0],[[ 71, 255,  36], 798.0],[[ 91, 255,  46], 797.0],[[113, 255,  57], 796.0],[[133, 255,  67], 795.0],[[156, 255,  78], 794.0],[[176, 255,  88], 793.0],[[195, 255,  98], 792.0],[[218, 255, 110], 791.0],[[238, 255, 119], 790.0],[[255, 252, 127], 789.0],[[255, 229, 115], 788.0],[[255, 210, 105], 787.0],[[255, 190,  95], 786.0],[[255, 167,  84], 785.0],[[255, 147,  74], 784.0],[[255, 125,  63], 783.0],[[255, 105,  53], 782.0],[[255,  85,  43], 781.0],[[255,  62,  31], 780.0],[[255,  42,  21], 779.0],[[255,  23,  11], 778.0],[[255,   0,   0], 777.0],[[235,   0,   0], 776.0],[[215,   0,   0], 775.0],[[193,   0,   0], 774.0],[[173,   0,   0], 773.0],[[150,   0,   0], 772.0],[[130,   0,   0], 771.0],[[111,   0,   0], 770.0],[[88,  0,  0], 769.0],[[68,  0,  0], 768.0],[[48,  0,  0], 767.0],[[25,  0,  0], 766.0],[[6, 0, 0], 765.0]]
    try:
        p.run(img1, img2, fvfm)
    except (ValueError, TypeError) as e:
        print(e)
    #print(type(res))

def args():
    parser = argparse.ArgumentParser()

class Pickcell:
    def __init__(self) -> None:
        self.num_cpu = os.cpu_count()

    def run(self, img_leaf, img_fvfm, fvfm_list):
        try:
            img_leaf = self.__input(img_leaf)
            img_fvfm = self.__input(img_fvfm)
            self.__set(fvfm_list)
        except (TypeError, ValueError) as e:
            raise
        if img_leaf.shape != img_fvfm.shape:
            raise ValueError('Size differs in the two images.')
        img_leaf = self.__reshape_bgr(img_leaf)
        img_fvfm = self.__reshape_bgr(img_fvfm)
        img_leaf = np.array_split(img_leaf, self.num_cpu, axis=0)
        img_fvfm = np.array_split(img_fvfm, self.num_cpu, axis=0) 
        px_list = []
        for i in range(self.num_cpu):
            px_list.append([img_leaf[i], img_fvfm[i]])
        with Pool(self.num_cpu) as p:
            result = p.map(self.pick_wrap, px_list)
        res_px = []
        res_fvfm = []
        for i in range(len(result)):
            res_px.extend(result[i][0])
            res_fvfm.extend(result[i][1])
        return res_px, res_fvfm

    def __pick(self, img_leaf, img_fvfm):
        px = []
        fvfm = []
        length = img_leaf.shape[0]
        for i in range(length):
            if not ((img_leaf[i].sum() <= 50) or (img_fvfm[i].sum() == 0)):
                idx = np.abs(self.color - img_fvfm[i]).sum(axis=1).argmin()
                #result.append([img_leaf[i], self.value[idx]])
                px.append(img_leaf[i].tolist())
                #hue.append(img_hue[i])
                fvfm.append(self.value[idx])
        return px,fvfm
    
    def pick_wrap(self, args):
        px, fvfm = self.__pick(*args)
        return px, fvfm
    
    def __input(self, input):
        if type(input) == str:
            if os.path.isfile(input):
                img = cv2.imread(input)
                if not isinstance(img, np.ndarray):
                    raise TypeError(f'\'{input}\' is not an image file.')
                return img
            else:
                raise ValueError(f'Cannot access \'{input}\': No such file or directory.')
        elif type(input) == np.ndarray:
            if (input.ndim == 3) and (input.shape[2] == 3):
                return input
            else:
                raise ValueError('Can read only RGB image.')
        else:
            raise TypeError('Can read only image.')
    
    def __reshape_bgr(self, img):
        h, w = img.shape[:2]
        length = h * w 
        return img.reshape(length, 3)

    def __reshape_hue(self, img):
        h, w = img.shape[:2]
        length = h * w
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
        h, _, _ = cv2.split(hsv)
        return h.reshape(length)

    def __set(self, fvfm_list):
        self.color = np.array([a[0] for a in fvfm_list])
        self.value = [a[1] for a in fvfm_list]

if __name__ == '__main__':
    main()
