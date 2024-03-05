import cv2

img = cv2.imread('./1.png')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask_hsv = cv2.inRange(img_hsv, (30,50,50), (90,255,255))
cnts, _ = cv2.findContours(mask_hsv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)