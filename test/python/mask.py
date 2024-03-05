import cv2
import numpy as np

img = cv2.imread('naname.JPG')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
_, bin = cv2.threshold(v, 50, 255, cv2.THRESH_BINARY)
cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = list(filter(lambda x: cv2.contourArea(x) > 5000, cnts))

mask = np.zeros(img.shape[:2], np.uint8)
print(mask.shape)
print(img.shape)
#cv2.drawContours(mask, cnts, 1, 255, -1)

#print(len(cnts))
#cv2.imwrite('test.png', img)
