import cv2
import numpy as np
import os
from functools import singledispatch

def main():
    ken = Kensyutsu()
    ken.set_param(bin_thr=80)
    ken.detect('./test/img/naname.JPG', './test/output/ken', save_files=["canny", "bin"])

class Kensyutsu:
    def __init__(self) -> None:
        self.set_default()

    def set_default(self) -> None:
        self.size = 1000
        self.canny_thr1 = 100
        self.canny_thr2 = 200
        self.bin_thr = 100
        self.bin_max = 255
        self.min_area = 100
        self.hsv_min = np.array([30,50,50])
        self.hsv_max = np.array([90,255,200])

    def set_param(self,
                  size=1000,
                  canny_thr1=100,
                  canny_thr2=200,
                  bin_thr=100,
                  bin_max=255,
                  min_area=100,
                  hsv_min=[30,50,50],
                  hsv_max=[90,255,200]
                  )-> None:
        self.size = size
        self.canny_thr1 = canny_thr1
        self.canny_thr2 = canny_thr2
        self.bin_thr = bin_thr
        self.bin_max = bin_max
        self.min_area = min_area
        self.hsv_min = np.array(hsv_min)
        self.hsv_max = np.array(hsv_max)

    def detect(self,
               input_path: str, 
               output_path=None, 
               resize=False, 
               save_files=[]
               ) -> None:
        # Set Input and Outpu
        img = cv2.imread(input_path)
        self.img_name = os.path.splitext(os.path.basename(input_path))[0]
        if output_path is None:
            self.output_path = "./"
        else:
            self.output_path = output_path + "/"
        self.save_files = save_files
        
        # Get size
        if resize:
            img = self.resize(img)
        height, width = img.shape[:2]
        

        # Detection
        best_hsv_list = self.best_hsv(img)
        cnts_list = self.get_cnts(best_hsv_list[0][1])
        self.save(best_hsv_list[0][1], 'best.png')
        self.extract_leaf(img, cnts_list)

    def save(self, img: np.ndarray, name: str, ext=".png") -> None:
        output = self.output_path + self.img_name + "_" + name + ext
        cv2.imwrite(output, img)

    def resize(self, img: np.ndarray, name: str = None, ext=".png"
               ) -> np.ndarray:
        scale = self.size / img.shape[1]
        img_resized = cv2.resize(img, dsize=None, fx=scale, fy=scale)
        if "resize" in self.save_files:
            if name is not None:
                tag = "-"
            else:
                tag = ""
            self.save(img_resized, name + tag + "resized", ext=ext)
        return img_resized
    
    def split_hsv(self, img: np.ndarray, name: str = None, ext=".png"
                  ) -> tuple[np.ndarray, ...]:
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_h, img_s, img_v = cv2.split(img_hsv)
        if "hsv" in self.save_files:
            if name is not None:
                tag = "-"
            else:
                tag = ""
            self.save(img_h, name + tag + "h")
            self.save(img_s, name + tag + "s")
            self.save(img_v, name + tag + "v")
        return img_h, img_s, img_v

    def canny(self, img: np.ndarray, name: str = None, ext=".png"
              ) -> np.ndarray:
        img_canny = cv2.Canny(img, self.canny_thr1, self.canny_thr2, )
        if "canny" in self.save_files:
            if name is not None:
                tag = "-canny"
            else:
                tag = "canny"
            self.save(img_canny, name + tag, ext=ext)
        return img_canny
    
    def bin(self, img: np.ndarray, name: str = None, ext=".png") -> np.ndarray:
        _, img_bin = cv2.threshold(img, self.bin_thr, self.bin_max, cv2.THRESH_BINARY)
        if "bin" in self.save_files:
            if name is not None:
                tag = "-bin"
            else:
                tag = "bin"
            self.save(img_bin, name + tag, ext=ext)
        return img_bin
    
    def best_hsv(self, img: np.ndarray) -> list[float, np.ndarray, str]:
        img_h, img_s, img_v = self.split_hsv(img)
        hsv_list = [[img_h, "h"], [img_s, "s"], [img_v, "v"]]
        self.save(img_v, "v")
        best_hsv_list = []
        for image in hsv_list:
            img_canny = self.canny(image[0], name=image[1])
            img_bin = self.bin(img_canny, image[1])
            img_or = cv2.bitwise_or(image[0], img_bin)
            self.save(img_or, "or" + image[1])
            img_masked = self.bin(img_or, image[1] + "-maseked")
            pixel_num = np.size(img)
            pixel_sum = np.sum(img_masked)
            white_px = pixel_sum / 255
            w_ratio = white_px / pixel_num
            
            best_hsv_list.append([w_ratio, img_masked, image[1]])
        best_hsv_list.sort(key=lambda x: x[0])
        return best_hsv_list
    
    def get_cnts(self, bin: np.ndarray):
        cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        height, width = bin.shape[:2]
        min_area = height * width / self.min_area
        cnts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, cnts))
        #cv2.drawContours(img, cnts_list, -1, (0,0,255), 5)
        #if "contours" in self.save_files:
        #    if name is not None:
        #        tag = "-cnt"
        #    else:
        #        tag = "cnt"
        #    self.save(img, name + tag)
        return cnts_list
    
    def get_green(self, img: np.ndarray) -> tuple[np.ndarray, int]:
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask_hsv = cv2.inRange(img_hsv, self.hsv_min, self.hsv_max)
        print(img_hsv.shape)
        px_num = np.size(mask_hsv)
        px_sum = np.sum(mask_hsv)
        px_white = int(px_sum / 255)
        green_ratio = px_white / px_num
        print('px num: ', px_num)
        print('px sum: ', px_sum)
        print('px white: ', px_white)
        print('green ratio: ', green_ratio)
        return mask_hsv, px_white
    
    def check_green_area(self, img: np.ndarray, cnts_list: list) -> list:
        height, width = img.shape[:2]
        areas_list = []
        for i, cnts in enumerate(cnts_list):
            blank = np.zeros((height, width), np.uint8)
            mask = cv2.drawContours(blank, [cnts], 0, 255, -1)
            img_base = img.copy()
            black = np.zeros((height, width, 3), np.uint8)
            area = cv2.bitwise_or(img_base, black, mask=mask)
            print('area: ', area.shape)
            self.save(area, str(i) + 'area')
            mask_hsv, green_area = self.get_green(area)
            cnts_area = cv2.contourArea(cnts)
            self.save(mask_hsv, str(i) + 'green')
            print(i, cnts_area)
            print(i, green_area)
            green_ratio = green_area / cnts_area
            print(str(i) + ': ratio = ', green_ratio)
            if green_ratio >= 0.8:
                areas_list.append(cnts)
        return areas_list
    
    def extract_leaf(self, img: np.ndarray, cnts_list: list, name=None, ext='.png'):
        areas_list = self.check_green_area(img, cnts_list)
        height, width = img.shape[:2]
        mask = np.zeros((height, width), np.uint8)
        for cnts in areas_list:
            cv2.drawContours(mask, [cnts], 0, 255, -1)
        black = np.zeros((height, width, 3), np.uint8)
        img_leaf = cv2.bitwise_or(img, black, mask=mask)
        if name is None:
            tag = 'leaf'
        else:
            tag = '-leaf'
        self.save(img_leaf, str(name) + tag, ext)
        return img_leaf

if __name__ == '__main__':
    main()