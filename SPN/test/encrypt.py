from SPN.SPN import do_SPN


def encrypt(x, K):
    # S盒参数
    S_Box = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]

    # P盒参数
    P_Box = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    return do_SPN(x, S_Box, P_Box, K)


if __name__ == '__main__':
    x = 0b0010011010110111
    K = 0b00111010100101001101011000111111
    assert encrypt(x, K) == 0b1011110011010110
    # print(bin(encrypt(x, K)))
