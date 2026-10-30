import sys, io
P = "pets/CinderOverlord.py"
src = io.open(P, encoding="utf-8").read()
a = src.index("    # ================= head (throat pivot)")
b = src.index("    JR = Euler((math.radians(6), 0, 0)")
new_head = '''    # ================= head (throat pivot): lofted oval wedge skull (review 1 MUST 5: no brick), heavy jaw,
    # obsidian brows with forward points, rose slit eyes, fangs
    SK0, SK1 = Vector((0, -0.45, 1.696)), Vector((0, -1.10, 1.618))
    sd = (SK1 - SK0).normalized()
    sside, sup = frame_of(sd)
    skl = (SK1 - SK0).length
    rings = []
    for f, rw, rh, dz in ((0.0, 0.110, 0.090, 0.0), (0.06, 0.172, 0.138, 0.0), (0.18, 0.200, 0.155, 0.0),
                          (0.40, 0.188, 0.146, 0.0), (0.62, 0.160, 0.124, -0.004), (0.80, 0.122, 0.100, -0.008),
                          (0.93, 0.078, 0.070, -0.010), (1.0, 0.036, 0.040, -0.012)):
        rings.append(oval(SK0 + sd * skl * f + Vector((0, 0, dz)), sside, sup, rw, rh, seg=20, n=2.6))
    skull = B.tube(rings, PLUM_OBS, "Head")
    r0, _ = surf_hit(B, [skull], (0, -0.60, 2.4), (0, 0, -1))
    r1, _ = surf_hit(B, [skull], (0, -0.99, 2.4), (0, 0, -1))
    B.seg(r0, r1, 0.010, 0.022, OBS_D, "Head", top=(0.6, 1.0), rnd=0.3)            # nasal ridge (thin, NICE 2)
    B.seg((0, -0.54, 1.560), (0, -0.98, 1.548), 0.13, 0.03, PALE_S, "Head", top=(0.50, 1.0), rnd=0.3, nostud=True)
    for s in (1, -1):                                                                   # jaw muscles / cheek plates
        B.add((s * 0.17, -0.60, 1.64), (0.065, 0.12, 0.095), PLUM_OBS, "Head", rot=(0, 0, s * 10), rnd=0.42)
        B.add((s * 0.205, -0.56, 1.66), (0.03, 0.09, 0.07), OBS_D, "Head", rot=(0, 0, s * 12), rnd=0.4)
        npt, nn = surf_hit(B, [skull], (s * 0.042, -1.00, 2.4), (0, 0, -1))
        B.add(npt, (0.014, 0.006, 0.020), BLACK, "Head", R=face_R(nn, up=(0, 1, 0)), studs=[], role="detail",
              bevel=0.003)                                                              # nostril pits (on top)
        for z, dz, L, w in ((1.60, -0.35, 0.15, 0.040), (1.67, -0.05, 0.18, 0.044), (1.74, 0.25, 0.13, 0.036)):
            B.spike((s * 0.20, -0.53, z), (s * 0.55, 0.85, dz), L, w, OBS_D, "Head", top=(0.12, 0.35))  # cheek spikes
'''
src = src[:a] + new_head + src[b:]
src = src.replace('''0.150, 0.052, PLUM_OBS, "Jaw", top=(0.58, 0.8), ext=0.04,''', '''0.150, 0.052, PLUM_OBS, "Jaw", top=(0.48, 0.8), ext=0.04,''')
old_eye = '''        B.add(ep, (0.088, 0.010, 0.032), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)       # socket
        B.add(ep + en * 0.008 + R @ Vector((0, 0, -0.004)), (0.074, 0.007, 0.0165), ROSE, "Head", bevel=0.004,'''
new_eye = '''        B.add(ep, (0.098, 0.010, 0.032), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)       # socket
        B.add(ep + en * 0.008 + R @ Vector((0, 0, -0.004)), (0.085, 0.007, 0.0165), ROSE, "Head", bevel=0.004,'''
assert old_eye in src
src = src.replace(old_eye, new_eye)
old_brow = '''              rnd=0.2, studs=[], nostud=True)                                                   # heavy brow
'''
new_brow = '''              rnd=0.2, studs=[], nostud=True)                                                   # heavy brow
        bf = ep + en * 0.020 + Vector((0, 0, 0.056)) + Rb @ Vector((-s * 0.090, 0, 0))
        B.spike(bf, Vector((-s * 0.30, -1.0, -0.28)), 0.090, 0.028, OBS_D, "Head", top=(0.12, 0.35),
                nostud=True)                                                            # brow forward point (NICE 3)
'''
assert old_brow in src
src = src.replace(old_brow, new_brow)
old_mount = '''    B.add((0, -0.585, 1.835), (0.30, 0.050, 0.034), OBS_D, "Head", top=(0.92, 0.80), rnd=0.40)       # crown mount
    for s in (1, -1):
        B.add((s * 0.27, -0.565, 1.825), (0.06, 0.055, 0.040), OBS_D, "Head", rot=(0, s * 14, 0), rnd=0.40)'''
new_mount = '''    for s in (1, -1):                                       # crown mount: ends taper to 0.04 high (NICE 2)
        B.seg((0, -0.585, 1.835), (s * 0.30, -0.585, 1.835), 0.034, 0.050, OBS_D, "Head", side=(0, 0, 1),
              ext=0.02, top=(0.59, 0.85), rnd=0.40)
        B.add((s * 0.27, -0.565, 1.828), (0.05, 0.050, 0.030), OBS_D, "Head", rot=(0, s * 14, 0), rnd=0.40)'''
assert old_mount in src
src = src.replace(old_mount, new_mount)
io.open(P, "w", encoding="utf-8").write(src)
print("ok")
