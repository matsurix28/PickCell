import numpy as np
import cv2
from PIL import Image, ImageTk

img = np.full((48,48,3), (255,0,0), np.uint8)
img = Image.fromarray(img)
cv2.imwrite('test.png', img)
