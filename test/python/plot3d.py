import cv2
import numpy as np
from matplotlib import pyplot as plt
from scipy import optimize
from mpl_toolkits.mplot3d import Axes3D

img = cv2.imread('test/output/daen/1_arranged.png')
h,w = img.shape[:2]
scale = 10 / w
img = cv2.resize(img,dsize=None, fx=scale, fy=scale)
x,y,z = cv2.split(img)
x= x.ravel()
y = y.ravel()
z = z.ravel()
print(y.sum())

#x = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])
#y = np.array([-1,-3,-1,9,21,30,37,39,59,65,95,123,142,173,191,216,256,292,328,358])
#z = np.array([-89,-77,-69,-48,-47,-42,-40,-36,-32,-27,-24,-22,-21,-4,-3,5,19,24,27,40])


def fitting_func(param, x,y,z):
    residual = z - (param[0]*x**2 + param[1]*y**2 + param[2]*x + param[3]*y + param[4])
    return residual

def ffit(param, x,y,z):
    residual = z - (param[0]*x + param[1]*y + param[2])
    return residual

param = [0,0,0,0,0]

optimize_param = optimize.leastsq(fitting_func, param, args=(x,y,z))
print(optimize_param)

#parm = [0,0,0]
#optimize_param = optimize.leastsq(ffit, parm, args=(x,y,z))

a = optimize_param[0][0]
b = optimize_param[0][1]
c = optimize_param[0][2]
d = optimize_param[0][3]
e = optimize_param[0][4]

f = a*x**2 + b*y**2 + c*x + d*y + e

#f = a*x + b*y + c

T = np.arange(10)
E = np.arange(10)


fig = plt.figure()
ax = plt.axes(projection="3d")
#ax = Axes3D(fig)
#ax.scatter(x,y,z)
ax.plot(x,y,f)

#fig.plot(T, E, 'rx-')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.savefig('fig.png')
plt.show()
