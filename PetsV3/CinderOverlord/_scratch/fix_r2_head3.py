import io
P = "pets/CinderOverlord.py"
s = io.open(P, encoding="utf-8").read()
a = s.index("    # ================= head (throat pivot)")
b = s.index("    for s in (1, -1):\n        B.spike(jp((s * 0.075, -0.37, 0.012))")
new = '''    # ================= head (throat pivot): lofted wedge skull with a squared muzzle (review 1 MUST 5: no brick),
    # obsidian skull cap brow-to-crown, lofted jaw, jaw-muscle bulges, brows with forward points, rose slit eyes, fangs
    SK0, SK1 = Vector((0, -0.45, 1.696)), Vector((0, -1.10, 1.618))
    SKS = ((0.0, 0.110, 0.090, 0.0), (0.06, 0.172, 0.138, 0.0), (0.18, 0.200, 0.155, 0.0), (0.40, 0.186, 0.142, -0.004),
           (0.62, 0.150, 0.112, -0.014), (0.82, 0.118, 0.084, -0.026), (0.96, 0.098, 0.066, -0.034),
           (1.0, 0.080, 0.052, -0.036))
    skull, skf = loft(B, SK0, SK1, SKS, PLUM_OBS, "Head", n=2.8)
    cap = []                                   # obsidian skull cap (r2: darker, fiercer face read; brow to crown)
    for f in (0.03, 0.08, 0.18, 0.30, 0.42, 0.54, 0.66, 0.78):
        c, side_v, up_v, rw, rh = skf(f)
        aa, ab = math.radians(55), math.radians(125)
        cap.append((oval(c, side_v, up_v, rw, rh, aa, ab, seg=8, n=2.8, off=0.008),
                    oval(c, side_v, up_v, rw, rh, aa, ab, seg=8, n=2.8, off=-0.014)))
    B.tube(cap, OBS_D, "Head", closed=False, nostud=False)
    r0, _ = surf_hit(B, [skull], (0, -0.95, 2.4), (0, 0, -1))
    r1, _ = surf_hit(B, [skull], (0, -1.07, 2.4), (0, 0, -1))
    B.seg(r0, r1, 0.010, 0.020, OBS_D, "Head", top=(0.6, 1.0), rnd=0.3, ext=0.05)    # nasal ridge tip (thin, NICE 2)
    B.seg((0, -0.54, 1.560), (0, -0.98, 1.548), 0.12, 0.03, PALE_S, "Head", top=(0.50, 1.0), rnd=0.3, nostud=True)
    for s in (1, -1):                                                                   # jaw-muscle bulges
        ellip(B, (s * 0.158, -0.62, 1.635), 0.058, 0.115, 0.088, PLUM_OBS, "Head")
        npt, nn = surf_hit(B, [skull], (s * 0.042, -1.035, 2.4), (0, 0, -1))
        B.add(npt, (0.010, 0.005, 0.016), BLACK, "Head", R=face_R(nn, up=(s * 0.4, 1, 0)), studs=[], role="detail",
              bevel=0.003)                                                              # nostril pits (on top)
        for z, dz, L, w in ((1.60, -0.35, 0.15, 0.040), (1.67, -0.05, 0.18, 0.044), (1.74, 0.25, 0.13, 0.036)):
            B.spike((s * 0.20, -0.53, z), (s * 0.55, 0.85, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))  # cheek spikes
    JR = Euler((math.radians(6), 0, 0), "XYZ").to_matrix()
    JP = Vector((0, -0.55, 1.555))

    def jp(p):
        return JP + JR @ Vector(p)
    loft(B, jp((0, 0.03, -0.01)), jp((0, -0.48, -0.035)), ((0.0, 0.118, 0.044, 0.0), (0.12, 0.148, 0.054, 0.0),
                                                            (0.55, 0.126, 0.052, 0.0), (0.85, 0.098, 0.046, 0.0),
                                                            (1.0, 0.074, 0.034, 0.0)), PLUM_OBS, "Jaw", n=2.8)
    B.seg(jp((0, -0.02, -0.052)), jp((0, -0.42, -0.062)), 0.11, 0.014, PALE_S, "Jaw", top=(0.6, 1.0), rnd=0.3,
          nostud=True)
    B.seg(jp((0, -0.04, 0.030)), jp((0, -0.42, 0.012)), 0.11, 0.010, MOUTH, "Jaw", studs=[], role="detail",
          bevel=0.003, top=(0.6, 1))
'''
s = s[:a] + new + s[b:]
helpers = '''

def loft(B, p0, p1, stations, color, bone, n=2.6, seg=20, up=(0, 0, 1)):
    """closed lofted solid from p0 to p1 through (f, rw, rh, dz) stations; returns (tube, frame(f))"""
    p0, p1 = Vector(p0), Vector(p1)
    d = (p1 - p0).normalized()
    side, upv = frame_of(d, up)
    L = (p1 - p0).length

    def fr(f):
        for (fa, wa, ha, za), (fb, wb, hb, zb) in zip(stations, stations[1:]):
            if fa <= f <= fb:
                u = (f - fa) / max(fb - fa, 1e-6)
                return (p0 + d * L * f + Vector((0, 0, za + (zb - za) * u)), side, upv, wa + (wb - wa) * u,
                        ha + (hb - ha) * u)
        fa, wa, ha, za = stations[-1]
        return p0 + d * L * f + Vector((0, 0, za)), side, upv, wa, ha
    rings = [oval(p0 + d * L * f + Vector((0, 0, dz)), side, upv, rw, rh, seg=seg, n=n) for f, rw, rh, dz in stations]
    return B.tube(rings, color, bone), fr


def ellip(B, c, rx, ry, rz, color, bone):
    """smooth ellipsoid bulge (lofted along y)"""
    c = Vector(c)
    rings = []
    for t in (-0.97, -0.8, -0.45, 0.0, 0.45, 0.8, 0.97):
        k = math.sqrt(max(1 - t * t, 0.05))
        rings.append(oval(c + Vector((0, t * ry, 0)), Vector((1, 0, 0)), Vector((0, 0, 1)), rx * k, rz * k, seg=14))
    return B.tube(rings, color, bone)


def vent('''
s = s.replace("\n\ndef vent(", helpers, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
