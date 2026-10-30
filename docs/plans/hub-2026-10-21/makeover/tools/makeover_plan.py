"""SLINGSHOT hub makeover (2026-10-21 night): the wall / placement plan in world studs + the annotated top-down.

Run:  python -I makeover_plan.py
  -> prints the plan tables, writes ../plan.json and ../plan_annotated.png (drawn over ../shots/before_01_top.jpg)
World axes: x right, z down the page (the runway is up the page = -Z). Floor top y = 0.
The outline is the live Hub V2 floor outline (HubV2Kit.Layout.EDGES / hub_layout.py OUTLINE), unchanged.
"""
import json
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

# ------------------------------------------------------------------ the floor outline (unchanged, from hub_layout.py)
OUTLINE = [(-81.0, -60.0), (-215.0, -60.0), (-215.0, 12.0), (-183.0, 12.0), (-183.0, 78.0), (-73.0, 78.0), (-73.0, 171.0),
           (73.0, 171.0), (73.0, 78.0), (183.0, 78.0), (183.0, 12.0), (215.0, 12.0), (215.0, -60.0), (81.0, -60.0)]

# ------------------------------------------------------------------ wall section (d = distance OUTWARD from the floor edge)
WALL = {
    "panel_d": (0.8, 6.8), "panel_y": (3.6, 24.0),      # recessed studded panel (BODY)
    "wainscot_d": (0.0, 6.6), "wainscot_y": (0.0, 3.6),  # base band flush with the floor edge (DARK)
    "coping_d": (0.4, 7.4), "coping_y": (24.0, 25.6),    # light coping, 0.4 lip over the panel (CAP)
    "pillar_w": 4.0, "pillar_d": (-0.1, 6.6), "pillar_y": (0.0, 27.2),     # proud of the panel by 0.9 (DARK)
    "pcap_w": 5.0, "pcap_d": (-0.5, 7.2), "pcap_y": (27.2, 28.4),          # pillar cap (CAP)
    "pfoot_w": 5.0, "pfoot_d": (-0.1, 6.6), "pfoot_y": (0.0, 2.0),         # pillar foot (FOOT)
    "tower_y": 32.0,                                                      # the 2 runway-junction towers rise higher
}
COLOURS = {"BODY": (96, 132, 170), "DARK": (58, 84, 130), "CAP": (232, 222, 196), "FOOT": (46, 66, 104)}
BAYS = {1: 5, 2: 3, 3: 1, 4: 2, 5: 4, 6: 3, 7: 5, 8: 3, 9: 4, 10: 2, 11: 1, 12: 3, 13: 5}   # bays per edge


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def outward(a, b):
    dx, dz = b[0] - a[0], b[1] - a[1]
    m = math.hypot(dx, dz)
    return (-dz / m, dx / m)


def edges():
    out = []
    for i in range(len(OUTLINE) - 1):
        a, b = OUTLINE[i], OUTLINE[i + 1]
        L = math.dist(a, b)
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        out.append({"i": i + 1, "a": a, "b": b, "len": L, "u": u, "n": outward(a, b), "bays": BAYS[i + 1]})
    return out


EDGES = edges()


def pillars():
    """every pillar: position on the floor-edge line, the edge(s) it belongs to, kind (corner / mid / junction)"""
    seen, out = {}, []
    for e in EDGES:
        n = e["bays"]
        for k in range(n + 1):
            p = add(e["a"], e["u"], e["len"] * k / n)
            key = (round(p[0], 2), round(p[1], 2))
            if key in seen:
                seen[key]["edges"].append(e["i"])
                continue
            kind = "mid"
            if k in (0, n):
                kind = "junction" if key in ((-81.0, -60.0), (81.0, -60.0)) else "corner"
            rec = {"x": key[0], "z": key[1], "edges": [e["i"]], "kind": kind}
            seen[key] = rec
            out.append(rec)
    return out


PILLARS = pillars()


def bays():
    out = []
    for e in EDGES:
        n = e["bays"]
        for k in range(n):
            a = add(e["a"], e["u"], e["len"] * k / n)
            b = add(e["a"], e["u"], e["len"] * (k + 1) / n)
            out.append({"edge": e["i"], "k": k + 1, "a": a, "b": b, "mid": ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2),
                        "span": e["len"] / n, "n": e["n"], "u": e["u"]})
    return out


BAYS_ALL = bays()

# ------------------------------------------------------------------ wall decor assignment
VINE_BAYS = {(7, 2), (7, 4)}                       # the pumpkin "hands" (VineGrip) flank the alley-end bay under the head
BAT_BAYS = {(7, 3): 4, (1, 1): 4, (13, 5): 4}      # 12 flat wall bats in 3 loose flocks
LANTERN_AT = [(-14.6, 171.0), (14.6, 171.0), (-73.0, 78.0), (73.0, 78.0), (-81.0, -60.0), (81.0, -60.0), (-215.0, 12.0), (215.0, 12.0)]
# pumpkin-egg clusters on the floor at the wall foot (cluster footprint centres): the alley end (one, centred under the
# head, between the hands), beside the 2 runway-junction towers (clear of the stall decks + the plot 1/6 treadmills) and
# at the 2 corridor ends between plots 1-2 / 5-6 (under the corner lanterns). 5 of the 6 live clusters; #6 -> backup.
PUMPKINS_AT = [(0.0, 164.0), (-90.0, -56.0), (90.0, -56.0), (-209.0, 6.0), (209.0, 6.0)]
WEBS_AT = [(-183.0, 78.0), (183.0, 78.0), (-73.0, 171.0), (73.0, 171.0)]
GARLAND_LEN = 26.4

for b in BAYS_ALL:
    key = (b["edge"], b["k"])
    clear = b["span"] - WALL["pillar_w"]
    b["vine"] = key in VINE_BAYS
    b["bats"] = BAT_BAYS.get(key, 0)
    b["garland"] = not b["vine"]
    # every garland hooks onto the FRONT faces of its two pillars (hooks 0.4 inside the pillar centres; the stock
    # garland's hooks are 26.0 apart): scale = (span / 2 - 0.4) / 13.0  -> 0.89 (24-stud bays) .. 1.24 (33-stud bays)
    b["garland_scale"] = round((b["span"] / 2 - 0.4) / 13.0, 3)

# ------------------------------------------------------------------ snapped placements (pass 1)
PLACE = {
    "UpgradeStall": {"plinth": (-70.0, 0.95, -54.0), "rotY": 180, "ring": (-70.0, -48.37), "front": "+Z"},
    "SellStall": {"plinth": (70.0, 0.95, -54.0), "rotY": 180, "ring": (70.0, -48.37), "front": "+Z"},
    "LeftMarket": {"centre": (-70.0, 0.3, -47.6), "rotY": 0, "size": 24},
    "RightMarket": {"centre": (70.0, 0.3, -47.6), "rotY": 0, "size": 24},
    "RichestBoard": {"pivot": (-26.0, None, 3.0), "rotY": -135, "faces": (0.707, 0.707)},
    "TimeBoard": {"pivot": (26.0, None, 3.0), "rotY": 135, "faces": (-0.707, 0.707)},
    "SpeedBoard": {"pivot": (-26.0, None, 37.0), "rotY": -45, "faces": (0.707, -0.707)},
    "HeaviestBoard": {"pivot": (26.0, None, 37.0), "rotY": 45, "faces": (-0.707, -0.707)},
    "Chest": {"pivot": (0.0, 1.8, 20.0), "rotY": 0, "front": "-Z"},
    "PadRing": {"centre": (0.0, 0.39, 20.0), "rotY": 0},
    "FreeGiftZone": {"centre": (0.0, 0.95, 20.0)},
    "Spawn": {"centre": (0.0, -0.4, 52.0), "rotY": 0, "faces": "-Z"},
    "Medallion": {"centre": (0.0, 0.2, 20.0)},
}
BOARD_W, BOARD_D = 16.4, 7.3

# ------------------------------------------------------------------ ground (pass 3)
GROUND = {
    "paving": (212, 190, 152), "lane": (230, 214, 180), "lane_edge": (176, 146, 110), "apron": (186, 158, 120),
    "kerb": (156, 128, 96), "medallion_band": (150, 96, 64),
}
LANES = [  # (name, a, b, width) on the floor, flat (top y 0.06)
    ("Spine_Front", (0.0, -38.0), (0.0, -6.0), 14.0),
    ("Spine_Back", (0.0, 46.0), (0.0, 168.0), 14.0),
    ("Avenue_L", (-112.0, -30.0), (-7.0, -30.0), 10.0),
    ("Avenue_R", (7.0, -30.0), (112.0, -30.0), 10.0),
    ("Spoke_P2", (-27.0, 22.0), (-80.0, 42.0), 8.0),       # medallion side gap -> plot 2 gate apron
    ("Spoke_P5", (27.0, 22.0), (80.0, 42.0), 8.0),
    ("Spoke_P3", (-10.0, 44.0), (-36.0, 68.0), 8.0),       # medallion back gap -> plot 3 gate apron
    ("Spoke_P4", (10.0, 44.0), (36.0, 68.0), 8.0),
]
GATES = {1: ((-122.0, -30.0), (1, 0)), 2: ((-90.0, 42.0), (1, 0)), 3: ((-40.0, 78.0), (0, -1)),
         4: ((40.0, 78.0), (0, -1)), 5: ((90.0, 42.0), (-1, 0)), 6: ((122.0, -30.0), (-1, 0))}
SLOTS = {1: (-212, -60, -122, 0), 2: (-180, 12, -90, 72), 3: (-70, 78, -10, 168), 4: (10, 78, 70, 168),
         5: (90, 12, 180, 72), 6: (122, -60, 212, 0)}

# ------------------------------------------------------------------ fixed things (for the drawing + checks)
SLING = (0.53, -44.97)
PAD = (-9.0, -52.0, 10.0, -38.0)
INTRO_ZONE = (-12.0, -40.0, 24.0, 12.0)
LAUNCH_ZONE = (-14.0, -62.0, 15.0, -30.0)
TREADMILLS = {1: (-107.7, -46.0, "x"), 2: (-75.7, 26.0, "x"), 3: (-56.0, 63.7, "z"), 4: (56.0, 63.7, "z"),
              5: (75.7, 26.0, "x"), 6: (107.7, -46.0, "x")}
SIGNS = {1: (-116, -57), 2: (-84, 15), 3: (-67, 72), 4: (67, 72), 5: (84, 15), 6: (116, -57)}

REMOVE = {  # what pass 5 moves to ServerStorage._Backup_HubMakeover.Before (approx. centres)
    "Hub.Decor.Trees": [(-88, -51), (-82, -57), (88, -51), (82, -57), (-86, 73), (86, 73)],
    "Hub.Decor.Benches": [(-34, 16), (34, 16), (-11, 48), (11, 48)],
    "Hub.Decor.Garden": [(-111, -6), (-52, 38), (-150, 6), (-197, 6), (-38, 26), (110, -5), (56, -8), (55, 38),
                         (150, 6), (197, 7), (40, -29), (37, 26)],
    "Hub.Decor.GateBeds": [(-118, -13), (-86, 51), (-23, 75), (22, 74), (86, 52), (118, -13)],
    "Hub.Decor.AlleyBed": [(0, 90), (0, 110), (0, 130), (0, 150), (0, 165)],
    "Hub.Decor.Lamps (posts)": [(-26, -12), (29, -6), (-20, 50), (20, 50), (-75, -22), (75, -22), (-62, 44), (62, 44)],
    "Hub.Decor.Backdrop": [(0, 194)],
    "HalloweenDecor.Garden": [(-126, 6), (-172, 6), (-208, 6), (-74, -55), (74, -12), (126, 6), (172, 6), (208, 6),
                              (62, 2), (71, -56), (0, 70), (0, 100), (0, 140)],
    "HalloweenDecor.Spiders (16 of 20)": [(-133, 10), (-128, -1), (-164, 8), (-171, 2), (-170, 7), (-65, -54),
                                          (-69, -59), (71, -11), (74, -8), (131, 0), (170, 12), (173, 13), (60, 4),
                                          (79, -53), (74, -63), (69, -59)],
}


def board_poly(c, faces):
    fx, fz = faces
    rx, rz = -fz, fx        # along the board's width
    hw, hd = BOARD_W / 2, 1.6
    return [(c[0] + rx * hw + fx * hd, c[1] + rz * hw + fz * hd), (c[0] - rx * hw + fx * hd, c[1] - rz * hw + fz * hd),
            (c[0] - rx * hw - fx * hd, c[1] - rz * hw - fz * hd), (c[0] + rx * hw - fx * hd, c[1] + rz * hw - fz * hd)]


# ------------------------------------------------------------------ checks (quick sanity, the real ones run in Studio)
def checks():
    res = []
    # boards outside the intro zone's camera dolly (x 13.5..18, z -24..2): keep 2.5+ from the board polygon
    for n in ("RichestBoard", "TimeBoard", "SpeedBoard", "HeaviestBoard"):
        p = PLACE[n]
        poly = board_poly((p["pivot"][0], p["pivot"][2]), p["faces"])
        cam = [(18.0, 2.0), (16.0, -10.0), (13.5, -24.0)]
        dmin = min(min(math.dist(c, v) for v in poly) for c in cam)
        res.append(f"{n}: nearest intro dolly camera {dmin:.1f} studs")
    # stall rings vs the stall decks
    for s, m in (("UpgradeStall", "LeftMarket"), ("SellStall", "RightMarket")):
        r = PLACE[s]["ring"]
        c = PLACE[m]["centre"]
        inside = abs(r[0] - c[0]) + 6.1 <= 12 and abs(r[1] - c[2]) + 6.1 <= 12
        res.append(f"{s}: ring {r} fully on its deck = {inside}")
    # chest ring vs boards
    for n in ("RichestBoard", "TimeBoard", "SpeedBoard", "HeaviestBoard"):
        p = PLACE[n]
        poly = board_poly((p["pivot"][0], p["pivot"][2]), p["faces"])
        d = min(math.dist((0, 20), v) for v in poly)
        res.append(f"{n}: nearest corner to the chest centre {d:.1f} (pad ring r 8, medallion r 25.9)")
    # garland fit
    for name, a, b, w in LANES:
        L = math.dist(a, b)
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        worst = 1e9
        for n in ("RichestBoard", "TimeBoard", "SpeedBoard", "HeaviestBoard"):
            pp = PLACE[n]
            for v in board_poly((pp["pivot"][0], pp["pivot"][2]), pp["faces"]):
                t = max(0.0, min(L, (v[0] - a[0]) * u[0] + (v[1] - a[1]) * u[1]))
                q = (a[0] + u[0] * t, a[1] + u[1] * t)
                worst = min(worst, math.dist(v, q) - w / 2)
        res.append(f"lane {name}: nearest board corner {worst:.1f} outside the lane edge")
    scales = sorted({b["garland_scale"] for b in BAYS_ALL if b["garland"]})
    res.append(f"garlands: {sum(1 for b in BAYS_ALL if b['garland'])} (scales {scales})")
    res.append(f"pillars: {len(PILLARS)} (corner {sum(p['kind'] == 'corner' for p in PILLARS)}, "
               f"mid {sum(p['kind'] == 'mid' for p in PILLARS)}, junction {sum(p['kind'] == 'junction' for p in PILLARS)})")
    res.append(f"bats: {sum(b['bats'] for b in BAYS_ALL)}, vines: {sum(b['vine'] for b in BAYS_ALL)}, lanterns: {len(LANTERN_AT)}, "
               f"webs: {len(WEBS_AT)}, pumpkin clusters: {len(PUMPKINS_AT)}")
    pk = {(p["x"], p["z"]) for p in PILLARS}
    for q in LANTERN_AT + WEBS_AT:
        if q not in pk:
            res.append(f"FAIL: {q} is not a pillar")
    return res


# ------------------------------------------------------------------ the annotated top-down (over the real Studio capture)
def P(x, z, y=0.0):
    # screen_capture camera (0, 210, 56.5) -> (0, 0, 55), FOV 70, 1519 x 753: k = 376.5 / tan(35 deg) = 537.7
    depth = 210.0 - y
    k = 537.7
    return (759.5 + x * k / depth, 376.5 + (z - 55.0) * k / depth)


def draw():
    base = Image.open(os.path.join(ROOT, "shots", "before_01_top.jpg")).convert("RGB")
    W, H = base.size
    # fade the capture so the plan reads on top of it
    veil = Image.new("RGB", base.size, (255, 255, 255))
    img = Image.blend(base, veil, 0.45)
    ov = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    try:
        f = ImageFont.truetype("arialbd.ttf", 12)
        fs = ImageFont.truetype("arial.ttf", 10)
        fb = ImageFont.truetype("arialbd.ttf", 15)
    except OSError:
        f = fs = fb = ImageFont.load_default()

    def line(a, b, col, w, y=0.0):
        d.line([P(a[0], a[1], y), P(b[0], b[1], y)], fill=col, width=w)

    def poly(pts, fill=None, outline=None, y=0.0, width=1):
        d.polygon([P(x, z, y) for x, z in pts], fill=fill, outline=outline)
        if outline and width > 1:
            q = [P(x, z, y) for x, z in pts]
            d.line(q + [q[0]], fill=outline, width=width)

    def dot(c, r_px, fill, outline=None, y=0.0):
        x, yy = P(c[0], c[1], y)
        d.ellipse([x - r_px, yy - r_px, x + r_px, yy + r_px], fill=fill, outline=outline)

    def arrow(a, b, col, w=3):
        line(a, b, col, w)
        L = math.dist(a, b)
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        n = (-u[1], u[0])
        h1 = add(add(b, u, -3.5), n, 2.2)
        h2 = add(add(b, u, -3.5), n, -2.2)
        d.polygon([P(*b), P(*h1), P(*h2)], fill=col)

    def text(c, s, col=(20, 20, 30, 255), font=None, y=0.0, dx=0, dy=0):
        x, yy = P(c[0], c[1], y)
        d.text((x + dx, yy + dy), s, font=font or fs, fill=col)

    # removed clutter: red crosses
    for grp, pts in REMOVE.items():
        for c in pts:
            x, yy = P(c[0], c[1])
            d.line([x - 5, yy - 5, x + 5, yy + 5], fill=(220, 30, 30, 230), width=2)
            d.line([x - 5, yy + 5, x + 5, yy - 5], fill=(220, 30, 30, 230), width=2)
    # ground: aprons along the walls, lanes, gate aprons, medallion
    for e in EDGES:
        a2, b2 = add(e["a"], e["n"], -1.5), add(e["b"], e["n"], -1.5)
        line(a2, b2, GROUND["apron"] + (200,), 7)
    for name, a, b, w in LANES:
        L = math.dist(a, b)
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        n = (-u[1], u[0])
        pts = [add(a, n, w / 2), add(b, n, w / 2), add(b, n, -w / 2), add(a, n, -w / 2)]
        poly(pts, fill=GROUND["lane"] + (235,), outline=GROUND["lane_edge"] + (255,), width=2)
    for pid, (g, F) in GATES.items():
        R = (-F[1], F[0])
        pts = [add(add(g, R, 8), F, 0.5), add(add(g, R, -8), F, 0.5), add(add(g, R, -8), F, 10.5), add(add(g, R, 8), F, 10.5)]
        poly(pts, fill=GROUND["lane"] + (235,), outline=GROUND["lane_edge"] + (255,), width=2)
    for pid, (x0, z0, x1, z1) in SLOTS.items():
        poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], outline=GROUND["kerb"] + (255,), width=3)
    cx, cz = P(0, 20)
    r = 25.9 * 537.7 / 210
    d.ellipse([cx - r, cz - r, cx + r, cz + r], outline=GROUND["medallion_band"] + (255,), width=4)
    # walls: panel band + pillars
    for e in EDGES:
        mid = (WALL["panel_d"][0] + WALL["panel_d"][1]) / 2
        a2, b2 = add(e["a"], e["n"], mid), add(e["b"], e["n"], mid)
        line(a2, b2, COLOURS["BODY"] + (255,), 15, y=24)
        line(add(e["a"], e["n"], 0.4), add(e["b"], e["n"], 0.4), COLOURS["CAP"] + (255,), 3, y=25.6)
    for e in EDGES:
        m = add(((e["a"][0] + e["b"][0]) / 2, (e["a"][1] + e["b"][1]) / 2), e["n"], 11)
        text(m, f"E{e['i']}", (20, 30, 90, 255), f, y=24, dx=-8, dy=-6)
    for p in PILLARS:
        c = (p["x"], p["z"])
        col = (30, 40, 80, 255) if p["kind"] != "junction" else (120, 20, 120, 255)
        rr = 6 if p["kind"] != "junction" else 8
        x, yy = P(c[0], c[1], 27)
        d.rectangle([x - rr, yy - rr, x + rr, yy + rr], fill=col, outline=COLOURS["CAP"] + (255,))
    # wall decor
    for b in BAYS_ALL:
        a = add(b["a"], b["u"], 3.0)
        bb = add(b["b"], b["u"], -3.0)
        a, bb = add(a, b["n"], -0.5), add(bb, b["n"], -0.5)
        if b["garland"]:
            line(a, bb, (240, 120, 30, 255), 4, y=21)
        if b["vine"]:
            line(a, bb, (40, 150, 60, 255), 9, y=24)
            text(b["mid"], "HANDS", (20, 90, 30, 255), f, y=24, dx=-20, dy=12)
        if b["bats"]:
            for i in range(b["bats"]):
                q = add(add(b["mid"], b["u"], (i - 1.5) * 4.5), b["n"], -6)
                dot(q, 3, (20, 20, 20, 255), y=16)
    for c in LANTERN_AT:
        x, yy = P(c[0], c[1], 27)
        pts = [(x + 11 * math.cos(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45),
                yy - 11 * math.sin(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45)) for i in range(10)]
        d.polygon(pts, fill=(255, 215, 40, 255), outline=(90, 60, 0, 255))
    for c in PUMPKINS_AT:
        dot(c, 6, (255, 120, 0, 255), (90, 40, 0, 255))
    for c in WEBS_AT:
        x, yy = P(c[0], c[1], 24)
        d.line([x - 9, yy, x + 9, yy], fill=(255, 255, 255, 255), width=2)
        d.line([x, yy - 9, x, yy + 9], fill=(255, 255, 255, 255), width=2)
        d.ellipse([x - 6, yy - 6, x + 6, yy + 6], outline=(255, 255, 255, 255), width=2)
    # snapped placements
    for n in ("LeftMarket", "RightMarket"):
        c = PLACE[n]["centre"]
        poly([(c[0] - 12, c[2] - 12), (c[0] + 12, c[2] - 12), (c[0] + 12, c[2] + 12), (c[0] - 12, c[2] + 12)],
             fill=(200, 160, 110, 200), outline=(110, 70, 40, 255), width=2)
    for n, col in (("UpgradeStall", (40, 110, 230, 255)), ("SellStall", (40, 170, 70, 255))):
        p = PLACE[n]["plinth"]
        poly([(p[0] - 6, p[2] - 3.2), (p[0] + 6, p[2] - 3.2), (p[0] + 6, p[2] + 3.2), (p[0] - 6, p[2] + 3.2)], fill=col)
        rc = PLACE[n]["ring"]
        rr = 6.06 * 537.7 / 210
        x, yy = P(rc[0], rc[1])
        d.ellipse([x - rr, yy - rr, x + rr, yy + rr], outline=(0, 230, 255, 255) if "Up" in n else (255, 220, 0, 255), width=3)
        arrow((p[0], p[2]), (p[0], p[2] + 14), (10, 10, 10, 255))
        text((p[0] - 9, p[2] - 8), n.replace("Stall", " stall"), (10, 10, 10, 255), f)
    for n in ("RichestBoard", "TimeBoard", "SpeedBoard", "HeaviestBoard"):
        p = PLACE[n]
        c = (p["pivot"][0], p["pivot"][2])
        col = (40, 110, 230, 255) if p["pivot"][0] < 0 else (40, 170, 70, 255)
        poly(board_poly(c, p["faces"]), fill=col, outline=(10, 10, 10, 255), width=2)
        arrow(c, add(c, p["faces"], 10), (10, 10, 10, 255))
        text(c, n.replace("Board", ""), (10, 10, 10, 255), f, dx=-18, dy=10 if p["pivot"][2] > 20 else -22)
    x, yy = P(0, 20)
    rr = 8 * 537.7 / 210
    d.ellipse([x - rr, yy - rr, x + rr, yy + rr], outline=(150, 255, 0, 255), width=4)
    poly([(-3.2, 17.9), (3.2, 17.9), (3.2, 22.1), (-3.2, 22.1)], fill=(200, 30, 30, 255))
    arrow((0, 17.9), (0, 10), (10, 10, 10, 255))
    text((5, 16), "Chest + FREE zone", (10, 10, 10, 255), f)
    sx0, sy0 = P(-8, 44)
    sx1, sy1 = P(8, 60)
    d.rectangle([sx0, sy0, sx1, sy1], outline=(10, 10, 10, 255), width=2)
    text((-7, 49), "SPAWN", (10, 10, 10, 255), f)
    arrow((0, 44), (0, 37), (10, 10, 10, 255))
    # intro + launch zones
    for zz, col, lab in ((INTRO_ZONE, (230, 120, 40, 255), "intro"), (LAUNCH_ZONE, (200, 40, 40, 255), "launch")):
        x0, z0, x1, z1 = zz
        poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], outline=col, width=2)
        text((x0 + 1, z1 - 7), lab, col, fs)
    # legend
    lx, ly = 1180, 455
    d.rectangle([lx - 8, ly - 8, lx + 330, ly + 292], fill=(255, 255, 255, 235), outline=(40, 40, 40, 255))
    rows = [((30, 40, 80, 255), "wall pillar (42) / magenta = runway-junction tower"),
            (COLOURS["BODY"] + (255,), "big wall 25.6 tall + light coping"),
            ((240, 120, 30, 255), "pumpkin garland, one per bay (39)"),
            ((40, 150, 60, 255), "pumpkin HANDS (VineGrip) on the back wall"),
            ((255, 215, 40, 255), "wall lantern = the 8 night-boost lamps"),
            ((20, 20, 20, 255), "flat wall bats (12, 3 flocks)"),
            ((255, 120, 0, 255), "pumpkin cluster at the wall foot (5)"),
            ((150, 150, 150, 255), "corner web + spider (4)"),
            (GROUND["lane"] + (255,), "lanes + gate aprons (light paving)"),
            (GROUND["apron"] + (255,), "wall apron band (3 wide)"),
            (GROUND["kerb"] + (255,), "plot kerb (60 x 90 slot outline)"),
            ((220, 30, 30, 255), "removed clutter -> _Backup_HubMakeover"),
            ((10, 10, 10, 255), "arrow = the side a model's FRONT faces")]
    d.text((lx, ly - 4), "HUB MAKEOVER PLAN (top = runway / -Z)", font=f, fill=(10, 10, 10, 255))
    for i, (col, s) in enumerate(rows):
        yy = ly + 18 + i * 20
        d.rectangle([lx, yy, lx + 14, yy + 12], fill=col, outline=(40, 40, 40, 255))
        d.text((lx + 22, yy - 1), s, font=fs, fill=(10, 10, 10, 255))
    img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
    out = os.path.join(ROOT, "plan_annotated.png")
    img.save(out)
    return out


def main():
    plan = {"outline": OUTLINE, "wall": WALL, "colours": COLOURS, "edges": EDGES, "pillars": PILLARS,
            "bays": BAYS_ALL, "lanterns": LANTERN_AT, "pumpkins": PUMPKINS_AT, "webs": WEBS_AT, "place": PLACE,
            "ground": GROUND, "lanes": LANES, "gates": GATES, "slots": SLOTS}
    with open(os.path.join(ROOT, "plan.json"), "w") as fh:
        json.dump(plan, fh, indent=1, default=str)
    print("EDGES")
    for e in EDGES:
        print(f"  E{e['i']:>2} {e['a']} -> {e['b']} len {e['len']:.0f} bays {e['bays']} x {e['len'] / e['bays']:.1f} outward {e['n']}")
    print("PILLARS", len(PILLARS))
    for p in PILLARS:
        print(f"  ({p['x']:>7.1f},{p['z']:>6.1f}) {p['kind']:<8} edges {p['edges']}")
    for line in checks():
        print(line)
    print("wrote", draw())


if __name__ == "__main__":
    main()
