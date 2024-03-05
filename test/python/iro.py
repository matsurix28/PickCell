import cv2
import numpy as np

def main():
    img1 = cv2.imread('./1.png')
    img2 = cv2.imread('./2.png')
    h,w = img1.shape[:2]
    d1_1 = np.reshape(img1, (h * w, 3))
    d1_2 = np.reshape(img2, (h * w, 3))
    taiouhyo = []
    for (fvfm, leaf) in zip(d1_1, d1_2):
        if not (np.sum(fvfm) == 0) and not (np.sum(leaf) == 0):
            taiouhyo.append([fvfm.tolist(), leaf.tolist()])

    print(taiouhyo[0][1])


if __name__ == '__main__':
    main()
