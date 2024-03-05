import glob
import tempfile
from test.python.ppp import Pickcell

import cv2
import numpy as np
from matplotlib import colors
from matplotlib import pyplot as plt
from PIL import Image
from plotly import graph_objects as go
from plotly_resampler import register_plotly_resampler

img1 = cv2.imread('0220/1_arranged.png')
img2 = cv2.imread('0220/2_arranged.png')

#img1 = cv2.imread('0220/1_arranged.png')
#img2 = cv2.imread('0220/2_arranged.png')
fvfm = [[[  0,  74, 255], 831.0],[[  0,  64, 255], 832.0],[[  0,  53, 255], 833.0],[[  0,  43, 255], 834.0],[[  0,  33, 255], 835.0],[[  0,  21, 255], 836.0],[[  0,  11, 255], 837.0],[[  0,   1, 255], 838.0],[[  0,  95, 255], 829.0],[[  0, 105, 255], 828.0],[[  0, 117, 255], 827.0],[[  0, 127, 255], 826.0],[[  0, 136, 255], 825.0],[[  0, 148, 255], 824.0],[[  0, 158, 255], 823.0],[[  0, 168, 255], 822.0],[[  0, 179, 255], 821.0],[[  0, 189, 255], 820.0],[[  0, 199, 255], 819.0],[[  0, 210, 255], 818.0],[[  0, 220, 255], 817.0],[[  0, 231, 255], 816.0],[[  0, 241, 255], 815.0],[[  0, 251, 255], 814.0],[[  0, 255, 241], 813.0],[[  0, 255, 221], 812.0],[[  0, 255, 201], 811.0],[[  0, 255, 179], 810.0],[[  0, 255, 159], 809.0],[[  0, 255, 139], 808.0],[[  0, 255, 116], 807.0],[[  0, 255,  96], 806.0],[[  0, 255,  74], 805.0],[[  0, 255,  54], 804.0],[[  0, 255,  34], 803.0],[[  0, 255,  11], 802.0],[[  9, 255,   4], 801.0],[[ 28, 255,  14], 800.0],[[ 51, 255,  26], 799.0],[[ 71, 255,  36], 798.0],[[ 91, 255,  46], 797.0],[[113, 255,  57], 796.0],[[133, 255,  67], 795.0],[[156, 255,  78], 794.0],[[176, 255,  88], 793.0],[[195, 255,  98], 792.0],[[218, 255, 110], 791.0],[[238, 255, 119], 790.0],[[255, 252, 127], 789.0],[[255, 229, 115], 788.0],[[255, 210, 105], 787.0],[[255, 190,  95], 786.0],[[255, 167,  84], 785.0],[[255, 147,  74], 784.0],[[255, 125,  63], 783.0],[[255, 105,  53], 782.0],[[255,  85,  43], 781.0],[[255,  62,  31], 780.0],[[255,  42,  21], 779.0],[[255,  23,  11], 778.0],[[255,   0,   0], 777.0],[[235,   0,   0], 776.0],[[215,   0,   0], 775.0],[[193,   0,   0], 774.0],[[173,   0,   0], 773.0],[[150,   0,   0], 772.0],[[130,   0,   0], 771.0],[[111,   0,   0], 770.0],[[88,  0,  0], 769.0],[[68,  0,  0], 768.0],[[48,  0,  0], 767.0],[[25,  0,  0], 766.0],[[6, 0, 0], 765.0]]

p = Pickcell()
try:
    px, hue, val = p.run(img1, img2, fvfm)
except (TypeError, ValueError) as e:
    print(e)

val2 = [[i,0,0] for i in val]
a = np.stack([px, val2], 1)
b = np.unique(a, axis=0)
#c = np.stack([hue, val], 1)
#d = np.unique(c, axis=0)
#print(len(px))
#print(len(b))
#print(len(d))

#hue = np.array(hue)
#val = np.array(val)

#correlation = np.corrcoef(hue, val)
#print(correlation[0])

#huee = [i[0] for i in d]
#valu = [i[1] for i in d]

#plt.scatter(huee, valu)
#plt.show()

#b = [i[0] for i in px]
#g = [i[0] for i in px]
#r = [i[0] for i in px]

bl = [i[0,0] for i in b]
g = [i[0,1] for i in b]
r = [i[0,2] for i in b]

va = [i[1,0] for i in b]

mi = min(va)
ma = max(va)

#min = va.min()
#max = va.max()

#print(min, max)


#cm = plt.cm.get_cmap('RdYlBu_r')

#fig = plt.figure()

#ax = fig.add_subplot(1, 1, 1, projection='3d')

#mappable = ax.scatter(r,g, bl, c=va, vmin=min, vmax=max, cmap=cm)
#fig.colorbar(mappable, ax=ax)
#ax.scatter(r,g,bl, c='b')
#plt.show()

# ------------------------------------
normal = colors.Normalize(vmin=mi, vmax=ma)
array_px = [[i,j,k] for (i,j,k) in zip(r,g,bl)]
#array_px = normal(va).tolist()
vvv = 1
marker = {'size': 1}
if vvv  is not None:
    marker.update(color=array_px)
    #marker['colorbar'] = {'title': 'Fv/Fm'}

#register_plotly_resampler(mode='auto')

figure = go.Figure(
    data=[go.Scatter3d(
        x=r,
        y=g,
        z=bl,
        mode='markers',
        marker=marker
        #marker=dict(
        #    size=1,
        #    color=array_px,
            #colorbar=dict(
            #    title='Fv/Fm'
            #)
        #)
    )]
)

# 表示
#figure.write_html('fvfm.html')
figure.show()
#figure.show_dash(mode='inline')

def rotate(x,y,z,theta):
    w = x + 1j *y
    return np.real(np.exp(1j * theta) * w), np.imag(np.exp(1j * theta) * w), z

x_eye = -1.25
y_eye = 2
z_eye = 0.5

'''
with tempfile.TemporaryDirectory(prefix='temp_', dir='.') as temp:
    angels = np.arange(0, 2 * np.pi, 0.1)
    for i, theta in enumerate(angels):
        print(i)
        no = str(i).zfill(3)
        x_r, y_r, z_r = rotate(x_eye, y_eye, z_eye, -theta)
        figure.update_layout(scene_camera_eye=dict(
            x=x_r,
            y=y_r,
            z=z_r
        ))
        print('save ', i)
        figure.write_image(temp + '/' + no + '.png', scale=1)
        print('save finished ', i)

    files = sorted(glob.glob(temp + '/*.png'))
    images = list(map(lambda file: Image.open(file), files))
    images[0].save('res.gif', save_all=True, append_images=images[1:], duration=500, loop=0)
'''