import cv2
import numpy as np

wid = 500
heig = 100

low = [30,50,50]
up = [80,255,200]

hsv = np.zeros((heig, wid, 3), np.uint8)
h = np.linspace(low[0], up[0], wid)
s = np.linspace(low[1], up[1], heig)
v = np.linspace(low[2], up[2], heig)

for i in range(wid):
    for j in range(heig):
        hsv[j,i,0] = h[i]
        hsv[j,i,1] = s[j]
        hsv[j,i,2] = v[j]

bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
img = cv2.resize(bgr, (500,50))
cv2.imwrite('test.png', img)