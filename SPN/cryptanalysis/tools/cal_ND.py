# 计算整个ND表
def cal_nd(s_box):
    ND = []
    for i in range(16):
        ND.append([0] * 16)
    for i in range(16):
        for j in range(16):
            a = i ^ j
            b = s_box[i] ^ s_box[j]
            ND[a][b] = ND[a][b] + 1
    return ND

if __name__ == '__main__':
    s_box = [14, 2, 1, 3, 13, 9, 0, 6, 15, 4, 5, 10, 8, 12, 7, 11]
    ND = cal_nd(s_box)

    print('b=', end='\t')
    print('\t'.join([hex(i)[2].upper() for i in range(16)]))
    for i in range(16):
        print('a=' + hex(i)[2].upper() + '\t' + '\t'.join([str(tmp) for tmp in ND[i]]))
