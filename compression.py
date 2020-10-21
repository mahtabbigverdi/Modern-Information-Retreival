import sys


####### Variable length encoding:
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
            n = n * 128 + b
        else:
            n = n * 128 + (b - 128)
            numbers.append(n)
            n = 0
    return numbers


####### Gamma encoding:
def gamma_encode_number(num):
    binary_num = format(num, 'b')
    binary_num = binary_num[1:]
    length = '1' * (len(binary_num)) + '0'
    res = length + binary_num
    return res


def gamma_encode_all(numbers):
    bytestream = ''
    for num in numbers:
        x = gamma_encode_number(num)
        bytestream += x
    return bytestream


def gamma_decode(bits):
    numbers = []
    i = 0
    last = 0
    while i < len(bits):
        if bits[i] == '0':
            length = i - last
            offset = '1' + bits[i + 1:i + length + 1]
            numbers += [int(offset, 2)]
            i += length + 1
            last = i
        else:
            i += 1
    return numbers

# t = VB_encode_all([824, 5])
# print(VB_decode(t))

# t = gamma_encode_all([1025, 9, 4, 3])
# print(gamma_decode(t))
