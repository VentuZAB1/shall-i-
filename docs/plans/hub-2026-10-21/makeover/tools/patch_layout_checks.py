"""Second one-shot patch of ../../tools/hub_layout.py (the rule checks) for the hub makeover (2026-10-21 night)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "tools", "hub_layout.py")
s = open(P, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:70], n)
    s = s.replace(old, new)


# 4: intro zone exemption for the owner-placed front boards + measured-camera clearance for every solid
rep('''    for n, poly in S.items():
        bad = poly_dist(poly, rect_xz(LAUNCH_ZONE)) < 2 or poly_dist(poly, rect_xz(INTRO_ZONE)) < 0.5 or any(v[1] < -60 for v in poly)
        if bad:
            rep(False, f"{n} touches the launch zone / intro corridor / runway")
    rep(True, "launch zone + intro corridor + runway line checked against every solid")''',
    '''    for n, poly in S.items():
        in_intro = poly_dist(poly, rect_xz(INTRO_ZONE)) < 0.5 and n not in INTRO_EXEMPT
        bad = poly_dist(poly, rect_xz(LAUNCH_ZONE)) < 2 or in_intro or any(v[1] < -60 for v in poly)
        if bad:
            rep(False, f"{n} touches the launch zone / intro corridor / runway")
        cam = min(min(math.dist(c, v) for v in poly) if not point_in_poly(c, poly) else 0.0 for c in INTRO_CAMS)
        if cam < 3.0:
            rep(False, f"{n} only {cam:.1f} from an IntroCutscene camera (>= 3)")
    rep(True, "launch zone + intro corridor (+ measured intro cameras, owner-placed front boards exempt) + runway line checked")''')

# 7: stall rings are owner-placed at the front corners (on the gate-edge fan lines by necessity): they must lie fully on
# their own deck instead; the Free Gift ring keeps the old clearance rule
rep('''    for rn, (c, r) in RINGS.items():
        worst = min(seg_dist(c, a, b) - r - half for _, _, a, b, half in lines())
        rep(worst >= 0, f"{rn}: clearance to the nearest walking line {worst:.1f} (>= 0)")''',
    '''    for rn, (c, r) in RINGS.items():
        if rn in ("UpgradeRing", "SellRing"):
            st = STALLS["UpgradeStall" if rn == "UpgradeRing" else "SellStall"]
            dk = st["deck"]
            on = abs(c[0] - dk[0]) + r <= 12.0 and abs(c[1] - dk[1]) + r <= 12.0
            rep(on, f"{rn}: owner-placed front-corner stall, ring fully on its 24 x 24 deck ({on})")
            continue
        worst = min(seg_dist(c, a, b) - r - half for _, _, a, b, half in lines())
        rep(worst >= 0, f"{rn}: clearance to the nearest walking line {worst:.1f} (>= 0)")''')

# 8: the owner's board arena stands across the straight lines to plots 3/4 (players walk round it; Stage C pathfinding
# proves every plot is reachable); everything else keeps the rule
rep('''    for n, poly in S.items():
        for pid, kind, a, b, half in lines():
            if owner_of(n) == pid:
                continue''', '''    for n, poly in S.items():
        if n in BOARDS:
            continue                          # (makeover) owner's arena: walked round, checked by the Stage C walker
        for pid, kind, a, b, half in lines():
            if owner_of(n) == pid:
                continue''')

# 11: density -> anti-clutter (owner rule #1)
i0 = s.index("    # 11. (review MUST 13) keep it dense")
i1 = s.index("    return ok_all, res, ds", i0)
s = s[:i0] + '''    # 11. (2026-10-21 makeover, owner rule #1 - replaces the review's MUST 13 density rule) NO clutter: no trees, bushes,
    # flowers or benches in the hub; the only plaza solids are the functional models + the wall-foot pumpkin clusters
    allowed = set(BOARDS) | set(STALLS) | {"FreeGiftChest"}
    clutter = [n for n in S if not (owner_of(n) or n in allowed or n.startswith("HalloweenWallPumpkins"))]
    rep(not clutter and not DECOR and not GARDEN and not HGARDEN and not HALLOWEEN_BEDS and ALLEY_BED is None,
        f"no clutter: freestanding decor on the plaza = {clutter + [d['name'] for d in DECOR + GARDEN + HGARDEN]}")
    # 12. (makeover) the wall-foot pumpkin clusters sit on the ground, off every plot slot, 2+ from the floor edge
    for i, (p, r) in enumerate(WALL_PUMPKINS):
        okp = on_ground(p) and all(poly_dist(circle(p, r), plot_rect(pid, W_MAX, L_MAX)) >= 0.5 for pid in PLOTS)
        rep(okp, f"wall pumpkins {i + 1} at {p} on the ground, off the plots")
    # 13. (makeover) the lantern light spots are on the ground
    for i, p in enumerate(LAMP_SPOTS):
        rep(on_ground(p), f"lantern {i + 1} light spot {p} on the ground")
''' + s[i1:]
# render(): skip the removed things, draw the wall pumpkins + lantern spots
rep('''        poly(pp["bed_poly"], fill=(96, 150, 70))
''', '')
rep('''    a = ALLEY_BED
    poly(rect_xz((a["centre"][0] - a["size"][0] / 2, a["centre"][1] - a["size"][1] / 2, a["centre"][0] + a["size"][0] / 2, a["centre"][1] + a["size"][1] / 2)), fill=(96, 150, 70))
''', '''    for p, r in WALL_PUMPKINS:
        dot(p, r, outline=(255, 140, 20), width=2)
''')
rep('''    bd = BACKDROP
    dot(bd["centre"], bd["radius"], fill=(90, 150, 70), outline=(70, 50, 30), width=2)
    d.text((P(bd["centre"])[0] - 30, P(bd["centre"])[1] - 6), "Backdrop", font=f, fill=(255, 255, 255))
''', '')
open(P, "w", encoding="utf-8").write(s)
print("patched checks")
