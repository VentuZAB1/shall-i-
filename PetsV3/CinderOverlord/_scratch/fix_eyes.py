D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets"
p = D + r"\CinderOverlord.py"
t = open(p, encoding="utf-8").read()
a = """        B.add(ep, (0.088, 0.010, 0.034), BLACK, "Head", bevel=0.005, **kw)                        # socket
        B.add(ep + en * 0.008, (0.075, 0.007, 0.0195), ROSE, "Head", bevel=0.004, **kw)           # rose slit
        B.add(ep + en * 0.013 + R @ Vector((-s * 0.014, 0, 0)), (0.008, 0.005, 0.018), BLACK, "Head",
              bevel=0.002, **kw)                                                                # slit pupil"""
b = """        B.add(ep, (0.088, 0.010, 0.032), BLACK, "Head", bevel=0.005, top=(0.78, 1.0), **kw)       # socket
        B.add(ep + en * 0.008 + R @ Vector((0, 0, -0.004)), (0.074, 0.007, 0.0165), ROSE, "Head", bevel=0.004,
              top=(0.55, 1.0), **kw)                                                            # rose slit (wedge)
        B.add(ep + en * 0.013 + R @ Vector((-s * 0.006, 0, -0.004)), (0.0055, 0.005, 0.0165), BLACK, "Head",
              bevel=0.002, **kw)                                                                # reptile pupil"""
assert a in t
t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)

p = D + r"\CoralCrusher.py"
t = open(p, encoding="utf-8").read()
a = """    B.add(c, (0.050 * sc, 0.008, 0.026 * sc), BLACK, bone, bevel=0.004, **kw)
    B.add(c + nn * 0.006, (0.041 * sc, 0.006, 0.0125 * sc), ROSE, bone, bevel=0.003, **kw)
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.006 * sc, 0, 0)), (0.0055 * sc, 0.004, 0.0125 * sc), BLACK, bone,
          bevel=0.002, **kw)"""
b = """    B.add(c, (0.050 * sc, 0.008, 0.026 * sc), BLACK, bone, bevel=0.004, top=(0.78, 1.0), **kw)
    B.add(c + nn * 0.006 + R @ Vector((0, 0, -0.003)), (0.042 * sc, 0.006, 0.0125 * sc), ROSE, bone, bevel=0.003,
          top=(0.55, 1.0), **kw)
    B.add(c + nn * 0.010 + R @ Vector((-s * 0.004 * sc, 0, -0.003)), (0.0042 * sc, 0.004, 0.0125 * sc), BLACK,
          bone, bevel=0.0015, **kw)"""
assert a in t
t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
