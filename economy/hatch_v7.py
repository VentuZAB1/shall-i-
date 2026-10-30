"""Area + KG hatch times (owner 2026-10-12: Celestial 200K -> 6-12 h, ~1M -> 12-24 h; further areas longer).
hatch = 9 h x AREA[area] x (KG / 200K) ^ 0.43, at least 10 s.  (200K x5 KG -> x2 time: 9 h -> 18 h)"""
import math, random, statistics, sys
import pacing_model as pm
import v5_model as v
AREA = [0.02, 0.04, 0.1, 0.25, 0.5, 1.0]
def hatch(area, kg):
    return max(10, 32400 * AREA[area - 1] * (max(kg, 1) / 200_000) ** 0.43)
def fmt_t(s):
    if s < 60: return f"{s:.0f}s"
    if s < 3600: return f"{s/60:.0f}m"
    return f"{s/3600:.1f}h"
print("hatch table:")
print(f"{'KG':>8} " + " ".join(f"{n:>9}" for n in pm.AREA_NAMES))
for kg in (1, 100, 1_000, 10_000, 30_000, 100_000, 200_000, 500_000, 1_000_000, 5_000_000):
    print(f"{pm.fmt(kg):>8} " + " ".join(f"{fmt_t(hatch(a, kg)):>9}" for a in range(1, 7)))
print(f"{'v4/v6':>8} now: 1KG 10s, 1K 2m, 10K 4.5m, 100K 9.5m, 1M 23m (same everywhere)")
if "--sim" in sys.argv:
    sys.argv = sys.argv[:1]
    exec(open("tread_v6.py").read().split("FINAL = ")[0])  # v6 treadmills + curve
    # the model's place(): hatch time by area
    def place(self, area, kg):
        new_income = pm.income(area, kg)
        ready = self.t + hatch(area, kg)
        if len(self.pets) < self.slots():
            self.pets.append([area, kg, ready]); return
        worst = min(range(len(self.pets)), key=lambda i: pm.income(self.pets[i][0], self.pets[i][1]))
        if new_income > pm.income(self.pets[worst][0], self.pets[worst][1]) * 1.05:
            self.pets[worst] = [area, kg, ready]
    pm.Player.place = place
    # rebirth pet requirement must be HATCHED (ready) to count
    pm.Player.has_pet = lambda self, area, kg: any(a == area and k >= kg and r <= self.t for a, k, r in self.pets)
    FINAL = [40e3, 2e6, 5.5e6, 25e6, 125e6, 800e6, 1.8e9, 4e9, 20e9, 50e9, 80e9, 250e9, 900e9, 1.5e12, 2.25e12, 3.5e12, 5e12, 6.5e12, 9e12, 14e12]
    lad = [[c, a, k] for c, (_, a, k) in zip(FINAL, pm.LADDER)]
    v.report(lad, seeds=30)
