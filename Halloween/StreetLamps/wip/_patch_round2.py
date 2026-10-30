p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\StreetLamps\lamp.py"
s = open(p, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, old[:80]
    s = s.replace(old, new) if count == 0 else s.replace(old, new, count)


# smoother straps
rep("""            idx = adaptive_samples(P, Rl, sag=0.005, max_len=0.36)""",
    """            idx = adaptive_samples(P, Rl, sag=0.004, max_len=0.22)""")
# cap 28 sides, top ring 24, saucer 20
rep("""    lathe_part(accs["body"], capz, nth if hi else 20, hi, ax, seed=94, mat=0 if hi else gm["body"])""",
    """    lathe_part(accs["body"], capz, nth if hi else 28, hi, ax, seed=94, mat=0 if hi else gm["body"])""")
rep("""               (192 // hs) if hi else 16, (24 // hs) if hi else 6, hi, seed=90, mat=0 if hi else gm["body"])""",
    """               (192 // hs) if hi else 24, (24 // hs) if hi else 6, hi, seed=90, mat=0 if hi else gm["body"])""")
rep("""    lathe_part(accs["seat"], sau, nth if hi else 16, hi, ax, prio=0.8, seed=92, mat=0 if hi else gm["seat"])""",
    """    lathe_part(accs["seat"], sau, nth if hi else 20, hi, ax, prio=0.8, seed=92, mat=0 if hi else gm["seat"])""")
# pumpkin skin 48 x 18
rep("""    lo = build_mesh("Pumpkin", [sphere_surface(f_lo, 48, 16) + (0, 1.0),""",
    """    lo = build_mesh("Pumpkin", [sphere_surface(f_lo, 48, 18) + (0, 1.0),""")
# candle lo 12 x 8, puddle lo 8
rep("""    th_lo = [2 * math.pi * j / 16 for j in range(16)]
    s_lo = [0.0, 0.2, 0.4, 0.6, 0.7, 0.78, 0.86, 0.9, 0.95]""",
    """    th_lo = [2 * math.pi * j / 12 for j in range(12)]
    s_lo = [0.0, 0.3, 0.6, 0.7, 0.78, 0.86, 0.9, 0.95]""")
rep("""    for tag, nth, hi_flag in (("lo", 12, False), ("hi", 128 // hs, True)):""",
    """    for tag, nth, hi_flag in (("lo", 8, False), ("hi", 128 // hs, True)):""")
# web: coarser spoke / frame segments, ring 4 single segment
rep("""        n = max(4, int(L / 0.45))
        S.tube([lift(hub + (p - hub) * k / n) for k in range(n + 1)], R_SP, 3)""",
    """        n = max(4, int(L / 0.6))
        S.tube([lift(hub + (p - hub) * k / n) for k in range(n + 1)], R_SP, 3)""")
rep("""            nseg = 1 if kr < 3 else 2""", """            nseg = 1 if kr < 4 else 2""")
rep("""        n = max(2, int(np.linalg.norm(pb - pa) / 0.35))
        S.tube([lift(pa + (pb - pa) * k / n) for k in range(n + 1)], R_FR, 4)""",
    """        n = max(2, int(np.linalg.norm(pb - pa) / 0.5))
        S.tube([lift(pa + (pb - pa) * k / n) for k in range(n + 1)], R_FR, 4)""")
# column: two fewer base rings
rep("(0.762, 0.666), (0.800, 0.640), (0.950, 0.668)", "(0.775, 0.660), (0.950, 0.668)")
rep("(2.262, 0.430),\n    (2.305, 0.472)", "(2.262, 0.430),\n    (2.315, 0.478)")
# toes 4-sided lo
rep("""            njt = (24 // hs) if hi else 5""", """            njt = (24 // hs) if hi else 4""")
# bat bake rays
rep("""                                                                  (0.03, 0.06), (0.05, 0.10)))]),
    "Cage\"""" if False else """                                                                  (0.03, 0.06), (0.05, 0.10)))]),""",
    """                                                                  (0.03, 0.06), (0.07, 0.14)))]),""")
# ground spot energy
rep("""LIGHT_E = dict(inside=40.0, spot=700.0)""", """LIGHT_E = dict(inside=40.0, spot=2500.0)""")
# calibration: keep the best iteration
rep("""        rg = _tolin(NIGHT_TARGET["green"]) / np.maximum(_tolin(meas["green"]), 1e-4)""",
    """        err = float(np.abs(np.array(meas["green"]) - NIGHT_TARGET["green"]).sum() +
                    np.abs(np.array(meas["cream"]) - NIGHT_TARGET["cream"]).sum())
        hist[-1]["err"] = round(err, 2)
        rg = _tolin(NIGHT_TARGET["green"]) / np.maximum(_tolin(meas["green"]), 1e-4)""")
rep("""    L, S, mcol = setup(E)
    final = dict(E=[float(x) for x in E],""", """    best = min(hist, key=lambda h: h["err"])
    E = np.array(best["E"])
    L, S, mcol = setup(E)
    final = dict(E=[float(x) for x in E], best=best,""")
# bat feet: one shared path for lo and hi
rep('''def build_bat_hi(cv):''', '''def bat_foot_path(O, ra, sy, n=8):
    y0 = 0.055 * sy
    pts = [O + np.array([0.0, y0, 0.11])]
    for ang in np.radians([95, 80, 62, 42, 22]):
        pts.append(O + np.array([0.0, y0, -ra]) + (ra + 0.022) * np.array([math.cos(ang), 0, math.sin(ang)]))
    return catmull([tuple(p) for p in pts], n)


def build_bat_hi(cv):''')
rep('''    for sy in (-1, 1):
        y0 = 0.055 * sy
        pts = [O + np.array([0.0, y0, 0.11])]
        for ang in np.radians([95, 80, 62, 42, 22]):
            pts.append(O + np.array([0.0, y0, -ra]) + (ra + 0.022) * np.array([math.cos(ang), 0, math.sin(ang)]))
        Pfoot = catmull([tuple(p) for p in pts], 8)
        T, N, B = frames_transport(Pfoot)''', '''    for sy in (-1, 1):
        Pfoot = bat_foot_path(O, ra, sy)
        T, N, B = frames_transport(Pfoot)''')
rep('''    for sy in (-1, 1):
        y0 = 0.055 * sy
        pts = [O + np.array([0.0, y0, 0.11])]
        for ang in np.radians([90, 55, 22]):
            pts.append(O + np.array([0.0, y0, -ra]) + (ra + 0.022) * np.array([math.cos(ang), 0, math.sin(ang)]))
        Pfoot = np.array(pts)
        T, N, B = frames_transport(Pfoot)''', '''    for sy in (-1, 1):
        Pd = bat_foot_path(O, ra, sy)
        Pfoot = Pd[np.linspace(0, len(Pd) - 1, 4).astype(int)]
        T, N, B = frames_transport(Pfoot)''')
open(p, "w", encoding="utf-8").write(s)
print("round2 ok")
