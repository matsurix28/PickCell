import cv2
import numpy as np

in_path = "test/img/pen.JPG"
out_path = "test/output/"
img = cv2.imread(in_path)
height, width = img.shape[:2]

# tekari
#mask = np.full((height, width, 3), (255,255,255), np.uint8)
#tekari = cv2.illuminationChange(img, mask, alpha=0.2, beta=0.4)
#tekari_name = out_path + "tekari.jpeg"
#cv2.imwrite(tekari_name, tekari)

# HSV
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv_name = out_path + "hsv.jpeg"
cv2.imwrite(hsv_name, img_hsv)

# Gaussian blur
img_gauss = cv2.GaussianBlur(img_hsv, (5,5), 0)
gauss_name = out_path + "gauss.jpeg"
cv2.imwrite(gauss_name, img_gauss)

# Gray scale
img_gray = cv2.cvtColor(img_hsv, cv2.COLOR_BGR2GRAY)
gray_name = out_path + "gray.jpeg"
cv2.imwrite(gray_name, img_gray)

# binary
_, thresh = cv2.threshold(img_gray, 80, 255, cv2.THRESH_BINARY)
binary_name = out_path + "binary.jpeg"
cv2.imwrite(binary_name, thresh)


# Canny Edge
#canny = cv2.Canny(img_gauss, 100, 200)
#canny_name = out_path + "canny.jpeg"
#cv2.imwrite(canny_name, canny)

# Laplacian Edge
#lap = cv2.Laplacian(img, cv2.CV_64F)
#lap_name = out_path + "lap.jpeg"
#cv2.imwrite(lap_name, lap)




# Remove background
#bg_sub = cv2.createBackgroundSubtractorMOG2()
#fg_mask = bg_sub.apply(img_gauss)
#bg_name = out_path + "background.jpeg"
#cv2.imwrite(bg_name, fg_mask)