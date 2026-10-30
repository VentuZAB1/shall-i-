p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
t = open(p, encoding="utf-8").read()
rep = [
('''def body_seg(B, a, b, r0, r1, bone, color=None, ext0=0.0, ext1=0.0, flat=0.92, up=(0, 0, 1), cap=True):
    """smooth lofted body segment from a to b (radius r0 -> r1), ends extended + rounded to overlap neighbours"""
    a, b = Vector(a), Vector(b)
    d = (b - a).normalized()
    side, upv = frame_of(d, up)
    st = []
    if cap and ext0 > 0:
        st += [(-ext0, 0.55), (-ext0 * 0.55, 0.88)]
    st += [(0.0, 1.0), (0.5, 1.0), (1.0, 1.0)]
    if cap and ext1 > 0:
        st += [(1.0 + ext1 * 0.55 / max((b - a).length, 1e-6), 0.88), (1.0 + ext1 / max((b - a).length, 1e-6), 0.55)]
    rings = []
    L = (b - a).length
    for t, k in st:
        tt = t if t >= 0 else t / L
        tt = t if (0 <= t <= 1 or t > 1) else t / L
        c = a + d * (tt * L) if t >= 0 else a + d * t
        r = (r0 + (r1 - r0) * max(0.0, min(1.0, tt))) * k
        rings.append(oval(c, side, upv, r, r * flat))
    return B.tube(rings, color or PLUM_OBS, bone)''',
'''def body_seg(B, a, b, r0, r1, bone, color=None, ext0=0.0, ext1=0.0, flat=0.92, up=(0, 0, 1)):
    """smooth lofted body segment from a to b (radius r0 -> r1), ends extended + rounded to overlap neighbours"""
    a, b = Vector(a), Vector(b)
    L = (b - a).length
    d = (b - a) / L
    side, upv = frame_of(d, up)
    st = []                                              # (distance from a, radius factor, radius interpolation)
    if ext0 > 0:
        st += [(-ext0, 0.55, 0.0), (-ext0 * 0.55, 0.88, 0.0)]
    st += [(0.0, 1.0, 0.0), (L * 0.5, 1.0, 0.5), (L, 1.0, 1.0)]
    if ext1 > 0:
        st += [(L + ext1 * 0.55, 0.88, 1.0), (L + ext1, 0.55, 1.0)]
    rings = []
    for dist, kf, tt in st:
        r = (r0 + (r1 - r0) * tt) * kf
        rings.append(oval(a + d * dist, side, upv, r, r * flat))
    return B.tube(rings, color or PLUM_OBS, bone)'''),
('''    B.poly([c] + pts + [pts[0]] if False else pts, t, OBS_D, bone)
    # gold frame along the two upper edges and the two sides (front face, proud), gold-dark on the back face
    nrm = back_d.cross(side).normalized() if False else (-back_d).normalized()''',
'''    B.poly(pts, t, OBS_D, bone)
    # gold frame along the two upper edges and the two sides (front face, proud)
    nrm = up_d.cross(side).normalized()'''),
('''    c = sum(pts, Vector()) / 5\n''', ''),
('''    _p.z = RAD[_i] * 0.90                       # lying on the ground (slightly flattened belly)''',
 '''    _p.z = RAD[_i] * 0.96                       # lying on the ground (slightly flattened belly)'''),
]
for a, b in rep:
    if a not in t:
        print("MISSING", a[:80])
    t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
