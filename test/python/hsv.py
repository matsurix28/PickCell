import cv2
import numpy as np

path = './tukue.JPG'

img = cv2.imread(path)
#img = cv2.resize(img, dsize=None, fx=0.5, fy=0.5)
#img = cv2.blur(img, (5,5))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)
canny = cv2.Canny(img, 20, 150)
cv2.imwrite('test.png',s)
