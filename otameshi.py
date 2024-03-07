import re

a= ['jpg', 'jpeg', 'png', 'tiff', 'bmp']
b = sum([[i.lower(), i.upper()] for i in a], [])
print(b)