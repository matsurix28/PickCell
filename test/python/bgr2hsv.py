import cv2

img = cv2.imread('test/output/daen/1_arranged.png')
h,w = img.shape[:2]
len = h*w
a = img.reshape(len, 3)
#b = cv2.cvtColor(a, cv2.COLOR_BGR2HSV)

bgr1 = ()