import cv2

def main():
    img = cv2.imread('bar.bmp')
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img_gray = cv2.blur(img_gray, (5,5))
    _, bin = cv2.threshold(img_gray, 230, 255, cv2.THRESH_BINARY_INV)
    cnts_list, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_list = list(filter(lambda x: cv2.contourArea(x) > 500, cnts_list))
    x,y,w,h = cv2.boundingRect(cnts_list[0])
    img = cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,0),3)
    print(x,y,w,h)
    if check_bar(w, h, img.shape[0]):
        print('koreha bar')
    else:
        print('bar janai')
    cv2.imwrite('teest.png', img)

def check_bar(w, h, ih):
    hi = h / w
    if hi > 0.7:
        tate = True
    else:
        tate = False
    img_hi = h / ih
    if img_hi > 0.8:
        img_tate = True
    else:
        img_tate = False
    if tate and img_tate:
        return True
    else:
        return False


if __name__ == '__main__':
    main()