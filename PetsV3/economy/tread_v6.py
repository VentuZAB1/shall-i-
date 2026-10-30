"""Linear treadmills x1 x2 x4 x6 x8 x10 (+2 per tier, more tiers later) with a re-tuned walk curve:
identical to v5 up to Thunder (walk 75 at Speed ~100M), then compressed so Fire / Shadow / Celestial need
200M / 360M / 750M Speed (a few minutes on the tier you'd own then). Model speeds are on the old scale (+10M)."""
import math, random, statistics, sys
import pacing_model as pm
import v5_model as v
OFF = 10_000_000
def X(s): return math.log10(1 + s + OFF)
pm.CURVE = [(0, 16), (6, 30), (7, 48), (7.1, 54), (7.25, 60), (7.5, 66), (X(100e6), 75), (X(200e6), 92), (X(360e6), 115),
            (X(750e6), 141), (X(7.5e9), 165), (X(75e9), 190), (X(750e9), 215), (X(7.5e12), 240), (X(25e12), 250)]
TIER_PRICE = [0, 10_000, 2_000_000, float(sys.argv[1]) if len(sys.argv) > 1 else 100e6,
              float(sys.argv[2]) if len(sys.argv) > 2 else 1.5e9, float(sys.argv[3]) if len(sys.argv) > 3 else 80e9]
pm.TREADMILL = [(p, 50_000 * m) for p, m in zip(TIER_PRICE, [1, 2, 4, 6, 8, 10])]
FINAL = [40e3, 2e6, 5.5e6, 25e6, 125e6, 800e6, 1.8e9, 4e9, 20e9, 50e9, 80e9, 250e9, 900e9, 1.5e12, 2.25e12, 3.5e12, 5e12, 6.5e12, 9e12, 14e12]
lad = [[c, a, k] for c, (_, a, k) in zip(FINAL, pm.LADDER)]
print("tiers:", [(f"${pm.fmt(p)}", f"{r//1000}K/s") for p, r in pm.TREADMILL])
print("speed for walk 58/75/92/115/141:", [pm.fmt(pm.speed_for_walk(w) - OFF) for w in (58, 75, 92, 115, 141)])
if "--tune" in sys.argv:
    v.TARGET = v.TARGET  # same targets as v5
    lad = v.tune()
v.report(lad, seeds=40)
# treadmill purchase timeline (all tiers)
ev = {}
for s in range(40):
    p = v.P(random.Random(s))
    for cost, a, k in lad:
        if p.run_rebirth(cost, a, k) is None: break
    for t, what in p.buys:
        if what.startswith("Treadmill"): ev.setdefault(what, []).append(t)
for what, tl in sorted(ev.items(), key=lambda kv: statistics.median(kv[1])):
    print(f"   {what}: median at {statistics.median(tl)/3600:5.1f} h ({len(tl)}/40 players)")
