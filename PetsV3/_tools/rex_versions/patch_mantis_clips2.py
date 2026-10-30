# Mantis clip pass 2: forward strike reach (not into the ground), roar head-lock, hindwings close WITH the tegmina,
# tegmina follow the abdomen sway, a real groom (head bends to the blade).
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThornbladeMantis.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''def wings(k, f, el=0.0, el_roll=0.0, wi=0.0, wi_roll=0.0):
    """el / wi + = tegmina / hindwings RAISED (kit + lifts a +Y bone); *_roll + = rolled outward (mirrored)"""
    for s, sd in ((1, "L"), (-1, "R")):
        k.key("Elytra_" + sd, f, rot=(el, 0, s * el_roll))
        k.key("Wing_" + sd, f, rot=(wi, 0, s * wi_roll))


def abdomen(k, f, curl=(0.0, 0.0, 0.0), yaw=(0.0, 0.0, 0.0)):
    """curl + = the abdomen curls UP"""
    for b, c, yw in zip(TAIL, curl, yaw):
        k.key(b, f, rot=(c, yw, 0))''',
'''def wings(k, f, el=0.0, el_roll=0.0, wi=0.0, wi_roll=0.0, yaw=0.0):
    """el / wi + = tegmina / hindwings RAISED (kit + lifts a +Y bone); *_roll + = rolled outward (mirrored);
    yaw = the folded wings ride the abdomen sway (see abdomen())"""
    for s, sd in ((1, "L"), (-1, "R")):
        k.key("Elytra_" + sd, f, rot=(el, yaw, s * el_roll))
        k.key("Wing_" + sd, f, rot=(wi, yaw, s * wi_roll))


def abdomen(k, f, curl=(0.0, 0.0, 0.0), yaw=(0.0, 0.0, 0.0)):
    """curl + = the abdomen curls UP. Returns the yaw the folded wings need so their tips (lying on Tail3, 0.9 from
    the hinge) follow the abdomen's lateral sway there."""
    for b, c, yw in zip(TAIL, curl, yaw):
        k.key(b, f, rot=(c, yw, 0))
    return (0.70 * yaw[0] + 0.38 * yaw[1] + 0.08 * yaw[2]) / 0.9'''))
# idle: wings follow; groom = head bends to the blade
R.append(('''        abdomen(k, f, yaw=(-1.0 * pk.wave(f, n, -0.05, 3), -1.5 * pk.wave(f, n, -0.08, 3),
                           -2.0 * pk.wave(f, n, -0.11, 3)))
        wings(k, f)
        tilt = ease(0, 12, 18, 23, f) if f <= 48 else ease(12, 0, 48, 56, f)
        dn = 8.0 * math.sin(math.pi * (f - 66) / 34.0) if 66 <= f <= 100 else 0.0
        head(k, f, up=-dn, roll=-3.0 * w + tilt)''',
'''        ey = abdomen(k, f, yaw=(-1.0 * pk.wave(f, n, -0.05, 3), -1.5 * pk.wave(f, n, -0.08, 3),
                                -2.0 * pk.wave(f, n, -0.11, 3)))
        wings(k, f, yaw=ey)
        tilt = ease(0, 12, 18, 23, f) if f <= 48 else ease(12, 0, 48, 56, f)
        g = ease(0, 1, 62, 72, f) if f <= 92 else ease(1, 0, 92, 102, f)
        head(k, f, up=-10.0 * g, yaw=8.0 * g, roll=-3.0 * w + tilt)'''))
R.append(('''    for f, a in ((0, 0.0), (62, 0.0), (72, 1.0), (92, 1.0), (102, 0.0), (120, 0.0)):
        arm(k, f, "L", up=0.0, out=-12.0 * a, fore=6.0 * a, blade=55.0 * a)
        arm(k, f, "R")''',
'''    for f, a in ((0, 0.0), (62, 0.0), (72, 1.0), (92, 1.0), (102, 0.0), (120, 0.0)):
        groom(k, f, a)
        arm(k, f, "R")'''))
R.append(('''def idle(k):''', '''def groom(k, f, a):
    """the LEFT blade comes in front of the mandibles (no raise: yaw IN, femur reaches a little, tibia part-open)"""
    arm(k, f, "L", up=0.0, out=-8.0 * a, fore=-10.0 * a, blade=30.0 * a)


def idle(k):'''))
# walk: wings follow
R.append(('''        abdomen(k, f, yaw=(-2.0 * pk.wave(f, n, -0.07), -2.5 * pk.wave(f, n, -0.1), -3.0 * pk.wave(f, n, -0.13)))
        wings(k, f)''',
'''        ey = abdomen(k, f, yaw=(-2.0 * pk.wave(f, n, -0.07), -2.5 * pk.wave(f, n, -0.1), -3.0 * pk.wave(f, n, -0.13)))
        wings(k, f, yaw=ey)'''))
# roar: head-lock (net world tilt ~ +18 instead of +40), hindwings align under the tegmina then close with them
R.append(('''            z, p, ch, hu = -0.04 * u, 4.0 * u, -6.0 * u, -6.0 * u
        elif f <= 20:
            z, p, ch, hu = ease(-0.04, 0.035, 10, 20, f), ease(4, -10, 10, 20, f), ease(-6, 12, 10, 20, f), \\
                ease(-6, 18, 10, 20, f)
        elif f <= 60:
            z, p, ch, hu = 0.035, -10.0, 12.0, 18.0
        elif f <= 76:
            z, p, ch, hu = ease(0.035, 0.0, 60, 76, f), ease(-10, 0, 60, 76, f), ease(12, 0, 60, 76, f), \\
                ease(18, 0, 60, 76, f)''',
'''            z, p, ch, hu = -0.04 * u, 4.0 * u, -6.0 * u, -6.0 * u
        elif f <= 20:                                  # head-lock: the body rears 22, the head stays on the threat
            z, p, ch, hu = ease(-0.04, 0.035, 10, 20, f), ease(4, -10, 10, 20, f), ease(-6, 12, 10, 20, f), \\
                ease(-6, -4, 10, 20, f)
        elif f <= 60:
            z, p, ch, hu = 0.035, -10.0, 12.0, -4.0
        elif f <= 76:
            z, p, ch, hu = ease(0.035, 0.0, 60, 76, f), ease(-10, 0, 60, 76, f), ease(12, 0, 60, 76, f), \\
                ease(-4, 0, 60, 76, f)'''))
R.append(('''        wi = ease(0, 80, 16, 26, f) if f <= 60 else ease(80, 0, 60, 70, f)
        shiver = (3.0 if (f // 3) % 2 == 0 else -3.0) if 26 <= f <= 58 else 0.0
        wr = (ease(0, 15, 16, 26, f) if f <= 60 else ease(15, 0, 60, 70, f)) + shiver''',
'''        # fold: the hindwings first drop + roll in UNDER the tegmina (f60-64), then both close together (f64-74)
        wi = ease(0, 80, 16, 26, f) if f <= 60 else (ease(80, 63.5, 60, 64, f) if f <= 64 else ease(63.5, 0, 64, 74, f))
        shiver = (3.0 if (f // 3) % 2 == 0 else -3.0) if 26 <= f <= 58 else 0.0
        wr = (ease(0, 15, 16, 26, f) if f <= 60 else (ease(15, 40, 60, 64, f) if f <= 64 else ease(40, 0, 64, 74, f))) \\
            + shiver'''))
# act: forward strikes at head height
R.append(('''        (25, -45, -45, 0, -50, 85, 85), (27, -45, -45, 0, -50, 10, 10),                 # STRIKE 1: snap open / shut
        (29, -14, -14, 4, -8, 6, 6), (31, -10, -10, 6, -4, 4, 4), (33, -10, -10, 6, -4, 4, 4),     # recoil
        (34, -44, -50, -18, -45, 60, 0), (35, -50, -50, -18, -45, 5, 60), (36, -50, -56, -18, -45, -5, -5),   # X-cross
        (50, -48, -54, -18, -42, -5, -5),                                                 # executioner hold (clutch)''',
'''        (25, -12, -12, 0, -45, 85, 85), (27, -12, -12, 0, -45, 10, 10),                 # STRIKE 1: FORWARD reach
        (29, -6, -6, 4, -10, 6, 6), (31, -4, -4, 6, -6, 4, 4), (33, -4, -4, 6, -6, 4, 4),         # recoil
        (34, -14, -20, -18, -40, 60, 0), (35, -16, -20, -18, -40, 5, 60), (36, -16, -22, -18, -40, -5, -5),  # X-cross
        (50, -15, -21, -18, -38, -5, -5),                                                 # executioner hold (clutch)'''))
R.append(('''    for f, a in ((64, 1.0), (72, 1.0), (78, 0.0), (100, 0.0)):                             # groom (left blade)
        arm(k, f, "L", up=0.0, out=-12.0 * a, fore=6.0 * a, blade=55.0 * a)
        arm(k, f, "R")''',
'''    for f, a in ((64, 1.0), (72, 1.0), (78, 0.0), (100, 0.0)):                             # groom (left blade)
        groom(k, f, a)
        arm(k, f, "R")'''))
for a, b in R:
    assert s.count(a) == 1, "MISSING/DUP: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
