# f85 M5 v2: the flat cap clips to lemon in the kit portrait (H 60, not counted) -> a ROUNDED gold nib above the blue
# V (its shading gradient stays inside the gold window) + deeper gold frames on the centre blade (counted side faces)
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("""        cf = 0.58                                                    # f85 M5: gold tip cap (top 42 % = ~0.06 H)
        hw = w * 0.95 * (1.0 - (cf - 0.55) / 0.45)
        B.poly([base - side * hw + up_d * h * cf, base + up_d * (h + 0.004), base + side * hw + up_d * h * cf],
               t + 0.010, GOLD_D, bone)                                # GOLD_D: lit, it stays gold (GOLD clips to lemon)""",
    """        # f85 M5: a rounded gold tip nib over the top of the centre blade (f72-100 % of h, above the blue V apex)
        B.add(base + up_d * h * 0.855, (w * 0.50, t * 0.5 + 0.008, h * 0.145), GOLD, bone,
              R=Matrix((side, nrm, up_d)).transposed(), top=(0.22, 0.75), rnd=0.45, studs=[], nostud=True,
              role="limb")""")
rep("""        B.seg(p - dv * 0.012, q + dv * 0.012, gw, t * 0.5 + 0.009, GOLD, bone, side=nrm.cross(dv),""",
    """        B.seg(p - dv * 0.012, q + dv * 0.012, gw, t * 0.5 + (0.015 if gem else 0.009), GOLD, bone, side=nrm.cross(dv),""")
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
