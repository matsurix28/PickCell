px = [[24,34,56], [34,56,78], [98,100,23]]
val = [3,8,20]
import numpy as np

vallist = [[i,0,0] for i in val]
gti = np.stack([px, vallist], 1)
uniq = np.unique(gti, axis=0)

min = 0

for p,v in zip(px, val):
    px.count(p[0])

np.count_nonzero(px == px[0], axis=0)

np.sum(px == [24,34,56], axis=0)