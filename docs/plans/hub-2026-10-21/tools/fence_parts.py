"""Part count of one plot built by BaseBuilder (same maths) for every rebirth size: old 64x80 vs new 60x90."""
import math
S = 3.2
D = dict(postW=0.22*S, inset=0.30*S, picW=0.141*S, picPitch=0.235*S, postPitch=1.16*S, gateW=1.38*S)
RANCH = {0: True, 1: True, 2: False, 3: False, 4: False, 5: True}

def size(r, mw, ml):
    t = min(r, 5) / 5
    return math.floor(40 + (mw - 40) * t + 0.5), math.floor(40 + (ml - 40) * t + 0.5)

def count(w, l, ranch):
    hx, hz = w / 2 - D["inset"], l / 2 - D["inset"]
    gx = D["gateW"] / 2 + D["postW"] / 2
    lines = [((-hx, hz), (hx, hz)), ((-hx, -hz), (-hx, hz)), ((hx, -hz), (hx, hz)), ((-hx, -hz), (-gx, -hz)), ((gx, -hz), (hx, -hz))]
    parts, posts = 0, set()
    for a, b in lines:
        L = math.dist(a, b)
        n = max(1, math.floor(L / D["postPitch"] + 0.5))
        pts = [(a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n) for i in range(n + 1)]
        for i in range(n):
            ln = math.dist(pts[i], pts[i + 1])
            clear = ln - D["postW"]
            parts += 2 + 1  # rails + collider
            if ranch:
                parts += 2
            else:
                parts += 2 * max(1, math.floor(clear / D["picPitch"]))
        for p in pts:
            posts.add((round(p[0], 2), round(p[1], 2)))
    parts += 2 * len(posts) + 15 + 1  # posts+caps, gate door, floor
    return parts

for label, mw, ml in (("OLD 64x80", 64, 80), ("NEW 60x90", 60, 90)):
    row = []
    for r in range(6):
        w, l = size(r, mw, ml)
        row.append(f"R{r} {w}x{l}: {count(w, l, RANCH[r])}")
    print(label, " | ".join(row))
