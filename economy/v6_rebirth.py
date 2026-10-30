"""SLINGSHOT rebirth ladder v6 (2026-10-21, owner: "lower all rebirthing making the higher amounts harder to reach,
but for the newbies from 0 to 10th to be slightly easy").
  * R1 = money only (no Water pet) and $25K: only 11% of new players reached Rebirth 1 (funnel 10-21)
  * R2-R10 about 25-30% cheaper than v5
  * R11-R20 about 1.5-2.3x pricier than v5 (the long game takes longer)
Pet requirements from R2 are unchanged. Compares v5 vs v6 run times with the v5 player model.
Run: python v6_rebirth.py [seeds]"""
import sys, statistics, random
import v5_model as v5
import pacing_model as pm

V6 = [
    [25_000, 1, 1],              # R1  money only (any Grass pet = the tutorial pet)
    [1_200_000, 2, 1],           # R2  Water pet
    [4_000_000, 3, 1],           # R3
    [18_000_000, 3, 100],        # R4
    [90_000_000, 4, 1],          # R5
    [550_000_000, 4, 100],       # R6
    [1_300_000_000, 4, 1000],    # R7
    [3_000_000_000, 5, 1],       # R8
    [15_000_000_000, 5, 100],    # R9
    [38_000_000_000, 5, 1000],   # R10
    [120_000_000_000, 5, 10000],  # R11
    [400_000_000_000, 6, 1],     # R12
    [1_500_000_000_000, 6, 100],     # R13
    [2_600_000_000_000, 6, 1000],    # R14
    [4_000_000_000_000, 6, 5000],    # R15
    [6_500_000_000_000, 6, 10000],   # R16
    [9_500_000_000_000, 6, 25000],   # R17
    [13_000_000_000_000, 6, 50000],  # R18
    [19_000_000_000_000, 6, 100000],  # R19
    [32_000_000_000_000, 6, 1000000],  # R20
]

def runs(ladder, seeds):
    out = []
    for s in range(seeds):
        p = v5.P(random.Random(s))
        ts = []
        for cost, area, kg in ladder:
            dt = p.run_rebirth(cost, area, kg)
            ts.append(dt if dt is not None else float("inf"))
            if dt is None:
                break
        out.append(ts)
    return out

def medians(rs, n):
    return [statistics.median([r[i] for r in rs if len(r) > i]) for i in range(n)]

if __name__ == "__main__":
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    cur = [[40_000, 2, 1]] + [list(x) for x in v5.LADDER[1:]]
    # v5 as live in Studio (RebirthConfig.LADDER, 2026-10-21)
    cur = [[40_000, 2, 1], [2_000_000, 2, 1], [5_500_000, 3, 1], [25_000_000, 3, 100], [125_000_000, 4, 1],
           [800_000_000, 4, 100], [1_800_000_000, 4, 1000], [4_000_000_000, 5, 1], [20_000_000_000, 5, 100],
           [50_000_000_000, 5, 1000], [80_000_000_000, 5, 10000], [250_000_000_000, 6, 1], [900_000_000_000, 6, 100],
           [1_500_000_000_000, 6, 1000], [2_250_000_000_000, 6, 5000], [3_500_000_000_000, 6, 10000],
           [5_000_000_000_000, 6, 25000], [6_500_000_000_000, 6, 50000], [9_000_000_000_000, 6, 100000],
           [14_000_000_000_000, 6, 1000000]]
    a = medians(runs(cur, seeds), 20)
    b = medians(runs(V6, seeds), 20)
    ta = tb = 0
    print(f"{'R':>3} {'v5 cost':>9} {'v6 cost':>9} {'v5 run':>8} {'v6 run':>8} {'v5 total':>9} {'v6 total':>9}")
    for i in range(20):
        ta += a[i]; tb += b[i]
        print(f"{i+1:>3} {pm.fmt(cur[i][0]):>9} {pm.fmt(V6[i][0]):>9} {a[i]/60:7.1f}m {b[i]/60:7.1f}m {ta/3600:8.1f}h {tb/3600:8.1f}h")
