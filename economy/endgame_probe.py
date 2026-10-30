import sys, random, statistics
sys.argv = [sys.argv[0], "--sim"]
src = open("hatch_v7.py").read().replace("    v.report(lad, seeds=30)\n", "")
exec(src)
incs, rebirth_inc = [], {}
for s in range(12):
    p = v.P(random.Random(s))
    for i, (cost, a, k) in enumerate(lad):
        if p.run_rebirth(cost, a, k) is None: break
        rebirth_inc.setdefault(i + 1, []).append(p.income_at(p.t + 1e7))
    incs.append(p.income_at(p.t + 1e7))
for r in (12, 16, 18, 20):
    print(f"income/s after R{r}: median ${pm.fmt(statistics.median(rebirth_inc[r]))}")
med = statistics.median(incs)
print(f"R20 player earns ~${pm.fmt(med)}/s = ${pm.fmt(med*3600)}/h")
for name, price in [("x12", 2e12), ("x14", 10e12), ("x16", 50e12), ("x18", 200e12), ("x20", 1e15)]:
    print(f"  {name} ${pm.fmt(price)} = {price/med/3600:6.1f} h of R20 income")
