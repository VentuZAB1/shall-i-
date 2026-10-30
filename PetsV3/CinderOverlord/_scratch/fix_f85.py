# Cinder Overlord final-8.5 fixes (_review/CinderOverlord_final85.md): M1-M5, C1, T1-T4
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b, cnt=1):
    global s, n_ok
    c = s.count(a)
    assert c == cnt, (c, a[:90])
    s = s.replace(a, b)
    n_ok += 1


# ---- M1 + T2: radii (body +12 %, tail +25 %), neck +5 %, chest base sits on the thicker body
rep("RAD = [0.265, 0.275, 0.250, 0.225, 0.180, 0.134, 0.108, 0.082, 0.060, 0.042]   # r1 MUST 6 +15 %, r2 MUST 4 +10 %",
    "RAD = [0.297, 0.308, 0.280, 0.252, 0.200, 0.168, 0.135, 0.103, 0.072, 0.042]   # f85 M1 body +12 %, T2 tail +25 %\n"
    "# (r1 MUST 6 +15 %, r2 MUST 4 +10 %; r6 was 0.265, 0.275, 0.250, 0.225, 0.180, 0.134, 0.108, 0.082, 0.060, 0.042)")
rep("FRONT = [Vector(p) for p in ((0, -0.24, 0.254), (0, -0.48, 0.37),",
    "FRONT = [Vector(p) for p in ((0, -0.24, 0.285), (0, -0.48, 0.37),")
rep("FRAD = [0.268, 0.262, 0.245, 0.220, 0.198, 0.180]    # rearing neck thickened with the body (+~10 %)",
    "FRAD = [0.282, 0.275, 0.257, 0.231, 0.208, 0.189]    # f85 M1 +5 % (r6 0.268, 0.262, 0.245, 0.220, 0.198, 0.180)")

# ---- M1: rings - every second ring dropped on Body2-4 / Tail1-4, the rest narrowed
rep("""        ring_band(a, b, RAD[i], RAD[i + 1], bone, *((0.55, 0.84) if i < 5 else (0.62, 0.79)))   # r6: rings trimmed (body share margin)""",
    """        if i not in (3, 5, 7):          # f85 M1: Body3 / Tail1 / Tail3 rings dropped (no caterpillar read)
            ring_band(a, b, RAD[i], RAD[i + 1], bone, *((0.62, 0.80) if i < 5 else (0.66, 0.76)))   # f85: narrowed""")

# ---- T1: the pale scutes wrap 8 deg further up each flank on Body1-4
rep("""        a0, a1 = (188, 352) if i < 5 else ((200, 340) if i == 5 else (212, 328))""",
    """        a0, a1 = (180, 360) if 1 <= i < 5 else (188, 352) if i == 0 else ((200, 340) if i == 5 else (212, 328))  # f85 T1""")
# the vents move up 4 deg so the wider scutes do not cover their lower ends
rep("""            ang = math.radians(24 if s > 0 else 156)""",
    """            ang = math.radians(28 if s > 0 else 152)                       # f85 (was 24 / 156): clear of the T1 scutes""")

# ---- M2: smaller jaw-muscle bulges + a flat tapered obsidian cheek plate
rep("""        ellip(B, (s * 0.158, -0.62, 1.635), 0.058, 0.115, 0.088, PLUM_OBS, "Head")""",
    """        ellip(B, (s * 0.168, -0.62, 1.628), 0.035, 0.069, 0.053, PLUM_OBS, "Head")      # f85 M2: 60 % bulge
        c0, n0 = surf_hit(B, [skull], (s * 0.6, -0.565, 1.628), (-s, 0, 0))
        c1, n1 = surf_hit(B, [skull], (s * 0.6, -0.800, 1.612), (-s, 0, 0))
        B.seg(c0 + n0 * 0.006, c1 + n1 * 0.006, 0.050, 0.011, OBS_D, "Head", side=(0, 0, 1), top=(0.55, 1.0),
              rnd=0.25, studs=[], nostud=True, role="limb")                             # f85 M2: flat cheek plate""")

# ---- M3: eyes +30 % (socket, slit; the pupil follows the slit height)
rep("""        B.add(ep, (0.098, 0.010, 0.032), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)       # socket""",
    """        B.add(ep, (0.125, 0.010, 0.036), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)       # socket (f85 M3)""")
rep("""        B.add(ep + en * 0.018 + R @ Vector((0, 0, -0.004)), (0.085, 0.007, 0.0165), ROSE, "Head", bevel=0.004,""",
    """        B.add(ep + en * 0.018 + R @ Vector((0, 0, -0.004)), (0.110, 0.010, 0.020), ROSE, "Head", bevel=0.004,""")
rep("""        B.add(ep + en * 0.023 + R @ Vector((-s * 0.006, 0, -0.004)), (0.0055, 0.005, 0.0165), BLACK, "Head",""",
    """        B.add(ep + en * 0.026 + R @ Vector((-s * 0.008, 0, -0.004)), (0.0065, 0.005, 0.020), BLACK, "Head",""")

# ---- M4: crown mount ends shortened + dropped behind the blades, side blocks removed
rep("""        B.seg((0, -0.585, 1.835), (s * 0.30, -0.585, 1.835), 0.034, 0.050, OBS_D, "Head", side=(0, 0, 1),
              ext=0.02, top=(0.59, 0.85), rnd=0.40)
        B.add((s * 0.27, -0.565, 1.828), (0.05, 0.050, 0.030), OBS_D, "Head", rot=(0, s * 14, 0), rnd=0.40)""",
    """        B.seg((0, -0.585, 1.835), (s * 0.22, -0.585, 1.815), 0.034, 0.050, OBS_D, "Head", side=(0, 0, 1),
              ext=0.02, top=(0.59, 0.85), rnd=0.40)                      # f85 M4: ends 0.30 -> 0.22, dropped 0.02
        # (f85 M4: the two side blocks at s * 0.27 are removed - the blades alone carry the crown)""")

# ---- M5: a gold tip cap on the centre blade (front + back, the blue V stays in front of it)
rep("""    if gem:
        B.spike(pts[2] - up_d * 0.03, up_d + nrm * 0.1, 0.075, 0.026, LAVA, bone, nostud=True)    # r2 MUST 5""",
    """    if gem:
        B.spike(pts[2] - up_d * 0.03, up_d + nrm * 0.1, 0.075, 0.026, LAVA, bone, nostud=True)    # r2 MUST 5
        cf = 0.68                                                    # f85 M5: gold tip cap (top 32 % of the blade)
        hw = w * 0.95 * (1.0 - (cf - 0.55) / 0.45)
        B.poly([base - side * hw + up_d * h * cf, base + up_d * (h + 0.004), base + side * hw + up_d * h * cf],
               t + 0.010, GOLD, bone)""")

# ---- C1: the outer blades rise 45 (centre 40), the reseats stretched (centre f84-100, outers to f108)
rep("""            back_f = 96 - 2 * i                                          # reseat in reverse order""",
    """            back_f = 100 - 2 * i                                         # reseat in reverse order (f85 C1: was 96)""")
rep("""                keys = [(0, 0), (up_f, 0), (up_f + 10, 35), (44, 35), (52, 40), (84, 40), (95, 6), (104, 0), (110, 0)]""",
    """                keys = [(0, 0), (up_f, 0), (up_f + 10, 35), (44, 35), (52, 40), (84, 40), (100, 6), (106, 0), (110, 0)]""")
rep("""                keys = [(0, 0), (up_f, 0), (up_f + 10, 35), (44, 35), (54, 10), (84, 10), (back_f, 2), (104, 0), (110, 0)]""",
    """                keys = [(0, 0), (up_f, 0), (up_f + 10, 45), (44, 45), (54, 10), (84, 10), (back_f, 2), (108, 0), (110, 0)]""")
rep("""            vals.append((lift, fan, 0.05 * lift / 40.0 if i == 2 else 0.025 * lift / 35.0))""",
    """            vals.append((lift, fan, 0.05 * lift / 40.0 if i == 2 else 0.025 * min(lift, 35.0) / 35.0))""")

# ---- T3: a deeper idle breath (each neck bone ~3 deg)
rep("""        neck(k, f, pitch=-6 * br, yaw=sway, head_pitch=4 * br, head_yaw=-0.6 * sway)""",
    """        neck(k, f, pitch=-9 * br, yaw=sway, head_pitch=6 * br, head_yaw=-0.6 * sway)    # f85 T3 (was -6 / 4)""")

io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
