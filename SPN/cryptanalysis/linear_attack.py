from random import randrange

from SPN.SPN import gen_K_list
from SPN.SPN import reverse_Sbox
from SPN.tools.gen_pair import gen_pair

# SPN加密参数
s_box = [8, 4, 2, 1, 12, 6, 3, 13, 10, 5, 14, 7, 15, 11, 9, 0]
# S盒的逆
s_rebox = reverse_Sbox(s_box)
p_box = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]


# 对候选子密钥计算差分值
def cal_xuu(k5_1, k5_3, pair):
    p = pair[0]
    c = pair[1]

    X16 = p % 2

    y_1 = c >> 12
    v4_1 = y_1 ^ k5_1
    u4_1 = s_rebox[v4_1]
    U4_1 = u4_1 >> 3

    y_3 = (c >> 4) % (2 ** 4)
    v4_3 = y_3 ^ k5_3
    u4_3 = s_rebox[v4_3]
    U4_9 = u4_3 >> 3

    return X16 ^ U4_1 ^ U4_9


if __name__ == '__main__':
    # 真实密钥
    K = randrange(0, 2 ** 32)
    k5 = gen_K_list(K)[4]
    k5_1 = k5 >> 12
    k5_3 = (k5 >> 4) % (2 ** 4)
    real_kp = (k5_1, k5_3)
    print("真实子密钥:" + str(real_kp))

    # 候选子密钥
    dic = {}
    for i in range(2 ** 4):
        for j in range(2 ** 4):
            dic[(i, j)] = 0

    # 计数
    print("明文-密文数T\t猜测密钥\t偏差值")
    for i, cp in enumerate(gen_pair(s_box, p_box, K)):
        for kp in dic:
            if cal_xuu(kp[0], kp[1], cp) == 0:
                dic[kp] = dic[kp] + 1

        # 分析密钥
        if i % 200 == 0 and i > 0:
            score = {}
            for kp in dic:
                score[kp] = abs(dic[kp] / i - 0.5)
            fk = sorted(score.items(), key=lambda item: item[1], reverse=True)[0]
            print("%d\t%s\t%5f" % (i, fk[0], fk[1]))
        if i >= 2000:
            break
