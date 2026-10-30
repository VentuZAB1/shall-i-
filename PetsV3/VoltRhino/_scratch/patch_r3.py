# round-2 verdict fixes (MUST 1-4 + NICE): flush horn rings, sunk brow, one tapered elbow-fold wedge per leg (no
# shin gaiter), saddle rear edge f 0.22 -> 0.06, rump rear edge -> 0.06, sunk horn zig, a lime tip band on the horn
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\VoltRhino.py"
s = io.open(P, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)


rep('''          (-0.14, 0.40, "Spine", 0.34, 0.22, 0.020),        # saddle''',
    '''          (-0.14, 0.40, "Spine", 0.34, 0.06, 0.020),        # saddle (rear edge runs down the flank, review 2 M4)''')
rep('''          (0.36, 0.93, "Spine", -0.30, -0.02, 0.032)]       # rump plate''',
    '''          (0.36, 0.93, "Spine", -0.30, 0.06, 0.032)]        # rump plate (rear edge tapered, review 2 NICE)''')
rep('''        bc = p + up * 0.066 + n * 0.016 + d * 0.004''', '''        bc = p + up * 0.066 + n * 0.006 + d * 0.004                       # sunk 0.010 (review 2 M2)''')
rep('''    for t0, t1, g in ((0.05, 0.13, 0.014), (0.47, 0.51, 0.008), (0.66, 0.70, 0.008)):''',
    '''    for t0, t1, g in ((0.05, 0.13, 0.014), (0.47, 0.51, 0.003), (0.66, 0.70, 0.003)):   # rings flush (review 2 M1)''')
rep('''            Q.append((c + ax * s * (hw + 0.004) + dv * dz, ax * s, min(0.060, 1.15 * hd)))''',
    '''            Q.append((c + ax * s * (hw - 0.007) + dv * dz, ax * s, min(0.060, 1.15 * hd)))   # sunk (r2 NICE)''')
rep('''    B.spike((0, -1.22, 1.11), (0, -0.40, 1.0), 0.21, 0.050, HORN_IVORY, "Head", top=(0.12, 0.12), nostud=True)''',
    '''    i0, i1 = int(0.84 * (len(C) - 1)), int(math.ceil(0.90 * (len(C) - 1)))     # lime tip band (game camera)
    B.tube(horn_rings(C[i0:i1 + 1], A[i0:i1 + 1], D[i0:i1 + 1], [w + 0.004 for w in W[i0:i1 + 1]],
                      [h + 0.004 for h in H[i0:i1 + 1]]), VOLT, "Head", nostud=True)
    B.spike((0, -1.22, 1.11), (0, -0.40, 1.0), 0.21, 0.050, HORN_IVORY, "Head", top=(0.12, 0.12), nostud=True)''')
rep('''            dk = (A - K).normalized()                                                          # elbow / knee fold
            B.seg(K + dk * 0.02, K + dk * 0.09, (0.15 if fb == "F" else 0.137), (0.155 if fb == "F" else 0.142),
                  IRON_D, shin, rnd=0.40, role="limb")
            if fb == "F":                                                                       # shin gaiter
                B.seg(K + dk * 0.22, K + dk * 0.30, 0.134, 0.139, IRON_D, shin, rnd=0.40, role="limb")
''', '''            dk = (A - K).normalized()          # ONE elbow / knee fold: a tapered wedge on the outer face (r2 M3)
            ox = s * (0.138 if fb == "F" else 0.122)
            c0 = K + dk * 0.035 + Vector((ox, -0.125, 0.03))
            c1 = K + dk * 0.075 + Vector((ox, 0.125, -0.03))
            B.seg(c0, c1, 0.013, 0.032, IRON_D, shin, side=(1, 0, 0), top=(1.0, 0.15), studs=[], rnd=0.40,
                  role="limb", bevel=0.006)
''')
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
