p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\FrostfangLynx.py"
s = open(p, encoding="utf-8").read()
rep = [
 # M5: idle life - a breathing rise (0.01H) + a slow +-8 deg tail sway, both 0 at f0 (loop closed)
 ('''        b = pk.wave(f, n, 0, 3)
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.003 * b))
        k.key("Chest", f, rot=(-0.6 * b, 0, 0))''',
  '''        b = pk.wave(f, n, 0, 3)
        rb = 0.5 - 0.5 * math.cos(2 * math.pi * 3 * f / n)            # final85 M5: breathing rise 0..0.01H
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0.01 * H_U * rb))
        k.key("Chest", f, rot=(-0.6 * b - 1.2 * rb, 0, 0))'''),
 ('''        bobtail(k, f, lift=-2.0 * b, flick=10.0 * tab(FL, f))
    cm.plant(k, n)
    k.finish()''',
  '''        bobtail(k, f, lift=-2.0 * b, flick=10.0 * tab(FL, f), sway=8.0 * math.sin(2 * math.pi * f / n))  # M5
    cm.plant(k, n)
    k.finish()'''),
 # M4 + T3: deeper crouch, stronger body pitch, an 18 deg locked stare with flattened tufts, a big claw open
 ('''    YW = [(0, 0.0), (4, 0.0), (16, 14.0), (40, 14.0), (48, 0.0), (96, 0.0)]     # stare at the camera side''',
  '''    YW = [(0, 0.0), (4, 0.0), (14, 18.0), (40, 18.0), (48, 0.0), (96, 0.0)]     # T3: an 18 deg locked stare'''),
 ('''    TF = [(0, 0.0), (4, 0.0), (14, -8.0), (22, -8.0), (34, 4.0), (72, 4.0), (86, 0.0), (96, 0.0)]  # tufts''',
  '''    TF = [(0, 0.0), (4, 0.0), (12, -12.0), (24, -12.0), (34, 4.0), (72, 4.0), (86, 0.0), (96, 0.0)]  # tufts (T3)'''),
 ('''    drop = 0.05 * H_U
    for f in range(0, n + 1):
        c, yw, lk, pr = tab(CR, f), tab(YW, f), tab(LK, f), tab(PR, f)''',
  '''    drop = 0.10 * H_U                                                     # final85 M4: 0.10H (was 0.05H)
    for f in range(0, n + 1):
        c, yw, lk, pr = tab(CR, f), tab(YW, f), tab(LK, f), tab(PR, f)'''),
 ('''        k.key("Spine", f, rot=(3.5 * c, 0, -1.5 * pr), loc=(0, 0, -drop * c))
        k.key("Chest", f, rot=(1.5 * c, 0, -1.5 * pr))
        k.key("Neck", f, rot=(-5.0 * c + 4.0 * lk, 0.35 * yw, 0))
        k.key("Head", f, rot=(-1.5 * c + 6.0 * lk, 0.65 * yw, -0.2 * yw))''',
  '''        k.key("Spine", f, rot=(6.0 * c, 0, -1.5 * pr), loc=(0, 0, -drop * c))
        k.key("Chest", f, rot=(3.0 * c, 0, -1.5 * pr))
        k.key("Neck", f, rot=(-5.0 * c + 4.0 * lk, 0.30 * yw, 0))          # neck total <= 7.4 deg (limit 8)
        k.key("Head", f, rot=(-4.0 * c + 6.0 * lk, 0.70 * yw, -0.2 * yw))  # the face stays level in the crouch'''),
 ('''        k.key("Claw_FL", f, rot=(-35.0 * tab(CL, f) + 4.0 * kn * tab(CL, f), 0, 0))
        k.key("Claw_FR", f, rot=(-35.0 * tab(CRt, f) - 4.0 * kn * tab(CRt, f), 0, 0))''',
  '''        k.key("Claw_FL", f, rot=(-55.0 * tab(CL, f) + 4.0 * kn * tab(CL, f), 0, 0))     # M4: -55 (was -35)
        k.key("Claw_FR", f, rot=(-55.0 * tab(CRt, f) - 4.0 * kn * tab(CRt, f), 0, 0))'''),
 ('''                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.008 * a)), toe=-12.0 * a)''',
  '''                k.solve_leg(leg, f, Vector((k.J[leg].x, k.J[leg].y, 0.008 * a)), toe=-20.0 * a)   # M4: -20'''),
 ('''    CR = [(0, 0.0), (10, 1.0), (72, 1.0), (88, 0.0), (96, 0.0)]                 # crouch 0.05H (L2: ~8-10 f)''',
  '''    CR = [(0, 0.0), (10, 1.0), (72, 1.0), (88, 0.0), (96, 0.0)]                 # crouch 0.10H (L2: ~8-10 f)'''),
]
for a, b in rep:
    assert a in s, a[:70]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("ok")
