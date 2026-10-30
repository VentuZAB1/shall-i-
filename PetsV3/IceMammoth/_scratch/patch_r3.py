# round-2 NICE fixes: tusk cap edge, two big head clumps, tighter eye socket
import re, io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\IceMammoth.py"
s = io.open(P, encoding="utf-8").read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)
rep('''MINT = (150, 236, 210)       # THE accent: tusk crack lines, eye slits
''', '''MINT = (150, 236, 210)       # THE accent: tusk crack lines, eye slits
ICE_MINT = (190, 240, 230)   # short transition ring between the white tusk and its mint cap
''')
old_clumps = '''    for x, y, z, dz, L in ((0.0, -1.10, 1.58, 0.2, 0.15), (0.09, -1.06, 1.57, 0.3, 0.13), (-0.09, -1.06, 1.57, 0.3, 0.13),
                           (0.0, -0.90, 1.62, 0.8, 0.14)):
        B.spike((x, y, z - 0.03), (x * 2.5, -0.9 + dz, 1.0), 0.08 + 0.03, 0.07, WOOL_D, "Head", top=(0.6, 0.6),
                studs=None, role="limb", rnd=0.45)                                      # rounded wool clump
'''
new_clumps = '''    for base, d, L in (((0, -1.08, 1.56), (0, -0.45, 1.0), 0.11), ((0, -0.92, 1.585), (0, 0.35, 1.0), 0.12)):
        B.spike(base, d, L, 0.098, WOOL_D, "Head", top=(0.62, 0.62), studs=None, role="limb", rnd=0.55)  # 2 big clumps
'''
rep(old_clumps, new_clumps)
rep('''B.add((s * 0.128, -1.186, 1.350), (0.082, 0.012, 0.030), DARK''', '''B.add((s * 0.128, -1.186, 1.350), (0.078, 0.012, 0.024), DARK''')
rep('''        i0 = int(0.60 * (len(C) - 1))                                       # mint ice cap on the tusk tip
''', '''        i0 = int(0.60 * (len(C) - 1))                                       # mint ice cap on the tusk tip
        im = int(0.52 * (len(C) - 1))                                       # pale ice-mint ring: soft cap edge
        B.tube(tube_rings(C[im:i0 + 1], [r + 0.002 for r in R[im:i0 + 1]], 10), ICE_MINT, "Head", nostud=True)
''')
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
