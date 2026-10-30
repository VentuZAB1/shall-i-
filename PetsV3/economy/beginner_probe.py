"""How long until a NEW player can afford the first purchases (current v4 numbers)?
Player: tutorial done (Sling Lv1 free -> Water reachable), trains to Water walk speed first, then farms Water,
never buys anything; we just record when money first reaches each price."""
import random, statistics, sys
import pacing_model as pm

PRICES = [("Sling Lv2", 49_000), ("Rebirth 1", 250_000), ("Sling Lv5", 360_000), ("Treadmill x6", 1_000_000)]

def probe(eggs_seen, seeds=80, horizon=4 * 3600):
    pm.ASSUME["eggs_seen"] = eggs_seen
    res = {n: [] for n, _ in PRICES}
    inc10 = []
    for s in range(seeds):
        p = pm.Player(random.Random(s))
        p.sling = 1
        need = pm.speed_for_walk(pm.AREA_WALK[1])
        p.train_until(need)
        hit = {}
        t_inc = None
        while p.t < horizon and len(hit) < len(PRICES):
            p.trip(2)
            for n, price in PRICES:
                if n not in hit and p.money >= price:
                    hit[n] = p.t
            if t_inc is None and p.t >= 600:
                t_inc = p.income_at(p.t)
        for n, _ in PRICES:
            res[n].append(hit.get(n, float("inf")))
        inc10.append(t_inc or 0)
    print(f"eggs_seen={eggs_seen}: income/s at 10 min median ${statistics.median(inc10):,.0f}")
    for n, price in PRICES:
        print(f"   {n:13s} ${price:>9,}  reached after {statistics.median(res[n]) / 60:6.1f} min (median)")

for k in (1, 2, 4):
    probe(k)
