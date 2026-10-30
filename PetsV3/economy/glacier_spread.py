"""Spread (P25 / median / P90) of the late runs in glacier_sim.py, 40 seeds. python glacier_spread.py [--continuous]"""
import sys, statistics, random
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\economy")
import glacier_sim as g
if "--continuous" in sys.argv:
    g.SESSION[1] = 0
    g.PAYBACK_H = 96
seeds = 40
rows = [g.simulate(g.GLACIER, s) for s in range(seeds)]
def q(v, p):
    v = sorted(v); return v[min(len(v) - 1, int(p * len(v)))]
print("continuous" if g.SESSION[1] == 0 else "3h/day + offline", seeds, "seeds")
for i in range(19, 25):
    runs = [r[0][i] for r in rows if len(r[0]) > i]
    tot = [r[1].ms.get(f"R{i+1}", float('inf')) for r in rows]
    print(f"R{i+1}: run P25 {q(runs,.25)/3600:5.1f}  med {statistics.median(runs)/3600:5.1f}  P90 {q(runs,.9)/3600:5.1f} h | total med {statistics.median(tot)/3600:6.1f}  P90 {q(tot,.9)/3600:6.1f} h")
fg = [r[1].ms.get("first Glacier egg") for r in rows]
print("first Glacier egg: med", round(statistics.median(fg)/3600,1), "h  P90", round(q(fg,.9)/3600,1))
