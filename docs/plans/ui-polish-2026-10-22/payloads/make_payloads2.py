# make_payloads2.py (2026-10-22 UI polish, phase 2 round 2): fixes from the first test pass. Writes payloads/round2/<Script>.json.
# old_strings = the live source after round 1 (round-1 new_strings or untouched original lines).
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "round2")
SPS = "game.StarterPlayer.StarterPlayerScripts."
P = {}
def add(path, old, new): P.setdefault(path, []).append((old, new))

# ---------------------------------------------------------------- BrickUI: tapArea 46 px default (pixel rounding) + clampTo
BR = "game.ReplicatedStorage.BrickUI"
add(BR,
"function BrickUI.tapArea(button, onActivate, minPx)\n\tminPx = minPx or 44\n",
"-- (round 2) default 46 (pixel rounding left some at 43 px); clampTo = a frame the area must not outgrow (a Settings row,\n"
"-- a Shop rail slot), so neighbouring buttons' areas never overlap\n"
"function BrickUI.tapArea(button, onActivate, minPx, clampTo)\n\tminPx = minPx or 46\n")
add(BR,
"\t\tlocal fx, fy = math.max(1, minPx / a.X), math.max(1, minPx / a.Y)\n",
"\t\tlocal fx, fy = math.max(1, minPx / a.X), math.max(1, minPx / a.Y)\n"
"\t\tif clampTo and clampTo.AbsoluteSize.X > 0 then\n"
"\t\t\tfx = math.min(fx, math.max(1, clampTo.AbsoluteSize.X / a.X))\n"
"\t\t\tfy = math.min(fy, math.max(1, clampTo.AbsoluteSize.Y / a.Y))\n"
"\t\tend\n")

# ---------------------------------------------------------------- MenuController
MC = "game.StarterGui.MainMenu.MenuController"
add(MC,
"\tlocal LAYOUT = {Shop = {2.28, 1.82, 0.11}, Index = {2.3, 1.85}, Gift = {2.25, 1.32}, Rebirth = {2.0, 1.45}, Sell = {1.5, 1.05}, Settings = {2.05, 1.3}}",
"\t-- (round 2) Shop {2.28, 1.55}: as wide as the money pills allow (fitScale), taller; Index {2.3, 1.6} the same width, a\n"
"\t-- bit shorter than the Shop (M10: the Shop stays the biggest); Rebirth 2.15 and Settings 2.2 for the 16 px floor + 44 pt rows\n"
"\tlocal LAYOUT = {Shop = {2.28, 1.55, 0.11}, Index = {2.3, 1.6}, Gift = {2.25, 1.32}, Rebirth = {2.15, 1.45}, Sell = {1.5, 1.05}, Settings = {2.2, 1.3}}")
add(MC,
"\tlocal limitBottom = workspace.CurrentCamera.ViewportSize.Y - GuiService:GetGuiInset().Y - 6 -- the hotbar hides while a window is open\n"
"\t-- don't cover the money / speed pills: if the window reaches over them sideways, stop above them\n"
"\tlocal hud = player.PlayerGui:FindFirstChild(\"SpeedUI\")\n"
"\tlocal pills = hud and hud:FindFirstChild(\"Holder\")\n"
"\tif pills and win.AbsolutePosition.X < pills.AbsolutePosition.X + pills.AbsoluteSize.X and pills.AbsolutePosition.Y > top then\n"
"\t\tlimitBottom = math.min(limitBottom, pills.AbsolutePosition.Y - 6)\n"
"\tend\n"
"\t-- first slide up (as far as the top allows), then shrink if it still doesn't fit\n"
"\tlocal over = top + h - limitBottom\n"
"\tlocal shift = 0\n"
"\tif over > 0 then shift = math.min(over, math.max(0, top - limitTop)) end\n"
"\twin.Position = basePos - UDim2.fromOffset(0, shift)\n"
"\ttop -= shift\n"
"\tlocal centre = top + h / 2\n"
"\tlocal k = math.min(1, (limitBottom - centre) * 2 / h, (centre - limitTop) * 2 / h)\n"
"\treturn math.max(k, 0.5)\nend",
"\tlocal screenBottom = workspace.CurrentCamera.ViewportSize.Y - GuiService:GetGuiInset().Y - 6 -- the hotbar hides while a window is open\n"
"\tlocal limitBottom = screenBottom\n"
"\t-- don't cover the money / speed pills: if the window reaches over them sideways, stop above them\n"
"\t-- (2026-10-22 UI polish, M5 / M10) ... or, when that keeps it bigger, get just narrow enough to clear them sideways: a\n"
"\t-- wide window (Shop, Index) used to be shrunk all the way above the pills (the Shop came out at 0.61 of the screen)\n"
"\tlocal hud = player.PlayerGui:FindFirstChild(\"SpeedUI\")\n"
"\tlocal pills = hud and hud:FindFirstChild(\"Holder\")\n"
"\tlocal kSide\n"
"\tif pills and win.AbsolutePosition.X < pills.AbsolutePosition.X + pills.AbsoluteSize.X and pills.AbsolutePosition.Y > top then\n"
"\t\tlimitBottom = math.min(limitBottom, pills.AbsolutePosition.Y - 6)\n"
"\t\tlocal w = win.AbsoluteSize.X\n"
"\t\tif w > 0 then kSide = (win.AbsolutePosition.X + w / 2 - (pills.AbsolutePosition.X + pills.AbsoluteSize.X + 6)) * 2 / w end\n"
"\tend\n"
"\t-- first slide up (as far as the top allows), then shrink if it still doesn't fit\n"
"\tlocal function fitTo(lb)\n"
"\t\tlocal over = top + h - lb\n"
"\t\tlocal shift = 0\n"
"\t\tif over > 0 then shift = math.min(over, math.max(0, top - limitTop)) end\n"
"\t\tlocal centre = top - shift + h / 2\n"
"\t\treturn math.min(1, (lb - centre) * 2 / h, (centre - limitTop) * 2 / h), shift\n"
"\tend\n"
"\tlocal k, shift = fitTo(limitBottom)\n"
"\tif kSide and kSide > k then\n"
"\t\tlocal k2, shift2 = fitTo(screenBottom)\n"
"\t\tk2 = math.min(k2, kSide)\n"
"\t\tif k2 > k then k, shift = k2, shift2 end\n"
"\tend\n"
"\twin.Position = basePos - UDim2.fromOffset(0, shift)\n"
"\treturn math.max(k, 0.5)\nend")
add(MC,
"\tB.tapArea(f, flip) -- (2026-10-22 UI polish, M7)",
"\tB.tapArea(f, flip, nil, f.Parent.Parent) -- (2026-10-22 UI polish, M7; round 2: kept inside its row)")
add(MC,
"B.tapArea(minus, volDown) B.tapArea(plus, volUp) -- (2026-10-22 UI polish, M7: the - / + were 22 x 18 pt on a phone)",
"B.tapArea(minus, volDown, nil, minus.Parent.Parent) B.tapArea(plus, volUp, nil, plus.Parent.Parent) -- (2026-10-22 UI polish, M7: the - / + were 22 x 18 pt on a phone)")
add(MC,
"B.tapArea(prev, songPrev) B.tapArea(nxt, songNext) -- (2026-10-22 UI polish, M7)",
"B.tapArea(prev, songPrev, nil, prev.Parent.Parent) B.tapArea(nxt, songNext, nil, nxt.Parent.Parent) -- (2026-10-22 UI polish, M7)")

# ---------------------------------------------------------------- StreakClient (Day 7 ribbon label floor + insets)
SC = SPS + "StreakClient"
add(SC,
"\t\tlocal title = text(face, \"Secret\", UDim2.fromScale(0.48, 0.15), UDim2.fromScale(0.73, 0.37), 0.1)",
"\t\tlocal title = text(face, \"Secret\", UDim2.fromScale(0.48, 0.15), UDim2.fromScale(0.73, 0.405), 0.1)")
add(SC,
"\t\tc.lines[1] = text(face, \"Line1\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.53))\n"
"\t\tc.lines[2] = text(face, \"Line2\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.68))\n"
"\t\tc.lines[3] = text(face, \"Line3\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.83))\n"
"\t\tlocal rh, rf = B.brick(face, \"Ribbon\", UDim2.fromScale(0.32, 0.19), UDim2.fromScale(0.81, 0.17), C(255, 32, 80)) -- (M1 / M5: 0.2 x 0.13 at 0.87, 0.115; its label was 11 px)\n"
"\t\trh.Rotation = 4\n"
"\t\trh.ZIndex = 7\n"
"\t\tlocal rl = text(rf, \"Label\", UDim2.fromScale(0.9, 0.72), UDim2.fromScale(0.5, 0.5), 0.1)",
"\t\tc.lines[1] = text(face, \"Line1\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.555))\n"
"\t\tc.lines[2] = text(face, \"Line2\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.7))\n"
"\t\tc.lines[3] = text(face, \"Line3\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.845))\n"
"\t\tlocal rh, rf = B.brick(face, \"Ribbon\", UDim2.fromScale(0.36, 0.19), UDim2.fromScale(0.79, 0.185), C(255, 32, 80)) -- (M1 / M5: 0.2 x 0.13 at 0.87, 0.115; its label was 11 px)\n"
"\t\trh.Rotation = 4\n"
"\t\trh.ZIndex = 7\n"
"\t\tlocal rl = text(rf, \"Label\", UDim2.fromScale(0.9, 0.8), UDim2.fromScale(0.5, 0.5), 0.1)")
add(SC,
"\tlocal bh, bf = B.brick(face, \"Claim\", UDim2.fromScale(big and 0.42 or 0.86, 0.24), UDim2.fromScale(big and 0.24 or 0.5, 0.83), OFF, nil, {button = true})",
"\tlocal bh, bf = B.brick(face, \"Claim\", UDim2.fromScale(big and 0.42 or 0.86, 0.23), UDim2.fromScale(big and 0.24 or 0.5, 0.825), OFF, nil, {button = true})")

# ---------------------------------------------------------------- PlaytimeClient: potion names readable on the navy cells
PC = SPS + "PlaytimeClient"
add(PC,
"\t\t\tc.top.Text = potion.name\n\t\t\tc.top.TextColor3 = potion.color",
"\t\t\tc.top.Text = potion.name\n\t\t\tc.top.TextColor3 = potion.color:Lerp(WHITE, 0.35) -- (2026-10-22 UI polish, M6: 3.8:1 on the navy cell)")

# ---------------------------------------------------------------- ShopClientLegacy: wider rail tiles (labels >= 16 px), bigger price labels
SH = SPS + "ShopClientLegacy"
add(SH,
"page.Size = UDim2.fromScale(0.86, 0.95)\npage.AnchorPoint = Vector2.new(0.5, 0.5)\npage.Position = UDim2.fromScale(0.44, 0.5)",
"page.Size = UDim2.fromScale(0.83, 0.95)\npage.AnchorPoint = Vector2.new(0.5, 0.5)\npage.Position = UDim2.fromScale(0.425, 0.5)")
add(SH,
"tabs.Position = UDim2.fromScale(0.947, 0.5)\ntabs.Size = UDim2.fromScale(0.095, 0.96)",
"tabs.Position = UDim2.fromScale(0.925, 0.5)\ntabs.Size = UDim2.fromScale(0.13, 0.96) -- (round 2: 0.095; wider tiles so \"Treadmill\" reads at 16 px)")
add(SH, "tl.Padding = UDim.new(0.012, 0)", "tl.Padding = UDim.new(0.008, 0)")
add(SH,
"\t\tslot.Size = UDim2.fromScale(1, 0.185)\n\t\tslot.LayoutOrder = i\n\t\tslot.Parent = tabs",
"\t\tslot.Size = UDim2.fromScale(1, 0.192)\n\t\tslot.LayoutOrder = i\n\t\tslot.Parent = tabs")
add(SH,
"\t\tlocal tar = Instance.new(\"UIAspectRatioConstraint\") tar.Parent = tile\n\t\ticon = B.image(b, \"Icon\", s.icon, UDim2.fromScale(0.74, 0.58), UDim2.fromScale(0.5, 0.4))",
"\t\tlocal tar = Instance.new(\"UIAspectRatioConstraint\") tar.AspectRatio = 1.5 tar.Parent = tile -- (round 2: wider than tall)\n"
"\t\ticon = B.image(b, \"Icon\", s.icon, UDim2.fromScale(0.6, 0.56), UDim2.fromScale(0.5, 0.36))")
add(SH,
"\tB.tapArea(b, go) -- (2026-10-22 UI polish, M7)",
"\tB.tapArea(b, go, nil, b.Parent.Parent) -- (2026-10-22 UI polish, M7; inside its slot)")
add(SH,
"\tlabel.Size = UDim2.fromScale(0.7, 0.56)",
"\tlabel.Size = UDim2.fromScale(0.7, 0.66) -- (2026-10-22 UI polish, M5: 0.56, OWNED was 13 px)")

# ---------------------------------------------------------------- IndexClientLegacy: tabs, header sub, cards
IX = SPS + "IndexClientLegacy"
add(IX,
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.92, 0.42), UDim2.fromScale(0.5, 0.3), 0.09)\n"
"\tname.Text = string.upper(a.name)\n"
"\tlocal prog = B.text(face, \"Prog\", B.FRED, WHITE, UDim2.fromScale(0.5, 0.34), UDim2.fromScale(0.4, 0.73), 0.08)\n"
"\tlocal star = B.image(face, \"Star\", STAR_ICON, UDim2.fromScale(0.4, 0.4), UDim2.fromScale(0.86, 0.71))\n"
"\tlocal sr = Instance.new(\"UIAspectRatioConstraint\") sr.Parent = star\n"
"\tlocal bang = B.frame(face, \"Ready\", UDim2.fromScale(0.4, 0.4), UDim2.fromScale(0.86, 0.71), Color3.fromRGB(235, 45, 45))",
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.96, 0.44), UDim2.fromScale(0.5, 0.27), 0.09)\n"
"\tname.Text = string.upper(a.name)\n"
"\tlocal prog = B.text(face, \"Prog\", B.FRED, WHITE, UDim2.fromScale(0.5, 0.36), UDim2.fromScale(0.36, 0.72), 0.08)\n"
"\tlocal star = B.image(face, \"Star\", STAR_ICON, UDim2.fromScale(0.3, 0.3), UDim2.fromScale(0.83, 0.72))\n"
"\tlocal sr = Instance.new(\"UIAspectRatioConstraint\") sr.Parent = star\n"
"\tlocal bang = B.frame(face, \"Ready\", UDim2.fromScale(0.3, 0.3), UDim2.fromScale(0.83, 0.72), Color3.fromRGB(235, 45, 45))")
add(IX,
"\tlocal vp = viewport(face, \"View\", UDim2.fromScale(0.96, 0.66), UDim2.fromScale(0.5, 0.47))\n"
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.94, 0.13), UDim2.fromScale(0.5, 0.1), 0.08) -- (M5: 0.12)",
"\t-- (2026-10-22 UI polish, M5) the name gets 0.2 of the card and wraps (two lines for long names), the model 0.56\n"
"\tlocal vp = viewport(face, \"View\", UDim2.fromScale(0.96, 0.56), UDim2.fromScale(0.5, 0.51))\n"
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.94, 0.2), UDim2.fromScale(0.5, 0.12), 0.08)\n"
"\tname.TextWrapped = true")
add(IX,
"\tlocal badge = B.frame(face, \"Secret\", UDim2.fromScale(0.66, 0.085), UDim2.fromScale(0.5, 0.205), Color3.fromRGB(255, 70, 150))",
"\tlocal badge = B.frame(face, \"Secret\", UDim2.fromScale(0.66, 0.085), UDim2.fromScale(0.5, 0.29), Color3.fromRGB(255, 70, 150)) -- (under the 2-line name)")
add(IX,
"\thSub.Text = \"Hatched from the <font color='#ffffff'>\" .. IndexConfig.eggName(area.egg) .. \"</font>\"",
"\thSub.Text = \"From the <font color='#ffffff'>\" .. IndexConfig.eggName(area.egg) .. \"</font>\" -- (2026-10-22 UI polish, M5: was \"Hatched from the\")")

# ---------------------------------------------------------------- RebirthClientLegacy: reward tile names
RB = SPS + "RebirthClientLegacy"
add(RB,
"\tlocal name = B.text(face, \"Name\", B.LUCKY, Color3.fromRGB(255, 250, 225), UDim2.fromScale(0.52, 0.24), UDim2.fromScale(0.72, 0.5), 0.08)",
"\tlocal name = B.text(face, \"Name\", B.LUCKY, Color3.fromRGB(255, 250, 225), UDim2.fromScale(0.56, 0.24), UDim2.fromScale(0.7, 0.5), 0.08)")

# ---------------------------------------------------------------- UpgradeClientLegacy
UP = SPS + "UpgradeClientLegacy"
add(UP,
"local SIZE, PHONE_SIZE = UDim2.fromScale(0.62, 0.62), UDim2.fromScale(0.8, 0.82)",
"local SIZE, PHONE_SIZE = UDim2.fromScale(0.82, 0.82), UDim2.fromScale(0.8, 0.82) -- (2026-10-22 UI polish, M5: PC 0.62 -> 0.82, every label >= 16 px)")
add(UP,
"local headIcon = B.image(head, \"Icon\", BOOST_ICON, UDim2.fromScale(0.09, 0.8), UDim2.fromScale(0.06, 0.5))",
"local headIcon = B.image(head, \"Icon\", BOOST_ICON, UDim2.fromScale(0.08, 0.68), UDim2.fromScale(0.06, 0.5)) -- (M1: 0.8 tall touched the header top)")
add(UP,
"local foot = B.text(win, \"Foot\", B.FRED, Color3.fromRGB(190, 195, 210), UDim2.fromScale(0.9, 0.045), UDim2.fromScale(0.5, 0.955), 0.05)",
"local foot = B.text(win, \"Foot\", B.FRED, Color3.fromRGB(222, 226, 236), UDim2.fromScale(0.9, 0.045), UDim2.fromScale(0.5, 0.955), 0.05) -- (M6: 190,195,210 = 4.3:1)")
add(UP,
"\tlocal lvl = B.text(f, \"Level\", B.LUCKY, r.color, UDim2.fromScale(0.24, 0.26), UDim2.fromScale(0.43, 0.24), 0.07, Vector2.new(0, 0.5))",
"\tlocal lvl = B.text(f, \"Level\", B.LUCKY, r.color:Lerp(WHITE, 0.3), UDim2.fromScale(0.24, 0.26), UDim2.fromScale(0.43, 0.24), 0.07, Vector2.new(0, 0.5)) -- (M6: lighter, the purple was 4.4:1)")
add(UP,
"\tlocal price = B.text(btn, \"Price\", B.LUCKY, WHITE, UDim2.fromScale(0.66, 0.55), UDim2.fromScale(0.62, 0.52), 0.08)",
"\tlocal price = B.text(btn, \"Price\", B.LUCKY, WHITE, UDim2.fromScale(0.68, 0.55), UDim2.fromScale(0.64, 0.52), 0.08)")
add(UP,
"\t\trow.price.Position = row.cash.Visible and UDim2.fromScale(0.62, 0.52) or UDim2.fromScale(0.5, 0.52) -- no icon: centred",
"\t\trow.price.Position = row.cash.Visible and UDim2.fromScale(0.64, 0.52) or UDim2.fromScale(0.5, 0.52) -- no icon: centred")

# ---------------------------------------------------------------- FreeGiftClientLegacy: header icon inset, tag colour
FG = SPS + "FreeGiftClientLegacy"
add(FG,
"new(\"ImageLabel\", {Name = \"Icon\", Image = GIFT_ICON, ScaleType = Enum.ScaleType.Fit, BackgroundTransparency = 1, Size = UDim2.fromOffset(46, 46),\n"
"\tPosition = UDim2.fromOffset(42, 29), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 6}, header)",
"new(\"ImageLabel\", {Name = \"Icon\", Image = GIFT_ICON, ScaleType = Enum.ScaleType.Fit, BackgroundTransparency = 1, Size = UDim2.fromOffset(42, 42),\n"
"\tPosition = UDim2.fromOffset(40, 30), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 6}, header) -- (2026-10-22 UI polish, M1: 9 px inside, was 6)")
add(FG,
"grad(tag, seq(Color3.fromRGB(255, 110, 110), Color3.fromRGB(230, 25, 45)))",
"grad(tag, seq(Color3.fromRGB(255, 235, 240), Color3.fromRGB(255, 190, 205))) -- (2026-10-22 UI polish, M6: the red was 1.6:1 on the slate)")

# ---------------------------------------------------------------- OfflineClientLegacy: header icon inset
OF = SPS + "OfflineClientLegacy"
add(OF,
"new(\"ImageLabel\", {Name = \"Icon\", Image = CASH, ScaleType = Enum.ScaleType.Fit, BackgroundTransparency = 1, Size = UDim2.fromOffset(44, 44),\n"
"\tPosition = UDim2.new(0, 37, 0.5, -2), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 4}, header)",
"new(\"ImageLabel\", {Name = \"Icon\", Image = CASH, ScaleType = Enum.ScaleType.Fit, BackgroundTransparency = 1, Size = UDim2.fromOffset(40, 40),\n"
"\tPosition = UDim2.new(0, 37, 0.5, 0), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 4}, header) -- (2026-10-22 UI polish, M1: 10 px inside, was 6)")

os.makedirs(OUT, exist_ok=True)
for path, edits in P.items():
    name = path.split(".")[-1]
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"file_path": path, "datamodel_type": "Edit", "edits": [{"old_string": o, "new_string": n} for o, n in edits]}, f, ensure_ascii=False, indent=1)
    print(f"{name:24s} {len(edits)} edits")
print("total", sum(len(e) for e in P.values()))
