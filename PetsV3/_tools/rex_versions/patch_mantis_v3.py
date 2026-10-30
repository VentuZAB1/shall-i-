# Thornblade Mantis v3 = review 2 M1-M5 + S1-S5 (reviewer-tested code).
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThornbladeMantis.py"
s = open(p, encoding="utf-8").read()
R = []
# M2: ruby thorn
R.append(('''    B.spike(c - n * 0.01, n, size * 1.0, size * 0.55, RUBY_D, bone, top=(0.7, 0.7))
    B.spike(c + n * size * 0.25, n, size * 0.85, size * 0.42, RUBY, bone, top=(0.15, 0.15))
    B.spike(c + n * size * 0.75, n, size * 0.40, size * 0.18, RUBY_HOT, bone, top=(0.1, 0.1))''',
'''    B.spike(c - n * 0.01, n, size * 0.40, size * 0.34, RUBY_D, bone, top=(0.75, 0.75), nostud=True)  # (review 2 M2:
    B.spike(c + n * size * 0.22, n, size * 0.88, size * 0.30, RUBY, bone, top=(0.10, 0.10), nostud=True)  # a thorn,
    B.spike(c + n * size * 0.80, n, size * 0.36, size * 0.13, RUBY_HOT, bone, top=(0.08, 0.08), nostud=True)  # no die)


def gem_inlay(B, c, n, size, bone):
    """flush 45 deg diamond: deep frame -> ruby -> hot glint (review 2 M4)"""
    n = Vector(n).normalized()
    x = Vector((0, 0, 1)).cross(n).normalized()
    z = n.cross(x).normalized()
    Rr = Matrix((x, n, z)).transposed() @ Matrix.Rotation(math.radians(45), 3, "Y")
    kw = dict(R=Rr, studs=[], nostud=True, role="detail")
    B.add(c, (size, 0.008, size), RUBY_D, bone, bevel=0.004, **kw)
    B.add(c + n * 0.006, (size * 0.72, 0.007, size * 0.72), RUBY, bone, bevel=0.003, **kw)
    B.add(c + n * 0.011 + (x + z) * size * 0.25, (size * 0.16, 0.004, size * 0.16), RUBY_HOT, bone, bevel=0.002, **kw)'''))
# S3
R.append(('''ANT0 = (0.03, -0.095, 0.105)''', '''ANT0 = (0.055, -0.095, 0.105)'''))
# S4 (+ the hindwing eye-spot anchor uses the same point)
R.append(('''        eye = leaf(s, 0.55, 0.45) - Vector((0, 0, 0.026))''', '''        eye = leaf(s, 0.55, 0.40) - Vector((0, 0, 0.026))'''))
# S2
R.append(('''            B.spike(base + dv * L * 0.6, dv, L * 0.55, 0.014, RUBY, "Chest", studs=[], nostud=True)''',
          '''            B.spike(base + dv * L * 0.5, dv, L * 0.6, 0.02, RUBY, "Chest", studs=[], nostud=True)'''))
# S1
R.append(('''    B.add(HC + Vector((0, -0.083, -0.15)), (0.03, 0.008, 0.016), BELLY_D, "Head", studs=[], role="detail",''',
          '''    B.add(HC + Vector((0, -0.083, -0.15)), (0.03, 0.008, 0.016), ARMOR, "Head", studs=[], role="detail",'''))
# M3
R.append(('''        ellipsoid(B, e, (0.072, 0.07, 0.090), RUBY_D, "Head", Re, n=24, rings=14)               # deep rim (back)
        eb, axb = e + Vector((s * 0.012, -0.018, 0.004)), (0.066, 0.064, 0.086)
        ellipsoid(B, eb, axb, RUBY, "Head", Re, n=24, rings=14)                                  # ruby body
        ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.12, -0.98, 0.0), 0.92), (0.009, 0.012, 0.032), BLACK, "Head",
                  Re)                                                                            # pseudo-pupil slit''',
'''        ellipsoid(B, e + Re @ Vector((-s * 0.004, 0.014, -0.012)), (0.066, 0.064, 0.084), RUBY_D, "Head", Re, n=24,
                  rings=14)                                                     # deep crescent tucked back + low
        eb, axb = e + Vector((s * 0.006, -0.008, 0.006)), (0.069, 0.067, 0.089)                   # ruby body (bigger)
        ellipsoid(B, eb, axb, RUBY, "Head", Re, n=24, rings=14)
        ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.5, -0.86, -0.16), 0.95), (0.009, 0.012, 0.032), BLACK, "Head", Re,
                  n=12, rings=6)                                                # pupil: inner-front, under the lid'''))
# M1 crown + M4 gems + S5 cone rings
R.append(('''    B.add(HC + Vector((0, 0, 0.12)), (0.09, 0.06, 0.032), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.01)
    B.spike(HC + Vector((0, 0, 0.14)), (0, 0.25, 1), 0.34, 0.065, GOLD, "Head", top=(0.12, 0.12))
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.055, 0, 0.14)), (s * 0.5, 0.2, 1), 0.18, 0.042, GOLD, "Head", top=(0.12, 0.12))
    B.spike(HC + Vector((0, 0.02, 0.19)), (0, 0.35, 1), 0.16, 0.03, GOLD_D, "Head", top=(0.3, 0.3))   # cone keel
    ruby_gem(B, HC + Vector((0, -0.062, 0.12)), (0, -1, 0.15), 0.06, "Head")
    B.add(HC + Vector((0, 0.062, 0.115)), (0.07, 0.012, 0.03), GOLD, "Head", role="limb", bevel=0.006)  # back plate
    ruby_gem(B, HC + Vector((0, 0.072, 0.115)), (0, 1, 0.15), 0.045, "Head")''',
'''    B.add(HC + Vector((0, 0, 0.12)), (0.09, 0.06, 0.032), GOLD, "Head", top=(0.85, 0.85), role="limb", bevel=0.01,
          nostud=True)
    cb, cd = HC + Vector((0, 0, 0.14)), Vector((0, 0.25, 1)).normalized()
    B.spike(cb, cd, 0.34, 0.065, GOLD, "Head", top=(0.12, 0.12), nostud=True)                  # polished gold spire
    for f in (0.35, 0.65):                                                                      # S5: ornament rings
        w = 0.065 * (1 - 0.88 * f) + 0.008
        B.add(cb + cd * 0.34 * f, (w, w, 0.012), GOLD_D, "Head", R=__import__("blockkit").frame_from(
              cb, cb + cd, Vector((1, 0, 0))), studs=[], nostud=True, role="detail", bevel=0.003)
    for s in (1, -1):
        B.spike(HC + Vector((s * 0.055, 0, 0.14)), (s * 0.5, 0.2, 1), 0.18, 0.042, GOLD, "Head", top=(0.12, 0.12),
                nostud=True)
    B.spike(HC + Vector((0, 0.02, 0.19)), (0, 0.35, 1), 0.16, 0.03, GOLD_D, "Head", top=(0.3, 0.3),
            nostud=True)                                                                         # cone keel
    gem_inlay(B, HC + Vector((0, -0.064, 0.12)), (0, -1, 0), 0.034, "Head")                    # M4 front jewel
    B.add(HC + Vector((0, 0.062, 0.115)), (0.07, 0.012, 0.03), GOLD, "Head", role="limb", bevel=0.006,
          nostud=True)                                                                           # back plate
    gem_inlay(B, HC + Vector((0, 0.076, 0.115)), (0, 1, 0), 0.026, "Head")                     # back jewel (game cam)'''))
# M1 arms
R.append(('''        B.spike(F1 + Vector((0, 0, 0.03)), (s * 0.7, 0.5, 0.5), 0.11, 0.032, GOLD, fore, top=(0.12, 0.12))  # spine''',
          '''        B.spike(F1 + Vector((0, 0, 0.03)), (s * 0.7, 0.5, 0.5), 0.11, 0.032, GOLD, fore, top=(0.12, 0.12),
                nostud=True)                                                                         # knee spine'''))
R.append(('''        B.seg(F1, T1, 0.032, 0.042, GOLD, blade, ext=0.02, top=(0.7, 0.6))                           # gold tibia''',
          '''        B.seg(F1, T1, 0.032, 0.042, GOLD, blade, ext=0.02, top=(0.7, 0.6), nostud=True)              # gold tibia'''))
R.append(('''        B.spike(T1 - td * 0.01, hd_, 0.08, 0.028, GOLD, blade, top=(0.3, 0.3))                       # hook''',
          '''        B.spike(T1 - td * 0.01, hd_, 0.08, 0.028, GOLD, blade, top=(0.3, 0.3), nostud=True)          # hook'''))
# M5 anchors
R.append(('''    k.joint("Strike", tuple(HC + Vector((0, -0.45, -0.25))), "Chest", tail=(0, -0.2, 0))   # strike VFX anchor''',
'''    k.joint("Strike", tuple(HC + Vector((0, -0.45, -0.25))), "Chest", tail=(0, -0.2, 0))   # strike VFX anchor (moved
    k.joint("Crown", (0, -0.437, 1.61), "Head", tail=(0, 0.02, 0.08))                      # after keying, review 2)'''))
R.append(('''        k.joint("Wing_" + side, tuple(X(WROOT, s) - Vector((0, 0, 0.02))), "Spine", tail=(0, 0.5, 0.02))''',
'''        k.joint("Wing_" + side, tuple(X(WROOT, s) - Vector((0, 0, 0.02))), "Spine", tail=(0, 0.5, 0.02))
        k.joint("EyeSpot_" + side, tuple(leaf(s, 0.55, 0.40) - Vector((0, 0, 0.026))), "Wing_" + side,
                tail=(0, 0, -0.06))                                                      # hindwing eye-spot VFX
        F1v, T1v = Vector(F1), Vector(T1)
        td = (T1v - F1v).normalized()
        te = (Vector((0, -1, 0)) - td * Vector((0, -1, 0)).dot(td)).normalized()
        hd_ = (td * 0.3 - te * 0.95).normalized()
        tip = T1v - td * 0.01 + hd_ * 0.075 + (hd_ + td * 0.3).normalized() * 0.05
        k.joint("BladeTip_" + side, tuple(tip), "Blade_" + side, tail=tuple(hd_ * 0.05))   # claw tip VFX'''))
R.append(('''    P += [("Fore_L", "Fore_R"), ("Blade_L", "Blade_R"), ("Fore_L", "Blade_R"), ("Fore_R", "Blade_L"),
          ("Elytra_L", "Elytra_R"), ("Wing_L", "Wing_R")]''',
'''    P += [("Fore_L", "Fore_R"), ("Blade_L", "Blade_R"), ("Fore_L", "Blade_R"), ("Fore_R", "Blade_L"),
          ("Elytra_L", "Elytra_R"), ("Wing_L", "Wing_R"), ("Head", "Chest"), ("Elytra_L", "Wing_R"),
          ("Elytra_R", "Wing_L")]
    for s in ("L", "R"):                                                               # review 2 M5
        P += [("Elytra_" + s, "Chest"), ("Wing_" + s, "Chest"), ("Fore_" + s, "Chest"), ("Fore_" + s, "Leg_F" + s),
              ("Blade_" + s, "Leg_F" + s), ("Antenna_" + s, "Blade_" + s), ("Antenna_" + s, "Fore_" + s)]'''))
for a, b in R:
    assert s.count(a) == 1, "MISSING/DUP: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
