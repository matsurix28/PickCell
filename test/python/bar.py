import cv2

def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)

in_path = "test/img/bar.bmp"
out_path = "test/output/bar/"
img = cv2.imread(in_path)
height, width = img.shape[:2]
min_area = height * width / 100

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
_, imgs, _ = cv2.split(img_hsv)
_, imgs_bin = cv2.threshold(imgs, 100, 255, cv2.THRESH_BINARY)

save("bin.jpeg", imgs_bin)

conts, _ = cv2.findContours(imgs_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
conts_list = list(filter(lambda x: cv2.contourArea(x) > min_area, conts))

rect_list = []
approx_list = []
for i, cnt in enumerate(conts_list):
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    #approx = cv2.convexHull(approx)
    #approx = cv2.approxPolyDP(approx, 0.08 * cv2.arcLength(approx, True), True)
    #cv2.drawContours(img, approx, -1, color=(0,0,255), thickness=5)
    if len(approx) == 4:
        rect_list.append(i)
        approx_list.append(approx)
        print("4 points")
        print(approx)

#cv2.drawContours(img, conts_list, -1, color=(0,0,255), thickness=10)
save("conts.jpeg", img)