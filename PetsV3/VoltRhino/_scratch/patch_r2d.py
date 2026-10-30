import os
p = os.path.join(os.path.dirname(__file__), "..", "..", "pets", "VoltRhino.py")
s = open(p, encoding="utf-8").read()
def R(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
R('''zhi=-0.92, zhi1=-0.46, grow=0.008, step=0.04)
    Lb.band(B, sy(-0.56), sj, PALE, "Chest", zlo=-1.0, zhi=-0.46, grow=0.008, step=0.06)
    Lb.band(B, sj, sy(0.56), PALE, "Spine", zlo=-1.0, zhi=-0.46, grow=0.008, step=0.06)
    Lb.band(B, sy(0.56), sy(0.82), PALE, "Spine", zlo=-1.0, zhi=-0.46, zhi1=-0.92,''',
  '''zhi=-0.92, zhi1=-0.38, grow=0.008, step=0.04)
    Lb.band(B, sy(-0.56), sj, PALE, "Chest", zlo=-1.0, zhi=-0.38, grow=0.008, step=0.06)
    Lb.band(B, sj, sy(0.56), PALE, "Spine", zlo=-1.0, zhi=-0.38, grow=0.008, step=0.06)
    Lb.band(B, sy(0.56), sy(0.82), PALE, "Spine", zlo=-1.0, zhi=-0.38, zhi1=-0.92,''')
R('''    Ln.tube(B, 0.0, Ln.length, IRON, "Neck", step=0.06)
''', '''    Ln.tube(B, 0.0, Ln.length, IRON, "Neck", step=0.06)
    Ln.band(B, 0.0, Ln.length, PALE, "Neck", zlo=-1.0, zhi=-0.55, grow=0.008, step=0.05)          # pale throat
''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
