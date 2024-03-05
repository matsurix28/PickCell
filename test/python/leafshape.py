import cv2
import math
import numpy as np

path = './tukue.JPG'
num = 0

img = cv2.imread(path)
hei, wid = img.shape[:2]
min = hei * wid / 100
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

_, bin = cv2.threshold(v, 50, 255, cv2.THRESH_BINARY)
cnts, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = list(filter(lambda x: cv2.contourArea(x) > min, cnts))

if len(cnts) > 0:
    elip = cv2.fitEllipse(cnts[num])
    black = np.zeros(img.shape[:3], np.uint8)
    bb = black.copy()
    cv2.ellipse(black, elip, (255,255,255), -1)
    cv2.drawContours(bb, cnts, num, (255,255,255), -1)

    bit = cv2.bitwise_and(bb, black)
    b2 = cv2.bitwise_xor(bit, black)
    cv2.imwrite('test.png', b2)

    menseki = np.sum(b2) / 255 / 3
    elip_area = np.sum(black) / 255 / 3
    elp_h, elp_w = elip[1]
    x, y = elip[0]
    print(menseki)
    print(elip_area)
    print(hei, wid)
    print(elp_h, elp_w)
    tate = np.abs(hei / 2 - y) + (elp_h / 2)
    yoko = np.abs(wid / 2 - x) + (elp_w / 2)
    print(tate, yoko)
    #print(elip[1])
    #print(img.shape[:2])

#h, w = elip[1]

#menseki = cv2.contourArea(cnts[1])
##area = (h / 2) * (w / 2) * math.pi
#print(h, w)
#print(menseki)
#print(area)
