def invRotationMatrix(in_m):
    m = [x[:] for x in in_m]
    det = m[0][0] * (m[1][1] * m[2][2] - m[2][1] * m[1][2]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    if det == 0:
        return m
    invdet = 1.0 / det
    m[0][0] = (m[1][1] * m[2][2] - m[2][1] * m[1][2]) * invdet
    m[0][1] = (m[0][2] * m[2][1] - m[0][1] * m[2][2]) * invdet
    m[0][2] = (m[0][1] * m[1][2] - m[0][2] * m[1][1]) * invdet
    m[1][0] = (m[1][2] * m[2][0] - m[1][0] * m[2][2]) * invdet
    m[1][1] = (m[0][0] * m[2][2] - m[0][2] * m[2][0]) * invdet
    m[1][2] = (m[1][0] * m[0][2] - m[0][0] * m[1][2]) * invdet
    m[2][0] = (m[1][0] * m[2][1] - m[2][0] * m[1][1]) * invdet
    m[2][1] = (m[2][0] * m[0][1] - m[0][0] * m[2][1]) * invdet
    m[2][2] = (m[0][0] * m[1][1] - m[1][0] * m[0][1]) * invdet
    return m


def transformNodeWithParent(parent, child):
    result = [x[:] for x in parent]
    result = invRotationMatrix(result)
    for i in range(3):
        for j in range(3):
            sum = 0
            for k in range(3):
                sum = sum + parent[i][k] * child[k][j]
            result[i][j] = sum
    result[3][0] = parent[3][0] + child[3][0]
    result[3][1] = parent[3][1] + child[3][1]
    result[3][2] = parent[3][2] + child[3][2]
    return result
