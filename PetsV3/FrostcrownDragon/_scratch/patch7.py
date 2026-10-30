# review 2 M1 follow-up: from the front the outer points stood on the gold horn roots (gold on gold); the horn roots
# move out to the skull edge and back so all five points read against the skull / sky; a GOLD back band with three
# points (a crown ring the game camera sees from behind); thicker sides. N1: saddle shell pad 0.022 -> 0.030.
p = "pets/FrostcrownDragon.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''        P = [HC + Vector((s * 0.09, 0.04, 0.12)), HC + Vector((s * 0.17, 0.16, 0.27)),          # roots BEHIND the
             HC + Vector((s * 0.25, 0.36, 0.30)), HC + Vector((s * 0.31, 0.74, 0.40))]          # band, leaning back''',
    '''        P = [HC + Vector((s * 0.17, 0.05, 0.10)), HC + Vector((s * 0.22, 0.17, 0.24)),          # roots behind the
             HC + Vector((s * 0.27, 0.36, 0.30)), HC + Vector((s * 0.31, 0.74, 0.40))]          # band ends, lean back''')
rep('''        B.seg(HC + Vector((s * 0.146, -0.15, 0.106)), HC + Vector((s * 0.142, 0.15, 0.10)), 0.022, 0.040, GOLD,''',
    '''        B.seg(HC + Vector((s * 0.150, -0.15, 0.106)), HC + Vector((s * 0.146, 0.15, 0.10)), 0.028, 0.050, GOLD,''')
rep('''    B.add(HC + Vector((0, 0.158, 0.10)), (0.13, 0.016, 0.04), GOLD_D, "Head", studs=[], nostud=True, role="limb",
          bevel=0.006)                                                                             # diadem back''',
    '''    B.add(HC + Vector((0, 0.160, 0.105)), (0.15, 0.022, 0.05), GOLD, "Head", studs=[], nostud=True, role="limb",
          bevel=0.006)                                                                             # diadem back
    for x, h, w in ((-0.07, 0.06, 0.020), (0.0, 0.08, 0.024), (0.07, 0.06, 0.020)):              # back points
        B.spike(HC + Vector((x, 0.172, 0.14)), (x * 0.8, 0.30, 1), h, w, GOLD_D, "Head", top=(0.12, 0.12), nostud=True)''')
rep("def shell(B, b, y0, y1, za, color, pad=0.022, bone=None, rnd=0.34, **kw):",
    "def shell(B, b, y0, y1, za, color, pad=0.030, bone=None, rnd=0.34, **kw):")
open(p, "w", encoding="utf-8").write(s)
print("ok")
