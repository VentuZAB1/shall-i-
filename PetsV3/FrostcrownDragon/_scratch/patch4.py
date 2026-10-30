# round 2b: the frost core layering bug (the DARK setting stood in front of the ICE_W crystal, so only the small
# ICE_BELLY facet showed): setting recessed, crystal 0.011 proud of it, facet + facet edges on the crystal face
p = "pets/FrostcrownDragon.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:90])
    s = s.replace(a, b)


rep('''    B.poly([cp + cn * 0.004 + cu * (x * 1.18) + cv * (y * 1.14) for x, y in hexa], 0.03, DARK, "Chest")
    B.poly([cp + cn * (0.012 - 0.022) + cu * x + cv * y for x, y in hexa], 0.044, ICE_W, "Chest")
    B.poly([cp + cn * 0.016 + cu * (x * 0.52) + cv * (y * 0.56) for x, y in hexa], 0.008, ICE_BELLY, "Chest")''',
    '''    B.poly([cp - cn * 0.004 + cu * (x * 1.16) + cv * (y * 1.12) for x, y in hexa], 0.03, DARK, "Chest")   # setting
    B.poly([cp + cu * x + cv * y for x, y in hexa], 0.044, ICE_W, "Chest")                  # crystal, face at +0.022
    B.poly([cp + cn * 0.024 + cu * (x * 0.52) + cv * (y * 0.56) for x, y in hexa], 0.006, ICE_BELLY, "Chest")''')
rep('''        B.bar(cp + cn * 0.013 + cu * x0 + cv * y0, cp + cn * 0.013 + cu * x1 + cv * y1, cn, 0.012, 0.004, ICE_BELLY,''',
    '''        B.bar(cp + cn * 0.024 + cu * x0 + cv * y0, cp + cn * 0.024 + cu * x1 + cv * y1, cn, 0.012, 0.004, ICE_BELLY,''')
rep('    ANCH["Core"] = tuple(cp + cn * 0.02)', '    ANCH["Core"] = tuple(cp + cn * 0.03)')
open(p, "w", encoding="utf-8").write(s)
print("ok")
