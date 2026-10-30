# make_payloads.py (2026-10-22 UI polish, PREP): writes one multi_edit payload per script (payloads/<Script>.json).
# Every old_string is copied from the source read with script_read on 2026-10-22; phase 2 re-checks each is unique
# before applying (apply_edit_mode.lua). Indentation in Studio sources = tabs (written here as \t).
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
SPS = "game.StarterPlayer.StarterPlayerScripts."
T = "\t"
P = {}  # file_path -> [(old, new)]

def add(path, old, new):
    P.setdefault(path, []).append((old, new))

# ------------------------------------------------------------------------------------------------ BrickUI (M6-A, M7)
BR = "game.ReplicatedStorage.BrickUI"
add(BR,
"\tt.Parent = parent\n\tBrickUI.stroke(t, th or 0.07)\n\treturn t\nend",
"\tt.Parent = parent\n"
"\tif CUI then\n"
"\t\t-- (2026-10-22 UI polish, M6-A) the outline is pure black and never thinner than 2.5 px at the 1050 x 620 base (the\n"
"\t\t-- Check-UI canon is 2.6-3.5 px): small labels on lime / silver / gold / cyan keep a readable edge (black outline\n"
"\t\t-- vs lime 12.4:1, vs cyan 5.1:1; white fill vs outline 21:1). Big labels keep their ScaledSize share as before.\n"
"\t\tBrickUI.minOutline(t, BrickUI.stroke(t, th or 0.07, Color3.new(0, 0, 0)), th or 0.07)\n"
"\telse\n"
"\t\tBrickUI.stroke(t, th or 0.07)\n"
"\tend\n"
"\treturn t\nend")
add(BR,
"function BrickUI.text(parent, name, font, color, size, pos, th, anchor)",
"-- (2026-10-22 UI polish, M6-A) minOutline(label, stroke, th): the ScaledSize stroke th (a share of the label's shorter\n"
"-- side) is raised to at least MIN_OUTLINE base px, re-checked when the label's size changes (event-driven, nothing per\n"
"-- frame). A script that sets the stroke's Thickness itself keeps its value as the new share.\n"
"BrickUI.MIN_OUTLINE = 2.5\n"
"local function outlineScale()\n"
"\tlocal vp = BrickUI.viewportSize()\n"
"\tif not viewportReady(vp) then return 1 end\n"
"\treturn math.max(0.52, math.min(vp.X / 1050, vp.Y / 620))\n"
"end\n"
"function BrickUI.minOutline(t, s, th)\n"
"\tif not IS_CLIENT then return s end\n"
"\tlocal base, writing = th, false\n"
"\tlocal function fit()\n"
"\t\tlocal a = t.AbsoluteSize\n"
"\t\tlocal m = math.min(a.X, a.Y)\n"
"\t\tif m <= 0 then return end\n"
"\t\twriting = true\n"
"\t\ts.Thickness = math.max(base, BrickUI.MIN_OUTLINE * outlineScale() / m)\n"
"\t\twriting = false\n"
"\tend\n"
"\ts:GetPropertyChangedSignal(\"Thickness\"):Connect(function() if not writing then base = s.Thickness fit() end end)\n"
"\tt:GetPropertyChangedSignal(\"AbsoluteSize\"):Connect(fit)\n"
"\tfit()\n"
"\treturn s\n"
"end\n\n"
"function BrickUI.text(parent, name, font, color, size, pos, th, anchor)")
add(BR,
"------------------------------------------------------------------ HATCH NIGHT window skin (2026-10-21)",
"------------------------------------------------------------------ (2026-10-22 UI polish, M7) tap areas\n"
"-- tapArea(button, onActivate, minPx): an invisible TextButton BEHIND the button (a sibling, ZIndex - 1), centred on it,\n"
"-- never smaller than minPx x minPx SCREEN px (default 44 = 44 pt on a phone). Taps on the button itself still reach the\n"
"-- button (its press / hover feel stays); taps on the extension call onActivate. Follows the button's size, position\n"
"-- and visibility. Works under any UIScale (the size is a factor of the button's own UDim2).\n"
"function BrickUI.tapArea(button, onActivate, minPx)\n"
"\tminPx = minPx or 44\n"
"\tlocal hit = Instance.new(\"TextButton\")\n"
"\thit.Name = button.Name .. \"TapArea\"\n"
"\thit.Text = \"\"\n"
"\thit.BackgroundTransparency = 1\n"
"\thit.AutoButtonColor = false\n"
"\thit.Selectable = false\n"
"\thit.AnchorPoint = button.AnchorPoint\n"
"\thit.ZIndex = math.max(1, button.ZIndex - 1)\n"
"\tlocal ar = button:FindFirstChildOfClass(\"UIAspectRatioConstraint\")\n"
"\tif ar then ar:Clone().Parent = hit end\n"
"\tlocal function fit()\n"
"\t\tlocal a = button.AbsoluteSize\n"
"\t\thit.Visible = button.Visible\n"
"\t\thit.Position = button.Position\n"
"\t\thit.Rotation = button.Rotation\n"
"\t\tif a.X <= 0 or a.Y <= 0 then return end\n"
"\t\tlocal s = button.Size\n"
"\t\tlocal fx, fy = math.max(1, minPx / a.X), math.max(1, minPx / a.Y)\n"
"\t\thit.Size = UDim2.new(s.X.Scale * fx, s.X.Offset * fx, s.Y.Scale * fy, s.Y.Offset * fy)\n"
"\tend\n"
"\tfor _, prop in {\"AbsoluteSize\", \"Position\", \"Visible\", \"Size\"} do button:GetPropertyChangedSignal(prop):Connect(fit) end\n"
"\thit.Activated:Connect(function() onActivate() end)\n"
"\thit.Parent = button.Parent\n"
"\tfit()\n"
"\treturn hit\n"
"end\n\n"
"------------------------------------------------------------------ HATCH NIGHT window skin (2026-10-21)")

# ------------------------------------------------------------------------------------------------ MenuController
MC = "game.StarterGui.MainMenu.MenuController"
add(MC,
"\tlocal LAYOUT = {Shop = {2.0, 1.6, 0.11}, Index = {2.0, 1.75}, Gift = {1.95, 1.2}, Rebirth = {1.55, 1.25}, Sell = {1.5, 1.05}, Settings = {1.55, 1.3}}",
"\t-- (2026-10-22 UI polish) bigger Gift / Settings / Rebirth / Index (M5: every label >= 16 px at the 1050 x 620 base) and a\n"
"\t-- wider Shop (M3: its side tabs moved INSIDE the window). Was Shop {2.0, 1.6} (the window is height-dominant + fit-within: a wider aspect alone makes it shorter), Index {2.0, 1.75}, Gift {1.95, 1.2},\n"
"\t-- Rebirth {1.55, 1.25}, Settings {1.55, 1.3}.\n"
"\tlocal LAYOUT = {Shop = {2.28, 1.82, 0.11}, Index = {2.3, 1.85}, Gift = {2.25, 1.32}, Rebirth = {2.0, 1.45}, Sell = {1.5, 1.05}, Settings = {2.05, 1.3}}")
add(MC,
"\tlocal TITLES = {Gift = \"Playtime Rewards\", Index = \"Creature Index\"}\n\tpanel.Title.Text = TITLES[name] or name",
"\tlocal TITLES = {Gift = \"Playtime Rewards\", Index = \"Creature Index\"}\n\tpanel.Title.Text = TITLES[name] or name\n"
"\t-- (2026-10-22 UI polish, M4) the white Settings header: its title gets a solid 3 px black outline (the shared title's\n"
"\t-- ScaledSize stroke is about 2.3 px there); every other page gets the shared stroke back\n"
"\tlocal ts = panel.Title:FindFirstChildOfClass(\"UIStroke\")\n"
"\tif ts then\n"
"\t\tif ts:GetAttribute(\"PolishBase\") == nil then\n"
"\t\t\tts:SetAttribute(\"PolishBase\", ts.Thickness)\n"
"\t\t\tts:SetAttribute(\"PolishMode\", ts.StrokeSizingMode.Name)\n"
"\t\t\tts:SetAttribute(\"PolishColor\", ts.Color)\n"
"\t\tend\n"
"\t\tif name == \"Settings\" then\n"
"\t\t\tts.StrokeSizingMode = Enum.StrokeSizingMode.FixedSize\n"
"\t\t\tts.Thickness = 3 * math.max(B.viewportSize().Y / 620, 0.7)\n"
"\t\t\tts.Color = Color3.new(0, 0, 0)\n"
"\t\telse\n"
"\t\t\tts.StrokeSizingMode = Enum.StrokeSizingMode[ts:GetAttribute(\"PolishMode\")]\n"
"\t\t\tts.Thickness = ts:GetAttribute(\"PolishBase\")\n"
"\t\t\tts.Color = ts:GetAttribute(\"PolishColor\")\n"
"\t\tend\n"
"\tend")
add(MC,
"\tlocal size = lay and mul(winSize, lay[1]) or winSize\n\tsize = mul(size, fitScale(size))",
"\tlocal size = lay and mul(winSize, lay[1]) or winSize\n"
"\t-- (2026-10-22 UI polish, M5) phones: a window keeps >= 0.7 of its 620 px-tall size (a Scale window would get 390 / 620 =\n"
"\t-- 0.63 on a 390 px phone); fitScale below still keeps it on the screen\n"
"\tsize = mul(size, math.max(1, 434 / math.max(B.viewportSize().Y, 1)))\n"
"\tsize = mul(size, fitScale(size))")
add(MC,
"if closeFace then\n\tcloseFace.Activated:Connect(closeWindow)\nelse",
"if closeFace then\n\tcloseFace.Activated:Connect(closeWindow)\n\tB.tapArea(closeFace, closeWindow) -- (2026-10-22 UI polish, M7) >= 44 pt\nelse")
add(MC,
"\tlocal t = B.text(r, \"Title\", B.LUCKY, WHITE, UDim2.fromScale(0.5, 0.46), UDim2.fromScale(0.035, 0.37), 0.08, Vector2.new(0, 0.5))",
"\tlocal t = B.text(r, \"Title\", B.LUCKY, WHITE, UDim2.fromScale(0.5, 0.42), UDim2.fromScale(0.035, 0.3), 0.08, Vector2.new(0, 0.5)) -- (2026-10-22 UI polish, M5: was 0.46 at y 0.37)")
add(MC,
"\tlocal st = B.text(r, \"Subtitle\", B.LUCKY, SUB, UDim2.fromScale(0.5, 0.26), UDim2.fromScale(0.035, 0.75), 0.06, Vector2.new(0, 0.5))",
"\tlocal st = B.text(r, \"Subtitle\", B.LUCKY, SUB, UDim2.fromScale(0.5, 0.34), UDim2.fromScale(0.035, 0.72), 0.06, Vector2.new(0, 0.5)) -- (M5: was 0.26 at y 0.75)")
add(MC,
"\tf.Activated:Connect(function()\n\t\tlocal v = settingsData()[key]\n\t\tif v == nil then v = default end\n\t\tsend(key, not v)\n\tend)",
"\tlocal function flip()\n\t\tlocal v = settingsData()[key]\n\t\tif v == nil then v = default end\n\t\tsend(key, not v)\n\tend\n"
"\tf.Activated:Connect(flip)\n\tB.tapArea(f, flip) -- (2026-10-22 UI polish, M7)")
add(MC,
"minus.Activated:Connect(function() local v = step(savedVol() - 0.1) showVol(v) send(\"musicVol\", v) end)\n"
"plus.Activated:Connect(function() local v = step(savedVol() + 0.1) showVol(v) send(\"musicVol\", v) end)",
"local function volDown() local v = step(savedVol() - 0.1) showVol(v) send(\"musicVol\", v) end\n"
"local function volUp() local v = step(savedVol() + 0.1) showVol(v) send(\"musicVol\", v) end\n"
"minus.Activated:Connect(volDown)\nplus.Activated:Connect(volUp)\n"
"B.tapArea(minus, volDown) B.tapArea(plus, volUp) -- (2026-10-22 UI polish, M7: the - / + were 22 x 18 pt on a phone)")
add(MC,
"prev.Activated:Connect(function() local t = (savedTrack() - 1) % (#TRACKS + 1) songName.Text = songLabel(t) send(\"track\", t) end)\n"
"nxt.Activated:Connect(function() local t = (savedTrack() + 1) % (#TRACKS + 1) songName.Text = songLabel(t) send(\"track\", t) end)",
"local function songPrev() local t = (savedTrack() - 1) % (#TRACKS + 1) songName.Text = songLabel(t) send(\"track\", t) end\n"
"local function songNext() local t = (savedTrack() + 1) % (#TRACKS + 1) songName.Text = songLabel(t) send(\"track\", t) end\n"
"prev.Activated:Connect(songPrev)\nnxt.Activated:Connect(songNext)\n"
"B.tapArea(prev, songPrev) B.tapArea(nxt, songNext) -- (2026-10-22 UI polish, M7)")

# ------------------------------------------------------------------------------------------------ StreakClient (Gift Daily)
SC = SPS + "StreakClient"
add(SC,
"\tlocal dayLabel = text(face, \"Day\", UDim2.fromScale(big and 0.5 or 0.9, 0.14), UDim2.fromScale(0.5, 0.1), 0.09)",
"\t-- (2026-10-22 UI polish, M5) DAY n 0.15 tall; Day 7's sits over its portrait column (left)\n"
"\tlocal dayLabel = text(face, \"Day\", UDim2.fromScale(big and 0.4 or 0.9, 0.15), UDim2.fromScale(big and 0.24 or 0.5, 0.1), 0.09)")
add(SC,
"\t\tsunburst = square(B.image(face, \"Sunburst\", B.SUNBURST, UDim2.fromScale(0.5, 0.86), UDim2.fromScale(0.24, 0.53))) -- (2026-10-22 UI revert) 0.86: stays inside the card (was 0.95)\n"
"\t\tsunburst.ImageTransparency = 0.15\n"
"\t\tc.icon = square(B.image(face, \"Icon\", \"\", UDim2.fromScale(0.38, 0.66), UDim2.fromScale(0.24, 0.54)))\n"
"\t\tc.icon.ZIndex = 3\n"
"\t\tlocal title = text(face, \"Secret\", UDim2.fromScale(0.54, 0.16), UDim2.fromScale(0.71, 0.27), 0.1)",
"\t\t-- (2026-10-22 UI polish, M5 / M1) Day 7 re-flow: DAY 7 + portrait + CLAIM in the LEFT column, the SECRET! ribbon\n"
"\t\t-- (bigger, 6+ px inside the top-right corner), SECRET PET! and 3 lines (0.14 tall each) in the RIGHT column\n"
"\t\tsunburst = square(B.image(face, \"Sunburst\", B.SUNBURST, UDim2.fromScale(0.5, 0.6), UDim2.fromScale(0.24, 0.47)))\n"
"\t\tsunburst.ImageTransparency = 0.15\n"
"\t\tc.icon = square(B.image(face, \"Icon\", \"\", UDim2.fromScale(0.3, 0.44), UDim2.fromScale(0.24, 0.47)))\n"
"\t\tc.icon.ZIndex = 3\n"
"\t\tlocal title = text(face, \"Secret\", UDim2.fromScale(0.48, 0.15), UDim2.fromScale(0.73, 0.37), 0.1)")
add(SC,
"\t\tc.lines[1] = text(face, \"Line1\", UDim2.fromScale(0.54, 0.11), UDim2.fromScale(0.71, 0.41))\n"
"\t\tc.lines[2] = text(face, \"Line2\", UDim2.fromScale(0.54, 0.1), UDim2.fromScale(0.71, 0.52))\n"
"\t\tc.lines[3] = text(face, \"Line3\", UDim2.fromScale(0.54, 0.1), UDim2.fromScale(0.71, 0.62))\n"
"\t\tlocal rh, rf = B.brick(face, \"Ribbon\", UDim2.fromScale(0.2, 0.13), UDim2.fromScale(0.87, 0.115), C(255, 32, 80)) -- (2026-10-22 UI revert) inside the card corner (was 0.22 x 0.15 at 0.9, 0.1, 10 deg)\n"
"\t\trh.Rotation = 4\n"
"\t\trh.ZIndex = 7\n"
"\t\tlocal rl = text(rf, \"Label\", UDim2.fromScale(0.86, 0.66), UDim2.fromScale(0.5, 0.5), 0.1)",
"\t\tc.lines[1] = text(face, \"Line1\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.53))\n"
"\t\tc.lines[2] = text(face, \"Line2\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.68))\n"
"\t\tc.lines[3] = text(face, \"Line3\", UDim2.fromScale(0.48, 0.14), UDim2.fromScale(0.73, 0.83))\n"
"\t\tlocal rh, rf = B.brick(face, \"Ribbon\", UDim2.fromScale(0.32, 0.19), UDim2.fromScale(0.81, 0.17), C(255, 32, 80)) -- (M1 / M5: 0.2 x 0.13 at 0.87, 0.115; its label was 11 px)\n"
"\t\trh.Rotation = 4\n"
"\t\trh.ZIndex = 7\n"
"\t\tlocal rl = text(rf, \"Label\", UDim2.fromScale(0.9, 0.72), UDim2.fromScale(0.5, 0.5), 0.1)")
add(SC,
"\t\tc.icon = square(B.image(face, \"Icon\", \"\", UDim2.fromScale(0.6, 0.3), UDim2.fromScale(0.5, 0.34)))\n"
"\t\tc.icon.ZIndex = 3\n"
"\t\tc.lines[1] = text(face, \"Line1\", UDim2.fromScale(0.94, 0.13), UDim2.fromScale(0.5, 0.565))\n"
"\t\tc.lines[2] = text(face, \"Line2\", UDim2.fromScale(0.94, 0.1), UDim2.fromScale(0.5, 0.685))",
"\t\t-- (2026-10-22 UI polish, M5) DAY 0.15 / icon 0.2 / value 0.17 / 2nd line 0.15 / button 0.24 (were icon 0.3, lines 0.13 / 0.1)\n"
"\t\tc.icon = square(B.image(face, \"Icon\", \"\", UDim2.fromScale(0.6, 0.2), UDim2.fromScale(0.5, 0.29)))\n"
"\t\tc.icon.ZIndex = 3\n"
"\t\tc.lines[1] = text(face, \"Line1\", UDim2.fromScale(0.96, 0.17), UDim2.fromScale(0.5, 0.485))\n"
"\t\tc.lines[2] = text(face, \"Line2\", UDim2.fromScale(0.96, 0.15), UDim2.fromScale(0.5, 0.64))")
add(SC,
"\tlocal bh, bf = B.brick(face, \"Claim\", UDim2.fromScale(big and 0.48 or 0.86, 0.19), UDim2.fromScale(big and 0.71 or 0.5, 0.865), OFF, nil, {button = true})\n"
"\tbh.ZIndex = 6\n"
"\tlocal state = text(bf, \"State\", UDim2.fromScale(0.7, 0.62), UDim2.fromScale(0.55, 0.5), 0.1)",
"\t-- (2026-10-22 UI polish, M5 / M7) 0.24 tall (was 0.19), 6+ px above the card's bottom; Day 7's under its portrait\n"
"\tlocal bh, bf = B.brick(face, \"Claim\", UDim2.fromScale(big and 0.42 or 0.86, 0.24), UDim2.fromScale(big and 0.24 or 0.5, 0.83), OFF, nil, {button = true})\n"
"\tbh.ZIndex = 6\n"
"\tlocal state = text(bf, \"State\", UDim2.fromScale(0.7, 0.66), UDim2.fromScale(0.55, 0.5), 0.1)")
add(SC,
"\tif d == 1 then return {money(cashOf(15)), \"+1 Money Potion\"}\n"
"\telseif d == 2 then return {\"+1 Hatch & Speed Potion\", \"+\" .. SpeedStat.Format(speedOf(0.2)) .. \" Speed\"}\n"
"\telseif d == 3 then return {money(cashOf(30)), \"+2 Money Potions\"}\n"
"\telseif d == 4 then return {\"BIG EGG\", (eggKind():gsub(\"Egg$\", \" Egg\")) .. \" \" .. SpeedStat.Format(S.EGG_KG[area()]) .. \" KG\"}",
"\t-- (2026-10-22 UI polish, M5) 2nd lines <= 14 characters so they stay >= 16 px (the potion / egg kind is the icon)\n"
"\tif d == 1 then return {money(cashOf(15)), \"+1 Potion\"}\n"
"\telseif d == 2 then return {\"+\" .. SpeedStat.Format(speedOf(0.2)) .. \" Speed\", \"+2 Potions\"}\n"
"\telseif d == 3 then return {money(cashOf(30)), \"+2 Potions\"}\n"
"\telseif d == 4 then return {\"BIG EGG\", SpeedStat.Format(S.EGG_KG[area()]) .. \" KG\"}")
add(SC,
"\treturn {petDisplay(petName()) .. \" \" .. SpeedStat.Format(S.SECRET_KG[area()]) .. \" KG\", \"+5 of EVERY Potion\", money(cashOf(120))}",
"\treturn {petDisplay(petName()), SpeedStat.Format(S.SECRET_KG[area()]) .. \" KG + \" .. money(cashOf(120)), \"+5 ALL Potions\"} -- (M5)")
add(SC,
"\t\t\tcelebrate(pet, lines[1] .. \" + 5 of every potion + \" .. lines[3])",
"\t\t\tcelebrate(pet, lines[1] .. \" \" .. lines[2] .. \" + 5 of every potion\")")
add(SC,
"\tc.button.Activated:Connect(press)",
"\tc.button.Activated:Connect(press)\n\tB.tapArea(c.face, press) -- (2026-10-22 UI polish, M7) the whole card claims (a card is >= 44 pt on a phone)")
add(SC,
"tabDaily.Activated:Connect(function() page:SetAttribute(\"Tab\", \"Daily\") end)\n"
"tabPlay.Activated:Connect(function() page:SetAttribute(\"Tab\", \"Playtime\") end)",
"local function toDaily() page:SetAttribute(\"Tab\", \"Daily\") end\n"
"local function toPlay() page:SetAttribute(\"Tab\", \"Playtime\") end\n"
"tabDaily.Activated:Connect(toDaily)\ntabPlay.Activated:Connect(toPlay)\n"
"B.tapArea(tabDaily, toDaily) B.tapArea(tabPlay, toPlay) -- (2026-10-22 UI polish, M7)")
# nothing runs per frame for the "!" dot: it follows its attribute instead of every frame
add(SC,
"RunService.RenderStepped:Connect(function(dt)\n\tlocal t = os.clock()\n\tdot.Visible = player:GetAttribute(\"StreakClaimable\") == true\n",
"-- (2026-10-22 UI polish) the \"!\" dot follows its attribute (it was written every frame, window closed or not)\n"
"local function dotState() dot.Visible = player:GetAttribute(\"StreakClaimable\") == true end\n"
"player:GetAttributeChangedSignal(\"StreakClaimable\"):Connect(dotState)\ndotState()\n"
"RunService.RenderStepped:Connect(function(dt)\n\tlocal t = os.clock()\n")

# ------------------------------------------------------------------------------------------------ PlaytimeClient
PC = SPS + "PlaytimeClient"
add(PC,
"\t\tUDim2.fromScale(0.7, 0.5), UDim2.fromScale(0.5, 0.5))\n"
"\ticon.ZIndex = 3\n"
"\tlocal top = B.text(face, \"Top\", B.LUCKY, WHITE, UDim2.fromScale(0.92, 0.24), UDim2.fromScale(0.5, 0.15), 0.08)\n"
"\ttop.ZIndex = 4\n"
"\tlocal bottom = B.text(face, \"Time\", B.LUCKY, WHITE, UDim2.fromScale(0.88, 0.24), UDim2.fromScale(0.5, 0.85), 0.08)",
"\t\tUDim2.fromScale(0.7, 0.34), UDim2.fromScale(0.5, 0.5)) -- (2026-10-22 UI polish, M5: icon 0.5 -> 0.34, texts 0.24 -> 0.3)\n"
"\ticon.ZIndex = 3\n"
"\tlocal top = B.text(face, \"Top\", B.LUCKY, WHITE, UDim2.fromScale(0.94, 0.3), UDim2.fromScale(0.5, 0.17), 0.08)\n"
"\ttop.ZIndex = 4\n"
"\tlocal bottom = B.text(face, \"Time\", B.LUCKY, WHITE, UDim2.fromScale(0.9, 0.3), UDim2.fromScale(0.5, 0.83), 0.08)")
add(PC,
"\t\t\tc.icon.Size = UDim2.fromScale(0.8, 0.6)",
"\t\t\tc.icon.Size = UDim2.fromScale(0.8, 0.4) -- (M5: was 0.6, now under the bigger texts)")

# ------------------------------------------------------------------------------------------------ ShopClientLegacy (M3)
SH = SPS + "ShopClientLegacy"
add(SH,
"page.Size = UDim2.fromScale(0.97, 0.95)\npage.AnchorPoint = Vector2.new(0.5, 0.5)\npage.Position = UDim2.fromScale(0.5, 0.5)",
"-- (2026-10-22 UI polish, M3) the page leaves the body's right side to the section tabs (they hung outside the window)\n"
"page.Size = UDim2.fromScale(0.86, 0.95)\npage.AnchorPoint = Vector2.new(0.5, 0.5)\npage.Position = UDim2.fromScale(0.44, 0.5)")
add(SH,
"local tabs = Instance.new(\"Frame\")\ntabs.Name = \"ShopTabs\"\ntabs.BackgroundTransparency = 1\n"
"tabs.Position = UDim2.fromScale(1.022, 0.2)\ntabs.Size = UDim2.fromScale(0.09, 0.78)\ntabs.ZIndex = 5\ntabs.Visible = false\ntabs.Parent = win",
"local tabs = Instance.new(\"Frame\")\ntabs.Name = \"ShopTabs\"\ntabs.BackgroundTransparency = 1\n"
"-- (2026-10-22 UI polish, M3) INSIDE the window: the body's right strip, an 8+ px gutter to the page (was x 1.022 of the window)\n"
"tabs.AnchorPoint = Vector2.new(0.5, 0.5)\ntabs.Position = UDim2.fromScale(0.947, 0.5)\ntabs.Size = UDim2.fromScale(0.095, 0.96)\n"
"tabs.ZIndex = 5\ntabs.Visible = false\ntabs.Parent = body")
add(SH,
"\t\tlabel = B.text(b, \"Label\", B.LUCKY, WHITE, UDim2.fromScale(0.96, 0.27), UDim2.fromScale(0.5, 0.81), 0.1)",
"\t\tlabel = B.text(b, \"Label\", B.LUCKY, WHITE, UDim2.fromScale(0.98, 0.3), UDim2.fromScale(0.5, 0.8), 0.1) -- (M5: 0.27)")
add(SH,
"\tb.Activated:Connect(function()\n\t\tSFX.play(\"Click\")\n\t\tscrollTo(s.name, true)\n\tend)",
"\tlocal function go()\n\t\tSFX.play(\"Click\")\n\t\tscrollTo(s.name, true)\n\tend\n\tb.Activated:Connect(go)\n\tB.tapArea(b, go) -- (2026-10-22 UI polish, M7)")

# ------------------------------------------------------------------------------------------------ IndexClientLegacy
IX = SPS + "IndexClientLegacy"
add(IX,
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.86, 0.46), UDim2.fromScale(0.5, 0.36), 0.09)\n"
"\tname.Text = string.upper(a.name)\n"
"\tlocal prog = B.text(face, \"Prog\", B.FRED, WHITE, UDim2.fromScale(0.6, 0.32), UDim2.fromScale(0.5, 0.76), 0.08)\n"
"\tlocal star = B.image(face, \"Star\", STAR_ICON, UDim2.fromScale(0.34, 0.6), UDim2.fromScale(0.95, 0.12))\n"
"\tlocal sr = Instance.new(\"UIAspectRatioConstraint\") sr.Parent = star\n"
"\tlocal bang = B.frame(face, \"Ready\", UDim2.fromScale(0.26, 0.48), UDim2.fromScale(0.95, 0.12), Color3.fromRGB(235, 45, 45))",
"\t-- (2026-10-22 UI polish) M5: the name gets the full width + 0.42 of the height; M1: the star / \"!\" badges sit INSIDE the\n"
"\t-- tab's bottom-right (they stuck half out of the top-right corner), the progress text moves left of them\n"
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.92, 0.42), UDim2.fromScale(0.5, 0.3), 0.09)\n"
"\tname.Text = string.upper(a.name)\n"
"\tlocal prog = B.text(face, \"Prog\", B.FRED, WHITE, UDim2.fromScale(0.5, 0.34), UDim2.fromScale(0.4, 0.73), 0.08)\n"
"\tlocal star = B.image(face, \"Star\", STAR_ICON, UDim2.fromScale(0.4, 0.4), UDim2.fromScale(0.86, 0.71))\n"
"\tlocal sr = Instance.new(\"UIAspectRatioConstraint\") sr.Parent = star\n"
"\tlocal bang = B.frame(face, \"Ready\", UDim2.fromScale(0.4, 0.4), UDim2.fromScale(0.86, 0.71), Color3.fromRGB(235, 45, 45))")
add(IX,
"\tface.Activated:Connect(function() areaSel = i creatureSel = nil refresh() end)\nend",
"\tlocal function pick() areaSel = i creatureSel = nil refresh() end\n\tface.Activated:Connect(pick)\n"
"\tB.tapArea(face, pick) -- (2026-10-22 UI polish, M7)\nend")
add(IX,
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.92, 0.12), UDim2.fromScale(0.5, 0.1), 0.08)",
"\tlocal name = B.text(face, \"Name\", B.LUCKY, WHITE, UDim2.fromScale(0.94, 0.13), UDim2.fromScale(0.5, 0.1), 0.08) -- (M5: 0.12)")
add(IX,
"\tlocal pillText = B.text(pill, \"T\", B.LUCKY, WHITE, UDim2.fromScale(0.86, 0.72), UDim2.fromScale(0.5, 0.52), 0.1)",
"\tlocal pillText = B.text(pill, \"T\", B.LUCKY, WHITE, UDim2.fromScale(0.9, 0.8), UDim2.fromScale(0.5, 0.52), 0.1) -- (M5: 0.72)")
add(IX,
"local tBg = B.frame(bookBar, \"Bar\", UDim2.fromScale(0.62, 0.62), UDim2.fromScale(0.42, 0.5), Color3.fromRGB(20, 24, 44))",
"-- (2026-10-22 UI polish, M4) the count sits BESIDE the trough (it was printed on the moving fill): trough 0.12-0.42,\n"
"-- \"n / 30 FOUND\" 0.44-0.73 (CLAIM ALL starts at 0.75)\n"
"local tBg = B.frame(bookBar, \"Bar\", UDim2.fromScale(0.3, 0.62), UDim2.fromScale(0.27, 0.5), Color3.fromRGB(20, 24, 44))")
add(IX,
"local tText = B.text(tBg, \"Text\", B.LUCKY, WHITE, UDim2.fromScale(0.9, 0.82), UDim2.fromScale(0.5, 0.52), 0.08)\ntText.ZIndex = 3",
"local tText = B.text(bookBar, \"Text\", B.LUCKY, WHITE, UDim2.fromScale(0.29, 0.8), UDim2.fromScale(0.44, 0.5), 0.08, Vector2.new(0, 0.5))\n"
"tText.TextXAlignment = Enum.TextXAlignment.Left\ntText.ZIndex = 3")
add(IX,
"\ttText.Text = \"DISCOVERED \" .. total .. \" / \" .. all",
"\ttText.Text = total .. \" / \" .. all .. \" FOUND\" -- (2026-10-22 UI polish, M4 / M5: was \"DISCOVERED n / 30\" on the fill)")

# ------------------------------------------------------------------------------------------------ RebirthClientLegacy
RB = SPS + "RebirthClientLegacy"
add(RB,
"\tlocal value = B.text(face, \"Value\", B.LUCKY, WHITE, UDim2.fromScale(0.5, 0.38), UDim2.fromScale(0.72, 0.32), 0.09)\n"
"\tvalue.ZIndex = 3\n"
"\tlocal name = B.text(face, \"Name\", B.LUCKY, Color3.fromRGB(255, 250, 225), UDim2.fromScale(0.5, 0.2), UDim2.fromScale(0.72, 0.63), 0.08)\n"
"\tname.Text = t.name\n"
"\tname.ZIndex = 3\n"
"\tlocal line = B.text(face, \"Line\", B.FRED, WHITE, UDim2.fromScale(0.92, 0.21), UDim2.fromScale(0.5, 0.855), 0.07)",
"\t-- (2026-10-22 UI polish, M5) value 0.32 / name 0.24 / line 0.24 (were 0.38 / 0.2 / 0.21: name + line were 10-11 px base)\n"
"\tlocal value = B.text(face, \"Value\", B.LUCKY, WHITE, UDim2.fromScale(0.5, 0.32), UDim2.fromScale(0.72, 0.21), 0.09)\n"
"\tvalue.ZIndex = 3\n"
"\tlocal name = B.text(face, \"Name\", B.LUCKY, Color3.fromRGB(255, 250, 225), UDim2.fromScale(0.52, 0.24), UDim2.fromScale(0.72, 0.5), 0.08)\n"
"\tname.Text = t.name\n"
"\tname.ZIndex = 3\n"
"\tlocal line = B.text(face, \"Line\", B.FRED, WHITE, UDim2.fromScale(0.94, 0.24), UDim2.fromScale(0.5, 0.835), 0.07)")
add(RB,
"\tlocal icon = square(B.image(face, \"Icon\", t.icon, UDim2.fromScale(1, 0.62), UDim2.fromScale(0.05, 0.43), Vector2.new(0, 0.5)))",
"\tlocal icon = square(B.image(face, \"Icon\", t.icon, UDim2.fromScale(1, 0.5), UDim2.fromScale(0.05, 0.36), Vector2.new(0, 0.5))) -- (M5: 0.62 at 0.43)")
add(RB,
"local petSub = left(B.text(petCard, \"Sub\", B.FRED, Color3.fromRGB(205, 212, 240), UDim2.fromScale(0.62, 0.3), UDim2.fromScale(0.2, 0.73), 0.06, Vector2.new(0, 0.5)))",
"local petSub = left(B.text(petCard, \"Sub\", B.FRED, Color3.fromRGB(205, 212, 240), UDim2.fromScale(0.62, 0.36), UDim2.fromScale(0.2, 0.72), 0.06, Vector2.new(0, 0.5))) -- (M5: 0.3)")
add(RB,
"local function setButton(color, text)\n\tbtn.BackgroundColor3 = color\n\tbtnHolder.Depth.BackgroundColor3 = color:Lerp(Color3.new(0, 0, 0), 0.4)\n\tif os.clock() > flashUntil then btnLabel.Text = text end\nend",
"-- (2026-10-22 UI polish, M4) not ready = a solid silver button (the CLAIMED palette) with an INK label and no checkerboard\n"
"-- behind it; ready = lime with its checker and the white outlined label, as before\n"
"local SILVER_OFF = Color3.fromRGB(200, 205, 212)\n"
"local function setButton(color, text)\n"
"\tlocal off = color == GREY\n"
"\tbtn.BackgroundColor3 = off and SILVER_OFF or color\n"
"\tbtnHolder.Depth.BackgroundColor3 = (off and SILVER_OFF or color):Lerp(Color3.new(0, 0, 0), 0.4)\n"
"\tlocal studs = btn:FindFirstChild(\"Studs\")\n"
"\tif studs then studs.Visible = not off end\n"
"\tbtnLabel.TextColor3 = off and B.INK or WHITE\n"
"\tlocal ls = btnLabel:FindFirstChildOfClass(\"UIStroke\")\n"
"\tif ls then ls.Enabled = not off end\n"
"\tif os.clock() > flashUntil then btnLabel.Text = text end\nend")
add(RB,
"btn.Activated:Connect(press)\nif RunService:IsStudio() then -- (2026-10-21 tests) RebirthPage.TestPress:Fire() = one press of the REBIRTH button",
"btn.Activated:Connect(press)\nB.tapArea(btn, press) -- (2026-10-22 UI polish, M7)\n"
"if RunService:IsStudio() then -- (2026-10-21 tests) RebirthPage.TestPress:Fire() = one press of the REBIRTH button")

# ------------------------------------------------------------------------------------------------ UpgradeClientLegacy
UP = SPS + "UpgradeClientLegacy"
add(UP,
"\t{kind = \"Sling\", icon = \"rbxassetid://84334196742101\", name = \"Slingshot Power\", desc = \"Launch further down the runway\", color = Color3.fromRGB(255, 150, 40)},\n"
"\t{kind = \"Grab\", icon = \"rbxassetid://104553006398763\", name = \"Fast Grab\", desc = \"Pick up eggs quicker\", color = Color3.fromRGB(80, 200, 255)},\n"
"\t{kind = \"Shield\", icon = \"rbxassetid://131653504755402\", name = \"Wave Shield\", desc = \"Survive 1 wave hit on every trip\", color = Color3.fromRGB(170, 110, 255)},",
"\t-- (2026-10-22 UI polish, M5) shorter descriptions so they read at >= 16 px base in their 0.28-wide box\n"
"\t{kind = \"Sling\", icon = \"rbxassetid://84334196742101\", name = \"Slingshot Power\", desc = \"Launch further\", color = Color3.fromRGB(255, 150, 40)},\n"
"\t{kind = \"Grab\", icon = \"rbxassetid://104553006398763\", name = \"Fast Grab\", desc = \"Grab eggs faster\", color = Color3.fromRGB(80, 200, 255)},\n"
"\t{kind = \"Shield\", icon = \"rbxassetid://131653504755402\", name = \"Wave Shield\", desc = \"Block 1 wave hit\", color = Color3.fromRGB(170, 110, 255)},")
add(UP,
"\tlocal _, btn = B.brick(f, \"Buy\", UDim2.fromScale(0.17, 0.62), UDim2.fromScale(0.77, 0.5), GREEN, nil, {button = true, radius = 0.18, stroke = 0.04})",
"\tlocal _, btn = B.brick(f, \"Buy\", UDim2.fromScale(0.2, 0.66), UDim2.fromScale(0.765, 0.5), GREEN, nil, {button = true, radius = 0.18, stroke = 0.04}) -- (M5 / M7: 0.17 x 0.62)")
add(UP,
"\tlocal price = B.text(btn, \"Price\", B.LUCKY, WHITE, UDim2.fromScale(0.62, 0.55), UDim2.fromScale(0.62, 0.52), 0.08)",
"\tlocal price = B.text(btn, \"Price\", B.LUCKY, WHITE, UDim2.fromScale(0.66, 0.55), UDim2.fromScale(0.62, 0.52), 0.08)")
add(UP,
"\t\tif level >= max then return (\"Range %d studs (%s)\"):format(now, U.areaAt(now)) end\n"
"\t\treturn (\"Range %d → <font color='#7dff5a'>%d</font> studs (%s)\"):format(now, new, U.areaAt(new))\n"
"\telseif kind == \"Grab\" then\n"
"\t\tif level >= max then return (\"Grab time %.1fs\"):format(U.grabTime(level)) end\n"
"\t\treturn (\"Grab time %.1fs → <font color='#7dff5a'>%.1fs</font>\"):format(U.grabTime(level), U.grabTime(nxt))\n"
"\telse\n"
"\t\tlocal function hits(n) return n == 1 and \"1 hit\" or (n .. \" hits\") end\n"
"\t\tif level >= max then return \"Survive \" .. hits(level) .. \" per trip\" end\n"
"\t\treturn (\"Survive %s → <font color='#7dff5a'>%s</font> per trip\"):format(hits(level), hits(nxt))",
"\t\t-- (2026-10-22 UI polish, M5) short stat lines (>= 16 px base in a 0.25-wide box): the numbers only\n"
"\t\tif level >= max then return (\"%d studs\"):format(now) end\n"
"\t\treturn (\"%d → <font color='#7dff5a'>%d</font> studs\"):format(now, new)\n"
"\telseif kind == \"Grab\" then\n"
"\t\tif level >= max then return (\"%.1fs grab\"):format(U.grabTime(level)) end\n"
"\t\treturn (\"%.1fs → <font color='#7dff5a'>%.1fs</font>\"):format(U.grabTime(level), U.grabTime(nxt))\n"
"\telse\n"
"\t\tlocal function hits(n) return n == 1 and \"1 hit\" or (n .. \" hits\") end\n"
"\t\tif level >= max then return hits(level) .. \" blocked\" end\n"
"\t\treturn (\"%s → <font color='#7dff5a'>%s</font>\"):format(tostring(level), hits(nxt))")

add(RB,
"local skipBusy = false\nskipBtn.Activated:Connect(function()\n\tif skipBusy or RebirthConfig.isMax(player:GetAttribute(\"Rebirths\") or 0) then return end",
"local skipBusy = false\nlocal function pressSkip()\n\tif skipBusy or RebirthConfig.isMax(player:GetAttribute(\"Rebirths\") or 0) then return end")
add(RB,
"\t\ttask.delay(1.35, refresh)\n\tend\nend)\n\n---------------------------------------------------------------- motion: spinning rays",
"\t\ttask.delay(1.35, refresh)\n\tend\nend\nskipBtn.Activated:Connect(pressSkip)\nB.tapArea(skipBtn, pressSkip) -- (2026-10-22 UI polish, M7)\n\n"
"---------------------------------------------------------------- motion: spinning rays")

# Upgrades: the buy / +1 LV / [X] tap areas
add(UP,
"for kind, row in rows do\n\trow.btn.Activated:Connect(function()\n\t\tlocal ok, r = Buy:InvokeServer(kind)\n",
"for kind, row in rows do\n\tlocal function buy()\n\t\tlocal ok, r = Buy:InvokeServer(kind)\n")
add(UP,
"\t\trefresh()\n\tend)\nend\nfor kind, row in rows do\n\trow.rbtn.Activated:Connect(function()\n\t\tlocal ok, r = Buy:InvokeServer(kind, \"robux\")\n",
"\t\trefresh()\n\tend\n\trow.btn.Activated:Connect(buy)\n\tB.tapArea(row.btn, buy) -- (2026-10-22 UI polish, M7)\nend\n"
"for kind, row in rows do\n\tlocal function buyLevel()\n\t\tlocal ok, r = Buy:InvokeServer(kind, \"robux\")\n")
add(UP,
"\t\t\ttask.delay(1.25, refresh)\n\t\tend\n\tend)\nend\nfor _, attr in {\"Money\", \"Rebirths\", \"SlingLevel\", \"GrabLevel\", \"ShieldLevel\", \"FreeSling\"} do",
"\t\t\ttask.delay(1.25, refresh)\n\t\tend\n\tend\n\trow.rbtn.Activated:Connect(buyLevel)\n\tB.tapArea(row.rbtn, buyLevel)\nend\n"
"for _, attr in {\"Money\", \"Rebirths\", \"SlingLevel\", \"GrabLevel\", \"ShieldLevel\", \"FreeSling\"} do")
add(UP,
"closeF.Activated:Connect(function() setOpen(false) end)",
"closeF.Activated:Connect(function() setOpen(false) end)\nB.tapArea(closeF, function() setOpen(false) end) -- (2026-10-22 UI polish, M7)")

# ------------------------------------------------------------------------------------------------ FreeGiftClientLegacy (M8)
FG = SPS + "FreeGiftClientLegacy"
add(FG,
"local SFX = require(RS:WaitForChild(\"SFX\"))\nlocal PotionConfig = require(RS:WaitForChild(\"PotionConfig\"))",
"local SFX = require(RS:WaitForChild(\"SFX\"))\nlocal PotionConfig = require(RS:WaitForChild(\"PotionConfig\"))\n"
"local B = require(RS:WaitForChild(\"BrickUI\")) -- (2026-10-22 UI polish: B.tapArea)")
add(FG,
"local likeCard, likeWell = card(\"Like\", UDim2.fromOffset(145, 290), \"1. Like the game!\")\n"
"new(\"TextLabel\", {Name = \"Thumb\", Text = \"\U0001F44D\", TextScaled = true, Font = FONT, BackgroundTransparency = 1, Size = UDim2.fromOffset(56, 56),\n"
"\tPosition = UDim2.fromOffset(42, 40), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 6}, likeWell)\n"
"local how = text(likeWell, {Name = \"How\", Text = TOUCH and \"Tap LIKE on the game page!\" or \"Click LIKE on the game page!\", Size = UDim2.fromOffset(150, 50),\n"
"\tPosition = UDim2.fromOffset(150, 40), ZIndex = 6, Stroke = 2})\n"
"new(\"UITextSizeConstraint\", {MaxTextSize = 20}, how)\n"
"\n"
"local groupCard, groupWell, groupDone = card(\"Group\", UDim2.fromOffset(415, 290), \"2. Join the group!\")",
"-- (2026-10-22 owner: the like step is NO LONGER required) the reward needs the group only. A small friendly like ask stays\n"
"-- under the reward lines: no tick, no number, never checked, it never changes CLAIM. The group card is the one step.\n"
"local likeAsk = text(win, {Name = \"LikeAsk\", Text = \"Like the game too! \U0001F44D\", Size = UDim2.fromOffset(260, 18), Position = UDim2.fromOffset(378, 223),\n"
"\tTextColor3 = Color3.fromRGB(255, 225, 120), ZIndex = 5, Stroke = 2})\n"
"\n"
"local groupCard, groupWell, groupDone = card(\"Group\", UDim2.fromOffset(280, 301), \"Join the group!\")")
add(FG,
"local hint = text(win, {Name = \"Hint\", Text = \"\", Size = UDim2.fromOffset(420, 18), Position = UDim2.fromOffset(280, 367),",
"local hint = text(win, {Name = \"Hint\", Text = \"\", Size = UDim2.fromOffset(420, 16), Position = UDim2.fromOffset(280, 376),")
add(FG,
"local claimBtn, claimLabel, claimGrad = standardButton(win, \"Claim\", UDim2.fromOffset(236, 56), UDim2.fromOffset(280, 408), \"CLAIM!\", CLAIM_GRAD, 34)",
"local claimBtn, claimLabel, claimGrad = standardButton(win, \"Claim\", UDim2.fromOffset(236, 56), UDim2.fromOffset(280, 416), \"CLAIM!\", CLAIM_GRAD, 34)")
add(FG,
"local joined = false\nlocal function checkGroup()\n\tlocal ok, member = pcall(player.IsInGroup, player, GROUP_ID)\n\tif ok and member then joined = true end\nend",
"local joined = false\n"
"-- (2026-10-22 owner: the reward needs the group only) the SERVER's group check decides (FreeGift.InGroup runs the same\n"
"-- inGroup() as the claim, uncached), so the UI and the claim always agree; IsInGroup (cached per session) is the fallback\n"
"local InGroup = folder:WaitForChild(\"InGroup\", 10)\n"
"local function checkGroup()\n"
"\tif InGroup then\n"
"\t\tlocal ok, member = pcall(InGroup.InvokeServer, InGroup)\n"
"\t\tif ok and type(member) == \"boolean\" then joined = member return end\n"
"\tend\n"
"\tlocal ok, member = pcall(player.IsInGroup, player, GROUP_ID)\n"
"\tif ok and member then joined = true end\nend")
add(FG,
"\tlocal done = claimed()\n\tclaimLabel.Text = done and \"CLAIMED!\" or \"CLAIM!\"\n\tclaimGrad.Color = done and CLAIMED_GRAD or CLAIM_GRAD\n\tclaimBtn.Active = not done",
"\tlocal done = claimed()\n"
"\t-- CLAIM! lime when you're in the group, silver JOIN FIRST when not (a press then opens the join prompt), CLAIMED! after\n"
"\tclaimLabel.Text = done and \"CLAIMED!\" or (joined and \"CLAIM!\" or \"JOIN FIRST\")\n"
"\tclaimGrad.Color = (done or not joined) and CLAIMED_GRAD or CLAIM_GRAD\n"
"\tclaimBtn.Active = not done")
add(FG,
"claimBtn.Activated:Connect(function()\n\tif busy or claimed() then return end\n\tbusy = true",
"local function pressClaim()\n\tif busy or claimed() then return end\n\tif not joined then promptJoin() return end -- (the group is the one step)\n\tbusy = true")
add(FG,
"\telseif ok and why == \"wait\" then\n\t\tshowHint(\"Loading your data... try again in a second!\")\n\tend\nend)",
"\telseif ok and why == \"wait\" then\n\t\tshowHint(\"Loading your data... try again in a second!\")\n\tend\nend\n"
"claimBtn.Activated:Connect(pressClaim)\n"
"B.tapArea(claimBtn, pressClaim) B.tapArea(joinBtn, promptJoin) -- (2026-10-22 UI polish, M7: >= 44 pt on a phone)")
add(FG,
"\t\tcheckGroup()\n\t\trefresh()\n\t\twindowScale.Scale = deviceScale()",
"\t\trefresh() -- (2026-10-22 UI polish) opens at once with the last answer; the server check follows\n"
"\t\ttask.spawn(function() checkGroup() refresh() end)\n\t\twindowScale.Scale = deviceScale()")
add(FG,
"\treturn math.clamp(math.min(vp.X / 1050, vp.Y / 620), 0.52, 1.18)\nend\nworkspace.CurrentCamera:GetPropertyChangedSignal(\"ViewportSize\"):Connect(function() windowScale.Scale = deviceScale() end)",
"\treturn math.clamp(math.min(vp.X / 1050, vp.Y / 620), 0.7, 1.18) -- (2026-10-22 UI polish, M5: phone floor 0.7, was 0.52)\nend\n"
"workspace.CurrentCamera:GetPropertyChangedSignal(\"ViewportSize\"):Connect(function() windowScale.Scale = deviceScale() end)")
add(FG,
"close.Activated:Connect(function() setOpen(false) end)\ntask.spawn(function()\n\tlocal opened = mainMenu:WaitForChild(\"WindowOpened\", 30)",
"close.Activated:Connect(function() setOpen(false) end)\nB.tapArea(close, function() setOpen(false) end) -- (2026-10-22 UI polish, M7)\n"
"task.spawn(function()\n\tlocal opened = mainMenu:WaitForChild(\"WindowOpened\", 30)")

# ------------------------------------------------------------------------------------------------ FreeGiftServer (M8)
FS = "game.ServerScriptService.FreeGiftServer"
add(FS,
"-- ONCE per player (saved PlayerData.FreeGift). A game can't see likes, so the like step is on trust.",
"-- ONCE per player (saved PlayerData.FreeGift). (2026-10-22 owner) The like is a friendly ask only: never checked, never\n"
"-- required. The reward needs the group. FreeGift.InGroup() lets the window show the SAME check the claim runs.\n"
"-- Studio only: player attribute FreeGiftTestNotInGroup = true makes inGroup() answer false (tests).")
add(FS,
"local function inGroup(player)\n\tlocal ok, groups = pcall(GroupService.GetGroupsAsync, GroupService, player.UserId)",
"local function inGroup(player)\n"
"\tif game:GetService(\"RunService\"):IsStudio() and player:GetAttribute(\"FreeGiftTestNotInGroup\") == true then return false end\n"
"\tlocal ok, groups = pcall(GroupService.GetGroupsAsync, GroupService, player.UserId)")
add(FS,
"local busy, last = {}, {}\nClaim.OnServerInvoke = function(player)",
"-- the window's group state = the claim's own check (1 call per 2 s per player; a faster call gets the last answer)\n"
"local InGroup = folder:FindFirstChild(\"InGroup\") or Instance.new(\"RemoteFunction\")\n"
"InGroup.Name = \"InGroup\"\nInGroup.Parent = folder\n"
"local lastCheck, lastAnswer = {}, {}\n"
"InGroup.OnServerInvoke = function(player)\n"
"\tlocal now = os.clock()\n"
"\tif lastCheck[player] and now - lastCheck[player] < 2 and lastAnswer[player] ~= nil then return lastAnswer[player] end\n"
"\tlastCheck[player] = now\n"
"\tlastAnswer[player] = inGroup(player)\n"
"\treturn lastAnswer[player]\n"
"end\n\n"
"local busy, last = {}, {}\nClaim.OnServerInvoke = function(player)")
add(FS,
"Players.PlayerRemoving:Connect(function(p)\n\tbusy[p], last[p] = nil, nil\nend)",
"Players.PlayerRemoving:Connect(function(p)\n\tbusy[p], last[p] = nil, nil\n\tlastCheck[p], lastAnswer[p] = nil, nil\nend)")

# ------------------------------------------------------------------------------------------------ OfflineClientLegacy (M9, M1, M7)
OF = SPS + "OfflineClientLegacy"
add(OF,
"local OfflineConfig = require(RS:WaitForChild(\"OfflineConfig\"))",
"local OfflineConfig = require(RS:WaitForChild(\"OfflineConfig\"))\n"
"local B = require(RS:WaitForChild(\"BrickUI\")) -- (2026-10-22 UI polish: B.tapArea)")
add(OF,
"-- buttons: CLAIM x5! (rainbow, live price on its corner) + CLAIM!\n"
"local x5Btn, x5Label = standardButton(win, \"ClaimX5\", UDim2.fromOffset(240, 64), UDim2.fromOffset(160, 364), \"CLAIM x5!\", RAINBOW, 36, 20)\n"
"-- (2026-10-22 UI revert) the x5 price sits just above the button, no longer over its corner (was y 330)\n"
"local priceTag = new(\"Frame\", {Name = \"Price\", Size = UDim2.fromOffset(92, 28), Position = UDim2.fromOffset(50, 308), AnchorPoint = Vector2.new(0.5, 0.5),\n"
"\tBackgroundTransparency = 1, ZIndex = 10}, win)\n"
"local priceText = text(priceTag, {Name = \"Amount\", Text = tostring(OfflineConfig.PRICE), Size = UDim2.fromOffset(50, 28), Position = UDim2.fromOffset(0, 14),\n"
"\tAnchorPoint = Vector2.new(0, 0.5), TextXAlignment = Enum.TextXAlignment.Right, ZIndex = 10, Stroke = 2.6})\n"
"grad(priceText, MONEY_GRAD)\n"
"new(\"ImageLabel\", {Name = \"Robux\", Image = ROBUX, ImageColor3 = Color3.fromRGB(120, 255, 60), ScaleType = Enum.ScaleType.Fit, BackgroundTransparency = 1,\n"
"\tSize = UDim2.fromOffset(26, 26), Position = UDim2.fromOffset(56, 14), AnchorPoint = Vector2.new(0, 0.5), ZIndex = 10}, priceTag)\n"
"local claimBtn, claimLabel = standardButton(win, \"Claim\", UDim2.fromOffset(200, 64), UDim2.fromOffset(400, 364), \"CLAIM!\", CLAIM_GRAD, 36)",
"-- buttons (2026-10-22 UI polish, M9): the FREE claim is the loudest - CLAIM! lime, 270 x 68, on the right; CLAIM x5 gold\n"
"-- (the Check-UI Skip amber), 230 x 68, on the left, its price INSIDE (M1: the Robux icon + price 8 px from its right\n"
"-- edge). No rainbow on the paid button. (Was: CLAIM x5! rainbow 240 x 64 with the price above it, CLAIM! 200 x 64.)\n"
"local GOLD_GRAD = seq(Color3.fromRGB(255, 208, 0), Color3.fromRGB(255, 140, 0))\n"
"local x5Btn, x5Label = standardButton(win, \"ClaimX5\", UDim2.fromOffset(230, 68), UDim2.fromOffset(132, 364), \"CLAIM x5\", GOLD_GRAD, 24)\n"
"x5Label.Size = UDim2.new(1, -88, 1, 0)\n"
"x5Label.Position = UDim2.new(0, 10, 0.5, -1)\n"
"x5Label.AnchorPoint = Vector2.new(0, 0.5)\n"
"x5Label.TextXAlignment = Enum.TextXAlignment.Left\n"
"local priceTag = new(\"Frame\", {Name = \"Price\", Size = UDim2.fromOffset(70, 30), Position = UDim2.new(1, -8, 0.5, -1), AnchorPoint = Vector2.new(1, 0.5),\n"
"\tBackgroundTransparency = 1, ZIndex = 9}, x5Btn)\n"
"new(\"ImageLabel\", {Name = \"RobuxOutline\", Image = ROBUX, ImageColor3 = BLACK, ScaleType = Enum.ScaleType.Fit, BackgroundTransparency = 1,\n"
"\tSize = UDim2.fromOffset(28, 28), Position = UDim2.fromOffset(14, 15), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 9}, priceTag)\n"
"new(\"ImageLabel\", {Name = \"Robux\", Image = ROBUX, ImageColor3 = WHITE, ScaleType = Enum.ScaleType.Fit, BackgroundTransparency = 1,\n"
"\tSize = UDim2.fromOffset(22, 22), Position = UDim2.fromOffset(14, 15), AnchorPoint = Vector2.new(0.5, 0.5), ZIndex = 10}, priceTag)\n"
"local priceText = text(priceTag, {Name = \"Amount\", Text = tostring(OfflineConfig.PRICE), Size = UDim2.fromOffset(40, 28), Position = UDim2.new(1, 0, 0.5, 0),\n"
"\tAnchorPoint = Vector2.new(1, 0.5), TextXAlignment = Enum.TextXAlignment.Right, ZIndex = 10, Stroke = 2.6})\n"
"local claimBtn, claimLabel = standardButton(win, \"Claim\", UDim2.fromOffset(270, 68), UDim2.fromOffset(392, 364), \"CLAIM!\", CLAIM_GRAD, 38)")
add(OF,
"\treturn math.clamp(math.min(vp.X / 1050, vp.Y / 620), 0.52, 1.18)\nend",
"\treturn math.clamp(math.min(vp.X / 1050, vp.Y / 620), 0.7, 1.18) -- (2026-10-22 UI polish, M5: phone floor 0.7, was 0.52)\nend")
add(OF,
"claimBtn.Activated:Connect(claimNormal)\nclose.Activated:Connect(claimNormal) -- X claims the x1 too: nothing is ever lost",
"claimBtn.Activated:Connect(claimNormal)\nclose.Activated:Connect(claimNormal) -- X claims the x1 too: nothing is ever lost\n"
"B.tapArea(close, claimNormal) -- (2026-10-22 UI polish, M7: the [X] was 27 pt on a phone)")

# ------------------------------------------------------------------------------------------------ StarterPackClient (Starter items, M7)
ST = SPS + "StarterPackClient"
add(ST,
"local function updateTimer()\n\tlocal left = timeLeft()\n\ttagText.Text = \"ENDS IN \" .. P.clockText(left)\n\ttagGrad.Color = left < 3600 and RED_TIMER or GOLD_TIMER\nend",
"local function updateTimer()\n\tlocal left = timeLeft()\n\ttagText.Text = \"ENDS IN \" .. P.clockText(left)\n"
"\ttagGrad.Color = GOLD_TIMER -- (2026-10-22 UI polish: no red last-hour escalation, Roblox: no pushy urgency with minors)\nend")
add(ST,
"local noBtn = standardButton(win, \"NoThanks\", UDim2.fromOffset(170, 56), UDim2.fromOffset(115, 382), \"NO THANKS\", SILVER_GRAD, 22)",
"local noBtn = standardButton(win, \"NoThanks\", UDim2.fromOffset(170, 64), UDim2.fromOffset(115, 382), \"NO THANKS\", SILVER_GRAD, 22) -- (M7: 56 tall)")
add(ST,
"\tbuyWord.Size = UDim2.fromOffset(270, 38)\nend",
"\tbuyWord.Size = UDim2.fromOffset(270, 38)\n"
"\ttagText.Visible = word ~= \"OFFER ENDED\" -- (2026-10-22 UI polish) the timer hides while OFFER ENDED shows\nend")
add(ST,
"\ttitle.Text = \"STARTER PACK!\"\n\tif os.clock() > flashUntil then\n\t\tbuyWord.Text = \"BUY\"",
"\ttitle.Text = \"STARTER PACK!\"\n\tif os.clock() > flashUntil then\n\t\ttagText.Visible = true\n\t\tbuyWord.Text = \"BUY\"")
add(ST,
"\t\t\tcard.tag.BackgroundColor3 = left < 3600 and C(230, 30, 60) or C(255, 170, 0)",
"\t\t\tcard.tag.BackgroundColor3 = C(255, 170, 0) -- (2026-10-22 UI polish: no red last hour)")
add(ST,
"\t\tif card and card.row.Visible then",
"\t\tif card and card.row.Visible and menuWin.Visible then -- (2026-10-22 UI polish: nothing runs while the Shop is closed)")
add(ST,
"\treturn math.clamp(math.min(vp.X / 1050, vp.Y / 620), 0.52, 1.18)\nend\nworkspace.CurrentCamera:GetPropertyChangedSignal(\"ViewportSize\"):Connect(function() windowScale.Scale = deviceScale() end)",
"\treturn math.clamp(math.min(vp.X / 1050, vp.Y / 620), 0.7, 1.18) -- (2026-10-22 UI polish, M5: phone floor 0.7, was 0.52)\nend\n"
"workspace.CurrentCamera:GetPropertyChangedSignal(\"ViewportSize\"):Connect(function() windowScale.Scale = deviceScale() end)")
add(ST,
"close.Activated:Connect(closePopup)\nnoBtn.Activated:Connect(closePopup)\nbackdrop.Activated:Connect(closePopup)",
"close.Activated:Connect(closePopup)\nnoBtn.Activated:Connect(closePopup)\nbackdrop.Activated:Connect(closePopup)\n"
"B.tapArea(close, closePopup) B.tapArea(noBtn, closePopup) -- (2026-10-22 UI polish, M7)")

# ------------------------------------------------------------------------------------------------ StarterPackHud (Starter items)
SHUD = SPS + "StarterPackHud"
add(SHUD,
"local FULL, COMPACT = V(150, 170), V(150, 156) -- Root at the 1050x620 baseline: art + caption / art only (incl. the motion envelope)",
"local FULL, COMPACT = V(150, 186), V(150, 156) -- Root at the 1050x620 baseline: art + caption / art only (incl. the motion envelope)\n"
"-- (2026-10-22 UI polish: FULL 170 -> 186, the timer moved BELOW the egg and the caption under it)")
add(SHUD,
"local CAPTION_Y = 156 -- the caption's centre in Root px (FULL only): right under the art like reference 1",
"local CAPTION_Y = 175 -- the caption's centre in Root px (FULL only): under the timer (2026-10-22 UI polish: was 156)")
add(SHUD,
"local PRICE_OFF, PRICE_OFF_COMPACT = V(38, 50), V(38, 53)",
"local PRICE_OFF, PRICE_OFF_COMPACT = V(44, 18), V(44, 18) -- (2026-10-22 UI polish: the egg's right flank, clear of the timer below)")
add(SHUD,
"new(\"ImageLabel\", {Name = \"RobuxOutline\", Image = ROBUX, ImageColor3 = BLACK, BackgroundTransparency = 1, AnchorPoint = V(0.5, 0.5),\n"
"\tScaleType = Enum.ScaleType.Fit, Size = UDim2.fromOffset(22, 22), Position = UDim2.fromOffset(10, 12), ZIndex = 9}, price)\n"
"new(\"ImageLabel\", {Name = \"Robux\", Image = ROBUX, ImageColor3 = C(150, 255, 40), BackgroundTransparency = 1, AnchorPoint = V(0.5, 0.5),\n"
"\tScaleType = Enum.ScaleType.Fit, Size = UDim2.fromOffset(18, 18), Position = UDim2.fromOffset(10, 12), ZIndex = 10}, price)\n"
"local amount = new(\"TextLabel\", {Name = \"Amount\", Text = tostring(ShopConfig.StarterPackPrice), Font = FONT, TextSize = 22,\n"
"\tTextColor3 = WHITE, TextXAlignment = Enum.TextXAlignment.Left, BackgroundTransparency = 1, AnchorPoint = V(0, 0.5),\n"
"\tPosition = UDim2.fromOffset(20, 12), Size = UDim2.fromOffset(32, 24), ZIndex = 10}, price)\n"
"new(\"UIGradient\", {Rotation = 90, Color = ColorSequence.new(C(200, 255, 80), C(90, 220, 0))}, amount) -- the Check-UI lime\n"
"stroke(amount, 3)",
"-- (2026-10-22 UI polish) a GOLD pill (Check-UI Skip amber) with an INK Robux glyph + price: it no longer sits lime on the\n"
"-- green potion\n"
"price.BackgroundTransparency = 0\nprice.BackgroundColor3 = WHITE\n"
"new(\"UIGradient\", {Rotation = 90, Color = ColorSequence.new(C(255, 208, 0), C(255, 140, 0))}, price)\n"
"new(\"UICorner\", {CornerRadius = UDim.new(0.5, 0)}, price)\n"
"new(\"UIStroke\", {Thickness = 2, Color = BLACK, ApplyStrokeMode = Enum.ApplyStrokeMode.Border}, price)\n"
"new(\"ImageLabel\", {Name = \"Robux\", Image = ROBUX, ImageColor3 = C(17, 23, 26), BackgroundTransparency = 1, AnchorPoint = V(0.5, 0.5),\n"
"\tScaleType = Enum.ScaleType.Fit, Size = UDim2.fromOffset(16, 16), Position = UDim2.fromOffset(12, 12), ZIndex = 10}, price)\n"
"local amount = new(\"TextLabel\", {Name = \"Amount\", Text = tostring(ShopConfig.StarterPackPrice), Font = FONT, TextSize = 20,\n"
"\tTextColor3 = C(17, 23, 26), TextXAlignment = Enum.TextXAlignment.Left, BackgroundTransparency = 1, AnchorPoint = V(0, 0.5),\n"
"\tPosition = UDim2.fromOffset(22, 12), Size = UDim2.fromOffset(28, 24), ZIndex = 10}, price)")
add(SHUD,
"local TIMER_OFF, TIMER_OFF_COMPACT = V(0, 33), V(0, 33) -- from the egg's centre (Float px)",
"local TIMER_OFF, TIMER_OFF_COMPACT = V(0, 69), V(0, 69) -- from the egg's centre (Float px): BELOW the egg, 6 px clear of its outline (2026-10-22 UI polish: was ON the egg at (0, 33))")
add(SHUD,
"\tif urgent ~= was or force then timerGrad.Color = urgent and TIMER_RED or TIMER_GOLD end",
"\tif urgent ~= was or force then timerGrad.Color = TIMER_GOLD end -- (2026-10-22 UI polish: no red last hour)")
add(SHUD,
"\ttimerScale.Scale = timerBase * ((urgent and not reduced) and (1 + 0.10 * (0.5 - 0.5 * math.cos(TAU * t))) or 1)",
"\ttimerScale.Scale = timerBase -- (2026-10-22 UI polish: no last-hour pulse)")
add(SHUD,
"\tcolRight = math.min(colRight, gs.X)",
"\tcolRight = math.min(colRight, gs.X - 8 * k) -- (2026-10-22 UI polish: 8 px inside the right edge on phones, the egg was clipped)")

# ------------------------------------------------------------------------------------------------ write
os.makedirs(HERE, exist_ok=True)
for path, edits in P.items():
    name = path.split(".")[-1]
    with open(os.path.join(HERE, name + ".json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"file_path": path, "datamodel_type": "Edit", "edits": [{"old_string": o, "new_string": n} for o, n in edits]}, f, ensure_ascii=False, indent=1)
    print(f"{name:24s} {len(edits)} edits")
print("total", sum(len(e) for e in P.values()))
