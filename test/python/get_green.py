import cv2
import numpy as np
in_path = "test/img/naname.JPG"
out_path = "test/output/green/"
image = cv2.imread(in_path)
scale = 1000 / image.shape[1]
img = cv2.resize(image, dsize=None, fx=scale, fy=scale)
min_area = None
pixel_num = None

def main():
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    hsv_min = np.array([30,50,50])
    hsv_max = np.array([90,255,200])
    height, width = img.shape[:2]
    mama = np.zeros((height, width, 3), np.uint8)
    mama = cv2.bitwise_not(mama)
    save("mask.png", mama)
    print(img.shape)
    print(mama.shape)
    mask_hsv = cv2.inRange(img_hsv, hsv_min, hsv_max)
    save("hsvmask.png", mask_hsv)
    print("mask_hsv shape", mask_hsv.shape)
    pixel_num = np.size(mask_hsv)
    pixel_img = np.size(img)
    print("mask", pixel_num)
    print("img", pixel_img)
    save("mask.png", mask_hsv)
    pixel_sum = np.sum(mask_hsv)
    white = pixel_sum / 255
    print("white", white)
    result = cv2.bitwise_or(mama, img, mask=mask_hsv)
    save("green.png", result)
    print("maskhsv type", type(mask_hsv))


def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)



if __name__ == '__main__':
    main()