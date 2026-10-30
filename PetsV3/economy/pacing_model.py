"""SLINGSHOT economy v4 pacing model.

Simulates an engaged FREE player (no passes, no potions) to pick the numbers for the economy rework:
rebirth costs, rebirth pet requirements, treadmill tiers and slingshot prices.

The real game formulas are copied from the Roblox scripts (as of 2026-10-05):
  - pet income  = AREA_INCOME[area] * KG ** 0.25            (CreatureConfig.income)
  - egg KG roll = EggSpawner.rollWeight (normal + lucky roll)
  - hatch time  = 10 * 3 ** (0.75 * log10(KG)) seconds       (CreatureConfig.hatchSeconds)
  - walk speed  = SpeedStat curve (log10(Speed) -> WalkSpeed)
Everything about player behaviour (trip times, wave overhead, how picky they are) is an assumption,
named in ASSUME below so it is easy to see and change.

Run:  python pacing_model.py           -> prints the per-rebirth table for the chosen numbers
      python pacing_model.py --tune    -> solves rebirth costs so each run takes TARGET minutes
"""
import math
import random
import statistics
import sys

# ----------------------------------------------------------------------------- game formulas (real)
AREA_INCOME = [8, 50, 300, 1800, 10000, 55000]
KG_MAX = [30000, 60000, 100000, 200000, 300000, 500000]
KG_SKEW = [3.2, 3.0, 2.8, 2.6, 2.4, 2.2]
KG_LUCKY_ODDS = [0, 800, 600, 450, 330, 250]
KG_LUCKY_MAX = [30000, 150000, 300000, 800000, 2500000, 5000000]
AREA_NAMES = ["Grass", "Water", "Thunder", "Fire", "Shadow", "Celestial"]
CURVE = [(0, 16), (6, 30), (7, 48), (7.1, 54), (7.25, 60), (7.5, 66), (8, 74), (9, 92), (10, 115),
         (11, 140), (12, 165), (13, 190), (14, 215), (15, 240), (16, 250)]


def roll_kg(area, rng):
    a = area - 1
    odds = KG_LUCKY_ODDS[a]
    if odds > 0 and rng.randint(1, odds) == 1:
        w = min(KG_LUCKY_MAX[a], KG_MAX[a] * (1 - rng.random()) ** (-1 / 1.5))
    else:
        w = 10 ** (math.log10(KG_MAX[a]) * rng.random() ** KG_SKEW[a])
    return max(1, math.floor(w))


def income(area, kg):
    return AREA_INCOME[area - 1] * max(kg, 1) ** 0.25


def hatch_seconds(kg):
    return math.floor(10 * 3 ** (math.log10(max(kg, 1)) * 0.75) + 0.5)


def walk_speed(speed):
    x = math.log10(1 + max(speed, 0))
    for (x0, y0), (x1, y1) in zip(CURVE, CURVE[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return 250


def speed_for_walk(w):
    """inverse of walk_speed: the Speed stat that gives walk speed w"""
    for (x0, y0), (x1, y1) in zip(CURVE, CURVE[1:]):
        if w <= y1:
            return 10 ** (x0 + (x1 - x0) * (w - y0) / (y1 - y0))
    return 10 ** 16


# ----------------------------------------------------------------------------- the design (proposal)
START_SPEED = 10_000_000
BASE_SLOTS = 3                    # pet slots = BASE_SLOTS + rebirths
MULT_PER_REBIRTH = 0.25           # money and speed multiplier = 1 + 0.25 * rebirths
MAX_REBIRTH = 20

# walk speed a player needs before farming an area (outrun that area's typical waves)
AREA_WALK = [0, 58, 75, 92, 115, 141]      # Normal 55 / -- / SemiFast 90 / -- / Fast 140

# treadmill tiers: (price, speed per second at x1). Each tier is priced at ~30% of the rebirth where
# its speed becomes necessary (T2 Thunder ~R3, T3 Fire ~R5, T4 Shadow ~R8, T5 Celestial ~R12, T6 late goal)
TREADMILL = [(0, 50_000), (1_000_000, 300_000), (50_000_000, 2_000_000), (2_500_000_000, 12_000_000),
             (50_000_000_000, 75_000_000), (2_000_000_000_000, 500_000_000)]

# slingshot: level L reaches area SLING_AREA_LEVEL; price of level L = SLING_BASE * SLING_GROWTH ** (L - 1)
SLING_AREA_LEVEL = {2: 1, 3: 6, 4: 11, 5: 17, 6: 22}
SLING_BASE = 25_000
SLING_GROWTH = 1.95
SLING_MAX = 25

INDEX_BONUS = 0.05     # +5% money AND speed per completed Index area (claimed)
INDEX_TRIPS = 20       # assume an area's Index is complete after this many egg trips there
PLAYTIME_BONUS = 1.08  # playtime gifts ~ +8% income on average (cash = minutes of income)

# rebirth ladder: (cost, required area, required KG)  -- costs filled by --tune
LADDER = [  # tuned with --tune (2026-10-05), then rounded to nice numbers
    # cost,              area, kg
    (250_000,              2, 1),
    (2_000_000,            2, 1),
    (7_000_000,            3, 1),
    (50_000_000,           3, 100),
    (125_000_000,          4, 1),
    (500_000_000,          4, 100),
    (2_000_000_000,        4, 1_000),
    (5_000_000_000,        5, 1),
    (20_000_000_000,       5, 100),
    (50_000_000_000,       5, 1_000),
    (80_000_000_000,       5, 10_000),
    (250_000_000_000,      6, 1),
    (900_000_000_000,      6, 100),
    (1_500_000_000_000,    6, 1_000),
    (2_250_000_000_000,    6, 5_000),
    (3_500_000_000_000,    6, 10_000),
    (5_000_000_000_000,    6, 25_000),
    (6_500_000_000_000,    6, 50_000),
    (9_000_000_000_000,    6, 100_000),
    (14_000_000_000_000,   6, 1_000_000),
]
PAID = dict(money=1.0, speed=1.0)  # --paid: x2 Money pass, x2 Speed pass + always a x2 speed potion

TARGET_MIN = [15 * 1.22 ** i for i in range(MAX_REBIRTH)]   # minutes per run (R1 15 min ... R20 ~11 h)

# ----------------------------------------------------------------------------- player assumptions
ASSUME = dict(
    eggs_seen=4,          # player picks the heaviest of this many visible eggs per trip
    hub_overhead=10.0,    # s per trip: walk base <-> gate, place egg, grab (hold E 1.5 s)
    wave_k=40.0,          # walking time is multiplied by (1 + wave_k / walk): trench stops, detours
    flight=6.0,           # s of slingshot flight when the slingshot reaches the farm area
    train_max_min=12.0,   # player trains on the treadmill right away if it takes <= this many minutes
    buy_tread_frac=0.35,  # buys the next treadmill tier when it costs <= this share of the next rebirth
    buy_sling_frac=0.10,  # buys the next slingshot level when it costs <= this share of the next rebirth
)


def egg_distance(area, rng):
    """studs from the launch gate to a random egg spot in the area (areas are 400 studs long)"""
    return 400 * (area - 1) + rng.uniform(20, 380) + 60


class Player:
    def __init__(self, rng):
        self.rng = rng
        self.t = 0.0
        self.money = 0.0
        self.speed = START_SPEED
        self.r = 0
        self.tier = 1
        self.sling = 0
        self.pets = []           # list of [area, kg, ready_time]
        self.trips = [0] * 6     # egg trips per area (Index completion)
        self.log = []

    # ------------------------------------------------------------------ derived
    def index_mult(self):
        return 1 + INDEX_BONUS * sum(1 for n in self.trips if n >= INDEX_TRIPS)

    def mult(self):
        return (1 + MULT_PER_REBIRTH * self.r) * self.index_mult()

    def slots(self):
        return BASE_SLOTS + self.r

    def income_at(self, t):
        return sum(income(a, kg) for a, kg, ready in self.pets if ready <= t) * self.mult() * PLAYTIME_BONUS * PAID["money"]

    def tread_rate(self):
        return TREADMILL[self.tier - 1][1] * self.mult() * PAID["speed"]

    def sling_area(self):
        best = 1
        for area, lvl in SLING_AREA_LEVEL.items():
            if self.sling >= lvl:
                best = max(best, area)
        return best

    # ------------------------------------------------------------------ time passing
    def advance(self, dt):
        # pets that finish hatching inside dt start earning at their ready time
        t0, t1 = self.t, self.t + dt
        cuts = sorted({t0, t1} | {ready for _, _, ready in self.pets if t0 < ready < t1})
        for a, b in zip(cuts, cuts[1:]):
            self.money += self.income_at(a + 1e-9) * (b - a)
        self.t = t1

    def train_until(self, target_speed):
        need = max(0.0, target_speed - self.speed)
        dt = need / self.tread_rate()
        self.advance(dt)
        self.speed = max(self.speed, target_speed)
        return dt

    # ------------------------------------------------------------------ actions
    def trip(self, area):
        w = walk_speed(self.speed)
        d = egg_distance(area, self.rng)
        walk = d / w * (1 + ASSUME["wave_k"] / w)
        out = ASSUME["flight"] if self.sling_area() >= area else walk
        self.advance(out + walk + ASSUME["hub_overhead"])
        self.trips[area - 1] += 1
        kg = max(roll_kg(area, self.rng) for _ in range(ASSUME["eggs_seen"]))
        self.place(area, kg)

    def place(self, area, kg):
        new_income = income(area, kg)
        ready = self.t + hatch_seconds(kg)
        if len(self.pets) < self.slots():
            self.pets.append([area, kg, ready])
            return
        worst = min(range(len(self.pets)), key=lambda i: income(self.pets[i][0], self.pets[i][1]))
        if new_income > income(self.pets[worst][0], self.pets[worst][1]) * 1.05:
            self.pets[worst] = [area, kg, ready]
        # (a worse egg would be sold; ignored)

    def has_pet(self, area, kg):
        return any(a == area and k >= kg for a, k, _ in self.pets)

    def best_area_allowed(self):
        w = walk_speed(self.speed)
        best = 1
        for a in range(1, 7):
            if w >= AREA_WALK[a - 1]:
                best = a
        return best

    def run_rebirth(self, cost, req_area, req_kg, max_seconds=60 * 3600):
        start = self.t
        need_walk = AREA_WALK[req_area - 1]
        need_speed = speed_for_walk(need_walk)
        while self.t - start < max_seconds:
            # rebirth as soon as possible
            if self.money >= cost and self.has_pet(req_area, req_kg):
                self.money = 0.0
                self.speed = START_SPEED
                self.r += 1
                return self.t - start
            # shopping: treadmill tier (cheap enough, or needed because training would take too long),
            # then slingshot level
            if self.tier < len(TREADMILL):
                price = TREADMILL[self.tier][0]
                slow = self.speed < need_speed and \
                    (need_speed - self.speed) / self.tread_rate() / 60 > ASSUME["train_max_min"]
                if self.money >= price and (price <= ASSUME["buy_tread_frac"] * cost or slow):
                    self.money -= price
                    self.tier += 1
                    continue
            if self.sling < SLING_MAX:
                price = SLING_BASE * SLING_GROWTH ** self.sling
                if self.money >= price and price <= ASSUME["buy_sling_frac"] * cost:
                    self.money -= price
                    self.sling += 1
                    continue
            # speed: train for the required area if it doesn't take too long
            if self.speed < need_speed:
                minutes = (need_speed - self.speed) / self.tread_rate() / 60
                if minutes <= ASSUME["train_max_min"]:
                    self.train_until(need_speed)
                    continue
            # farm the best area we can safely reach (never past the required one)
            area = min(self.best_area_allowed(), req_area)
            # if we are stuck below the required area, mix in some training
            if area < req_area and self.speed < need_speed:
                self.advance(0)  # no-op, keeps structure readable
                self.train_until(min(need_speed, self.speed + self.tread_rate() * 120))
            self.trip(area)
        return None


def simulate(seed, ladder=LADDER, upto=MAX_REBIRTH):
    rng = random.Random(seed)
    p = Player(rng)
    times = []
    for r in range(upto):
        cost, area, kg = ladder[r]
        dt = p.run_rebirth(cost, area, kg)
        if dt is None:
            times.append(float("inf"))
            break
        times.append(dt)
    return times, p


def median_times(ladder, seeds=60, upto=MAX_REBIRTH):
    runs = [simulate(s, ladder, upto)[0] for s in range(seeds)]
    out = []
    for i in range(upto):
        vals = [r[i] for r in runs if len(r) > i]
        out.append(statistics.median(vals) if vals else float("inf"))
    return out


def nice(n):
    if n < 100:
        return round(n)
    p = 10 ** (math.floor(math.log10(n)) - 1)
    return round(n / p) * p


def tune(seeds=40):
    """Solve each rebirth cost (in order) so that the median run takes TARGET_MIN minutes.
    Player states are kept between rebirths, so each step only simulates one run per seed."""
    import copy
    ladder = [list(x) for x in LADDER]
    states = [Player(random.Random(s)) for s in range(seeds)]
    for i in range(MAX_REBIRTH):
        _, area, kg = ladder[i]
        lo, hi = 1e3, 1e16
        for _ in range(26):
            mid = math.sqrt(lo * hi)
            times = []
            for st in states:
                p = copy.deepcopy(st)
                dt = p.run_rebirth(mid, area, kg)
                times.append(dt if dt is not None else float("inf"))
            if statistics.median(times) / 60 < TARGET_MIN[i]:
                lo = mid
            else:
                hi = mid
        ladder[i][0] = nice(math.sqrt(lo * hi))
        for st in states:
            st.run_rebirth(ladder[i][0], area, kg)
        p0 = states[0]
        print(f"R{i + 1}: cost ${fmt(ladder[i][0])}  target {TARGET_MIN[i]:.0f} min  | seed0 after: tier {p0.tier} "
              f"sling {p0.sling} income/s {fmt(p0.income_at(p0.t + 1e9))}", flush=True)
    return [tuple(x) for x in ladder]


def fmt(n):
    for unit, v in [("Qa", 1e15), ("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)]:
        if n >= v:
            return f"{n / v:.3g}{unit}"
    return f"{n:.0f}"


def report(ladder, seeds=60):
    med = median_times(ladder, seeds)
    total = 0
    print(f"{'R':>3} {'cost':>9} {'needs':>18} {'run':>8} {'total':>8}")
    for i, (cost, area, kg) in enumerate(ladder):
        total += med[i]
        need = f"{AREA_NAMES[area - 1]} >= {fmt(kg)}KG"
        print(f"{i + 1:>3} {fmt(cost):>9} {need:>18} {med[i] / 60:7.1f}m {total / 3600:7.1f}h")
    _, p = simulate(0, ladder)
    print(f"seed 0 end: tier {p.tier}, sling {p.sling}, speed {fmt(p.speed)}, pets {len(p.pets)}")


if __name__ == "__main__":
    if "--paid" in sys.argv:
        PAID["money"], PAID["speed"] = 2.0, 4.0
    if "--tune" in sys.argv:
        tuned = tune()
        print()
        report(tuned)
    else:
        report(LADDER)
