import cv2
import numpy as np

img_fvfm = cv2.imread('./6.png')
img_leaf = cv2.imread('./1.png')

def main():
    test()
    print(img_leaf.shape[:2])

def test():
    bin = sbin(img_fvfm)
    cnts, fimg = get_area(bin)
    angle, center, _ = elip(cnts)
    rotated = rotate(fimg, angle, center)
    rotated_cf = rotate(img_fvfm, angle, center)
    mask_cf = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)
    rotated_cf = cv2.bitwise_and(rotated_cf, mask_cf)
    ftate = max_tate(rotated)

    lbin = green(img_leaf)
    lcnts, limg = get_area(lbin)
    langle, lcenter, lr = elip(lcnts)
    lrotated = rotate(limg, langle, lcenter)
    rotated_cl = rotate(img_leaf, langle, lcenter)
    mask_lf = cv2.cvtColor(lrotated, cv2.COLOR_GRAY2BGR)
    rotated_cl = cv2.bitwise_and(rotated_cl, mask_lf)
    ltate = max_tate(lrotated)
    
    scale = ltate / ftate
    fresize = cv2.resize(rotated, dsize=None, fx=scale, fy=scale)
    resize_cf = cv2.resize(rotated_cf, dsize=None, fx=scale, fy=scale)

    recnts, reimg = get_area(fresize)
    reangle, recenter, fr = elip(recnts)

    #reimg = cv2.resize(reimg, dsize=None, fx=1.08, fy=1)

    #haba = list(map(lambda x: x + 150, lr))
    haba = list(map(lambda x: x * 1.2, lr))
    lcut = kiru(lrotated, haba)
    cut_cl = kiru(rotated_cl, haba)
    #fcut = kiru(reimg, haba, 20)

    lc_cnts, lccimg = get_cnts(lcut)
    #fc_cnts, fccimg = get_cnts(fcut)

    #print(lccimg.shape[:2])
    #print(fccimg.shape[:2])

    #gousei = kasane(lccimg, fccimg)
    print()
    itiban = chosei(reimg, lccimg, haba)
    per = (100 + itiban[1]) / 100
    iti = itiban[2]
    reimg_cf = cv2.resize(resize_cf, dsize=None, fx=per, fy=1)
    img = kiru(reimg_cf, haba, iti)

    #img = cv2.addWeighted(cut_cl, 1, img, 0.5, 0)
    cv2.imwrite('test.png', img)
    cv2.imwrite('test2.png', cut_cl) 

def chosei(img1, img2, haba):
    hani = int(haba[1] / 10)
    ll = []
    for i in range(-20, 21, 1):
        per = (100 + i) / 100
        reimg = cv2.resize(img1, dsize=None, fx=per, fy=1)
        for iti in range(-hani, hani, 1):
            img = kiru(reimg, haba, iti)
            _, img = get_cnts(img)
            gousei = kasane(img, img2)
            shiro = np.sum(gousei)
            ll.append([shiro, i, iti])
    itiban = max(ll, key=lambda x: x[0])
    per = (100 + itiban[1]) / 100
    iti = itiban[2]
    reimg = cv2.resize(img1, dsize=None, fx=per, fy=1)
    img = kiru(reimg, haba, iti)
    _,img = get_cnts(img)
    kekka = cv2.addWeighted(img2, 0.5, img, 0.5, 0)
    print(itiban)
    return itiban


def green(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green = cv2.inRange(img_hsv, (30,50,50), (90,255,255))
    return green

def kasane(img1, img2):
    kasane = cv2.bitwise_and(img1, img2)
    #kasane = cv2.addWeighted(img1, 0.5, img2, 0.5,0)
    return kasane

def sbin(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img_hsv)
    _, bin = cv2.threshold(s, 10, 255, cv2.THRESH_BINARY)
    return bin

def get_area(img):
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bets_cnts = max(cnts, key=lambda x: cv2.contourArea(x))
    black = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(black, [bets_cnts], 0, 255, -1)
    return bets_cnts, black

def get_cnts(img):
    cnts, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bets_cnts = max(cnts, key=lambda x: cv2.contourArea(x))
    black = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(black, [bets_cnts], 0, 255, 5)
    return bets_cnts, black

def elip(cnts):
    ellipse = cv2.fitEllipse(cnts)
    angle = ellipse[2]
    center = ellipse[0]
    rudius = ellipse[1]
    return angle, center, rudius

def rotate(img, angle, center):
    h, w = img.shape[:2]
    corners = np.array([(0,0), (w,0), (w,h), (0,h)])
    radius = np.sqrt(max(np.sum((center - corners)**2, axis=1)))
    frame = int(2 * radius)
    trans = cv2.getRotationMatrix2D(center, angle - 90, 1)
    trans[0][2] += radius - center[0]
    trans[1][2] += radius - center[1]
    rotated = cv2.warpAffine(img, trans, (frame, frame))
    return rotated

def max_tate(bin):
    tate = (bin == 255).sum(axis=0)
    maxtate = tate.max()
    return maxtate

def kiru(img, haba, prm=0):
    h, w = list(map(lambda x: int(x), img.shape[:2]))
    t, y = list(map(lambda x: int(x), haba[:2]))
    cut = img[int(h/2 - t/2) : int(h/2 + t/2), int(w/2 - y/2 - prm) : int(w/2 + y/2 - prm)]
    return cut

if __name__ == '__main__':
    main()
