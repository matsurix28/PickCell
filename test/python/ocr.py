import easyocr
import cv2
import re
import itertools
import statistics
import math

out_path = "test/output/ocr/"

def save(name, img):
    output = out_path + name
    cv2.imwrite(output, img)

reader = easyocr.Reader(['en'])
path = "bar.bmp"

#img = cv2.imread(path)
#img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#_, img_bin = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)
#save("bin.bmp", img_bin)

ppath = out_path + "bin.bmp"
result = reader.readtext(path)
#result = [["aaa", "0.5"], ["bbbb", "1.7"], ["dddd", "0.89"]]
print([row[1] for row in result])

fvfm_scale = []
for res in result:
    # Get 1,000 times of fv/fm value
    if re.compile("0(\.|,)\d{2}$").match(res[1]): 
        pos = (res[0][3][1] - res[0][0][1]) / 2 + res[0][0][1]
        fvfm_scale.append([pos, float((res[1].replace(',', '.'))) * 1000])

if len(fvfm_scale) >= 2:
    print("keisan suruyo")

else:
    print("taran")

print(fvfm_scale)
fvfm_scale.sort(key=lambda x: x[0])

# Check error value
#for i, fvfm in enumerate(fvfm_scale):
#    if i != 0 and i != len(fvfm_scale):
#        v_prev = fvfm_scale[i-1][1]
#        v = fvfm[1]
#        v_next = fvfm_scale[i+1][1]
#        if v_next < v < v_prev


# Get combination
scale_list = []
for pair in itertools.combinations(fvfm_scale, 2):
    print(pair)
    v1 = pair[0][1]
    v2 = pair[1][1]
    h1 = pair[0][0]
    h2 = pair[1][0]

    if h2 > h1:
        v_def = v1 - v2
        h_def = h2 - h1
        scale = h_def / v_def
        scale_list.append(scale)

scale = statistics.median(scale_list)
print(scale)


# Test calculation
top = 10
bottom = 530
top_v = math.ceil((fvfm_scale[0][0] - top) / scale + fvfm_scale[0][1])
bottom_v = math.ceil(fvfm_scale[-1][1] - (bottom - fvfm_scale[-1][0]) / scale)
print(top_v)
print(bottom_v)

iti = []
for i in range(bottom_v, top_v):
    upper = (fvfm_scale[0][1] - i) * scale + fvfm_scale[0][0]
    lower = (fvfm_scale[-1][1] - i) * scale + fvfm_scale[-1][0]
    ave = round((upper + lower) / 2)
    iti.append([upper, lower, ave])
    print([upper, lower, ave])


#img = cv2.imread(path)
#img_1 = img.copy()

#for i in range(len(res)):
#    cv2.rectangle(img_1, res[i][0][0], res[i][0][2], (0,255,0), 3)

#save("basho.jpeg", img_1)
