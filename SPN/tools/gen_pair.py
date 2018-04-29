from SPN.SPN import do_SPN
from random import randrange


# 随机数生成器，每次取出不同的随机数
def sample_generator(n):
    pool = {}
    for i in range(n):
        j = randrange(n - i)
        result = pool.get(j, j)
        pool[j] = pool.get(n - i - 1, n - i - 1)
        yield result


# 生成密钥k的明文-密文对
def gen_pair(s_box, p_box, k):
    m = 2 ** 16
    for p in sample_generator(m):
        c = do_SPN(p, s_box, p_box, k)
        yield (p, c)


# 生成密钥为k，明文具有固定异或值x_的两个明文密文对((x, y),(x_star, y_star))
def gen_two_pairs(x_, s_box, p_box, k):
    m = 2 ** 16
    x_star_set = set()
    for p in sample_generator(m):
        if p in x_star_set:
            continue
        else:
            x = p
            x_star = x ^ x_
            x_star_set.add(x_star)
            y = do_SPN(x, s_box, p_box, k)
            y_star = do_SPN(x_star, s_box, p_box, k)
            yield ((x, y), (x_star, y_star))
