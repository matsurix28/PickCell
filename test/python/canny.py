import cv2
import numpy as np

def main():
    img = cv2.imread('1.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    black = np.zeros(img.shape[:2], np.uint8)
    img_canny = cv2.Canny(v, 100, 200)
    cnts, hie = cv2.findContours(img_canny, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    next_c = 0
    img_canny = cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)
    count = 0
    mmax = 0
    pos = 0
    for i in range(len(cnts)):
        img_cnt = cv2.drawContours(img_canny, cnts, next_c, (0,0,255), 5)
        
        area = cv2.contourArea(cnts[next_c])
        #print(next_c, area)
        count += 1
        if mmax < area:
            mmax = area
            pos = next_c
        next_c = hie[0][next_c][0]
        if next_c == -1:
            break
    #cv2.drawContours(img_canny, cnts, 2475, (0,0,255), -1)
    cv2.imwrite('test.png', img_canny)
    print(count)
    print(mmax)
    print(pos)
    print(img.shape[:2])

if __name__ == '__main__':
    main()