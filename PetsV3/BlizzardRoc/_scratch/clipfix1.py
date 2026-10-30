# clip pass 1 fixes: knee capsule (the Thunderbird's: the drumstick top is buried in the belly feathers), shallower
# crouches, the walk chest rides with the spine (the folded wings moved against the flank), wider trailing legs
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep("        out.append((tuple(K - d * 0.08), tuple(K + d * 0.15), 0.10, \"Shin_\" + sd))     # knee (trouser top)",
    "        out.append((tuple(K - d * 0.10), tuple(K + d * 0.20), 0.13, \"Shin_\" + sd))     # knee (trouser top in the belly feathers, the Thunderbird's capsule)")
# walk: chest rides with the spine, smaller roll / yaw, lower foot lift, wider pass
rep('''        sy = 3 * pk.wave(f, n, 0.0)
        sr = 4 * pk.wave(f, n, 0.05)
        cy, cr = -1.5 * pk.wave(f, n, 0.05), -1.5 * pk.wave(f, n, 0.05)''',
    '''        sy = 2 * pk.wave(f, n, 0.0)
        sr = 3 * pk.wave(f, n, 0.05)
        cy, cr = 0.0, 0.0''')
rep("        T = Vector(T) + Vector((sx * 0.025 * min(1.0, lift / 0.05), 0, FOOT_LIFT))",
    "        T = Vector(T) + Vector((sx * 0.04 * min(1.0, lift / 0.05), 0, FOOT_LIFT))")
rep("        return cm.biped_walk(k, n, 0.15, 0.09, body, legs=((\"Leg_L\", 0.0), (\"Leg_R\", 0.5)), duty=0.6)",
    "        return cm.biped_walk(k, n, 0.15, 0.07, body, legs=((\"Leg_L\", 0.0), (\"Leg_R\", 0.5)), duty=0.6)")
# idle regrip lift
rep("                z, toe = FOOT_LIFT + 0.06 * math.sin(math.pi * u), 14 * math.sin(math.pi * u)",
    "                z, toe = FOOT_LIFT + 0.04 * math.sin(math.pi * u), 14 * math.sin(math.pi * u)")
# roar crouch
rep("(8, 2, -0.02, -2, -6, 0, -6, 2), (14, -3, -0.01, -3, -12, 0, -8, 4)", "(8, 2, -0.01, -2, -6, 0, -6, 2), (14, -3, 0.0, -3, -12, 0, -8, 4)")
# bow bobs: -0.02 base, -0.06 bottom
rep('''        (12, 6, -0.02, 2, 14, 0, 4), (22, 10, -0.03, 3, 25, 0, 8),
        (28, 10, -0.09, 3, 25, 0, 8), (33, 10, -0.03, 3, 25, 0, 8), (38, 10, -0.09, 3, 25, 0, 8), (44, 10, -0.03, 3, 25, 0, 8),''',
    '''        (12, 6, -0.01, 2, 14, 0, 4), (22, 10, -0.02, 3, 25, 0, 8),
        (28, 10, -0.06, 3, 25, 0, 8), (33, 10, -0.02, 3, 25, 0, 8), (38, 10, -0.06, 3, 25, 0, 8), (44, 10, -0.02, 3, 25, 0, 8),''')
# takeoff crouch
rep('''    for f, z, p, ch, w in ((3, -0.03, 4, 2, LIFT1), (6, -0.06, 7, 3, LIFT2), (8, -0.08, 8, 3, LIFT3),
                           (9, -0.09, 9, 3, LIFT4), (10, -0.10, 9, 3, (34, 0, 0, 0)),''',
    '''    for f, z, p, ch, w in ((3, -0.02, 4, 2, LIFT1), (6, -0.04, 7, 3, LIFT2), (8, -0.05, 8, 3, LIFT3),
                           (9, -0.055, 9, 3, LIFT4), (10, -0.06, 9, 3, (34, 0, 0, 0)),''')
# land absorb
rep("    for f, z, p, w in ((17, -0.08, 7, SPAN), (22, -0.05, 4, SPAN), (24, -0.04, 3, LIFT4),",
    "    for f, z, p, w in ((17, -0.05, 7, SPAN), (22, -0.035, 4, SPAN), (24, -0.03, 3, LIFT4),")
# flight legs: trail a little higher and wider, beside the four tail feathers
rep("THI, SHI, FOO = 70.0, -36.0, 70.0", "THI, SHI, FOO = 62.0, -32.0, 64.0")
rep('''        k.key("Leg_" + side, f, rot=((THI + 4 * math.sin(2 * math.pi * (p - 0.15))) * amt, 0, -s * 3 * amt),''',
    '''        k.key("Leg_" + side, f, rot=((THI + 4 * math.sin(2 * math.pi * (p - 0.15))) * amt, 0, -s * 9 * amt),''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
