p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\FrostfangLynx.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


rep('''    for a, b, hw, bone in (((0, -0.385, 0.754), (0, 0.005, 0.754), 0.140, "Chest"),
                           ((0, -0.06, 0.729), (0, 0.22, 0.729), 0.120, "Spine"),
                           ((0, 0.18, 0.771), (0, 0.44, 0.744), 0.121, "Spine")):
        B.seg(a, b, hw, 0.043, BACK_SHADE, bone, side=(1, 0, 0), top=(0.92, 1), rnd=0.45)''',
    '''    # (flush dorsal inlays on each torso top: see saddle() below the torso blocks)''')
rep('''    # darker saddle along the top line, draped over the top edges: withers -> waist -> rump (one continuous run)''',
    '''    # darker saddle along the top line: flush irregular inlays on the tops of chest, waist and hips (no plates)
    for blk, w, sd in ((rib, 0.092, 5), (waist, 0.080, 6), (hips, 0.082, 7)):
        saddle(B, blk, w, sd)''')
rep('''SPOT = BACK_SHADE


def model(k):''', '''SPOT = BACK_SHADE


def saddle(B, b, w, seed):
    """a darker-back inlay lying flush on the top face of torso block b: an irregular elongated octagon"""
    rng = random.Random(seed)
    L = b.h.y * b.top[1] - 0.034
    ts = Vector((b.ts[0], b.ts[1], 0))
    pts = []
    for u, v in ((-0.62, -1), (0.62, -1), (1, -0.72), (1, 0.72), (0.62, 1), (-0.62, 1), (-1, 0.72), (-1, -0.72)):
        j = 0.94 + 0.10 * rng.random()
        pts.append(b.world(Vector((u * w * j, v * L, b.h.z + 0.004)) + ts))
    B.poly(pts, 0.010, BACK_SHADE, b.bone)


def model(k):''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
