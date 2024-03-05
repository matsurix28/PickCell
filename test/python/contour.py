import cv2

def main():
    img = cv2.imread('scan1.png')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    _, bin = cv2.threshold(v, 60, 255, cv2.THRESH_BINARY)
    cv2.imwrite('test.png', s)

if __name__ == '__main__':
    main()