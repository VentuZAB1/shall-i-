# round 2b MUST 4: the gape->eye CHAR piece + the brow framed the eye from the front (goggles); the stripe now starts
# AT the eye and runs back along the skull side to the nape (the osprey line), the socket a little lower
p = "pets/BlizzardRoc.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''        # osprey mask: ONE slanted CHAR stripe from the gape through the eye and back along the skull side to the
        # nape (no box round the eye): a front piece under the eye on the face, the side band, the nape tail
        ec = HC + Vector((s * 0.104, -0.128, 0.022))
        B.bar(HC + Vector((s * 0.084, -0.172, -0.022)), HC + Vector((s * 0.112, -0.108, 0.010)),
              Vector((s, -0.55, 0)), 0.042, 0.012, CHAR, "Head", studs=[], role="detail", bevel=0.004)
''', '''        # osprey mask: ONE CHAR stripe from the eye back along the skull side to the nape (no box round the eye, no
        # piece in front of it): the side band + the nape tail
        ec = HC + Vector((s * 0.104, -0.128, 0.022))
''')
rep('''    B.add(c + R @ Vector((s * 0.002, 0, 0.003 * sc)), (0.050 * sc, 0.008, 0.019 * sc), BLACK, bone, R=R, studs=[],''',
    '''    B.add(c + R @ Vector((s * 0.002, 0, 0.0 * sc)), (0.050 * sc, 0.008, 0.017 * sc), BLACK, bone, R=R, studs=[],''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
