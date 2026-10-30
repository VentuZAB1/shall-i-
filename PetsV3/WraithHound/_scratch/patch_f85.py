import sys
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\WraithHound.py"
SIDE_SOOT = "--side-soot" in sys.argv          # T1: Mane1 / Mane3 side tips soot (only if the game accent stays >= 5 %)
s = open(p, encoding="utf-8").read()
rep = [
 # M1: mid-slate mane roots + middles (smoke rising from a lavender back), soot stays on the outer-low wisps
 ('''def wisp(B, root, d0, d1, L0, L1, w, d, bone, side=(1, 0, 0), tipfrac=0.42, tipcol=INDIGO):''',
  '''def wisp(B, root, d0, d1, L0, L1, w, d, bone, side=(1, 0, 0), tipfrac=0.42, tipcol=INDIGO, body=None):'''),
 ('''    B.seg(root, m, w, d, SOOT, bone, side=side, top=(0.70, 0.70), ext=0.04, ext1=0.0, rnd=0.42)
    B.seg(m, j, w * 0.70, d * 0.70, SOOT, bone, side=side, top=(0.62, 0.62), ext=0.035, ext1=0.0, rnd=0.42)''',
  '''    body = body or WISP_ROOT                           # final85 M1: mid-slate roots + middles (was SOOT)
    B.seg(root, m, w, d, body, bone, side=side, top=(0.70, 0.70), ext=0.04, ext1=0.0, rnd=0.42)
    B.seg(m, j, w * 0.70, d * 0.70, body, bone, side=side, top=(0.62, 0.62), ext=0.035, ext1=0.0, rnd=0.42)'''),
 # M2: one plume - only Mane2's centre keeps its indigo point, and it streams further back
 ('''    out = {"C": wisp(B, root, (0, 0.85, 0.55), (0, 1.0, 0.36), 0.21 * sc, 0.36 * sc, 0.070 * sc, 0.088 * sc, bone)}''',
  '''    out = {"C": wisp(B, root, (0, 0.85, 0.55), (0, 1.0, 0.36), 0.21 * sc, (0.44 if bone == "Mane2" else 0.36) * sc,
                     0.070 * sc, 0.088 * sc, bone, tipcol=(INDIGO if bone == "Mane2" else SOOT))}   # final85 M2'''),
 ('''             0.10 * sc, 0.15 * sc, 0.046 * sc, 0.060 * sc, bone + "_" + sd, tipcol=SOOT)   # outer-low wisp''',
  '''             0.10 * sc, 0.15 * sc, 0.046 * sc, 0.060 * sc, bone + "_" + sd, tipcol=SOOT, body=SOOT)   # outer-low'''),
 # T2: lavender chest front (no white bib), narrower
 ('''    B.add((0, -0.567, 0.66), (0.090, 0.046, 0.175), MIST, "Chest", bot=(0.40, 0.8), top=(0.95, 1), rot=(-14, 0, 0),''',
  '''    B.add((0, -0.567, 0.66), (0.075, 0.046, 0.175), ASH_LAV, "Chest", bot=(0.40, 0.8), top=(0.95, 1), rot=(-14, 0, 0),'''),
 # M3: taller eye slit + rim (the socket keeps its size)
 ('''        B.add(c + Vector((0, -0.005, 0)), (0.047, 0.006, 0.014), INDIGO_L, "Head", rot=rot, studs=[],''',
  '''        B.add(c + Vector((0, -0.005, 0)), (0.047, 0.006, 0.020), INDIGO_L, "Head", rot=rot, studs=[],'''),
 ('''        B.add(c + Vector((0, -0.008, 0)), (0.042, 0.006, 0.012), INDIGO, "Head", rot=rot, studs=[],''',
  '''        B.add(c + Vector((0, -0.008, 0)), (0.042, 0.006, 0.018), INDIGO, "Head", rot=rot, studs=[],'''),
 ('''        B.add(c + Vector((-s * 0.004, -0.0125, -0.001)), (0.0060, 0.004, 0.0130), BLACK, "Head",''',
  '''        B.add(c + Vector((-s * 0.004, -0.0125, -0.001)), (0.0060, 0.004, 0.0175), BLACK, "Head",'''),
 # M1: tail lavender to Tail3, soot tuft on Tail4 only
 ('''        B.seg(a, b, w, d, ASH_LAV if i < 2 else SOOT, "Tail%d" % (i + 1), ext=0.06, ext1=0.03, top=(tp, tp),''',
  '''        B.seg(a, b, w, d, ASH_LAV if i < 3 else SOOT, "Tail%d" % (i + 1), ext=0.06, ext1=0.03, top=(tp, tp),'''),
 # C1: no 4-frame flutter - a 3 Hz tremble
 ('''        tr = 2.0 * math.sin(2 * math.pi * f / 4) if 26 <= f <= 44 else 0.0''',
  '''        tr = 2.0 * math.sin(2 * math.pi * f / 10) if 26 <= f <= 44 else 0.0     # final85 C1: 3 Hz, not 7.5 Hz'''),
 # C2: roar side wisps 12 deg (no batwing horns)
 ('''             [25.0 * m for m in mf], [0.0, 0.0, 0.0])''',
  '''             [12.0 * m for m in mf], [0.0, 0.0, 0.0])                    # final85 C2: 12 deg (was 25)'''),
 # C3: the cloak fans sideways, not up
 ('''        mane(k, f, [14.0 * a for a in fan], [60.0 * a + 0.5 * d for a, d in zip(fan, dr)], dr)   # wide, low cloak''',
  '''        mane(k, f, [6.0 * a for a in fan], [60.0 * a + 0.5 * d for a, d in zip(fan, dr)], dr)   # C3: lift 6 (was 14)'''),
]
for a, b in rep:
    assert a in s, a[:70]
    s = s.replace(a, b)
a = '''INDIGO_L = '''
i = s.index(a)
j = s.index("\n", i)
s = s[:j + 1] + "WISP_ROOT = (128, 124, 166)   # final85 M1: mid-slate mane roots + middles (smoke over a lavender back)\n" + s[j + 1:]
if SIDE_SOOT:
    a = '''        out[sd] = wisp(B, r, (s_ * 0.40, 0.85, 0.60), (s_ * 0.20, 1.0, 0.42), 0.19 * sc, 0.28 * sc, 0.056 * sc,'''
    assert a in s
open(p, "w", encoding="utf-8").write(s)
print("ok")
