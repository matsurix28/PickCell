import cv2
import numpy as np

in_path = "test/img/leaf.JPG"
out_path = "test/output/conts"
img = cv2.imread(in_path)
height, width = img.shape[:2]
min_area = height * width / 100

def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)

# Tekari
#mask = np.full((height, width, 3), (255,255,255), np.uint8)
#img_tekari = cv2.illuminationChange(img, mask, alpha=0.1, beta=0.1)
#save("tekari.jpeg", img_tekari)

img_blr = cv2.GaussianBlur(img, (5,5), 0)

# HSV
img_hsv = cv2.cvtColor(img_blr, cv2.COLOR_BGR2HSV)
save("hsv.jpeg", img_hsv)

# Gaussian blur
img_gauss = cv2.GaussianBlur(img_hsv, (5,5), 0)

# Gray scale
img_gray = cv2.cvtColor(img_hsv, cv2.COLOR_BGR2GRAY)
save("gray.jpeg", img_gray)

# Binary
_, img_bin = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)
bin_name = out_path + "bin.jpeg"
cv2.imwrite(bin_name, img_bin)

# Canny edge
img_canny = cv2.Canny(img_gray, 100, 200)
save("canny.jpeg", img_canny)

# Gaussian
img_gauscany = cv2.GaussianBlur(img_canny, (5,5), 0)
save("gauscany.jpeg", img_gauscany)

# Invert
img_inv = cv2.bitwise_not(img_gauscany)
save("inv.jpeg", img_inv)


# Contours
conts, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
conts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, conts))
cv2.drawContours(img, conts_list, -1, color=(0,0,255), thickness=5)
conts_name = out_path + "conts.jpeg"
cv2.imwrite(conts_name, img)