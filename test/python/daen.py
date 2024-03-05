import cv2
import numpy as np
img = cv2.imread('./1.png')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v, = cv2.split(img_hsv)
#_, bin = cv2.threshold(s, 10, 255, cv2.THRESH_BINARY)
#cv2.imwrite('bin.png', bin)
#cnts,_ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
mask_hsv = cv2.inRange(img_hsv, (30,50,50), (90,255,255))
cnts,_ = cv2.findContours(mask_hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# chokusen
#rows, cols = img.shape[:2]
#[vx,vy,x,y] = cv2.fitLine(cnts[1], cv2.DIST_L2, 0,0.01,0.01)
#lefty = int((-x * vy / vx) + y)
#righty = int(((cols - x) * vy/vx) + y)
#im = cv2.line(img, (cols -1, righty), (0,lefty), (255,0,0), 2)

print(len(cnts))
print(cv2.contourArea(cnts[1]))

# naname sikaku
rect = cv2.minAreaRect(cnts[1])
box = cv2.boxPoints(rect)
box = np.intp(box)
im = cv2.drawContours(img, [box], 0, (0,0,255), 2)

# daen
ellipse = cv2.fitEllipse(cnts[1])
print(ellipse)
im = cv2.ellipse(img, ellipse, (0,255,0), 2)
#cv2.imwrite('sikaku.png', im)

height, width = img.shape[:2]
center = ((int(width / 2)), int(height / 2))
trans = cv2.getRotationMatrix2D(center, -33, 1.0)
img2 = cv2.warpAffine(im, trans, (width, height))
#cv2.imwrite('3trans.png', img2)