"""One-shot patch of ../../tools/make_layout_lua.py for the hub makeover (2026-10-21 night)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "tools", "make_layout_lua.py")
s = open(P, encoding="utf-8").read()
BS = chr(92)  # backslash
TT = BS + "t"


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (old[:70], n)
    s = s.replace(old, new)


rep('''w("-- The redesigned hub (A HORSESHOE): FINAL world CFrames. Staging builds at Layout.OFFSET + these (Layout.stage(cf)).")''',
    '''w("-- The redesigned hub (A HORSESHOE): FINAL world CFrames. Staging builds at Layout.OFFSET + these (Layout.stage(cf)).")
w("-- (2026-10-21 makeover) owner-placed stalls / boards / Free Gift snapped, spawn moved, no trees / bushes / benches,")
w("-- lamps = wall lanterns, wall-foot pumpkin clusters. Docs: docs/plans/hub-2026-10-21/makeover/DESIGN.md")''')
rep('''    w(f"''' + TT + TT + '''bed = {cf(pp['bed'], 0, F)}, bedSize = Vector3.new({pp['bed_len']:.1f}, 0.8, 4), -- gate flower bed (Hub.Decor.GateBeds)")
''', '')
rep('''w(f"Layout.SPAWN = CFrame.new({H.SPAWN['centre'][0]}, -0.4, {H.SPAWN['centre'][1]}) -- SpawnLocation 16 x 1 x 16")''',
    '''w(f"Layout.SPAWN = CFrame.new({H.SPAWN['centre'][0]}, -0.4, {H.SPAWN['centre'][1]}) -- SpawnLocation 16 x 1 x 16 (LookVector -Z)")''')
rep('''bd = H.BACKDROP
w(f"Layout.BACKDROP = {{centre = {v3(bd['centre'][0], 0, bd['centre'][1])}, radius = {bd['radius']}, treeScale = {bd['tree_scale']}}} -- (owner call 3) floating garden island + giant tree beyond the back wall")''',
    '''w("Layout.BACKDROP = nil -- (makeover) the floating island + tree went to ServerStorage._Backup_HubMakeover.Before")''')
rep('''w("Layout.LAMP_SPOTS = { -- HalloweenDecor.StreetLamps (pivot = pole foot; arm/LookVector towards the plaza centre)")''',
    '''w("Layout.LANTERN_PILLARS = { -- (makeover) the 8 lamps = wall lanterns on these pillars (floor-edge points)")
for p in H.LANTERN_PILLARS:
    w(f"''' + TT + '''{v3(p[0], 0, p[1])},")
w("}")
w("Layout.LAMP_SPOTS = { -- (makeover) floor point 2 in front of each lantern pillar (its light pool; on the ground)")''')
rep('''a = H.ALLEY_BED
w(f"Layout.ALLEY_BED = {{cf = CFrame.new({a['centre'][0]}, 0.4, {a['centre'][1]}), size = Vector3.new({a['size'][0]}, 0.8, {a['size'][1]})}}")''',
    '''w("Layout.ALLEY_BED = nil -- (makeover) the alley is the paved spine lane")
w("Layout.WALL_PUMPKINS = { -- (makeover) pumpkin-egg clusters at the wall foot: footprint centre + radius (no collision)")
for p, r in H.WALL_PUMPKINS:
    w(f"''' + TT + '''{{pos = {v3(p[0], 0, p[1])}, r = {r}}},")
w("}")
w("Layout.INTRO_CAMS = { -- (makeover) IntroCutscene camera positions in the hub (x, z): solids keep 3+ studs away")
for c in H.INTRO_CAMS:
    w(f"''' + TT + '''Vector2.new({c[0]}, {c[1]}),")
w("}")
w("Layout.INTRO_EXEMPT = {" + ", ".join(f"{n} = true" for n in H.INTRO_EXEMPT) + "} -- owner-placed front boards may overlap INTRO_ZONE")''')
open(P, "w", encoding="utf-8").write(s)
print("patched", P)
