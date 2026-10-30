# review 1 (APPROVED WITH FIXES 7/10): MUST 1-6 + NICE 1, 2
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


# MUST 1 span 1.89 H -> >= 2.0 H
rep("_raise((2.00 + WDX, 0.30, 1.40))", "_raise((2.11 + WDX, 0.30, 1.40))")
# MUST 2 covert bars violet (straight, one per feather)
rep("taper=0.5, bars=[(CHAR, 0.30)] if t > 0.22 else None)", "taper=0.5, bars=[(FROST_V, 0.24)] if t > 0.22 else None)")
# MUST 3 crest: violet outer 60 %, fatter plumes
rep("def plume(B, root, d, L, w, bone, cols=(SNOW, FROST_V), fracs=(0.55, 0.45)):",
    "def plume(B, root, d, L, w, bone, cols=(SNOW, FROST_V), fracs=(0.40, 0.60)):")
rep('(("C", (0, -0.47, 1.70), (0, 0.30, 0.95), 0.31, 0.10),', '(("C", (0, -0.47, 1.70), (0, 0.30, 0.95), 0.31, 0.115),')
rep('("L", (0.05, -0.45, 1.69), (0.36, 0.34, 0.87), 0.25, 0.088),', '("L", (0.055, -0.45, 1.69), (0.36, 0.34, 0.87), 0.25, 0.105),')
rep('("R", (-0.05, -0.45, 1.69), (-0.36, 0.34, 0.87), 0.25, 0.088)):', '("R", (-0.055, -0.45, 1.69), (-0.36, 0.34, 0.87), 0.25, 0.105)):')
# MUST 4 osprey stripe, not a visor
rep("(0.088, 0.008, 0.044), CHAR, \"Head\", R=Re, studs=[],", "(0.070, 0.008, 0.028), CHAR, \"Head\", R=Re, studs=[],")
rep("0.07, 0.014, CHAR, \"Head\", studs=[], role=\"detail\", bevel=0.005, top=(1, 0.6))",
    "0.07, 0.018, CHAR, \"Head\", studs=[], role=\"detail\", bevel=0.005, top=(1, 0.45))")
rep("B.add(HC + Vector((s * 0.080, -0.090, 0.072)), (0.088, 0.04, 0.034), CHAR, \"Head\",",
    "B.add(HC + Vector((s * 0.080, -0.090, 0.068)), (0.075, 0.04, 0.024), CHAR, \"Head\",")
# MUST 5 white nape collar (top Neck2 cape row SNOW)
rep('''    neck_cape(B, n2a, n2b, 0.13, [(0.85, (-0.065, 0.0, 0.065)), (0.50, (-0.065, 0.0, 0.065))], "Neck2")''',
    '''    neck_cape(B, n2a, n2b, 0.13, [(0.85, (-0.065, 0.0, 0.065))], "Neck2", col=SNOW)        # white nape collar
    neck_cape(B, n2a, n2b, 0.13, [(0.50, (-0.065, 0.0, 0.065))], "Neck2")''')
# MUST 6 tail: four wider feathers
rep('tp = feather(B, root, root + d * L, fan_n, 0.15, 0.03, STORM_GREY, "Tail2", taper=0.30,',
    'tp = feather(B, root, root + d * L, fan_n, 0.22, 0.03, STORM_GREY, "Tail2", taper=0.45,')
# NICE 1 violet centre chevron, NICE 2 wider pale belly strip
rep('''    for lz, hw in ((0.12, 0.46), (0.01, 0.56), (-0.10, 0.46)):
        face_bar(B, keel, -1, lz, hw * keel.h.x * 2, 0.03, CHAR, "Chest", vee=20.0, proud=0.026)''',
    '''    for lz, hw, c in ((0.12, 0.46, CHAR), (0.01, 0.56, FROST_V), (-0.10, 0.46, CHAR)):
        face_bar(B, keel, -1, lz, hw * keel.h.x * 2, 0.03, c, "Chest", vee=20.0, proud=0.026)''')
rep('B.seg((0, -0.07, 0.585), (0, 0.22, 0.51), 0.10, 0.03, PALE_G, "Spine", top=(0.7, 1.0))',
    'B.seg((0, -0.07, 0.585), (0, 0.22, 0.51), 0.13, 0.03, PALE_G, "Spine", top=(0.7, 1.0))')
open(p, "w", encoding="utf-8").write(s)
print("ok")
