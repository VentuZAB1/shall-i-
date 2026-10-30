# make_payloads3.py (2026-10-22 UI polish, phase 2 round 3): the second test pass. Writes payloads/round3/<Script>.json.
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "round3")
SPS = "game.StarterPlayer.StarterPlayerScripts."
P = {}
def add(path, old, new): P.setdefault(path, []).append((old, new))

MC = "game.StarterGui.MainMenu.MenuController"
add(MC,
"Rebirth = {2.15, 1.45}, Sell = {1.5, 1.05}, Settings = {2.2, 1.3}}",
"Rebirth = {2.15, 1.45}, Sell = {1.5, 1.05}, Settings = {2.3, 1.3}} -- (round 3: Settings 2.3, rows 44+ px apart at the phone scale)")
add(MC,
"\tB.tapArea(f, flip, nil, f.Parent.Parent) -- (2026-10-22 UI polish, M7; round 2: kept inside its row)",
"\tB.tapArea(f, flip, 44.5) -- (2026-10-22 UI polish, M7: 44 px tall, the rows are 44+ px apart)")
add(MC,
"B.tapArea(minus, volDown, nil, minus.Parent.Parent) B.tapArea(plus, volUp, nil, plus.Parent.Parent) -- (2026-10-22 UI polish, M7: the - / + were 22 x 18 pt on a phone)",
"B.tapArea(minus, volDown, 44.5) B.tapArea(plus, volUp, 44.5) -- (2026-10-22 UI polish, M7: the - / + were 22 x 18 pt on a phone)")
add(MC,
"B.tapArea(prev, songPrev, nil, prev.Parent.Parent) B.tapArea(nxt, songNext, nil, nxt.Parent.Parent) -- (2026-10-22 UI polish, M7)",
"B.tapArea(prev, songPrev, 44.5) B.tapArea(nxt, songNext, 44.5) -- (2026-10-22 UI polish, M7)")

SC = SPS + "StreakClient"
add(SC,
"\t\tlocal title = text(face, \"Secret\", UDim2.fromScale(0.48, 0.15), UDim2.fromScale(0.73, 0.405), 0.1)",
"\t\tlocal title = text(face, \"Secret\", UDim2.fromScale(0.48, 0.17), UDim2.fromScale(0.73, 0.4), 0.1) -- (round 3: large text, 3:1 on the rainbow's purple)")

SH = SPS + "ShopClientLegacy"
add(SH, "tl.Padding = UDim.new(0.008, 0)", "tl.Padding = UDim.new(0.002, 0)")
add(SH,
"\t\tslot.Size = UDim2.fromScale(1, 0.192)\n\t\tslot.LayoutOrder = i\n\t\tslot.Parent = tabs",
"\t\tslot.Size = UDim2.fromScale(1, 0.198) -- (round 3: 44+ px tap slots at the phone scale)\n\t\tslot.LayoutOrder = i\n\t\tslot.Parent = tabs")

IX = SPS + "IndexClientLegacy"
add(IX,
"\tlocal holder, face = B.brick(page, \"Tab\" .. i, UDim2.fromScale(0.125, 0.128), UDim2.fromScale(0.0625, 0.07 + (i - 1) * 0.142),",
"\tlocal holder, face = B.brick(page, \"Tab\" .. i, UDim2.fromScale(0.125, 0.138), UDim2.fromScale(0.0625, 0.07 + (i - 1) * 0.142), -- (round 3: 0.128)")
add(IX,
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.96, 0.44), UDim2.fromScale(0.5, 0.27), 0.09)\n"
"\tname.Text = string.upper(a.name)\n"
"\tlocal prog = B.text(face, \"Prog\", B.FRED, WHITE, UDim2.fromScale(0.5, 0.36), UDim2.fromScale(0.36, 0.72), 0.08)\n"
"\tlocal star = B.image(face, \"Star\", STAR_ICON, UDim2.fromScale(0.3, 0.3), UDim2.fromScale(0.83, 0.72))\n"
"\tlocal sr = Instance.new(\"UIAspectRatioConstraint\") sr.Parent = star\n"
"\tlocal bang = B.frame(face, \"Ready\", UDim2.fromScale(0.3, 0.3), UDim2.fromScale(0.83, 0.72), Color3.fromRGB(235, 45, 45))",
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.96, 0.42), UDim2.fromScale(0.5, 0.26), 0.09)\n"
"\tname.Text = string.upper(a.name)\n"
"\tlocal prog = B.text(face, \"Prog\", B.FRED, WHITE, UDim2.fromScale(0.46, 0.42), UDim2.fromScale(0.3, 0.73), 0.08)\n"
"\tlocal star = B.image(face, \"Star\", STAR_ICON, UDim2.fromScale(0.26, 0.26), UDim2.fromScale(0.8, 0.7))\n"
"\tlocal sr = Instance.new(\"UIAspectRatioConstraint\") sr.Parent = star\n"
"\tlocal bang = B.frame(face, \"Ready\", UDim2.fromScale(0.26, 0.26), UDim2.fromScale(0.8, 0.7), Color3.fromRGB(235, 45, 45))")
add(IX,
"\tB.tapArea(face, pick) -- (2026-10-22 UI polish, M7)\nend",
"\t-- (2026-10-22 UI polish, M7) the tap area fills the tab's whole slot in the column (6 stacked tabs: on a phone the slot\n"
"\t-- is ~31 pt tall, 44+ pt wide; neighbouring areas never overlap)\n"
"\tlocal slot = B.frame(page, \"TabSlot\" .. i, UDim2.fromScale(0.125, 0.142), UDim2.fromScale(0.0625, 0.07 + (i - 1) * 0.142))\n"
"\tB.tapArea(face, pick, nil, slot)\nend")
add(IX,
"local hSub = B.text(header, \"Sub\", B.FRED, WHITE, UDim2.fromScale(0.5, 0.26), UDim2.fromScale(0.04, 0.76), 0.06, Vector2.new(0, 0.5))",
"local hSub = B.text(header, \"Sub\", B.FRED, WHITE, UDim2.fromScale(0.5, 0.3), UDim2.fromScale(0.04, 0.78), 0.06, Vector2.new(0, 0.5)) -- (round 3, M5: 0.26 at 0.76)")
add(IX,
"\tlocal _, pill = B.brick(face, \"Chance\", UDim2.fromScale(0.62, 0.13), UDim2.fromScale(0.5, 0.86), WHITE, NAVY, {radius = 0.5, stroke = 0.08})",
"\tlocal _, pill = B.brick(face, \"Chance\", UDim2.fromScale(0.62, 0.15), UDim2.fromScale(0.5, 0.865), WHITE, NAVY, {radius = 0.5, stroke = 0.08}) -- (round 3: 0.13)")
add(IX,
"\tlocal q = B.text(face, \"Q\", B.LUCKY, Color3.fromRGB(255, 255, 255), UDim2.fromScale(0.5, 0.3), UDim2.fromScale(0.5, 0.45), 0.06)",
"\tlocal q = B.text(face, \"Q\", B.LUCKY, Color3.fromRGB(255, 255, 255), UDim2.fromScale(0.5, 0.26), UDim2.fromScale(0.5, 0.5), 0.06) -- (round 3: clear of the SECRET tag)")
add(IX,
"\tlocal badge = B.frame(face, \"Secret\", UDim2.fromScale(0.66, 0.085), UDim2.fromScale(0.5, 0.29), Color3.fromRGB(255, 70, 150)) -- (under the 2-line name)",
"\tlocal badge = B.frame(face, \"Secret\", UDim2.fromScale(0.9, 0.11), UDim2.fromScale(0.5, 0.29), Color3.fromRGB(255, 70, 150)) -- (under the 2-line name; round 3: 0.66 x 0.085)")
add(IX,
"\tlocal bt = B.text(badge, \"T\", B.LUCKY, WHITE, UDim2.fromScale(0.9, 0.78), UDim2.fromScale(0.5, 0.52), 0.1)\n\tbt.Text = \"SECRET\" bt.ZIndex = 4",
"\tlocal bt = B.text(badge, \"T\", B.LUCKY, WHITE, UDim2.fromScale(0.92, 0.84), UDim2.fromScale(0.5, 0.52), 0.1)\n\tbt.Text = \"SECRET\" bt.ZIndex = 4")
add(IX,
"\tlocal rowF = B.frame(insp, \"Stat\" .. k, UDim2.fromScale(0.86, 0.062), UDim2.fromScale(0.5, y), Color3.fromRGB(22, 26, 50))",
"\tlocal rowF = B.frame(insp, \"Stat\" .. k, UDim2.fromScale(0.86, 0.068), UDim2.fromScale(0.5, y), Color3.fromRGB(22, 26, 50)) -- (round 3, M5: 0.062)")
add(IX,
"\tlocal l = B.text(rowF, \"L\", B.FRED, Color3.fromRGB(190, 205, 255), UDim2.fromScale(0.5, 0.75), UDim2.fromScale(0.05, 0.52), 0.08, Vector2.new(0, 0.5))",
"\tlocal l = B.text(rowF, \"L\", B.FRED, Color3.fromRGB(190, 205, 255), UDim2.fromScale(0.5, 0.8), UDim2.fromScale(0.05, 0.52), 0.08, Vector2.new(0, 0.5))")
add(IX,
"\tlocal v = B.text(rowF, \"V\", B.LUCKY, WHITE, UDim2.fromScale(0.44, 0.75), UDim2.fromScale(0.95, 0.52), 0.08, Vector2.new(1, 0.5))",
"\tlocal v = B.text(rowF, \"V\", B.LUCKY, WHITE, UDim2.fromScale(0.44, 0.8), UDim2.fromScale(0.95, 0.52), 0.08, Vector2.new(1, 0.5))")
add(IX,
"\t\t\t{\"Income (best KG)\", known and",
"\t\t\t-- (2026-10-22 UI polish, M5: short stat names, were \"Income (best KG)\" / \"Best weight\" / \"Hatch chance\")\n\t\t\t{\"Income\", known and")
add(IX, "\t\t\t{\"Best weight\", known and", "\t\t\t{\"Best KG\", known and")
add(IX, "\t\t\t{\"Hatch chance\", pctText(odds) .. bonus},", "\t\t\t{\"Chance\", pctText(odds) .. bonus},")

os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT): os.remove(os.path.join(OUT, f))
for path, edits in P.items():
    name = path.split(".")[-1]
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"file_path": path, "datamodel_type": "Edit", "edits": [{"old_string": o, "new_string": n} for o, n in edits]}, f, ensure_ascii=False, indent=1)
    print(f"{name:24s} {len(edits)} edits")
print("total", sum(len(e) for e in P.values()))
