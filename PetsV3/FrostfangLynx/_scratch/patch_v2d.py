p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\FrostfangLynx.py"
s = open(p, encoding="utf-8").read()


def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (a[:70], s.count(a))
    s = s.replace(a, b)


# saddle: thicker, wider, rounder (a dark fur cape, not plates) + a dark nape scruff that carries it up the neck
rep('''        B.seg(a, b, 0.088, 0.016, BACK_SHADE, bone, side=(1, 0, 0), ext=0.03, ext1=0.03, top=(0.94, 1), rnd=0.4)''',
    '''        B.seg(a, b, 0.100, 0.022, BACK_SHADE, bone, side=(1, 0, 0), ext=0.04, ext1=0.04, top=(0.86, 1), rnd=0.45)''')
rep('''    B.seg((0, -0.33, 0.66), (0, -0.53, 0.845), 0.096, 0.106, WARM_SILVER, "Neck", ext=0.05)''',
    '''    neck = B.seg((0, -0.33, 0.66), (0, -0.53, 0.845), 0.096, 0.106, WARM_SILVER, "Neck", ext=0.05)
    B.seg((0, -0.27, 0.770), (0, -0.50, 0.880), 0.090, 0.040, BACK_SHADE, "Neck", side=(1, 0, 0), ext=0.02,
          top=(0.80, 1), rnd=0.45)                                                          # dark nape scruff''')
# ICE frost cap on each ear tip + bolder pencils
rep('''        tip = root + R @ Vector((0, 0, 0.100))
        for dx, L in ((-0.25, 0.066), (0.15, 0.054)):                       # the tuft: two thin ice pencils
            B.spike(tip - R @ Vector((0, 0, 0.014)), R @ Vector((s * dx * 0.5, 0.10, 1)), L, 0.0085, ICE,
                    "Ear_" + side, top=(0.15, 0.35))''',
    '''        B.add(root + R @ Vector((0, 0, 0.094)), (0.018, 0.0165, 0.020), ICE, "Ear_" + side, R=R, top=(0.35, 0.7),
              studs=[], role="detail", bevel=0.004)                                         # frosted ear tip
        tip = root + R @ Vector((0, 0, 0.100))
        for dx, L in ((-0.25, 0.070), (0.15, 0.058)):                       # the tuft: two ice pencils
            B.spike(tip - R @ Vector((0, 0, 0.010)), R @ Vector((s * dx * 0.5, 0.10, 1)), L, 0.0115, ICE,
                    "Ear_" + side, top=(0.15, 0.35))''')
# neck spots + bigger leg spots
rep('''                (rosette if ros else blob)(B, hips, s, ly, lz, r, sd + 201 + 7 * i, ang=a)
        for s, fb, up, lo in LEGBLK:''', '''                (rosette if ros else blob)(B, hips, s, ly, lz, r, sd + 201 + 7 * i, ang=a)
            for i, (ly, lz, r, a) in enumerate(((0.035, -0.040, 0.034, 20), (-0.030, 0.055, 0.030, 70),
                                                (0.050, 0.070, 0.024, 40))):
                blob(B, neck, s, ly, lz, r, sd + 301 + 7 * i, el=1.2, ang=a)
        for s, fb, up, lo in LEGBLK:''')
rep('''                blob(B, up, s, 0.010, -0.040, 0.034, sd, el=1.1, ang=70)
                blob(B, up, s, -0.020, 0.060, 0.028, sd + 3, el=1.2, ang=20)''',
    '''                blob(B, up, s, 0.010, -0.040, 0.040, sd, el=1.1, ang=70)
                blob(B, up, s, -0.020, 0.065, 0.034, sd + 3, el=1.2, ang=20)''')
rep('''                rosette(B, up, s, 0.000, -0.050, 0.048, sd, ang=20)
                blob(B, up, s, 0.020, 0.065, 0.032, sd + 3, el=1.2, ang=60)''',
    '''                rosette(B, up, s, 0.000, -0.050, 0.056, sd, ang=20)
                blob(B, up, s, 0.020, 0.070, 0.036, sd + 3, el=1.2, ang=60)''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
