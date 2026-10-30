local plr = game.Players.LocalPlayer
local pg = plr.PlayerGui
local mm = pg.MainMenu
local PotionConfig = require(game.ReplicatedStorage.PotionConfig)
local C = Color3.fromRGB
local OUT = C(24, 30, 34)
local PANEL = C(26, 44, 52)
local HIGH = C(75, 125, 145)
local WHITE = Color3.new(1, 1, 1)
local DAMIER = "rbxassetid://385956923"
local RAINBOW = ColorSequence.new{
	ColorSequenceKeypoint.new(0.00, C(255, 30, 80)), ColorSequenceKeypoint.new(0.18, C(255, 140, 0)),
	ColorSequenceKeypoint.new(0.35, C(255, 230, 0)), ColorSequenceKeypoint.new(0.52, C(40, 230, 50)),
	ColorSequenceKeypoint.new(0.70, C(0, 210, 255)), ColorSequenceKeypoint.new(0.85, C(90, 60, 255)),
	ColorSequenceKeypoint.new(1.00, C(220, 0, 230)),
}
local win = mm.Window
local face = win.Face
win.AnchorPoint = Vector2.new(0.5, 0.5) win.Position = UDim2.fromScale(0.5, 0.5)
win.UIAspectRatioConstraint.AspectRatio = 1.575 win.Size = UDim2.fromScale(0.64, 0.82)
face.Size = UDim2.fromScale(1, 0.993)
win.Depth.Size = face.Size win.Depth.Position = face.Position + UDim2.fromOffset(0, 4)
face.Body.Visible = false
face.Header.Size = UDim2.fromScale(1, 0.15)
local function place(o, x, y, w, h) o.AnchorPoint = Vector2.new(0.5, 0.5) o.Position = UDim2.fromScale(x, y) o.Size = UDim2.fromScale(w, h) end
place(face.Icon, 0.065, 0.07, 0.075, 0.14) place(face.Title, 0.5, 0.075, 0.6, 0.105) place(face.Close, 0.955, 0.075, 0.046, 0.073)
if face:FindFirstChild("CloseOld") then face.CloseOld.Visible = false end
local old = face:FindFirstChild("MockBody") if old then old:Destroy() end
local root = Instance.new("Frame") root.Name = "MockBody" root.BackgroundTransparency = 1 root.Size = UDim2.fromScale(1, 1) root.ZIndex = 5 root.Parent = face

local function corner(o, px) local c = Instance.new("UICorner") c.CornerRadius = UDim.new(0, px or 6) c.Parent = o end
local function stroke(o, t, col) local s = Instance.new("UIStroke") s.Thickness = t s.Color = col or OUT s.ApplyStrokeMode = Enum.ApplyStrokeMode.Border s.Parent = o return s end
local function grad(o, a, b, rot) local g = Instance.new("UIGradient") g.Color = typeof(a) == "ColorSequence" and a or ColorSequence.new(a, b) g.Rotation = rot or 90 g.Parent = o return g end
local function frame(parent, x, y, w, h, col, z)
	local f = Instance.new("Frame") f.BorderSizePixel = 0 f.Position = UDim2.fromScale(x, y) f.Size = UDim2.fromScale(w, h)
	f.BackgroundColor3 = col or PANEL f.ZIndex = z or 6 f.Parent = parent return f
end
local function damier(parent, col, tr)
	local d = Instance.new("ImageLabel") d.Name = "Damier" d.BackgroundTransparency = 1 d.Image = DAMIER d.ScaleType = Enum.ScaleType.Tile
	d.TileSize = UDim2.fromOffset(18, 18) d.ImageColor3 = col d.ImageTransparency = tr d.Size = UDim2.fromScale(1, 1) d.ZIndex = parent.ZIndex
	d.Parent = parent corner(d, 6) return d
end
local function text(parent, s, x, y, w, h, col, maxPx, z, align)
	local t = Instance.new("TextLabel") t.BackgroundTransparency = 1 t.Font = Enum.Font.GothamBlack t.Text = s t.RichText = true
	t.TextColor3 = col or WHITE t.TextScaled = true t.Position = UDim2.fromScale(x, y) t.Size = UDim2.fromScale(w, h) t.ZIndex = z or 9
	t.TextXAlignment = align or Enum.TextXAlignment.Center t.Parent = parent
	local c = Instance.new("UITextSizeConstraint") c.MaxTextSize = maxPx or 40 c.Parent = t
	local st = Instance.new("UIStroke") st.Thickness = math.clamp((maxPx or 20) / 9, 1.5, 3) st.Color = C(0, 0, 0) st.Parent = t
	return t
end
local function brick(parent, x, y, w, h, top, bot, bevel, z, opts)
	opts = opts or {}
	local holder = frame(parent, x, y, w, h, nil, z) holder.BackgroundTransparency = 1
	local depth = frame(holder, 0, 0, 1, 1, bevel, z) depth.Name = "Depth" depth.Position = UDim2.new(0, 0, 0, opts.bevelPx or 4) corner(depth, opts.r or 6) stroke(depth, opts.out or 3)
	local f = frame(holder, 0, 0, 1, 1, WHITE, z + 1) f.Name = "Face" corner(f, opts.r or 6) stroke(f, opts.out or 3) grad(f, top, bot, 90)
	if opts.damier ~= false then damier(f, opts.damierCol or C(0, 0, 0), opts.damierT or 0.9) end
	return holder, f
end
local function cornerBadge(holder, kind)
	if kind == "star" then
		local s = Instance.new("ImageLabel") s.BackgroundTransparency = 1 s.Image = "rbxassetid://112780117360743" s.ScaleType = Enum.ScaleType.Fit
		s.AnchorPoint = Vector2.new(0.5, 0.5) s.Position = UDim2.fromScale(0.885, 0.06) s.Size = UDim2.fromScale(0.2, 0.42) s.ZIndex = 14 s.Parent = holder
		local a = Instance.new("UIAspectRatioConstraint") a.Parent = s
	else
		local b = frame(holder, 0.885, 0.06, 0.17, 0.36, C(235, 45, 45), 14) b.AnchorPoint = Vector2.new(0.5, 0.5) corner(b, 100) stroke(b, 2, C(0, 0, 0))
		local a = Instance.new("UIAspectRatioConstraint") a.Parent = b
		text(b, "!", 0, 0.08, 1, 0.84, WHITE, 18, 15)
	end
end
-- tabs: top 0.167, h 0.1077, pitch 0.1197
local TABS = {
	{"GRASS", "5/6", C(160, 240, 40), C(110, 200, 20), C(50, 110, 10)},
	{"WATER", "6/6", C(60, 200, 255), C(0, 130, 235), C(0, 70, 150), "star"},
	{"THUNDER", "6/6", C(255, 236, 80), C(255, 205, 0), C(160, 110, 0), "star"},
	{"FIRE", "4/6", C(255, 140, 60), C(230, 60, 20), C(130, 25, 10)},
	{"SHADOW", "3/6", C(170, 80, 255), C(110, 30, 200), C(60, 10, 120)},
	{"CELESTIAL", "2/6", C(40, 230, 200), C(0, 170, 160), C(0, 90, 90)},
	{"GLACIER", "6/6", C(150, 225, 255), C(60, 140, 230), C(20, 60, 130), "bang"},
}
for i, t in ipairs(TABS) do
	local sel = i == 7
	local holder, f = brick(root, 0.012 + (sel and 0.006 or 0), 0.167 + (i - 1) * 0.1197, 0.118, 0.1077 - 0.007, t[3], t[4], t[5], 6, {bevelPx = 3})
	if sel then f.UIStroke.Color = WHITE f.UIStroke.Thickness = 3.5 end
	text(f, t[1], 0.08, 0.12, 0.78, 0.44, WHITE, 20, 9)
	text(f, t[2], 0.25, 0.6, 0.5, 0.28, WHITE, 14, 9)
	if t[6] then cornerBadge(holder, t[6]) end
end
-- area header 0.167..0.256
local _, ah = brick(root, 0.148, 0.167, 0.568, 0.089, C(200, 240, 255), C(60, 120, 220), C(20, 60, 130), 6, {damierT = 0.88})
text(ah, "GLACIER CREATURES", 0.03, 0.1, 0.47, 0.44, WHITE, 26, 9, Enum.TextXAlignment.Left)
text(ah, "Hatched from the <font color='#FFF3A0'>Glacier Egg</font>", 0.03, 0.56, 0.47, 0.3, WHITE, 15, 9, Enum.TextXAlignment.Left)
local trough = frame(ah, 0.52, 0.26, 0.28, 0.48, C(20, 30, 36), 9) corner(trough, 8) stroke(trough, 2, C(12, 18, 22))
local tf = frame(trough, 0, 0, 1, 1, WHITE, 9) corner(tf, 8) grad(tf, C(180, 255, 25), C(105, 225, 0), 90)
text(trough, "5 / 5", 0, 0.1, 1, 0.8, WHITE, 16, 10)
local _, pip = brick(ah, 0.815, 0.2, 0.16, 0.58, C(255, 224, 96), C(232, 160, 28), C(150, 80, 0), 9, {bevelPx = 3, out = 2})
text(pip, "BONUS 1/1", 0.05, 0.1, 0.9, 0.8, WHITE, 15, 12)
-- grid panel 0.264..0.792, cards h 0.245 rows 0.274 / 0.535
local grid = frame(root, 0.148, 0.264, 0.568, 0.528, PANEL, 6) corner(grid, 6) stroke(grid, 3)
local gh = frame(grid, 0, 0, 1, 1, PANEL, 6) gh.BackgroundTransparency = 1 corner(gh, 6) local ghs = stroke(gh, 1.2, HIGH) ghs.Transparency = 0.4
local PETS = {
	{"FROSTFANG LYNX", "50%"}, {"ICE MAMMOTH", "26%"}, {"GLACIER YETI", "14%"},
	{"BLIZZARD ROC", "7.4%"}, {"PERMAFROST TITAN", "2.5%", "secret"}, {"FROSTCROWN DRAGON", "0.1%", "mythic"},
}
local XS, YS, CWID, CH = {0.160, 0.3453, 0.5306}, {0.274, 0.535}, 0.1733, 0.245
local slots = {}
local SELECT = _G.MockSelect or 6
for k, p in ipairs(PETS) do
	local x, y = XS[(k - 1) % 3 + 1], YS[math.floor((k - 1) / 3) + 1]
	local holder, f
	if p[3] == "mythic" then
		local ring = frame(root, x, y, CWID, CH, WHITE, 7) ring.Size = UDim2.new(CWID, 4, CH, 4) ring.Position = UDim2.new(x, -2, y, -2) corner(ring, 8) grad(ring, RAINBOW, nil, 45)
		if k == SELECT then local sel = Instance.new("UIStroke") sel.Thickness = 3 sel.Color = WHITE sel.Parent = ring end
		holder, f = brick(root, x, y, CWID, CH, C(40, 34, 84), C(16, 14, 40), C(16, 14, 40), 8, {damierCol = WHITE, damierT = 0.93})
		f.UIStroke.Enabled = false holder.Depth.UIStroke.Enabled = false holder.Depth.BackgroundTransparency = 1
		local disc = frame(f, 0.5, 0.56, 0, 0, WHITE, 9) disc.AnchorPoint = Vector2.new(0.5, 0.5) disc.Size = UDim2.fromScale(0.5, 0.66) disc.BackgroundTransparency = 0.9 corner(disc, 100)
		local ar = Instance.new("UIAspectRatioConstraint") ar.Parent = disc
	elseif p[3] == "secret" then
		holder, f = brick(root, x, y, CWID, CH, C(255, 224, 96), C(232, 160, 28), C(150, 80, 0), 8)
		local hl = Instance.new("Frame") hl.BackgroundTransparency = 1 hl.Size = UDim2.new(1, -4, 1, -4) hl.Position = UDim2.fromOffset(2, 2) hl.ZIndex = 9 hl.Parent = f corner(hl, 5)
		local hs = stroke(hl, 1.2, C(255, 250, 210)) hs.Transparency = 0.4
	else
		holder, f = brick(root, x, y, CWID, CH, C(226, 246, 255), C(160, 210, 245), C(60, 120, 190), 8)
	end
	if k == SELECT and p[3] ~= "mythic" then f.UIStroke.Color = WHITE f.UIStroke.Thickness = 3.5 end
	text(f, p[1], 0.04, 0.11, 0.92, 0.12, WHITE, 14, 12)
	local slot = frame(f, 0.1, 0.22, 0.8, 0.68, WHITE, 9) slot.BackgroundTransparency = 1 slot.Name = "Portrait"
	local _, pill = brick(f, 0.22, 0.83, 0.56, 0.12, C(36, 58, 68), PANEL, C(12, 18, 22), 12, {bevelPx = 2, out = 2, damier = false, r = 10})
	text(pill, p[2], 0.05, 0.1, 0.9, 0.8, WHITE, 13, 15)
	if p[3] == "secret" then
		local _, r = brick(holder, 0.24, -0.03, 0.52, 0.13, C(255, 20, 128), C(212, 0, 85), C(120, 10, 45), 14, {bevelPx = 2, out = 2, damier = false, r = 8})
		text(r, "SECRET", 0.05, 0.08, 0.9, 0.84, WHITE, 12, 16)
	elseif p[3] == "mythic" then
		local edge = frame(holder, 0.24, -0.03, 0.52, 0.13, WHITE, 14) edge.Size = UDim2.new(0.52, 4, 0.13, 4) edge.Position = UDim2.new(0.24, -2, -0.03, -2) corner(edge, 10) grad(edge, RAINBOW, nil, 0)
		local rib = frame(holder, 0.24, -0.03, 0.52, 0.13, C(20, 14, 40), 15) corner(rib, 8)
		text(rib, "MYTHIC", 0.05, 0.08, 0.9, 0.84, WHITE, 12, 16)
	end
	if k == SELECT then local sc = Instance.new("UIScale") sc.Scale = 1.04 sc.Parent = holder end
	slots[k] = slot
end
-- reward strip 0.800..0.880
local rs = frame(root, 0.148, 0.8, 0.568, 0.08, PANEL, 6) corner(rs, 6) stroke(rs, 3)
local rsh = frame(rs, 0, 0, 1, 1) rsh.BackgroundTransparency = 1 corner(rsh, 6) local rss = stroke(rsh, 2, HIGH) rss.Transparency = 0.4
text(rs, "COMPLETE<br/>GLACIER:", 0.02, 0.1, 0.22, 0.8, C(255, 210, 60), 15, 9, Enum.TextXAlignment.Left)
local function chip(i, icon, val)
	local c = frame(rs, 0.255 + (i - 1) * 0.132, 0.17, 0.12, 0.66, PANEL, 8) corner(c, 6) stroke(c, 2, C(0, 0, 0))
	local hl = frame(c, 0, 0, 1, 1) hl.BackgroundTransparency = 1 corner(hl, 6) local s = stroke(hl, 1.5, HIGH) s.Transparency = 0.3
	local im = Instance.new("ImageLabel") im.BackgroundTransparency = 1 im.Image = icon im.ScaleType = Enum.ScaleType.Fit im.Position = UDim2.fromScale(0.04, 0.12) im.Size = UDim2.fromScale(0.42, 0.76) im.ZIndex = 9 im.Parent = c
	text(c, val, 0.46, 0.2, 0.5, 0.6, WHITE, 15, 10)
end
chip(1, "rbxassetid://131724750673548", "+5%") chip(2, "rbxassetid://80829076123513", "+5%")
chip(3, PotionConfig.byKey.Money.icon, "x1") chip(4, PotionConfig.byKey.Hatch.icon, "x1")
local _, cb = brick(rs, 0.795, 0.14, 0.19, 0.66, C(180, 255, 25), C(105, 225, 0), C(15, 120, 15), 8, {bevelPx = 3})
text(cb, "CLAIM!", 0.05, 0.12, 0.9, 0.76, WHITE, 20, 12)
-- footer 0.890..0.986 (+ its own 3 px bevel/outline reaches the face edge)
local ft = frame(root, 0.148, 0.89, 0.568, 0.096, PANEL, 6) corner(ft, 6) stroke(ft, 3)
local book = Instance.new("ImageLabel") book.BackgroundTransparency = 1 book.Image = "rbxassetid://122195701390652" book.ScaleType = Enum.ScaleType.Fit
book.AnchorPoint = Vector2.new(0.5, 0.5) book.Position = UDim2.fromScale(0.052, 0.5) book.Size = UDim2.fromScale(0.088, 0.82) book.ZIndex = 9 book.Parent = ft
local tr = frame(ft, 0.118, 0.26, 0.6, 0.48, C(20, 30, 36), 8) corner(tr, 10) stroke(tr, 2, C(12, 18, 22))
local fill = frame(tr, 0, 0, 33 / 42, 1, WHITE, 8) corner(fill, 10) grad(fill, C(255, 200, 0), C(255, 106, 0), 90)
text(tr, "DISCOVERED 33 / 42", 0.04, 0.12, 0.92, 0.76, WHITE, 18, 10)
local caH, ca = brick(ft, 0.745, 0.2, 0.235, 0.56, C(255, 208, 0), C(255, 140, 0), C(153, 76, 0), 8, {bevelPx = 3})
text(ca, "CLAIM ALL", 0.06, 0.16, 0.88, 0.68, WHITE, 16, 12)
local cnt = frame(caH, 1, 0, 0, 0, C(255, 255, 255), 16) cnt.AnchorPoint = Vector2.new(0.5, 0.5) cnt.Position = UDim2.fromScale(0.97, 0.05) cnt.Size = UDim2.fromScale(0.2, 0.62) corner(cnt, 100) stroke(cnt, 2, C(0, 0, 0))
local car = Instance.new("UIAspectRatioConstraint") car.Parent = cnt
local ct = text(cnt, "1", 0, 0.08, 1, 0.84, C(20, 20, 20), 16, 17) ct.UIStroke.Enabled = false
-- inspect 0.167..0.986
local INS = {
	mythic = {"FROSTCROWN DRAGON", "GLACIER · MYTHIC · <font color='#7DFF6A'>$x8.8</font>", {C(150, 140, 230), C(60, 52, 130)}, "rainbow", {"$83.5M/s", "1M KG", "x1", "0.1%"}, C(20, 14, 40)},
	secret = {"PERMAFROST TITAN", "GLACIER · SECRET · <font color='#7DFF6A'>$x3.3</font>", {C(255, 224, 96), C(232, 160, 28)}, C(255, 214, 90), {"$31.2M/s", "1M KG", "x2", "2.5%"}, C(120, 10, 45)},
	common = {"FROSTFANG LYNX", "GLACIER", {C(190, 228, 255), C(110, 170, 230)}, C(226, 246, 255), {"$9.5M/s", "1M KG", "x14", "50%"}, C(20, 60, 130)},
}
local ins = INS[_G.MockInspect or "mythic"]
local ip = frame(root, 0.73, 0.167, 0.258, 0.819, PANEL, 6) corner(ip, 6) stroke(ip, 3)
local iph = frame(ip, 0, 0, 1, 1) iph.BackgroundTransparency = 1 corner(iph, 6) local ips = stroke(iph, 2, HIGH) ips.Transparency = 0.4
damier(ip, C(0, 0, 0), 0.92)
local ringD = frame(ip, 0.5, 0.235, 0, 0, WHITE, 7) ringD.AnchorPoint = Vector2.new(0.5, 0.5) ringD.Size = UDim2.new(0.73, 6, 0.73, 6) corner(ringD, 1000)
if ins[4] == "rainbow" then grad(ringD, RAINBOW, nil, 45) else ringD.BackgroundColor3 = ins[4] end
local ar1 = Instance.new("UIAspectRatioConstraint") ar1.Parent = ringD
local disc = frame(ip, 0.5, 0.235, 0.73, 0.73, WHITE, 8) disc.AnchorPoint = Vector2.new(0.5, 0.5) corner(disc, 1000) grad(disc, ins[3][1], ins[3][2], 90)
local ar2 = Instance.new("UIAspectRatioConstraint") ar2.Parent = disc
local stage = frame(ip, 0.06, 0.03, 0.88, 0.40, WHITE, 9) stage.BackgroundTransparency = 1 stage.Name = "Stage"
text(ip, ins[1], 0.04, 0.452, 0.92, 0.065, WHITE, 18, 10)
if ins[4] == "rainbow" then local re = frame(ip, 0.08, 0.527, 0.84, 0.058, WHITE, 8) corner(re, 10) grad(re, RAINBOW, nil, 0) end
local rp = frame(ip, 0.088, 0.531, 0.824, 0.05, ins[6], 9) corner(rp, 9) if ins[4] ~= "rainbow" then stroke(rp, 2, C(0, 0, 0)) end
text(rp, ins[2], 0.04, 0.12, 0.92, 0.76, WHITE, 14, 10)
local LBL = {"Income (best KG)", "Best weight", "Hatched", "Hatch chance"}
for i = 1, 4 do
	local row = frame(ip, 0.058, 0.62 + (i - 1) * 0.088, 0.884, 0.074, C(24, 36, 44), 8) corner(row, 8) stroke(row, 2, C(12, 18, 22))
	text(row, LBL[i], 0.04, 0.26, 0.5, 0.48, C(190, 205, 255), 13, 10, Enum.TextXAlignment.Left)
	text(row, i == 1 and ("<font color='#78EB5A'>" .. ins[5][1] .. "</font>") or ins[5][i], 0.56, 0.22, 0.4, 0.56, WHITE, 16, 10, Enum.TextXAlignment.Right)
end
task.wait(0.5)
local function rr(o) local p, s = o.AbsolutePosition, o.AbsoluteSize return string.format("(%d, %d, %d, %d)", p.X, p.Y + 58, s.X, s.Y) end
local out = {}
for k = 1, 6 do table.insert(out, rr(slots[k])) end
return "RECTS " .. table.concat(out, ", ") .. "\nSTAGE " .. rr(stage) .. "\nWIN " .. rr(win)