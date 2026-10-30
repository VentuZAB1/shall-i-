p = "pets/FrostcrownDragon.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:80])
    s = s.replace(a, b)


rep('''DARK = (66, 72, 108)          # brow spines, back line, claw / fin sockets, scute gaps, nostril ridge''',
    '''DEEP_STEEL = (84, 110, 178)   # dorsal saddle (neck top, back, tail top, skull cap): the dark top band
DARK = (66, 72, 108)          # brow spines, back line, wing fingers + trim, claw / fin sockets, scute gaps''')
rep('''def fierce_eye(''', '''def prof(b, lz):
    t = (lz / b.h.z + 1) / 2
    fx = b.bot[0] + (b.top[0] - b.bot[0]) * t
    fy = b.bot[1] + (b.top[1] - b.bot[1]) * t
    return b.h.x * fx, b.h.y * fy, b.ts[1] * t


def shell(B, b, y0, y1, za, color, pad=0.022, bone=None, rnd=0.34, **kw):
    """saddle shell over body block b: local y range [y0, y1], local z from za up over the top (ThunderRex)"""
    xa, ya, oa = prof(b, za)
    xb, yb, ob = prof(b, b.h.z)
    zb = b.h.z + pad
    lo_a, hi_a = max(y0 + oa, oa - ya - pad), min(y1 + oa, oa + ya + pad)
    lo_b, hi_b = max(y0 + ob, ob - yb - pad), min(y1 + ob, ob + yb + pad)
    cy, hy = (lo_a + hi_a) / 2, (hi_a - lo_a) / 2
    hx = xa + pad
    c = b.world(Vector((0, cy, (za + zb) / 2)))
    return B.add(c, (hx, hy, (zb - za) / 2), color, bone or b.bone, R=b.R,
                 top=((xb + pad) / hx, (hi_b - lo_b) / 2 / hy), top_shift=(0, (lo_b + hi_b) / 2 - cy), rnd=rnd, **kw)


def fierce_eye(''')
rep('''    withers = B.add((0, -0.38, 1.19), (0.22, 0.26, 0.07), STEEL_BLUE, "Chest", top=(0.70, 0.80))''',
    '''    withers = B.add((0, -0.38, 1.20), (0.22, 0.26, 0.07), DEEP_STEEL, "Chest", top=(0.70, 0.80))''')
rep('''    # pale ice scute underside: brisket plate''', '''    # the dark top band: DEEP_STEEL saddle shells over the ribcage, waist and hips
    sh_rib = shell(B, rib, -0.40, 0.40, 0.08, DEEP_STEEL)
    sh_waist = shell(B, waist, -0.26, 0.26, 0.02, DEEP_STEEL)
    sh_hips = shell(B, hips, -0.24, 0.24, 0.0, DEEP_STEEL)
    # pale ice scute underside: brisket plate''')
rep('''        B.seg(a + fn * (off - 0.035), b + fn * (off - 0.035), hw, 0.05, ICE_BELLY, bone, ext=0.02, ext1=0.0)''',
    '''        B.seg(a + fn * (off - 0.035), b + fn * (off - 0.035), hw, 0.05, ICE_BELLY, bone, ext=0.02, ext1=0.0)
        B.seg(a - fn * (off - 0.05), b - fn * (off - 0.05), hw * 1.25, 0.06, DEEP_STEEL, bone, ext=0.04, ext1=0.0,
              rnd=0.4)                                                                             # neck saddle''')
rep('''    B.add(HC, (0.155, 0.16, 0.125), STEEL_BLUE, "Head", top=(0.80, 0.85), rnd=0.25)                   # skull''',
    '''    B.add(HC, (0.155, 0.16, 0.125), STEEL_BLUE, "Head", top=(0.80, 0.85), rnd=0.25)                   # skull
    B.add(HC + Vector((0, 0.03, 0.10)), (0.125, 0.13, 0.04), DEEP_STEEL, "Head", top=(0.8, 0.8), rnd=0.3)  # skull cap''')
rep('''    tops = [rib, withers, waist, hips]''', '''    tops = [sh_rib, withers, sh_waist, sh_hips]''')
rep('''        B.seg(a - fn * (off - 0.05)''', '''        B.seg(a - fn * (off - 0.05)''')
# neck stripe offset must clear the neck saddle (+0.06)
rep('''(N0 + Vector((0, 0.03, -0.05)), N1, "Neck", 0.17, 0.085), (N1, N2, "Neck2", 0.145, 0.07)):''',
    '''(N0 + Vector((0, 0.03, -0.05)), N1, "Neck", 0.215, 0.085), (N1, N2, "Neck2", 0.19, 0.07)):''')
# tail: DEEP_STEEL top band under the dark stripe
rep('''        B.seg(a + Vector((0, 0, d - 0.025)), b + Vector((0, 0, dims[min(i + 1, 3)][1] * 0.82 - 0.025)), w * 0.55,
              0.02, DARK, bone, ext=0.02 if i else -0.04, top=(0.8, 1), rnd=0.4)                  # dorsal band''',
    '''        B.seg(a + Vector((0, 0, d * 0.55)), b + Vector((0, 0, dims[min(i + 1, 3)][1] * 0.82 * 0.55)), w * 0.96,
              d * 0.55, DEEP_STEEL, bone, ext=0.04 if i else -0.02, top=(0.82, 0.82), rnd=0.4)     # tail saddle
        B.seg(a + Vector((0, 0, d * 1.08 - 0.01)), b + Vector((0, 0, dims[min(i + 1, 3)][1] * 0.82 * 1.08 - 0.01)),
              w * 0.45, 0.02, DARK, bone, ext=0.02 if i else -0.04, top=(0.8, 1), rnd=0.4)        # dorsal band''')
rep('''            B.spike(p + Vector((0, 0, hgt - 0.02)), (0, 0.6, 0.8)''', '''            B.spike(p + Vector((0, 0, hgt + 0.01)), (0, 0.6, 0.8)''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
