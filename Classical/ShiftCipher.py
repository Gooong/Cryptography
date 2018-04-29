# 移位密码

def _move_leter(letter, n):
    """
    把字母变为字母表后n位的字母,z后面接a
    :param letter: 小写字母
    :param n: 要移动的字母
    :return: 移动的结果
    """
    return chr((ord(letter) - ord('a') + n) % 26 + ord('a'))


def Encrypt(k, p):
    """
    移位密码加密函数E
    :param k: 秘钥k,每个字母在字母表中移动k位
    :param p: 明文p
    :return: 密文c
    """
    letter_list = list(p.lower())
    c = ''.join([_move_leter(x, k) for x in letter_list])
    return c


def Decrypt(k, c):
    """
    移位密码解密函数D
    :param k: 秘钥k,每个字母在字母表中移动k位
    :param c: 密文c
    :return: 明文p
    """
    letter_list = list(c.lower())
    p = ''.join([_move_leter(x, -k) for x in letter_list])
    return p


def analyze(c):
    """
    移位密码分析
    :param c: 密文c
    :return:
    """
    for k in range(26):
        print(Decrypt(k, c))


if __name__ == '__main__':
    p = 'ilovecoding'
    print('明文：' + p)
    print('密文：' + Encrypt(1, p))
    print('解密：' + Decrypt(1, Encrypt(1, p)))
    assert Decrypt(1, Encrypt(1, p)) == p

    analyze(Encrypt(1, p))
