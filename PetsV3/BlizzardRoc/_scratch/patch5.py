# round 2b MUST 4 test (the front still read as goggles): the violet slit thinner and set low under a heavy black lid
# (a slit, not a lens); slit, FROST_H spot and pupil kept (D3), only their heights
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.045 * sc, 0.006, 0.0125 * sc), FROST_V, bone, R=R,''',
    '''    B.add(c + R @ Vector((0.002 * s, -0.006, -0.006 * sc)), (0.045 * sc, 0.006, 0.0085 * sc), FROST_V, bone, R=R,''')
rep('''    B.add(c + R @ Vector((s * 0.020 * sc, -0.0095, -0.001)), (0.014 * sc, 0.004, 0.006 * sc), FROST_H, bone, R=R,''',
    '''    B.add(c + R @ Vector((s * 0.020 * sc, -0.0095, -0.006 * sc)), (0.014 * sc, 0.004, 0.0045 * sc), FROST_H, bone, R=R,''')
rep('''    B.add(c + R @ Vector((-s * 0.004 * sc, -0.0105, -0.001)), (0.005 * sc, 0.004, 0.0118 * sc), BLACK, bone, R=R,''',
    '''    B.add(c + R @ Vector((-s * 0.004 * sc, -0.0105, -0.006 * sc)), (0.005 * sc, 0.004, 0.0085 * sc), BLACK, bone, R=R,''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
