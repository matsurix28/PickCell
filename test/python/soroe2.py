import cv2
import numpy as np

sa = 14
hi = 0.97

img_fvfm = cv2.imread('./6.png')
img_leaf = cv2.imread('./1.png')

fvfm_hsv = cv2.cvtColor(img_fvfm, cv2.COLOR_BGR2HSV)
leaf_hsv = cv2.cvtColor(img_leaf, cv2.COLOR_BGR2HSV)

fh, fs, fv = cv2.split(fvfm_hsv)
lh, ls, lv = cv2.split(leaf_hsv)

_, f_bin = cv2.threshold(fs, 10, 255, cv2.THRESH_BINARY)
f_cnts, _ = cv2.findContours(f_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#print(len(f_cnts))

f_area = f_cnts[1]

fh, fw = img_fvfm.shape[:2]
fblack = np.zeros((fh, fw), np.uint8)
lblack = np.zeros(img_leaf.shape[:2], np.uint8)
img_fvfm = cv2.drawContours(fblack, [f_area], 0, 255, 10)


mask_green = cv2.inRange(leaf_hsv, (30,50,50), (90,255,255))
l_cnts, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
l_area = l_cnts[1]

img_leaf = cv2.drawContours(lblack, [l_area], 0, 255, 10)

#print(cv2.contourArea(f_area))
#print(cv2.contourArea(l_area))

f_ellipse = cv2.fitEllipse(f_area)
l_ellipse = cv2.fitEllipse(l_area)

#print('f ellipse',f_ellipse)
#print(l_ellipse)
f_angle = f_ellipse[2]
l_angle = l_ellipse[2]

#print(f_angle)
#print(l_angle)

#f_height, f_width = img_fvfm.shape[:2]
#f_center = (int(f_width / 2), int(f_height / 2))
#f_trans = cv2.getRotationMatrix2D(f_center, f_angle - 90, 1.0)
#f_rotated = cv2.warpAffine(img_fvfm, f_trans, (f_width, f_height))

#l_height, l_width = img_leaf.shape[:2]
#l_center = (int(l_width / 2), int(l_height / 2))
#l_trans = cv2.getRotationMatrix2D(l_center, l_angle - 90, 1.0)
#l_rotated = cv2.warpAffine(img_leaf, l_trans, (l_width, l_height))

f_haba = f_ellipse[1][0]
l_haba = l_ellipse[1][0]

#print('l ellipse', l_ellipse)
#print(f_haba)
#print(l_haba)


#print(scale)
#f_resize = cv2.resize(img_fvfm, dsize=None, fx=scale, fy=scale)

# Henkouuuuuuu
#fvfm_hsv = cv2.cvtColor(f_resize, cv2.COLOR_BGR2HSV)
#fh, fs, fv = cv2.split(fvfm_hsv)
#_, f_bin = cv2.threshold(fs, 10, 255, cv2.THRESH_BINARY)
#f_cnts, _ = cv2.findContours(f_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#f_cnts, _ = cv2.findContours(f_resize, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#print(cv2.contourArea(f_cnts[0]))
#f_area = f_cnts[0]
#f_ellipse = cv2.fitEllipse(f_area)
#print('new f ellipse', f_ellipse)

f_angle = f_ellipse[2]
l_angle = l_ellipse[2]

f_center = f_ellipse[0]
#print('f_center' ,f_center)
f_height, f_width = img_fvfm.shape[:2]
f_corners = np.array([(0,0), (f_width,0), (f_width,f_height), (0,f_height)])
f_radius = np.sqrt(max(np.sum((f_center - f_corners)**2, axis=1)))
f_frame = int(2 * f_radius)
#print('f_height', f_height)
#print('f_width', f_width)
#print('f_radius', f_radius)
#print('f angle',f_angle)

f_trans = cv2.getRotationMatrix2D(f_center, f_angle - 90, 1.0)
#print('trans', f_trans)
f_trans[0][2] += f_radius - f_center[0]
f_trans[1][2] += f_radius - f_center[1]
f_rotated = cv2.warpAffine(img_fvfm, f_trans, (f_frame, f_frame))


# Henkoooooooo
#fvfm_hsv = cv2.cvtColor(f_rotated, cv2.COLOR_BGR2HSV)
#fh, fs, fv = cv2.split(fvfm_hsv)
#_, f_bin = cv2.threshold(fs, 10, 255, cv2.THRESH_BINARY)
#f_cnts, _ = cv2.findContours(f_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

f_cnts, _ = cv2.findContours(f_rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
f_area = f_cnts[0]

nuri = np.zeros(f_rotated.shape[:2], np.uint8)
cv2.drawContours(nuri, [f_area], 0, 255, -1)

hanotate = (nuri == 255).sum(axis=0)
max_tate = hanotate.max()
print('max',max_tate)
print('f haba', f_haba)
print('l haba', l_haba)

scale = l_haba / f_haba






scale = cv2.contourArea(l_area) / cv2.contourArea(f_area) * hi
print('menseki hi',scale)
f_rotated = cv2.resize(f_rotated, dsize=None, fx=scale, fy=1)


# Henkooooooo
#fvfm_hsv = cv2.cvtColor(f_rotated, cv2.COLOR_BGR2HSV)
#fh, fs, fv = cv2.split(fvfm_hsv)
#_, f_bin = cv2.threshold(fs, 10, 255, cv2.THRESH_BINARY)
#f_cnts, _ = cv2.findContours(f_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

f_cnts, _ = cv2.findContours(f_rotated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

f_area = f_cnts[0]
f_ellipse = cv2.fitEllipse(f_area)
f_center = f_ellipse[0]

l_center = l_ellipse[0]
l_height, l_width = img_leaf.shape[:2]
l_corners = np.array([(0,0), (l_width, 0), (l_width,l_height), (0,l_height)])
l_radius = np.sqrt(max(np.sum((l_center - l_corners)**2, axis=1)))
l_frame = int(2 * l_radius)
l_trans = cv2.getRotationMatrix2D(l_center, l_angle - 90, 1.0)
l_trans[0][2] += l_radius - l_center[0]
l_trans[1][2] += l_radius - l_center[1]
l_rotated = cv2.warpAffine(img_leaf, l_trans, (l_frame, l_frame))
#cv2.imwrite('lrr.png', l_rotated)
print(l_rotated.shape[:2])

f_size, _ = f_rotated.shape[:2]
fh, fw = f_rotated.shape[:2]
l_size, _ = l_rotated.shape[:2]
print(f_size)
ha_yoko = 450
ha_tate = 200
print('f size', f_rotated.shape[:2])
print('l size', l_rotated.shape[:2])

#f_cut = f_rotated[500 : 1100, 300 : 1300]


f_cut = f_rotated[int(fh / 2 - ha_tate) : int(fh / 2 + ha_tate), int(fw / 2 - ha_yoko - sa) : int(fw / 2 + ha_yoko - sa)]
l_cut = l_rotated[int(l_size / 2 - ha_tate) : int(l_size / 2 + ha_tate), int(l_size / 2 - ha_yoko) : int(l_size / 2 + ha_yoko)]
#cv2.imwrite('cutf.png', f_cut)
#cv2.imwrite('cutl.png', l_cut)

#dst = cv2.cvtColor(f_cut, cv2.COLOR_BGR2BGRA)
#dst[:,:,3] = 50
#l_cut = cv2.cvtColor(f_cut, cv2.COLOR_BGR2BGRA)
#l_cut[:,:,3] = 255

res = cv2.addWeighted(l_cut, 0.5, f_cut, 0.5, 0)
cv2.imwrite('gattai.png', res)

#fvfm_hsv = cv2.cvtColor(f_cut, cv2.COLOR_BGR2HSV)
#leaf_hsv = cv2.cvtColor(l_cut, cv2.COLOR_BGR2HSV)

#fh, fs, fv = cv2.split(fvfm_hsv)
#lh, ls, lv = cv2.split(leaf_hsv)

#_, f_bin = cv2.threshold(fs, 10, 255, cv2.THRESH_BINARY)
#f_cnts, _ = cv2.findContours(f_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#f_area = f_cnts[1]

#mask_green = cv2.inRange(leaf_hsv, (30,50,50), (90,255,255))
#l_cnts, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#l_area = l_cnts[0]

#h, w = f_cut.shape[:2]
#f_black = np.zeros((h, w), np.uint8)
#l_black = f_black.copy()
#cv2.drawContours(f_black, [f_area], 0, 255, 1)
#cv2.drawContours(l_black, [l_area], 0, 255, 1)
#print('f area: ', cv2.contourArea(f_area))
#print('l area: ', cv2.contourArea(l_area))
#scale = cv2.contourArea(l_area) / cv2.contourArea(f_area)
#cv2.imwrite('farea.png', f_black)
#cv2.imwrite('larea.png', l_black)
#re = cv2.resize(f_black, dsize=None, fx=scale, fy=1)
#cv2.imwrite('resize.png', re)