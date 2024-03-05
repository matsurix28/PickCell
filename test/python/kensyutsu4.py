#!/usr/bin/env python3.11
# -*- conding: utf-8 -*-
"""Extract green leaves from an image."""


import cv2
import numpy as np
import os

def main():
    k = Kensyutsu()
    k.

class Kensyutsu:
    """Extract green leaves from an image.
    
    Extract green leaves from an image, and detect each leaf size 
    and tilt.
    
    Attributes:
        resize (:obj:`int`): Image size after resizing. Defaults to 1000.
        canny_thr1 (:obj:`int`): Canny threshold1. Defaults to 100.
        canny_thr2 (:obj:`int`): Canny threshold2. Defaults to 200.
        bin_thr (:obj:`float`): Threshold of binarization. Defaults to 60.
        bin_max (:obj:`float`): Max value of binarization. Defaults to 255.
        min_area (:obj:`int`): Minimun leaf area as a fraction of the 
            image. Defaults to 100.
        hsv_min (:obj:`numpy.ndarray[int]`): Minimum HSV value of green.
            Defaults to [30, 50, 50].
        hsv_max (:obj:`numpy.ndarray[int]`): Maximum HSV value of green. 
            Defaults to [90, 255, 200].
        blur (:obj:`tuple`): Kernel size of blur (width, height). 
            Defaults to (5,5)
    """
    def __init__(self):
        self.__set_default()

    def __set_default(self) -> None:
        """Set default value to each parameter."""
        self.__resize = 1000
        self.canny_thr1 = 100
        self.canny_thr2 = 200
        self.bin_thr = 60
        self.bin_max = 255
        self.min_area = 100
        self.hsv_min = np.array([30,50,50])
        self.hsv_max = np.array([90,255,200])
        self.blur = (5,5)

    def set_param(self,
                  resize=1000,
                  canny_thr1=100,
                  canny_thr2=200,
                  bin_thr=60,
                  bin_max=255,
                  min_area=100,
                  hsv_min=[30,50,50],
                  hsv_max=[90,255,200],
                  blur=(5,5)
                  ) -> None:
        """Set value to each parameter.
        
        Args:
            resize (:obj:`int`, optional): Image size after resizing. 
                Defaults to 1000.
            canny_thr1 (:obj:`int`, optional): Canny threshold1. 
                Defaults to 100.
            canny_thr2 (:obj:`int`, optional): Canny threshold2. 
                Defaults to 200.
            bin_thr (:obj:`float`, optional): Threshold of binarization. 
                Defaults to 60.
            bin_max (:obj:`float`, optional): Max value of binarization. 
                Defaults to 255.
            min_area (:obj:`int`, optional): Minimun leaf area 
                as a fraction of the image. Defaults to 100.
            hsv_min (:obj:`list[int]`, optional): Minimum HSV value of 
                green. Defaults to [30, 50, 50].
            hsv_max (:obj:`list[int]`, optional): Maximum HSV value of 
                green. Defaults to [90, 255, 200].
            blur (:obj:`tuple`): Kernel size of blur (width, height).
                Defaults to (5,5).

        Returns:
            None
        """
        self.__resize = resize
        self.canny_thr1 = canny_thr1
        self.canny_thr2 = canny_thr2
        self.bin_thr = bin_thr
        self.bin_max = bin_max
        self.min_area = min_area
        self.hsv_min = np.array(hsv_min)
        self.hsv_max = np.array(hsv_max)
        self.blur = blur

    def __save(self, img: np.ndarray, name: str, ext='.png') -> None:
        """Save as image file.
        
        Args:
            img (:obj:`numpy.ndarray`): Image to save
            name (:obj:`str`): File name without extension
            ext (:obj:`str`, optional): File extension. 
                Defaults to '.png'
        
        Returns:
            None
        """
        output = self.output_path + self.img_name + '_' + name + ext
        cv2.imwrite(output, img)

    def __resize(self, 
               img: np.ndarray, name: str = '', 
               ext='.png', export: bool = False
               ) -> np.ndarray:
        """Resize image.
        
        Args:
            img (:obj:`numpy.ndarray`): Input image.
            name (:obj:`str`, optional): Sample name. This name is used 
                when saving as an image. Defaults to ''.
                (e.g. name='sample1', file name is 
                'SOURCE_sample1-resized.png')
            ext (:obj:`str`, optional): File extension. 
                Defaults to '.png'
            export (:onj:`bool`, optional): Save as image or not. 
                Defaults to False.

        Returns:
            numpy.ndarray: Resized image.
        """
        scale = self.__resize / img.shape[1]
        img_resized = cv2.resize(img, None, fx=scale, fy=scale)
        if export:
            if name == '':
                tag = '-'
            else:
                tag = ''
            self.__save(img_resized, name + tag + 'resized', ext)
        return img_resized
    
    def __split_hsv(self, 
                  img: np.ndarray, name: str = '', 
                  ext='.png', export: bool = False
                  ) -> tuple[np.ndarray, ...]:
        """Split image into Hue, Saturation, Value.

        Args
            img (:obj:`numpy.ndarray`): Input image.
            name (:obj:`str`, optional): Sample name. This name is used 
                when saving as an image. Defaults to ''.
                (e.g. name='sample1', file name is 
                'SOURCE_sample1-resized.png')
            ext (:obj:`str`, optional): File extension. 
                Defaults to '.png'
            export (:onj:`bool`, optional): Save as image or not. 
                Defaults to False.

        Returns:
            numpy.ndarray: Hue-only image.
            numpy.ndarray: Saturation-only image.
            numpy.ndarray: Value-only image.
        """
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_h, img_s, img_v = cv2.split(img_hsv)
        if export:
            if name == '':
                tag = ''
            else:
                tag = '-'
            self.__save(img_h, name + tag + 'H', ext)
            self.__save(img_s, name + tag + 'S', ext)
            self.__save(img_v, name + tag + 'V', ext)
        return img_h, img_s, img_v
    
    def __canny(self, 
              img: np.ndarray, name: str = '',
              ext='.png', export: bool = False
              ) -> np.ndarray:
        """Detect edge.
        
        Args:
            img (:obj:`numpy.ndarray`): Input gray scale image.
            name (:obj:`str`, optional): Sample name. This name is 
                used when saving as an image. Defaults to ''.
                (e.g. name='sample1', file name is 
                'SOURCE_sample1-resized.png')
            ext (:obj:`str`, optional): File extension. 
                Defaults to '.png'
            export (:onj:`bool`, optional): Save as image or not. 
                Defaults to False.

        Returns:
            numpy.ndarray: Edge image.
        """
        img_canny = cv2.Canny(img, self.canny_thr1, self.canny_thr2)
        if export:
            if name == '':
                tag = 'canny'
            else:
                tag = '-canny'
            self.__save(img_canny, name + tag, ext)
        return img_canny
    
    def __bin(self, 
            img: np.ndarray, name: str = '',
            ext='.png', export: bool = False
            ) -> np.ndarray:
        """Binarization.
        
        Args:
            img (:obj:`numpy.ndarray`): Input gray scale image.
            name (:obj:`str`, optional): Sample name. This name is used 
                when saving as an image. Defaults to ''.
                (e.g. name='sample1', file name is 
                'SOURCE_sample1-resized.png')
            ext (:obj:`str`, optional): File extension. 
                Defaults to '.png'
            export (:onj:`bool`, optional): Save as image or not. 
                Defaults to False.

        Returns:
            numpy.ndarray: Binary image.
        """
        _, img_bin = cv2.threshold(img, self.bin_thr, self.bin_max, 
                                   cv2.THRESH_BINARY)
        if export:
            if name == '':
                tag = 'bin'
            else:
                tag = '-bin'
            self.__save(img_bin, name + tag, ext)
        return img_bin
    
    def __get_cnts(self, img: np.ndarray) -> list:
        """Find contours with an area larger than the set value.
        
        Args:
            img (:obj:`numpy.ndarray`): Input binary image.

        Returns:
            list: Contours with an area larger than the set value.
        """
        cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, 
                                   cv2.CHAIN_APPROX_SIMPLE)
        height, width = img.shape[:2]
        min_area = height * width / self.min_area
        cnts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, cnts))
        return cnts_list
    
    def __assess_noise(self, img: np.ndarray) -> int:
        """Assess noise of image.
        
        Args:
            img (:obj:`numpy.ndarray`): Input binary image.

        Returns:
            int: Number of noise.
        """
        img_canny = cv2.Canny(img, self.canny_thr1, self.canny_thr2)
        cnts, _ = cv2.findContours(img_canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        height, width = img.shape[:2]
        min_area = height * width / 1000
        cnts_list = list(filter(lambda x: cv2.contourArea(x) < min_area, cnts))
        return len(cnts_list)
    
    def __assess_area(self, img: np.ndarray, cnts: tuple) -> bool:
        """Whether the area of the region is larger than the standard value.
        
        Args:
            img (:obj:`numpy.ndarray`): Input image.
            cnts (:obj:`numpy.ndarray`): List of contours.

        Returns:
            bool: Returns True if list contains an area larger than 
                the standared value.
        """
        height, width = img.shape[:2]
        min_area = height * width / self.min_area
        larger_cnts = list(filter(lambda x: cv2.contourArea(x) > min_area, cnts))
        return len(larger_cnts) > 0
    
    def __get_green_area(self, img: np.ndarray) -> int:
        """Get the area of green region.
        
        Args:
            img (:obj:`numpy.ndarray`): Input color image.

        Returns:
            int: Number of pixels in green area.
        """
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask_hsv = cv2.inRange(img_hsv, self.hsv_min, self.hsv_max)
        px_sum = np.sum(mask_hsv)
        px_white = int(px_sum / 255)
        return px_white
    
    def __get_green_ratio(self, img: np.ndarray, cnts: np.ndarray
                        ) -> tuple[np.ndarray, np.ndarray]:
        """Calcurate the percentage of green area in the region.
        
        Args:
            img (:obj:`numpy.ndarray`): Input color image.
            cnts (:obj:`numpy.ndarray`): Area contour.

        Returns:
            numpy.ndarray: Masked image.
            numpy.ndarray: Percentage of green area in the region.
        """
        height, width = img.shape[:2]
        mask = np.zeros((height, width, 3), np.uint8)
        cv2.drawContours(mask, [cnts], -1, (255,255,255), -1)
        region = cv2.bitwise_and(img, mask)
        green_area = self.__get_green_area(region)
        region_area = cv2.contourArea(cnts)
        green_ratio = green_area / region_area * 100
        return region, green_ratio
    
    def __best_hsv(self, img: np.ndarray) -> list:
        img_h, img_s, img_v = self.__split_hsv(img)
        hsv_list = [img_h, img_s, img_v]
        result = []
        for image in hsv_list:
            bin = self.__bin(image)
            noise = self.__assess_noise(bin)
            result.append([noise, image])
        result.sort(key=lambda x: x[0])
        return result
    
    def extr_green_leaves(self, img_path):
        img = cv2.imread(img_path)
        h, s, v = self.__split_hsv(img)

    def extr_fvfm(self):
        pass

    def extr_others(self):
        pass

if __name__ == '__main__':
    main()