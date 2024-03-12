import time

import cv2
import numpy as np

low = [30, 0, 0]
high = [90, 255,255]
height = 80
width = 500
img = np.zeros((height, width, 3), np.uint8)
hue = np.linspace(low[0], high[0], width)
saido = np.linspace(low[1], high[1], height)
value = np.linspace(low[2], high[2], height)

start = time.time()
'''
for i in range(width):
    for j in range(height):
        img[j,i,0] = hue[i]
        img[j,i,1] = saido[j]
        img[j,i,2] = value[j]
'''
#img = np.array([[h,s,v] for (s, v) in zip(saido, value) for h in hue], np.uint8).reshape(height, width, 3)
img = [[h,255,255]  for h in hue]
img = np.array([img for i in range(height)], np.uint8)

end = time.time()
print('time: ', end - start)
img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
cv2.imwrite('test_res.png', img)