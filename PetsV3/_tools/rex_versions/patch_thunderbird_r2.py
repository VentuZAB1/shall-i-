# one-shot patch: Thunderbird review-2 fixes 1-7 + 9 (+ new check pairs). Run with plain python.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\Thunderbird.py"
s = open(p, encoding="utf-8").read()
R = []
# 9 - bake constants (no environment reads)
R.append(('''TAIL_SPREAD = float(os.environ.get("TB_TS", "38"))   # rest fan half-angle (deg)''',
          '''TAIL_SPREAD = 38.0                                   # rest fan half-angle (deg)'''))
R.append(('''WDX = float(os.environ.get("TB_DX", "0.15"))     # wing x offset vs v1 (review: +0.07; fold tests may override)''',
          '''WDX = 0.07                                       # wing x offset vs v1 (review 2: no shoulder blocks, +0.07)'''))
# 1 - delete the flight-muscle shoulder blocks (the Wing-vs-Chest blocker)
R.append(('''    for s in (1, -1):
        B.add((s * 0.20, -0.10, 1.12), (0.10, 0.12, 0.11), TEAL, "Chest", rot=(46, 0, 0), top=(0.8, 0.85),
              rnd=0.40)                                                                         # flight muscles
''', ''))
R.append(('''FOLD = (86.0, 4.0, -95.0, -15.0)''', '''FOLD = (86.0, 10.0, -80.0, 0.0)          # review 2: 0 hits, half-width 0.549 / 0.461 (90 %)'''))
# 2 - STORM dorsal saddle under the mantle; 5 - top mantle row seated 0.02 lower, outer two dropped
R.append(('''    face_shingles(B, chest, 1, [(0.20, (-0.12, 0.0, 0.12)), (0.06, (-0.18, -0.06, 0.06, 0.18)),
                                (-0.08, (-0.12, 0.0, 0.12))], lambda r, x: STORM, "Chest", size=(0.065, 0.022, 0.09))''',
'''    face_shingles(B, chest, 1, [(0.18, (0.0,)), (0.06, (-0.18, -0.06, 0.06, 0.18)),
                                (-0.08, (-0.12, 0.0, 0.12))], lambda r, x: STORM, "Chest", size=(0.065, 0.022, 0.09))'''))
R.append(('''    face_shingles(B, low, 1, [(0.08, (-0.10, 0.0, 0.10)), (-0.06, (-0.05, 0.05))], lambda r, x: STORM, "Spine",
                  size=(0.06, 0.02, 0.08))''',
'''    face_shingles(B, low, 1, [(0.08, (-0.10, 0.0, 0.10)), (-0.06, (-0.05, 0.05))], lambda r, x: STORM, "Spine",
                  size=(0.06, 0.02, 0.08))
    B.add(chest.world(Vector((0, 0.09, 0.0))), (0.25, 0.17, 0.25), STORM, "Chest", R=chest.R, bot=(0.62, 0.56),
          top=(0.92, 0.92), rnd=0.40)                      # dorsal saddle: chest back
    B.add(low.world(Vector((0, 0.07, 0.0))), (0.185, 0.14, 0.16), STORM, "Spine", R=low.R, bot=(0.72, 0.66),
          top=(0.92, 0.9), rnd=0.38)                       # dorsal saddle: lower back'''))
# 3 - arm bar: teal shoulder patch, storm to the wrist; storm knuckle
R.append(('''    B.seg(S0, W, 0.06, 0.09, TEAL, wb, side=nrm, ext=0.05, role="limb", top=(0.8, 0.75))
    B.add(W, (0.05, 0.065, 0.065), TEAL, wb, R=frame(W - S, nrm), role="limb")''',
'''    Wm = S0.lerp(W, 0.38)
    B.seg(S0, Wm, 0.06, 0.09, TEAL, wb, side=nrm, ext=0.05, role="limb", top=(0.95, 0.95))
    B.seg(Wm, W, 0.057, 0.085, STORM, wb, side=nrm, ext=0.01, role="limb", top=(0.85, 0.8))
    B.add(W, (0.05, 0.065, 0.065), STORM, wb, R=frame(W - S, nrm), role="limb")'''))
# 4 - face: lid-heavy socket, no pupil; brow back 0.014; shorter forward hook; low narrow crest
R.append(('''    B.add(c, (0.05 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[], role="detail", bevel=0.004)
    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.042 * sc, 0.006, 0.014 * sc), BOLT, bone, R=R, studs=[],''',
'''    B.add(c + R @ Vector((s * 0.003, 0, 0.007 * sc)), (0.053 * sc, 0.008, 0.026 * sc), BLACK, bone, R=R, studs=[],
          role="detail", bevel=0.004)                                   # lid-heavy socket
    B.add(c + R @ Vector((0.002 * s, -0.006, -0.002)), (0.042 * sc, 0.006, 0.014 * sc), BOLT, bone, R=R, studs=[],'''))
R.append(('''    B.add(c + R @ Vector((-s * 0.004 * sc, -0.011, 0.0)), (0.005 * sc, 0.004, 0.013 * sc), BLACK, bone, R=R,
          studs=[], role="detail", bevel=0.002)
''', ''))
R.append(('''        B.add(HC + Vector((s * 0.086, -0.118, 0.076)), (0.092, 0.05, 0.034), WHITE_D, "Head",''',
          '''        B.add(HC + Vector((s * 0.086, -0.104, 0.076)), (0.092, 0.05, 0.034), WHITE_D, "Head",'''))
R.append(('''    B.spike(HC + Vector((0, -0.36, -0.046)), (0, -0.25, -1), 0.13, 0.038, GOLD_D, "Head", top=(0.15, 0.2))  # hook''',
          '''    B.spike(HC + Vector((0, -0.365, -0.05)), (0, -0.55, -1), 0.09, 0.038, GOLD_D, "Head", top=(0.15, 0.2))  # hook'''))
R.append(('''    for x, L, up, row in ((-0.075, 0.42, 30, 0), (-0.025, 0.46, 36, 0), (0.025, 0.40, 33, 0), (0.075, 0.44, 27, 0),
                          (-0.05, 0.24, 42, 1), (0.0, 0.26, 46, 1), (0.05, 0.22, 40, 1)):''',
'''    for x, L, up, row in ((-0.075, 0.42, 16, 0), (-0.025, 0.46, 22, 0), (0.025, 0.40, 19, 0), (0.075, 0.44, 14, 0),
                          (-0.05, 0.24, 26, 1), (0.0, 0.26, 30, 1), (0.05, 0.22, 24, 1)):'''))
R.append(('''        d = Vector((x * 6.5 * (1 if row == 0 else 0.6), math.cos(ang), math.sin(ang))).normalized()''',
          '''        d = Vector((x * 3.0 * (1 if row == 0 else 0.6), math.cos(ang), math.sin(ang))).normalized()'''))
# 6 - trousers: narrower, rounder, 7-spike ragged cuff (STORM / PRIMARY)
R.append(('''        B.seg(K, A + Vector((0, 0, 0.04)), 0.08, 0.085, STORM, "Shin_" + side, ext=0.05, top=(1.25, 1.2), rnd=0.4)
        for i, dx in enumerate((-0.07, -0.035, 0.0, 0.035, 0.07)):                                # trouser fringe
            L = 0.10 + 0.03 * (i % 2)
            B.spike(A + Vector((s * dx, -0.02 + 0.015 * abs(dx) / 0.07, 0.11)), (s * dx * 0.6, -0.15, -1), L, 0.045,
                    STORM, "Shin_" + side, top=(0.2, 0.4))''',
'''        B.seg(K, A + Vector((0, 0, 0.04)), 0.07, 0.075, STORM, "Shin_" + side, ext=0.05, top=(1.21, 1.2), rnd=0.45)
        for i in range(7):                                                                    # ragged trouser cuff
            ang = 2 * math.pi * i / 7 + 0.3
            rv = Vector((math.cos(ang) * 0.075, math.sin(ang) * 0.08, 0))
            L = 0.12 + 0.03 * ((i * 3) % 4) / 3.0
            B.spike(A + rv + Vector((0, 0, 0.11)), (rv.x * 6, rv.y * 6 - 0.15, -1), L, 0.04,
                    STORM if i % 2 == 0 else PRIMARY, "Shin_" + side, top=(0.2, 0.4))'''))
# 7 - cup the tail fan
R.append(('''        d = Vector((math.sin(ang), math.cos(ang), -0.30 * math.cos(ang))).normalized()''',
          '''        d = Vector((math.sin(ang), math.cos(ang), -0.30 * math.cos(ang) + 0.10 * abs(a))).normalized()'''))
# clip-plan check pairs: crest vs cape, trousers vs flank skirt
R.append(('''    P += [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest")]''',
          '''    P += [("Leg_L", "Leg_R"), ("Shin_L", "Shin_R"), ("Foot_L", "Foot_R"), ("Head", "Chest"), ("Jaw", "Chest"),
          ("Head", "Neck"), ("Shin_L", "Spine"), ("Shin_R", "Spine")]'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
