import sys
sys.argv = [a for a in sys.argv]
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\PumpkinEggs")
import eggs
from eggs import *
key = sys.argv[sys.argv.index("--") + 1]
E = EGGS[key]; P = E["P"]
fresh(8)
flesh = mat_flesh()
outl = {k: clean(v) for k, v in E["face"]().items()}
def selfx(pts):
    n = len(pts); hits = 0
    def inter(a, b, c, d):
        def cr(o, p, q): return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
        d1, d2, d3, d4 = cr(c, d, a), cr(c, d, b), cr(a, b, c), cr(a, b, d)
        return (d1 * d2 < 0) and (d3 * d4 < 0)
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1: continue
            if inter(pts[i], pts[(i+1)%n], pts[j], pts[(j+1)%n]): hits += 1
    return hits
for k, v in outl.items():
    one = {k: v}
    cut = cutter_radial("C_" + k, one, P["R"], P["Rz"], flesh, inner_k=0.55, outer_k=1.4, egg=P["egg"])
    bm = bmesh.new(); bm.from_mesh(cut.data)
    nm = sum(1 for e in bm.edges if not e.is_manifold)
    vol = bm.calc_volume(signed=True)
    bm.free()
    print("OUTLINE", k, "pts", len(v), "selfx", selfx(v), "nonmanifold", nm, "vol", round(vol, 4))
