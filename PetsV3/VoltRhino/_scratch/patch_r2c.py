import os
p = os.path.join(os.path.dirname(__file__), "..", "..", "pets", "VoltRhino.py")
s = open(p, encoding="utf-8").read()
def R(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
R("""        for t, dz in ((0.16, 0.045), (0.34, -0.040), (0.56, 0.032), (0.74, -0.026), (0.86, 0.010)):""",
  """        for t, dz in ((0.16, 0.045), (0.33, -0.040), (0.52, 0.030), (0.68, -0.020), (0.80, 0.006)):""")
R("""            Q.append((c + ax * s * (hw + 0.004) + dv * dz, ax * s))
        zig(B, Q, VOLT, "Head", 0.060, thick=0.013)""",
  """            hd = H[j] + (H[j + 1] - H[j]) * u
            Q.append((c + ax * s * (hw + 0.004) + dv * dz, ax * s, min(0.060, 1.15 * hd)))
        for i_, ((a_, na), (c_, nc)) in enumerate(zip([(q[0], q[1]) for q in Q], [(q[0], q[1]) for q in Q[1:]])):
            d_ = (c_ - a_).normalized()
            w_ = min(Q[i_][2], Q[i_ + 1][2])
            B.bar(a_ - d_ * (w_ * 0.35 if i_ else 0.0), c_, (na + nc).normalized(), w_, 0.013, VOLT, "Head",
                  studs=[], bevel=0.004, top=(1, 0.15) if i_ == len(Q) - 2 else (1, 1))""")
R("""    B.seg((0, -1.18, 0.703), (0, -1.56, 0.698), 0.10, 0.022, PALE, "Jaw", top=(0.85, 1), rnd=0.45, studs=[])  # chin""",
  """    B.seg((0, -1.18, 0.735), (0, -1.56, 0.703), 0.10, 0.016, PALE, "Jaw", top=(0.85, 1), rnd=0.45, studs=[])  # chin""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
