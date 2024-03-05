import cv2
import numpy as np

in_path = "test/img/mottle.JPG"
out_path = "test/output/nuri/"
image = cv2.imread(in_path)
scale = 1000 / image.shape[1]
img = cv2.resize(image, dsize=None, fx=scale, fy=scale)
height, width = img.shape[:2]

def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)

def main():
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    v_canny = cv2.Canny(v, 100, 200)
    save("canny.png", v_canny)
    print("v_canny shape", v_canny.shape)
    _, v_bin = cv2.threshold(v_canny, 100, 255, cv2.THRESH_BINARY)
    img_or = cv2.bitwise_or(v, v_bin)
    save("or.png", img_or)
    print("or shape", img_or.shape)
    _, img_bin = cv2.threshold(img_or, 100, 255, cv2.THRESH_BINARY)
    print("bin shape", img_bin.shape)
    save("bin.png", img_bin)
    cnts, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_list = list(filter(lambda x: cv2.contourArea(x) > 10000, cnts))
    blank = np.zeros((height, width), np.uint8)
    for i, cnt in enumerate(cnts_list):
        base_img = blank.copy()
        masked = cv2.drawContours(base_img, [cnt], 0, 255, -1)
        save(str(i) + ".png", masked)
    img1 = img.copy()
    mask = cv2.drawContours(blank, [cnts_list[1]], 0, 255, -1)
    black = np.zeros((height, width, 3), np.uint8)
    resl = cv2.bitwise_or(img1, black, mask=mask)
    save("0masked.png", resl)
    blank = np.zeros((height, width), np.uint8)
    mask2 = cv2.drawContours(blank, [cnts_list[0]], 0, 255, -1)
    black2 = np.zeros((height, width, 3), np.uint8)
    resl2 = cv2.bitwise_or(img, black2, mask=mask2)
    save("1masked.png", resl2)
    save("blank.png", blank)


if __name__ == '__main__':
    main()