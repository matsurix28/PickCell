import cv2
import numpy as np

in_path = "test/img/naname.JPG"
out_path = "test/output/hsv/"
img = cv2.imread(in_path)
height, width = img.shape[:2]
min_area = height * width / 100

def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
imgh, imgs, imgv = cv2.split(img_hsv)

save("h.jpeg", imgh)
save("s.jpeg", imgs)
save("v.jpeg", imgv)

_, imgh_bin = cv2.threshold(imgh, 50, 255, cv2.THRESH_BINARY)
_, imgs_bin = cv2.threshold(imgs, 50, 255, cv2.THRESH_BINARY)
_, imgv_bin = cv2.threshold(imgv, 50, 255, cv2.THRESH_BINARY)

save("h_bin.jpeg", imgh_bin)
save("s_bin.jpeg", imgs_bin)
save("v_bin.jpeg", imgv_bin)

#imgh_noise = cv2.medianBlur(imgh_bin, )
#save("h_noise.jpeg", imgh_noise)

conts_h, _ = cv2.findContours(imgh_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contsh_list = list(filter(lambda x: cv2.contourArea(x) > min_area, conts_h))
conts_s, _ = cv2.findContours(imgs_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contss_list = list(filter(lambda x: cv2.contourArea(x) > min_area, conts_s))
conts_v, _ = cv2.findContours(imgv_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contsv_list = list(filter(lambda x: cv2.contourArea(x) > min_area, conts_v))

conth = img.copy()
conts = img.copy()
contv = img.copy()

cv2.drawContours(conth, contsh_list, -1, color=(0,0,255), thickness=5)
cv2.drawContours(conts, contss_list, -1, color=(0,0,255), thickness=5)
cv2.drawContours(contv, contsv_list, -1, color=(0,0,255), thickness=5)

save("conth.jpeg", conth)
save("conts.jpeg", conts)
save("contv.jpeg", contv)


print(len(conts_h))
print(len(conts_s))
print(len(conts_v))

print(len(contsh_list))
print(len(contss_list))
print(len(contsv_list))