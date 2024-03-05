import numpy as np

px = [[23,44,556], [21,34,55], [22,33,44], [23,44,556], [21,34,55], [23,44,556]]
hue = [1,2,3,1,2,1]
val = [780,790,800,810,820,780]

hue2 = [[i,0,0] for i in hue]
val2 = [[i,0,0] for i in val]

a = np.stack([px, val2, hue2], 1)
b = np.unique(a, axis=0)