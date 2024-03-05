import cv2
import numpy as np

in_path = "test/img/leaf.JPG"
out_path = "test/output/array/"
img = cv2.imread(in_path)
height, width = img.shape[:2]
print(img.shape[:2])
mask = np.full((height, width, 3),(255,255,255))
#mask = np.zeros((100, 200, 3))
mask_name = out_path + "mask.jpeg"
cv2.imwrite(mask_name, mask)