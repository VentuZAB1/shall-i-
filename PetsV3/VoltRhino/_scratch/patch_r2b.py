import os
p = os.path.join(os.path.dirname(__file__), "..", "..", "pets", "VoltRhino.py")
s = open(p, encoding="utf-8").read()


def R(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:80])
    s = s.replace(a, b)


# smooth tube horn (no segment seams), base collar + 2 growth rings, zig on the flat-ish sides
a = s.index("    b0, h1, h2, tip = horn_pts()\n    B.seg(b0, h1,")
b = s.index("    B.spike((0, -1.22, 1.11), (0, -0.40, 1.0), 0.21, 0.050, HORN_IVORY")
s = s[:a] + '''    C, A, D, W, H = horn_curve()
    B.tube(horn_rings(C, A, D, W, H), HORN_IVORY, "Head", nostud=True)
    # horn root collar (review 1 M6) + 2 thin growth rings on the upper horn (NICE)
    for t0, t1, g in ((0.05, 0.13, 0.014), (0.47, 0.51, 0.008), (0.66, 0.70, 0.008)):
        i0, i1 = int(t0 * (len(C) - 1)), int(math.ceil(t1 * (len(C) - 1)))
        B.tube(horn_rings(C[i0:i1 + 1], A[i0:i1 + 1], D[i0:i1 + 1], [w + g for w in W[i0:i1 + 1]],
                          [h + g for h in H[i0:i1 + 1]]), HORN_SHADE, "Head", nostud=True)
    # lightning down each flat-ish side of the horn (3 zigzag segments + a point)
    for s in (1, -1):
        Q = []
        for t, dz in ((0.16, 0.045), (0.34, -0.040), (0.56, 0.032), (0.74, -0.026), (0.86, 0.010)):
            i = t * (len(C) - 1)
            j = min(int(i), len(C) - 2)
            u = i - j
            c = C[j].lerp(C[j + 1], u)
            ax = A[j].lerp(A[j + 1], u).normalized()
            dv = D[j].lerp(D[j + 1], u).normalized()
            hw = W[j] + (W[j + 1] - W[j]) * u
            Q.append((c + ax * s * (hw + 0.004) + dv * dz, ax * s))
        zig(B, Q, VOLT, "Head", 0.060, thick=0.013)
''' + s[b:]
# helpers after horn_pts
R('''    return b0, h1, h2, tip
''', '''    return b0, h1, h2, tip


def _cr(p0, p1, p2, p3, t):
    t2, t3 = t * t, t * t * t
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3)


def horn_curve(n=18):
    """smooth horn centreline through horn_pts (Catmull-Rom), per-sample side axis A (x), fore-aft axis D, half
    width W (along A) and half depth H; the base starts buried in the nose"""
    P = list(horn_pts())
    P[0] = P[0] - (P[1] - P[0]).normalized() * 0.05
    E = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    seg = len(P) - 1
    C = []
    for i in range(n + 1):
        u = i / n * seg
        j = min(int(u), seg - 1)
        C.append(_cr(E[j], E[j + 1], E[j + 2], E[j + 3], u - j))
    A, D, W, H = [], [], [], []
    for i, c in enumerate(C):
        d = (C[min(i + 1, n)] - C[max(i - 1, 0)]).normalized()
        ax = Vector((1, 0, 0))
        ax = (ax - d * ax.dot(d)).normalized()
        A.append(ax)
        D.append(d.cross(ax).normalized())
        t = i / n
        W.append(0.112 * (1 - t ** 1.35) + 0.005)
        H.append(0.120 * (1 - t ** 1.35) + 0.005)
    return C, A, D, W, H


def horn_rings(C, A, D, W, H, m=16, n_se=3.0):
    """superellipse rings (flat-ish sides for the lightning inlay) around the horn centreline"""
    rings = []
    for c, ax, dv, w, h in zip(C, A, D, W, H):
        r = []
        for j in range(m):
            a = 2 * math.pi * j / m
            cx, sz = math.cos(a), math.sin(a)
            r.append(c + ax * (w * math.copysign(abs(cx) ** (2 / n_se), cx)) +
                     dv * (h * math.copysign(abs(sz) ** (2 / n_se), sz)))
        rings.append(r)
    return rings
''')
# pale band ends taper to points (no white rim at the chest front / rump)
R('''    Lb.band(B, sy(-0.84), sj, PALE, "Chest", zlo=-1.0, zhi=-0.46, grow=0.008, step=0.06)
    Lb.band(B, sj, sy(0.80), PALE, "Spine", zlo=-1.0, zhi=-0.46, grow=0.008, step=0.06)''',
  '''    Lb.band(B, sy(-0.80), sy(-0.56), PALE, "Chest", zlo=-1.0, zhi=-0.92, zhi1=-0.46, grow=0.008, step=0.04)
    Lb.band(B, sy(-0.56), sj, PALE, "Chest", zlo=-1.0, zhi=-0.46, grow=0.008, step=0.06)
    Lb.band(B, sj, sy(0.56), PALE, "Spine", zlo=-1.0, zhi=-0.46, grow=0.008, step=0.06)
    Lb.band(B, sy(0.56), sy(0.82), PALE, "Spine", zlo=-1.0, zhi=-0.46, zhi1=-0.92, grow=0.008, step=0.04)''')
# soft pale chin set into the jaw bottom (no flat board)
R('''    B.seg((0, -1.20, 0.684), (0, -1.63, 0.684), 0.105, 0.014, PALE, "Jaw", top=(0.9, 1), studs=[])     # chin''',
  '''    B.seg((0, -1.18, 0.703), (0, -1.56, 0.698), 0.10, 0.022, PALE, "Jaw", top=(0.85, 1), rnd=0.45, studs=[])  # chin''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
