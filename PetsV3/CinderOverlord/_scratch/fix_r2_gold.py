import io
P = "pets/CinderOverlord.py"
s = io.open(P, encoding="utf-8").read()
rep = [
('''PLUM_OBS = (150, 84, 110)   # body scales (studded); review 1 MUST 1: oxblood-mauve H ~336, 36 deg off the
                             # Cosmic Leviathan's H 300 magenta hide (r1 was 160,90,136)''',
 '''PLUM_OBS = (144, 80, 96)    # body scales (studded); review 1 MUST 1 moved it to (150,84,110) H 336; the portrait
                             # still read pink, so per the review's fallback it went deeper + redder: oxblood H 345,
                             # S 0.44, luma 101 (45 deg off the Cosmic Leviathan's H 300 magenta; r1 was 160,90,136)'''),
('''        B.seg(p - dv * 0.010, q + dv * 0.010, 0.016, t * 0.5 + 0.009, GOLD, bone, side=nrm.cross(dv),''',
 '''        B.seg(p - dv * 0.012, q + dv * 0.012, 0.025, t * 0.5 + 0.009, GOLD, bone, side=nrm.cross(dv),'''),
('''    inner = [base.lerp(pp, 0.80) + up_d * h * 0.05 for pp in pts]''',
 '''    inner = [base.lerp(pp, 0.66) + up_d * h * 0.05 for pp in pts]'''),
('''    for i, (x, h, w, roll, back) in enumerate(((-0.300, 0.15, 0.040, -24, 24), (-0.150, 0.19, 0.048, -12, 24),
                                               (0.0, 0.25, 0.060, 0, 24), (0.150, 0.19, 0.048, 12, 24),
                                               (0.300, 0.15, 0.040, 24, 24))):''',
 '''    for i, (x, h, w, roll, back) in enumerate(((-0.300, 0.17, 0.042, -24, 24), (-0.150, 0.215, 0.050, -12, 24),
                                               (0.0, 0.28, 0.062, 0, 24), (0.150, 0.215, 0.050, 12, 24),
                                               (0.300, 0.17, 0.042, 24, 24))):'''),
]
for a, b in rep:
    assert a in s, a[:70]
    s = s.replace(a, b)
io.open(P, "w", encoding="utf-8").write(s)
print("ok")
