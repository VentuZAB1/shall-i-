"""SLINGSHOT water wall sim (2026-10-27, engagement fix 2): when does a brand-new player first reach WATER?

Greedy new player from the moment they join, launch by launch (not the old per-trip abstraction):
  * every launch is a real shot: height + power from an aim-skill model, landing from the real flight loop
    (egg_run_probe.land_z = SlingshotClient), Water starts at z -460
  * the tutorial as it is today: intro, free Slingshot Power Lv1 after the first hatch, 10 s tutorial eggs until then,
    step 10 buys the next level with money, step 11 = Rebirth 1 ($25K, money only)
  * money: pets in the base (3 + rebirths slots) earn AREA_INCOME x KG^0.25 x rarity x (1 + 0.25 R); eggs hatch in
    max(10, 32400 x AREA_HATCH x (KG/200K)^0.43) s; full slots -> replace the worst pet / sell (60 s / 120 s of income)
  * shopping: next Slingshot Power level as soon as it's affordable and unlocked (Lv4+ needs R1, Lv6+ R2), rebirth as
    soon as the money (and for R2 a Water pet) is there
Calibration: today's sim is held against the live data (Area Ladder: 33% of Grass egg grabbers ever grab a Water egg;
first session: 80% still playing at 1:40, 44% at 5 min, 20% at 10 min). P(Water) = E[S(T_water)] / E[S(T_grass)].
Run: python water_wall_sim.py
"""
import math, random, statistics, sys
import egg_run_probe as fx

AREA_INCOME = [20, 120]
AREA_HATCH = [0.02, 0.04]
ODDS = {1: [52, 28, 13, 5, 2], 2: [53, 27, 13, 5.5, 1.5]}
WATER_Z = -460
WALK = 48.0

def rarity(rng, area):
    odds = ODDS[area]
    r = rng.random() * sum(odds)
    for o in odds:
        r -= o
        if r <= 0:
            return max(1.0, (50 / o) ** 0.35)
    return 1.0

def income(area, kg, rar, rebirths):
    return AREA_INCOME[area - 1] * max(kg, 1) ** 0.25 * rar * (1 + 0.25 * rebirths)

def hatch_s(area, kg):
    return max(10.0, 32400 * AREA_HATCH[area - 1] * (kg / 200000) ** 0.43)

def nice(n):
    if n < 100: return math.floor(n)
    p = 10 ** (math.floor(math.log10(n)) - 1)
    return math.floor(n / p + 0.5) * p

# ------------------------------------------------------------------ the knobs a proposal can turn
def today():
    return dict(
        sling_cost=lambda L: nice(min(500 * 2.6 ** (L - 1), 25000 * 1.95 ** (L - 1))),
        sling_rebirth=[0, 0, 0, 1, 1, 2, 2, 2, 3, 3],
        sling_speed=fx.sling_speed,          # max launch speed per level (UpgradeConfig)
        r1=25_000, r2=1_200_000,
        near_miss=False,                      # the near-miss banner (behaviour effect, see shoot())
        assist=True,                          # fix 1 (built): the first 3 egg runs always come home with an egg
    )

# ------------------------------------------------------------------ aim skill (ASSUMPTION, calibrated below)
SKILL = dict(h0=0.22, h1=0.12, t0=0.35, t1=0.20, tau=6.0)  # calibrated 2026-10-27
# real players are slower than a bot: walking around, reading, menus. SLOW multiplies every non-physics wait,
# IDLE is extra seconds per launch cycle. Both calibrated to the onboarding funnel (see calibrate()).
PACE = dict(slow=3.0, idle=20.0)  # calibrated 2026-10-27: free upgrade 4.7 min, Lv2 5.5, Water egg 8.6, ladder 36%

def shoot(rng, n, cfg, nudge):
    k = math.exp(-n / SKILL["tau"])
    sh = SKILL["h1"] + (SKILL["h0"] - SKILL["h1"]) * k
    st = SKILL["t1"] + (SKILL["t0"] - SKILL["t1"]) * k
    if nudge:      # the banner right after a near miss: "hold to the top" -> this shot's power error shrinks
        st *= 0.7
    h = min(1, max(0, rng.gauss(0.5, sh)))
    p = max(0.0, min(1.0, 1 - abs(rng.gauss(0, st))))
    return h, p

class Player:
    def __init__(self, rng, cfg):
        self.rng, self.cfg = rng, cfg
        self.t = 0.0
        self.money = 0.0
        self.sling = 0
        self.r = 0
        self.pets = []          # [area, kg, rar, ready_at]
        self.launches = 0
        self.grabs = 0
        self.assists_left = 3 if cfg["assist"] else 0
        self.free_sling = True  # the tutorial's free Lv1 waits
        self.first_hatch_at = None
        self.ms = {}            # milestone -> minute
        self.near = False
        self.short = []

    def act(self, dt):          # a human action (walking, reading, menus): slowed by PACE
        self.wait(dt * PACE["slow"])

    # money ticks while time passes
    def wait(self, dt):
        t0, t1 = self.t, self.t + dt
        cuts = sorted({t0, t1} | {p[3] for p in self.pets if t0 < p[3] < t1})
        for a, b in zip(cuts, cuts[1:]):
            rate = sum(income(p[0], p[1], p[2], self.r) for p in self.pets if p[3] <= a + 1e-9)
            self.money += rate * (b - a)
        self.t = t1

    def mark(self, what):
        self.ms.setdefault(what, self.t / 60)

    def slots(self):
        return 3 + self.r

    def place(self, area, kg):
        rar = rarity(self.rng, area)
        tut = self.free_sling     # tutorial eggs: 10 s until the free upgrade is taken
        ready = self.t + (10.0 if tut else hatch_s(area, kg))
        new_inc = income(area, kg, rar, 0)
        if len(self.pets) < self.slots():
            self.pets.append([area, kg, rar, ready])
            return
        worst = min(range(len(self.pets)), key=lambda i: income(*self.pets[i][:3], 0))
        w = self.pets[worst]
        if new_inc > income(w[0], w[1], w[2], 0) * 1.05:
            self.money += income(w[0], w[1], w[2], 0) * 120
            self.pets[worst] = [area, kg, rar, ready]
        else:
            self.money += AREA_INCOME[area - 1] * max(kg, 1) ** 0.25 * 60

    def shop(self):
        c = self.cfg
        while True:
            nxt = self.sling + 1
            if nxt < len(c["sling_rebirth"]) + 1 and self.r >= c["sling_rebirth"][nxt - 1] and self.money >= c["sling_cost"](nxt) \
                    and not self.free_sling:
                self.money -= c["sling_cost"](nxt)
                self.sling = nxt
                self.mark(f"Sling Lv{nxt}")
                self.act(3)
                continue
            if self.r == 0 and self.money >= c["r1"]:
                self.rebirth(); continue
            if self.r == 1 and self.money >= c["r2"] and any(p[0] == 2 and p[3] <= self.t for p in self.pets):
                self.rebirth(); continue
            break

    def rebirth(self):
        self.money = 0.0
        self.r += 1
        self.mark(f"Rebirth {self.r}")
        self.act(6)

    def launch(self):
        rng = self.rng
        self.wait(PACE["idle"])
        self.act(3.0)   # board + lock the arc + hold to pull
        h, p = shoot(rng, self.launches, self.cfg, self.near)
        self.launches += 1
        lv = self.sling
        z, flight = fx.land_z(h, p, lv, vmax=self.cfg["sling_speed"](lv))
        self.wait(flight)
        area = 2 if z <= WATER_Z else 1
        miss = WATER_Z - z if area == 1 else None     # studs short of Water (negative = short)
        # the near-miss banner: landed short of Water by at most 25% of the distance to it (~105 studs)
        self.near = area == 1 and self.cfg["near_miss"] and 0 < z - WATER_Z <= 0.25 * abs(WATER_Z - fx.REST[2])
        if area == 2:
            self.mark("Water landing")
            self.ms.setdefault("water_level", lv)
        else:
            self.short.append(WATER_Z - z)   # studs short of Water (negative)
        # grab
        assisted = self.assists_left > 0 or (area == 2 and self.cfg.get("assist_new_area") and "Water egg" not in self.ms)
        if assisted:
            self.wait(1.3)
            ok = True
        else:
            eggs = [fx.spawn_egg(area, rng) for _ in range(7 if area == 1 else 6)]
            d = min(math.hypot(e[0] - 0.5, e[1] - z) for e in eggs)
            self.act(1.5 + max(0.0, d - 10) / WALK)
            self.wait(1.5)
            fail = 0.25 if self.grabs < 6 else 0.16       # waves before the grab (probe ~28%, veterans dodge)
            ok = rng.random() > fail
        if not ok:
            self.act(4 + 3 + 10)       # knocked out, respawn, walk back to the pad
            return
        self.grabs += 1
        if assisted and self.assists_left > 0:
            self.assists_left -= 1
        if area == 2:
            self.mark("Water egg")
        self.mark("first egg")
        kg = fx.roll_kg(area, rng)
        # carry home: walk + wave dodging (pacing_model wave_k: x(1 + 40/48))
        self.act((abs(z) - 60) / WALK * (1 + 40 / WALK))
        if rng.random() < 0.07 and self.grabs > 1:      # knocked out on the way home (tutorial run is scripted)
            self.act(3 + 10)
            return
        self.act(12)                                   # bank, walk into the base, place
        self.place(area, kg)
        if self.first_hatch_at is None:
            self.first_hatch_at = self.pets[-1][3] if self.pets else self.t
        self.act(8)                                    # back to the pad (shopping on the way)

    def tutorial_upgrade(self):
        if self.free_sling and self.first_hatch_at is not None:
            if self.t < self.first_hatch_at:
                self.wait(self.first_hatch_at - self.t)      # watch it hatch (step 8)
            self.act(12)                                    # walk to the Upgrade stall, FREE
            self.sling = 1
            self.free_sling = False
            self.mark("Sling Lv1 (free)")
            self.act(15)                                    # step 9: treadmill 5 s + walking

def run(cfg, seed, minutes=40):
    rng = random.Random(seed)
    pl = Player(rng, cfg)
    pl.act(35)            # load + intro cutscene
    pl.act(8)             # walk to the slingshot
    while pl.t < minutes * 60:
        pl.launch()
        pl.tutorial_upgrade()
        pl.shop()
    return pl.ms

SURV = [(0, 1.0), (1.67, 0.80), (5, 0.44), (10, 0.20), (15, 0.12), (20, 0.08), (30, 0.05), (60, 0.02)]
def survival(m):
    if m is None: return 0.0
    for (a, sa), (b, sb) in zip(SURV, SURV[1:]):
        if m <= b:
            return sa + (sb - sa) * (m - a) / (b - a)
    return 0.02

def summary(cfg, seeds=400, minutes=60):
    rows = [run(cfg, s, minutes) for s in range(seeds)]
    def med(key):
        v = [r.get(key, float("inf")) for r in rows]
        m = statistics.median(v)
        return m
    reach = statistics.mean(survival(r.get("Water egg")) for r in rows) / statistics.mean(survival(r.get("first egg")) for r in rows)
    return dict(water_land=med("Water landing"), water_egg=med("Water egg"), lv2=med("Sling Lv2"), lv3=med("Sling Lv3"),
                r1=med("Rebirth 1"), r2=med("Rebirth 2"), reach=reach, rows=rows)

def fmt(m):
    return " >60" if m == float("inf") else f"{m:5.1f}"

def table(label, s):
    print(f"{label:44} {fmt(s['lv2'])} {fmt(s['lv3'])} {fmt(s['water_land'])} {fmt(s['water_egg'])} {fmt(s['r1'])} {fmt(s['r2'])}   {100 * s['reach']:4.0f}%")

HEAD = f"{'(median minute since joining)':44} {'Lv2':>5} {'Lv3':>5} {'Water':>5} {'WEgg':>5} {'R1':>5} {'R2':>5}  Water ladder"

# ------------------------------------------------------------------ proposals
RANGE = lambda L: fx.BASE_RANGE + (2300 - fx.BASE_RANGE) * L / 25        # UpgradeConfig.slingRange
def with_range_bonus(cfg, bonus):
    cfg["sling_speed"] = lambda L: fx.BASE_MAX if L <= 0 else fx.speed_for(RANGE(L) + bonus.get(L, 0))
    return cfg
def with_prices(cfg, over):
    old = cfg["sling_cost"]
    cfg["sling_cost"] = lambda L: over.get(L, old(L))
    return cfg

PRICES = {2: 600, 3: 1500}                       # Lv2 $1.3K -> $600, Lv3 $3.4K -> $1.5K
BONUS = {1: 30, 2: 35, 3: 30, 4: 15}             # studs of extra range, Lv5+ unchanged (Thunder stays Lv6)

def proposals():
    out = [("TODAY (fix 1 built)", today())]
    out.append(("A  Lv2 $600 + Lv3 $1.5K", with_prices(today(), PRICES)))
    out.append(("B  Lv1-4 range +30/+35/+30/+15", with_range_bonus(today(), BONUS)))
    out.append(("A + B", with_range_bonus(with_prices(today(), PRICES), BONUS)))
    c = with_range_bonus(with_prices(today(), PRICES), BONUS); c["near_miss"] = True
    out.append(("A + B + near-miss banner (assumed effect)", c))
    c = today(); c["near_miss"] = True
    out.append(("near-miss banner only (assumed effect)", c))
    c = with_range_bonus(with_prices(today(), PRICES), BONUS); c["near_miss"] = True; c["assist_new_area"] = True
    out.append(("A + B + banner + C first-Water egg assist", c))
    return out

def water_chance(cfg, level, n=15000, seed=9):
    rng = random.Random(seed)
    hit = near = 0
    for _ in range(n):
        h, p = shoot(rng, 6, cfg, False)
        z = fx.land_z(h, p, level, vmax=cfg["sling_speed"](level))[0]
        if z <= WATER_Z: hit += 1
        elif z - WATER_Z <= 0.25 * abs(WATER_Z - fx.REST[2]): near += 1
    return hit / n, near / n

if __name__ == "__main__":
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    print("Slingshot Power per level (learned aim, 6th launch): range studs / P(lands in Water) / P(near miss <= 105 studs short)")
    for label, cfg in (("today", today()), ("B", with_range_bonus(today(), BONUS))):
        cells = []
        for L in range(0, 6):
            a, b = water_chance(cfg, L)
            cells.append(f"Lv{L} {RANGE(L) + (BONUS.get(L, 0) if label == 'B' and L > 0 else 0):4.0f} {100 * a:3.0f}%/{100 * b:2.0f}%")
        print(f"  {label:6}", "  ".join(cells))
    print()
    print(HEAD + "   Water egg 25%..75%, by 10 min")
    for label, cfg in proposals():
        s = summary(cfg, seeds)
        v = sorted(r.get("Water egg", 99) for r in s["rows"])
        by10 = 100 * sum(1 for x in v if x <= 10) / len(v)
        print(f"{label:44} {fmt(s['lv2'])} {fmt(s['lv3'])} {fmt(s['water_land'])} {fmt(s['water_egg'])} {fmt(s['r1'])} {fmt(s['r2'])}   "
              f"{100 * s['reach']:4.0f}%      {v[len(v) // 4]:4.1f}..{v[3 * len(v) // 4]:4.1f}, {by10:3.0f}%")
