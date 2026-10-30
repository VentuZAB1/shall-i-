# Plain-python forward kinematics of the Thornblade Mantis raptorial arm (kit semantics: every key is a rotation in
# ARMATURE axes about the bone head, Rq = Rz(yaw) Rx(pitch) Ry(roll), composed down the chain) - used to solve the
# review-3 C1 / C2 world-space targets before pose_try verifies them in Blender.
import math, itertools, sys

S0 = (0, 0.04, 0.44)
P0 = (0, -0.06, 0.52)
HEADP = (0, -0.45, 1.02)
NECK = (0, -0.40, 0.96)
HC = (0, -0.52, 1.14)
C0 = (0.08, -0.30, 0.84)
C1 = (0.17, -0.46, 0.62)
F1 = (0.21, -0.64, 1.00)
T1 = (0.20, -0.73, 0.66)
KS = (0.21, -0.64, 1.03)          # knee-spine base (F1 + 0.03 z), spine dir (0.7, 0.5, 0.5) * 0.11


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, k):
    return tuple(x * k for x in a)


def norm(a):
    L = math.sqrt(sum(x * x for x in a))
    return tuple(x / L for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rot(p, y, r):
    """R = Rz(y) Rx(p) Ry(r) (degrees) as a function on vectors"""
    p, y, r = (math.radians(v) for v in (p, y, r))

    def f(v):
        x, yy, z = v
        x, z = x * math.cos(r) + z * math.sin(r), -x * math.sin(r) + z * math.cos(r)          # Ry
        yy, z = yy * math.cos(p) - z * math.sin(p), yy * math.sin(p) + z * math.cos(p)        # Rx
        x, yy = x * math.cos(y) - yy * math.sin(y), x * math.sin(y) + yy * math.cos(y)        # Rz
        return (x, yy, z)
    return f


def about(R, h):
    return lambda p: add(h, R(sub(p, h)))


def arm_chain(body=dict(), up=0.0, out=0.0, fore=0.0, blade=0.0, s=1):
    """returns world positions of C1 (elbow), F1 (knee), T1 (tibia tip), KS tip, for side s (+1 = L)"""
    sp = about(rot(body.get("pitch", 0), body.get("yaw", 0), body.get("roll", 0)), S0)
    ch = about(rot(-body.get("chest", 0), body.get("chest_yaw", 0), 0), P0)
    loc = (body.get("x", 0), body.get("y", 0), body.get("z", 0))
    m = lambda p: (s * p[0], p[1], p[2])
    ar = about(rot(-up, s * out, 0), m(C0))
    fo = about(rot(-fore, 0, 0), m(C1))
    bl = about(rot(-blade, 0, 0), m(F1))

    def W(p, depth):
        q = m(p)
        for i, T in enumerate((bl, fo, ar, ch, sp)):
            if 5 - i <= depth:
                q = T(q)
        return add(q, loc)
    ks_tip = add(KS, mul(norm((0.7, 0.5, 0.5)), 0.11))
    return {"C1": W(C1, 3), "F1": W(F1, 4), "T1": W(T1, 5), "KS": W(ks_tip, 4)}


def head_world(body=dict(), up=0.0, yaw=0.0):
    sp = about(rot(body.get("pitch", 0), body.get("yaw", 0), body.get("roll", 0)), S0)
    ch = about(rot(-body.get("chest", 0), body.get("chest_yaw", 0), 0), P0)
    nk = max(-8.0, min(8.0, up / 3.0))
    ne = about(rot(-nk, yaw * 0.3, 0), NECK)
    hd = about(rot(-(up - nk), yaw * 0.7, 0), HEADP)
    loc = (body.get("x", 0), body.get("y", 0), body.get("z", 0))
    return lambda p: add(sp(ch(ne(hd(p)))), loc)


def angles(c):
    fd = sub(c["F1"], c["C1"])
    td = sub(c["T1"], c["F1"])
    elev_f = math.degrees(math.atan2(fd[2], math.hypot(fd[0], fd[1])))
    inner = math.degrees(math.acos(max(-1, min(1, dot(norm(mul(fd, -1)), norm(td))))))
    return elev_f, inner


if __name__ == "__main__":
    print("rest", arm_chain(), angles(arm_chain()))
