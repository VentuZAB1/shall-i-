"""SLINGSHOT redesigned hub (A HORSESHOE): the planned layout in real world studs, its rule checks and a top-down PNG.

Run (from this folder):  python hub_layout.py
  -> prints every rule check (PASS/FAIL), writes ../planned_layout.png and ../planned_layout.json
World axes: x to the right, z down the page (the runway is up the page = -Z). Every floor top is y = 0.
This file is the single source of truth for the coordinates in docs/plans/2026-10-21-redesigned-hub.md.
Builders: if you nudge anything in Studio, change it here first and re-run until ALL PASS.
"""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "..", "planned_layout.png")
OUT_JSON = os.path.join(HERE, "..", "planned_layout.json")

# ------------------------------------------------------------------ fixed world (measured in Studio 2026-10-21, never moves)
SLING = (0.53, -44.97)                  # Hub.Slingshot pivot (x, z); faces +Z, launches -Z
PAD = (-9.0, -52.0, 10.0, -38.0)        # Hub.LaunchPlatform 19 x 1 x 14 at (0.5, 0.5, -45) (x0, z0, x1, z1)
GATE_Z = -61.0                          # Runway.LaunchGate 120 x 16 x 2 at (0, 8, -61); Slingshot.Config.GateZ = -60
RUNWAY_WALL = (59.0, 81.0)              # runway side walls |x| 59..81 for z <= -60
INTRO_ZONE = (-12.0, -40.0, 24.0, 12.0)  # IntroCutscene START (5,-4) / HOP_FROM (0.5,-30) / FINISH (-6,~-22) + its cameras
LAUNCH_ZONE = (-14.0, -62.0, 15.0, -30.0)  # pad + fork + the pulled-back pouch (z -32) + the hop-on lane
# (2026-10-21 makeover) the IntroCutscene camera positions in the hub (shot 1 behind START, shot 2 side dolly START ->
# HOP_FROM, shot 3, the gate / skid / WHEW shots and the outro orbit round FINISH): every solid keeps 3+ studs from them.
# Solids in INTRO_EXEMPT may overlap INTRO_ZONE (owner-placed front boards; the cameras never look at them).
# (2026-10-22) shot 2 + the skid re-aimed (measured in Play): shot 2 = p + (10, 1.5, 7), the skid = (p.X + 13, 3.2, p.Z + 9)
INTRO_CAMS = [(9.5, 4.5), (9.5, 2.5), (14.9, 2.7), (14.1, -2.3), (13.2, -7.0), (12.4, -11.7), (11.0, -21.0),
              (-1.5, -34.9), (1.2, -27.4), (3.9, -20.0), (6.0, -15.0), (7.5, -12.0),
              (9.0, -30.0), (-3.6, -33.0), (-5.2, -31.0), (-13.5, -23.5), (-12.0, -14.0), (-6.0, -9.0)]
INTRO_EXEMPT = ("TimeBoard", "RichestBoard")

# ------------------------------------------------------------------ the plots
W_MAX, L_MAX = 60, 90                   # spec: capped at 60 x 90 (width along the gate edge x length away from the plaza)
START, EXPAND = (40, 40), 5             # RebirthConfig.START_SIZE / EXPAND_STEPS (unchanged)


def base_size(r):
    t = min(max(r, 0), EXPAND) / EXPAND
    return (math.floor(START[0] + (W_MAX - START[0]) * t + 0.5), math.floor(START[1] + (L_MAX - START[1]) * t + 0.5))


# gate = centre of the plot's front (gate) edge at y 0 = the Slot's front edge; F = unit facing from the plot towards the
# plaza (= Slot LookVector); R = F x Up = (-Fz, Fx) (= Slot RightVector). s = which side of the gate the treadmill is on.
PLOTS = {
    1: {"gate": (-122.0, -30.0), "F": (1, 0), "s": -1},   # left front  (sketch GRASS)
    2: {"gate": (-90.0, 42.0), "F": (1, 0), "s": -1},     # left back   (sketch WATER)
    3: {"gate": (-40.0, 78.0), "F": (0, -1), "s": -1},    # back left   (sketch THUNDER)
    4: {"gate": (40.0, 78.0), "F": (0, -1), "s": 1},      # back right  (sketch FIRE)
    5: {"gate": (90.0, 42.0), "F": (-1, 0), "s": 1},      # right back  (sketch SHADOW)
    6: {"gate": (122.0, -30.0), "F": (-1, 0), "s": 1},    # right front (sketch CELESTIAL)
}
TREAD_F, TREAD_S = 14.3, 16.0           # treadmill pivot: 14.3 out from the gate line, 16 to the side (today B2: 14.3 / 11.5)
# (2026-10-21 builder, review MUST 4) was 18: the Tier 11 model is 14.7 wide, so 16 keeps the sign (27 out) on the ground at plots 1/6
# (2026-10-21 builder, review MUST 4) the BIGGEST tier footprint (envelope of Assets.Treadmills Tier1..11, measured in pivot space):
# along R +-7.35; along F from -9.2 (towards the plot) to +11.64 (towards the plaza; Tier10 reaches 11.64)
TREAD_R_HALF, TREAD_F_PLOT, TREAD_F_PLAZA = 7.35, 9.25, 11.64
SIGN_F = 6.0                            # upgrade sign pivot (the larger UpgradeSign_B3 model, board 4.0 x 2.6)
SIGN_S = {1: 27.0, 2: 27.0, 3: 27.0, 4: 27.0, 5: 27.0, 6: 27.0}  # (2026-10-21 builder, MUST 4) clears the Tier 11 box by 1.6
SIGN_W, SIGN_D = 4.04, 1.2               # UpgradeSign_B3 clone footprint (measured x +-2.02)
SPAWN_F = 8.0                           # BaseManager.spawnAtBase: 8 studs outside the gate
EXIT_BEHIND = 7.5                       # TreadmillClient: jump off = 7.5 behind the belt (towards the plot)
# (2026-10-22, OWNER edit in Studio) plots 1 / 6: treadmill + upgrade sign moved to the plaza side of the gate, beside the
# plot (same facings as the formula). Exact owner values, deliberately NOT mirrored (103.65 vs 105.65, 109.91 vs 113.91).
OWNER_TREAD = {1: (-103.6503, -14.5395), 6: (105.6504, -14.5395)}
OWNER_SIGN = {1: (-109.9084, -4.8940), 6: (113.9084, -4.8940)}
BED_F = 3.5                             # gate flower bed on the non-treadmill half of the front fence (4 deep)
BED_SPAN = {1: (7.0, 27.0), 2: (7.0, 12.0), 3: (7.0, 27.0), 4: (7.0, 27.0), 5: (7.0, 12.0), 6: (7.0, 27.0)}  # 2/5 short: corner boards
PUMPKIN_PLOTS = ()                      # (2026-10-21 makeover) gate beds + their pumpkin clusters removed (owner rule #1)


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def R_of(F):
    return (-F[1], F[0])


def look_at(frm, to):
    dx, dz = to[0] - frm[0], to[1] - frm[1]
    m = math.hypot(dx, dz)
    return (dx / m, dz / m)


def rect_poly(cx, cz, along_r, along_f, F):
    R = R_of(F)
    pts = []
    for sr, sf in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        pts.append((cx + R[0] * along_r / 2 * sr + F[0] * along_f / 2 * sf, cz + R[1] * along_r / 2 * sr + F[1] * along_f / 2 * sf))
    return pts


def rect_poly_f(c, along_r, f0, f1, F):
    # a box centred on c along R, spanning f0..f1 along F (asymmetric: the treadmill reaches further towards the plaza)
    mid = add(c, F, (f0 + f1) / 2)
    return rect_poly(mid[0], mid[1], along_r, f1 - f0, F)


def plot_rect(pid, w, l):
    p = PLOTS[pid]
    G, F = p["gate"], p["F"]
    R = R_of(F)
    a, b = add(G, R, w / 2), add(G, R, -w / 2)
    return [a, b, add(b, F, -l), add(a, F, -l)]


def plot_parts(pid):
    p = PLOTS[pid]
    G, F, s = p["gate"], p["F"], p["s"]
    R = R_of(F)
    tread = OWNER_TREAD.get(pid) or add(add(G, F, TREAD_F), R, s * TREAD_S)
    sign = OWNER_SIGN.get(pid) or add(add(G, F, SIGN_F), R, s * SIGN_S[pid])
    s0, s1 = BED_SPAN[pid]
    bed = add(add(G, F, BED_F), R, -s * (s0 + s1) / 2)
    return {
        "tread": tread, "tread_poly": rect_poly_f(tread, TREAD_R_HALF * 2, -TREAD_F_PLOT, TREAD_F_PLAZA, F),
        "sign": sign, "sign_poly": rect_poly(sign[0], sign[1], SIGN_W, SIGN_D, F),
        "bed": bed, "bed_len": s1 - s0, "bed_poly": rect_poly(bed[0], bed[1], s1 - s0, 4.0, F),
        "pumpkins": add(add(G, F, 4.0), R, -s * 17.0) if pid in PUMPKIN_PLOTS else None,
        "spawn": add(G, F, SPAWN_F), "exit": add(tread, F, -EXIT_BEHIND),
        "slot_centre": add(G, F, -L_MAX / 2), "R": R,
    }


# ------------------------------------------------------------------ plaza items
PLAZA_CENTRE = (0.0, 20.0)
STALL_RING_F = 5.636                    # Plinth (model pivot) -> ring centre along the facing (both stalls since the makeover)
# (2026-10-21 makeover, owner placement) the stalls stand at the plaza's FRONT CORNERS, backs to the orange runway-wall
# ends (x +-60..80), square to the front wall, counters facing +Z (the plaza). Decks 24 x 24 centred on the wall ends.
STALLS = {
    "UpgradeStall": {"ring_c": (-70.0, -48.364), "ring": "blue"},
    "SellStall": {"ring_c": (70.0, -48.364), "ring": "gold"},
}
for _n, _st in STALLS.items():
    _st["F"] = (0.0, 1.0)
    _st["pivot"] = add(_st["ring_c"], _st["F"], -STALL_RING_F)
    _st["deck"] = (_st["ring_c"][0], -47.6)
BOARD_W, BOARD_D = 16.4, 7.3
K = math.sqrt(0.5)
BOARDS = {                               # model pivot (y 10.25), F = the way the FRONT screen faces
    # (2026-10-21 makeover, owner placement) the 4 boards ring the Free Gift chest on the diagonals, screens facing it
    # (an arena); every board also has a back screen (<Board>_Back model) facing out, so both sides read
    "RichestBoard": {"pivot": (-26.0, 3.0), "F": (K, K)},
    "TimeBoard": {"pivot": (26.0, 3.0), "F": (-K, K)},
    "SpeedBoard": {"pivot": (-26.0, 37.0), "F": (K, -K)},
    "HeaviestBoard": {"pivot": (26.0, 37.0), "F": (-K, -K)},
}
FREE_GIFT = {"pad": (0.0, 20.0), "F": (0.0, -1.0)}      # (makeover, owner placement) plaza centre; chest faces the slingshot (-Z)
SPAWN = {"centre": (0.0, 52.0), "size": 16}             # (makeover) SpawnLocation 16 x 1 x 16 at y -0.4, behind the back board gap
MEDALLION = {"centre": (0.0, 20.0), "radius": 25.9}     # copy of Hub.Decor.Plaza (5 studded cylinders, 51.8 wide)

# ------------------------------------------------------------------ permanent decor (Hub.Decor) + seasonal (HalloweenDecor)
# r = SOLID footprint radius (trunk / body that blocks walking); canopies above head height don't block
DECOR = []                               # (2026-10-21 makeover, owner rule #1) no trees / bushes / benches in the hub
# (2026-10-21 makeover) the 8 lamps are WALL LANTERNS on pillars; LANTERN_PILLARS = the pillar points on the floor edge,
# LAMP_SPOTS = the floor point 2 studs in front of each (where its light pool falls; must be on the ground)
LANTERN_PILLARS = [(-14.6, 171.0), (14.6, 171.0), (-73.0, 78.0), (73.0, 78.0), (-81.0, -60.0), (81.0, -60.0), (-215.0, 12.0), (215.0, 12.0)]
LAMP_SPOTS = [(-14.6, 169.0), (14.6, 169.0), (-71.6, 76.6), (71.6, 76.6), (-83.0, -58.0), (83.0, -58.0), (-213.0, 10.0), (213.0, 10.0)]
ALLEY_BED = None                         # (makeover) the planted alley strip is gone: the alley is the paved spine lane
PUMPKIN = (0.0, 64.0, 230.0)            # HalloweenDecor.GiantPumpkin.Pivot, LookVector -Z (was (0, 64, 169))
HALLOWEEN_BEDS = []                      # (makeover) removed (owner rule #1)
PUMPKIN_ALLEY = []                       # (makeover) replaced by WALL_PUMPKINS
# (makeover) pumpkin-egg clusters on the floor at the wall foot: the alley end (centred, between the pumpkin hands),
# beside the runway-junction towers, at the corridor ends between plots 1-2 / 5-6. r = footprint radius (no collision)
WALL_PUMPKINS = [((0.0, 164.0), 6.0), ((-88.0, -55.0), 4.5), ((88.0, -55.0), 4.5), ((-209.0, 6.0), 5.0), ((209.0, 6.0), 5.0)]
# (2026-10-21 builder, review MUST 13b) PERMANENT garden clusters (Hub.Decor.Garden): a centrepiece (TreeRound / Blossom /
# Bush / Rock from ServerStorage.HalloweenGardenBackup) + bushes, rocks and grass tufts within `r`. r = cluster footprint
# (bushes and tufts do not collide; trees collide on the trunk only). Left side; the right side is the mirror (x -> -x).
GARDEN = []                              # (makeover, owner rule #1) the permanent garden clusters are gone
# (2026-10-21 builder, review MUST 14) the SEASONAL Halloween garden (HalloweenDecor.Garden): the free-standing HQ
# pieces re-placed in the free wedges / plot gaps / front corners (the alley stays low: graves only). tree = the live
# garden tree moved there (with its spiders); extra = bushes; r = ground footprint (nothing collides; canopies are high).
HGARDEN = []                             # (makeover, owner rule #1) the seasonal Halloween garden is gone
# (2026-10-21 builder, owner call 3) PERMANENT backdrop behind plots 3/4 at the end of the alley, beyond the back wall
# (not walkable): a floating garden island with a giant tree; the October giant pumpkin rises behind it.
BACKDROP = None  # (makeover) island + tree moved to the backup; was {"centre": (0.0, 194.0), "radius": 20.0, "tree_scale": 1.7}  # 1.7: the tree stays under the October pumpkin's chin (head bottom ~y 36 at z 190)

# ------------------------------------------------------------------ ground, edge walls, bounds
GROUND = [                              # (x0, z0, x1, z1), top y 0, 8 thick (like the old Hub.Floor)
    ("GroundFront", (-215.0, -60.0, 215.0, 12.0)),
    ("GroundMid", (-183.0, 12.0, 183.0, 78.0)),
    ("GroundBack", (-73.0, 78.0, 73.0, 171.0)),
]
OUTLINE = [(-81.0, -60.0), (-215.0, -60.0), (-215.0, 12.0), (-183.0, 12.0), (-183.0, 78.0), (-73.0, 78.0), (-73.0, 171.0),
           (73.0, 171.0), (73.0, 78.0), (183.0, 78.0), (183.0, 12.0), (215.0, 12.0), (215.0, -60.0), (81.0, -60.0)]
WALL_T, WALL_H = 2.0, 4.0               # low studded edge wall, built OUTSIDE the floor edge
BOUND_T = 4.0                           # invisible Map.Bounds column OUTSIDE the wall, y 0..1040


def outward(a, b):
    # the outline runs counter-clockwise on the page (x right, z down): for a->b the outside is (-dz, dx)
    dx, dz = b[0] - a[0], b[1] - a[1]
    m = math.hypot(dx, dz)
    return (-dz / m, dx / m)


def convex(prev_a, corner, next_b):
    # True when the outline turns AWAY from the floor at `corner` (an outer corner: wall pieces must be extended to meet);
    # False at an inner corner (extending would push a wall onto the floor). The two runway ends count as not convex.
    if prev_a is None or next_b is None:
        return False
    d1 = (corner[0] - prev_a[0], corner[1] - prev_a[1])
    d2 = (next_b[0] - corner[0], next_b[1] - corner[1])
    return d1[0] * d2[1] - d1[1] * d2[0] < 0


def edge_segments():
    out = []
    n_pts = len(OUTLINE)
    for i in range(n_pts - 1):
        a, b = OUTLINE[i], OUTLINE[i + 1]
        n = outward(a, b)
        u = ((b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b))
        L = math.dist(a, b)
        ext_a = convex(OUTLINE[i - 1] if i > 0 else None, a, b)
        ext_b = convex(a, b, OUTLINE[i + 2] if i + 2 < n_pts else None)
        wa, wb = (WALL_T if ext_a else 0.0), (WALL_T if ext_b else 0.0)
        ba, bb = (WALL_T + BOUND_T if ext_a else 0.0), (WALL_T + BOUND_T if ext_b else 0.0)
        w_mid = add(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), u, (wb - wa) / 2)
        b_mid = add(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), u, (bb - ba) / 2)
        out.append({"i": i + 1, "a": a, "b": b, "len": L, "n": n, "dir": u, "outer_a": ext_a, "outer_b": ext_b,
                    "wall_c": add(w_mid, n, WALL_T / 2), "wall_len": L + wa + wb,
                    "bound_c": add(b_mid, n, WALL_T + BOUND_T / 2), "bound_len": L + ba + bb})
    return out


# ------------------------------------------------------------------ walking lines (spec: decor never blocks them)
ENTRY = (0.5, -56.0)                    # just inside the LaunchGate, in front of the pad (TutorialClient SAFE = (0, -52))
GATE_EDGES = [(-50.0, -58.0), (50.0, -58.0)]
MAIN_HALF, FAN_HALF = 6.0, 3.0          # main line ENTRY -> spawn spot (rings stay off it), fan lines from the gate edges


def seg_dist(p, a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dz) / (dx * dx + dz * dz)))
    return math.hypot(p[0] - (a[0] + t * dx), p[1] - (a[1] + t * dz))


def lines():
    out = []
    for pid in PLOTS:
        sp = plot_parts(pid)["spawn"]
        out.append((pid, "main", ENTRY, sp, MAIN_HALF))
        for g in GATE_EDGES:
            out.append((pid, "fan", g, sp, FAN_HALF))
    return out


# ------------------------------------------------------------------ geometry helpers
def poly_edges(poly):
    return [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]


def point_in_poly(p, poly):
    x, z = p
    inside = False
    for (x1, z1), (x2, z2) in poly_edges(poly):
        if (z1 > z) != (z2 > z):
            if x1 + (z - z1) * (x2 - x1) / (z2 - z1) > x:
                inside = not inside
    return inside


def seg_seg(a, b, c, d):
    def ccw(p, q, r):
        return (r[1] - p[1]) * (q[0] - p[0]) - (q[1] - p[1]) * (r[0] - p[0])
    if (ccw(a, b, c) * ccw(a, b, d) < 0) and (ccw(c, d, a) * ccw(c, d, b) < 0):
        return 0.0
    return min(seg_dist(a, c, d), seg_dist(b, c, d), seg_dist(c, a, b), seg_dist(d, a, b))


def poly_dist(p1, p2):
    if any(point_in_poly(v, p2) for v in p1) or any(point_in_poly(v, p1) for v in p2):
        return 0.0
    return min(seg_seg(a, b, c, d) for a, b in poly_edges(p1) for c, d in poly_edges(p2))


def circle(c, r, n=20):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def rect_xz(r):
    x0, z0, x1, z1 = r
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def poly_seg_dist(poly, a, b):
    if point_in_poly(a, poly) or point_in_poly(b, poly):
        return 0.0
    return min(seg_seg(p, q, a, b) for p, q in poly_edges(poly))


def on_ground(p):
    return any(point_in_poly(p, rect_xz(r)) for _, r in GROUND)


# ------------------------------------------------------------------ the solid things on the plaza (name -> polygon)
def solids():
    s = {}
    for pid in PLOTS:
        pp = plot_parts(pid)
        s[f"Treadmill_B{pid}"] = pp["tread_poly"]
        s[f"UpgradeSign_B{pid}"] = pp["sign_poly"]
    for n, st in STALLS.items():
        s[n] = rect_poly(st["pivot"][0], st["pivot"][1], 13.0, 8.0, st["F"])
    for n, b in BOARDS.items():
        s[n] = rect_poly(b["pivot"][0], b["pivot"][1], BOARD_W, BOARD_D, b["F"])
    s["FreeGiftChest"] = rect_poly(FREE_GIFT["pad"][0], FREE_GIFT["pad"][1], 6.4, 4.2, FREE_GIFT["F"])
    for d in DECOR:
        s[d["name"]] = circle(d["pos"], d["r"])
    for g in GARDEN:
        s["Garden" + g["name"]] = circle(g["pos"], g["r"])
    for i, (p, r) in enumerate(WALL_PUMPKINS):
        s[f"HalloweenWallPumpkins{i + 1}"] = circle(p, r)
    for g in HGARDEN:
        s["HalloweenGarden" + g["name"]] = circle(g["pos"], g["r"])
    return s


RINGS = {"UpgradeRing": (STALLS["UpgradeStall"]["ring_c"], 6.2), "SellRing": (STALLS["SellStall"]["ring_c"], 6.2),
         "FreeGiftRing": (FREE_GIFT["pad"], 7.5)}


def owner_of(name):
    for pid in PLOTS:
        if name.endswith(f"_B{pid}"):
            return pid
    return None


# ------------------------------------------------------------------ checks
def checks():
    res, ok_all = [], True

    def rep(ok, msg):
        nonlocal ok_all
        ok_all = ok_all and ok
        res.append(("PASS " if ok else "FAIL ") + msg)

    # 1. plots >= 10 apart at max size (and therefore at every smaller size: the gate edge is fixed, plots only grow back)
    for i in PLOTS:
        for j in PLOTS:
            if i < j:
                d = poly_dist(plot_rect(i, W_MAX, L_MAX), plot_rect(j, W_MAX, L_MAX))
                if d < 60:
                    rep(d >= 10, f"plot {i}-{j} gap at 60x90 = {d:.1f} (>= 10)")
    # 2. gate -> slingshot <= 140 and fair (max/min <= 1.10)
    ds = {pid: math.dist(p["gate"], SLING) for pid, p in PLOTS.items()}
    for pid, d in ds.items():
        rep(d <= 140, f"plot {pid} gate -> slingshot {d:.1f} studs (<= 140)")
    rep(max(ds.values()) / min(ds.values()) <= 1.10, f"fairness max/min = {max(ds.values()) / min(ds.values()):.3f} (<= 1.10)")
    # 3. each plot (max size) sits on the ground and inside the outline
    for pid in PLOTS:
        rep(all(on_ground(v) or any(seg_dist(v, *e) < 0.01 for e in poly_edges(rect_xz(r)) for _, r in GROUND)
                for v in plot_rect(pid, W_MAX, L_MAX)), f"plot {pid} at 60x90 is on the ground")
    S = solids()
    # 4. nothing solid in the launch zone or the intro corridor, nothing past the gate line
    for n, poly in S.items():
        in_intro = poly_dist(poly, rect_xz(INTRO_ZONE)) < 0.5 and n not in INTRO_EXEMPT
        bad = poly_dist(poly, rect_xz(LAUNCH_ZONE)) < 2 or in_intro or any(v[1] < -60 for v in poly)
        if bad:
            rep(False, f"{n} touches the launch zone / intro corridor / runway")
        low = rect_poly(BOARDS[n]["pivot"][0], BOARDS[n]["pivot"][1], BOARD_W, 3.0, BOARDS[n]["F"]) if n in BOARDS else poly  # cameras fly at y < 9: board posts, not its roof
        cam = min(min(math.dist(c, v) for v in low) if not point_in_poly(c, low) else 0.0 for c in INTRO_CAMS)
        if cam < 3.0:
            rep(False, f"{n} only {cam:.1f} from an IntroCutscene camera (>= 3)")
    rep(True, "launch zone + intro corridor (+ measured intro cameras, owner-placed front boards exempt) + runway line checked")
    # 5. no overlaps: items vs items (>= 3 apart, own treadmill/sign/bed pairs >= 1.5) and items vs plots at max (>= 2)
    names = list(S)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            need = 1.5 if owner_of(a) and owner_of(a) == owner_of(b) else 3.0
            if owner_of(a) and owner_of(a) == owner_of(b) and owner_of(a) in OWNER_TREAD:
                need = 0.0                    # (2026-10-22) owner-placed pair (plots 1 / 6): no overlap is enough
            if {a, b} in ({"UpgradeStall", "GardenStallBackL"}, {"SellStall", "GardenStallBackR"}):
                need = 0.5                    # (2026-10-21 builder) the deck bushes stand right behind their own counter
            if {a, b} <= {"AlleyBed", "HalloweenBed2", "HalloweenBed3"}:
                continue                      # the alley Halloween beds sit ON the alley bed (by design)
            d = poly_dist(S[a], S[b])
            if d < need:
                rep(False, f"{a} vs {b} only {d:.1f} apart (>= {need})")
        for pid in PLOTS:
            d = poly_dist(S[names[i]], plot_rect(pid, W_MAX, L_MAX))
            if d < 1.0:
                rep(False, f"{names[i]} overlaps plot {pid} at 60x90 (gap {d:.1f})")
    rep(True, "item / item and item / plot overlaps checked")
    # 6. everything stands on the ground
    for n, poly in S.items():
        if not all(on_ground(v) for v in poly):
            rep(False, f"{n} hangs over the edge")
    # 7. walk-in rings keep their edge 6+ studs off every main line and 3+ off every fan line (no accidental windows)
    for rn, (c, r) in RINGS.items():
        if rn == "FreeGiftRing":
            rep(math.dist(c, PLAZA_CENTRE) < 0.01, f"{rn}: owner-placed at the plaza centre (walked round / once-only window)")
            continue
        if rn in ("UpgradeRing", "SellRing"):
            st = STALLS["UpgradeStall" if rn == "UpgradeRing" else "SellStall"]
            dk = st["deck"]
            on = abs(c[0] - dk[0]) + r <= 12.0 and abs(c[1] - dk[1]) + r <= 12.0
            rep(on, f"{rn}: owner-placed front-corner stall, ring fully on its 24 x 24 deck ({on})")
            continue
        worst = min(seg_dist(c, a, b) - r - half for _, _, a, b, half in lines())
        rep(worst >= 0, f"{rn}: clearance to the nearest walking line {worst:.1f} (>= 0)")
    # 8. solids keep off the walking lines (a plot's own treadmill / sign / bed may sit beside its own line)
    for n, poly in S.items():
        if n in BOARDS or n in STALLS or n == "FreeGiftChest":
            continue                          # (makeover) owner placements: walked round, checked by the Stage C walker
        for pid, kind, a, b, half in lines():
            if owner_of(n) == pid:
                continue
            d = poly_seg_dist(poly, a, b)
            if d < half:
                rep(False, f"{n} on the {kind} line {a} -> plot {pid} (dist {d:.1f} < {half})")
    rep(True, "solids vs walking lines checked")
    # 8b. edge walls + bounds columns sit outside the floor (never on the walkable ground)
    for e in edge_segments():
        rep(not on_ground(e["wall_c"]) and not on_ground(e["bound_c"]), f"edge {e['i']} wall + bounds outside the floor")
    # 9. treadmill exit spot (7.5 behind the belt) is on the plaza, outside the plot
    for pid in PLOTS:
        e = plot_parts(pid)["exit"]
        rep(on_ground(e) and not point_in_poly(e, plot_rect(pid, W_MAX, L_MAX)), f"treadmill {pid} exit spot ({e[0]:.1f},{e[1]:.1f}) on the plaza")
    # 10. plot spawn spots are on the ground and free
    for pid in PLOTS:
        sp = plot_parts(pid)["spawn"]
        free = all(not point_in_poly(sp, poly) for poly in S.values())
        rep(on_ground(sp) and free, f"plot {pid} spawn spot ({sp[0]:.1f},{sp[1]:.1f}) on free ground")
    # 11. (2026-10-21 makeover, owner rule #1 - replaces the review's MUST 13 density rule) NO clutter: no trees, bushes,
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
    return ok_all, res, ds


# ------------------------------------------------------------------ render
def render(ds):
    pad = 46
    xmin, xmax, zmin, zmax = -240, 240, -110, 250
    sc = 2.2
    Wpx, Hpx = int((xmax - xmin) * sc) + 2 * pad, int((zmax - zmin) * sc) + 2 * pad + 66
    img = Image.new("RGB", (Wpx, Hpx), (30, 36, 58))
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype("arialbd.ttf", 12)
        fs = ImageFont.truetype("arial.ttf", 10)
        fb = ImageFont.truetype("arialbd.ttf", 18)
    except OSError:
        f = fs = fb = ImageFont.load_default()

    def P(p):
        return (pad + (p[0] - xmin) * sc, pad + (p[1] - zmin) * sc)

    def poly(pts, fill=None, outline=None, width=1):
        d.polygon([P(p) for p in pts], fill=fill, outline=outline)
        if outline and width > 1:
            d.line([P(p) for p in pts] + [P(pts[0])], fill=outline, width=width)

    def dot(c, r, fill=None, outline=None, width=1):
        d.ellipse([P((c[0] - r, c[1] - r)), P((c[0] + r, c[1] + r))], fill=fill, outline=outline, width=width)

    for x in range(xmin, xmax + 1, 20):
        d.line([P((x, zmin)), P((x, zmax))], fill=(42, 50, 76) if x % 100 else (64, 74, 104))
        if x % 40 == 0:
            d.text((P((x, zmin))[0] - 8, pad - 18), str(x), font=fs, fill=(150, 160, 190))
    for z in range(zmin + 10, zmax + 1, 20):
        d.line([P((xmin, z)), P((xmax, z))], fill=(42, 50, 76) if z % 100 else (64, 74, 104))
        if z % 40 == 0:
            d.text((8, P((xmin, z))[1] - 6), str(z), font=fs, fill=(150, 160, 190))
    d.text((pad, 6), "x ->", font=fs, fill=(150, 160, 190))
    d.text((6, pad - 2), "z", font=fs, fill=(150, 160, 190))
    # runway, its walls, the gate
    poly(rect_xz((-60, -110, 60, -60)), fill=(110, 200, 120))
    poly(rect_xz((-81, -110, -59, -60)), fill=(120, 110, 100))
    poly(rect_xz((59, -110, 81, -60)), fill=(120, 110, 100))
    d.line([P((-60, GATE_Z)), P((60, GATE_Z))], fill=(170, 230, 255), width=3)
    d.text(P((-22, -104)), "RUNWAY (-Z, unchanged)", font=f, fill=(20, 60, 20))
    # ground tiles
    for _, r in GROUND:
        poly(rect_xz(r), fill=(214, 206, 180))
    # edge walls + bounds
    for e in edge_segments():
        n = e["n"]
        a2, b2 = add(e["a"], n, WALL_T / 2), add(e["b"], n, WALL_T / 2)
        d.line([P(a2), P(b2)], fill=(96, 132, 170), width=max(2, int(WALL_T * sc)))
        a3, b3 = add(e["a"], n, WALL_T + BOUND_T / 2), add(e["b"], n, WALL_T + BOUND_T / 2)
        d.line([P(a3), P(b3)], fill=(200, 80, 200), width=1)
    # walking lines
    for pid, kind, a, b, half in lines():
        if kind == "main":
            d.line([P(a), P(b)], fill=(198, 184, 150), width=int(half * 2 * sc))
        else:
            d.line([P(a), P(b)], fill=(196, 186, 160), width=1)
    poly(rect_xz(INTRO_ZONE), outline=(230, 120, 40), width=2)
    d.text(P((INTRO_ZONE[0] + 1, INTRO_ZONE[3] - 6)), "intro", font=fs, fill=(200, 90, 20))
    poly(rect_xz(LAUNCH_ZONE), outline=(200, 60, 60), width=1)
    # medallion + spawn
    dot(MEDALLION["centre"], MEDALLION["radius"], fill=(236, 226, 196), outline=(180, 160, 120), width=2)
    sp = SPAWN["centre"]
    h = SPAWN["size"] / 2
    d.rectangle([P((sp[0] - h, sp[1] - h)), P((sp[0] + h, sp[1] + h))], fill=(250, 250, 250), outline=(60, 60, 60))
    d.text((P(sp)[0] - 18, P(sp)[1] - 6), "Spawn", font=f, fill=(30, 30, 30))
    # plots
    cols = {1: (110, 200, 90), 2: (80, 160, 230), 3: (235, 205, 60), 4: (240, 120, 60), 5: (150, 100, 220), 6: (235, 220, 160)}
    for pid, p in PLOTS.items():
        poly(plot_rect(pid, W_MAX, L_MAX), fill=tuple(int(c * 0.5) for c in cols[pid]), outline=(15, 15, 25), width=2)
        for r in range(0, 5):
            w, l = base_size(r)
            poly(plot_rect(pid, w, l), outline=cols[pid], width=1)
        pp = plot_parts(pid)
        g = p["gate"]
        dot(g, 2.2, fill=(255, 255, 255))
        scn = pp["slot_centre"]
        d.text((P(scn)[0] - 28, P(scn)[1] - 18), f"Base{pid}", font=fb, fill=(255, 255, 255))
        d.text((P(scn)[0] - 32, P(scn)[1] + 6), f"gate {g[0]:.0f},{g[1]:.0f}", font=fs, fill=(240, 240, 240))
        d.text((P(scn)[0] - 32, P(scn)[1] + 18), f"to sling {ds[pid]:.0f}", font=fs, fill=(240, 240, 240))
        poly(pp["tread_poly"], fill=(70, 70, 92), outline=(20, 20, 20))
        poly(pp["sign_poly"], fill=(40, 40, 170))
        if pp["pumpkins"]:
            dot(pp["pumpkins"], 1.6, fill=(255, 140, 20))
        dot(pp["exit"], 1.0, fill=(255, 70, 70))
        s = pp["spawn"]
        d.rectangle([P((s[0] - 1.5, s[1] - 1.5)), P((s[0] + 1.5, s[1] + 1.5))], fill=(255, 255, 255))
    # stalls + decks + rings
    for n, st in STALLS.items():
        poly(rect_poly(st["deck"][0], st["deck"][1], 24, 24, st["F"]), fill=(196, 168, 118))
        poly(rect_poly(st["pivot"][0], st["pivot"][1], 13, 8, st["F"]), fill=(120, 80, 50), outline=(20, 20, 20))
        col = (40, 160, 255) if st["ring"] == "blue" else (255, 200, 0)
        dot(st["ring_c"], 6.2, outline=col, width=3)
        d.text((P(st["pivot"])[0] - 34, P(st["pivot"])[1] - 38), n.replace("Stall", " stall"), font=f, fill=(20, 20, 30))
    for n, b in BOARDS.items():
        poly(rect_poly(b["pivot"][0], b["pivot"][1], BOARD_W, BOARD_D, b["F"]), fill=(90, 90, 112), outline=(10, 10, 10))
        tip = add(b["pivot"], b["F"], 6)
        d.line([P(b["pivot"]), P(tip)], fill=(255, 255, 255), width=1)
        d.text((P(b["pivot"])[0] - 22, P(b["pivot"])[1] + 12), n.replace("Board", ""), font=fs, fill=(30, 30, 40))
    fg = FREE_GIFT["pad"]
    dot(fg, 7.5, outline=(120, 255, 60), width=3)
    poly(rect_poly(fg[0], fg[1], 6.4, 4.2, FREE_GIFT["F"]), fill=(210, 40, 40))
    d.text((P(fg)[0] - 24, P(fg)[1] + 20), "Free Gift", font=f, fill=(30, 30, 30))
    # decor
    for dd in DECOR:
        col = {"TreeRound": (40, 130, 50), "Blossom": (230, 140, 190), "Bush": (60, 150, 60), "Rock": (130, 130, 130), "Bench": (150, 100, 60)}[dd["kind"]]
        dot(dd["pos"], max(dd["r"], 2.5), fill=col)
    for i, p in enumerate(LAMP_SPOTS):
        dot(p, 1.6, fill=(255, 230, 120), outline=(60, 40, 0))
    for p, r in WALL_PUMPKINS:
        dot(p, r, outline=(255, 140, 20), width=2)
    for p in HALLOWEEN_BEDS:
        dot(p, 4.0, outline=(255, 130, 0), width=2)
    for g in GARDEN:
        col = {"TreeRound": (40, 130, 50), "Blossom": (230, 140, 190), "Bush": (60, 150, 60), "Rock": (130, 130, 130)}[g["kind"]]
        dot(g["pos"], g["r"], outline=(60, 110, 50), width=1)
        dot(g["pos"], 2.5, fill=col)
    for g in HGARDEN:
        dot(g["pos"], g["r"], outline=(255, 130, 0), width=1)
        dot(g["pos"], 1.8, fill=(160, 80, 20))
    for p in PUMPKIN_ALLEY:
        dot(p, 1.6, fill=(255, 140, 20))
    dot((PUMPKIN[0], PUMPKIN[2]), 16, fill=(240, 120, 20), outline=(90, 40, 0), width=2)
    d.text((P((PUMPKIN[0], PUMPKIN[2]))[0] - 54, P((PUMPKIN[0], PUMPKIN[2]))[1] + 38), "Giant pumpkin (Halloween)", font=f, fill=(255, 190, 120))
    # slingshot
    poly(rect_xz(PAD), fill=(140, 90, 50))
    dot(SLING, 4, fill=(100, 60, 30))
    d.text(P((13, -55)), "SLINGSHOT (fixed)", font=f, fill=(30, 30, 30))
    y0 = Hpx - 58
    legend = ["A HORSESHOE - PLANNED (real studs, grid 20). Plots drawn at 60x90 max with R0-R4 outlines. White dot = gate,"
              " white square = spawn spot, red dot = treadmill exit, orange dot = pumpkin cluster, yellow dot = lamp spot.",
              "Beige bands = main walking lines (gate -> every plot), thin lines = gate-edge fans (kept clear). Blue = low edge wall,"
              " magenta = Map.Bounds column. Orange box = intro corridor, red box = launch zone (kept clear).",
              "Green bars = gate flower beds. Tan squares = MarketCorners decks. Pink = blossom trees, dark green = round trees,"
              " grey = rocks, brown = benches. Orange rings = Halloween beds (seasonal)."]
    for i, line in enumerate(legend):
        d.text((pad, y0 + 17 * i), line, font=fs, fill=(230, 230, 240))
    img.save(OUT_PNG)
    return OUT_PNG


def dump(ds):
    data = {"note": "generated by tools/hub_layout.py - (x, z) pairs; y is given per item in the plan",
            "plots": {}, "stalls": {}, "boards": {}, "free_gift": FREE_GIFT, "spawn": SPAWN, "medallion": MEDALLION,
            "decor": DECOR, "garden": GARDEN, "halloween_garden": HGARDEN, "backdrop": BACKDROP, "lamp_spots": LAMP_SPOTS, "alley_bed": ALLEY_BED, "giant_pumpkin": PUMPKIN,
            "halloween_beds": HALLOWEEN_BEDS, "pumpkin_alley": PUMPKIN_ALLEY, "ground": GROUND, "edges": edge_segments()}
    for pid, p in PLOTS.items():
        pp = plot_parts(pid)
        data["plots"][pid] = {"gate": p["gate"], "F": p["F"], "R": pp["R"], "slot_centre": pp["slot_centre"],
                              "treadmill": pp["tread"], "sign": pp["sign"], "bed": pp["bed"], "pumpkins": pp["pumpkins"],
                              "spawn_spot": pp["spawn"], "tread_exit": pp["exit"], "to_sling": round(ds[pid], 1)}
    for n, st in STALLS.items():
        data["stalls"][n] = {"pivot": st["pivot"], "F": st["F"], "ring": st["ring_c"], "deck": st["deck"]}
    data["boards"] = BOARDS
    with open(OUT_JSON, "w") as fh:
        json.dump(data, fh, indent=1)


if __name__ == "__main__":
    ok, res, ds = checks()
    for line in res:
        print(line)
    print("ALL PASS" if ok else "SOME FAIL")
    print(render(ds))
    dump(ds)
