"""SLINGSHOT Glacier update economy sim (2026-10-27): area 7 FROSTFALL GLACIER, +1 pet per area, rebirths R21-R25,
Slingshot Power Lv26-30. PLANNING ONLY - nothing here changes the game.

One greedy FREE player (no passes, no potions, no Robux), the same behaviour rules as economy/v5_model.py (P) +
pacing_model.py, but with every live number read from Studio on 2026-10-27 (the older sims predate several changes):
  * pet income = AREA_INCOME[area] x KG^0.25 x rarityMult, rarityMult = max(1, (50 / odds%)^0.35)  (CreatureConfig)
  * species roll = CreatureConfig.odds: heavier eggs are luckier (up to x4 for the rarest at 10M KG)
  * hatch = max(10, 32400 x AREA_HATCH[area] x (KG/200K)^0.43) s on the REAL clock (keeps going offline)
  * egg KG roll = EggSpawner.rollWeight (normal + lucky roll)
  * pet slots = 3 + rebirths, shared by growing eggs and pets (BaseHatchery); replaced pets go to the inventory
  * money boost = (1 + 0.25 R) x (1 + 0.05 x Index claims) x 1.08 playtime gifts; offline = 10% for up to 24 h
  * speed: treadmill tiers x1..x20 (ShopConfig), Speed mult = rebirth x Index, walk = SpeedStat curve (OFFSET 10M)
  * Slingshot Power: price/lock/range from UpgradeConfig (Lv1 free in the tutorial)
Player rules (pacing_model ASSUME): picks the heaviest of 4 visible eggs, buys a treadmill tier at <= 35% of the next
rebirth (or when training would take > 12 min), a sling level at <= 10% (Lv1-5 always), Fast Grab at <= 15%; farms
the area the next rebirth needs (never further), trains to that area's walk speed first; swaps an earning pet for a
growing egg only when the egg pays its hatch time back within PAYBACK_H real hours - eggs a rebirth needs always go in.
Sessions: DEDICATED = 3 h of play a day, offline the other 21 h (eggs hatch, 10% offline money). --continuous = no
breaks (the old "time in a server" numbers).

Run:  python glacier_sim.py                 full report (today vs Glacier), 24 seeds
      python glacier_sim.py --tune          solve R21-R25 costs for the run-time targets (prints the costs)
      python glacier_sim.py --continuous    same report, no offline breaks
"""
import math
import random
import statistics
import sys
import copy

# ------------------------------------------------------------------ live numbers (Studio, 2026-10-27)
NAMES = ["Grass", "Water", "Thunder", "Fire", "Shadow", "Celestial", "Glacier"]
AREA_INCOME = [20, 120, 300, 1800, 10000, 55000, 300000]          # [7] = PROPOSED ($55K x 5.5)
AREA_HATCH = [0.02, 0.04, 0.1, 0.25, 0.5, 1.0, 2.0]                 # [7] = PROPOSED
KG_MAX = [30e3, 60e3, 100e3, 200e3, 300e3, 500e3, 800e3]            # [7] = PROPOSED
KG_SKEW = [3.2, 3.0, 2.8, 2.6, 2.4, 2.2, 2.0]                       # [7] = PROPOSED
KG_LUCKY_ODDS = [0, 800, 600, 450, 330, 250, 180]                   # [7] = PROPOSED
KG_LUCKY_MAX = [30e3, 150e3, 300e3, 800e3, 2.5e6, 5e6, 10e6]        # [7] = PROPOSED

ODDS_TODAY = [[52, 28, 13, 5, 2], [53, 27, 13, 5.5, 1.5], [54, 26, 14, 5, 1], [54, 27, 13, 4, 2],
              [54, 27, 13.5, 4, 1.5], [55, 27, 13, 4, 1]]
ODDS_NEW = [[40, 30, 16, 8.5, 3.5, 2], [45, 25, 15, 9, 4.5, 1.5], [50, 25, 14, 6, 4, 1], [53.5, 27, 13, 4, 2, 0.5],
            [50, 25, 10, 9.5, 4, 1.5], [54.9, 27, 13, 4, 1, 0.1], [50, 26, 14, 7.4, 2.5, 0.1]]

OFFSET = 10_000_000
def X(s): return math.log10(1 + s + OFFSET)
CURVE = [(0, 16), (6, 30), (7, 48), (7.1, 54), (7.25, 60), (7.5, 66), (X(100e6), 75), (X(200e6), 92), (X(360e6), 115),
         (X(750e6), 141), (X(7.5e9), 165), (X(75e9), 190), (X(750e9), 215), (X(7.5e12), 240), (X(25e12), 250)]
AREA_WALK = [0, 58, 75, 92, 115, 141, 156]   # walk needed to farm an area; [7] = beat a 155 Glacier-only BLIZZARD wave

TREAD_PRICE = [0, 10e3, 2e6, 100e6, 1.5e9, 80e9, 2e12, 8e12, 25e12, 75e12, 200e12]
TREAD_RATE = [50e3 * m for m in (1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)]

SLING_BASE_RANGE = 370.32
SLING_STEP = (2300 - SLING_BASE_RANGE) / 25          # 77.19 studs per level (kept for Lv26+)
SLING_EARLY_RANGE = {1: 30, 2: 35, 3: 30, 4: 15}
SLING_EARLY_COST = {2: 600, 3: 1500}
SLING_LOCK_TODAY = [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 7, 7, 7, 9, 9, 11, 11, 13, 13]
SLING_LOCK_NEW = SLING_LOCK_TODAY + [16, 20, 20, 22, 22]          # Lv26..30 PROPOSED
AREA_Z = [-60, -460, -860, -1260, -1660, -2060, -2460]
GRAB_COSTS = [100e3, 5e6, 250e6, 10e9, 500e9]
GRAB_LOCK = [1, 3, 5, 8, 12]
GRAB_TIMES = [1.5, 1.2, 0.9, 0.6, 0.4, 0.2]

LADDER_TODAY = [  # RebirthConfig.LADDER v6 (live): (cost, area, kg); R1 = money only (any Grass pet in the model)
    (25e3, 1, 1), (1.2e6, 2, 1), (4e6, 3, 1), (18e6, 3, 100), (90e6, 4, 1), (550e6, 4, 100), (1.3e9, 4, 1000),
    (3e9, 5, 1), (15e9, 5, 100), (38e9, 5, 1000), (120e9, 5, 10000), (400e9, 6, 1), (1.5e12, 6, 100),
    (2.6e12, 6, 1000), (4e12, 6, 5000), (6.5e12, 6, 10000), (9.5e12, 6, 25000), (13e12, 6, 50000),
    (19e12, 6, 100000), (32e12, 6, 1000000)]
LADDER_R21_25 = [  # PROPOSED (tuned with --tune, rounded)
    (40e12, 7, 1), (130e12, 7, 1000), (230e12, 7, 10000), (350e12, 7, 100000), (500e12, 7, 1000000)]

INDEX_BONUS = 0.05
PLAYTIME = 1.08
OFFLINE_RATE = 0.10
EGGS_SEEN = 4
PAYBACK_H = 192  # real hours: a pet is swapped for a growing egg only if the egg pays back its hatch time within this
                 # (best result for a smart player: 192 h with 3 h/day + offline, 96 h with --continuous)

# ------------------------------------------------------------------ helpers
def fmt(n):
    for unit, v in [("Qa", 1e15), ("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)]:
        if n >= v:
            return f"{n / v:.3g}{unit}"
    return f"{n:.0f}"

def fmt_t(s):
    if s < 60: return f"{s:.0f} s"
    if s < 3600: return f"{s / 60:.0f} min"
    return f"{s / 3600:.1f} h"

def nice(n):
    if n < 100: return math.floor(n)
    p = 10 ** (math.floor(math.log10(n)) - 1)
    return math.floor(n / p + 0.5) * p

def rarity(pct):
    return max(1.0, (50 / max(pct, 0.01)) ** 0.35)

def walk_speed(speed):
    x = math.log10(1 + max(speed, 0) + OFFSET)
    for (x0, y0), (x1, y1) in zip(CURVE, CURVE[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return 250

def speed_for_walk(w):
    for (x0, y0), (x1, y1) in zip(CURVE, CURVE[1:]):
        if w <= y1:
            return max(0.0, 10 ** (x0 + (x1 - x0) * (w - y0) / (y1 - y0)) - OFFSET - 1)
    return 25e12

def hatch_s(area, kg):
    return max(10.0, 32400 * AREA_HATCH[area - 1] * (max(kg, 1) / 200_000) ** 0.43)

def roll_kg(area, rng):
    a = area - 1
    if KG_LUCKY_ODDS[a] > 0 and rng.randint(1, KG_LUCKY_ODDS[a]) == 1:
        w = min(KG_LUCKY_MAX[a], KG_MAX[a] * (1 - rng.random()) ** (-1 / 1.5))
    else:
        w = 10 ** (math.log10(KG_MAX[a]) * rng.random() ** KG_SKEW[a])
    return max(1, math.floor(w))

def species_weights(odds, kg):
    n = len(odds)
    luck = min(1.0, max(0.0, math.log10(max(kg, 1)) / 7))
    w = [o * (1 + luck * 3 * i / max(n - 1, 1)) for i, o in enumerate(odds)]
    t = sum(w)
    return [x / t for x in w]

def sling_range(level):
    return SLING_BASE_RANGE + SLING_STEP * level + SLING_EARLY_RANGE.get(level, 0)

def sling_area(level, n_areas):
    z = -45 - sling_range(level)
    best = 1
    for i in range(n_areas):
        if z <= AREA_Z[i]:
            best = i + 1
    return best

def sling_cost(level):
    if level in SLING_EARLY_COST: return SLING_EARLY_COST[level]
    return nice(min(500 * 2.6 ** (level - 1), 25000 * 1.95 ** (level - 1)))

# ------------------------------------------------------------------ the player
class Scenario:
    def __init__(self, name, odds, ladder, sling_lock, n_areas):
        self.name, self.odds, self.ladder, self.sling_lock, self.n_areas = name, odds, ladder, sling_lock, n_areas
        self.sling_max = len(sling_lock)
        self.rar = [[rarity(100 * o / sum(od)) for o in od] for od in odds]

TODAY = Scenario("TODAY (6 areas, R20, Lv25)", ODDS_TODAY, LADDER_TODAY, SLING_LOCK_TODAY, 6)
GLACIER = Scenario("GLACIER (7 areas, R25, Lv30)", ODDS_NEW, LADDER_TODAY + LADDER_R21_25, SLING_LOCK_NEW, 7)

SESSION = [3 * 3600, 21 * 3600]   # play, offline

class Player:
    def __init__(self, rng, sc):
        self.rng, self.sc = rng, sc
        self.play = 0.0       # seconds played
        self.real = 0.0       # real clock (hatching)
        self.session_left = SESSION[0]
        self.money = 0.0
        self.speed = 0.0
        self.r = 0
        self.tier = 1
        self.sling = 1        # tutorial: free Lv1
        self.grab = 0
        self.slots = []       # [inc, area, kg, ready_real]  (eggs + pets in the base)
        self.inv = []         # [inc, area, kg]  unequipped pets (count for rebirth requirements)
        self.found = [set() for _ in range(sc.n_areas)]
        self.claims = 0
        self.claimed = set()
        self.ms = {}          # milestone -> play seconds
        self.ms_real = {}
        self.rate_cache = None

    # ---------------- boosts
    def perm(self):
        return (1 + 0.25 * self.r) * (1 + INDEX_BONUS * self.claims)

    def base_rate(self, at_real):
        return sum(p[0] for p in self.slots if p[3] <= at_real)

    def tread_rate(self):
        return TREAD_RATE[self.tier - 1] * self.perm()

    def mark(self, key):
        if key not in self.ms:
            self.ms[key] = self.play
            self.ms_real[key] = self.real

    # ---------------- time
    def _earn(self, dt, mult):
        """money over dt seconds of REAL time at `mult` x the boosted rate (hatches inside dt start earning)"""
        t0, t1 = self.real, self.real + dt
        cuts = sorted({t0, t1} | {p[3] for p in self.slots if t0 < p[3] < t1})
        k = self.perm() * mult
        for a, b in zip(cuts, cuts[1:]):
            self.money += self.base_rate(a + 1e-9) * k * (b - a)
        self.real = t1

    def advance(self, dt):
        """dt seconds of PLAY; crosses into offline breaks when a session ends"""
        while dt > 0:
            step = min(dt, self.session_left)
            self._earn(step, PLAYTIME)
            self.play += step
            dt -= step
            self.session_left -= step
            if self.session_left <= 1e-9:
                if SESSION[1] > 0:
                    off = SESSION[1]
                    # offline: pets keep earning 10% (24 h cap), eggs keep hatching
                    self._earn(min(off, 86400), OFFLINE_RATE)
                    self.real += max(0.0, off - 86400)
                    self.after_offline()
                self.session_left = SESSION[0]

    def after_offline(self):
        self.reap()

    def train_until(self, target):
        need = max(0.0, target - self.speed)
        self.advance(need / self.tread_rate())
        self.speed = max(self.speed, target)

    # ---------------- pets
    def reap(self):
        """hatched eggs -> discovered species / Index claims"""
        for i, a in enumerate(range(1, self.sc.n_areas + 1)):
            if a not in self.claimed and len(self.found[i]) == len(self.sc.odds[i]):
                self.claimed.add(a)
                self.claims += 1
                self.mark(f"Index {NAMES[i]}")

    def exp_income(self, area, kg):
        w = species_weights(self.sc.odds[area - 1], kg)
        return AREA_INCOME[area - 1] * max(kg, 1) ** 0.25 * sum(x * r for x, r in zip(w, self.sc.rar[area - 1]))

    def roll_species(self, area, kg):
        w = species_weights(self.sc.odds[area - 1], kg)
        x = self.rng.random()
        for i, p in enumerate(w):
            x -= p
            if x <= 0: return i
        return len(w) - 1

    def n_slots(self):
        return 3 + self.r

    def place(self, area, kg, req):
        sp = self.roll_species(area, kg)        # fixed when the egg is placed, revealed when it hatches
        inc = AREA_INCOME[area - 1] * max(kg, 1) ** 0.25 * self.sc.rar[area - 1][sp]
        ready = self.real + hatch_s(area, kg)
        exp = self.exp_income(area, kg)
        needed = req and area == req[0] and kg >= req[1] and not self.has_pet(req[0], req[1], any_time=True)
        sell = AREA_INCOME[area - 1] * max(kg, 1) ** 0.25 * self.sc.rar[area - 1][0] * 60   # SellConfig egg value
        if len(self.slots) < self.n_slots():
            self.slots.append([inc, area, kg, ready])
            self.found[area - 1].add(sp)
            return
        hatched = [i for i, p in enumerate(self.slots) if p[3] <= self.real]
        if not hatched:
            self.money += sell
            return
        worst = min(hatched, key=lambda i: self.slots[i][0])
        old, h = self.slots[worst][0], hatch_s(area, kg) / 3600
        if needed or (exp > old * 1.05 and (exp - old) * (PAYBACK_H - h) > old * h):
            w = self.slots[worst]
            self.inv.append([w[0], w[1], w[2]])
            self.slots[worst] = [inc, area, kg, ready]
            self.found[area - 1].add(sp)
        else:
            self.money += sell

    def refill(self):
        """after a rebirth (+1 slot): equip the best inventory pets"""
        self.inv.sort(key=lambda p: -p[0])
        while len(self.slots) < self.n_slots() and self.inv:
            p = self.inv.pop(0)
            self.slots.append([p[0], p[1], p[2], self.real])

    def has_pet(self, area, kg, any_time=False):
        if any(p[1] == area and p[2] >= kg and (any_time or p[3] <= self.real) for p in self.slots):
            return True
        return any(p[1] == area and p[2] >= kg for p in self.inv)

    # ---------------- actions
    def trip(self, area, req):
        w = walk_speed(self.speed)
        d = 400 * (area - 1) + self.rng.uniform(20, 380) + 60
        walk = d / w * (1 + 40.0 / w)
        out = (3 + sling_range(self.sling) / 350) if sling_area(self.sling, self.sc.n_areas) >= area else walk
        overhead = 10.0 - (1.5 - GRAB_TIMES[self.grab])
        self.advance(out + walk + overhead)
        self.mark(f"first {NAMES[area - 1]} egg")
        kg = max(roll_kg(area, self.rng) for _ in range(EGGS_SEEN))
        self.place(area, kg, req)
        if self.rng.random() < 0.15:
            self.reap()

    def best_area_allowed(self):
        w = walk_speed(self.speed)
        best = 1
        for a in range(1, self.sc.n_areas + 1):
            if w >= AREA_WALK[a - 1]:
                best = a
        return best

    def run_rebirth(self, cost, req_area, req_kg, max_play=400 * 3600):
        start = self.play
        need_speed = speed_for_walk(AREA_WALK[req_area - 1])
        req = (req_area, req_kg)
        while self.play - start < max_play:
            self.reap()
            if self.money >= cost and self.has_pet(req_area, req_kg):
                self.money = 0.0
                self.speed = 0.0
                self.r += 1
                self.mark(f"R{self.r}")
                self.refill()
                return self.play - start
            if self.tier < len(TREAD_PRICE):
                price = TREAD_PRICE[self.tier]
                slow = self.speed < need_speed and (need_speed - self.speed) / self.tread_rate() / 60 > 12
                if self.money >= price and (price <= 0.35 * cost or slow or self.tier == 1):
                    self.money -= price
                    self.tier += 1
                    self.mark(f"Treadmill x{[1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20][self.tier - 1]}")
                    continue
            if self.grab < len(GRAB_COSTS) and self.r >= GRAB_LOCK[self.grab]:
                price = GRAB_COSTS[self.grab]
                if self.money >= price and price <= 0.15 * cost:
                    self.money -= price
                    self.grab += 1
                    continue
            if self.sling < self.sc.sling_max and self.r >= self.sc.sling_lock[self.sling]:
                price = sling_cost(self.sling + 1)
                if self.money >= price and (self.sling < 5 or price <= 0.10 * cost):
                    self.money -= price
                    self.sling += 1
                    self.mark(f"Sling Lv{self.sling}")
                    continue
            if self.speed < need_speed:
                if (need_speed - self.speed) / self.tread_rate() / 60 <= 12:
                    self.train_until(need_speed)
                    continue
            area = min(self.best_area_allowed(), req_area)
            if area < req_area and self.speed < need_speed:
                self.train_until(min(need_speed, self.speed + self.tread_rate() * 120))
            self.trip(area, req)
        return None


def simulate(sc, seed, ladder=None):
    rng = random.Random(seed)
    p = Player(rng, sc)
    runs = []
    for cost, area, kg in (ladder or sc.ladder):
        dt = p.run_rebirth(cost, area, kg)
        runs.append(dt if dt is not None else float("inf"))
        if dt is None:
            break
    return runs, p


def med(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else float("inf")


def report(seeds=24):
    print(f"Sessions: {SESSION[0] / 3600:.0f} h play + {SESSION[1] / 3600:.0f} h offline per day "
          f"({'continuous play' if SESSION[1] == 0 else 'offline hatching ON'}); {seeds} seeds, medians.\n")
    res = {}
    for sc in (TODAY, GLACIER):
        rows = [simulate(sc, s) for s in range(seeds)]
        res[sc.name] = rows
    t_rows, g_rows = res[TODAY.name], res[GLACIER.name]
    print(f"{'R':>3} {'cost':>7} {'needs':>20} | {'TODAY run':>9} {'total h':>8} | {'GLACIER run':>11} {'total h':>8} {'real d':>6}")
    for i, (cost, area, kg) in enumerate(GLACIER.ladder):
        need = f"{NAMES[area - 1]} {fmt(kg)}+ KG" if i > 0 else "money only"
        tr = med([r[0][i] for r in t_rows if len(r[0]) > i]) if i < 20 else None
        tt = med([r[1].ms.get(f"R{i + 1}") for r in t_rows]) if i < 20 else None
        gr = med([r[0][i] for r in g_rows if len(r[0]) > i])
        gt = med([r[1].ms.get(f"R{i + 1}") for r in g_rows])
        gd = med([r[1].ms_real.get(f"R{i + 1}") for r in g_rows])
        a = f"{tr / 3600:8.1f}h {tt / 3600:8.1f}" if tr is not None else f"{'-':>9} {'-':>8}"
        print(f"{i + 1:>3} {fmt(cost):>7} {need:>20} | {a} | {gr / 3600:10.1f}h {gt / 3600:8.1f} {gd / 86400:6.1f}")
    print("\nMilestones (median PLAY hours; d = real days since joining):")
    keys = ["first Water egg", "first Thunder egg", "first Fire egg", "first Shadow egg", "first Celestial egg",
            "Sling Lv25", "Treadmill x10", "Treadmill x12", "Treadmill x14", "Treadmill x16", "Treadmill x18",
            "Treadmill x20", "R20", "Sling Lv26", "Sling Lv27", "first Glacier egg", "R21", "Sling Lv30", "R25",
            "Index Fire", "Index Celestial", "Index Glacier"]
    print(f"{'milestone':>22} | {'TODAY':>14} | {'GLACIER':>14}")
    for k in keys:
        cells = []
        for rows in (t_rows, g_rows):
            v = [r[1].ms.get(k) for r in rows]
            got = [x for x in v if x is not None]
            if len(got) * 2 < len(v):
                cells.append(f"{'-':>8} ({len(got)}/{len(v)})" if got else f"{'never':>14}")
            else:
                d = med([r[1].ms_real.get(k) for r in rows if r[1].ms_real.get(k) is not None])
                cells.append(f"{med(got) / 3600:6.1f} h {d / 86400:4.1f} d")
        print(f"{k:>22} | {cells[0]:>14} | {cells[1]:>14}")
    # state at R20 / R25
    print("\nPlayer at the moment of R20 / end (GLACIER scenario, medians):")
    for label, rows in (("TODAY end (R20)", t_rows), ("GLACIER end (R25)", g_rows)):
        inc = med([r[1].base_rate(r[1].real + 1e9) * r[1].perm() * PLAYTIME for r in rows])
        tier = med([r[1].tier for r in rows])
        cl = med([r[1].claims for r in rows])
        print(f"  {label:>18}: income ${fmt(inc)}/s (${fmt(inc * 3600)}/h), treadmill tier {tier:.0f}, Index claims {cl:.0f}")


def glacier_entry_probe(seeds=24):
    """what an R20 player has when Glacier opens: income, treadmill, minutes to Glacier walk speed, Lv27 cost"""
    print("\nGlacier entry (GLACIER scenario, the moment R20 is done):")
    need = speed_for_walk(AREA_WALK[6])
    out = []
    for s in range(seeds):
        rng = random.Random(s)
        p = Player(rng, GLACIER)
        for cost, area, kg in GLACIER.ladder[:20]:
            if p.run_rebirth(cost, area, kg) is None:
                break
        inc = p.base_rate(p.real + 1e9) * p.perm() * PLAYTIME
        out.append((inc, p.tier, p.perm(), need / p.tread_rate() / 60, p.sling))
    inc = med([o[0] for o in out])
    print(f"  income ${fmt(inc)}/s, treadmill x{[1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20][int(med([o[1] for o in out])) - 1]},"
          f" Speed mult x{med([o[2] for o in out]):.2f}, sling Lv{med([o[4] for o in out]):.0f}")
    print(f"  Glacier walk 156 needs Speed {fmt(need)} = {med([o[3] for o in out]):.0f} min on that treadmill "
          f"(Celestial 141 needs {fmt(speed_for_walk(141))})")
    for lv in range(26, 31):
        print(f"  Sling Lv{lv} ${fmt(sling_cost(lv))} = {sling_cost(lv) / inc / 60:.0f} min of R20 income")


def tune(seeds=16, targets_h=None):
    """solve R21-R25 costs so the median run takes targets_h hours of play (states carried between rebirths)"""
    states = []
    for s in range(seeds):
        p = Player(random.Random(s), GLACIER)
        for cost, area, kg in LADDER_TODAY:
            p.run_rebirth(cost, area, kg)
        states.append(p)
    r20 = med([p.ms.get("R20") - p.ms.get("R19", 0) for p in states])
    print(f"R20 run (median) = {r20 / 3600:.1f} h of play")
    targets_h = targets_h or [r20 / 3600 * 1.15 ** (i + 1) for i in range(5)]
    out = []
    for i, (_, area, kg) in enumerate(LADDER_R21_25):
        lo, hi = 1e12, 1e17
        for _ in range(18):
            mid = math.sqrt(lo * hi)
            ts = []
            for st in states:
                q = copy.deepcopy(st)
                dt = q.run_rebirth(mid, area, kg)
                ts.append(dt if dt is not None else float("inf"))
            if statistics.median(ts) / 3600 < targets_h[i]:
                lo = mid
            else:
                hi = mid
        c = nice(math.sqrt(lo * hi))
        out.append((c, area, kg))
        for st in states:
            st.run_rebirth(c, area, kg)
        print(f"R{21 + i}: ${fmt(c)}  {NAMES[area - 1]} {fmt(kg)}+ KG  target {targets_h[i]:.1f} h", flush=True)
    return out


def tables():
    print("Odds tables (sum) and money bonus per pet, today -> new:")
    for a in range(6):
        t, n = ODDS_TODAY[a], ODDS_NEW[a]
        print(f"  {NAMES[a]:>9}: today sum {sum(t):g}, new sum {sum(n):g}")
    g = ODDS_NEW[6]
    print(f"  {'Glacier':>9}: new sum {sum(g):g}")
    print("\nGlacier hatch times (AREA_HATCH 2.0) vs Celestial (1.0):")
    for kg in (1, 100, 1000, 10_000, 100_000, 200_000, 800_000, 1_000_000, 2_500_000, 10_000_000):
        print(f"  {fmt(kg):>6} KG: Glacier {fmt_t(hatch_s(7, kg)):>8}   Celestial {fmt_t(hatch_s(6, kg)):>8}")
    print("\nGlacier egg KG odds (one egg; normal roll + 1 in 180 lucky):")
    rng = random.Random(1)
    N = 400_000
    ks = [roll_kg(7, rng) for _ in range(N)]
    for th in (1000, 10_000, 100_000, 1_000_000, 2_500_000):
        n = sum(1 for k in ks if k >= th)
        print(f"  >= {fmt(th):>5} KG: 1 in {N / max(n, 1):,.0f} eggs")
    rng = random.Random(2)
    ks6 = [roll_kg(6, rng) for _ in range(N)]
    n6 = sum(1 for k in ks6 if k >= 1_000_000)
    print(f"  (Celestial >= 1M KG today: 1 in {N / max(n6, 1):,.0f} eggs)")


PET_NAMES = [
    ["Bramble Badger*", "Mossback Tortoise", "Forest Stag", "Treant", "Venom Basilisk", "Thornblade Mantis"],
    ["Kappa", "Sea Turtle Warrior", "Coral Crusher Crab*", "Kraken", "Hammerjaw Shark", "Abyssal Orca"],
    ["Raiju", "Thunder Bull", "Storm Wyvern", "Volt Rhino*", "Thunderbird", "Thunder Rex"],
    ["Molten Boar", "Lava Golem", "Cerberus", "Ivonrath", "Inferno Phoenix", "Cinder Wyrm Overlord*"],
    ["Shade Panther", "Nightmare Stallion", "Wraith Hound*", "Black Eastern Dragon", "Pharaoh Asparuh", "Abyss Weaver"],
    ["Solar Lion", "Griffin", "Celestial Dragon", "Cvetibara", "Cosmic Leviathan", "Eclipse Seraph*"],
    ["Frostfang Lynx*", "Ice Mammoth*", "Glacier Yeti*", "Blizzard Roc*", "Permafrost Titan*", "Absolute Zero Dragon*"],
]
OLD_INDEX = [  # where each NEW-table pet sits in today's table (None = new pet)
    [None, 0, 1, 2, 3, 4], [0, 1, None, 2, 3, 4], [0, 1, 2, None, 3, 4], [0, 1, 2, 3, 4, None],
    [0, 1, None, 2, 3, 4], [0, 1, 2, 3, 4, None], [None] * 6]


def pets():
    print("Per pet: odds today -> new, money bonus (rarityMult) today -> new, change for owned pets (* = new pet)")
    for a in range(7):
        new = ODDS_NEW[a]
        print(f"  {NAMES[a]} (AREA_INCOME ${fmt(AREA_INCOME[a])}):")
        for i, o in enumerate(new):
            j = OLD_INDEX[a][i]
            r_new = rarity(o)
            if j is None:
                print(f"    {PET_NAMES[a][i]:>22}: {'new':>6} -> {o:>5g}%   x{r_new:.2f}   1 KG ${fmt(AREA_INCOME[a] * r_new)}/s")
            else:
                ot = ODDS_TODAY[a][j]
                r_old = rarity(ot)
                print(f"    {PET_NAMES[a][i]:>22}: {ot:>5g}% -> {o:>5g}%   x{r_old:.2f} -> x{r_new:.2f}  ({100 * (r_new / r_old - 1):+.0f}%)")
        e_old = sum(o / 100 * rarity(o) for o in ODDS_TODAY[a]) if a < 6 else None
        e_new = sum(o / 100 * rarity(o) for o in new)
        sell_old = rarity(ODDS_TODAY[a][0]) if a < 6 else None
        line = f"    average money bonus of a 1 KG egg: "
        line += (f"x{e_old:.3f} -> x{e_new:.3f} ({100 * (e_new / e_old - 1):+.1f}%)" if e_old else f"x{e_new:.3f}")
        line += f"; egg sell value (1st pet) x{rarity(new[0]):.3f}" + (f" (was x{sell_old:.3f})" if sell_old else "")
        print(line)
    print("\nGlacier pets: $/s (raw, before rebirth/Index boosts) and pet sell value (120 s) by KG")
    for i, o in enumerate(ODDS_NEW[6]):
        r = rarity(o)
        cells = "  ".join(f"{fmt(kg):>4}: ${fmt(AREA_INCOME[6] * kg ** 0.25 * r):>6}" for kg in (1, 1000, 100_000, 1_000_000))
        print(f"  {PET_NAMES[6][i]:>22} {o:>4g}% x{r:.2f} | {cells} | sell 1 KG ${fmt(AREA_INCOME[6] * r * 120)}")
    print("  Glacier EGG sell value (60 s of Frostfang Lynx at that KG): " +
          ", ".join(f"{fmt(kg)} KG ${fmt(AREA_INCOME[6] * kg ** 0.25 * 60)}" for kg in (1, 1000, 100_000, 1_000_000, 10_000_000)))
    print("\nChance of the rarest pet per egg, by egg KG (heavy eggs are luckier):")
    for a in (3, 5, 6):
        n = ODDS_NEW[a]
        cells = "  ".join(f"{fmt(kg):>4} KG {100 * species_weights(n, kg)[-1]:.2f}%" for kg in (1, 1000, 100_000, 1_000_000, 10_000_000))
        print(f"  {PET_NAMES[a][-1]:>22}: {cells}")
    print("\nEggs to hatch until every pet of an area is found (Index claim), median of 2000 tries, 1 KG eggs / best-of-4 eggs:")
    rng = random.Random(7)
    for a in range(7):
        for label, odds in (("today", ODDS_TODAY[a] if a < 6 else None), ("new", ODDS_NEW[a])):
            if odds is None: continue
            res = []
            for kgmode in ("1kg", "best4"):
                ns = []
                for _ in range(2000):
                    seen, n = set(), 0
                    while len(seen) < len(odds) and n < 100000:
                        kg = 1 if kgmode == "1kg" else max(roll_kg(a + 1, rng) for _ in range(4))
                        w = species_weights(odds, kg)
                        x = rng.random()
                        for i, p in enumerate(w):
                            x -= p
                            if x <= 0: break
                        seen.add(i); n += 1
                    ns.append(n)
                res.append(statistics.median(ns))
            print(f"  {NAMES[a]:>9} {label:>5}: {res[0]:6.0f} / {res[1]:6.0f} eggs")


if __name__ == "__main__":
    if "--continuous" in sys.argv:
        SESSION[1] = 0
        PAYBACK_H = 96
    if "--tables" in sys.argv:
        tables()
        print()
        pets()
    elif "--tune" in sys.argv:
        tune()
    else:
        report()
        glacier_entry_probe()
