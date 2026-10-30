# review 2 M1: the eye is a slit under a black lid, not a lens (socket 0.046 x 0.011 at z +0.004, hot spot 0.003 tall)
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''    B.add(c + R @ Vector((s * 0.002, 0, 0.0 * sc)), (0.050 * sc, 0.008, 0.017 * sc), BLACK, bone, R=R, studs=[],''',
    '''    B.add(c + R @ Vector((s * 0.002, 0, 0.004 * sc)), (0.046 * sc, 0.008, 0.011 * sc), BLACK, bone, R=R, studs=[],''')
rep('''(0.014 * sc, 0.004, 0.0045 * sc), FROST_H, bone, R=R,''', '''(0.014 * sc, 0.004, 0.003 * sc), FROST_H, bone, R=R,''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
