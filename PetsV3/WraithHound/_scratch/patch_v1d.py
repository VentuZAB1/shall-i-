p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\WraithHound.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''import math
from mathutils import Vector, Euler''', '''import math
import os
from mathutils import Vector, Euler''')
# rows sweep back further (each row's tail lies over the next row's root: one streaming mass)
rep('''    out = {"C": wisp(B, root, (0, 0.28, 1.0), (0, 1.0, 0.50), 0.22 * sc, 0.21 * sc, 0.068 * sc, 0.085 * sc, bone)}''',
    '''    out = {"C": wisp(B, root, (0, 0.30, 1.0), (0, 1.0, 0.36), 0.21 * sc, 0.25 * sc, 0.070 * sc, 0.088 * sc, bone)}''')
rep('''        out[sd] = wisp(B, r, (s_ * 0.40, 0.38, 1.0), (s_ * 0.30, 1.0, 0.30), 0.16 * sc, 0.17 * sc, 0.055 * sc,
                       0.070 * sc, bone + "_" + sd)''',
    '''        out[sd] = wisp(B, r, (s_ * 0.40, 0.40, 1.0), (s_ * 0.30, 1.0, 0.18), 0.15 * sc, 0.20 * sc, 0.056 * sc,
                       0.072 * sc, bone + "_" + sd)''')
# mane base: a soot ridge along the neck top (the wisps rise out of it); WH_NOMANE=1 skips the mane (share test)
rep('''    global MANE_TIPS
    MANE_TIPS = {}
    for bone, parent, root, sc in MANE:
        MANE_TIPS[bone] = mane_row(B, bone, root, sc)''', '''    global MANE_TIPS
    MANE_TIPS = {}
    if not os.environ.get("WH_NOMANE"):
        B.seg((0, -0.71, 0.985), (0, -0.44, 0.915), 0.058, 0.040, SOOT, "Neck", side=(1, 0, 0), ext=0.02,
              top=(0.92, 1), rnd=0.45)                                                       # mane ridge
        for bone, parent, root, sc in MANE:
            MANE_TIPS[bone] = mane_row(B, bone, root, sc)
    else:
        MANE_TIPS = {m[0]: {"C": m[2]} for m in MANE}''')
# thicker shins + mist socks
rep('''                B.seg(K, A, 0.050, 0.056, ASH_LAV, shin, top=(0.85, 0.85), ext=0.03, ext1=0.02, rnd=0.40)''',
    '''                B.seg(K, A, 0.054, 0.060, ASH_LAV, shin, top=(0.85, 0.85), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A + (K - A) * 0.36, A, 0.050, 0.056, MIST, shin, ext1=0.02, rnd=0.40, top=(1.02, 1.02))  # sock''')
rep('''                B.seg(K, A, 0.052, 0.060, ASH_LAV, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.046, 0.048, ASH_LAV, foot, ext=0.03, rnd=0.40)''',
    '''                B.seg(K, A, 0.056, 0.064, ASH_LAV, shin, top=(0.80, 0.80), ext=0.03, ext1=0.02, rnd=0.40)
                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.049, 0.051, MIST, foot, ext=0.03, rnd=0.40)   # sock''')
# softer tail tuft: a fat rounded brush instead of an arrowhead
rep('''    B.spike(P[4] - Vector((0, 0.04, -0.02)), (0, 0.40, -0.92), 0.13, 0.062, SOOT, "Tail4", top=(0.20, 0.30))  # tuft''',
    '''    B.seg(P[4] - Vector((0, 0.05, -0.03)), P[4] + Vector((0, 0.07, -0.12)), 0.070, 0.080, SOOT, "Tail4",
          top=(0.30, 0.40), rnd=0.45)                                                       # soft tuft''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
