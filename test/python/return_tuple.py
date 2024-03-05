def main():
    t1, t2, te = canny("b", "c", "d")
    print(t1)
    print(t2)

def canny(*img: str) -> str:
    ll = []
    if len(img) == 1:
        return img[0]
    else:
        for ss in img:
            ll.append("aa" + ss)
        return tuple(ll)

if __name__ == '__main__':
    main()