p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\FrostfangLynx.py"
s = open(p, encoding="utf-8").read()
rep = [
 # T2 coat switch (comparison renders); default picked after the comparison
 ('''WARM_SILVER = (190, 172, 150)  # body / legs / head sides (studded)
BACK_SHADE = (126, 116, 110)   # saddle, brows, ear backs, rosette spots (>= 20 % of the side view)''',
  '''WARM_SILVER = (190, 172, 150)  # body / legs / head sides (studded)
BACK_SHADE = (126, 116, 110)   # saddle, brows, ear backs, rosette spots (>= 20 % of the side view)
COATS = {"warm": ((190, 172, 150), (126, 116, 110)),          # v2 (beige in game - final85 review T2)
         "sand": ((170, 156, 138), (108, 98, 92)),            # deeper sand
         "frost": ((168, 176, 188), (100, 106, 122))}         # cool frost-silver
COAT = os.environ.get("LYNX_COAT", "warm")
WARM_SILVER, BACK_SHADE = COATS[COAT]'''),
 # M1: one continuous dorsal band instead of three inlays
 ('''    # darker saddle along the top line: flush irregular inlays on the tops of chest, waist and hips (no plates)
    for blk, w, sd in ((rib, 0.092, 5), (waist, 0.080, 6), (hips, 0.082, 7)):
        saddle(B, blk, w, sd)
    # (flush dorsal inlays on each torso top: see saddle() below the torso blocks)''',
  '''    # final85 M1: ONE continuous dark dorsal band from the nape scruff over chest, waist and hips to the tail root
    dorsal_band(B, (rib, waist, hips))'''),
 # M3: chest-ruff points get ICE tips
 ('''    for s in (1, -1):                                       # chest-ruff points between the forelegs
        B.spike((s * 0.030, -0.355, 0.515), (s * 0.15, -0.30, -1), 0.062, 0.028, SNOW, "Chest", top=(0.15, 0.45))''',
  '''    for s in (1, -1):                                       # chest-ruff points between the forelegs, ICE tips (M3)
        frost_point(B, (s * 0.030, -0.355, 0.515), (s * 0.15, -0.30, -1), 0.062, 0.028, "Chest")'''),
 ('''        B.spike(q, (sx * 0.25, -0.45, -1), 0.058, 0.026, SNOW, "Neck", top=(0.45, 0.60), rnd=0.40)   # soft tips''',
  '''        frost_point(B, q, (sx * 0.25, -0.45, -1), 0.058, 0.026, "Neck", soft=True)             # soft ICE tips (M3)'''),
 ('''        B.spike((s * 0.033, -0.757, 0.846), (0, -0.1, -1), 0.066, 0.014, ICE_CLAW, "Head", role="detail")  # frost fangs''',
  '''        B.spike((s * 0.033, -0.757, 0.846), (0, -0.1, -1), 0.066, 0.014, ICE, "Head", role="detail")  # frost fangs (M3)'''),
 # M2: warm paws + thin snow sole
 ('''                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.050, 0.050, SNOW, foot, ext=0.03, rnd=0.40)''',
  '''                B.seg(A, Pw + Vector((0, 0.03, 0.025)), 0.050, 0.050, WARM_SILVER, foot, ext=0.03, rnd=0.40)'''),
 ('''            B.add(Pw, (0.076, 0.088, 0.042), SNOW, foot, top=(0.86, 0.80), rnd=0.40)            # snowshoe paw
            for j, gx in enumerate(CLAWX):
                cb = ("Claw_%s%s%d" % (fb, side, j + 1)) if fb == "F" else foot   # review 3 M2: one bone per claw
                B.spike((Pw.x + gx, Pw.y - 0.076, 0.032), (0, -1, -0.55), 0.056, 0.012, ICE, cb)''',
  '''            B.add(Pw, (0.076, 0.088, 0.042), WARM_SILVER, foot, top=(0.86, 0.80), rnd=0.40)     # snowshoe paw (M2)
            B.add((Pw.x, Pw.y, 0.006), (0.078, 0.090, 0.006), SNOW, foot, studs=[], role="detail",
                  bevel=0.003)                                                              # thin snow sole (M2)
            for j, gx in enumerate(CLAWX):
                cb = ("Claw_%s%s%d" % (fb, side, j + 1)) if fb == "F" else foot   # review 3 M2: one bone per claw
                B.spike((Pw.x + gx, Pw.y - 0.076, CLAWZ), CLAWD, 0.072, 0.014, ICE, cb)   # final85 M4: longer'''),
 ('''CLAWX = (-0.043, -0.015, 0.015, 0.043)''',
  '''CLAWX = (-0.043, -0.015, 0.015, 0.043)
CLAWZ, CLAWD = 0.036, (0, -1, -0.50)      # claw base height + direction (0.072 long: tips stay above the floor)'''),
 ('''                    k.joint("Claw_F%s%d" % (side, j + 1), (Pw.x + gx, Pw.y - 0.076, 0.032), "Claw_F" + side,
                            tail=(0, -0.05, -0.0275))''',
  '''                    k.joint("Claw_F%s%d" % (side, j + 1), (Pw.x + gx, Pw.y - 0.076, CLAWZ), "Claw_F" + side,
                            tail=(0, -0.05, -0.025))'''),
 # T1: drop one spot per flank block
 ('''                                                     (0.150, 0.040, 0.028, 70, False), (-0.130, 0.140, 0.024, 10, False))):''',
  '''                                                     (0.150, 0.040, 0.028, 70, False))):'''),
 ('''            for i, (ly, lz, r, a, ros) in enumerate(((-0.070, 0.030, 0.046, 30, True), (0.065, 0.050, 0.040, 70, False),
                                                     (0.010, -0.045, 0.036, 0, False))):''',
  '''            for i, (ly, lz, r, a, ros) in enumerate(((-0.070, 0.030, 0.046, 30, True), (0.065, 0.050, 0.040, 70, False))):'''),
 ('''                                                     (-0.100, -0.060, 0.030, 60, False), (0.040, 0.105, 0.028, 30, False))):''',
  '''                                                     (-0.100, -0.060, 0.030, 60, False))):'''),
]
for a, b in rep:
    assert a in s, a[:70]
    s = s.replace(a, b)

old = s[s.index("def rosette("):s.index("SPOT = BACK_SHADE")]
new = '''def rosette(B, b, s, ly, lz, r, seed, ang=0.0):
    """lynx rosette (final85 T1): a ring of 6 small dark blobs around an open coat-coloured centre"""
    for i in range(6):
        a = math.radians(ang + 60 * i)
        blob(B, b, s, ly + math.cos(a) * r * 0.74, lz + math.sin(a) * r * 0.74, r * 0.36, seed + i, el=1.25,
             ang=ang + 60 * i + 90, n=6)


def frost_point(B, base, d, L, w, bone, soft=False):
    """a SNOW fur point with a frosted ICE tip (outer 45 %, smooth) - the cheek-ruff method (final85 M3)"""
    dn = Vector(d).normalized()
    kb = dict(top=(0.45, 0.60), rnd=0.40) if soft else dict(top=(0.57, 0.62))
    B.spike(base, d, L * 0.55, w, SNOW, bone, **kb)
    kt = dict(top=(0.45, 0.60), rnd=0.40) if soft else dict(top=(0.38, 0.50))
    B.spike(Vector(base) + dn * (L * 0.55 - 0.004), d, L * 0.45 + 0.004, w * (0.62 if soft else 0.57), ICE,
            bone, role="detail", nostud=True, **kt)


def top_z(blk, y):
    """height of the rounded top of torso block blk along its centre line at world y (None = not over it).
    Edge rounding = the blockkit bevel: rnd x the smallest half-size (capped at 0.45 x)."""
    mn = min(blk.h.x * min(blk.top[0], blk.bot[0]), blk.h.y * min(blk.top[1], blk.bot[1]), blk.h.z)
    r = min(blk.rnd if blk.rnd is not None else 0.3, 0.45) * mn
    hy = blk.h.y * blk.top[1]
    best = None
    for i in range(81):                                   # walk the local top edge, keep the sample nearest world y
        ly = -hy + 2 * hy * i / 80
        d = max(0.0, abs(ly) - (hy - r))
        lz = blk.h.z - (r - math.sqrt(max(0.0, r * r - d * d)))
        p = blk.world(Vector((0, ly + blk.ts[1], lz)))
        if best is None or abs(p.y - y) < abs(best.y - y):
            best = p
    return best.z if best is not None and abs(best.y - y) < 0.006 else None


def dorsal_band(B, blocks, w=0.050):
    """final85 M1: one continuous dark dorsal band (a studded closed Tube lofted along y) lying on the union of the
    torso block tops: nape scruff -> chest -> waist -> hips -> tail root. Two tubes (Chest / Spine) overlap at y 0.02."""
    def zt(y):
        zs = [z for z in (top_z(b, y) for b in blocks) if z is not None]
        return max(zs) if zs else None
    for bone, y0, y1 in (("Chest", -0.40, 0.032), ("Spine", 0.016, 0.445)):
        rings, n = [], int(round((y1 - y0) / 0.008))
        for i in range(n + 1):
            y = y0 + (y1 - y0) * i / n
            z = zt(y)
            if z is None:
                continue
            ww = w * (0.80 + 0.20 * max(0.0, min(1.0, (y + 0.40) / 0.12, (0.445 - y) / 0.10)))   # tapered ends
            top, bot = z + 0.005, z - 0.030
            rings.append([Vector((-ww, y, bot)), Vector((ww, y, bot)), Vector((ww, y, top)),
                          Vector((0.6 * ww, y, top + 0.002)), Vector((-0.6 * ww, y, top + 0.002)),
                          Vector((-ww, y, top))])
        B.tube(rings, BACK_SHADE, bone)


'''
s = s.replace(old, new)
open(p, "w", encoding="utf-8").write(s)
print("ok")
