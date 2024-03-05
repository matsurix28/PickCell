import cv2
import numpy as np

img = cv2.imread('./1.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
cv2.imwrite('v.png', v)
_, bin = cv2.threshold(v, 100, 255, cv2.THRESH_BINARY)
cv2.imwrite('bin.png', bin)
cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
h, w = img.shape[:2]
mask = np.zeros((h,w, 3), np.uint8)
c = cnts[3]
cv2.drawContours(mask, [c], -1, (255,255,255), -1)
cv2.imwrite('mask.png', mask)

kirinuki = cv2.bitwise_and(img, mask)
cv2.imwrite('kiri.png', kirinuki)
cv2.imwrite('img.png', img)

area = cv2.contourArea(c)
print(area)
size = h * w
print(size)