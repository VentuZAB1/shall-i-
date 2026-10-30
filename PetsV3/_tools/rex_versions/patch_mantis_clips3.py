# Mantis clip pass 3: the deimatic FAN (pose_try vJ: tegmina 66 / splay 10 / roll 6, hindwings 58 / splay 72 / roll 52
# - a real V with both eye-spots to the game camera; the kit applies roll BEFORE pitch, so the V needs a mirrored YAW
# splay), wing-root hinge capsule, higher + wider X-cross, gentler abdomen sway.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThornbladeMantis.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''def wings(k, f, el=0.0, el_roll=0.0, wi=0.0, wi_roll=0.0, yaw=0.0):
    """el / wi + = tegmina / hindwings RAISED (kit + lifts a +Y bone); *_roll + = rolled outward (mirrored);
    yaw = the folded wings ride the abdomen sway (see abdomen())"""
    for s, sd in ((1, "L"), (-1, "R")):
        k.key("Elytra_" + sd, f, rot=(el, yaw, s * el_roll))
        k.key("Wing_" + sd, f, rot=(wi, yaw, s * wi_roll))''',
'''def wings(k, f, el=0.0, el_roll=0.0, wi=0.0, wi_roll=0.0, yaw=0.0, el_splay=0.0, wi_splay=0.0):
    """el / wi + = tegmina / hindwings RAISED (kit + lifts a +Y bone); *_roll + = twisted about the wing's own long
    axis (the kit applies roll BEFORE pitch, so it only turns the face); *_splay + = swung OUT into a V (mirrored yaw,
    applied after the raise); yaw = the folded wings ride the abdomen sway (see abdomen())"""
    for s, sd in ((1, "L"), (-1, "R")):
        k.key("Elytra_" + sd, f, rot=(el, yaw - s * el_splay, s * el_roll))
        k.key("Wing_" + sd, f, rot=(wi, yaw - s * wi_splay, s * wi_roll))'''))
R.append(('''    return (0.70 * yaw[0] + 0.38 * yaw[1] + 0.08 * yaw[2]) / 0.9''',
          '''    return 1.1 * (0.70 * yaw[0] + 0.38 * yaw[1] + 0.08 * yaw[2]) / 0.9'''))
R.append(('''        ey = abdomen(k, f, yaw=(-1.0 * pk.wave(f, n, -0.05, 3), -1.5 * pk.wave(f, n, -0.08, 3),
                                -2.0 * pk.wave(f, n, -0.11, 3)))''',
          '''        ey = abdomen(k, f, yaw=(-0.6 * pk.wave(f, n, -0.05, 3), -0.9 * pk.wave(f, n, -0.08, 3),
                                -1.2 * pk.wave(f, n, -0.11, 3)))'''))
R.append(('''        ey = abdomen(k, f, yaw=(-2.0 * pk.wave(f, n, -0.07), -2.5 * pk.wave(f, n, -0.1), -3.0 * pk.wave(f, n, -0.13)))''',
          '''        ey = abdomen(k, f, yaw=(-1.2 * pk.wave(f, n, -0.07), -1.5 * pk.wave(f, n, -0.1), -1.8 * pk.wave(f, n, -0.13)))'''))
R.append(('''        el = ease(0, 65, 14, 24, f) if f <= 60 else ease(65, 0, 64, 74, f)
        er = ease(0, 40, 14, 24, f) if f <= 60 else ease(40, 0, 64, 74, f)
        # fold: the hindwings first drop + roll in UNDER the tegmina (f60-64), then both close together (f64-74)
        wi = ease(0, 80, 16, 26, f) if f <= 60 else (ease(80, 63.5, 60, 64, f) if f <= 64 else ease(63.5, 0, 64, 74, f))
        shiver = (3.0 if (f // 3) % 2 == 0 else -3.0) if 26 <= f <= 58 else 0.0
        wr = (ease(0, 15, 16, 26, f) if f <= 60 else (ease(15, 40, 60, 64, f) if f <= 64 else ease(40, 0, 64, 74, f))) \\
            + shiver
        wings(k, f, el=el, el_roll=er, wi=wi, wi_roll=wr)''',
'''        te = ease(0, 1, 14, 24, f) if f <= 60 else ease(1, 0, 62, 74, f)          # tegmina: up first, close last
        tw = ease(0, 1, 16, 26, f) if f <= 60 else ease(1, 0, 60, 70, f)          # hindwings: 2 f lag, fold first
        shiver = (3.0 if (f // 3) % 2 == 0 else -3.0) if 26 <= f <= 58 else 0.0
        wings(k, f, el=66 * te, el_splay=10 * te, el_roll=6 * te, wi=58 * tw, wi_splay=72 * tw, wi_roll=52 * tw + shiver)'''))
R.append(('''        (34, -14, -20, -18, -40, 60, 0), (35, -16, -20, -18, -40, 5, 60), (36, -16, -22, -18, -40, -5, -5),  # X-cross
        (50, -15, -21, -18, -38, -5, -5),                                                 # executioner hold (clutch)''',
'''        (34, -6, -16, -14, -40, 60, 0), (35, -8, -16, -14, -40, 5, 60), (36, -8, -18, -14, -40, -5, -5),     # X-cross
        (50, -7, -17, -14, -38, -5, -5),                                                  # executioner hold (clutch)'''))
R.append(('''HEAD_XF = []''', '''def joints():
    # wing articulation strip: tegmina and hindwings hinge 0.02 apart along the thorax side, so the fan's roots cross
    # there (pose_try: every crossing of the display fan lies within 0.07 of this axis)
    return [(tuple(X(WROOT, s)), tuple(X(WROOT + Vector((0.02, 0.20, -0.005)), s)), 0.07, "Wing_" + side)
            for s, side in ((1, "L"), (-1, "R"))]


HEAD_XF = []'''))
for a, b in R:
    assert s.count(a) == 1, "MISSING/DUP: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
