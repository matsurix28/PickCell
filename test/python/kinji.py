import cv2
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import optimize

img = cv2.imread('test/output/daen/1_arranged.png')
h,w = img.shape[:2]
len = h*w
b,g,r = cv2.split(img)
b = b.reshape(len)
g = g.reshape(len)
r = r.reshape(len)

def fitt(param, x,y,z):
    residual = z - (param[0]*x**2 + param[1]*y**2 + param[2]*x + param[3]*y + param[4])
    return residual

param = [0,0,0,0,0]

optimised_param =  optimize.leastsq(fitt, param, args=(b, g, r))

print(optimised_param)

f = a*x**2 + b*y**2 + c*x + d*y + e