import numpy as np
ll = np.array([[100, 20,55], [20, 40, 10], [30, 5, 100]])
print(max(ll, key=lambda x: x[2]))
print(ll[2])