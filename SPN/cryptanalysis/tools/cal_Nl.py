# 计算Nl(a,b)
def cal_nl(a, b):
    result = 0
    for i in range(16):
        c = (i & a) ^ (pi_s[i] & b)
        r = 1
        while c:
            r = r ^ (c % 2)
            c = c >> 1
        result = result + r
    return result


if __name__ == '__main__':
    pi_s = [8, 4, 2, 1, 12, 6, 3, 13, 10, 5, 14, 7, 15, 11, 9, 0]
    assert len(pi_s) == 16
    print('b=', end='')
    for b in range(16):
        print('\t'+hex(b)[2].upper(), end='')
    print('')
    for a in range(16):
        print('a=' + hex(a)[2].upper() + '\t', end='')
        for b in range(16):
            print(str(cal_nl(a, b)) + '\t', end='')
        print('')
