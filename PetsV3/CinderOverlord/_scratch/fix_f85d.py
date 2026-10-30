# f85 M5 v3: middle blades (2, 4) get a smaller rounded gold nib + slightly deeper frames; the outer blades (1, 5)
# stay plain (T4: they never outshine the centre)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("""def plate_crown(B, base, up_d, back_d, h, w, bone, gem=False, gw=0.025):""",
    """def plate_crown(B, base, up_d, back_d, h, w, bone, gem=False, gw=0.025, nib=0.0, fd=0.009):""")
rep("""        B.seg(p - dv * 0.012, q + dv * 0.012, gw, t * 0.5 + (0.015 if gem else 0.009), GOLD, bone, side=nrm.cross(dv),""",
    """        B.seg(p - dv * 0.012, q + dv * 0.012, gw, t * 0.5 + fd, GOLD, bone, side=nrm.cross(dv),""")
rep("""        # f85 M5: a rounded gold tip nib over the top of the centre blade (f72-100 % of h, above the blue V apex)
        B.add(base + up_d * h * 0.855, (w * 0.50, t * 0.5 + 0.008, h * 0.145), GOLD, bone,
              R=Matrix((side, nrm, up_d)).transposed(), top=(0.22, 0.75), rnd=0.45, studs=[], nostud=True,
              role="limb")""",
    """    if nib > 0:
        # f85 M5: a rounded gold tip nib over the top of the blade (above the blue V apex; its shading stays gold in
        # the kit portrait where flat gold faces clip to lemon)
        B.add(base + up_d * h * (1.0 - nib), (w * 0.50, t * 0.5 + 0.008, h * nib), GOLD, bone,
              R=Matrix((side, nrm, up_d)).transposed(), top=(0.22, 0.75), rnd=0.45, studs=[], nostud=True,
              role="limb")""")
rep("""        tip = plate_crown(B, base, up_d, back_d, h, w, bone, gem=(i == 2), gw=0.020 if i in (0, 4) else 0.038 if i == 2 else 0.028)""",
    """        tip = plate_crown(B, base, up_d, back_d, h, w, bone, gem=(i == 2), gw=0.020 if i in (0, 4) else 0.038 if i == 2 else 0.028,
                          nib=0.145 if i == 2 else 0.11 if i in (1, 3) else 0.0,                 # f85 M5
                          fd=0.015 if i == 2 else 0.012 if i in (1, 3) else 0.009)""")
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
