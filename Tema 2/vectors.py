

def vec(i, l):
    res = []
    for idx in range(l):
        res.append(i)
    return res


def mul(v, i):
    res = []
    for idx, val in enumerate(v):
        t = v[idx] * i
        res.append(t)
    return res


def add(vx, vy):
    res = []

    lx = len(vx)
    ly = len(vy)
    l = min(lx, ly)
    for i in range(l):
        t = vx[i] + vy[i]
        res.append(t)
    return res


def dot(vx, vy):
    res = 0
    lx = len(vx)
    ly = len(vy)
    l = min(lx, ly)
    for i in range(l):
        t = vx[i] * vy[i]
        res += t
    return res
