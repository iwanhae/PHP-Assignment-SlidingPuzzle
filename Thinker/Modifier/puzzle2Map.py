import numpy as np
import math


def puzzle2Map(data: np.ndarray):
    map = np.zeros((22, 22))
    (row, col) = data.shape
    (r, c) = np.where(data == 0)
    (r, c) = (r[0], c[0])
    for i in range(row):
        for j in range(col):
            (rm, cm) = ((i + 5 - r)*2, (j + 5 - c)*2)  # map
            if 0 <= rm and rm < 22 and 0 <= cm and cm < 22:
                v = data[i][j]
                (rd, cd) = (math.floor(v / col), v % col)  # destination
                (rg, cg) = (rd - i, cd - j)       # gap
                if 0 < rg:
                    map[rm + 1][cm] += rg / row
                    map[rm + 1][cm + 1] += rg / row
                else:
                    map[rm][cm] -= rg / row
                    map[rm][cm + 1] -= rg / row
                if 0 < cg:
                    map[rm][cm + 1] += cg / col
                    map[rm + 1][cm + 1] += cg / col
                else:
                    map[rm][cm] -= cg / col
                    map[rm + 1][cm] -= cg / col

    (rs, cs) = ((5 - r) * 2 - 1, (5 - c) * 2 - 1)
    
#    for i in range((col + 1) * 2):
#        (r1, c1) = (rs + col * 2 + 1, cs + i)
#        if 0 <= c1 and c1 < 22:
#            if 0 <= rs and rs < 22:
#                map[rs][c1] = -1
#            if 0 <= r1 and r1 < 22:
#                map[r1][c1] = -1
#    for i in range((row + 1) * 2):
#        (r1, c1) = (rs + i, cs + row * 2 + 1)
#        if 0 <= r1 and r1 < 22:
#            if 0 <= cs and cs < 22:
#                map[r1][cs] = -1
#            if 0 <= c1 and c1 < 22:
#                map[r1][c1] = -1
    return map
