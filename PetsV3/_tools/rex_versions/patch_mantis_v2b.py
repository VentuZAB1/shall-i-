# Thornblade Mantis v2b: lathed ruby dome eyes (Tube ellipsoids), arcing antennae, small mint mouth plate.
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\ThornbladeMantis.py"
s = open(p, encoding="utf-8").read()
R = []
R.append(('''def disc(B, c, r, color, bone, sx=0.75, sy=1.15, thick=0.012, dz=0.0):''',
'''def ellipsoid(B, c, ax, color, bone, R=None, n=18, rings=10):
    """lathed ellipsoid (a smooth dome, no studs): semi-axes ax=(x, y, z) in the local frame R, centre c"""
    from mathutils import Matrix
    R = R if R is not None else Matrix.Identity(3)
    out = []
    for i in range(rings + 1):
        th = math.pi * (0.03 + 0.94 * i / rings)
        z, r = math.cos(th), math.sin(th)
        out.append([Vector(c) + R @ Vector((ax[0] * r * math.cos(2 * math.pi * j / n),
                                            ax[1] * r * math.sin(2 * math.pi * j / n), ax[2] * z))
                    for j in range(n)])
    return B.tube(out, color, bone, nostud=True)


def on_surf(c, ax, R, u, t=1.0):
    """the point of the ellipsoid (c, ax, R) in direction u (scaled by t: < 1 sinks it in)"""
    u = Vector(u).normalized()
    return Vector(c) + R @ Vector((ax[0] * u.x, ax[1] * u.y, ax[2] * u.z)) * t


def disc(B, c, r, color, bone, sx=0.75, sy=1.15, thick=0.012, dz=0.0):'''))
R.append(('''        e = HC + Vector((s * 0.165, -0.02, 0.075))                                             # FIX 2: ruby domes
        rot = (0, s * 12, s * 18)
        B.add(e, (0.072, 0.07, 0.088), RUBY_D, "Head", rot=rot, rnd=0.5, studs=[], nostud=True, bot=(0.70, 0.75),
              top=(0.60, 0.70))
        body = B.add(e + Vector((s * 0.006, -0.012, 0.014)), (0.064, 0.062, 0.078), RUBY, "Head", rot=rot, rnd=0.5,
                     studs=[], nostud=True, bot=(0.65, 0.7), top=(0.55, 0.65), role="detail")
        B.add(e + Vector((s * 0.028, -0.04, 0.06)), (0.024, 0.022, 0.016), RUBY_HOT, "Head", rot=rot, rnd=0.5,
              studs=[], nostud=True, role="detail")                                              # hot cap
        hp, hn = surf_hit(B, [body], e + Vector((-s * 0.022, -0.5, -0.004)), (0, 1, 0))
        import blockkit as bk
        Rp = bk.frame_from(hp, hp + Vector((0, 0, 1)), hn)
        B.add(hp + hn * 0.004, (0.006, 0.013, 0.028), BLACK, "Head", R=Rp, studs=[], role="detail",
              bevel=0.003)                                                                     # pseudo-pupil slit''',
'''        from mathutils import Euler
        e = HC + Vector((s * 0.165, -0.02, 0.075))                                             # FIX 2: ruby DOMES
        Re = Euler((0, math.radians(s * 12), math.radians(s * 18)), "XYZ").to_matrix()          # (lathed ovals)
        ellipsoid(B, e, (0.072, 0.07, 0.088), RUBY_D, "Head", Re)                                # deep rim
        eb, axb = e + Vector((s * 0.007, -0.010, 0.006)), (0.068, 0.066, 0.084)
        ellipsoid(B, eb, axb, RUBY, "Head", Re)                                                  # ruby body
        ellipsoid(B, on_surf(eb, axb, Re, (s * 0.45, -0.5, 0.74), 0.93), (0.024, 0.022, 0.016), RUBY_HOT, "Head",
                  Re)                                                                            # hot glint
        ellipsoid(B, on_surf(eb, axb, Re, (-s * 0.15, -0.98, -0.05), 0.92), (0.010, 0.012, 0.030), BLACK, "Head",
                  Re)                                                                            # pseudo-pupil slit'''))
R.append(('''        a2 = a1 + Vector((s * 0.17, 0.24, 0.02))
        B.seg(a0, a1, 0.013, 0.013, ARMOR, "Antenna_" + side, ext=0.01, role="limb")
        B.seg(a1, a2, 0.010, 0.010, ARMOR, "Antenna_" + side, ext=0.005, role="limb")''',
'''        a2 = a1 + Vector((s * 0.10, 0.06, 0.10))                                               # arc up, out, back
        a3 = a2 + Vector((s * 0.13, 0.20, 0.03))
        B.seg(a0, a1, 0.013, 0.013, ARMOR, "Antenna_" + side, ext=0.01, role="limb")
        B.seg(a1, a2, 0.010, 0.010, ARMOR, "Antenna_" + side, ext=0.006, role="limb")
        B.seg(a2, a3, 0.008, 0.008, ARMOR, "Antenna_" + side, ext=0.005, role="limb")'''))
R.append(('''    B.add(HC + Vector((0, -0.083, -0.15)), (0.035, 0.008, 0.022), BELLY, "Head", studs=[], role="detail",''',
          '''    B.add(HC + Vector((0, -0.083, -0.15)), (0.03, 0.008, 0.016), BELLY_D, "Head", studs=[], role="detail",'''))
for a, b in R:
    assert a in s, "MISSING: " + a[:90]
    s = s.replace(a, b)
open(p, "w", encoding="utf-8").write(s)
print("patched", len(R))
