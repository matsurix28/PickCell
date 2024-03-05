import numpy as np

px = np.array([[0,74,255], [34,55,6], [0,74,255], [34,55,6],[23,12,90],[0,56,88]], np.uint8)
val = [0.78, 0.81, 0.78, 0.85, 0.72, 0.66]
lin_px = np.array_split(px, 3, axis=0)

#print(lin_px)

val2 = [[i,0,0] for i in val]
print(px)
a = np.stack([px, val2], 1)


print(np.unique(a, axis=0))