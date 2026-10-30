"""SLINGSHOT Egg Run probe (2026-10-27, engagement fix 1): why do 19.5% of launches end with no egg?

Copies the real launch / landing / egg-spawn / wave rules from the Studio scripts:
  * SlingshotClient + SlingshotServer: angle = 15 + 60h deg, speed = 55 + (max - 55)p, rider starts at the pouch
    (PouchRest + dir * (3 - pull)), pull = 0.9 + 7.1p, flight gravity 196.2 * 0.4, landing = the client's ray
    (4.5 + fall/30 studs) hits the floor, then the root is put 3 studs above the hit. Everyone lands on x = 0.5.
  * UpgradeConfig: max speed per Slingshot Power level (range 370 -> 2300 linear over 25 levels).
  * EggSpawner: 6 eggs per area, 60 s life, |x| in [7 + r/2, 42], z on the two floors minus a 10-stud end margin,
    prompt reach 8 + 3 * size, hold 1.5 s, KG roll per area.
  * WaveServer: the spawn rhythm (gaps 6-11 s, combos 16%, chasers 12%, calms 10%) -> how often a wave passes a spot.
Player behaviour (aim skill, look-around time) is an ASSUMPTION, named in SKILL / FIND below.
Run: python egg_run_probe.py
"""
import math, random, statistics

G = 196.2 * 0.4
REST = (0.53, 25.31, -39.87)
MIN_SPEED, BASE_MAX = 55, 165
WALK = 48                      # Speed 0 walk speed (SpeedStat offset)
HOLD = 1.5

# ------------------------------------------------------------------ UpgradeConfig
def range_of(v, h=25):
    c = v * math.cos(math.radians(45))
    return c / G * (c + math.sqrt(c * c + 2 * G * h))

def speed_for(rng_):
    lo, hi = 1, 2000
    for _ in range(60):
        mid = (lo + hi) / 2
        if range_of(mid) < rng_: lo = mid
        else: hi = mid
    return (lo + hi) / 2

BASE_RANGE = range_of(BASE_MAX)
def sling_speed(level):
    if level <= 0: return BASE_MAX
    return speed_for(BASE_RANGE + (2300 - BASE_RANGE) * min(level, 25) / 25)

# ------------------------------------------------------------------ the real flight (client loop, 60 Hz)
def land_z(h, p, level, floor_y=0.0, vmax=None):
    ang = math.radians(15 + 60 * h)
    dy, dz = math.sin(ang), -math.cos(ang)
    pull = 0.9 + 7.1 * p
    y = REST[1] + dy * (3 - pull)
    z = REST[2] + dz * (3 - pull)
    sp = MIN_SPEED + ((vmax or sling_speed(level)) - MIN_SPEED) * p
    vy, vz = sp * dy, sp * dz
    t, dt = 0.0, 1 / 60
    while t < 25:
        t += dt
        vy -= G * dt
        y += vy * dt
        z += vz * dt
        if t > 0.35 and vy <= 2:
            reach = 4.5 + max(0, -vy) / 30
            if y - floor_y <= reach:
                return z, t
    return z, t

# ------------------------------------------------------------------ eggs (EggSpawner)
KG_MAX = [30000, 60000]
KG_SKEW = [3.2, 3.0]
def roll_kg(area, rng):
    return max(1, math.floor(10 ** (math.log10(KG_MAX[area - 1]) * rng.random() ** KG_SKEW[area - 1])))

def egg_height(kg):
    pts = [(0, 3), (3, 6), (4, 10), (math.log10(50000), 14), (5, 16), (6, 24)]
    x = math.log10(max(1, kg))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return 24

FLOORS = {1: [-157, -363], 2: [-557, -763]}   # floor centres (z), 194 long
def spawn_egg(area, rng):
    kg = roll_kg(area, rng)
    r = egg_height(kg) * 0.3
    c = rng.choice(FLOORS[area])
    half = 97 - max(10, r)
    lo, hi = 7 + r * 0.5, max(7 + r * 0.5, min(42, 56 - r))
    x = (lo + rng.random() * (hi - lo)) * rng.choice((1, -1))
    z = c + (rng.random() * 2 - 1) * half
    size = egg_height(kg) / 6
    return x, z, 8 + 3 * size

# ------------------------------------------------------------------ aim skill (ASSUMPTION)
# height: the player locks the sweeping arc near 45 deg with a normal error; power: lets go near the peak of a 2 s
# sweep (1 s up, 1 s down) with a timing error in seconds. New = first runs, Learned = after ~10 launches.
SKILL = {"new": (0.22, 0.30), "learned": (0.14, 0.15)}
def shot(rng, skill):
    sh, st = SKILL[skill]
    h = min(1, max(0, rng.gauss(0.5, sh)))
    t = rng.gauss(1.0, st)
    p = max(0.0, min(1.0, 1 - abs(t - 1)))
    return h, p

FIND = 1.0      # s to spot the egg + turn after landing (ASSUMPTION)

# ------------------------------------------------------------------ waves (WaveServer rhythm)
def wave_rate(seconds=200000, seed=1):
    rng = random.Random(seed)
    t, n = 0.0, 0
    while t < seconds:
        r = rng.random()
        if r < 0.16:
            n += 2; t += rng.uniform(1, 2.5) + rng.uniform(6, 11) + 3
        elif r < 0.28:
            n += 2; t += rng.uniform(4, 8) + rng.uniform(6, 11) + 3
        else:
            n += 1
            ultra = rng.random() < 6 / 112
            t += (3 if ultra else 0) + rng.uniform(6, 11) + (6 if ultra else 0)
        if rng.random() < 0.1: t += rng.uniform(15, 20)
    return n / t

def main(n=40000, seed=7):
    rng = random.Random(seed)
    rate = wave_rate()
    print(f"waves passing any runway spot: one every {1 / rate:.1f} s on average\n")
    for level in (0, 1):
        for skill in ("new", "learned"):
            zs, near, reach0, t_grab, p_wave, short_gate, in_water = [], [], 0, [], [], 0, 0
            for _ in range(n):
                h, p = shot(rng, skill)
                z, _ = land_z(h, p, level)
                zs.append(z)
                area = 1 if z > -460 else 2
                if z <= -460: in_water += 1
                if z > -75: short_gate += 1
                eggs = [spawn_egg(area, rng) for _ in range(6)]
                best = min(eggs, key=lambda e: math.hypot(e[0] - 0.5, e[1] - z))
                d = math.hypot(best[0] - 0.5, best[1] - z)
                near.append(d)
                if d <= best[2]: reach0 += 1
                walk = max(0.0, d - best[2] + 1.5) / WALK
                tg = FIND + walk + HOLD
                t_grab.append(tg)
                p_wave.append(1 - math.exp(-rate * tg))
            q = statistics.quantiles(near, n=10)
            print(f"Sling Lv{level}, {skill:7} aim: land z median {statistics.median(zs):6.0f} "
                  f"(10%..90% {statistics.quantiles(zs, n=10)[0]:5.0f}..{statistics.quantiles(zs, n=10)[-1]:5.0f}); "
                  f"lands <15 studs past the gate {100 * short_gate / n:4.1f}%, in Water {100 * in_water / n:4.1f}%")
            print(f"    nearest egg: median {statistics.median(near):5.1f} studs, 90% {q[-1]:5.1f}; "
                  f"already in prompt reach on landing {100 * reach0 / n:4.1f}%; "
                  f"time to grab median {statistics.median(t_grab):4.1f} s; "
                  f"P(a wave passes before the grab) {100 * statistics.mean(p_wave):4.1f}%")
    # the assist: an egg next to the landing point, in reach at once (reach 14), hold 1.5 s / 0.9 s
    for hold in (1.5, 0.9):
        tg = 0.4 + hold
        print(f"\nASSIST egg in reach at landing, hold {hold} s: time to grab {tg:.1f} s, "
              f"P(wave first) {100 * (1 - math.exp(-rate * tg)):4.1f}% (0% with a {tg + 0.6:.1f} s landing grace)")

if __name__ == "__main__":
    main()


# ------------------------------------------------------------------ Grass density options (fix 1, part 2)
def spawn_egg_opt(area, rng, gate_margin):
    """EggSpawner.pickSpot with a bigger margin at the GATE end of Grass FloorA only (z -60 is the gate)"""
    while True:
        x, z, reach = spawn_egg(area, rng)
        if area != 1 or z <= -60 - gate_margin:
            return x, z, reach

def density(n=30000, seed=11):
    rng = random.Random(seed)
    rate = wave_rate()
    print("\nGrass egg density near early landings (Lv0 + Lv1, new + learned aim mixed):")
    for label, eggs, margin in (("today: 6 eggs, 10-stud gate margin", 6, 10),
                                ("7 eggs", 7, 10),
                                ("6 eggs, 80-stud gate margin", 6, 80),
                                ("7 eggs, 80-stud gate margin", 7, 80)):
        near, within, risk = [], 0, []
        for i in range(n):
            level, skill = i % 2, ("new", "learned")[(i // 2) % 2]
            h, p = shot(rng, skill)
            z, _ = land_z(h, p, level)
            if z <= -460:
                continue
            es = [spawn_egg_opt(1, rng, margin) for _ in range(eggs)]
            best = min(es, key=lambda e: math.hypot(e[0] - 0.5, e[1] - z))
            d = math.hypot(best[0] - 0.5, best[1] - z)
            near.append(d)
            within += d <= 25
            tg = FIND + max(0.0, d - best[2] + 1.5) / WALK + HOLD
            risk.append(1 - math.exp(-rate * tg))
        print(f"  {label:38} nearest egg median {statistics.median(near):5.1f} studs, 90% {statistics.quantiles(near, n=10)[-1]:5.1f}, "
              f"egg within 25 studs {100 * within / len(near):4.1f}%, P(wave before grab) {100 * statistics.mean(risk):4.1f}%")

if __name__ == "__main__":
    density()
