# axis-angle -> kit Euler (pitch, yaw, roll) for Rq = Rz(yaw) Rx(pitch) Ry(roll), degrees (plain python)
import math


def axis_euler(axis, deg):
    x, y, z = axis
    L = math.sqrt(x * x + y * y + z * z)
    x, y, z = x / L, y / L, z / L
    t = math.radians(deg)
    c, s, C = math.cos(t), math.sin(t), 1 - math.cos(t)
    R = [[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
         [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
         [z * x * C - y * s, z * y * C + x * s, c + z * z * C]]
    p = math.asin(max(-1, min(1, R[2][1])))
    r = math.atan2(-R[2][0], R[2][2])
    yw = math.atan2(-R[0][1], R[1][1])
    return tuple(round(math.degrees(v), 2) for v in (p, yw, r))


if __name__ == "__main__":
    import sys
    ax = tuple(float(v) for v in sys.argv[1].split(","))
    print(axis_euler(ax, float(sys.argv[2])))
