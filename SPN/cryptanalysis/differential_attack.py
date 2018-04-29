# SPN的差分攻击
from random import randrange

from SPN.SPN import gen_K_list
from SPN.SPN import reverse_Sbox
from SPN.tools.gen_pair import gen_two_pairs

# SPN加密参数
s_box = [14, 2, 1, 3, 13, 9, 0, 6, 15, 4, 5, 10, 8, 12, 7, 11]
# S盒的逆
s_rebox = reverse_Sbox(s_box)
p_box = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]

x_ = 0b1001000000001001
u4_ = 0b0001000100000000
_u4_1_ = 0b0001
_u4_2_ = 0b0001


# 判断实际的差分值是否与差分链中预测的相等
def is_match(k5_1, k5_2, y, y_star):
    # 过滤操作
    if (y % (2 ** 8)) != (y_star % (2 ** 8)):
        return False

    y_1 = y >> 12
    y_2 = (y >> 8) % (2 ** 4)
    y_1_star = y_star >> 12
    y_2_star = (y_star >> 8) % (2 ** 4)

    v4_1 = y_1 ^ k5_1
    v4_2 = y_2 ^ k5_2
    v4_1_star = y_1_star ^ k5_1
    v4_2_star = y_2_star ^ k5_2

    u4_1 = s_rebox[v4_1]
    u4_2 = s_rebox[v4_2]
    u4_1_star = s_rebox[v4_1_star]
    u4_2_star = s_rebox[v4_2_star]

    u4_1__ = u4_1 ^ u4_1_star
    u4_2__ = u4_2 ^ u4_2_star
    return (u4_1__ == _u4_1_) and (u4_2__ == _u4_2_)


if __name__ == '__main__':
    # 真实密钥
    K = randrange(0, 2 ** 32)
    k5 = gen_K_list(K)[4]
    k5_1 = k5 >> 12
    k5_2 = (k5 >> 8) % (2 ** 4)
    real_kp = (k5_1, k5_2)
    print("真实子密钥:" + str(real_kp))

    # 候选子密钥
    dic = {}
    for i in range(2 ** 4):
        for j in range(2 ** 4):
            dic[(i, j)] = 0

            # 计数
    print("明文-密文数T\t猜测密钥\t扩散率")
    for i, two_cp in enumerate(gen_two_pairs(x_, s_box, p_box, K)):
        for kp in dic:
            if is_match(kp[0], kp[1], two_cp[0][1], two_cp[1][1]):
                dic[kp] = dic[kp] + 1

                # 分析密钥
        if i % 50 == 0 and i > 0:
            score = {}
            for kp in dic:
                score[kp] = dic[kp] / i
            fk = sorted(score.items(), key=lambda item: item[1], reverse=True)[0]
            print("%d\t%s\t%5f" % (i, fk[0], fk[1]))
        if i >= 500:
            break
