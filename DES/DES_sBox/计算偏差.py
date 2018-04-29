from fractions import Fraction


def read_sbox(i):
    numbers = []
    f = open(str(i) + '.txt', 'r')  # 读取s盒的内容
    for line in f.readlines():
        line = line.strip()
        if line:
            numbers.append(int(line))
    return numbers


def cal(j):
    numbers = read_sbox(j)
    assert len(numbers) == 64
    zero_number = 0
    for i in range(64):
        x2 = (i % 16) >> 3
        y1 = numbers[i] >> 3
        y2 = (numbers[i] & 0b0100) >> 2
        y3 = (numbers[i] & 0b0010) >> 1
        y4 = (numbers[i] & 0b0001)
        result = x2 ^ y1 ^ y2 ^ y3 ^ y4
        assert result == 0 or result == 1
        if result == 0:
            zero_number = zero_number + 1
    print(j, Fraction(zero_number / 64.0 - 0.5))


if __name__ == '__main__':
    for i in range(1, 9):
        cal(i)
