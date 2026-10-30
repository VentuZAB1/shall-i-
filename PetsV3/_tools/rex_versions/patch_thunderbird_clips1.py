# Thunderbird clip pass 1 fixes (collisions + ground). Plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\Thunderbird.py"
s = open(p, encoding="utf-8").read()
R = []
# hinge regions: knee (trouser top inside the belly skirt) + throat (head pivot under the ruff, crest excluded)
R.append(('''def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
    return out''',
'''def joints():
    out = WING.joints()
    for s, sd in ((1, "L"), (-1, "R")):
        out.append((X(WING.S, s), X(WING.BB, s), 0.12, "Wing_" + sd))
        # knee: the trouser top emerges from the belly skirt (a bird's leg out of its body feathers)
        K, A = Vector(X(KNEE, s)), Vector(X(ANKLE, s))
        d = (A - K).normalized()
        out.append((tuple(K - d * 0.05), tuple(K + d * 0.16), 0.105, "Shin_" + sd))
    # throat pivot under the ruff (stops below the crest so crest-vs-cape still counts)
    out.append(((0, -0.28, 1.40), (0, -0.56, 1.40), 0.20, "Head"))
    return out'''))
# foot lift (the rest talons sit 0.028 under the ankle plane)
R.append(('''LEGS = ["Leg_L", "Leg_R"]


def ease(u):''', '''LEGS = ["Leg_L", "Leg_R"]
FOOT_LIFT = 0.012            # the modelled talon tips sit 0.028 under z 0: keep every planted claw >= -0.02


def ease(u):'''))
R.append(('''            z, toe = 0.0, 0.0
            if regrip and leg in regrip and regrip[leg][0] <= f <= regrip[leg][1]:
                u = (f - regrip[leg][0]) / float(regrip[leg][1] - regrip[leg][0])
                z, toe = 0.03 * math.sin(math.pi * u), 20 * math.sin(math.pi * u)
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y + dy, z)), toe=toe)''',
'''            z, toe = FOOT_LIFT, 0.0
            if regrip and leg in regrip and regrip[leg][0] <= f <= regrip[leg][1]:
                u = (f - regrip[leg][0]) / float(regrip[leg][1] - regrip[leg][0])
                z, toe = FOOT_LIFT + 0.07 * math.sin(math.pi * u), 14 * math.sin(math.pi * u)
            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y + dy, z)), toe=toe)'''))
# FK legs spread the feet sideways (no foot-vs-foot)
R.append(('''def legs_fk(k, f, thigh, shin, foot):
    for side in ("L", "R"):
        k.key("Leg_" + side, f, rot=(thigh, 0, 0), loc=(0, 0, 0))''',
'''def legs_fk(k, f, thigh, shin, foot, spread=5.0):
    for s, side in ((1, "L"), (-1, "R")):
        k.key("Leg_" + side, f, rot=(thigh, 0, -s * spread), loc=(0, 0, 0))'''))
# idle: breath on the Spine only (the chest pitch moved the folded wings into the fan); tail flick pitch only
R.append(('''        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(-1.5 * b, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
    look = [''', '''        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.008 * b))
        k.key("Chest", f, rot=(0, 0, 0))
        k.key("Jaw", f, rot=(0, 0, 0))
    look = ['''))
R.append(('''    for f, p, y in ((0, 0, 0), (86, 0, 0), (89, 10, 8), (92, -4, -6), (95, 0, 0), (132, 0, 0)):
        tail(k, f, p, y)''', '''    for f, p in ((0, 0), (86, 0), (89, 8), (92, -3), (95, 0), (132, 0)):    # tail flick (pitch only: the
        tail(k, f, p, 0)                                                      # folded primaries ride beside the fan)'''))
# walk: tail pitch only; gentler toe curl
R.append(('''        tail(k, f, 2 * pk.wave(f, n, 0.2, 2), 5 * pk.wave(f, n, 0.15))
    orig = k.solve_leg

    def strut(leg, f, T, foot_z=0.0, toe=None):
        lift = max(0.0, T.z)
        return orig(leg, f, T, foot_z, toe=22.0 * min(1.0, lift / 0.08) - (6.0 if 0 < lift < 0.02 else 0.0))''',
'''        tail(k, f, 2 * pk.wave(f, n, 0.2, 2), 0)
    orig = k.solve_leg

    def strut(leg, f, T, foot_z=0.0, toe=None):
        lift = max(0.0, T.z)
        T = Vector(T) + Vector((0, 0, FOOT_LIFT))
        return orig(leg, f, T, foot_z, toe=22.0 * min(1.0, lift / 0.12))'''))
# fly: fan raised (kit + lifts) clear of the balled feet
R.append(('''    tail(k, f, -6 + 4 * math.sin(2 * math.pi * (ph - 0.3)), 3 * math.sin(2 * math.pi * ph))
    if legs:
        fly_legs(k, f, ph)''', '''    tail(k, f, 6 + 4 * math.sin(2 * math.pi * (ph - 0.3)), 0)
    if legs:
        fly_legs(k, f, ph)'''))
# act: the hover / stoop fan flare is UP (kit +)
R.append(('''        (12, -0.02, 2, 0, 4, 6, 0, (30, 0, 0, 0), 4), (14, 0.12, 6, 0, 0, 4, 0, (-34, 8, 6, 4), -6),
        (18, 0.30, 10, 0, -2, 10, 0, (20, 4, 4, -4), -14), (21, 0.31, 10, 0, -2, 10, 0, (-20, 6, 4, 2), -14),
        (24, 0.30, 12, 0, -2, 10, 0, LIFT4, -14), (25, 0.28, 15, 0, -2, 10, 0, LIFT3, -12),
        (26, 0.25, 19, 0, -2, 10, 0, LIFT2, -10), (27, 0.21, 22, 0, -2, 10, 0, LIFT1, -8),
        (28, 0.16, 25, 0, -2, 10, 0, FOLD, -6), (30, 0.10, 25, 0, -2, 10, 0, FOLD, -6),''',
'''        (12, -0.02, 2, 0, 4, 6, 0, (30, 0, 0, 0), 4), (14, 0.12, 6, 0, 0, 4, 0, (-34, 8, 6, 4), 6),
        (18, 0.30, 10, 0, -2, 10, 0, (20, 4, 4, -4), 14), (21, 0.31, 10, 0, -2, 10, 0, (-20, 6, 4, 2), 14),
        (24, 0.30, 12, 0, -2, 10, 0, LIFT4, 14), (25, 0.28, 15, 0, -2, 10, 0, LIFT3, 12),
        (26, 0.25, 19, 0, -2, 10, 0, LIFT2, 10), (27, 0.21, 22, 0, -2, 10, 0, LIFT1, 8),
        (28, 0.16, 25, 0, -2, 10, 0, FOLD, 6), (30, 0.10, 25, 0, -2, 10, 0, FOLD, 6),'''))
R.append(('''            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)), toe=0.0)
    legs_fk(k, 16, 50, -30, 66)                                      # launch: push then tuck''',
'''            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT)), toe=0.0)
    legs_fk(k, 16, 50, -30, 66)                                      # launch: push then tuck'''))
R.append(('''            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.0)) + reach,
                        toe=-10.0 if f < 35 else 18.0)               # open, then clenched by f36''',
'''            k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT + 0.01)) + reach,
                        toe=-8.0 if f < 35 else 6.0)                 # open, then clenched by f36'''))
R.append(('''                T = Vector((k.J[leg].x, k.J[leg].y - 0.18 + 0.09 * ease(u), 0.04 * math.sin(math.pi * u)))
            elif f <= 72:
                u = (f - 66) / 6.0
                T = Vector((k.J[leg].x, k.J[leg].y - 0.09 + 0.09 * ease(u), 0.04 * math.sin(math.pi * u)))
            else:
                T = Vector((k.J[leg].x, k.J[leg].y, 0.0))''',
'''                T = Vector((k.J[leg].x, k.J[leg].y - 0.18 + 0.09 * ease(u), FOOT_LIFT + 0.05 * math.sin(math.pi * u)))
            elif f <= 72:
                u = (f - 66) / 6.0
                T = Vector((k.J[leg].x, k.J[leg].y - 0.09 + 0.09 * ease(u), FOOT_LIFT + 0.05 * math.sin(math.pi * u)))
            else:
                T = Vector((k.J[leg].x, k.J[leg].y, FOOT_LIFT))'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
