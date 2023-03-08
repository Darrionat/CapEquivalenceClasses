from cap import *
from pyfinite import ffield

if __name__ == '__main__':
    taiwon4 = [0, 5, 6, 7]
    taitwon6 = [0, 9, 26, 35, 44, 53, 62, 23]
    taitwon8 = [0, 17, 130, 243, 196, 165, 22, 23, 168, 249, 250, 203, 140, 173, 142, 207]
    cap = taitwon8
    dim = dimension(cap)
    assert dim % 2 == 0

    if dim == 4:
        for p in cap:
            left = p & 0b1100
            binLeft = "{0:b}".format(left)
            paddedBin = binLeft.rjust(dim, '0')
            newNum = paddedBin[0:int(dim / 2)]

            left = int(newNum, 2)
            right = p & 0b0011
            print(left, right)
    if dim == 6:
        for p in cap:
            left = p & 0b111000
            binLeft = "{0:b}".format(left)
            paddedBin = binLeft.rjust(dim, '0')
            newNum = paddedBin[0:int(dim / 2)]

            left = int(newNum, 2)
            right = p & 0b000111
            print(left, right)

    F = ffield.FField(int(dim / 2))
    for x in range(0, 16):
        xcubed = F.Multiply(F.Multiply(x, x), x)
        print(xcubed)

    if dim == 8:
        for p in cap:
            left = p & 0b11110000
            binLeft = "{0:b}".format(left)
            paddedBin = binLeft.rjust(dim, '0')
            newNum = paddedBin[0:int(dim / 2)]

            left = int(newNum, 2)
            right = p & 0b00001111
            print(left, right)
