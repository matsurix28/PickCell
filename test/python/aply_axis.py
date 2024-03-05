import numpy as np

def main():
    a = np.arange(12).reshape(3,2,2)
    print(a)
    np.apply_along_axis(kensan, 1, a)
    

def kensan(ina):
    print(ina)
    print(' ')
    return ina

if __name__ == '__main__':
    main()