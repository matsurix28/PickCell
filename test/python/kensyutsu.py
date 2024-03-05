import cv2
import numpy as np

in_path = "test/img/2.png"
out_path = "test/output/area/2/"
image = cv2.imread(in_path)
img_scaled = None
min_area = None
pixel_num = None

def main():
    global img_scaled
    img_scaled = scale(image)
    height, width = img_scaled.shape[:2]
    global min_area
    min_area = height * width / 100
    img_hsv = hsv(img_scaled)
    imgh, imgs, imgv = split_hsv(img_hsv)
    imgh_canny = canny(imgh, "h")
    imgs_canny = canny(imgs, "s")
    imgv_canny = canny(imgv, "v")
    global pixel_num
    pixel_num = np.size(img_scaled)
    imgh_bin = bin(imgh_canny, "h")
    imgs_bin = bin(imgs_canny, "s")
    imgv_bin = bin(imgv_canny, "v")
    #img_bin = cv2.cvtColor(imgs_bin, cv2.COLOR_GRAY2BGR)
    img_or = cv2.bitwise_or(imgs, imgs_bin)
    save("or.png", img_or)
    #img_gray = gray(img_or)
    img_binbin = bin(img_or, "2")
    print(img_binbin.shape)
    conts = cnts(img_binbin)
    print(conts)
    


def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)

def scale(img):
    scale = 1000 / img.shape[1]
    img_scaled = cv2.resize(img, dsize=None, fx=scale, fy=scale)
    return img_scaled

def hsv(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    save("hsv.png", img_hsv)
    return img_hsv

def split_hsv(img):
    imgh, imgs, imgv = cv2.split(img)
    save("h.png", imgh)
    save("s.png", imgs)
    save("v.png", imgv)
    return imgh, imgs, imgv

def gaussblur(img):
    return cv2.GaussianBlur(img, (5,5), 0)

def gray(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    save("gray.png", img_gray)
    return img_gray

def bin(img, name):
    _, img_bin = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    save(name + "bin.png", img_bin)
    return img_bin

def least_noise(img):
    pixel_sum = np.sum(img)
    white_pixel = pixel_sum / 255
    black_pixel = pixel_num - white_pixel
    return white_pixel, black_pixel

def canny(img, name):
    img_canny = cv2.Canny(img, 100, 200)
    save(name + "canny.png", img_canny)
    return img_canny

def invert(img):
    img_inv = cv2.bitwise_not(img)
    save("inv.png", img_inv)
    return img_inv

def cnts(img):
    conts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    conts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, conts))
    cv2.drawContours(img_scaled, conts_list, -1, (0,0,255), 5)
    save("conts.png", img_scaled)
    return conts_list

if __name__ == '__main__':
    main()