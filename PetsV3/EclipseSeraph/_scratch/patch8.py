# round 3 margins: game-camera red 9-10 px (target >= 10) -> the tail brush 1.2x; portrait saturation 0.32 (target
# >= 0.33) -> WING_LILAC (190,150,226) -> (200,146,232) (hue 278 = the body family, not the 271 violet; S 0.37)
p = "pets/EclipseSeraph.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep("WING_LILAC = (190, 150, 226)", "WING_LILAC = (200, 146, 232)")
rep('    B.add(tip + Vector((0, 0.02, -0.01)), (0.10, 0.11, 0.095), BLOOD, "Tail4", rnd=0.4)        # blood brush',
    '    B.add(tip + Vector((0, 0.02, -0.01)), (0.12, 0.13, 0.11), BLOOD, "Tail4", rnd=0.4)         # blood brush')
rep('''    for d, L in (((0, 0.5, -0.8), 0.17), ((0.5, 0.4, -0.7), 0.13), ((-0.5, 0.4, -0.7), 0.13), ((0, 0.9, -0.2), 0.14),
                 ((0, 0.1, -1.0), 0.14)):
        tuft(B, tip + Vector((0, 0.02, -0.01)), d, L, 0.06, BLOOD, "Tail4")''',
    '''    for d, L in (((0, 0.5, -0.8), 0.20), ((0.5, 0.4, -0.7), 0.16), ((-0.5, 0.4, -0.7), 0.16), ((0, 0.9, -0.2), 0.17),
                 ((0, 0.1, -1.0), 0.17)):
        tuft(B, tip + Vector((0, 0.02, -0.01)), d, L, 0.07, BLOOD, "Tail4")''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
