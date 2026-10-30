"""One-shot patch of ../../tools/hub_layout.py for the hub makeover (2026-10-21 night). Originals in tools/bak/."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "tools", "hub_layout.py")
s = open(P, encoding="utf-8").read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (old[:70], n)
    s = s.replace(old, new)


def cut_block(start_marker, end_marker_line_prefix, replacement):
    """replace from start_marker up to and including the first line starting with end_marker_line_prefix"""
    global s
    i0 = s.index(start_marker)
    i1 = s.index(end_marker_line_prefix, i0)
    i2 = s.index("\n", i1) + 1
    s = s[:i0] + replacement + s[i2:]


rep('PUMPKIN_PLOTS = (1, 3, 4, 6)            # pumpkin-egg clusters (10 x 7 x 8) sit on the 20-long gate beds only',
    'PUMPKIN_PLOTS = ()                      # (2026-10-21 makeover) gate beds + their pumpkin clusters removed (owner rule #1)')

rep('''STALL_RING_F = 4.53                     # Plinth (model pivot) -> ring centre along the facing (measured on both stalls)
STALLS = {
    "UpgradeStall": {"ring_c": (-100.0, -8.0), "ring": "blue"},
    "SellStall": {"ring_c": (100.0, -8.0), "ring": "gold"},
}
for _n, _st in STALLS.items():
    _st["F"] = look_at(_st["ring_c"], (0.5, -30.0))       # the counter + ring face the plaza front (where players come from)
    _st["pivot"] = add(_st["ring_c"], _st["F"], -STALL_RING_F)
    _st["deck"] = add(_st["ring_c"], _st["F"], -1.5)      # MarketCorners deck 24 x 24 (top y 0.6) under counter + ring''',
    '''STALL_RING_F = 5.636                    # Plinth (model pivot) -> ring centre along the facing (both stalls since the makeover)
# (2026-10-21 makeover, owner placement) the stalls stand at the plaza's FRONT CORNERS, backs to the orange runway-wall
# ends (x +-60..80), square to the front wall, counters facing +Z (the plaza). Decks 24 x 24 centred on the wall ends.
STALLS = {
    "UpgradeStall": {"ring_c": (-70.0, -48.364), "ring": "blue"},
    "SellStall": {"ring_c": (70.0, -48.364), "ring": "gold"},
}
for _n, _st in STALLS.items():
    _st["F"] = (0.0, 1.0)
    _st["pivot"] = add(_st["ring_c"], _st["F"], -STALL_RING_F)
    _st["deck"] = (_st["ring_c"][0], -47.6)''')

rep('''BOARDS = {                               # model pivot (y 10.2), F = the way the screen faces
    "RichestBoard": {"pivot": (-77.5, 63.5), "F": (K, -K)},
    "SpeedBoard": {"pivot": (-18.0, 63.0), "F": (0.0, -1.0)},
    "HeaviestBoard": {"pivot": (18.0, 63.0), "F": (0.0, -1.0)},
    "TimeBoard": {"pivot": (77.5, 63.5), "F": (-K, -K)},
}''', '''BOARDS = {                               # model pivot (y 10.25), F = the way the FRONT screen faces
    # (2026-10-21 makeover, owner placement) the 4 boards ring the Free Gift chest on the diagonals, screens facing it
    # (an arena); every board also has a back screen (<Board>_Back model) facing out, so both sides read
    "RichestBoard": {"pivot": (-26.0, 3.0), "F": (K, K)},
    "TimeBoard": {"pivot": (26.0, 3.0), "F": (-K, K)},
    "SpeedBoard": {"pivot": (-26.0, 37.0), "F": (K, -K)},
    "HeaviestBoard": {"pivot": (26.0, 37.0), "F": (-K, -K)},
}''')

rep('FREE_GIFT = {"pad": (0.0, 56.0), "F": (0.0, -1.0)}      # PadRing.Fill centre; chest faces the spawn (-Z)',
    'FREE_GIFT = {"pad": (0.0, 20.0), "F": (0.0, -1.0)}      # (makeover, owner placement) plaza centre; chest faces the slingshot (-Z)')
rep('SPAWN = {"centre": (0.0, 20.0), "size": 16}             # SpawnLocation 16 x 1 x 16 at y -0.4, on the medallion',
    'SPAWN = {"centre": (0.0, 52.0), "size": 16}             # (makeover) SpawnLocation 16 x 1 x 16 at y -0.4, behind the back board gap')

cut_block("DECOR = [\n", "]", "DECOR = []                               # (2026-10-21 makeover, owner rule #1) no trees / bushes / benches in the hub\n")

rep('''LAMP_SPOTS = [(-26.0, -12.0), (29.0, -6.0),  # (2026-10-21 builder) lamp 2 (27.5,-12) -> (29,-6): its cage hung 0.1 into the intro zone
              (-20.0, 50.0), (20.0, 50.0), (-75.0, -22.0), (75.0, -22.0), (-62.0, 44.0), (62.0, 44.0)]''',
    '''# (2026-10-21 makeover) the 8 lamps are WALL LANTERNS on pillars; LANTERN_PILLARS = the pillar points on the floor edge,
# LAMP_SPOTS = the floor point 2 studs in front of each (where its light pool falls; must be on the ground)
LANTERN_PILLARS = [(-14.6, 171.0), (14.6, 171.0), (-73.0, 78.0), (73.0, 78.0), (-81.0, -60.0), (81.0, -60.0), (-215.0, 12.0), (215.0, 12.0)]
LAMP_SPOTS = [(-14.6, 169.0), (14.6, 169.0), (-71.6, 76.6), (71.6, 76.6), (-83.0, -58.0), (83.0, -58.0), (-213.0, 10.0), (213.0, 10.0)]''')

rep('''ALLEY_BED = {"centre": (0.0, 125.0), "size": (8.0, 80.0)}  # low bushes / rocks / grass only (keeps the pumpkin view)''',
    '''ALLEY_BED = None                         # (makeover) the planted alley strip is gone: the alley is the paved spine lane''')

rep('''HALLOWEEN_BEDS = [(0.0, 70.0), (0.0, 100.0), (0.0, 140.0)]  # graves + thorn/TP bushes + dead grass, all low (< 6 tall)
PUMPKIN_ALLEY = [(0.0, 117.0), (0.0, 157.0)]  # the 2 pumpkin-egg clusters that do not fit the short beds of plots 2/5''',
    '''HALLOWEEN_BEDS = []                      # (makeover) removed (owner rule #1)
PUMPKIN_ALLEY = []                       # (makeover) replaced by WALL_PUMPKINS
# (makeover) pumpkin-egg clusters on the floor at the wall foot: the alley end (centred, between the pumpkin hands),
# beside the runway-junction towers, at the corridor ends between plots 1-2 / 5-6. r = footprint radius (no collision)
WALL_PUMPKINS = [((0.0, 164.0), 6.0), ((-90.0, -56.0), 5.0), ((90.0, -56.0), 5.0), ((-209.0, 6.0), 5.0), ((209.0, 6.0), 5.0)]''')

cut_block("_GARDEN_L = [\n", "GARDEN = [dict(", "GARDEN = []                              # (makeover, owner rule #1) the permanent garden clusters are gone\n")
cut_block("_HGARDEN_L = [\n", "HGARDEN = [dict(", "HGARDEN = []                             # (makeover, owner rule #1) the seasonal Halloween garden is gone\n")

rep('''BACKDROP = {"centre": (0.0, 194.0), "radius": 20.0, "tree_scale": 1.7}''',
    '''BACKDROP = None  # (makeover) island + tree moved to the backup; was {"centre": (0.0, 194.0), "radius": 20.0, "tree_scale": 1.7}''')

rep('''LAUNCH_ZONE = (-14.0, -62.0, 15.0, -30.0)  # pad + fork + the pulled-back pouch (z -32) + the hop-on lane''',
    '''LAUNCH_ZONE = (-14.0, -62.0, 15.0, -30.0)  # pad + fork + the pulled-back pouch (z -32) + the hop-on lane
# (2026-10-21 makeover) the IntroCutscene camera positions in the hub (shot 1 behind START, shot 2 side dolly START ->
# HOP_FROM, shot 3, the gate / skid / WHEW shots and the outro orbit round FINISH): every solid keeps 3+ studs from them.
# Solids in INTRO_EXEMPT may overlap INTRO_ZONE (owner-placed front boards; the cameras never look at them).
INTRO_CAMS = [(9.5, 4.5), (9.5, 2.5), (18.0, 2.0), (17.0, -4.0), (16.0, -10.0), (15.0, -16.0), (13.5, -24.0), (13.0, -16.0),
              (9.0, -30.0), (-3.6, -33.0), (-5.2, -31.0), (-13.5, -23.5), (-12.0, -14.0), (-6.0, -9.0)]
INTRO_EXEMPT = ("TimeBoard", "RichestBoard")''')

rep('''        s[f"GateBed_B{pid}"] = pp["bed_poly"]\n''', '')
rep('''    for i, p in enumerate(LAMP_SPOTS):
        s[f"Lamp{i + 1}"] = circle(p, 1.2)
    a = ALLEY_BED
    s["AlleyBed"] = rect_xz((a["centre"][0] - a["size"][0] / 2, a["centre"][1] - a["size"][1] / 2,
                             a["centre"][0] + a["size"][0] / 2, a["centre"][1] + a["size"][1] / 2))
''', '')
rep('''    for i, p in enumerate(HALLOWEEN_BEDS):
        s[f"HalloweenBed{i + 1}"] = circle(p, 4.0)
''', '''    for i, (p, r) in enumerate(WALL_PUMPKINS):
        s[f"HalloweenWallPumpkins{i + 1}"] = circle(p, r)
''')

open(P, "w", encoding="utf-8").write(s)
print("patched", P)
