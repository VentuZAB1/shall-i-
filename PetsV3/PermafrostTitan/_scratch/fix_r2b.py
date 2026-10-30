import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
s = io.open(p, encoding="utf-8").read()
a = """    ARM = [(0, 0, 0, 0), (18, 4, 14, 22), (30, 4, 14, 30), (50, 4, 14, 30), (62, 2, 6, 8), (80, 0, 0, 0), (100, 0, 0, 0)]"""
b = """    # r2 MUST 4: asymmetric hold - the RIGHT fist rests forward on the raised right knee, the LEFT arm hangs out to the
    # side so the kneeling left knee stays visible from the front / 3-4 (f, out, fwd, bend)
    ARM_R = [(0, 0, 0, 0), (18, 4, 18, 26), (30, 4, 20, 32), (50, 4, 20, 32), (62, 2, 8, 8), (80, 0, 0, 0), (100, 0, 0, 0)]
    ARM_L = [(0, 0, 0, 0), (18, 14, 0, 12), (30, 16, -2, 14), (50, 16, -2, 14), (62, 6, 2, 6), (80, 0, 0, 0), (100, 0, 0, 0)]"""
c = """        arms_fk(k, f, out=curve([(a[0], a[1]) for a in ARM], f), fwd=curve([(a[0], a[2]) for a in ARM], f),
                bend=curve([(a[0], a[3]) for a in ARM], f))"""
d = """        for sgn, side, T in ((1, "L", ARM_L), (-1, "R", ARM_R)):
            k.key("Arm_" + side, f, rot=(-curve([(a[0], a[2]) for a in T], f), 0, -sgn * curve([(a[0], a[1]) for a in T], f)))
            k.key("Fore_" + side, f, rot=(-curve([(a[0], a[3]) for a in T], f), 0, 0))
            k.key("Hand_" + side, f, rot=(0, 0, 0))"""
for x, y in ((a, b), (c, d)):
    assert s.count(x) == 1, x[:60]
    s = s.replace(x, y)
io.open(p, "w", encoding="utf-8").write(s)
print("ok")
