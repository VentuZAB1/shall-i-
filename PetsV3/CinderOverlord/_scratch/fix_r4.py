# Cinder Overlord final-8.5 round 4 (_review/CinderOverlord_final85_r4.md + coordinator)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
n_ok = 0


def rep(a, b):
    global s, n_ok
    c = s.count(a)
    assert c == 1, (c, a[:100])
    s = s.replace(a, b)
    n_ok += 1


# 1: the vent core is the same deep blue (the white cores read as ladder rungs)
rep("""    B.bar(p0 + ax * L * 0.16 + n * 0.004, p1 - ax * L * 0.22 + n * 0.004, n, w * 0.50, 0.004, LAVA, bone,""",
    """    B.bar(p0 + ax * L * 0.16 + n * 0.004, p1 - ax * L * 0.22 + n * 0.004, n, w * 0.50, 0.004, ROSE, bone,   # r4: was LAVA""")
rep('''    """rose lava vent slit (flush): rose body, LAVA hot core line; slanted back along the body"""''',
    '''    """deep-blue vent slit (flush), a raised blue core ridge (r4: the white-hot core read as ladder rungs); slanted"""''')
# 2: neck - Neck1 full ring, Neck2 a thin band (0.70-0.80), no Neck3 ring
rep("""        elif i in (3, 4):                                 # Neck2 + Neck3: narrow bands (0.62-0.80)
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.62, 0.80, up=(0, 1, 0))""",
    """        elif i == 3:                                      # r4: Neck2 a thin band (0.70-0.80); Neck3 has none
            ring_band(a, b, FRAD[i], FRAD[i + 1], fb[i], 0.70, 0.80, up=(0, 1, 0))""")
# T-a: eyes another 0.03 toward the nose
rep("""        ep, en = surf_hit(B, [skull], (s * 0.6, -0.83, 1.722), (-s, 0, 0))            # r3 T3: 0.03 toward the nose""",
    """        ep, en = surf_hit(B, [skull], (s * 0.6, -0.86, 1.722), (-s, 0, 0))            # r4 T-a: -0.86 (r3 -0.83, r2 -0.80)""")
# T-b: the snout front ~10 % flatter (the tip stations lower), the cover follows; the nostrils sit on it
rep("""           (0.62, 0.150, 0.112, -0.014), (0.82, 0.118, 0.084, -0.026), (0.96, 0.070, 0.048, -0.034),
           (1.0, 0.055, 0.040, -0.036))""",
    """           (0.62, 0.150, 0.112, -0.014), (0.82, 0.118, 0.084, -0.026), (0.96, 0.070, 0.043, -0.034),
           (1.0, 0.055, 0.036, -0.036))                                             # r4 T-b: tip 10 % flatter (0.048 / 0.040)""")
# T-c: outer molt blades 45 -> 50 (the reseat stays slower than the rise)
rep("""                keys = [(0, 0), (up_f, 0), (up_f + 10, 45), (44, 45), (54, 10), (84, 10), (back_f, 2), (108, 0), (110, 0)]""",
    """                keys = [(0, 0), (up_f, 0), (up_f + 10, 50), (44, 50), (54, 10), (84, 10), (back_f, 2), (108, 0), (110, 0)]  # r4: 45 -> 50""")
io.open(p, "w", encoding="utf-8").write(s)
print("patched", n_ok)
