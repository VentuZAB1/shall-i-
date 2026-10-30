local plr = game.Players.LocalPlayer
local pg = plr.PlayerGui
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
_G.HiddenGuis = _G.HiddenGuis or {}
for _, g in ipairs(pg:GetChildren()) do
	if g:IsA("ScreenGui") and g.Enabled and g.Name ~= "PhoneMock" then g.Enabled = false table.insert(_G.HiddenGuis, g) end
end
local old = pg:FindFirstChild("PhoneMock") if old then old:Destroy() end
local sg = Instance.new("ScreenGui") sg.Name = "PhoneMock" sg.IgnoreGuiInset = true sg.DisplayOrder = 50 sg.ResetOnSpawn = false sg.Parent = pg
local vp = workspace.CurrentCamera.ViewportSize
local canvas = Instance.new("Frame") canvas.Name = "Canvas" canvas.Size = UDim2.fromOffset(844, 390) canvas.AnchorPoint = Vector2.new(0.5, 0.5)
canvas.Position = UDim2.fromScale(0.5, 0.5) canvas.BackgroundColor3 = C(0, 0, 0) canvas.BackgroundTransparency = 0.45 canvas.ClipsDescendants = true canvas.Parent = sg
local cs = Instance.new("UIStroke") cs.Thickness = 6 cs.Color = C(10, 10, 12) cs.Parent = canvas

local function corner(o, px) local c = Instance.new("UICorner") c.CornerRadius = UDim.new(0, px or 6) c.Parent = o end
local function stroke(o, t, col) local s = Instance.new("UIStroke") s.Thickness = t s.Color = col or OUT s.ApplyStrokeMode = Enum.ApplyStrokeMode.Border s.Parent = o return s end
local function grad(o, a, b, rot) local g = Instance.new("UIGradient") g.Color = typeof(a) == "ColorSequence" and a or ColorSequence.new(a, b) g.Rotation = rot or 90 g.Parent = o return g end
local function frame(parent, x, y, w, h, col, z)
	local f = Instance.new("Frame") f.BorderSizePixel = 0 f.Position = UDim2.fromScale(x, y) f.Size = UDim2.fromScale(w, h)
	f.BackgroundColor3 = col or PANEL f.ZIndex = z or 6 f.Parent = parent return f
end
local function damier(parent, col, tr, tile)
	local d = Instance.new("ImageLabel") d.Name = "Damier" d.BackgroundTransparency = 1 d.Image = DAMIER d.ScaleType = Enum.ScaleType.Tile
	d.TileSize = UDim2.fromOffset(tile or 14, tile or 14) d.ImageColor3 = col d.ImageTransparency = tr d.Size = UDim2.fromScale(1, 1) d.ZIndex = parent.ZIndex
	d.Parent = parent corner(d, 6) return d
end
local function text(parent, s, x, y, w, h, col, maxPx, z, align)
	local t = Instance.new("TextLabel") t.BackgroundTransparency = 1 t.Font = Enum.Font.GothamBlack t.Text = s t.RichText = true
	t.TextColor3 = col or WHITE t.TextScaled = true t.Position = UDim2.fromScale(x, y) t.Size = UDim2.fromScale(w, h) t.ZIndex = z or 9
	t.TextXAlignment = align or Enum.TextXAlignment.Center t.Parent = parent
	local c = Instance.new("UITextSizeConstraint") c.MaxTextSize = maxPx or 40 c.MinTextSize = 10 c.Parent = t
	local st = Instance.new("UIStroke") st.Thickness = math.clamp((maxPx or 20) / 10, 1.2, 2.5) st.Color = C(0, 0, 0) st.Parent = t
	return t
end
local function brick(parent, x, y, w, h, top, bot, bevel, z, opts)
	opts = opts or {}
	local holder = frame(parent, x, y, w, h, nil, z) holder.BackgroundTransparency = 1
	local depth = frame(holder, 0, 0, 1, 1, bevel, z) depth.Name = "Depth" depth.Position = UDim2.new(0, 0, 0, opts.bevelPx or 3) corner(depth, opts.r or 6) stroke(depth, opts.out or 2.5)
	local f = frame(holder, 0, 0, 1, 1, WHITE, z + 1) f.Name = "Face" corner(f, opts.r or 6) stroke(f, opts.out or 2.5) grad(f, top, bot, 90)
	if opts.damier ~= false then damier(f, opts.damierCol or C(0, 0, 0), opts.damierT or 0.9) end
	return holder, f
end
-- window 0.96 x 0.94
local win = frame(canvas, 0.02, 0.03, 0.96, 0.94, C(59, 88, 102), 5) corner(win, 6) stroke(win, 3.5)
-- header 0 .. 0.15
local hd = frame(win, 0, 0, 1, 0.15, WHITE, 6) corner(hd, 6) grad(hd, C(0, 205, 255), C(0, 130, 245), 90) damier(hd, C(0, 75, 150), 0.8, 12)
local div = frame(win, 0, 0.15, 1, 0, C(0, 50, 110), 7) div.Size = UDim2.new(1, 0, 0, 3)
local div2 = frame(win, 0, 0.15, 1, 0, C(0, 0, 0), 7) div2.Size = UDim2.new(1, 0, 0, 3) div2.Position = UDim2.new(0, 0, 0.15, 3)
local book = Instance.new("ImageLabel") book.BackgroundTransparency = 1 book.Image = "rbxassetid://122195701390652" book.ScaleType = Enum.ScaleType.Fit
book.Position = UDim2.fromScale(0.012, 0.005) book.Size = UDim2.fromScale(0.06, 0.14) book.ZIndex = 9 book.Parent = win
text(win, "Creature Index", 0.3, 0.012, 0.4, 0.085, WHITE, 24, 9)
text(win, "DISCOVERED <font color='#FFD23C'>33 / 42</font>", 0.35, 0.095, 0.3, 0.045, WHITE, 12, 9)
local _, xb = brick(win, 0.94, 0.018, 0.048, 0.11, C(255, 125, 175), C(255, 20, 40), C(115, 0, 16), 10, {damier = false, r = 4})
text(xb, "X", 0.1, 0.06, 0.8, 0.86, WHITE, 24, 13)
-- tabs strip 0.175 .. 0.295 (44 px)
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
	local holder, f = brick(win, 0.0185 + (i - 1) * 0.138, 0.18, 0.13, 0.12, t[3], t[4], t[5], 8)
	if i == 7 then f.UIStroke.Color = WHITE f.UIStroke.Thickness = 3 end
	text(f, t[1], 0.06, 0.08, 0.88, 0.5, WHITE, 14, 11)
	text(f, t[2], 0.2, 0.58, 0.6, 0.34, WHITE, 12, 11)
	if t[6] == "star" then
		local s = Instance.new("ImageLabel") s.BackgroundTransparency = 1 s.Image = "rbxassetid://112780117360743" s.ScaleType = Enum.ScaleType.Fit
		s.AnchorPoint = Vector2.new(0.5, 0.5) s.Position = UDim2.fromScale(0.92, 0.1) s.Size = UDim2.fromOffset(18, 18) s.ZIndex = 14 s.Parent = holder
	elseif t[6] == "bang" then
		local b = frame(holder, 0.92, 0.1, 0, 0, C(235, 45, 45), 14) b.AnchorPoint = Vector2.new(0.5, 0.5) b.Size = UDim2.fromOffset(17, 17) corner(b, 10) stroke(b, 1.5, C(0, 0, 0))
		text(b, "!", 0, 0.05, 1, 0.9, WHITE, 13, 15)
	end
end
-- grid 0.315 .. 0.795: 3 x 2 horizontal cards
local grid = frame(win, 0.012, 0.315, 0.976, 0.48, PANEL, 6) corner(grid, 6) stroke(grid, 2.5)
local PETS = {
	{"FROSTFANG LYNX", "50%"}, {"ICE MAMMOTH", "26%"}, {"GLACIER YETI", "14%"},
	{"BLIZZARD ROC", "7.4%"}, {"PERMAFROST TITAN", "2.5%", "secret"}, {"FROSTCROWN DRAGON", "0.1%", "mythic"},
}
local slots = {}
local cw, ch = (0.976 - 4 * 0.01) / 3, (0.48 - 3 * 0.014) / 2
for k, p in ipairs(PETS) do
	local col, row = (k - 1) % 3, math.floor((k - 1) / 3)
	local x, y = 0.012 + 0.01 + col * (cw + 0.01), 0.315 + 0.014 + row * (ch + 0.014)
	local holder, f
	if p[3] == "mythic" then
		local ring = frame(win, x, y, cw, ch, WHITE, 7) ring.Size = UDim2.new(cw, 4, ch, 4) ring.Position = UDim2.new(x, -2, y, -2) corner(ring, 8) grad(ring, RAINBOW, nil, 45)
		holder, f = brick(win, x, y, cw, ch, C(40, 34, 84), C(16, 14, 40), C(16, 14, 40), 8, {damierCol = WHITE, damierT = 0.93})
		f.UIStroke.Enabled = false holder.Depth.UIStroke.Enabled = false holder.Depth.BackgroundTransparency = 1
	elseif p[3] == "secret" then
		holder, f = brick(win, x, y, cw, ch, C(255, 224, 96), C(232, 160, 28), C(150, 80, 0), 8)
	else
		holder, f = brick(win, x, y, cw, ch, C(226, 246, 255), C(160, 210, 245), C(60, 120, 190), 8)
	end
	-- portrait square on the left (0.9 of card h)
	local slot = frame(f, 0.02, 0.05, 0.3, 0.9, WHITE, 9) slot.BackgroundTransparency = 1 slot.Name = "Portrait"
	local ar = Instance.new("UIAspectRatioConstraint") ar.Parent = slot
	if p[3] == "mythic" then local d = frame(f, 0.02, 0.05, 0.3, 0.9, WHITE, 9) d.BackgroundTransparency = 0.9 corner(d, 100) local a2 = Instance.new("UIAspectRatioConstraint") a2.Parent = d end
	text(f, p[1], 0.36, 0.1, 0.6, 0.34, WHITE, 16, 12, Enum.TextXAlignment.Left)
	local _, pill = brick(f, 0.36, 0.56, 0.26, 0.3, C(36, 58, 68), PANEL, C(12, 18, 22), 12, {bevelPx = 2, out = 2, damier = false, r = 10})
	text(pill, p[2], 0.06, 0.1, 0.88, 0.8, WHITE, 14, 15)
	if p[3] == "secret" then
		local _, r = brick(f, 0.65, 0.56, 0.3, 0.3, C(255, 20, 128), C(212, 0, 85), C(120, 10, 45), 12, {bevelPx = 2, out = 2, damier = false, r = 10})
		text(r, "SECRET", 0.06, 0.12, 0.88, 0.76, WHITE, 12, 15)
	elseif p[3] == "mythic" then
		local edge = frame(f, 0.65, 0.56, 0.3, 0.3, WHITE, 12) edge.Size = UDim2.new(0.3, 4, 0.3, 4) edge.Position = UDim2.new(0.65, -2, 0.56, -2) corner(edge, 10) grad(edge, RAINBOW, nil, 0)
		local rib = frame(f, 0.65, 0.56, 0.3, 0.3, C(20, 14, 40), 13) corner(rib, 9)
		text(rib, "MYTHIC", 0.06, 0.12, 0.88, 0.76, WHITE, 12, 15)
	end
	slots[k] = slot
end
-- bottom row 0.81 .. 0.97
local br = frame(win, 0.012, 0.815, 0.976, 0.155, PANEL, 6) corner(br, 6) stroke(br, 2.5)
text(br, "COMPLETE GLACIER<br/><font color='#B4FF19'>5/5</font>  ·  <font color='#FFD23C'>BONUS 1/1</font>", 0.015, 0.1, 0.22, 0.8, C(255, 210, 60), 14, 9, Enum.TextXAlignment.Left)
local function chip(i, icon, val)
	local c = frame(br, 0.245 + (i - 1) * 0.088, 0.16, 0.08, 0.68, PANEL, 8) corner(c, 6) stroke(c, 2, C(0, 0, 0))
	local im = Instance.new("ImageLabel") im.BackgroundTransparency = 1 im.Image = icon im.ScaleType = Enum.ScaleType.Fit im.Position = UDim2.fromScale(0.04, 0.12) im.Size = UDim2.fromScale(0.44, 0.76) im.ZIndex = 9 im.Parent = c
	text(c, val, 0.46, 0.2, 0.5, 0.6, WHITE, 13, 10)
end
chip(1, "rbxassetid://131724750673548", "+5%") chip(2, "rbxassetid://80829076123513", "+5%")
chip(3, PotionConfig.byKey.Money.icon, "x1") chip(4, PotionConfig.byKey.Hatch.icon, "x1")
local _, cb = brick(br, 0.6, 0.12, 0.17, 0.72, C(180, 255, 25), C(105, 225, 0), C(15, 120, 15), 8)
text(cb, "CLAIM!", 0.06, 0.12, 0.88, 0.76, WHITE, 20, 12)
local caH, ca = brick(br, 0.79, 0.12, 0.19, 0.72, C(255, 208, 0), C(255, 140, 0), C(153, 76, 0), 8)
text(ca, "CLAIM ALL", 0.06, 0.16, 0.88, 0.68, WHITE, 16, 12)
local cnt = frame(caH, 0.96, 0.02, 0, 0, WHITE, 16) cnt.AnchorPoint = Vector2.new(0.5, 0.5) cnt.Size = UDim2.fromOffset(20, 20) corner(cnt, 10) stroke(cnt, 1.5, C(0, 0, 0))
local ct = text(cnt, "1", 0, 0.05, 1, 0.9, C(20, 20, 20), 13, 17) ct.UIStroke.Enabled = false
task.wait(0.5)
local out = {}
local function rr(o) local p, s = o.AbsolutePosition, o.AbsoluteSize return string.format("(%d, %d, %d, %d)", p.X, p.Y, s.X, s.Y) end
for k = 1, 6 do table.insert(out, rr(slots[k])) end
return "RECTS " .. table.concat(out, ", ") .. "\nCANVAS " .. rr(canvas)