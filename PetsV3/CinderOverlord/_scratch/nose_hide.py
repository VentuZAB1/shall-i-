# python CinderOverlord/_scratch/nose_hide.py <variant> : writes a variant of the pet file (hide test, r13 MUST 2)
import io, sys
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
base = io.open(r"C:\Users\ventu\AppData\Local\Temp\cin_r12_base.py", encoding="utf-8").read() if False else None
s = io.open(sys.argv[2], encoding="utf-8").read()
v = sys.argv[1]
if v in ("nosnout", "both"):
    a = "skf(f)[3] + 0.004, skf(f)[4] + 0.004, seg=20, n=2.8) for f in (0.74, 0.82, 0.90, 0.96, 1.0)]"
    assert s.count(a) == 1
    s = s.replace(a, "skf(f)[3] - 0.006, skf(f)[4] - 0.006, seg=20, n=2.8) for f in (0.74, 0.82, 0.90, 0.96, 1.0)]")
    a = "oval(*skf(1.012)[:3], skf(1.0)[3] * 0.80, skf(1.0)[4] * 0.60, seg=20, n=2.8)"
    assert s.count(a) == 1
    s = s.replace(a, "oval(*skf(0.99)[:3], skf(1.0)[3] * 0.30, skf(1.0)[4] * 0.30, seg=20, n=2.8)")
if v in ("nochin", "both"):
    a = "jkf(f)[3] + 0.004, jkf(f)[4] + 0.004, seg=20, n=2.8) for f in (0.80, 0.88, 0.95, 1.0)]"
    assert s.count(a) == 1
    s = s.replace(a, "jkf(f)[3] - 0.006, jkf(f)[4] - 0.006, seg=20, n=2.8) for f in (0.80, 0.88, 0.95, 1.0)]")
    a = "oval(*jkf(1.006)[:3], jkf(1.0)[3] * 0.80, jkf(1.0)[4] * 0.80, seg=20, n=2.8)"
    assert s.count(a) == 1
    s = s.replace(a, "oval(*jkf(0.99)[:3], jkf(1.0)[3] * 0.30, jkf(1.0)[4] * 0.30, seg=20, n=2.8)")
if v == "nopale":
    a = 'B.seg((0, -0.54, 1.560), (0, -0.98, 1.548), 0.12, 0.03, PALE_S, "Head"'
    assert s.count(a) == 1
    s = s.replace(a, 'B.seg((0, -0.54, 1.580), (0, -0.70, 1.578), 0.05, 0.01, PALE_S, "Head"')
io.open(p, "w", encoding="utf-8").write(s)
print("variant", v)
