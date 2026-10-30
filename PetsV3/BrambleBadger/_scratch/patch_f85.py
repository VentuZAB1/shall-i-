p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\BrambleBadger.py"
s = open(p, encoding="utf-8").read()
rep = [
 # T2: a bigger crest (lead ruling: past the plan's 8-10 % of HEIGHT is OK)
 ('''THORNS = [(-0.47, 0.515, 0.052, 30), (-0.37, 0.535, 0.056, 34), (-0.26, 0.545, 0.058, 38), (-0.15, 0.548, 0.058, 42),
          (-0.04, 0.546, 0.058, 46), (0.07, 0.542, 0.056, 50), (0.18, 0.534, 0.052, 54), (0.29, 0.522, 0.048, 58),
          (0.39, 0.505, 0.042, 62)]''',
  '''THORNS = [(-0.47, 0.515, 0.064, 30), (-0.37, 0.535, 0.072, 34), (-0.26, 0.545, 0.072, 38), (-0.15, 0.548, 0.072, 42),
          (-0.04, 0.546, 0.072, 46), (0.07, 0.542, 0.072, 50), (0.18, 0.534, 0.064, 54), (0.29, 0.522, 0.048, 58),
          (0.39, 0.505, 0.042, 62)]                      # final85 T2: middle five 0.072, the two flanking 0.064'''),
 ('''        B.spike((0, y - 0.004, z + 0.002), d, L, 0.056, AMBER, tb, top=(0.10, 0.34))''',
  '''        B.spike((0, y - 0.004, z + 0.002), d, L, 0.064, AMBER, tb, top=(0.10, 0.34))     # final85 T2: width 0.064'''),
 # M3: the rear block runs level with the back (one line), rounder
 ('''    B.add((0, 0.27, 0.415), (0.212, 0.19, 0.115), GREY, "Spine", top=(0.78, 0.70), rnd=0.42)''',
  '''    B.add((0, 0.27, 0.415), (0.212, 0.19, 0.115), GREY, "Spine", top=(0.95, 0.95), rnd=0.50)   # final85 M3'''),
 # T1: a GREY_D flank band between the grey back and the dark skirt (a second value on the flank)
 ('''    B.add((0, 0.27, 0.28), (0.212, 0.19, 0.02), BELLY_D, "Spine", bot=(0.72, 0.62), rnd=0.36)''',
  '''    B.add((0, 0.27, 0.28), (0.212, 0.19, 0.02), BELLY_D, "Spine", bot=(0.72, 0.62), rnd=0.36)
    for s in (1, -1):                                   # final85 T1: GREY_D flank band, z 0.315-0.350, y -0.26..0.27
        for y0, y1, x0, x1 in ((-0.26, 0.17, 0.222, 0.211), (0.17, 0.27, 0.211, 0.2105)):
            B.seg((s * (x0 - 0.003), y0, 0.3325), (s * (x1 - 0.003), y1, 0.3325), 0.006, 0.0175, GREY_D, "Spine",
                  side=(1, 0, 0), ext=0.0 if y0 < 0 else 0.004, studs=[], nostud=True, rnd=0.45)'''),
 # M1: the hind thigh - no pointed fin above the skirt
 ('''                B.seg(H + Vector((0, 0.02, -0.012)), K, 0.072, 0.088, BELLY_D, leg, bot=(0.9, 1), top=(0.80, 0.74),
                      ext=0.0, ext1=0.03)''',
  '''                B.seg(H + Vector((0, 0.02, -0.012)), K, 0.072, 0.088, BELLY_D, leg, bot=(0.9, 1), top=(0.95, 0.95),
                      ext=0.0, ext1=0.03, rnd=0.45)                                      # final85 M1: no fin'''),
 # M2: the haunch sits flush with the rear block (no proud box)
 ('''                B.add(H + Vector((s * 0.022, 0.025, -0.035)), (0.068, 0.110, 0.075), GREY, "Spine", bot=(0.72, 0.75),
                      rnd=0.45)                     # grey body fur over the haunch (on Spine: review 2 N-3)''',
  '''                B.add(H + Vector((0, 0.025, -0.035)), (0.050, 0.110, 0.075), GREY, "Spine", bot=(0.72, 0.75),
                      rnd=0.45)                     # haunch fur, flush with the rear block (final85 M2)'''),
 # C1: idle breathing visible, also during the sniff
 ('''        b = pk.wave(f, n, 0, 3) * (1 - d)                                 # slow breathing when up
        k.key("Spine", f, rot=(4.0 * d, 0, 0), loc=(0, 0, -0.010 * d + 0.002 * b))
        k.key("Chest", f, rot=(1.0 * d, 0, 0))''',
  '''        b = pk.wave(f, n, 0, 3)                                           # final85 C1: breathing all loop long
        k.key("Spine", f, rot=(4.0 * d, 0, 0), loc=(0, 0, -0.010 * d + 0.010 * b))
        k.key("Chest", f, rot=(1.0 * d + 1.2 * b, 0, 0))'''),
 # C2: ear + tail flicks at f40-46 and f96-102
 ('''        ears(k, f, -4.0 * d + 3.0 * lf)
        thorns(k, f, 3.0 * br)
        k.key("Tail1", f, rot=(4.0 * d, 6.0 * pk.wave(f, n, 0.0, 2), 0))   # 0 at f0: idle f0 = the acts' rest''',
  '''        fk = tab(FLICK, f)
        ears(k, f, -4.0 * d + 3.0 * lf + 10.0 * fk)                       # final85 C2: ear flick
        thorns(k, f, 3.0 * br)
        k.key("Tail1", f, rot=(4.0 * d + 14.0 * fk, 6.0 * pk.wave(f, n, 0.0, 2), 0))   # + a 14 deg tail flick'''),
 ('''    BRIS = [(0, 0.0), (64, 0.0), (70, 1.0), (78, 1.0), (88, 0.0), (120, 0.0)]
    for f in range(0, n + 1, 2):''',
  '''    BRIS = [(0, 0.0), (64, 0.0), (70, 1.0), (78, 1.0), (88, 0.0), (120, 0.0)]
    FLICK = [(0, 0.0), (40, 0.0), (43, 1.0), (46, 0.0), (96, 0.0), (99, 1.0), (102, 0.0), (120, 0.0)]
    for f in range(0, n + 1):'''),
 # C3: walk weight
 ('''        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 2.0 * pk.wave(f, n), 3.0 * pk.wave(f, n)),
              loc=(0, 0, -0.010 * bob))''',
  '''        k.key("Spine", f, rot=(0.8 * pk.wave(f, n, 0.1, 2), 2.0 * pk.wave(f, n), 4.0 * pk.wave(f, n)),
              loc=(0, 0, -0.020 * bob))                                  # final85 C3: bob 0.020, roll 4 deg'''),
 # T3: a stronger growl tremble
 ('''        tr = 1.5 * math.sin(2 * math.pi * f / 4) if 24 <= f <= 42 else 0.0''',
  '''        tr = 2.5 * math.sin(2 * math.pi * f / 4) if 24 <= f <= 42 else 0.0          # final85 T3: 2.5 deg'''),
 # T4: wider dig scoops
 ('''    SC = [(0, (0.0, 0.0)), (3, (-0.040, 0.026)), (5, (-0.048, 0.0)), (8, (0.032, 0.0)), (10, (0.0, 0.0))]''',
  '''    SC = [(0, (0.0, 0.0)), (3, (-0.056, 0.026)), (5, (-0.064, 0.0)), (8, (0.032, 0.0)), (10, (0.0, 0.0))]  # T4'''),
]
for a, b in rep:
    assert a in s, a[:70]
    s = s.replace(a, b)
if "GREY_D" not in s.split("def model")[0]:
    a = "BELLY_D = "
    i = s.index(a)
    j = s.index("\n", i)
    s = s[:j + 1] + "GREY_D = (150, 146, 156)       # final85 T1: flank band between the grey back and the dark skirt\n" + s[j + 1:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
