p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\PermafrostTitan.py"
t = open(p, encoding="utf-8").read()
a = """        B.seg(Ev + de * 0.09, Wv - de * 0.05, 0.158, 0.166, PLUM, fore, top=(1.08, 1.06), rnd=0.36)   # bracer"""
b = """        br = B.seg(Ev + de * 0.11, Wv - de * 0.06, 0.150, 0.158, PLUM, fore, top=(1.07, 1.05), rnd=0.40)  # bracer
        for t_, L, w, lean in ((0.35, 0.075, 0.042, 0.5), (0.70, 0.065, 0.038, 0.8)):                 # ice crusts
            q = (Ev + de * 0.11).lerp(Wv - de * 0.06, t_)
            ice_chunk(B, q + Vector((s * 0.135, 0.02, 0.0)), (s * 1.0, 0.25, lean), L, w, fore)"""
assert a in t
t = t.replace(a, b)
open(p, "w", encoding="utf-8").write(t)
print("ok")
