import numpy as np

def main():
    l = np.arange(12).reshape(3,2,2)
    ll = np.frompyfunc(keisn, 1, 0)
    a = ll(l)
    print(a)

def keisn(ina):
    print(ina)
    return ina

if __name__ == '__main__':
    main()