import math, sys
import hub_layout as H
S = H.solids()
def clearance(c):
    if not H.on_ground(c): return -1
    d = 99.0
    for pid in H.PLOTS:
        pr = H.plot_rect(pid, 60, 90)
        if H.point_in_poly(c, pr): return -1
        d = min(d, min(H.seg_dist(c, *e) for e in H.poly_edges(pr)))
    for pid, kind, a, b, half in H.lines():
        d = min(d, H.seg_dist(c, a, b) - half)
    for n, poly in S.items():
        if H.point_in_poly(c, poly): return -1
        d = min(d, min(H.seg_dist(c, *e) for e in H.poly_edges(poly)) - 1.5)
    for n,(rc, rr) in H.RINGS.items(): d = min(d, math.dist(c, rc) - rr - 2)
    d = min(d, math.dist(c, H.MEDALLION['centre']) - H.MEDALLION['radius'])
    for x0,z0,x1,z1 in (H.LAUNCH_ZONE, H.INTRO_ZONE):
        dx = max(x0 - c[0], 0, c[0] - x1); dz = max(z0 - c[1], 0, c[1] - z1)
        d = min(d, math.hypot(dx, dz))
    for k in range(16):
        a = 2*math.pi*k/16
        for r in (1, 2, 3, 4, 5, 6, 8):
            if not H.on_ground((c[0]+r*math.cos(a), c[1]+r*math.sin(a))): d = min(d, r - 1); break
    return d
pts = []
for x in range(-214, 1, 2):
    for z in range(-60, 172, 2):
        c = (float(x), float(z)); cl = clearance(c)
        if cl >= float(sys.argv[1] if len(sys.argv) > 1 else 3): pts.append((cl, c))
pts.sort(reverse=True)
chosen = []
for cl, c in pts:
    if all(math.dist(c, q) > 12 for _, q in chosen): chosen.append((cl, c))
for cl, c in chosen[:30]: print('clear %.1f at (%.0f, %.0f)' % (cl, c[0], c[1]))
