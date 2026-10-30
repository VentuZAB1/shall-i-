p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
t = open(p, encoding="utf-8").read()
a = """    B.add(c, (0.060 * sc, 0.008, 0.032 * sc), JOINT_D, bone, bevel=0.005, **kw)                    # socket
    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.003)), (0.045 * sc, 0.006, 0.0085 * sc), ICE_W, bone, bevel=0.003,
          **kw)                                                                                  # ice slit
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.008 * sc, 0, -0.003)), (0.005 * sc, 0.004, 0.0105 * sc), BLACK, bone,
          bevel=0.002, **kw)                                                                     # slit pupil"""
b = """    B.add(c, (0.060 * sc, 0.008, 0.030 * sc), JOINT_D, bone, bevel=0.005, top=(0.78, 1.0), **kw)   # socket
    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.004)), (0.047 * sc, 0.006, 0.0105 * sc), ICE_W, bone,
          bevel=0.003, top=(0.55, 1.0), **kw)                                                    # ice slit (wedge)
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.004 * sc, 0, -0.004)), (0.0036 * sc, 0.004, 0.0108 * sc), BLACK,
          bone, bevel=0.0015, **kw)                                                              # reptile pupil"""
assert a in t
t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
