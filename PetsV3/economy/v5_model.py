"""SLINGSHOT economy v5 (early-game rebalance, 2026-10-12) on top of pacing_model.py (v4).
Changes under test:
  * Grass / Water pet income buffed (AREA_INCOME 8 -> G, 50 -> W)
  * cheap early slingshot levels (Lv1-5 table), v4 curve from Lv6
  * cheap first treadmill upgrade (T2), later tiers unchanged unless set
  * rebirth ladder re-tuned: R1-R4 faster, R5+ keep the v4 run-time targets
Speed start 0 is only a display shift (walk curve offset 10M) -> no effect on this model.
Run: python v5_model.py [--tune]"""
import math, random, statistics, sys, copy
import pacing_model as pm

# ------------------------------------------------------------------ v5 proposal
pm.AREA_INCOME = [20, 120, 300, 1800, 10000, 55000]
SLING_START, SLING_STEP = 500, 2.6       # v5: smooth cheap curve until it meets the v4 curve (Lv15)
def sling_price(level):            # price of buying `level`
    return min(SLING_START * SLING_STEP ** (level - 1), pm.SLING_BASE * pm.SLING_GROWTH ** (level - 1))
pm.TREADMILL = [(0, 50_000), (10_000, 300_000), (2_000_000, 2_000_000), (2_500_000_000, 12_000_000),
                (50_000_000_000, 75_000_000), (2_000_000_000_000, 500_000_000)]
SLING_REBIRTH = [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 7, 7, 7, 9, 9, 11, 11, 13, 13]
GRAB_COSTS = [100_000, 5_000_000, 250_000_000, 10_000_000_000, 500_000_000_000]
GRAB_REBIRTH = [1, 3, 5, 8, 12]
GRAB_TIMES = [1.5, 1.2, 0.9, 0.6, 0.4, 0.2]
OLD_TARGET = [15 * 1.22 ** i for i in range(pm.MAX_REBIRTH)]
TARGET = [8, 11, 14, 18, 24, 31, 40, 52, 66] + OLD_TARGET[9:]
LADDER = [list(x) for x in pm.LADDER]

class P(pm.Player):
    def __init__(self, rng):
        super().__init__(rng)
        self.sling = 1          # tutorial gives Sling Lv1
        self.buys = []          # (time, what)
        self.grab = 0

    def run_rebirth(self, cost, req_area, req_kg, max_seconds=60 * 3600):
        start = self.t
        need_speed = pm.speed_for_walk(pm.AREA_WALK[req_area - 1])
        while self.t - start < max_seconds:
            if self.money >= cost and self.has_pet(req_area, req_kg):
                self.money = 0.0
                self.speed = pm.START_SPEED
                self.r += 1
                self.buys.append((self.t, f"Rebirth {self.r}"))
                return self.t - start
            if self.tier < len(pm.TREADMILL):
                price = pm.TREADMILL[self.tier][0]
                slow = self.speed < need_speed and (need_speed - self.speed) / self.tread_rate() / 60 > pm.ASSUME["train_max_min"]
                if self.money >= price and (price <= pm.ASSUME["buy_tread_frac"] * cost or slow or self.tier == 1):
                    self.money -= price
                    self.tier += 1
                    self.buys.append((self.t, f"Treadmill T{self.tier}"))
                    continue
            if self.grab < len(GRAB_COSTS) and self.r >= GRAB_REBIRTH[self.grab]:
                price = GRAB_COSTS[self.grab]
                if self.money >= price and price <= 0.15 * cost:
                    self.money -= price
                    self.grab += 1
                    pm.ASSUME["hub_overhead"] = 10.0 - (1.5 - GRAB_TIMES[self.grab])
                    self.buys.append((self.t, f"Grab Lv{self.grab}"))
                    continue
            if self.sling < pm.SLING_MAX and self.r >= SLING_REBIRTH[self.sling]:
                price = sling_price(self.sling + 1)
                if self.money >= price and (self.sling < 5 or price <= pm.ASSUME["buy_sling_frac"] * cost):
                    self.money -= price
                    self.sling += 1
                    self.buys.append((self.t, f"Sling Lv{self.sling}"))
                    continue
            if self.speed < need_speed:
                minutes = (need_speed - self.speed) / self.tread_rate() / 60
                if minutes <= pm.ASSUME["train_max_min"]:
                    self.train_until(need_speed)
                    continue
            area = min(self.best_area_allowed(), req_area)
            if area < req_area and self.speed < need_speed:
                self.train_until(min(need_speed, self.speed + self.tread_rate() * 120))
            self.trip(area)
        return None

def tune(seeds=40):
    ladder = [list(x) for x in LADDER]
    states = [P(random.Random(s)) for s in range(seeds)]
    for i in range(pm.MAX_REBIRTH):
        _, area, kg = ladder[i]
        lo, hi = 1e3, 1e16
        for _ in range(26):
            mid = math.sqrt(lo * hi)
            times = []
            for st in states:
                p = copy.deepcopy(st)
                dt = p.run_rebirth(mid, area, kg)
                times.append(dt if dt is not None else float("inf"))
            if statistics.median(times) / 60 < TARGET[i]:
                lo = mid
            else:
                hi = mid
        ladder[i][0] = pm.nice(math.sqrt(lo * hi))
        for st in states:
            st.run_rebirth(ladder[i][0], area, kg)
        print(f"R{i+1}: ${pm.fmt(ladder[i][0])} (v4 ${pm.fmt(pm.LADDER[i][0])})  target {TARGET[i]:.0f} min", flush=True)
    return ladder

def report(ladder, seeds=60):
    runs = []
    for s in range(seeds):
        p = P(random.Random(s))
        ts = []
        for cost, area, kg in ladder:
            dt = p.run_rebirth(cost, area, kg)
            ts.append(dt if dt is not None else float("inf"))
            if dt is None: break
        runs.append((ts, p))
    total = 0
    print(f"{'R':>3} {'cost':>9} {'v4 cost':>9} {'needs':>18} {'run':>8} {'v4 run':>7} {'total':>7}")
    for i, (cost, area, kg) in enumerate(ladder):
        med = statistics.median([r[0][i] for r in runs if len(r[0]) > i])
        total += med
        print(f"{i+1:>3} {pm.fmt(cost):>9} {pm.fmt(pm.LADDER[i][0]):>9} {pm.AREA_NAMES[area-1]+' >= '+pm.fmt(kg)+'KG':>18} "
              f"{med/60:7.1f}m {OLD_TARGET[i]:6.0f}m {total/3600:6.1f}h")
    # early purchase timeline (seed medians)
    print("\nfirst 60 minutes - when each purchase happens (median over seeds):")
    events = {}
    for ts, p in runs:
        for t, what in p.buys:
            if t <= 3600:
                events.setdefault(what, []).append(t)
    for what, tl in sorted(events.items(), key=lambda kv: statistics.median(kv[1])):
        if len(tl) >= seeds // 2:
            print(f"   {statistics.median(tl)/60:5.1f} min  {what}")

if __name__ == "__main__":
    lad = tune() if "--tune" in sys.argv else LADDER
    print()
    report(lad)
