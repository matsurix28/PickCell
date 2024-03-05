import cv2
import numpy as np

wid = 100
hei = 100

low = 100
up = 255

img = np.zeros((hei, wid, 1), np.uint8)
thresh = np.linspace(low, up, wid)
for i in range(wid):
    for j in range(hei):
        img[j,i,0] = thresh[i]

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

img = np.full((hei, wid), low, np.uint8)
cv2.imwrite('test.png', img)