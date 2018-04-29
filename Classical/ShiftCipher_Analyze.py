from Classical.ShiftCipher import _move_leter, Decrypt


def analyze(c):
    """
    移位密码分析
    :param c: 密文c
    :return:
    """
    for k in range(26):
        # 用不同的秘钥k尝试解密
        print('秘钥%d：' % k + Decrypt(k, c))


if __name__ == '__main__':
    c = 'jmpwfdpejoh'
    analyze(c)
