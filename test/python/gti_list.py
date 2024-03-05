import numpy as np
a = [[[[23,45,66], 98], [[345,66,77], 88]],[[[24,67,88], 98], [[45,55,32], 76]]]
b = []
for i in range(len(a)):
    b.extend(a[i])

print(b)