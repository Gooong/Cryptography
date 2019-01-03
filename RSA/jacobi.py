import math


def gcd(a, b):
    assert a >= b
    if b < 0:
        return gcd(a, a + b)
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def gcd_with_q(a, b, q=[]):
    if b == 0:
        return q, a
    else:
        q.append(int(a / b))
        return q, gcd_with_q(b, a % b, q=q)[1]


def SquareAndMultiply(x, c, n):
    # x^c mod n
    c_list = [int(i) for i in bin(c)[2:]]
    z = 1
    for ci in c_list:
        z = (z * z) % n
        if ci == 1:
            z = (z * x) % n
    return z


def Jacobi(a, n):
    assert n % 2 == 1
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        if n % 8 == 1 or n % 8 == 7:
            return 1
        else:
            return -1
    elif a > n:
        return Jacobi(a % n, n)
    elif a % 2 == 0:
        return Jacobi(2, n) * Jacobi(int(a / 2), n)
    else:
        if a % 4 == 3 and n % 4 == 3:
            return -Jacobi(n, a)
        else:
            return Jacobi(n, a)


def CountB(n):
    # 找出基b的个数，使得n是相对于b的欧拉伪素数
    assert n % 2 == 1
    count = 0
    c = int((n - 1) / 2)
    for b in range(1, n):
        if gcd(n, b) == 1:
            if abs(Jacobi(b, n)) == 1:
                count = count + 1
                print(b)
    return count


def Pollardp_1(n, B):
    a = 2
    for j in range(2, B + 1):
        a = SquareAndMultiply(a, j, n)
    d = gcd(n, a - 1)
    if (d > 1) and (d < n):
        return d
    else:
        return False


def Pollard_ro(n, x1, f):
    x = x1
    x_ = f(x1) % n
    p = gcd(n, x - x_)
    i = 1
    while p == 1:
        i = i + 1
        x = f(x) % n
        x_ = f(x_) % n
        x_ = f(x_) % n
        p = gcd(n, x - x_)
    if p == n:
        return False
    else:
        return i, p


def Dixon(n, z, B):
    def testA(y, B):
        d_ = dict(zip(B, [0] * len(B)))
        if y < 0:
            y = -y
            d_[-1] += 1

        while True:
            old_y = y
            for i in range(1, len(B)):
                if y % B[i] == 0:
                    d_[B[i]] += 1
                    y = int(y / B[i])
            if y == 1:
                return list(d_.values())
            elif old_y == y:
                return False

    # -1 in B
    # d = dict(zip(B, [0]*len(B)))
    while True:
        y = z * z % n
        r = testA(y, B)
        if r:
            print(z, y, r, sep='\t')
        y = y - n
        r = testA(y, B)
        if r:
            print(z, y, r)
        z += 1


def smallP_Q(n):
    for i in range(100000):
        m = int(math.sqrt(n + i))
        if m * m == n + i:
            return m + i, m - i


def Wiener(n, b):
    q, rm = gcd_with_q(b, n)
    print(q, b)
    c = [1, q[0]]
    d = [0, 1]

    for j in range(2, len(q) + 1):
        cj = q[j - 1] * c[j - 1] + c[j - 2]
        dj = q[j - 1] * d[j - 1] + d[j - 2]
        c.append(cj)
        d.append(dj)
        # print(cj / dj, cj, dj, b, (dj * b - 1) / cj)
        if (dj * b - 1) % cj == 0:
            n_ = int((dj * b - 1) / cj)
            bx = n - n_ + 1
            delta = math.sqrt(bx * bx - 4 * n)
            # print(delta)
            if int(delta) == delta:
                print(bx, n)
                print((bx + delta) / 2, (bx - delta) / 2)
                return delta


###############################
##########第六章################
###############################


def Discrete_Pollard_ro(n, alpha, beta):
    def f(x, a, b):
        if x % 3 == 1:
            return (beta * x) % n, a % n, (b + 1) % n
        elif x % 3 == 0:
            return (x * x) % n, (2 * a) % n, (2 * b) % n
        else:
            return (alpha * x) % n, (a + 1) % n, b % n

    x, a, b = f(1, 0, 0)
    x_, a_, b_ = f(x, a, b)
    i = 1
    while x != x_:
        i = i + 1
        x, a, b = f(x, a, b)
        x_, a_, b_ = f(x_, a_, b_)
        x_, a_, b_ = f(x_, a_, b_)

    if gcd(n, b_ - b) != 1:
        return False
    else:
        print(a - a_, b_ - b)
        return i, (x, a, b), (x_, a_, b_)


if __name__ == '__main__':
    # print(Jacobi(1, 9283))
    # print(SquareAndMultiply(9726, 3533, 11413))
    # print(CountB(8378511189))
    # print(SquareAndMultiply(152702, 907, 1511))
    # print(SquareAndMultiply(152702, 1345, 2003))
    # print(gcd(48, 12))

    # n = 9420457
    # for i in range(10, 200):
    #     d = Pollardp_1(n, i)
    #     if d:
    #         print(i, d)
    #         break
    #
    # n = 181937053
    # print(Pollard_ro(n, 1, lambda x: x * x + 1))

    # print(gcd(256961, 248229 - 42134))
    # n = 256961
    # z = 500
    # B = [-1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    # Dixon(n, z, B)

    # print(smallP_Q(2189284635403183))
    # print(gcd_with_q(75, 28))
    # print(Wiener(160523347, 60728973))
    # print(Wiener(317940011, 77537081))

    print(Discrete_Pollard_ro(809, 89, 618))
    print(Discrete_Pollard_ro(458009, 2, 56851))
    print(SquareAndMultiply(2, 25788, 458009))
    for i in range(1, 57251):
        if SquareAndMultiply(2, i, 458009) == 56851:
            print(i)
