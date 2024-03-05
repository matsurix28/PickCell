from functools import singledispatchmethod
from typing import overload
from multimethod import multidispatch

def main():
    ttt = Testes()
    res = ttt.canny(7)
    print(str(res))

class Testes:
    def __init__(self) -> None:
        pass
    def lll(self):
        print('yeah')


    
    def canny(self, img: str) -> str:
        return 'moji'
    
    @canny.register
    def _canny(self, img: int) -> int:
        return 5
    
    
    

if __name__ == '__main__':
    main()