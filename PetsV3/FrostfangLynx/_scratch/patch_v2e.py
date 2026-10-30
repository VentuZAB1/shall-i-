p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\FrostfangLynx.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


# saddle = a dark fur cape that WRAPS the top edges of each torso block (no plates lying on top)
rep('''    for a, b, bone in (((0, -0.33, 0.795), (0, -0.06, 0.788), "Chest"), ((0, -0.08, 0.788), (0, 0.12, 0.768), "Spine"),
                       ((0, 0.10, 0.770), (0, 0.38, 0.786), "Spine")):
        B.seg(a, b, 0.100, 0.022, BACK_SHADE, bone, side=(1, 0, 0), ext=0.04, ext1=0.04, top=(0.86, 1), rnd=0.45)''',
    '''    for a, b, hw, bone in (((0, -0.385, 0.754), (0, 0.005, 0.754), 0.140, "Chest"),
                           ((0, -0.06, 0.729), (0, 0.22, 0.729), 0.120, "Spine"),
                           ((0, 0.18, 0.771), (0, 0.44, 0.744), 0.121, "Spine")):
        B.seg(a, b, hw, 0.043, BACK_SHADE, bone, side=(1, 0, 0), top=(0.92, 1), rnd=0.45)''')
# slimmer V chest ruff
rep('''    B.add((0, -0.418, 0.600), (0.102, 0.028, 0.135), SNOW, "Chest", bot=(0.30, 0.8), top=(1.0, 1), rot=(-14, 0, 0),
          rnd=0.35)''', '''    B.add((0, -0.418, 0.600), (0.086, 0.028, 0.135), SNOW, "Chest", bot=(0.30, 0.8), top=(1.0, 1), rot=(-14, 0, 0),
          rnd=0.35)''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
