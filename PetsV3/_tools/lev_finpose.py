import math, sys
A = (math.cos(math.radians(65)) * math.cos(math.radians(14)), math.sin(math.radians(65)) * math.cos(math.radians(14)),
     math.sin(math.radians(14)))


def rot_axis(ax, deg):
    x, y, z = ax
    L = math.sqrt(x * x + y * y + z * z)
    x, y, z = x / L, y / L, z / L
    t = math.radians(deg)
    c, s, C = math.cos(t), math.sin(t), 1 - math.cos(t)
    return [[c + x * x * C, x * y * C - z * s, x * z * C + y * s], [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
            [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def fin_pose(up, back, s=1):
    R = mm(rot_axis((0, 0, 1), s * back), rot_axis((s * A[0], A[1], A[2]), -s * up))
    p = math.asin(max(-1, min(1, R[2][1])))
    return tuple(round(math.degrees(v), 2) for v in (p, math.atan2(-R[0][1], R[1][1]), math.atan2(-R[2][0], R[2][2])))


if __name__ == "__main__":
    for tok in sys.argv[1:]:
        lab, up, back = tok.split(":")
        p, y, r = fin_pose(float(up), float(back))
        print("%s=Fin_{s}:%g,%g,%g" % (lab, p, y, r))
