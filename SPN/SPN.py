# S盒参数
S_Box = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]

# P盒参数
P_Box = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]


def gen_K_list(K):
    """
    秘钥编排算法，由一个32比特秘钥生成5个16比特子秘钥
    :param K: 32比特秘钥
    :return: [k1,k2,k3,k4,k5]，五个16比特子秘钥
    """
    Ks = []
    for i in range(5, 0, -1):
        ki = K % (2 ** 16)
        Ks.insert(0, ki)
        K = K >> 4
    return Ks


def pi_s(s_box, ur):
    """
    分组代换操作
    :param s_box:S盒参数
    :param ur:输入比特串，16比特
    :return:输出比特串，16比特
    """
    vr = 0
    for i in range(4):
        uri = ur % (2 ** 4)
        vri = s_box[uri]
        vr = vr + (vri << (4 * i))
        ur = ur >> 4
    return vr


def pi_p(p_box, vr):
    """
    单比特置换操作
    :param p_box:P盒参数
    :param vr:输入比特串，16比特
    :return:输出比特串，16比特
    """
    wr = 0
    for i in range(15, -1, -1):
        vri = vr % 2
        vr = vr >> 1
        wr = wr + (vri << (16 - p_box[i]))
    return wr


def reverse_Sbox(s_box):
    """
    求S盒的逆
    :param s_box:S盒参数
    :return:S盒的逆
    """
    re_box = [-1] * 16
    for i in range(16):
        re_box[s_box[i]] = i
    return re_box


def reverse_Pbox(p_box):
    """
    求P盒的逆
    :param s_box:P盒参数
    :return:P盒的逆
    """
    re_box = [-1] * 16
    for i in range(16):
        re_box[p_box[i] - 1] = i + 1
    return re_box


def do_SPN(x, s_box, p_box, Ks):
    """
    4轮的SPN网络，可以用来进行加密或解密
    :param x: 16比特输入
    :param s_box: S盒参数
    :param p_box: P盒参数
    :param Ks: [k1,k2,k3,k4,k5]，五个16比特子秘钥
    :return: 16比特输出
    """
    wr = x
    for r in range(3):
        ur = wr ^ Ks[r]  # 异或操作
        vr = pi_s(s_box, ur)  # 分组代换
        wr = pi_p(p_box, vr)  # 单比特置换

    ur = wr ^ Ks[3]
    vr = pi_s(s_box, ur)
    y = vr ^ Ks[4]
    return y


def encrypt(K, x):
    """
    根据秘钥K对16比特明文x进行加密
    :param K:32比特秘钥
    :param x:16比特明文
    :return:16比特密文
    """
    Ks = gen_K_list(K)
    return do_SPN(x, S_Box, P_Box, Ks)


def decrypt(K, y):
    """
    根据秘钥K对16比特密文y进行解密。
    :param K:32比特秘钥
    :param y:16比特密文
    :return:16比特明文
    """
    Ks = gen_K_list(K)
    Ks.reverse()  # 秘钥逆序编排
    # 秘钥置换
    Ks[1] = pi_p(P_Box, Ks[1])
    Ks[2] = pi_p(P_Box, Ks[2])
    Ks[3] = pi_p(P_Box, Ks[3])

    s_rbox = reverse_Sbox(S_Box)  # S盒求逆
    p_rbox = reverse_Pbox(P_Box)  # P盒求逆
    return do_SPN(y, s_rbox, p_rbox, Ks)


if __name__ == '__main__':
    x = 0b0010011010110111
    K = 0b00111010100101001101011000111111
    print('初始明文：', format(x, '016b'))
    print('加密密文：', format(encrypt(K, x), '016b'))
    print('解密结果：', format(decrypt(K, encrypt(K, x)), '016b'))
    assert decrypt(K, encrypt(K, x)) == x
