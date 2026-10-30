-- hatch_pure.lua (2026-10-21, plan 8.1): BrickUI.Hatch pure checks. Edit datamodel (a clone: Edit caches requires).
local src = game.ReplicatedStorage.BrickUI:FindFirstChild("Hatch")
if not src then return "pass 0 fail 1\nFAIL BrickUI.Hatch missing" end
local c = src:Clone()
c.Parent = src.Parent
local ok, H = pcall(require, c)
c:Destroy()
if not ok then return "pass 0 fail 1\nFAIL require: " .. tostring(H) end
local pass, fail, lines = 0, 0, {}
local function check(name, cond, detail)
	if cond then pass += 1 else fail += 1 table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end
end
local function near(a, b, t) return math.abs(a - b) <= t end
-- 1 fitWindow, the 4 rows of plan section 3
for _, row in {
	{{1920, 1022, 412.1}, {1.18, 873.2, 554.6, 960, 511}},
	{{1050, 562, 229.3}, {1.0982, 812.7, 516.2, 635.65, 281}},
	{{732, 346, 144.3}, {0.7106, 525.9, 334.0, 407.24, 173}},
	{{667, 331, 137.9}, {0.6787, 502.3, 319.0, 389.03, 165.5}},
} do
	local s, w, h, cx, cy = H.fitWindow(row[1][1], row[1][2], row[1][3])
	local e = row[2]
	check(("fitWindow %d x %d"):format(row[1][1], row[1][2]),
		near(s, e[1], 0.05) and near(w, e[2], 0.5) and near(h, e[3], 0.5) and near(cx, e[4], 0.5) and near(cy, e[5], 0.5),
		("%.4f %.1f %.1f %.2f %.1f"):format(s, w, h, cx, cy))
end
-- 2 floor
check("fitWindow floor 0.5", H.fitWindow(500, 300, 140) == 0.5, H.fitWindow(500, 300, 140))
-- 3 header teeth
check("#HEADER_TEETH 37", #H.HEADER_TEETH == 37, #H.HEADER_TEETH)
local l, r, b = 1e9, -1e9, -1e9
for _, t in H.HEADER_TEETH do
	local half = (t[2] + 5) * math.sqrt(2) / 2
	l = math.min(l, t[1] - half) r = math.max(r, t[1] + half) b = math.max(b, 46 + half)
end
check("header teeth extents", l >= 0 and r <= 740 and b <= 62, ("%.2f %.2f %.2f"):format(l, r, b))
-- 4 shell teeth
check("#SHELL_TEETH 4", #H.SHELL_TEETH == 4)
local sl, sr, st, sb = 1e9, -1e9, 1e9, -1e9
for _, t in H.SHELL_TEETH do
	local half = (t[2] + 5) * math.sqrt(2) / 2
	sl = math.min(sl, t[1] - half) sr = math.max(sr, t[1] + half) st = math.min(st, 17 - half) sb = math.max(sb, 17 + half)
end
check("shell teeth extents", sl >= 0 and sr <= 104 and st >= 0 and sb <= 60, ("%.2f %.2f %.2f %.2f"):format(sl, sr, st, sb))
-- 5 palettes, bands, icons
for _, p in {"lime", "red", "silver", "off", "gold", "dusk"} do check("palette " .. p, H.PAL[p] ~= nil and H.PAL[p].side ~= nil) end
for _, b in {"Pumpkin", "HatchGold"} do check("band " .. b, H.BAND[b] ~= nil and H.BAND[b].tooth ~= nil) end
local icons = 0
for k, v in H.ICON do icons += 1 check("icon " .. k, type(v) == "string" and v:match("^rbxassetid://%d+$") ~= nil, v) end
check("icon count 12 (11 + robuxWhite, popup/shop plan 4.0)", icons == 12, icons)
-- 6 fit
local lab = Instance.new("TextLabel")
lab.Size = UDim2.fromOffset(150, 22)
lab:SetAttribute("HatchBase", 20)
lab:SetAttribute("HatchMin", 16)
local s = Instance.new("UIStroke") s.Thickness = 2.5 s.Parent = lab
check("fit $9K", H.fit(lab, "$9K") == true and lab.TextSize == 20, lab.TextSize)
check("fit variants", H.fit(lab, {"A VERY LONG LINE THAT CANNOT FIT HERE", "OK"}) == true and lab.Text == "OK", lab.Text)
local okFit = H.fit(lab, "A VERY LONG LINE THAT CANNOT FIT HERE")
check("fit fails at min", okFit == false and lab.TextSize == 16, tostring(okFit) .. " " .. lab.TextSize)
lab:Destroy()
-- 7 (MUST 3) stickers are centre-anchored at (x + size/2, y + size/2), the shadow 3 px lower
local holder = Instance.new("Frame")
local im, sh = H.sticker(holder, "Check", H.ICON.check, 50, 27, 58, 2)
check("sticker anchor", im.AnchorPoint == Vector2.new(0.5, 0.5) and sh.AnchorPoint == Vector2.new(0.5, 0.5))
check("sticker centre", im.Position == UDim2.fromOffset(79, 56) and sh.Position == UDim2.fromOffset(79, 59), tostring(im.Position))
-- 8 (MUST 2) glossButton hoverScale
local b1 = H.glossButton(holder, "Pill", 3, 3, 148, 32, "lime", {d = 3, r = 15, ol = 2, hoverScale = 1, faceFrame = true})
local b2 = H.glossButton(holder, "Btn", 8, 130, 142, 27, "lime", {text = "CLAIM!"})
check("glossButton hoverScale", b1.hoverScale == 1 and b2.hoverScale == 1.04, tostring(b1.hoverScale) .. " " .. tostring(b2.hoverScale))
check("glossButton centre-anchored", b2.holder.AnchorPoint == Vector2.new(0.5, 0.5) and b2.holder.Position == UDim2.fromOffset(79, 143.5), tostring(b2.holder.Position))
check("glossButton label box", b2.label and b2.label.Position == UDim2.fromOffset(0, 2) and b2.label.Size == UDim2.fromOffset(142, 20), b2.label and tostring(b2.label.Position))
-- (2026-10-21 fix round, visual review MUST 1) H.chip height argument: the hero's chips are 28 tall, the default stays 30
local ch28 = H.chip(holder, "C28", 10, 262, 74, 28)
local ch30 = H.chip(holder, "C30", 10, 262, 74)
check("chip h 28 / default 30", ch28.Size == UDim2.fromOffset(74, 28) and ch30.Size == UDim2.fromOffset(74, 30)
	and ch28:FindFirstChildOfClass("UICorner").CornerRadius == UDim.new(0, 14) and ch30:FindFirstChildOfClass("UICorner").CornerRadius == UDim.new(0, 15))
holder:Destroy()
-- 9 celebration teeth / crack
check("#CEL_TEETH 7", #H.CEL_TEETH == 7 and near(H.CEL_TEETH[7][1], 150, 0.01), H.CEL_TEETH[7] and H.CEL_TEETH[7][1])
check("#CEL_CRACK 9", #H.CEL_CRACK == 9)

---------------------------------------------------------------- popup/shop plan 7.1 + review MUST 1 / 4 / 5 / 6, SHOULD 11
-- (each block in a pcall: a missing helper is a FAIL line, not a crash)
local function try(name, f)
	local ok, err = pcall(f)
	if not ok then check(name, false, "error: " .. tostring(err)) end
end
-- 1 fitWindow, the popup rows (leftClear 0, modal, centred)
for _, row in {
	{{1920, 1022, 0}, {1.18, 873.2, 554.6, 960, 511}},
	{{1050, 562, 0}, {1.1702, 866.0, 550.0, 525, 281}},
	{{732, 346, 0}, {0.7106, 525.9, 334.0, 366, 173}},
	{{667, 331, 0}, {0.6787, 502.3, 319.0, 333.5, 165.5}},
} do
	local s, w, h, cx, cy = H.fitWindow(row[1][1], row[1][2], row[1][3])
	local e = row[2]
	check(("fitWindow popup %d x %d"):format(row[1][1], row[1][2]),
		near(s, e[1], 0.0006) and near(w, e[2], 0.5) and near(h, e[3], 0.5) and near(cx, e[4], 0.5) and near(cy, e[5], 0.5),
		("%.4f %.1f %.1f %.2f %.1f"):format(s, w, h, cx, cy))
end
-- MUST 1: the Shop per-page cap (R = 0.8148, the measured Check-UI Shop height ratio, Task 0)
try("pageCap", function()
	check("SHOP_CAP_R 0.8148", near(H.SHOP_CAP_R, 0.8148, 1e-6), H.SHOP_CAP_R)
	local c = H.pageCap("Shop", 1022)
	check("pageCap Shop 1022 = 1.7718", near(c, 1.7718, 0.0005), c)
	local s, w, h, cx, cy = H.fitWindow(1920, 1022, 412.1, c)
	check("fitWindow 1920 Shop cap", near(s, 1.7718, 0.0005) and near(w, 1311.1, 0.5) and near(h, 832.7, 0.5) and near(cx, 1067.66, 0.5) and near(cy, 511, 0.01),
		("%.4f %.1f %.1f %.2f %.1f"):format(s, w, h, cx, cy))
	check("pageCap Shop 346 = 1.18", near(H.pageCap("Shop", 346), 1.18, 1e-9), H.pageCap("Shop", 346))
	check("pageCap Gift = nil", H.pageCap("Gift", 1022) == nil)
	check("pageCap nil page = nil", H.pageCap(nil, 1022) == nil)
end)
-- 2 bandTheme(page)
try("bandTheme", function()
	local was = workspace:GetAttribute("HatchBand")
	workspace:SetAttribute("HatchBand", nil)
	check("bandTheme Shop", H.bandTheme("Shop") == "Shop", H.bandTheme("Shop"))
	check("bandTheme StarterPack", H.bandTheme("StarterPack") == "Shop", H.bandTheme("StarterPack"))
	check("bandTheme Gift == bandTheme()", H.bandTheme("Gift") == H.bandTheme(), H.bandTheme("Gift"))
	workspace:SetAttribute("HatchBand", "HatchGold")
	check("bandTheme override wins", H.bandTheme("Shop") == "HatchGold", H.bandTheme("Shop"))
	workspace:SetAttribute("HatchBand", was)
end)
-- 3 constants
try("constants", function()
	local SC = require(game.ReplicatedStorage.ShopConfig)
	check("PAL.violet", H.PAL.violet ~= nil and H.PAL.violet.side == Color3.fromRGB(80, 20, 130))
	check("BAND.Shop", H.BAND.Shop ~= nil and H.BAND.Shop.tooth == Color3.fromRGB(220, 0, 100))
	check("PAGE_BAND", H.PAGE_BAND.Shop == "Shop" and H.PAGE_BAND.StarterPack == "Shop")
	check("ICON.robuxWhite = ShopConfig.ROBUX_ICON", H.ICON.robuxWhite == SC.ROBUX_ICON, H.ICON.robuxWhite)
	check("GOLD_TIMER / RED_TIMER", typeof(H.GOLD_TIMER) == "ColorSequence" and H.GOLD_TIMER.Keypoints[2].Value == Color3.fromRGB(255, 170, 0)
		and H.RED_TIMER.Keypoints[2].Value == Color3.fromRGB(255, 60, 50))
end)
-- 4 recess radius (default = the old TopShade / BottomLine), chip radius
try("recess", function()
	local hold = Instance.new("Frame")
	local r0 = H.recess(hold, "R0", 10, 66, 308, 38, 5)
	check("recess default TopShade", r0.TopShade.Position == UDim2.fromOffset(19, 0) and r0.TopShade.Size == UDim2.fromOffset(270, 3)
		and r0.BottomLine.Position == UDim2.fromOffset(19, 36.5) and r0:FindFirstChildOfClass("UICorner").CornerRadius == UDim.new(0, 19), tostring(r0.TopShade.Position))
	local r1 = H.recess(hold, "R1", 10, 66, 120, 386, 4, 20)
	check("recess radius 20", r1.TopShade.Position == UDim2.fromOffset(20, 0) and r1.TopShade.Size == UDim2.fromOffset(80, 3)
		and r1:FindFirstChildOfClass("UICorner").CornerRadius == UDim.new(0, 20), tostring(r1.TopShade.Position))
	local c14 = H.chip(hold, "C14", 318, 66, 412, 66, 14)
	check("chip radius 14", c14:FindFirstChildOfClass("UICorner").CornerRadius == UDim.new(0, 14))
	hold:Destroy()
end)
-- 5 priceButton (+ MUST 4 step-down, MUST 5 short refusal)
try("priceButton", function()
	local hold = Instance.new("Frame")
	local function group(b)
		-- the visible group: Pre text + Robux glyph + Price text (logical offsets in the face)
		local face = b.face
		local x0, x1 = 1e9, -1e9
		for _, n in {"Pre", "Price"} do
			local t = face:FindFirstChild(n)
			if t and t.Visible then
				local tw = H.textWidth(t.Text, t.TextSize)
				x0 = math.min(x0, t.Position.X.Offset) x1 = math.max(x1, t.Position.X.Offset + tw)
			end
		end
		local g = face:FindFirstChild("Robux")
		if g and g.Visible then
			x0 = math.min(x0, g.Position.X.Offset - g.Size.X.Offset / 2) x1 = math.max(x1, g.Position.X.Offset + g.Size.X.Offset / 2)
		end
		return x0, x1
	end
	local b = H.priceButton(hold, "Buy", 404, 20, 160, 56, {d = 4, r = 12, glyph = 30, size = 28})
	b.setPrice("49")
	local x0, x1 = group(b)
	check("priceButton 49 centred", near((x0 + x1) / 2, 80, 1), ("%.1f..%.1f"):format(x0, x1))
	check("priceButton gold", b.pal == "gold" and b.holder:GetAttribute("HatchPad") == 8 and b.holder:GetAttribute("HatchPadBottom") == 3)
	b.setWord("OWNED", "silver")
	check("setWord hides the glyph", b.face.Robux.Visible == false and b.face.Price.Visible == false and b.face.Word.Visible and b.face.Word.Text == "OWNED" and b.pal == "silver")
	b.setPrice("1250")
	x0, x1 = group(b)
	check("setPrice 1250 re-centred + gold", near((x0 + x1) / 2, 80, 1) and x1 - x0 <= 160 - 16 and b.pal == "gold" and b.face.Robux.Visible, ("%.1f..%.1f"):format(x0, x1))
	local t = H.priceButton(hold, "T", 452, 32, 112, 54, {d = 4, r = 12, glyph = 26, size = 26})
	t.setPrice("1499")
	local p = t.face.Price
	local G = 26 + 6 + p.Size.X.Offset
	x0, x1 = group(t)
	-- in-engine "1499"@26 is 55 px (the review estimated 68 with the wider mockup font): it fits at 26 (G 93)
	check("MUST 4: 1499 fits 112 (G <= 96), centred", G <= 96 and near((x0 + x1) / 2, 56, 1), ("G %.1f size %d group %.1f..%.1f"):format(G, p.TextSize, x0, x1))
	t.setPrice("99999") -- a wider price really steps down
	G = 26 + 6 + p.Size.X.Offset
	x0, x1 = group(t)
	check("MUST 4: 99999 steps down to fit", G <= 96 and p.TextSize < 26 and p.TextSize >= 18 and near((x0 + x1) / 2, 56, 1), ("G %.1f size %d group %.1f..%.1f"):format(G, p.TextSize, x0, x1))
	local w2 = H.priceButton(hold, "W", 326, 32, 112, 54, {d = 4, r = 12, glyph = 26, size = 26, pal = "lime"})
	w2.setWord({"NEED MORE $!", "NEED $!"}, "red")
	check("MUST 5: NEED $! on a 112 button", w2.face.Word.Text == "NEED $!" and w2.pal == "red", w2.face.Word.Text)
	local pb = H.priceButton(hold, "P", 238, 384, 492, 60, {d = 4, r = 12, glyph = 34, size = 32, pre = "BUY"})
	pb.setPrice("49")
	x0, x1 = group(pb)
	check("popup BUY group centred", pb.face.Pre.Text == "BUY" and near((x0 + x1) / 2, 246, 1), ("%.1f..%.1f"):format(x0, x1))
	hold:Destroy()
end)
-- 6 pulse amplitude / period (SHOULD 11)
try("pulse", function()
	local hold = Instance.new("Frame")
	local a = H.glossButton(hold, "A", 0, 0, 100, 40, "gold", {})
	a.pulse(0.6)
	check("default pulse(0.6) = 1.05", near(a.scale.Scale, 1.05, 1e-6), a.scale.Scale)
	local b = H.glossButton(hold, "B", 0, 0, 100, 40, "gold", {pulseAmp = 0.01, pulsePeriod = 1.6})
	b.pulse(0.8)
	check("pulseAmp 0.01 period 1.6: pulse(0.8) = 1.02", near(b.scale.Scale, 1.02, 1e-6), b.scale.Scale)
	hold:Destroy()
end)
-- 7 MUST 6: transient buttons leave H.buttons when destroyed
try("transient", function()
	local hold = Instance.new("Frame")
	local n0 = #H.buttons
	for i = 1, 5 do H.priceButton(hold, "R" .. i, 0, 0, 134, 40, {glyph = 24, size = 22, transient = true}) end
	check("transient registered", #H.buttons == n0 + 5, #H.buttons - n0)
	hold:Destroy()
	task.wait()
	check("transient removed on destroy", #H.buttons == n0, #H.buttons - n0)
end)
-- 8 windowChrome opts.bats = false, shellCard noHit / grad / noHover, arrow, sectionHeader
try("chrome/card/arrow/header", function()
	local w = Instance.new("Frame")
	w.Size = UDim2.fromOffset(740, 470)
	local ch = H.windowChrome(w, {bats = false})
	check("windowChrome bats=false: no Bats", ch.front:FindFirstChild("Bats") == nil and ch.bats == nil)
	ch.setTheme("Shop")
	check("setTheme Shop tooth", ch.front.Crack.Tooth1.BackgroundColor3 == Color3.fromRGB(220, 0, 100))
	local card = H.shellCard(w, "Card", 0, 0, 576, 128, {noHit = true, noHover = true, grad = {Color3.fromRGB(110, 36, 150), Color3.fromRGB(60, 22, 104)}})
	check("shellCard noHit", card.holder:FindFirstChild("Hit") == nil and card.hit == nil)
	local g = card.face:FindFirstChildOfClass("UIGradient")
	check("shellCard grad", g and g.Color.Keypoints[1].Value == Color3.fromRGB(110, 36, 150))
	local def = H.shellCard(w, "Def", 0, 0, 158, 166)
	check("shellCard default keeps Hit", def.holder:FindFirstChild("Hit") ~= nil and def.hit ~= nil)
	local ar = H.arrow(w, "Arrow", 142, 49, 3)
	check("arrow 18 x 22, 4 segments", ar.Size == UDim2.fromOffset(18, 22) and #ar:GetChildren() == 4)
	local hd = H.sectionHeader(w, "Header_SPEED", 4, 4, 576, "SPEED", "rbxassetid://80829076123513", Color3.fromRGB(90, 220, 255))
	local tw = H.textWidth("SPEED", 20)
	check("sectionHeader line", hd.Size == UDim2.fromOffset(576, 30) and near(hd.Line.Position.X.Offset, 34 + tw + 12, 0.01) and near(hd.Line.Position.X.Offset + hd.Line.Size.X.Offset, 576, 0.01),
		tostring(hd.Line.Position))
	w:Destroy()
end)
-- 9 (popup/Shop fix round) HatchFill / HatchHug (visual review MUST 1: the 83 % rule), chrome.setHeight (SHOULD 3)
try("fix round", function()
	local lab = Instance.new("TextLabel")
	lab.Size = UDim2.fromOffset(100, 22)
	lab:SetAttribute("HatchBase", 20)
	lab:SetAttribute("HatchMin", 12)
	lab:SetAttribute("HatchFill", 0.83)
	local txt = "MMMMMM"
	local w20 = H.textWidth(txt, 20)
	H.fit(lab, txt)
	local w = H.textWidth(lab.Text, lab.TextSize)
	check("HatchFill 0.83: fitted text <= 83 % of the box", w <= 83 + 0.5, ("w20 %.1f -> size %d w %.1f"):format(w20, lab.TextSize, w))
	lab:Destroy()
	local hold = Instance.new("Frame")
	local b = H.priceButton(hold, "B", 0, 0, 160, 54, {d = 4, r = 12, glyph = 30, size = 28, pre = "BUY"})
	check("priceButton: Word HatchFill 0.83, Price + Pre HatchHug", b.face.Word:GetAttribute("HatchFill") == 0.83 and b.face.Price:GetAttribute("HatchHug") == true and b.face.Pre:GetAttribute("HatchHug") == true)
	local hd = H.sectionHeader(hold, "Header_X", 4, 4, 576, "SPEED", "rbxassetid://80829076123513", Color3.fromRGB(90, 220, 255))
	check("sectionHeader Title HatchHug", hd.Title:GetAttribute("HatchHug") == true)
	local w2 = H.priceButton(hold, "W2", 0, 0, 112, 54, {d = 4, r = 12, glyph = 26, size = 26, pal = "lime"})
	w2.setWord({"NEED MORE $!", "NEED $!"}, "red")
	local word = w2.face.Word
	local st = word:FindFirstChildOfClass("UIStroke")
	local fill = H.textWidth(word.Text, word.TextSize) / (word.Size.X.Offset - 2 * (st and st.Thickness or 0))
	check("112 button: the refusal word fills <= 83 %", fill <= 0.835, ("%s %.0f%%"):format(word.Text, fill * 100))
	hold:Destroy()
	local wf = Instance.new("Frame")
	wf.Size = UDim2.fromOffset(740, 470)
	local ch = H.windowChrome(wf, {bats = false})
	check("chrome.setHeight exists", type(ch.setHeight) == "function")
	ch.setHeight(374)
	check("setHeight(374): back / front / crack 374", ch.back.Size.Y.Offset == 374 and ch.front.Size.Y.Offset == 374 and ch.front.Crack.Size.Y.Offset == 374,
		ch.back.Size.Y.Offset .. " " .. ch.front.Size.Y.Offset .. " " .. ch.front.Crack.Size.Y.Offset)
	ch.setHeight()
	check("setHeight(): back to H.H " .. tostring(H.H), ch.back.Size.Y.Offset == H.H and ch.front.Crack.Size.Y.Offset == H.H, ch.back.Size.Y.Offset)
	wf:Destroy()
end)
-- 10 (fix round, perf review item 7) BrickUI viewport helpers (a clone: the Edit datamodel is not a running client)
try("BrickUI viewport", function()
	local bsrc = game.ReplicatedStorage.BrickUI
	local bc = bsrc:Clone()
	bc.Parent = bsrc.Parent
	local okB, Bm = pcall(require, bc)
	bc:Destroy()
	check("BrickUI requires", okB, not okB and Bm or nil)
	if okB then
		check("BrickUI.viewportSize / waitViewport / trackStroke / onViewport", type(Bm.viewportSize) == "function" and type(Bm.waitViewport) == "function" and type(Bm.trackStroke) == "function" and type(Bm.onViewport) == "function")
		local ds = Bm.deviceScale()
		check("deviceScale in 0.52..1.18, never the 1x1 0.52 lock on a real viewport", ds >= 0.52 and ds <= 1.18, ds)
		local s = Instance.new("UIStroke")
		Bm.trackStroke(s, 3.5)
		check("trackStroke sets px x deviceScale", math.abs(s.Thickness - 3.5 * ds) < 1e-6, s.Thickness)
		s:Destroy()
	end
end)

---------------------------------------------------------------- RIS plan 8.1 (2026-10-21, Rebirth / Index / Settings) + review MUST 1, SHOULD 3
-- R1-R10. Each block in a pcall (a missing helper is a FAIL line). The pre-RIS Hatch (ServerStorage backup) is the
-- reference for the arrow's default path (k = nil must be byte-identical in output).
local preH
do
	local bk = game.ServerStorage:FindFirstChild("_Backup_HatchNight")
	local pre = bk and bk:FindFirstChild("Before") and bk.Before:FindFirstChild("BrickUI_preRIS")
	local ph = pre and pre:FindFirstChild("Hatch")
	if ph then
		local pc = ph:Clone()
		pc.Parent = ph.Parent
		local okP, mod = pcall(require, pc)
		pc:Destroy()
		if okP then preH = mod end
	end
end
-- R1 bands
try("R1 bands", function()
	for name, tooth in {Rebirth = Color3.fromRGB(112, 0, 214), Index = Color3.fromRGB(0, 120, 235), Settings = Color3.fromRGB(104, 96, 176)} do
		local b = H.BAND[name]
		check("R1 BAND." .. name, b ~= nil and b.band ~= nil and b.fill ~= nil and b.tooth == tooth, b and tostring(b.tooth))
	end
end)
-- R2 bandTheme
try("R2 bandTheme", function()
	local was = workspace:GetAttribute("HatchBand")
	workspace:SetAttribute("HatchBand", nil)
	for _, p in {"Rebirth", "Index", "Settings"} do check("R2 bandTheme " .. p, H.bandTheme(p) == p, H.bandTheme(p)) end
	check("R2 bandTheme Gift == bandTheme()", H.bandTheme("Gift") == H.bandTheme())
	workspace:SetAttribute("HatchBand", "HatchGold")
	check("R2 HatchBand override wins on all 3", H.bandTheme("Rebirth") == "HatchGold" and H.bandTheme("Index") == "HatchGold" and H.bandTheme("Settings") == "HatchGold")
	workspace:SetAttribute("HatchBand", was)
end)
-- R3 pageCap (R = the Task 0 measures 0.6315 / 0.7069 / 0.6315)
try("R3 pageCap", function()
	check("R3 PAGE_CAP_R", type(H.PAGE_CAP_R) == "table" and near(H.PAGE_CAP_R.Rebirth or 0, 0.6315, 1e-6) and near(H.PAGE_CAP_R.Index or 0, 0.7069, 1e-6)
		and near(H.PAGE_CAP_R.Settings or 0, 0.6315, 1e-6) and H.PAGE_CAP_R.Shop == H.SHOP_CAP_R)
	check("R3 pageCap Rebirth 1022 = 1.3732", near(H.pageCap("Rebirth", 1022) or 0, 1.3732, 0.001), H.pageCap("Rebirth", 1022))
	check("R3 pageCap Index 1022 = 1.5371", near(H.pageCap("Index", 1022) or 0, 1.5371, 0.001), H.pageCap("Index", 1022))
	check("R3 pageCap Settings 1022 = 1.3732", near(H.pageCap("Settings", 1022) or 0, 1.3732, 0.001), H.pageCap("Settings", 1022))
	for _, p in {"Rebirth", "Index", "Settings"} do check("R3 pageCap " .. p .. " 562 = 1.18", H.pageCap(p, 562) == 1.18, H.pageCap(p, 562)) end
	check("R3 pageCap Shop 1022 unchanged 1.7718", near(H.pageCap("Shop", 1022), 1.7718, 0.0005), H.pageCap("Shop", 1022))
	check("R3 pageCap Gift = nil", H.pageCap("Gift", 1022) == nil)
end)
-- R4 fitWindow rows (plan section 3)
try("R4 fitWindow", function()
	local function row(label, args, e)
		local s, w, h, cx, cy = H.fitWindow(table.unpack(args))
		check("R4 " .. label, near(s, e[1], 0.0006) and near(w, e[2], 0.5) and near(h, e[3], 0.5) and near(cx, e[4], 0.5) and near(cy, e[5], 0.5),
			("%.4f %.1f %.1f %.2f %.1f"):format(s, w, h, cx, cy))
	end
	row("Rebirth 1920", {1920, 1022, 412.1, H.pageCap("Rebirth", 1022)}, {1.3732, 1016.2, 645.4, 960, 511})
	row("Settings 1920", {1920, 1022, 412.1, H.pageCap("Settings", 1022)}, {1.3732, 1016.2, 645.4, 960, 511})
	row("Index 1920", {1920, 1022, 412.1, H.pageCap("Index", 1022)}, {1.5371, 1137.5, 722.4, 980.85, 511})
	for _, p in {"Rebirth", "Index", "Settings"} do
		row(p .. " 1050", {1050, 562, 229.3, H.pageCap(p, 562)}, {1.0982, 812.7, 516.2, 635.65, 281})
		row(p .. " 844", {732, 346, 144.3, H.pageCap(p, 346)}, {0.7106, 525.9, 334.0, 407.24, 173})
	end
end)
-- R5 arrow: k = nil is the old arrow exactly; k = 0.75 scales the box
try("R5 arrow", function()
	local f = Instance.new("Frame")
	local a = H.arrow(f, "A", 0, 0)
	check("R5 arrow default 18 x 22", a.Size == UDim2.fromOffset(18, 22), tostring(a.Size))
	if preH then
		local g = Instance.new("Frame")
		local o = preH.arrow(g, "A", 0, 0)
		local same = #a:GetChildren() == #o:GetChildren()
		for _, c in o:GetChildren() do
			local n = a:FindFirstChild(c.Name)
			if not (n and n.Position == c.Position and n.Size == c.Size and n.Rotation == c.Rotation and n.BackgroundColor3 == c.BackgroundColor3 and n.ZIndex == c.ZIndex) then same = false end
		end
		check("R5 arrow default = the pre-RIS arrow (every segment)", same)
		g:Destroy()
	else
		check("R5 pre-RIS Hatch backup found", false, "ServerStorage._Backup_HatchNight.Before.BrickUI_preRIS.Hatch")
	end
	local b = H.arrow(f, "B", 0, 0, 3, 0.75)
	check("R5 arrow k 0.75 = 13.5 x 16.5", b.Size == UDim2.fromOffset(13.5, 16.5) and b.ZIndex == 3, tostring(b.Size))
	local ink = b:FindFirstChild("Ink1")
	-- (UDim offsets are integers: 7 x 0.75 = 5.25 is stored as UDim2.fromOffset gives it)
	check("R5 arrow k 0.75 Ink1 thickness 7 x 0.75", ink and ink.Size.Y.Offset == UDim2.fromOffset(0, 5.25).Y.Offset and ink.Size.Y.Offset < 7, ink and ink.Size.Y.Offset)
	f:Destroy()
end)
-- R6 nowNext (+ review MUST 1: HatchHug on Now / Next; SHOULD 3: opts.arrow = false)
try("R6 nowNext", function()
	local f = Instance.new("Frame")
	local nn = H.nowNext(f, "Head", 148, 80, 560, 28, {align = "left"})
	nn.set("REBIRTH 0", "1")
	local fr = f:FindFirstChild("Head")
	local now, ar, nx = fr and fr:FindFirstChild("Now"), fr and fr:FindFirstChild("Arrow"), fr and fr:FindFirstChild("Next")
	local tw1 = H.textWidth("REBIRTH 0", 28)
	local x0 = now and now.Position.X.Offset or 0
	check("R6 Now box = tw + 8", now and near(now.Size.X.Offset, tw1 + 8, 0.01), now and now.Size.X.Offset)
	check("R6 Arrow at x0 + tw1 + 10 (k 1 at size 28)", ar and near(ar.Position.X.Offset - x0, tw1 + 10, 0.01) and ar.Size == UDim2.fromOffset(18, 22), ar and ar.Position.X.Offset - x0)
	check("R6 Next at x0 + tw1 + 14 + 18", nx and near(nx.Position.X.Offset - x0, tw1 + 32, 0.01) and nx.Visible and ar.Visible, nx and nx.Position.X.Offset - x0)
	check("R6 left: Now glyphs start at the row's x (148)", fr and near(fr.Position.X.Offset + x0, 148, 0.01), fr and fr.Position.X.Offset + x0)
	check("R6 Arrow centre y = Now centre y +-1", now and ar and math.abs((ar.Position.Y.Offset + ar.Size.Y.Offset / 2) - (now.Position.Y.Offset + now.Size.Y.Offset / 2)) <= 1)
	check("R6 MUST 1: HatchHug on Now + Next", now and nx and now:GetAttribute("HatchHug") == true and nx:GetAttribute("HatchHug") == true)
	check("R6 HatchTile nn on the 3 parts", now and ar and nx and now:GetAttribute("HatchTile") == "nn" and ar:GetAttribute("HatchTile") == "nn" and nx:GetAttribute("HatchTile") == "nn")
	check("R6 Next colour LIME_TXT", nx and nx.TextColor3 == H.LIME_TXT)
	-- centred, w 158, size 16 (k 0.75): the visible group (Now glyphs .. Next box) centred on 79 +-1
	local c = H.nowNext(f, "Line", 8, 90, 158, 16)
	c.set("x1", "x1.25")
	local lf = f:FindFirstChild("Line")
	local n2, x2 = lf.Now, lf.Next
	local left = lf.Position.X.Offset + n2.Position.X.Offset
	local right = lf.Position.X.Offset + x2.Position.X.Offset + x2.Size.X.Offset
	local mid = (left + right) / 2 - 8 -- (in the 158-wide row at x 8)
	check("R6 centred group centre 79 +-1", near(mid, 79, 1), mid)
	check("R6 centred k 0.75 arrow", lf.Arrow.Size == UDim2.fromOffset(13.5, 16.5), tostring(lf.Arrow.Size))
	c.set("MAX", nil)
	check("R6 set(MAX, nil): Arrow + Next hidden", lf.Arrow.Visible == false and lf.Next.Visible == false and lf.Now.Text == "MAX")
	c.set("MAX REBIRTH", "20", {arrow = false, c2 = H.GOLD_TXT})
	check("R6 SHOULD 3 arrow = false: no chevron, Next shown gold", lf.Arrow.Visible == false and lf.Next.Visible and lf.Next.Text == "20" and lf.Next.TextColor3 == H.GOLD_TXT)
	-- too long for the row: steps down (never below 16)
	local d = H.nowNext(f, "Tight", 0, 0, 120, 22)
	d.set("x1.25", "x1.5625")
	check("R6 steps down to fit (>= 16)", f.Tight.Now.TextSize < 22 and f.Tight.Now.TextSize >= 16, f.Tight.Now.TextSize)
	f:Destroy()
end)
-- R7 progressBar
try("R7 progressBar", function()
	local f = Instance.new("Frame")
	local bar = H.progressBar(f, "VolBar", 476, 15, 180, 36, {size = 18})
	local fr = f:FindFirstChild("VolBar")
	local fill, text = fr and fr:FindFirstChild("Fill"), fr and fr:FindFirstChild("Text")
	bar.set(0, "0%")
	check("R7 set(0): Fill hidden, text 0%", fill and fill.Visible == false and text and text.Text == "0%")
	bar.set(0.5, "50%")
	check("R7 set(0.5): Fill width (w - 6) x 0.5", fill and fill.Visible and near(fill.Size.X.Offset, 87, 0.01) and fill.Position == UDim2.fromOffset(3, 3) and near(fill.Size.Y.Offset, 30, 0.01), fill and fill.Size.X.Offset)
	bar.set(0.01, "1%")
	check("R7 set(0.01): width = h - 6", fill and near(fill.Size.X.Offset, 30, 0.01), fill and fill.Size.X.Offset)
	bar.set(2, "200%")
	check("R7 set(2): width = w - 6", fill and near(fill.Size.X.Offset, 174, 0.01), fill and fill.Size.X.Offset)
	check("R7 Text = the given text, size 18, HatchFill 0.83", text and text.Text == "200%" and text.TextSize == 18 and text:GetAttribute("HatchFill") == 0.83)
	local c = fr and fr:FindFirstChildOfClass("UICorner")
	check("R7 trough corner h / 2", c and c.CornerRadius == UDim.new(0, 18))
	-- (run A, found by containment SET1) the gloss strip's rounded ends stay inside the fill pill at its smallest (h - 6)
	-- and full (w - 6) width: each end's arc centre within (rf - rg) of the pill's end-circle centre
	local gl = fill and fill:FindFirstChild("Gloss")
	local gc = gl and gl:FindFirstChildOfClass("UICorner")
	local okG, why = gl ~= nil and gc ~= nil and gc.CornerRadius.Scale == 0.5, "no round Gloss"
	if okG then
		local a, b, gh = gl.Position.X.Offset, gl.Position.Y.Offset, gl.Size.Y.Offset
		local rf, rg = 15, gh / 2
		for _, wf in {30, 174} do
			local gw = wf + gl.Size.X.Offset -- (Size X = (1, -2a))
			local dl = math.sqrt((a + rg - rf) ^ 2 + (b + rg - rf) ^ 2)
			local dr = math.sqrt((a + gw - rg - (wf - rf)) ^ 2 + (b + rg - rf) ^ 2)
			if gl.Size.X.Scale ~= 1 or gw < gh or dl > rf - rg + 0.01 or dr > rf - rg + 0.01 then
				okG = false
				why = ("fill %d: gloss %d wide, ends %.2f / %.2f from the pill centres (limit %.2f)"):format(wf, gw, dl, dr, rf - rg)
			end
		end
	end
	check("R7 gloss strip inside the fill pill (min + full width)", okG, not okG and why or nil)
	f:Destroy()
end)
-- R8 the canvas guard (perf review I-4): a hidden canvas keeps its scale; shown -> ref / 740
try("R8 canvas guard", function()
	local sg = Instance.new("ScreenGui")
	sg.Name = "HatchPureR8"
	local ref = Instance.new("Frame")
	ref.Size = UDim2.fromOffset(740, 470)
	ref.Parent = sg
	local canvas = Instance.new("Frame")
	canvas.Visible = false
	canvas.Parent = ref
	local ok = pcall(function() sg.Parent = game:GetService("CoreGui") end)
	if not ok then sg.Parent = game:GetService("StarterGui") end
	local sc = H.bindCanvasScale(canvas, ref, 740)
	task.wait()
	local before = sc.Scale
	ref.Size = UDim2.fromOffset(1110, 705)
	task.wait() task.wait()
	check("R8 hidden: CanvasScale unchanged", sc.Scale == before, sc.Scale)
	canvas.Visible = true
	task.wait() task.wait()
	check("R8 shown: CanvasScale = ref / 740", near(sc.Scale, ref.AbsoluteSize.X / 740, 0.001) and ref.AbsoluteSize.X > 0, ("%.3f vs %.3f"):format(sc.Scale, ref.AbsoluteSize.X / 740))
	sg:Destroy()
end)
-- R9 (review MUST 1) H.text opts.fill: HatchFill is set before the first fit
try("R9 text fill", function()
	local f = Instance.new("Frame")
	local t = H.text(f, "T", {"WWWWWWWW", "W"}, 0, 0, 100, 20, {fill = 0.83})
	check("R9 fill 0.83 picks the short variant", t.Text == "W" and t:GetAttribute("HatchFill") == 0.83, t.Text)
	local u = H.text(f, "U", "AB", 0, 0, 100, 20)
	check("R9 default path: no HatchFill", u:GetAttribute("HatchFill") == nil)
	-- a line that fits 100 % of the room but not 83 %: steps down (or takes the next variant)
	local s, w = "", 0
	repeat s ..= "M" w = H.textWidth(s, 16) until w > 0.83 * 95
	local v = H.text(f, "V", {s, "OK"}, 0, 0, 100, 16, {fill = 0.83})
	check("R9 fill 0.83 refuses a " .. math.floor(w) .. " px line in 95 px of room", v.Text == "OK", v.Text)
	f:Destroy()
end)
-- R10 (run C, review MUST 3) H.tutorialFit(s, cx, cy, guiH, topClear): the step-11 Rebirth window moves down under the
-- tutorial guide first and shrinks only by what is left. Rows = the review's derivations (gui space: the guide's text
-- bottom + 6): Studio 1519x753 (gui 695, s 1.18, clear 97) = no shrink, centre 347.5 -> 374.3 (+26.8); 1050x620 (gui 562,
-- s 1.0982, clear 75) = s 481 / 470 = 1.0234; 844x390 (gui 346, s 0.7106, clear 26) = s 314 / 470 = 0.6681; no guide
-- (clear 0) = unchanged.
try("R10 tutorialFit", function()
	local function row(name, s0, cx0, cy0, gh, clear, ws, wcy)
		local s, w, h, cx, cy = H.tutorialFit(s0, cx0, cy0, gh, clear)
		check(("R10 %s s %.4f (want %.4f)"):format(name, s, ws), math.abs(s - ws) <= 0.0005, s)
		check(("R10 %s centre y %.2f (want %.2f), cx kept"):format(name, cy, wcy), math.abs(cy - wcy) <= 0.05 and cx == cx0, cy)
		check(("R10 %s top >= clear, bottom <= gui - 6"):format(name), cy - h / 2 >= clear - 0.01 and cy + h / 2 <= gh - 6 + 0.01, ("%.2f..%.2f"):format(cy - h / 2, cy + h / 2))
		check(("R10 %s w, h = 740 s, 470 s"):format(name), math.abs(w - 740 * s) < 1e-6 and math.abs(h - 470 * s) < 1e-6)
	end
	row("studio", 1.18, 759.5, 347.5, 695, 97, 1.18, 97 + 470 * 1.18 / 2)
	row("1050x620", 1.0982, 635.65, 281, 562, 75, 481 / 470, 75 + 481 / 2)
	row("844x390", 0.7106, 407.24, 173, 346, 26, 314 / 470, 26 + 314 / 2)
	local s, w, h, cx, cy = H.tutorialFit(1.18, 759.5, 347.5, 695, 0)
	check("R10 no guide (clear 0): unchanged", s == 1.18 and cy == 347.5 and cx == 759.5, ("%.4f %.2f"):format(s, cy))
end)
---------------------------------------------------------------- UWF plan 8.1 (2026-10-22, Free Gift / Welcome Back / Upgrades)
-- U1-U10. Each block in a pcall. The pre-UWF Hatch (ServerStorage._Backup_HatchNight.Before.BrickUI_preUWF.Hatch) is the
-- A/B reference: every old default path must give the same result.
local preU
do
	local bk = game.ServerStorage:FindFirstChild("_Backup_HatchNight")
	local pre = bk and bk:FindFirstChild("Before") and bk.Before:FindFirstChild("BrickUI_preUWF")
	local ph = pre and pre:FindFirstChild("Hatch")
	if ph then
		local pc = ph:Clone()
		pc.Parent = ph.Parent
		local okP, mod = pcall(require, pc)
		pc:Destroy()
		if okP then preU = mod end
	end
end
check("U0 pre-UWF Hatch backup found", preU ~= nil, "ServerStorage._Backup_HatchNight.Before.BrickUI_preUWF.Hatch")
-- a sorted dump of a GUI subtree (A/B): name, class, geometry, colours, corners, strokes, images, texts, attributes
local function udump(root)
	local out = {}
	local function r2(n) return math.floor(n * 1000 + 0.5) / 1000 end
	local function walk(o, path)
		local kids = o:GetChildren()
		table.sort(kids, function(a, b) if a.Name ~= b.Name then return a.Name < b.Name end return a.ClassName < b.ClassName end)
		for i, c in kids do
			local p = path .. "/" .. c.Name .. "#" .. i
			local parts = {p, c.ClassName}
			if c:IsA("GuiObject") then
				table.insert(parts, tostring(c.Position) .. " " .. tostring(c.Size) .. " z" .. c.ZIndex .. " " .. tostring(c.BackgroundColor3) .. " " .. r2(c.BackgroundTransparency) .. " " .. tostring(c.Visible) .. " " .. tostring(c.AnchorPoint) .. " r" .. r2(c.Rotation))
			end
			if c:IsA("TextLabel") then table.insert(parts, c.Text .. " " .. c.TextSize .. " " .. tostring(c.TextColor3)) end
			if c:IsA("ImageLabel") or c:IsA("ImageButton") then table.insert(parts, c.Image .. " " .. tostring(c.ImageColor3) .. " " .. r2(c.ImageTransparency)) end
			if c:IsA("UICorner") then table.insert(parts, tostring(c.CornerRadius)) end
			if c:IsA("UIStroke") then table.insert(parts, r2(c.Thickness) .. " " .. tostring(c.Color) .. " " .. r2(c.Transparency)) end
			if c:IsA("UIGradient") then table.insert(parts, tostring(c.Color) .. " " .. r2(c.Rotation)) end
			if c:IsA("UIScale") then table.insert(parts, tostring(r2(c.Scale))) end
			local at = {}
			for k, v in c:GetAttributes() do table.insert(at, "@" .. k .. "=" .. tostring(v)) end
			table.sort(at)
			table.insert(parts, table.concat(at, " "))
			table.insert(out, table.concat(parts, " | "))
			walk(c, p)
		end
	end
	walk(root, "")
	return out
end
local function firstDiff(a, b)
	for i = 1, math.max(#a, #b) do if a[i] ~= b[i] then return i .. ": " .. tostring(a[i]) .. " <> " .. tostring(b[i]) end end
	return nil
end
-- U1 headerTeeth
try("U1 headerTeeth", function()
	local t740 = H.headerTeeth(740)
	local same = #t740 == #H.HEADER_TEETH
	for i, t in H.HEADER_TEETH do if not (t740[i] and t740[i][1] == t[1] and t740[i][2] == t[2]) then same = false end end
	check("U1 headerTeeth(740) == HEADER_TEETH exactly (37)", same and #t740 == 37, #t740)
	local t560 = H.headerTeeth(560)
	check("U1 headerTeeth(560): 28 teeth, 16 .. 544", #t560 == 28 and near(t560[1][1], 16, 1e-9) and near(t560[28][1], 544, 1e-9), #t560 .. " " .. tostring(t560[#t560] and t560[#t560][1]))
	local t540 = H.headerTeeth(540)
	check("U1 headerTeeth(540): 27 teeth, last 524", #t540 == 27 and near(t540[27][1], 524, 1e-9), #t540 .. " " .. tostring(t540[#t540] and t540[#t540][1]))
end)
-- U2 chrome A/B (bats = false and the default), the pre-UWF H vs the new H
try("U2 chrome A/B", function()
	if not preU then check("U2 needs the pre-UWF H", false) return end
	for _, o in {{bats = false}, false} do
		local fa, fb = Instance.new("Frame"), Instance.new("Frame")
		fa.Size, fb.Size = UDim2.fromOffset(740, 470), UDim2.fromOffset(740, 470)
		H.windowChrome(fa, o and table.clone(o) or nil)
		preU.windowChrome(fb, o and table.clone(o) or nil)
		local a, b = udump(fa), udump(fb)
		local d = firstDiff(a, b)
		check("U2 windowChrome(" .. (o and "{bats = false}" or "") .. ") identical to pre-UWF (" .. #a .. " lines)", d == nil, d)
		fa:Destroy() fb:Destroy()
	end
end)
-- U3 chrome 560 x 460
try("U3 chrome 560x460", function()
	local f = Instance.new("Frame")
	f.Size = UDim2.fromOffset(661, 543)
	local ch = H.windowChrome(f, {bats = false, w = 560, h = 460})
	local back, front = ch.back, ch.front
	check("U3 HatchBack / HatchFront 560 x 460", back.Size == UDim2.fromOffset(560, 460) and front.Size == UDim2.fromOffset(560, 460), tostring(back.Size))
	check("U3 Face 560 x 453, Rim 557 x 450", back.Face.Size == UDim2.fromOffset(560, 453) and back.Face.Rim.Size == UDim2.fromOffset(557, 450), tostring(back.Face.Size) .. " " .. tostring(back.Face.Rim.Size))
	local close = front:FindFirstChild("Close")
	check("U3 Close holder centre (531, 23)", close and close.Position == UDim2.fromOffset(531, 23), close and tostring(close.Position))
	check("U3 CloseHit centre (532, 28)", front.CloseHit.Position == UDim2.fromOffset(532, 28), tostring(front.CloseHit.Position))
	local okT, n, lo, hi = true, 0, 1e9, -1e9
	for _, d in front.Crack:GetDescendants() do
		if d:IsA("GuiObject") and d.Rotation ~= 0 then
			n += 1
			local c = d.Position.X.Offset + d.Size.X.Offset * (0.5 - d.AnchorPoint.X)
			lo, hi = math.min(lo, c), math.max(hi, c)
			if c < 16 - 0.6 or c > 544 + 0.6 then okT = false end
		end
	end
	check("U3 every tooth centre in [16, 544] (" .. n .. " teeth)", okT and n >= 28, ("%d %.1f..%.1f"):format(n, lo, hi))
	check("U3 Title Size.X 400", ch.title.Size.X.Offset == 400, ch.title.Size.X.Offset)
	check("U3 Bats absent (bats = false)", front:FindFirstChild("Bats") == nil)
	f:Destroy()
end)
-- U4 fitWindow rows (lw / lh)
try("U4 fitWindow lw/lh", function()
	local s, w, h = H.fitWindow(1920, 1022, 412.1, 1.18, 560, 460)
	check("U4 FG 1080p 1.18 660.8 x 542.8", near(s, 1.18, 0.001) and near(w, 660.8, 0.5) and near(h, 542.8, 0.5), ("%.4f %.1f %.1f"):format(s, w, h))
	s = H.fitWindow(732 - 57.3 + 8, 346, 144.3, 1.18, 560, 460)
	check("U4 FG phone 0.7261", near(s, 0.7261, 0.001), s)
	s = H.fitWindow(732 - 57.3 + 8, 346, 144.3, 1.18, 540, 430)
	check("U4 WB phone 0.7767", near(s, 0.7767, 0.001), s)
	s = H.fitWindow(1050 - 72.3 + 8, 562, 229.3, H.pageCap("Upgrades", 562), 740, 470)
	check("U4 UP 1050x620 1.0114", near(s, 1.0114, 0.001), s)
end)
-- U5 fitWindow A/B (no lw / lh = the pre-UWF results)
try("U5 fitWindow A/B", function()
	if not preU then check("U5 needs the pre-UWF H", false) return end
	local rows = {{1920, 1022, 412.1}, {1050, 562, 229.3}, {732, 346, 144.3}, {667, 331, 137.9}, {1920, 1022, 0}, {1050, 562, 0}, {732, 346, 0, 1.18}, {1920, 1022, 412.1, 1.4608}}
	local okAll, bad = true, nil
	for _, r in rows do
		local a = {H.fitWindow(r[1], r[2], r[3], r[4])}
		local b = {preU.fitWindow(r[1], r[2], r[3], r[4])}
		for i = 1, 5 do if a[i] ~= b[i] then okAll = false bad = r[1] .. "x" .. r[2] .. " #" .. i end end
	end
	check("U5 fitWindow 8 rows identical to pre-UWF", okAll, bad)
end)
-- U6 pageCap
try("U6 pageCap", function()
	check("U6 PAGE_CAP_R.Upgrades 0.6717", H.PAGE_CAP_R.Upgrades == 0.6717, H.PAGE_CAP_R.Upgrades)
	check("U6 pageCap Upgrades 1022 = R_U x 1022 / 470 (1.4606)", near(H.pageCap("Upgrades", 1022), 0.6717 * 1022 / 470, 1e-9) and near(H.pageCap("Upgrades", 1022), 1.4606, 0.0005), H.pageCap("Upgrades", 1022))
	check("U6 pageCap Upgrades 695 = 1.18", H.pageCap("Upgrades", 695) == 1.18, H.pageCap("Upgrades", 695))
	if preU then
		local same = true
		for _, p in {"Shop", "Rebirth", "Index", "Settings", "Gift"} do
			for _, g in {346, 562, 695, 1022} do if H.pageCap(p, g) ~= preU.pageCap(p, g) then same = false end end
		end
		check("U6 pageCap Shop / Rebirth / Index / Settings / Gift unchanged", same)
	end
end)
-- U7 tutorialFit lw / lh
try("U7 tutorialFit lw/lh", function()
	local s, w, h, cx, cy = H.tutorialFit(1.18, 759.5, 347.5, 695, 148.6, 740, 470)
	check("U7 studio guide: s 1.1498, cy 418.8", near(s, 1.1498, 0.0005) and near(cy, 418.8, 0.05), ("%.4f %.2f"):format(s, cy))
	s = H.tutorialFit(0.7106, 407.24, 173, 346, 67.5)
	check("U7 phone guide: s 0.5798", near(s, 0.5798, 0.0005), s)
	s, w, h = H.tutorialFit(1.18, 559.7, 281, 562, 126.4, 560, 460)
	check("U7 lw 560 / lh 460: w, h = 560 s, 460 s", near(w, 560 * s, 1e-6) and near(h, 460 * s, 1e-6), ("%.4f"):format(s))
	if preU then
		local same = true
		for _, r in {{1.18, 759.5, 347.5, 695, 97}, {1.0982, 635.65, 281, 562, 75}, {0.7106, 407.24, 173, 346, 26}, {1.18, 759.5, 347.5, 695, 0}} do
			local a, b = {H.tutorialFit(table.unpack(r))}, {preU.tutorialFit(table.unpack(r))}
			for i = 1, 5 do if a[i] ~= b[i] then same = false end end
		end
		check("U7 no lw / lh = the pre-UWF results (4 rows)", same)
	end
end)
-- U8 priceButton: default A/B, top, glyphImage, setGlyph
try("U8 priceButton", function()
	if preU then
		local fa, fb = Instance.new("Frame"), Instance.new("Frame")
		local a = H.priceButton(fa, "P", 0, 0, 200, 60, {d = 4, size = 22})
		local b = preU.priceButton(fb, "P", 0, 0, 200, 60, {d = 4, size = 22})
		a.setPrice("49") b.setPrice("49")
		local d1 = firstDiff(udump(fa), udump(fb))
		a.setWord("OWNED", "silver") b.setWord("OWNED", "silver")
		local d2 = firstDiff(udump(fa), udump(fb))
		check("U8 default priceButton identical after setPrice / setWord", d1 == nil and d2 == nil, d1 or d2)
		local pa = H.priceButton(fa, "Q", 0, 0, 156, 60, {d = 4, size = 22, pre = "BUY"})
		local pb = preU.priceButton(fb, "Q", 0, 0, 156, 60, {d = 4, size = 22, pre = "BUY"})
		pa.setPrice("1,499") pb.setPrice("1,499")
		local d3 = firstDiff(udump(fa), udump(fb))
		check("U8 pre = BUY identical", d3 == nil, d3)
		fa:Destroy() fb:Destroy()
	end
	local f = Instance.new("Frame")
	local t = H.priceButton(f, "T", 0, 0, 118, 60, {d = 4, size = 22, top = "+1 LV", topSize = 16})
	t.setPrice("29")
	local top = t.face:FindFirstChild("Top")
	check("U8 top: Top visible at y 5", top ~= nil and top.Visible and top.Position.Y.Offset == 5, top and top.Position.Y.Offset)
	check("U8 top: Top HatchFill 0.83", top ~= nil and top:GetAttribute("HatchFill") == 0.83)
	local gy = t.robux.Position.Y.Offset
	check("U8 top: group centre y = 23 + (56 - 23) / 2 +-1", math.abs(gy - (23 + (56 - 23) / 2)) <= 1, gy)
	t.setWord("MAX", "silver")
	check("U8 top: setWord hides Top", top ~= nil and not top.Visible)
	t.setPrice("29")
	check("U8 top: setPrice shows Top again", top ~= nil and top.Visible)
	local g = H.priceButton(f, "G", 0, 0, 156, 60, {d = 4, size = 22, glyphImage = H.ICON.cash})
	g.setPrice("$1.5K")
	check("U8 glyphImage = cash", g.robux.Image == H.ICON.cash, g.robux.Image)
	g.setGlyph(H.ICON.lock)
	g.setPrice("REBIRTH 13")
	local px, pw = g.priceLabel.Position.X.Offset, g.priceLabel.Size.X.Offset
	local gl = g.robux.Position.X.Offset - 11
	check("U8 setGlyph(lock): Robux.Image = lock", g.robux.Image == H.ICON.lock, g.robux.Image)
	check("U8 setGlyph + REBIRTH 13: group inside w - 16", gl >= 8 - 0.5 and px + pw - 6 <= 156 - 8 + 0.5, gl .. " .. " .. (px + pw - 6))
	f:Destroy()
end)
-- U9 bands
try("U9 bands", function()
	check("U9 BAND.FreeGift.tooth (0,160,90)", H.BAND.FreeGift ~= nil and H.BAND.FreeGift.tooth == Color3.fromRGB(0, 160, 90))
	check("U9 BAND.Upgrades.tooth (30,60,220)", H.BAND.Upgrades ~= nil and H.BAND.Upgrades.tooth == Color3.fromRGB(30, 60, 220))
	local was = workspace:GetAttribute("HatchBand")
	workspace:SetAttribute("HatchBand", nil)
	check("U9 bandTheme FreeGift / Upgrades / WelcomeBack", H.bandTheme("FreeGift") == "FreeGift" and H.bandTheme("Upgrades") == "Upgrades" and H.bandTheme("WelcomeBack") == "HatchGold",
		tostring(H.bandTheme("FreeGift")) .. " " .. tostring(H.bandTheme("Upgrades")) .. " " .. tostring(H.bandTheme("WelcomeBack")))
	workspace:SetAttribute("HatchBand", "Pumpkin")
	check("U9 HatchBand Pumpkin overrides all three", H.bandTheme("FreeGift") == "Pumpkin" and H.bandTheme("Upgrades") == "Pumpkin" and H.bandTheme("WelcomeBack") == "Pumpkin")
	workspace:SetAttribute("HatchBand", was)
	check("U9 HatchBand restored", workspace:GetAttribute("HatchBand") == was)
end)
-- U10 helpers exist (values: Play, the client suites' fit / hotbar sections)
try("U10 helpers", function()
	check("U10 H.hudClear / H.guideClear / H.fitStandalone / H.bindHotbar are functions",
		type(H.hudClear) == "function" and type(H.guideClear) == "function" and type(H.fitStandalone) == "function" and type(H.bindHotbar) == "function")
end)
return ("pass %d fail %d\n%s"):format(pass, fail, table.concat(lines, "\n"))
