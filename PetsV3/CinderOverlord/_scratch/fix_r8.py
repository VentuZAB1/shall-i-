# Cinder Overlord final-8.5 round 8 (_review/CinderOverlord_final85_r8.md + coordinator)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s, n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


# 1: head group 1.38 -> 1.45 (cap per lead), centre blade 0.36 -> 0.40
rep("""HEAD_XF = [((0, -0.50, 1.50), 1.38, [""", """HEAD_XF = [((0, -0.50, 1.50), 1.45, [""")
rep("""(0.0, 0.36, 0.064, 0, 24)""", """(0.0, 0.40, 0.064, 0, 24)""")
# 2: one more mid-body ring dropped (Body4): the back shows two bands (Body1, Tail4)
rep("""        if i not in (2, 3, 5, 6, 7):    # r6 MUST 1: rings only on Spine / Body1 / Body4 / Tail4 (was skip 3, 5, 7; worm read)""",
    """        if i not in (2, 3, 4, 5, 6, 7):  # r8: rings only on Spine / Body1 / Tail4 (r6 skip 2, 3, 5, 6, 7; worm read)""")
# 3: vents 30 % shorter and FLUSH: the slit follows the body curvature (4 short bars on surface points) and sits
#    in the skin (top 0.001 proud), so no straight bar end lifts off the curved flank past the outline
rep("""def vent(B, p, n, d, bone, L=0.095, w=0.026):""",
    """def vent_flush(B, j, t, ang, L, w, bone, side):
    \"\"\"r8: a deep-blue slit that FOLLOWS the curved flank (4 short bars between 5 surface points) and sits flush
    (top 0.001 proud). Slanted: the upper end sweeps toward the tail (as the r4 straight slit did).\"\"\"
    r = (RAD[j] + RAD[j + 1]) / 2
    seglen = (CP[j + 1] - CP[j]).length
    pts = []
    for u in (-0.5, -0.25, 0.0, 0.25, 0.5):
        tt = t + u * L * 0.5 / seglen
        aa = ang + side * u * L * 0.85 / r
        q, nq, _dq = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], tt, aa, off=0.0)
        pts.append((q, nq))
    for k_, ((p0, n0), (p1, n1)) in enumerate(zip(pts, pts[1:])):
        nn = (n0 + n1).normalized()
        B.bar(p0 - nn * 0.005, p1 - nn * 0.005, nn, w, 0.006, ROSE, bone, studs=[], nostud=True, role="detail",
              bevel=0.002)                                                 # slit: top at +0.001
        if k_ in (1, 2):
            B.bar(p0 - nn * 0.002, p1 - nn * 0.002, nn, w * 0.5, 0.004, ROSE, bone, studs=[], nostud=True,
                  role="detail", bevel=0.002)                              # core line: top at +0.002
    return pts[2]


def vent(B, p, n, d, bone, L=0.095, w=0.026):""")
rep("""            for dt in (0.0,):                                              # r4 T-e: ONE slit per segment side (pairs read as legs)
                p, n, dv = surf_pt(CP[j], CP[j + 1], RAD[j], RAD[j + 1], t + dt, ang, off=0.000)   # r3 T1: flush
                vent(B, p, n, dv, bone, L=vl, w=vw)""",
    """            vent_flush(B, j, t, ang, vl * 0.70, vw, bone, 1 if s > 0 else -1)   # r8: 30 % shorter, flush, curved""")
# 4: dorsal spikes +25 % (body + neck)
rep("""        B.spike(p - n * 0.03, n + dv * 0.55, L + 0.03, 0.045 * (L / 0.13) + 0.012, OBS_D, bone, top=(0.12, 0.35))""",
    """        B.spike(p - n * 0.03, n + dv * 0.55, (L + 0.03) * 1.25, (0.045 * (L / 0.13) + 0.012) * 1.25, OBS_D, bone,
                top=(0.12, 0.35))                                                       # r8: +25 % (spined read from behind)""")
rep("""        B.spike(p - n * 0.03, n + Vector((0, 0, -0.45)), L + 0.03, 0.045 * (L / 0.13) + 0.012, OBS_D, fb[i],
                top=(0.12, 0.35))""",
    """        B.spike(p - n * 0.03, n + Vector((0, 0, -0.45)), (L + 0.03) * 1.25, (0.045 * (L / 0.13) + 0.012) * 1.25, OBS_D,
                fb[i], top=(0.12, 0.35))                                                # r8: +25 %""")
# 9+: chin flatter again
rep("""                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.098, 0.044, 0.0),
                                                            (1.0, 0.063, 0.026, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r5 / r7 T-b: tip flatter (r7 -15 %)""",
    """                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.098, 0.040, 0.0),
                                                            (1.0, 0.056, 0.022, 0.0)), PLUM_OBS, "Jaw", n=2.8)  # r5 / r7 / r8 T-b: tip flatter""")
rep("""           + [oval(*jkf(1.012)[:3], jkf(1.0)[3] * 0.72, jkf(1.0)[4] * 0.72, seg=20, n=2.8)],   # r7: cap 1.024 -> 1.012""",
    """           + [oval(*jkf(1.006)[:3], jkf(1.0)[3] * 0.72, jkf(1.0)[4] * 0.72, seg=20, n=2.8)],   # r8: cap 1.012 -> 1.006""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
