import cv2

img = cv2.imread('test/output/daen/bar.bmp')
cv2.rectangle(img, (100,100), (101,101), (255,0,0))
cv2.imwrite('test.bmp', img)