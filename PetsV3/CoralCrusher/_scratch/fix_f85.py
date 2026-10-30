# Coral Crusher final-8.5 fixes (_review/CoralCrusher_final85.md): MM1, MM2, CM1, CM2, TO 9+ 1-4
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CoralCrusher.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s, n_ok
    c = s.count(a)
    assert c == 1, (c, a[:90])
    s = s.replace(a, b)
    n_ok += 1


# ---- MM1: rust copper body, deeper seams
rep("BRONZE = (200, 136, 88)      # carapace top, claw bodies (studded); plan (196,150,104); r2 copper lift (N4)",
    "BRONZE = (214, 110, 70)      # f85 MM1: RUST COPPER (was 200,136,88 - read tan / mud). Carapace top, claw bodies (studded)")
rep("BRONZE_D = (146, 96, 62)     # r2 (M2): leg merus, eye stalks + bulbs (a darker bronze, off the carapace value)",
    "BRONZE_D = (150, 74, 50)     # f85 MM1 (was 146,96,62): leg merus, eye stalks + bulbs (a darker copper)")
rep("SHELL_D = (100, 66, 46)      # legs, seams / ridges, claw knuckles, brow plate, fingertips (plan 132,96,66)",
    "SHELL_D = (80, 46, 34)       # f85 MM1 (was 100,66,46): legs, seams / ridges, claw knuckles, brow plate, fingertips")

# ---- MM2: the rim band turns cream (two-tone armour edge) with a thin slate seam above it; the cream lip lower + wider
rep("""    B.tube([ring(y, hw + 0.016, zc + 0.004, 0.026, 0.026, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], SHELL_D,
           "Spine", nostud=True)                                                                   # rim band""",
    """    B.tube([ring(y, hw + 0.016, zc + 0.004, 0.026, 0.026, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE,
           "Spine", nostud=True)                                                   # rim band (f85 MM2: cream, was slate)
    B.tube([ring(y, hw + 0.019, zc + 0.036, 0.006, 0.006, seg=28) for y, hw, zc, ht, hb in CAR[1:-1]], SHELL_D,
           "Spine", nostud=True)                                                   # f85 MM2: thin slate seam above it""")
rep("""    B.tube([ring(y, hw + 0.034, zc - 0.050, 0.026, 0.030, seg=28)
            for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE, "Spine", nostud=True)              # cream lip (r2 M1)""",
    """    B.tube([ring(y, hw + 0.040, zc - 0.100, 0.026, 0.030, seg=28)
            for y, hw, zc, ht, hb in CAR[1:-1]], BELLY_PALE, "Spine", nostud=True)   # cream lip (f85 MM2: lower, wider)""")

# ---- TO 9+ 3: two taller rose coral clusters on the dome centre (the game camera looks down)
rep("""    for x, y, sc, rot in ((0.26, 0.20, 1.0, 20), (-0.20, 0.30, 0.85, -35), (0.06, 0.40, 0.7, 60)):""",
    """    for x, y, sc, rot in ((0.26, 0.20, 1.0, 20), (-0.20, 0.30, 0.85, -35), (0.06, 0.40, 0.7, 60),
                          (0.075, 0.075, 1.30, 10), (-0.085, 0.02, 1.20, -30)):           # f85 9+ 3: dome centre""")

# ---- TO 9+ 2: wider pincer gape + bigger molars on the inner edges
rep("""            r0 = F + o * sgn * 0.085 * c - a * 0.06""",
    """            r0 = F + o * sgn * 0.097 * c - a * 0.06                # f85 9+ 2: roots 0.085 -> 0.097 (gape ~0.06 H)""")
rep("""            for t in (0.35, 0.75):                                                                  # crusher molars
                q = r0.lerp(m1, t) - o * sgn * 0.050 * c
                B.add(q, (0.028 * c, 0.022 * c, 0.018 * c), SHELL_D, bone, R=bk.frame_from(r0, m1, out),""",
    """            for t in (0.35, 0.75):                                                                  # crusher molars
                q = r0.lerp(m1, t) - o * sgn * 0.052 * c
                B.add(q, (0.030 * c, 0.026 * c, 0.022 * c), SHELL_D, bone, R=bk.frame_from(r0, m1, out),  # f85: bigger""")

# ---- TO 9+ 1: legs thicker (merus +20 %, coxa, top plate, spike follow)
rep("""            B.add(H, (0.072, 0.072, 0.062), SHELL_D, leg, rnd=0.42)                                  # coxa
            B.seg(H, K, 0.070, 0.092, BRONZE_D, leg, side=(0, 0, 1), ext=0.05, ext1=0.03, top=(0.90, 0.86),
                  rnd=0.40)                                                                         # merus (r2 M2)
            dm = (K - H).normalized()
            B.seg(H + dm * 0.03 + Vector((0, 0, 0.056)), K - dm * 0.03 + Vector((0, 0, 0.058)), 0.020, 0.072,
                  BRONZE, leg, side=(0, 0, 1), top=(1.0, 0.85), rnd=0.35)                           # merus top plate
            rose_spike(B, H.lerp(K, 0.62) + Vector((0, 0, 0.080)), dm * 0.35 + Vector((0, 0, 1)), 0.085, 0.029, leg)""",
    """            B.add(H, (0.080, 0.080, 0.068), SHELL_D, leg, rnd=0.42)                                  # coxa (f85)
            B.seg(H, K, 0.084, 0.110, BRONZE_D, leg, side=(0, 0, 1), ext=0.05, ext1=0.03, top=(0.90, 0.86),
                  rnd=0.40)                                                         # merus (f85 9+ 1: +20 %)
            dm = (K - H).normalized()
            B.seg(H + dm * 0.03 + Vector((0, 0, 0.068)), K - dm * 0.03 + Vector((0, 0, 0.070)), 0.022, 0.086,
                  BRONZE, leg, side=(0, 0, 1), top=(1.0, 0.85), rnd=0.35)                           # merus top plate
            rose_spike(B, H.lerp(K, 0.62) + Vector((0, 0, 0.094)), dm * 0.35 + Vector((0, 0, 1)), 0.085, 0.029, leg)""")

# ---- CM1: the idle breathes (crusher 20 +/- 3, 35 f arc: troughs f45 / f80, peak f62; body bob 0.008)
rep("""    for f in range(0, n + 1, 2):
        body(k, f, up=0.004 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n)))
        claw(k, f, "R", lift=curve(guard, f), fore=curve(gfore, f), pinch=curve(gpin, f))""",
    """    breath = [(0, 0), (28, 0), (45, -3), (62, 3), (80, -3), (98, 0), (120, 0)]   # f85 CM1: the guard breathes
    for f in range(0, n + 1, 2):
        body(k, f, up=0.008 * (0.5 - 0.5 * math.cos(4 * math.pi * f / n)))       # f85 CM1: bob 0.004 -> 0.008
        claw(k, f, "R", lift=curve(guard, f) + curve(breath, f), fore=curve(gfore, f), pinch=curve(gpin, f))""")

# ---- TO 9+ 4: a 4 deg crusher sway in the walk (twice per cycle, between the tripod contacts)
rep("""        for sd in ("L", "R"):
            claw(k, f, sd, lift=-10 + 3 * pk.wave(f, n, 0.0 if sd == "L" else 0.5), fore=-4,
                 wrist=2 * pk.wave(f, n, 0.2))""",
    """        for sd in ("L", "R"):
            claw(k, f, sd, lift=-10 + 3 * pk.wave(f, n, 0.0 if sd == "L" else 0.5), fore=-4,
                 wrist=2 * pk.wave(f, n, 0.2),
                 spread=4 * pk.wave(f, n, 0.125, 2) if sd == "R" else 0.0)       # f85 9+ 4: crusher sway""")

# ---- CM2: the act's secondary motion - eyestalks track the crusher (2 f behind the wave), the shell rolls with it
rep("""    tap_l = [(0, 0), (18, -6), (86, -6), (88, 6), (90, -6), (94, 6), (96, -6), (102, -6), (110, 0), (120, 0)]
    for f in range(0, n + 1):
        u = curve(up, f)
        body(k, f, up=0.10 * u, pitch=-5 * u, roll=-2 * u)                          # review 3 N2: stand taller""",
    """    tap_l = [(0, 0), (18, -6), (86, -6), (88, 6), (90, -6), (94, 6), (96, -6), (102, -6), (110, 0), (120, 0)]
    # f85 CM2: the wave's top/trough rhythm shifted 2 f later (tops held f28-36 / f51-59 / f74-82, troughs f41 / f64)
    track = [(0, 0), (20, 0.6)]
    for i, t0 in enumerate(TOPS):
        track += [(t0 + 2, 1.0), (t0 + HOLD + 2, 1.0)]
        if i < len(TROUGHS):
            track.append((TROUGHS[i] + 2, 0.0))
    track += [(88, 0.6), (100, 0.3), (110, 0), (120, 0)]
    for f in range(0, n + 1):
        u = curve(up, f)
        tr = curve(track, f)
        body(k, f, up=0.10 * u, pitch=-5 * u, roll=-2 * u - 2 * (2 * tr - 1) * u)   # f85 CM2: +/-2 deg with each beat""")
rep("""        eyes(k, f, up=6 * u, r=-8 * u)
        k.key("Mouth", f, rot=(0, 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_semaphore"]""",
    """        eyes(k, f, up=6 * u + 4 * tr * u, l=-12 * tr * u, r=-4 * u - 12 * tr * u)    # f85 CM2: track the crusher
        k.key("Mouth", f, rot=(0, 0, 0))
    plant6(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_semaphore"]""")

# docstrings
rep('''    """CLAW GUARD (plan; ref #7): the crusher lifts 20 deg to guard and holds, the eyestalks swivel one at a time with
    freezes between, the cutter taps the shell once (f70). Starts and ends in the base pose (portrait = f0)."""''',
    '''    """CLAW GUARD (plan; ref #7): the crusher lifts 20 deg to guard and BREATHES there (f85 CM1: +/-3 deg over one 35 f
    arc, troughs f45 / f80, peak f62; the body bobs 0.008), the eyestalks swivel one at a time with freezes between,
    the cutter taps the shell once (f70). Starts and ends in the base pose (portrait = f0)."""''')
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
