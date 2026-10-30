"""Writes ../HubLayout.lua (the ModuleScript source for ServerStorage.HubV2Kit.Layout) from hub_layout.py.
Run:  python make_layout_lua.py   (re-run after any change to hub_layout.py; never hand-edit HubLayout.lua)
All positions are FINAL world positions (the staging offset is added by the builder: Layout.OFFSET).
"""
import math
import os
import hub_layout as H

OUT = os.path.join(H.HERE, "..", "HubLayout.lua")


def v3(x, y, z):
    return f"Vector3.new({x:.3f}, {y:.3f}, {z:.3f})"


def cf(p, y, look):
    # CFrame.lookAt(pos, pos + look) with a flat look vector
    return f"CFrame.lookAt({v3(p[0], y, p[1])}, {v3(p[0] + look[0], y, p[1] + look[1])})"


ok, res, ds = H.checks()
assert ok, "hub_layout.py checks must ALL PASS before generating"
L = []
w = L.append
w("-- HubLayout (generated 2026-10-21 by docs/plans/hub-2026-10-21/tools/make_layout_lua.py from hub_layout.py - do not hand-edit)")
w("-- The redesigned hub (A HORSESHOE): FINAL world CFrames. Staging builds at Layout.OFFSET + these (Layout.stage(cf)).")
w("-- (2026-10-21 makeover) owner-placed stalls / boards / Free Gift snapped, spawn moved, no trees / bushes / benches,")
w("-- lamps = wall lanterns, wall-foot pumpkin clusters. Docs: docs/plans/hub-2026-10-21/makeover/DESIGN.md")
w("local Layout = {}")
w("Layout.OFFSET = Vector3.new(2000, 0, 0) -- Map.HubV2 is built here while the live hub keeps running; the swap moves it by -OFFSET")
w("function Layout.stage(cf) return CFrame.new(Layout.OFFSET) * cf end")
w(f"Layout.SLING = {v3(H.SLING[0], 1.0, H.SLING[1])} -- Hub.Slingshot pivot (fixed, never moved)")
w(f"Layout.PAD_CENTRE = Vector3.new(0.5, 0.5, -45) -- Hub.LaunchPlatform (fixed)")
w(f"Layout.ENTRY = {v3(H.ENTRY[0], 0, H.ENTRY[1])} -- just inside the LaunchGate: walking lines start here")
w(f"Layout.GATE_EDGES = {{{v3(H.GATE_EDGES[0][0], 0, H.GATE_EDGES[0][1])}, {v3(H.GATE_EDGES[1][0], 0, H.GATE_EDGES[1][1])}}}")
w(f"Layout.LINE_HALF = {{main = {H.MAIN_HALF}, fan = {H.FAN_HALF}}}")
x0, z0, x1, z1 = H.LAUNCH_ZONE
w(f"Layout.LAUNCH_ZONE = {{min = Vector3.new({x0}, 0, {z0}), max = Vector3.new({x1}, 40, {z1})}} -- nothing collidable inside")
x0, z0, x1, z1 = H.INTRO_ZONE
w(f"Layout.INTRO_ZONE = {{min = Vector3.new({x0}, 0, {z0}), max = Vector3.new({x1}, 12, {z1})}} -- IntroCutscene path + cameras: nothing taller than 0.8 inside")
w(f"Layout.PLOT_MAX = Vector2.new({H.W_MAX}, {H.L_MAX}) -- MaxWidth x MaxLength")
w("")
w("-- plots: Slot = 60 x 0.2 x 90 at y 0.1 (LookVector = towards the plaza); gate = Slot front edge centre")
w("Layout.PLOTS = {")
for pid, p in H.PLOTS.items():
    pp = H.plot_parts(pid)
    F = p["F"]
    w(f"\t[{pid}] = {{")
    w(f"\t\tslot = {cf(pp['slot_centre'], 0.1, F)},")
    w(f"\t\tgate = {v3(p['gate'][0], 0, p['gate'][1])},")
    w(f"\t\tspawnSpot = {v3(pp['spawn'][0], 0, pp['spawn'][1])}, -- BaseManager.spawnAtBase (8 out from the gate)")
    w(f"\t\ttreadmill = {cf(pp['tread'], 0.65, F)}, -- Treadmill_B{pid} pivot (LookVector = F, runner faces the plaza)")
    w(f"\t\ttreadExit = {v3(pp['exit'][0], 0, pp['exit'][1])}, -- where a jump-off lands (7.5 behind the belt)")
    w(f"\t\tsign = {cf(pp['sign'], 3.18, (-F[0], -F[1]))}, -- UpgradeSign_B{pid} pivot (LookVector = -F, board front faces the gate)")
    if pp["pumpkins"]:
        w(f"\t\tpumpkins = {cf(pp['pumpkins'], 0, F)}, -- Halloween pumpkin-egg cluster footprint centre (HalloweenDecor.PumpkinEggs)")
    w(f"\t\ttoSling = {ds[pid]:.1f},")
    w("\t},")
w("}")
w("")
w("-- stalls: model pivot = Plinth centre at y 0.9 (LookVector = the way the counter faces); deck = MarketCorners deck")
w("Layout.STALLS = {")
for n, st in H.STALLS.items():
    w(f"\t{n} = {{pivot = {cf(st['pivot'], 0.9, st['F'])}, ring = {v3(st['ring_c'][0], 0.6, st['ring_c'][1])}, "
      f"deck = {cf(st['deck'], 0.3, st['F'])}, deckSize = Vector3.new(24, 0.6, 24)}},")
w("}")
w("-- leaderboards: model pivot at y 10.2, LookVector = the way the screen faces")
w("Layout.BOARDS = {")
for n, b in H.BOARDS.items():
    w(f"\t{n} = {cf(b['pivot'], 10.2, b['F'])},")
w("}")
fg = H.FREE_GIFT
w(f"Layout.FREE_GIFT = {{pad = {v3(fg['pad'][0], 0, fg['pad'][1])}, look = Vector3.new({fg['F'][0]}, 0, {fg['F'][1]})}} -- PadRing.Fill centre; chest faces -Z")
w(f"Layout.SPAWN = CFrame.new({H.SPAWN['centre'][0]}, -0.4, {H.SPAWN['centre'][1]}) -- SpawnLocation 16 x 1 x 16 (LookVector -Z)")
w(f"Layout.MEDALLION = Vector3.new({H.MEDALLION['centre'][0]}, 0.2, {H.MEDALLION['centre'][1]}) -- Decor.Plaza (5 studded discs) centre")
w("")
w("-- permanent decor (Hub.Decor): kind = template name in ServerStorage.HubV2Kit.Templates; pos = ground point; look = facing")
w("Layout.DECOR = {")
for d in H.DECOR:
    face = d.get("face")
    look = H.look_at(d["pos"], face) if face else (0.0, -1.0)
    w(f"\t{{name = \"{d['name']}\", kind = \"{d['kind']}\", cf = {cf(d['pos'], 0, look)}, r = {d['r']}}},")
w("}")
w("-- (2026-10-21 builder, review MUST 13b) permanent garden clusters (Hub.Decor.Garden): centrepiece kind + footprint r;")
w("-- deck = true: stands on the MarketCorners deck (top y 0.6) behind its stall counter")
w("Layout.GARDEN = {")
for g in H.GARDEN:
    w(f"	{{name = \"{g['name']}\", kind = \"{g['kind']}\", pos = {v3(g['pos'][0], 0, g['pos'][1])}, r = {g['r']}, deck = {str(bool(g.get('deck'))).lower()}}},")
w("}")
w("-- (2026-10-21 builder, review MUST 14) the seasonal Halloween garden spots (HalloweenDecor.Garden): tree = live garden")
w("-- tree moved there with its spiders (nil = none), extra = bush kinds, r = ground footprint (nothing collides)")
w("Layout.HALLOWEEN_GARDEN = {")
for g in H.HGARDEN:
    tree = f'\"{g["tree"]}\"' if g["tree"] else "nil"
    extra = ", ".join(f'\"{e}\"' for e in g["extra"])
    w(f"	{{name = \"{g['name']}\", tree = {tree}, extra = {{{extra}}}, pos = {v3(g['pos'][0], 0, g['pos'][1])}, r = {g['r']}}},")
w("}")
w("Layout.BACKDROP = nil -- (makeover) the floating island + tree went to ServerStorage._Backup_HubMakeover.Before")
w(f"Layout.TREAD_ENVELOPE = {{rHalf = {H.TREAD_R_HALF}, fPlot = {H.TREAD_F_PLOT}, fPlaza = {H.TREAD_F_PLAZA}}} -- (MUST 4) all 11 tiers, pivot space")
w("Layout.LANTERN_PILLARS = { -- (makeover) the 8 lamps = wall lanterns on these pillars (floor-edge points)")
for p in H.LANTERN_PILLARS:
    w(f"\t{v3(p[0], 0, p[1])},")
w("}")
w("Layout.LAMP_SPOTS = { -- (makeover) floor point 2 in front of each lantern pillar (its light pool; on the ground)")
for p in H.LAMP_SPOTS:
    look = H.look_at(p, H.PLAZA_CENTRE)
    w(f"\t{cf(p, 0, look)},")
w("}")
w("Layout.ALLEY_BED = nil -- (makeover) the alley is the paved spine lane")
w("Layout.WALL_PUMPKINS = { -- (makeover) pumpkin-egg clusters at the wall foot: footprint centre + radius (no collision)")
for p, r in H.WALL_PUMPKINS:
    w(f"\t{{pos = {v3(p[0], 0, p[1])}, r = {r}}},")
w("}")
w("Layout.INTRO_CAMS = { -- (makeover) IntroCutscene camera positions in the hub (x, z): solids keep 3+ studs away")
for c in H.INTRO_CAMS:
    w(f"\tVector2.new({c[0]}, {c[1]}),")
w("}")
w("Layout.INTRO_EXEMPT = {" + ", ".join(f"{n} = true" for n in H.INTRO_EXEMPT) + "} -- owner-placed front boards may overlap INTRO_ZONE")
w(f"Layout.GIANT_PUMPKIN = {v3(*H.PUMPKIN)} -- GiantPumpkin.Pivot position (keep its rotation: face -Z)")
w("Layout.PUMPKIN_ALLEY = { -- the 2 pumpkin-egg clusters on the alley bed (footprint centres, fronts face -Z)")
for p in H.PUMPKIN_ALLEY:
    w(f"\t{cf(p, 0, (0.0, -1.0))},")
w("}")
w("Layout.HALLOWEEN_BEDS = {")
for p in H.HALLOWEEN_BEDS:
    w(f"\t{cf(p, 0, (0.0, -1.0))},")
w("}")
w("")
w("-- ground tiles (top y 0, 8 thick, like the old Hub.Floor): {name, min, max} in x/z")
w("Layout.GROUND = {")
for n, (gx0, gz0, gx1, gz1) in H.GROUND:
    w(f"\t{{name = \"{n}\", cf = CFrame.new({(gx0 + gx1) / 2}, -4, {(gz0 + gz1) / 2}), size = Vector3.new({gx1 - gx0}, 8, {gz1 - gz0})}},")
w("}")
w(f"-- edge walls ({H.WALL_T} thick x {H.WALL_H} tall, OUTSIDE the floor) + Map.Bounds columns ({H.BOUND_T} thick, y 0..1040, outside the walls)")
w("Layout.EDGES = {")
for e in H.edge_segments():
    u = e["dir"]
    # wall part: X axis along the edge -> CFrame.fromMatrix(pos, right = edge dir, up)
    wc, bc = e["wall_c"], e["bound_c"]
    w(f"\t{{i = {e['i']}, wall = CFrame.fromMatrix({v3(wc[0], H.WALL_H / 2, wc[1])}, {v3(u[0], 0, u[1])}, Vector3.yAxis), "
      f"wallSize = Vector3.new({e['wall_len']:.1f}, {H.WALL_H}, {H.WALL_T}), "
      f"bound = CFrame.fromMatrix({v3(bc[0], 520, bc[1])}, {v3(u[0], 0, u[1])}, Vector3.yAxis), "
      f"boundSize = Vector3.new({e['bound_len']:.1f}, 1040, {H.BOUND_T})}},")
w("}")
w("-- the runway bounds columns that reached into the hub (end at z -49) are cut back to end at the runway wall (z -60)")
w("Layout.RUNWAY_BOUNDS_FIX = {Runway_L_1 = {x = -70, zMin = -1266, zMax = -60}, Runway_R_1 = {x = 70, zMin = -1266, zMax = -60}}")
w("")
w("-- base sizes per rebirth for the new max (RebirthConfig.baseSize(r, 60, 90))")
sizes = ", ".join(f"[{r}] = Vector2.new({H.base_size(r)[0]}, {H.base_size(r)[1]})" for r in range(6))
w(f"Layout.SIZES = {{{sizes}}}")
w("return Layout")
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(L) + "\n")
print(OUT)
