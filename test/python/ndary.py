import numpy as np
import cv2

a1 = np.array([[[2,3,4], [0,1,1], [4,5,6]], [[5,6,7],[6,7,8],[8,7,6]], [[10,11,12], [12,13,14],[11,12,14]]])
a2 = a1 +1

a1 = a1.reshape(9,3)
a2 = a2.reshape(9,3)
a3 = np.stack([a1, a2], 1)
kuro = np.array([[0,0,0], [0,0,0]])
a4 = a3 != kuro
wh = np.where(a3[:3] == kuro)

#print(a3)
print(np.delete(a3, wh[0], axis=0))

#print(a3 * a4)
#print(a3[np.all(a3 != kuro)])

#img1 = cv2.imread('1_arranged.png')
#img2 = cv2.imread('6_arranged.png')
#h,w = img1.shape[:2]
#length = h*w
#img1 = img1.reshape(length, 3)
#img2 = img2.reshape(length, 3)
#img = np.stack([img1, img2], 1)
#black = np.array([[0,0,0],[0,0,0]])
#whe = np.where(img == black)
#nokori = np.delete(img, whe[0], axis=0)
#print(nokori)