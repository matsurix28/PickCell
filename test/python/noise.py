import cv2

img = cv2.imread('./1.png')
hi, wi = img.shape[:2]
scale = 1000 / hi
img = cv2.resize(img, dsize=None, fx=scale, fy=scale)
img = cv2.blur(img, (5,5))
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img_hsv)
_, bin_h = cv2.threshold(h, 60, 255, cv2.THRESH_BINARY)
_, bin_s = cv2.threshold(s, 60, 255, cv2.THRESH_BINARY)
_, bin_v = cv2.threshold(v, 60, 255, cv2.THRESH_BINARY)

cv2.imwrite('h.png', h)
cv2.imwrite('s.png', s)
cv2.imwrite('v.png', v)

cv2.imwrite('bin_h.png', bin_h)
cv2.imwrite('bin_s.png', bin_s)
cv2.imwrite('bin_v.png', bin_v)

canny_h = cv2.Canny(bin_h, 100,200)
canny_s = cv2.Canny(bin_s, 100,200)
canny_v = cv2.Canny(bin_v, 100,200)

cv2.imwrite('canny_h.png', canny_h)
cv2.imwrite('canny_s.png', canny_s)
cv2.imwrite('canny_v.png', canny_v)

cnts_h, _ = cv2.findContours(canny_h, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts_s, _ = cv2.findContours(canny_s, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts_v, hieraruki = cv2.findContours(canny_v, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

height, width = img.shape[:2]
min_area = height * width / 1000

print('height', height)
print('width', width)
print('min area', min_area)

nagasa = []
for i, cnts in enumerate(cnts_v):
    length = cv2.arcLength(cnts, True)
    nagasa.append([length, cnts])

fcnts_h = list(filter(lambda x: cv2.contourArea(x) < min_area, cnts_h))
fcnts_s = list(filter(lambda x: cv2.contourArea(x) < min_area, cnts_s))
fcnts_v = list(filter(lambda x: cv2.contourArea(x) < min_area, cnts_v))

print(type(cnts_h))
print('h: ', len(cnts_h))
print('s: ', len(cnts_s))
print('v: ', len(cnts_v))

print('h: ', len(fcnts_h))
print('s: ', len(fcnts_s))
print('v: ', len(fcnts_v))

copy = img.copy()
cv2.drawContours(copy, fcnts_h, -1, [0,0,255], 5)
cv2.imwrite('cnts_h.png', copy)

copy = img.copy()
cv2.drawContours(copy, fcnts_s, -1, [0,0,255], 5)
cv2.imwrite('cnts_s.png', copy)

copy = img.copy()
cv2.drawContours(copy, fcnts_v, -1, [0,0,255], -1)
cv2.imwrite('cnts_v.png', copy)

print('saisho', nagasa[0][0])
nagasa.sort(reverse=True,key=lambda x: x[0])
print('sort', nagasa[0][0])

#print(nagasa[0][1])
print(cv2.contourArea(nagasa[0][1]))
copy = img.copy()
cv2.drawContours(copy, nagasa[0][1], -1, [0,0,255], -1)
cv2.imwrite('nagai.png', copy)

next_c = 0
copy = img.copy()
for cnts in cnts_v:
    cv2.drawContours(copy, cnts_v, next_c, [0,0,255], -1)
    next_c = hieraruki[0][next_c][0]
    if next_c == -1:
        break
cv2.imwrite('soto.png', copy)
#copy = img.copy()
#cv2.drawContours(copy, fcnts_v, 0, [0,0,255], 1)
#cv2.imwrite('cnts_v0.png', copy)

#copy = img.copy()
#cv2.drawContours(copy, fcnts_v, 1, [0,0,255], 1)
#cv2.imwrite('cnts_v1.png', copy)