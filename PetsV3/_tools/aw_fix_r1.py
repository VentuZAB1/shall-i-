# one-off patch: Abyss Weaver review 1 FIX 1-3 + the roar shin yaw + merge clips into the spec + brief gold counter
import os
os.chdir(r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3")


def patch(path, reps):
    s = open(path, encoding="utf-8").read()
    for a, b in reps:
        assert s.count(a) == 1, (path, a[:70])
        s = s.replace(a, b)
    open(path, "w", encoding="utf-8").write(s)
    return s


patch("pets/AbyssWeaver.py", [
    ("""    B.add(c, (0.052 * sc, 0.008, 0.025 * sc), BLACK, bone, bevel=0.004, **kw)
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0135 * sc), ORCHID, bone, bevel=0.003, **kw)
    B.add(c + n * 0.011 + R @ Vector((s * 0.022 * sc, 0, 0.002)), (0.014 * sc, 0.004, 0.006 * sc), HOT, bone,
          bevel=0.002, **kw)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0095 * sc), BLACK, bone,
          bevel=0.002, **kw)
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.036 * sc)) + n * 0.024, (0.074 * sc, 0.034, 0.028 * sc), ARMOR_D, bone, R=Rb,
          role="detail", bevel=0.012)""",
     """    B.add(c, (0.052 * sc, 0.008, 0.028 * sc), BLACK, bone, bevel=0.004, **kw)                  # socket
    B.add(c + n * 0.006, (0.044 * sc, 0.006, 0.0165 * sc), ORCHID, bone, bevel=0.003, **kw)     # lens (review 1 FIX 1)
    B.add(c + n * 0.011 + R @ Vector((-s * 0.004, 0, 0)), (0.006 * sc, 0.004, 0.0115 * sc), BLACK, bone,
          bevel=0.002, **kw)                                                                  # slit pupil, 70 %
    Rb = Euler((0, math.radians(-s * 22), math.radians(s * yaw)), "XYZ").to_matrix()
    B.add(c + Vector((0, 0, 0.040 * sc)) + n * 0.010, (0.074 * sc, 0.022, 0.026 * sc), ARMOR_D, bone, R=Rb,
          role="detail", bevel=0.010)                                                         # thin V-brow, no glint"""),
    ("""    \"\"\"ThunderRex fierce_eye recolored: black socket (inner corner down) -> orchid slit -> hot spot on the OUTER half,
    a black vertical pupil (70 % of the lens height) at the inner front, an ARMOR_D V-brow lidding the top 30 %\"\"\"""",
     """    \"\"\"ThunderRex fierce_eye recolored: black socket (inner corner down) -> a tall orchid slit lens with a black
    vertical pupil (70 %) at the inner front, a thin ARMOR_D V-brow lidding ~30 % from the portrait camera. No HOT spot
    (it read as a cute glint once the eye shows; the EyeGlow VFX carries the burn - review 1 FIX 1)\"\"\""""),
    ("""    def shell(u0, u1, a0, a1, color, off=0.022, thick=0.03, seg=10):
        rings = []
        for i in range(4):
            u = u0 + (u1 - u0) * i / 3.0""",
     """    def shell(u0, u1, a0, a1, color, off=0.022, thick=0.03, seg=10, nr=4):
        rings = []
        for i in range(nr):
            u = u0 + (u1 - u0) * i / (nr - 1.0)"""),
    ("""    shell(0.14, 0.64, 200, 340, SILK, off=0.012, thick=0.02, seg=12)             # belly band (wine seams 0.04)""",
     """    shell(0.14, 0.64, 205, 335, SILK, off=0.014, thick=0.02, seg=12, nr=6)       # belly band (6 rings: no poke-through)"""),
    ("""    for col, wf, lift, cap in ((DEEP, 1.0, 0.010, 1.0), (ORCHID, 0.63, 0.016, 1.0), (HOT, 0.12, 0.021, 0.018)):
        for i in range(N):
            t0, t1 = i / N, (i + 1) / N
            ua, ub = U0 + (U1 - U0) * t0, U0 + (U1 - U0) * t1
            w = max(0.010, min(cap, wf * wt((t0 + t1) / 2)))
            B.bar(abd_top(ua, 0, lift), abd_top(ub, 0, lift), abd_nrm((ua + ub) / 2, 0), 2 * w, 0.006, col, "Abd",
                  studs=[], nostud=True, role="detail", bevel=0.003)""",
     """    # review 1 FIX 2: a torn orchid body + a meandering HOT crack with 2 side fractures (never a pupil slit, never a
    # regular zig-zag bolt); the closed gold lip frame stays
    JAG = [0.55, 0.62, 0.72, 0.58, 0.66, 0.80, 0.62, 0.70, 0.82, 0.64, 0.56, 0.70, 0.60, 0.55]   # torn orchid edge
    ZZ = [0.0, 0.20, 0.42, 0.16, -0.28, -0.48, -0.20, 0.18, 0.46, 0.30, -0.06, -0.36, -0.22, 0.06, 0.0]  # crack path
    for i in range(N):
        t0, t1 = i / N, (i + 1) / N
        ua, ub = U0 + (U1 - U0) * t0, U0 + (U1 - U0) * t1
        nm = abd_nrm((ua + ub) / 2, 0)
        B.bar(abd_top(ua, 0, 0.010), abd_top(ub, 0, 0.010), nm, 2 * max(0.010, wt((t0 + t1) / 2)), 0.006, DEEP,
              "Abd", studs=[], nostud=True, role="detail", bevel=0.003)                      # void field
        B.bar(abd_top(ua, 0, 0.016), abd_top(ub, 0, 0.016), nm, 2 * max(0.010, JAG[i] * wt((t0 + t1) / 2)), 0.006,
              ORCHID, "Abd", studs=[], nostud=True, role="detail", bevel=0.003)              # glow body, torn edge
    pts = []
    for i in range(N + 1):                                    # HOT: a meandering crack (S + jitter)
        t = i / N
        u = U0 + (U1 - U0) * t
        hw, _ = abd_interp(u)
        pts.append((abd_top(u, ZZ[i] * 0.45 * wt(t) / hw, 0.021), u))
    for (a, ua), (b, ub) in zip(pts, pts[1:]):
        d = (b - a).normalized()
        B.bar(a - d * 0.010, b + d * 0.010, abd_nrm((ua + ub) / 2, 0), 0.026, 0.004, HOT, "Abd", studs=[],
              nostud=True, role="detail", bevel=0.002)
    for i, side, du in ((5, -1, 0.05), (9, 1, -0.05)):       # 2 short side fractures (an eye never branches)
        a, ua = pts[i]
        ub = ua + du
        hw, _ = abd_interp(ub)
        b = abd_top(ub, (ZZ[i] * 0.45 + side * 0.42) * wt((ub - U0) / (U1 - U0)) / hw, 0.021)
        B.bar(a, b, abd_nrm((ua + ub) / 2, 0), 0.016, 0.004, HOT, "Abd", studs=[], nostud=True, role="detail",
              bevel=0.002)"""),
])
print("model fixes ok")

t = patch("_tools/aw_anim_v1.py.txt", [
    ("""def leg_raise(k, f, i, side, fem=0.0, shin=0.0, foot=0.0):
    \"\"\"FK about the leg-plane axis (brief 5.7, review W4): fem + = the femur leans OUT, shin / foot + = the knee /
    ankle OPEN (the shin swings up). R = the mirrored axis with the opposite angle.\"\"\"
    a = math.radians(AZ[i])
    s = 1 if side == "L" else -1
    t = Vector((-s * math.sin(a), math.cos(a), 0))
    cm.key_axis(k, "Leg%d_%s" % (i, side), f, t, s * fem)
    cm.key_axis(k, "Shin%d_%s" % (i, side), f, t, -s * shin)""",
     """def leg_raise(k, f, i, side, fem=0.0, shin=0.0, foot=0.0, shin_fwd=0.0):
    \"\"\"FK about the leg-plane axis (brief 5.7, review W4): fem + = the femur leans OUT, shin / foot + = the knee /
    ankle OPEN (the shin swings up). R = the mirrored axis with the opposite angle. shin_fwd = a forward yaw on the
    SHIN only (review 1 s6.2: legs 1 read as a raised V, not the banned sideways T; never yaw the femur).\"\"\"
    from mathutils import Quaternion
    a = math.radians(AZ[i])
    s = 1 if side == "L" else -1
    t = Vector((-s * math.sin(a), math.cos(a), 0))
    cm.key_axis(k, "Leg%d_%s" % (i, side), f, t, s * fem)
    cm.key_axis(k, "Shin%d_%s" % (i, side), f, t, -s * shin,
                extra=Quaternion((0, 0, 1), math.radians(-s * shin_fwd)) if shin_fwd else None)"""),
    ("""            leg_raise(k, f, 1, side, fe, sh + tr, fo)
        for f in range(24, 55, 3):                              # the leg-1 shin tremble keys
            leg_raise(k, f, 1, side, 15, 80 + (2 if (f // 3) % 2 else -2), 20)""",
     """            leg_raise(k, f, 1, side, fe, sh + tr, fo, shin_fwd=35.0 * sh / 80.0)
        for f in range(24, 55, 3):                              # the leg-1 shin tremble keys
            leg_raise(k, f, 1, side, 15, 80 + (2 if (f // 3) % 2 else -2), 20, shin_fwd=35.0)"""),
    ("""    k.events["idle"] = {"pulse": round(40 / n, 3), "flex": round(70 / n, 3), "pulse2": round(100 / n, 3)}""",
     """    k.events["idle"] = {"pulse1": round(40 / n, 3), "flex": round(70 / n, 3), "pulse2": round(100 / n, 3)}"""),
])
s = open("pets/AbyssWeaver.py", encoding="utf-8").read()
cut = s.index("# ------------------------------------------------------------------ animation (v0")
open("pets/AbyssWeaver.py", "w", encoding="utf-8").write(s[:cut] + t.lstrip("\n"))
print("clips merged")

patch("_tools/game_icon.py", [
    ("""out = {"gold_px_portrait_64": gold_px(me), "gold_px_game_64": gold_px(gm)}""",
     """def gold_px_brief(im):
    \"\"\"the Weaver brief's counter: hue 0.09-0.17, s > .45, v > .55\"\"\"
    import colorsys
    sm = im.resize((64, 64), Image.LANCZOS)
    n = 0
    for r, g, b, a in (sm.get_flattened_data() if hasattr(sm, "get_flattened_data") else sm.getdata()):
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if a > 128 and 0.09 <= h <= 0.17 and s > 0.45 and v > 0.55:
            n += 1
    return n


out = {"gold_px_portrait_64": gold_px(me), "gold_px_game_64": gold_px(gm),
       "gold_px_brief_counter": [gold_px_brief(me), gold_px_brief(gm)]}"""),
])
print("gold counter ok")
