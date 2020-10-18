import sys


def VB_encode_number(num):
    arr = bytearray()
    while True:
        b = (num % 128).to_bytes(1, sys.byteorder)
        arr = b + arr
        if num < 128:
            break
        else:
            num = num // 128
    res = arr[:-1]
    res += (arr[-1] + 128).to_bytes(1, sys.byteorder)
    return res


def VB_encode_all(numbers):
    bytestream = bytearray()
    for num in numbers:
        x = VB_encode_number(num)
        bytestream += x
    return bytestream


def VB_decode(bytestream):
    numbers = []
    n = 0
    for b in bytestream:
        if b < 128:
            n = n*128 + b
        else:
            n = n*128 + (b-128)
            numbers.append(n)
            n = 0
    return numbers


# t = VB_encode_all([824, 5])
# print(VB_decode(t))



