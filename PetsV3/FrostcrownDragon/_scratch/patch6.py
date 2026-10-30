# review 2 (REVISE 7/10) M1 crown from the front, M2 no belly rungs, M3 STEEL_BLUE darker
p = "pets/FrostcrownDragon.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep("STEEL_BLUE = (70, 118, 190)   # body, neck, legs, tail, head (studded) - plan hue 216, richer (review 1 MUST 4)",
    "STEEL_BLUE = (62, 104, 176)   # body, neck, legs, tail, head (studded) - plan hue 216, richer (review 2 M3)")
rep('''    for t, w in ((0.40, 0.10), (0.80, 0.09)):
        p = Vector((0, -0.14, 0.566)).lerp(Vector((0, 0.32, 0.686)), t)
        B.bar(p + Vector((-w, 0, 0)), p + Vector((w, 0, 0)), Vector((0, 0, -1)), 0.02, 0.008, DARK, "Spine",
              studs=[], bevel=0.003, nostud=True)
''', '')
rep("    # pale ice scute underside: brisket plate, belly strip up the tuck, keel plate on the chest front, scute gaps",
    "    # pale ice scute underside: brisket plate + a plain belly strip up the tuck (no rungs: review 2 M2)")
rep('''        P = [HC + Vector((s * 0.09, -0.06, 0.12)), HC + Vector((s * 0.17, 0.11, 0.27)),
             HC + Vector((s * 0.25, 0.36, 0.36)), HC + Vector((s * 0.31, 0.74, 0.40))]''',
    '''        P = [HC + Vector((s * 0.09, 0.04, 0.12)), HC + Vector((s * 0.17, 0.16, 0.27)),          # roots BEHIND the
             HC + Vector((s * 0.25, 0.36, 0.30)), HC + Vector((s * 0.31, 0.74, 0.40))]          # band, leaning back''')
rep('''    B.add(HC + Vector((0, -0.152, 0.11)), (0.15, 0.030, 0.040), GOLD, "Head", top=(0.92, 1), role="limb",''',
    '''    B.add(HC + Vector((0, -0.152, 0.11)), (0.20, 0.040, 0.050), GOLD, "Head", top=(0.92, 1), role="limb",''')
rep('''    for x, h, w in ((-0.10, 0.06, 0.020), (-0.05, 0.09, 0.024), (0.0, 0.13, 0.030), (0.05, 0.09, 0.024),
                    (0.10, 0.06, 0.020)):                                                       # five points''',
    '''    for x, h, w in ((-0.10, 0.07, 0.022), (-0.05, 0.10, 0.026), (0.0, 0.15, 0.032), (0.05, 0.10, 0.026),
                    (0.10, 0.07, 0.022)):                                                       # five points''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
