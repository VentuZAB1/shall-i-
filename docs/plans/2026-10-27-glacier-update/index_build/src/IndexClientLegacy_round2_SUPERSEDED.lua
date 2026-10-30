-- IndexClient (Check-UI, Glacier update 2026-10-28): the Creature Index page (MainMenu window, Index tile), built to the
-- APPROVED v8 mockup (docs/plans/2026-10-27-glacier-update/index_mockup: INDEX_MOCKUP_v8.png, MOCKUP_NOTES.md, review 5;
-- geometry + colours from recovered/mock_73374.lua + mock_74213 / 74229, CLAIM ALL = review 5 M1).
--   left:   one tab per area (7): x/N found, gold star when claimed, red ! when the reward waits
--   centre: area header (progress of the cards the claim needs + a BONUS x/y pip when the area has a mythic),
--           2 rows x 3 creature cards (black silhouette + ? until found; SECRET = gold card + pink badge, MYTHIC = the
--           Day-7 rainbow card + MYTHIC badge), reward strip + CLAIM (+5% money, +5% speed, 1 Money + 1 Hatch potion),
--           footer DISCOVERED x/N + CLAIM ALL
--   right:  inspect panel (portrait disc, name, area / rarity pill with the money bonus, income at the best KG, best
--           weight, times hatched, hatch chance)
-- No rarity names (vault rule): the area, SECRET / MYTHIC and the money bonus do the work.
-- Mythics (CreatureConfig mythic) are BONUS cards: they count in x/N, never in the claim (IndexConfig.areaComplete).
-- An area claimed before it grew (IndexConfig.isUpdated) can be completed and claimed AGAIN (CLAIM AGAIN!).
-- ONE layout on every device (owner 2026-10-28): the page fills the window face (MenuController CHROME.Index: 0.15
-- header, Body = the face) and is drawn in the mockup's own pixels (face DESIGN_H tall) under a UIScale (CanvasScale =
-- face height / DESIGN_H), so strokes, corners, bevels and text caps scale with the window: a phone = the PC page scaled.
-- Data: saved attribute IndexData (IndexServer / PetIndex). Rewards: Index.Claim remote (as before).
-- Tests: ServerStorage.HatchRISTests.index_client, sections v8*. IndexPage.TestPress:Fire(key): Tab_<i> / Card_<slot> /
-- Claim / ClaimAll; attribute IndexRefreshN counts refreshes. Before: ServerStorage._Backup_GlacierS2.IndexBuild.
-- 2026-10-29 build review 1 (before: _Backup_GlacierS2.IndexBuild2): M1 phone text floor (phoneBox, below: on a small
-- window the labels grow inside their own boxes, nothing moves), N3 header title / subtitle at the v8 size, N4 an
-- unfound creature's pill shows only its area, N5 one "?" per silhouette (the ??? name plate; no centre ?).
-- 2026-10-29 build review 2 (before: _Backup_GlacierS2.IndexBuild3): MUST 1 phone clearance (after the phone boxes: a
-- grown label keeps 3 px between its text and its box's edges; the CLAIM ALL count badge 2.5 px up / right on a
-- phone). IndexPage.PhoneClear:Invoke() = every phone label's clearance (tests + build notes).
local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local RS = game:GetService("ReplicatedStorage")
local IndexConfig = require(RS:WaitForChild("IndexConfig"))
local CreatureConfig = require(RS:WaitForChild("CreatureConfig"))
local SpeedStat = require(RS:WaitForChild("SpeedStat"))
local PotionConfig = require(RS:WaitForChild("PotionConfig"))
local SFX = require(RS:WaitForChild("SFX"))
local Claim = RS:WaitForChild("Index"):WaitForChild("Claim")
local MODELS = RS:WaitForChild("CreatureModels")

local player = Players.LocalPlayer
local menu = player:WaitForChild("PlayerGui"):WaitForChild("MainMenu")
local face = menu:WaitForChild("Window"):WaitForChild("Face")
local body = face:WaitForChild("Body")

local data = IndexConfig.decode(player:GetAttribute("IndexData"))
local areaSel, creatureSel = 1, nil

---------------------------------------------------------------- the v8 look
local C = Color3.fromRGB
local WHITE, BLACK = Color3.new(1, 1, 1), Color3.new(0, 0, 0)
local OUT = C(24, 30, 34) -- Check-UI outline
local PANEL = C(26, 44, 52) -- recessed card
local HIGH = C(75, 125, 145) -- card inner highlight
local TROUGH, TROUGH_EDGE = C(20, 30, 36), C(12, 18, 22)
local ROW = C(24, 36, 44)
local LABEL = C(190, 205, 255)
local GOLD_TEXT = C(255, 210, 60)
local DAMIER = "rbxassetid://385956923"
local BOOK_ICON = "rbxassetid://122195701390652"
local MONEY_ICON = "rbxassetid://131724750673548"
local SPEED_ICON = "rbxassetid://80829076123513"
local STAR_ICON = "rbxassetid://112780117360743"
local RAINBOW = ColorSequence.new({ -- Check-UI Day-7 spectrum
	ColorSequenceKeypoint.new(0.00, C(255, 30, 80)), ColorSequenceKeypoint.new(0.18, C(255, 140, 0)),
	ColorSequenceKeypoint.new(0.35, C(255, 230, 0)), ColorSequenceKeypoint.new(0.52, C(40, 230, 50)),
	ColorSequenceKeypoint.new(0.70, C(0, 210, 255)), ColorSequenceKeypoint.new(0.85, C(90, 60, 255)),
	ColorSequenceKeypoint.new(1.00, C(220, 0, 230)),
})
-- {top, bottom, bevel}
local LIME = {C(180, 255, 25), C(105, 225, 0), C(15, 120, 15)}
local SILVER = {C(216, 222, 228), C(148, 160, 176), C(72, 82, 96)}
local OFF = {C(80, 85, 90), C(45, 50, 55), C(28, 30, 34)}
local CLAIM_ALL = {C(214, 98, 0), C(190, 68, 0), C(120, 48, 0)} -- review 5 M1: darker amber, the white label passes 3:1
local GOLD = {C(255, 224, 96), C(232, 160, 28), C(150, 80, 0)}
local PINK = {C(255, 20, 128), C(212, 0, 85), C(120, 10, 45)}
local PILL = {C(36, 58, 68), PANEL, C(12, 18, 22)}
local MYTHIC_CARD = {C(40, 34, 84), C(16, 14, 40), C(16, 14, 40)}
local MYTHIC_DISC = {C(150, 140, 230), C(60, 52, 130)}
local MYTHIC_INK = C(20, 14, 40)
local SECRET_INK = C(120, 10, 45)
local SECRET_RING = C(255, 214, 90)
local UNKNOWN_DISC = {C(70, 75, 100), C(40, 44, 62)}
local UNKNOWN_RING = C(90, 96, 120)
local TAB_COLORS = { -- the mockup's tab bricks, by area
	{C(160, 240, 40), C(110, 200, 20), C(50, 110, 10)},
	{C(60, 200, 255), C(0, 130, 235), C(0, 70, 150)},
	{C(255, 236, 80), C(255, 205, 0), C(160, 110, 0)},
	{C(255, 140, 60), C(230, 60, 20), C(130, 25, 10)},
	{C(170, 80, 255), C(110, 30, 200), C(60, 10, 120)},
	{C(40, 230, 200), C(0, 170, 160), C(0, 90, 90)},
	{C(150, 225, 255), C(60, 140, 230), C(20, 60, 130)},
}
-- a normal card + its inspect disc in the area's colours (Glacier = the mockup's exact light-ice values)
local CARD_COLORS = {[7] = {C(226, 246, 255), C(160, 210, 245), C(60, 120, 190)}}
local DISC_COLORS = {[7] = {C(190, 228, 255), C(110, 170, 230)}}
local function tabColors(i)
	local a = IndexConfig.AREAS[i]
	return TAB_COLORS[i] or {a.colors[1], a.colors[2], a.colors[2]:Lerp(BLACK, 0.45)}
end
local function cardColors(i)
	local a = IndexConfig.AREAS[i]
	return CARD_COLORS[i] or {a.colors[1]:Lerp(WHITE, 0.45), a.colors[1]:Lerp(a.colors[2], 0.28), a.colors[2]:Lerp(BLACK, 0.15)}
end
local function discColors(i)
	local a = IndexConfig.AREAS[i]
	return DISC_COLORS[i] or {a.colors[1]:Lerp(a.colors[2], 0.07), a.colors[1]:Lerp(a.colors[2], 0.64)}
end
local function dim(c, k) return c:Lerp(BLACK, k) end
local function dimmed(cols) return {dim(cols[1], 0.55), dim(cols[2], 0.6), dim(cols[3], 0.4)} end

local DESIGN_H = 562 -- the mockup's face height in px: every px number below is at this size (CanvasScale does the rest)

---------------------------------------------------------------- building blocks (the mockup's helpers)
local function corner(o, px) local c = Instance.new("UICorner") c.CornerRadius = UDim.new(0, px or 6) c.Parent = o return c end
local function stroke(o, t, col)
	local s = Instance.new("UIStroke") s.Thickness = t s.Color = col or OUT s.ApplyStrokeMode = Enum.ApplyStrokeMode.Border s.Parent = o
	return s
end
local function grad(o, a, b, rot)
	local g = Instance.new("UIGradient") g.Color = typeof(a) == "ColorSequence" and a or ColorSequence.new(a, b) g.Rotation = rot or 90 g.Parent = o
	return g
end
local function aspect(o) local a = Instance.new("UIAspectRatioConstraint") a.Parent = o return a end
-- top-left Scale rect, like the mockup
local function frame(parent, x, y, w, h, col, z, name)
	local f = Instance.new("Frame") f.Name = name or "Frame" f.BorderSizePixel = 0 f.Position = UDim2.fromScale(x, y) f.Size = UDim2.fromScale(w, h)
	f.BackgroundColor3 = col or PANEL f.ZIndex = z or 6 f.Parent = parent
	return f
end
-- the same rect anchored at its centre (Check-UI: scale animations grow from the centre)
local function centred(o)
	local p, s = o.Position, o.Size
	o.AnchorPoint = Vector2.new(0.5, 0.5)
	o.Position = UDim2.new(p.X.Scale + s.X.Scale / 2, p.X.Offset + s.X.Offset / 2, p.Y.Scale + s.Y.Scale / 2, p.Y.Offset + s.Y.Offset / 2)
	return o
end
local function damier(parent, col, tr)
	local d = Instance.new("ImageLabel") d.Name = "Damier" d.BackgroundTransparency = 1 d.Image = DAMIER d.ScaleType = Enum.ScaleType.Tile
	d.TileSize = UDim2.fromOffset(18, 18) d.ImageColor3 = col d.ImageTransparency = tr d.Size = UDim2.fromScale(1, 1) d.ZIndex = parent.ZIndex
	d.Parent = parent
	corner(d, 6)
	return d
end
local function text(parent, s, x, y, w, h, col, maxPx, z, align, name)
	local t = Instance.new("TextLabel") t.Name = name or "Text" t.BackgroundTransparency = 1 t.Font = Enum.Font.GothamBlack t.Text = s t.RichText = true
	t.TextColor3 = col or WHITE t.TextScaled = true t.Position = UDim2.fromScale(x, y) t.Size = UDim2.fromScale(w, h) t.ZIndex = z or 9
	t.TextXAlignment = align or Enum.TextXAlignment.Center t.Parent = parent
	local c = Instance.new("UITextSizeConstraint") c.MaxTextSize = maxPx or 40 c.Parent = t
	local st = Instance.new("UIStroke") st.Thickness = math.clamp((maxPx or 20) / 9, 1.5, 3) st.Color = BLACK st.Parent = t
	return t
end
-- Check-UI brick: Depth (3D bottom bevel) + Face (gradient + damier); holder centre-anchored. opts.button: Face = TextButton
local function brick(parent, x, y, w, h, cols, z, opts)
	opts = opts or {}
	local holder = frame(parent, x, y, w, h, nil, z, opts.name)
	holder.BackgroundTransparency = 1
	centred(holder)
	local depth = frame(holder, 0, 0, 1, 1, cols[3], z, "Depth")
	depth.Position = UDim2.new(0, 0, 0, opts.bevelPx or 4)
	corner(depth, opts.r or 6)
	stroke(depth, opts.out or 3)
	local f
	if opts.button then
		f = Instance.new("TextButton") f.Text = "" f.AutoButtonColor = false f.BorderSizePixel = 0 f.Size = UDim2.fromScale(1, 1)
		f.ZIndex = z + 1 f.Parent = holder
	else
		f = frame(holder, 0, 0, 1, 1, WHITE, z + 1)
	end
	f.Name = "Face"
	f.BackgroundColor3 = WHITE
	corner(f, opts.r or 6)
	stroke(f, opts.out or 3)
	grad(f, cols[1], cols[2], 90)
	if opts.damier ~= false then damier(f, opts.damierCol or BLACK, opts.damierT or 0.9) end
	return holder, f
end
local function paint(holder, cols)
	holder.Face:FindFirstChildOfClass("UIGradient").Color = ColorSequence.new(cols[1], cols[2])
	holder.Depth.BackgroundColor3 = cols[3]
end
-- Check-UI micro-interaction: a UIScale on the holder (hover / press), times `base` (a selected card is 1.04);
-- `followers` = UIScales that move with it (a mythic card's rainbow ring + select frame)
local function interact(holder, button, hoverK)
	local sc = Instance.new("UIScale") sc.Parent = holder
	local st = {base = 1, over = false, down = false, followers = {}}
	local function apply(t, style)
		local s = st.base * (st.down and 0.94 or (st.over and (hoverK or 1.05) or 1))
		local info = TweenInfo.new(t, style or Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
		TweenService:Create(sc, info, {Scale = s}):Play()
		for _, f in st.followers do TweenService:Create(f, info, {Scale = s}):Play() end
	end
	button.MouseEnter:Connect(function() st.over = true apply(0.08) end)
	button.MouseLeave:Connect(function() st.over = false st.down = false apply(0.08) end)
	button.MouseButton1Down:Connect(function() st.down = true apply(0.05) end)
	button.MouseButton1Up:Connect(function() st.down = false apply(0.12, Enum.EasingStyle.Back) end)
	st.set = function(b) if b ~= st.base then st.base = b apply(0.12) end end
	st.scale = sc
	return st
end
local function upper(s) return (string.upper(s):gsub("\u{16B}", "\u{16A}")) end -- (Raijū's u-macron)
local function money(n) return "$" .. SpeedStat.Format(n) end
-- 0.015 -> "1.5%", 0.13 -> "13%", 0.001 -> "0.1%"
local function pctText(chance)
	local v = chance * 100
	if math.abs(v - math.floor(v + 0.5)) > 0.05 then return ("%.1f%%"):format(v) end
	return ("%d%%"):format(math.floor(v + 0.5))
end

---------------------------------------------------------------- page
local page = Instance.new("Frame")
page.Name = "IndexPage"
page.BackgroundTransparency = 1
page.AnchorPoint = Vector2.new(0.5, 0.5)
page.Position = UDim2.fromScale(0.5, 0.5)
page.Size = UDim2.fromOffset(891, DESIGN_H)
page.ZIndex = 5
page.Visible = false
page:SetAttribute("IndexV8", true)
page.Parent = body
local canvasScale = Instance.new("UIScale")
canvasScale.Name = "CanvasScale"
canvasScale.Parent = page

---------------------------------------------------------------- phone text floor (build review 1 M1, 2026-10-29)
-- One layout everywhere. On a small window (CanvasScale < PHONE_SCALE: phones) every label registered with phoneBox()
-- grows INSIDE its own box: its rect gets taller / wider around the SAME centre (the phone rect, in its container's
-- Scale) and its cap rises until the text is PHONE_PX on screen (about 9-10 px cap height) or runs out of room.
-- (build review 2: the UITextSizeConstraint works in SCREEN px under the UIScale, so on a phone the raised cap never
-- binds and the text is as big as its (trimmed, see the phone clearance) rect allows.)
-- Nothing moves; on PC every label keeps its v8 rect and cap.
local PHONE_SCALE, PHONE_PX = 0.75, 13
local phoneLabels = {} -- label -> {pcPos, pcSize, pcMax, phonePos, phoneSize}
local function isPhone() return canvasScale.Scale < PHONE_SCALE end
-- opts (build review 2): box = the GuiObject (or a function -> left, right, top, bottom on screen) whose edges the text
-- keeps CLEAR px from (default: the label's parent); vertical = also above / below the letters; gapL = a smaller gap on
-- the left (a chip's text next to its icon); keep = no trim (the count digit inside its round badge); padV = extra px
-- the ink is allowed above / below (a thick outline's anti-aliasing)
local function phoneBox(label, x, y, w, h, opts)
	opts = opts or {}
	phoneLabels[label] = {pcPos = label.Position, pcSize = label.Size, pcMax = label.UITextSizeConstraint.MaxTextSize,
		phonePos = UDim2.fromScale(x, y), phoneSize = UDim2.fromScale(w, h), box = opts.box, vertical = opts.vertical,
		gapL = opts.gapL, keep = opts.keep, padV = opts.padV}
end
-- the cap a label gets now (pcMax on PC; on a phone at least PHONE_PX on screen)
local function capOf(label, pcMax)
	if phoneLabels[label] and isPhone() then return math.max(pcMax, math.ceil(PHONE_PX / math.max(canvasScale.Scale, 0.05))) end
	return pcMax
end
local function setCap(label, pcMax)
	local e = phoneLabels[label]
	if e then e.pcMax = pcMax end
	label.UITextSizeConstraint.MaxTextSize = capOf(label, pcMax)
end
local function applyPhoneText()
	local phone = isPhone()
	page:SetAttribute("PhoneText", phone)
	for label, e in phoneLabels do
		label.Position = phone and e.phonePos or e.pcPos
		label.Size = phone and e.phoneSize or e.pcSize
		label.UITextSizeConstraint.MaxTextSize = capOf(label, e.pcMax)
	end
end

local function fitCanvas()
	local s = face.AbsoluteSize
	if s.X < 1 or s.Y < 1 then return end
	page.Size = UDim2.fromOffset(math.floor(DESIGN_H * s.X / s.Y + 0.5), DESIGN_H)
	canvasScale.Scale = s.Y / DESIGN_H
	applyPhoneText()
end
face:GetPropertyChangedSignal("AbsoluteSize"):Connect(fitCanvas)
fitCanvas()

---------------------------------------------------------------- creature portraits
-- Flat portraits (IndexConfig.PORTRAITS): no per-frame cost. Undiscovered = black silhouette. A creature without a
-- portrait falls back to a still 3D viewport.
-- PORTRAIT_CROP: the creature's box in its uploaded 512 px portrait (alpha bounding box + 6 px), so the pet fills its
-- slot like in the mockup (the new Glacier-update squares have wide margins). Measured 2026-10-28 in Studio: every
-- IndexConfig.PORTRAITS image drawn on magenta, box read from the screen capture (EditableImage reads are off in this
-- experience). A new or re-uploaded portrait without an entry shows the whole image (re-measure to add it).
local PORTRAIT_CROP = {
	AbyssWeaver = {11, 68, 500, 445}, AbyssalOrca = {11, 40, 498, 473}, BlackDragon = {19, 87, 492, 424},
	BlizzardRoc = {94, 104, 441, 462}, BrambleBadger = {85, 145, 402, 392}, CelestialDragon = {19, 58, 490, 454},
	Cerberus = {19, 83, 492, 426}, CinderOverlord = {92, 90, 362, 443}, CoralCrusher = {40, 107, 422, 454},
	CosmicLeviathan = {13, 104, 496, 407}, Cvetibara = {19, 40, 492, 471}, EclipseSeraph = {79, 100, 385, 445},
	ForestStag = {117, 17, 394, 492}, FrostcrownDragon = {72, 141, 387, 439}, FrostfangLynx = {83, 104, 379, 464},
	GlacierYeti = {79, 70, 443, 479}, Griffin = {83, 19, 428, 492}, HammerjawShark = {11, 64, 498, 447},
	IceMammoth = {45, 124, 402, 454}, InfernoPhoenix = {40, 13, 468, 498}, Ivonrath = {19, 77, 492, 436},
	Kappa = {94, 19, 417, 492}, Kraken = {19, 68, 492, 441}, LavaGolem = {64, 19, 447, 492},
	MoltenBoar = {19, 26, 492, 483}, MossbackTortoise = {19, 58, 492, 454}, NightmareStallion = {34, 19, 479, 492},
	PermafrostTitan = {98, 40, 441, 492}, PharaohAsparuh = {19, 21, 492, 488}, Raiju = {23, 19, 488, 492},
	SeaTurtleWarrior = {102, 19, 411, 492}, ShadePanther = {19, 98, 490, 411}, SolarLion = {30, 19, 483, 492},
	StormWyvern = {19, 28, 492, 486}, ThornbladeMantis = {58, 11, 454, 496}, ThunderBull = {19, 55, 492, 456},
	ThunderRex = {13, 17, 498, 494}, Thunderbird = {30, 13, 481, 496}, Treant = {85, 19, 426, 492},
	VenomBasilisk = {11, 51, 494, 460}, VoltRhino = {70, 115, 402, 407}, WraithHound = {58, 109, 387, 432},
}
local shown = {} -- image -> {name, silhouette}
local function fallbackViewport(img, name)
	local vp = img:FindFirstChild("Fallback")
	if not vp then
		vp = Instance.new("ViewportFrame")
		vp.Name = "Fallback"
		vp.BackgroundTransparency = 1
		vp.Size = UDim2.fromScale(1, 1)
		vp.Ambient = C(170, 170, 180)
		vp.LightColor = C(255, 250, 240)
		vp.LightDirection = Vector3.new(-0.4, -1, -0.6)
		vp.ZIndex = img.ZIndex
		vp.Parent = img
	end
	vp:ClearAllChildren()
	local cam = Instance.new("Camera")
	cam.FieldOfView = 30
	cam.Parent = vp
	vp.CurrentCamera = cam
	local src = MODELS:FindFirstChild(name)
	if not src then return vp end
	local m = src:Clone()
	for _, d in m:GetDescendants() do if d:IsA("Script") or d:IsA("LocalScript") then d:Destroy() end end
	m.Parent = vp
	local cf, size = m:GetBoundingBox()
	local dist = size.Magnitude / 2 / math.sin(math.rad(15)) * 0.74
	local dir = Vector3.new(0.5, 0, 0.866) -- three-quarter view like the portraits
	cam.CFrame = CFrame.lookAt(cf.Position + dir * dist + Vector3.new(0, size.Y * 0.15, 0), cf.Position)
	return vp
end
local function setModel(img, name, silhouette)
	local t = shown[img]
	if t and t.name == name and t.silhouette == silhouette then return end
	shown[img] = {name = name, silhouette = silhouette}
	local id = IndexConfig.PORTRAITS and IndexConfig.PORTRAITS[name]
	local tint = silhouette and BLACK or WHITE
	local fade = silhouette and 0.15 or 0
	local vp = img:FindFirstChild("Fallback")
	if id then
		img.Image = id
		local crop = PORTRAIT_CROP[name]
		img.ImageRectOffset = crop and Vector2.new(crop[1], crop[2]) or Vector2.zero
		img.ImageRectSize = crop and Vector2.new(crop[3] - crop[1], crop[4] - crop[2]) or Vector2.zero
		img.ImageColor3 = tint
		img.ImageTransparency = fade
		if vp then vp.Visible = false end
	else
		img.Image = ""
		vp = fallbackViewport(img, name)
		vp.Visible = true
		vp.ImageColor3 = tint
		vp.ImageTransparency = fade
	end
	-- little pop when the picture changes
	local sc = img:FindFirstChildOfClass("UIScale")
	sc.Scale = 0.86
	TweenService:Create(sc, TweenInfo.new(0.35, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {Scale = 1}):Play()
end
local function portrait(parent, name, x, y, w, h, z)
	local img = Instance.new("ImageLabel")
	img.Name = name
	img.BackgroundTransparency = 1
	img.Position, img.Size = UDim2.fromScale(x, y), UDim2.fromScale(w, h)
	centred(img)
	img.ScaleType = Enum.ScaleType.Fit
	img.ZIndex = z
	img.Parent = parent
	Instance.new("UIScale").Parent = img
	return img
end

local selectArea, selectCard, refresh -- (below)

---------------------------------------------------------------- left: area tabs (column 0.167 .. 0.986)
local TAB_TOP, TAB_SPAN, TAB_GAP = 0.167, 0.819, 0.019
local TAB_H = (TAB_SPAN - (#IndexConfig.AREAS - 1) * TAB_GAP) / #IndexConfig.AREAS -- 7 tabs: 0.1007, pitch 0.1197
local tabs = {}
for i, a in IndexConfig.AREAS do
	local holder, f = brick(page, 0.012, TAB_TOP + (i - 1) * (TAB_H + TAB_GAP), 0.118, TAB_H, tabColors(i), 6,
		{bevelPx = 3, button = true, name = "Tab" .. i})
	text(f, upper(a.name), 0.08, 0.12, 0.78, 0.44, WHITE, 20, 9, nil, "AreaName")
	local prog = text(f, "", 0.25, 0.6, 0.5, 0.28, WHITE, 14, 9, nil, "Prog")
	-- corner badges (review 5 NICE: the ! clears the last letter of GLACIER; 2 px was still touching the R in Studio,
	-- so 4 px right + 4 px up, in the page's design px)
	local star = Instance.new("ImageLabel")
	star.Name = "Star" star.BackgroundTransparency = 1 star.Image = STAR_ICON star.ScaleType = Enum.ScaleType.Fit
	star.AnchorPoint = Vector2.new(0.5, 0.5) star.Position = UDim2.new(0.885, 4, 0.06, -4) star.Size = UDim2.fromScale(0.2, 0.42)
	star.ZIndex = 14 star.Parent = holder
	aspect(star)
	local bang = frame(holder, 0, 0, 0.17, 0.36, C(235, 45, 45), 14, "Ready")
	bang.AnchorPoint = Vector2.new(0.5, 0.5) bang.Position = UDim2.new(0.885, 4, 0.06, -4)
	corner(bang, 100)
	stroke(bang, 2, BLACK)
	aspect(bang)
	text(bang, "!", 0, 0.08, 1, 0.84, WHITE, 18, 15, nil, "T")
	local it = interact(holder, f, 1.03)
	tabs[i] = {holder = holder, face = f, prog = prog, star = star, bang = bang, stroke = f:FindFirstChildOfClass("UIStroke"), base = holder.Position, it = it}
	f.Activated:Connect(function() selectArea(i) end)
end

---------------------------------------------------------------- centre: area header (0.167 .. 0.256)
local headH, headF = brick(page, 0.148, 0.167, 0.568, 0.089, {WHITE, WHITE, WHITE}, 6, {damierT = 0.88, name = "Header"})
-- (build review 1 N3: title + subtitle back at the v8 size; the 0.44 / 0.3 boxes came out one text size smaller)
local hName = text(headF, "", 0.03, 0.085, 0.47, 0.47, WHITE, 22, 9, Enum.TextXAlignment.Left, "Area")
local hSub = text(headF, "", 0.03, 0.545, 0.47, 0.33, WHITE, 15, 9, Enum.TextXAlignment.Left, "Sub")
local bar = frame(headF, 0.52, 0.26, 0.28, 0.48, TROUGH, 9, "Bar")
corner(bar, 8)
stroke(bar, 2, TROUGH_EDGE)
local barFill = frame(bar, 0, 0, 1, 1, WHITE, 9, "Fill")
corner(barFill, 8)
grad(barFill, LIME[1], LIME[2], 90)
local barText = text(bar, "", 0, 0.1, 1, 0.8, WHITE, 16, 10, nil, "Text")
local pipH, pipF = brick(headF, 0.815, 0.2, 0.16, 0.58, GOLD, 9, {bevelPx = 3, out = 2, name = "Bonus"})
local pipText = text(pipF, "", 0.05, 0.1, 0.9, 0.8, WHITE, 15, 12, nil, "Text")

---------------------------------------------------------------- centre: creature cards (grid 0.264 .. 0.792)
local grid = frame(page, 0.148, 0.264, 0.568, 0.528, PANEL, 5, "Grid")
corner(grid, 6)
stroke(grid, 3)
do
	local gh = frame(grid, 0, 0, 1, 1, PANEL, 5, "Highlight")
	gh.BackgroundTransparency = 1
	corner(gh, 6)
	stroke(gh, 1.2, HIGH).Transparency = 0.4
end
local MAX_CARDS = 0
for i in IndexConfig.AREAS do MAX_CARDS = math.max(MAX_CARDS, #IndexConfig.creatures(i)) end
local ROWS = math.max(2, math.ceil(MAX_CARDS / 3))
local CARD_W, CARD_GAP_X, CARD_GAP_Y = 0.1733, 0.012, 0.016
local CARD_H = (0.506 - (ROWS - 1) * CARD_GAP_Y) / ROWS -- 2 rows: 0.245 (the mockup)
local function cardRect(slot)
	local col, row = (slot - 1) % 3, math.floor((slot - 1) / 3)
	return 0.160 + col * (CARD_W + CARD_GAP_X), 0.274 + row * (CARD_H + CARD_GAP_Y), CARD_W, CARD_H
end
local cards = {}
for slot = 1, MAX_CARDS do
	local x, y, w, h = cardRect(slot)
	-- a selected MYTHIC: white select frame outside its rainbow ring (mock_74213)
	local sel = frame(page, x, y, w, h, WHITE, 6, "Select" .. slot)
	sel.Size = UDim2.new(w, 10, h, 10) sel.Position = UDim2.new(x, -5, y, -5)
	corner(sel, 10)
	centred(sel)
	local selScale = Instance.new("UIScale") selScale.Parent = sel
	local ring = frame(page, x, y, w, h, WHITE, 7, "Ring" .. slot)
	ring.Size = UDim2.new(w, 4, h, 4) ring.Position = UDim2.new(x, -2, y, -2)
	corner(ring, 8)
	grad(ring, RAINBOW, nil, 45)
	centred(ring)
	local ringScale = Instance.new("UIScale") ringScale.Parent = ring
	local holder, f = brick(page, x, y, w, h, {WHITE, WHITE, WHITE}, 8, {button = true, name = "Card" .. slot})
	local hl = frame(f, 0, 0, 1, 1, WHITE, 9, "SecretHighlight") -- the gold card's pale inner rim
	hl.BackgroundTransparency = 1 hl.Size = UDim2.new(1, -4, 1, -4) hl.Position = UDim2.fromOffset(2, 2)
	corner(hl, 5)
	stroke(hl, 1.2, C(255, 250, 210)).Transparency = 0.4
	local disc = frame(f, 0.5, 0.56, 0.5, 0.66, WHITE, 9, "MythicDisc")
	disc.AnchorPoint = Vector2.new(0.5, 0.5) disc.BackgroundTransparency = 0.9
	corner(disc, 100)
	aspect(disc)
	local name = text(f, "", 0.04, 0.11, 0.92, 0.12, WHITE, 14, 12, nil, "PetName")
	local img = portrait(f, "View", 0.1, 0.22, 0.8, 0.68, 10)
	local q = text(f, "?", 0.3, 0.34, 0.4, 0.4, WHITE, 48, 11, nil, "Q")
	q.TextTransparency = 0.25
	local _, pillF = brick(f, 0.22, 0.83, 0.56, 0.12, PILL, 12, {bevelPx = 2, out = 2, damier = false, r = 10, name = "Chance"})
	local pillText = text(pillF, "", 0.05, 0.1, 0.9, 0.8, WHITE, 13, 15, nil, "Text")
	local secret = brick(holder, 0.24, -0.03, 0.52, 0.13, PINK, 14, {bevelPx = 2, out = 2, damier = false, r = 8, name = "Secret"})
	text(secret.Face, "SECRET", 0.05, 0.08, 0.9, 0.84, WHITE, 12, 16, nil, "T")
	local edge = frame(holder, 0.24, -0.03, 0.52, 0.13, WHITE, 14, "MythicEdge")
	edge.Size = UDim2.new(0.52, 4, 0.13, 4) edge.Position = UDim2.new(0.24, -2, -0.03, -2)
	corner(edge, 10)
	grad(edge, RAINBOW, nil, 0)
	local rib = frame(holder, 0.24, -0.03, 0.52, 0.13, MYTHIC_INK, 15, "Mythic")
	corner(rib, 8)
	text(rib, "MYTHIC", 0.05, 0.08, 0.9, 0.84, WHITE, 12, 16, nil, "T")
	local it = interact(holder, f, 1.03)
	cards[slot] = {holder = holder, face = f, sel = sel, ring = ring, hl = hl, disc = disc, name = name, img = img, q = q,
		pillText = pillText, secret = secret, edge = edge, rib = rib, it = it, selScale = selScale, ringScale = ringScale,
		faceStroke = f:FindFirstChildOfClass("UIStroke"), depthStroke = holder.Depth:FindFirstChildOfClass("UIStroke"), damier = f.Damier}
	f.Activated:Connect(function() selectCard(slot) end)
end

---------------------------------------------------------------- centre: area reward strip (0.800 .. 0.880)
local reward = frame(page, 0.148, 0.8, 0.568, 0.08, PANEL, 6, "Reward")
corner(reward, 6)
stroke(reward, 3)
do
	local rh = frame(reward, 0, 0, 1, 1, PANEL, 6, "Highlight")
	rh.BackgroundTransparency = 1
	corner(rh, 6)
	stroke(rh, 2, HIGH).Transparency = 0.4
end
local rTitle = text(reward, "", 0.02, 0.1, 0.22, 0.8, GOLD_TEXT, 15, 9, Enum.TextXAlignment.Left, "Title")
local function chip(i, name, icon)
	local c = frame(reward, 0.255 + (i - 1) * 0.132, 0.17, 0.12, 0.66, PANEL, 8, name)
	corner(c, 6)
	stroke(c, 2, BLACK)
	local hl = frame(c, 0, 0, 1, 1, PANEL, 8, "Highlight")
	hl.BackgroundTransparency = 1
	corner(hl, 6)
	stroke(hl, 1.5, HIGH).Transparency = 0.3
	local im = Instance.new("ImageLabel") im.Name = "Icon" im.BackgroundTransparency = 1 im.Image = icon im.ScaleType = Enum.ScaleType.Fit
	im.Position = UDim2.fromScale(0.04, 0.12) im.Size = UDim2.fromScale(0.42, 0.76) im.ZIndex = 9 im.Parent = c
	return text(c, "", 0.46, 0.2, 0.5, 0.6, WHITE, 15, 10, nil, "T")
end
local rMoney = chip(1, "Money", MONEY_ICON)
local rSpeed = chip(2, "Speed", SPEED_ICON)
local rPotMoney = chip(3, "PotionMoney", PotionConfig.byKey.Money.icon)
local rPotHatch = chip(4, "PotionHatch", PotionConfig.byKey.Hatch.icon)
local CHIPS = {rMoney, rSpeed, rPotMoney, rPotHatch}
-- all chips use the smallest of their fitted text sizes so they read as one row
local evenQueued = false
local function evenChips()
	if evenQueued then return end
	evenQueued = true
	for _, t in CHIPS do t.UITextSizeConstraint.MaxTextSize = capOf(t, 15) end
	task.defer(function()
		evenQueued = false
		local s = math.huge
		for _, t in CHIPS do
			-- (build review 2, measured in Studio) under the page's UIScale BOTH TextBounds and the UITextSizeConstraint are in
			-- screen px, so this / CanvasScale only evens the chips on PC (scale ~0.99). On a phone "+5%" stays as small as its
			-- width allows while "x1" reaches ~11 px; left as is for the owner (evening them would shrink "x1" to "+5%")
			if t.Parent.Visible and t.TextBounds.Y > 0 then s = math.min(s, t.TextBounds.Y / math.max(canvasScale.Scale, 0.01)) end
		end
		if s == math.huge then return end
		for _, t in CHIPS do t.UITextSizeConstraint.MaxTextSize = math.max(1, math.floor(s)) end
	end)
end
local claimH, claimF = brick(reward, 0.795, 0.14, 0.19, 0.66, LIME, 8, {bevelPx = 3, button = true, name = "Claim"})
local claimLabel = text(claimF, "CLAIM!", 0.05, 0.12, 0.9, 0.76, WHITE, 20, 12, nil, "Label")
local claimIt = interact(claimH, claimF)

---------------------------------------------------------------- bottom: DISCOVERED x / N + CLAIM ALL (0.890 .. 0.986)
local total = frame(page, 0.148, 0.89, 0.568, 0.096, PANEL, 6, "Total")
corner(total, 6)
stroke(total, 3)
do
	local book = Instance.new("ImageLabel") book.Name = "Book" book.BackgroundTransparency = 1 book.Image = BOOK_ICON book.ScaleType = Enum.ScaleType.Fit
	book.AnchorPoint = Vector2.new(0.5, 0.5) book.Position = UDim2.fromScale(0.052, 0.5) book.Size = UDim2.fromScale(0.088, 0.82)
	book.ZIndex = 9 book.Parent = total
end
local tBar = frame(total, 0.118, 0.26, 0.6, 0.48, TROUGH, 8, "Bar")
corner(tBar, 10)
stroke(tBar, 2, TROUGH_EDGE)
local tFill = frame(tBar, 0, 0, 0.5, 1, WHITE, 8, "Fill")
corner(tFill, 10)
grad(tFill, C(120, 200, 255), C(60, 140, 230), 90) -- (mock_74213: blue trough, CLAIM ALL is the footer's only warm button)
local tText = text(tBar, "", 0.04, 0.12, 0.92, 0.76, WHITE, 18, 10, nil, "Text")
local allH, allF = brick(total, 0.745, 0.2, 0.235, 0.56, CLAIM_ALL, 8, {bevelPx = 3, button = true, name = "ClaimAll"})
local allLabel = text(allF, "CLAIM ALL", 0.06, 0.16, 0.88, 0.68, WHITE, 16, 12, nil, "Label")
allLabel.UIStroke.Thickness = 3 -- (review 5 M1: white label, 3 px black stroke)
local allCount = frame(allH, 0, 0, 0.2, 0.62, WHITE, 16, "Count")
allCount.AnchorPoint = Vector2.new(0.5, 0.5) allCount.Position = UDim2.fromScale(0.97, 0.05)
corner(allCount, 100)
stroke(allCount, 2, BLACK)
aspect(allCount)
local allCountText = text(allCount, "", 0, 0.08, 1, 0.84, C(20, 20, 20), 16, 17, nil, "T")
allCountText.UIStroke.Enabled = false
local allIt = interact(allH, allF)

---------------------------------------------------------------- right: inspect panel (0.167 .. 0.986)
local insp = frame(page, 0.73, 0.167, 0.258, 0.819, PANEL, 6, "Inspect")
corner(insp, 6)
stroke(insp, 3)
do
	local ih = frame(insp, 0, 0, 1, 1, PANEL, 6, "Highlight")
	ih.BackgroundTransparency = 1
	corner(ih, 6)
	stroke(ih, 2, HIGH).Transparency = 0.4
	damier(insp, BLACK, 0.92)
end
local iRing = frame(insp, 0.5, 0.235, 0, 0, WHITE, 7, "Ring")
iRing.AnchorPoint = Vector2.new(0.5, 0.5) iRing.Size = UDim2.new(0.73, 6, 0.73, 6)
corner(iRing, 1000)
aspect(iRing)
local iRingGrad = grad(iRing, RAINBOW, nil, 45)
local iDisc = frame(insp, 0.5, 0.235, 0.73, 0.73, WHITE, 8, "Disc")
iDisc.AnchorPoint = Vector2.new(0.5, 0.5)
corner(iDisc, 1000)
aspect(iDisc)
local iDiscGrad = grad(iDisc, MYTHIC_DISC[1], MYTHIC_DISC[2], 90)
local bigImg = portrait(insp, "View", 0.0952, 0.046, 0.8096, 0.368, 9) -- (the mockup's stage at 0.92)
local iName = text(insp, "", 0.04, 0.452, 0.92, 0.065, WHITE, 18, 10, nil, "PetName")
local iEdge = frame(insp, 0.08, 0.527, 0.84, 0.058, WHITE, 8, "RarityEdge")
corner(iEdge, 10)
grad(iEdge, RAINBOW, nil, 0)
local iPill = frame(insp, 0.088, 0.531, 0.824, 0.05, MYTHIC_INK, 9, "Rarity")
corner(iPill, 9)
local iPillStroke = stroke(iPill, 2, BLACK)
local iPillText = text(iPill, "", 0.04, 0.12, 0.92, 0.76, WHITE, 14, 10, nil, "Text")
local STAT_LABELS = {"Income (best KG)", "Best weight", "Hatched", "Hatch chance"}
local stats = {}
for k = 1, 4 do
	local row = frame(insp, 0.058, 0.62 + (k - 1) * 0.088, 0.884, 0.074, ROW, 8, "Stat" .. k)
	corner(row, 8)
	stroke(row, 2, TROUGH_EDGE)
	local l = text(row, STAT_LABELS[k], 0.04, 0.26, 0.5, 0.48, LABEL, 13, 10, Enum.TextXAlignment.Left, "L")
	local v = text(row, "", 0.56, 0.22, 0.4, 0.56, WHITE, 16, 10, Enum.TextXAlignment.Right, "V")
	stats[k] = {l = l, v = v}
end

---------------------------------------------------------------- phone boxes (M1): {x, y, w, h} in the label's container
-- Scale, same centre as the PC rect (left / right-aligned labels keep their edge), never past a neighbour
-- (build review 2 MUST 1) CLEAR = the screen px a phone label's text (black outline included) keeps from its box's
-- edges; CAP_H = GothamBlack's letter height / text size (the ink inside the line)
local CLEAR, CAP_H = 3, 0.72
local function outlinePx(label)
	local st = label:FindFirstChildOfClass("UIStroke")
	return (st and st.Enabled) and st.Thickness * canvasScale.Scale or 0
end
local function edges(box)
	if typeof(box) == "function" then return box() end
	local p, s = box.AbsolutePosition, box.AbsoluteSize
	return p.X, p.X + s.X, p.Y, p.Y + s.Y
end
for _, t in tabs do
	phoneBox(t.face.AreaName, 0.04, 0.12, 0.86, 0.44)
	phoneBox(t.prog, 0.2, 0.56, 0.6, 0.36)
end
-- (the header's title + subtitle end at the progress bar)
local function headBox()
	local p, s = headF.AbsolutePosition, headF.AbsoluteSize
	return p.X, bar.AbsolutePosition.X, p.Y, p.Y + s.Y
end
phoneBox(hName, 0.03, 0.07, 0.48, 0.5, {box = headBox})
phoneBox(hSub, 0.03, 0.555, 0.48, 0.33, {box = headBox})
phoneBox(barText, 0, 0.02, 1, 0.96)
phoneBox(pipText, 0.03, 0.02, 0.94, 0.96)
for _, card in cards do
	phoneBox(card.name, 0.035, 0.095, 0.93, 0.15)
	phoneBox(card.pillText, 0.03, 0.02, 0.94, 0.96)
	phoneBox(card.secret.Face.T, 0.03, 0.02, 0.94, 0.96)
	phoneBox(card.rib.T, 0.03, 0.02, 0.94, 0.96)
end
-- (the strip's title ends at the first chip)
phoneBox(rTitle, 0.015, 0.03, 0.23, 0.94, {box = function()
	local p, c = reward.AbsolutePosition, rMoney.Parent.AbsolutePosition
	return p.X, c.X, p.Y, p.Y + reward.AbsoluteSize.Y
end})
for _, t in CHIPS do
	-- the chip is the box; on the left the text only has to clear the icon's picture (Fit: a square in the icon's rect)
	phoneBox(t, 0.45, 0.08, 0.52, 0.84, {gapL = 1, box = function()
		local c, icon = t.Parent, t.Parent.Icon
		local ip, is = icon.AbsolutePosition, icon.AbsoluteSize
		local cp, cs = c.AbsolutePosition, c.AbsoluteSize
		return ip.X + (is.X + math.min(is.X, is.Y)) / 2, cp.X + cs.X, cp.Y, cp.Y + cs.Y
	end})
end
phoneBox(claimLabel, 0.03, 0.04, 0.94, 0.92, {vertical = true})
phoneBox(tText, 0.03, 0.04, 0.94, 0.92)
-- (padV: the 3 px outline's anti-aliasing on the orange shows ~1 px above the letters; measured on a 299 px window's
-- pixels: 9 px text = 2 px clear above, 8 px text = 4 above / 3 below)
phoneBox(allLabel, 0.04, 0.06, 0.92, 0.88, {vertical = true, padV = 0.5})
phoneBox(allCountText, 0, 0.02, 1, 0.96, {keep = true})
phoneBox(iName, 0.03, 0.452, 0.94, 0.065)
phoneBox(iPillText, 0.03, 0.04, 0.94, 0.92)
local statL = {}
for _, s in stats do
	-- a stat label may use the row's width the right-aligned value leaves free: its box ends at the value's text
	-- (height a little under the value's 0.72: the value stays the bigger text, as on PC)
	phoneBox(s.l, 0.035, 0.19, 0.75, 0.62, {box = function()
		local row, v = s.l.Parent, s.v
		local rp, rs = row.AbsolutePosition, row.AbsoluteSize
		return rp.X, v.AbsolutePosition.X + v.AbsoluteSize.X - v.TextBounds.X - outlinePx(v), rp.Y, rp.Y + rs.Y
	end})
	phoneBox(s.v, 0.56, 0.14, 0.41, 0.72)
	statL[s.l] = true
end
-- (build review 2 MUST 1) the floor must not push a label past its box: on a phone every grown label's rect is trimmed
-- to CLEAR px inside its box's left / right edges (outline included; `vertical`: the letters' ink also CLEAR px under
-- the top and over the bottom). TextScaled then fits the text, a step smaller where needed. Boxes and PC stay as they
-- are. The stat labels go last: their box ends at the value's text.
local function shownIn(g)
	while g and g ~= page do
		if g:IsA("GuiObject") and not g.Visible then return false end
		g = g.Parent
	end
	return g == page
end
-- a label's text on screen, outline included: left, right, ink top, ink bottom (one line: CAP_H of the size)
local function inkOf(label)
	local o = outlinePx(label)
	local ap, as, tb = label.AbsolutePosition, label.AbsoluteSize, label.TextBounds
	local al = label.TextXAlignment
	local tx = al == Enum.TextXAlignment.Left and ap.X or al == Enum.TextXAlignment.Right and ap.X + as.X - tb.X or ap.X + (as.X - tb.X) / 2
	local cy = ap.Y + as.Y / 2
	return tx - o, tx + tb.X + o, cy - CAP_H * tb.Y / 2 - o, cy + CAP_H * tb.Y / 2 + o
end
-- screen px between the text and its box: left, right (+ top, bottom for `vertical` labels)
local function clearOf(label, e)
	local l, r, t, b = edges(e.box or label.Parent)
	local x0, x1, y0, y1 = inkOf(label)
	local pv = e.padV or 0
	return x0 - l, r - x1, e.vertical and y0 - pv - t or nil, e.vertical and b - (y1 + pv) or nil
end
local function clearLabel(label, e)
	if e.keep then return end
	local par = label.Parent
	local pp, ps = par.AbsolutePosition, par.AbsoluteSize
	if ps.X < 1 or ps.Y < 1 then return end
	local o = outlinePx(label)
	local l, r, t, b = edges(e.box or par)
	local x0 = pp.X + e.phonePos.X.Scale * ps.X
	local x1 = x0 + e.phoneSize.X.Scale * ps.X
	local y0 = pp.Y + e.phonePos.Y.Scale * ps.Y
	local y1 = y0 + e.phoneSize.Y.Scale * ps.Y
	x0 = math.max(x0, l + (e.gapL or CLEAR) + o) + (e.trimL or 0)
	x1 = math.min(x1, r - CLEAR - o) - (e.trimR or 0)
	if e.vertical then
		local cy = (y0 + y1) / 2
		local h = math.min(y1 - y0, (b - t - 2 * (CLEAR + o + (e.padV or 0))) / CAP_H) - 2 * (e.trimV or 0)
		y0, y1 = cy - h / 2, cy + h / 2
	end
	if x1 - x0 < 2 or y1 - y0 < 2 then return end
	label.Position = UDim2.fromScale((x0 - pp.X) / ps.X, (y0 - pp.Y) / ps.Y)
	label.Size = UDim2.fromScale((x1 - x0) / ps.X, (y1 - y0) / ps.Y)
end
-- TextScaled can still draw a few tenths of a px past its rect: measure the shown labels and trim them again (the trims
-- stay until the window size changes)
local function settleClear()
	for _ = 1, 3 do
		local again = false
		for label, e in phoneLabels do
			if not e.keep and label.ContentText ~= "" and shownIn(label) then
				local cl, cr, ct, cb = clearOf(label, e)
				local d = math.max((e.gapL or CLEAR) - cl, CLEAR - cr, 0)
				local dv = math.max(ct and CLEAR - ct or 0, cb and CLEAR - cb or 0, 0)
				if d > 0.02 or dv > 0.02 then
					local al = label.TextXAlignment
					if d > 0.02 then
						d += 0.1
						if al ~= Enum.TextXAlignment.Left then e.trimL = (e.trimL or 0) + d end
						if al ~= Enum.TextXAlignment.Right then e.trimR = (e.trimR or 0) + d end
					end
					if dv > 0.02 then e.trimV = (e.trimV or 0) + dv + 0.1 end
					clearLabel(label, e)
					again = true
				end
			end
		end
		if not again then return end
		task.wait()
		if not isPhone() then return end
	end
end
local clearRunning, clearAgain = false, false
local function fitStatLabels() -- (refresh calls it after the values change; trims every phone label)
	if not isPhone() then return end
	if clearRunning then clearAgain = true return end
	clearRunning = true
	task.defer(function()
		repeat
			clearAgain = false
			local ok, err = pcall(function()
				if not isPhone() then return end
				for label, e in phoneLabels do if not statL[label] then clearLabel(label, e) end end
				task.wait() -- (the values' TextBounds at their trimmed rects)
				if not isPhone() then return end
				for label in statL do clearLabel(label, phoneLabels[label]) end
				task.wait()
				if not isPhone() then return end
				settleClear()
			end)
			if not ok then warn("[IndexClientLegacy] phone clearance: " .. tostring(err)) end
		until not clearAgain
		clearRunning = false
		page:SetAttribute("PhoneClearN", (page:GetAttribute("PhoneClearN") or 0) + 1)
		evenChips()
	end)
end
-- (build review 2) the CLAIM ALL count badge sits BADGE_NUDGE screen px further up / right on a phone: clear of the "L"
local BADGE_NUDGE = 2.5
local applyPhoneTextBase = applyPhoneText
applyPhoneText = function()
	applyPhoneTextBase()
	for _, e in phoneLabels do e.trimL, e.trimR, e.trimV = nil, nil, nil end
	local s = math.max(canvasScale.Scale, 0.05)
	allCount.Position = isPhone() and UDim2.new(0.97, BADGE_NUDGE / s, 0.05, -BADGE_NUDGE / s) or UDim2.fromScale(0.97, 0.05)
	fitStatLabels()
end
applyPhoneText()
-- (tests + build notes) every shown phone label's clearance in screen px: its text (outline included) to its box's
-- left / right edges, for `vertical` labels the letters' ink to the top / bottom; plus the CLAIM ALL count badge's
-- gap to the CLAIM ALL letters (negative = overlap)
local phoneClear = Instance.new("BindableFunction")
phoneClear.Name = "PhoneClear"
phoneClear.Parent = page
phoneClear.OnInvoke = function()
	local out = {}
	for label, e in phoneLabels do
		if label.ContentText ~= "" and shownIn(label) then
			local o = outlinePx(label)
			local cl, cr, ct, cb = clearOf(label, e)
			local lines = select(2, label.ContentText:gsub("\n", "")) + 1
			table.insert(out, {path = label:GetFullName():match("IndexPage%.(.+)$") or label.Name, text = label.ContentText,
				keep = e.keep == true, gapL = e.gapL, left = cl, right = cr, top = ct, bottom = cb,
				cap = CAP_H * label.TextBounds.Y / lines + 2 * o})
		end
	end
	if shownIn(allCount) and shownIn(allLabel) then
		local cp, cs = allCount.AbsolutePosition, allCount.AbsoluteSize
		local rad = cs.X / 2 + 2 * canvasScale.Scale -- (its 2 px black ring)
		local cx, cy = cp.X + cs.X / 2, cp.Y + cs.Y / 2
		local x0, x1, y0, y1 = inkOf(allLabel)
		local dx, dy = math.max(x0 - cx, 0, cx - x1), math.max(y0 - cy, 0, cy - y1)
		table.insert(out, {path = "Total.ClaimAll.Count badge vs the CLAIM ALL letters", text = allCountText.ContentText,
			badgeGap = math.sqrt(dx * dx + dy * dy) - rad})
	end
	return out
end

---------------------------------------------------------------- refresh
local function claimable()
	local n = 0
	for i in IndexConfig.AREAS do
		if IndexConfig.areaComplete(data, i) and not IndexConfig.isClaimed(data, i) then n += 1 end
	end
	return n
end
local function kind(c) return c.mythic and "mythic" or c.secret and "secret" or "normal" end
local refreshN = 0

function refresh()
	refreshN += 1
	page:SetAttribute("IndexRefreshN", refreshN)
	local area = IndexConfig.AREAS[areaSel]
	local list = IndexConfig.creatures(areaSel)
	local tabCol = tabColors(areaSel)
	-- tabs
	for i, t in tabs do
		local cl = IndexConfig.creatures(i)
		local found = 0
		for _, c in cl do if data.found[c.name] then found += 1 end end
		t.prog.Text = found .. "/" .. #cl
		local done = IndexConfig.areaComplete(data, i)
		local claimed = IndexConfig.isClaimed(data, i)
		t.star.Visible = done and claimed
		t.bang.Visible = done and not claimed
		local on = i == areaSel
		t.holder.Position = on and t.base + UDim2.fromScale(0.006, 0) or t.base
		t.stroke.Color = on and WHITE or OUT
		t.stroke.Thickness = on and 3.5 or 3
	end
	-- header: the cards the claim needs (mythics are a BONUS pip)
	paint(headH, {area.colors[1], area.colors[2], tabCol[3]})
	hName.Text = upper(area.name) .. " CREATURES"
	hSub.Text = "Hatched from the <font color='#FFF3A0'>" .. IndexConfig.eggName(area.egg) .. "</font>"
	local need, needFound, bonus, bonusFound = 0, 0, 0, 0
	for _, c in list do
		local got = data.found[c.name] ~= nil
		if c.mythic then
			bonus += 1
			if got then bonusFound += 1 end
		else
			need += 1
			if got then needFound += 1 end
		end
	end
	barText.Text = needFound .. " / " .. need
	local frac = needFound / math.max(need, 1)
	barFill.Visible = frac > 0
	TweenService:Create(barFill, TweenInfo.new(0.35, Enum.EasingStyle.Quad), {Size = UDim2.fromScale(math.max(frac, 0.06), 1)}):Play()
	pipH.Visible = bonus > 0
	pipText.Text = "BONUS " .. bonusFound .. "/" .. bonus
	bar.Size = UDim2.fromScale(bonus > 0 and 0.28 or 0.455, 0.48)
	-- default selection: the first discovered creature, else the first
	if not creatureSel or not list[creatureSel] then
		creatureSel = 1
		for i, c in list do if data.found[c.name] then creatureSel = i break end end
	end
	-- cards
	local odds = CreatureConfig.odds(area.egg, 1)
	local normal = cardColors(areaSel)
	for slot, card in cards do
		local c = list[slot]
		card.holder.Visible = c ~= nil
		local k = c and kind(c)
		local on = c ~= nil and slot == creatureSel
		card.ring.Visible = k == "mythic"
		card.sel.Visible = k == "mythic" and on
		if c then
			local known = data.found[c.name] ~= nil
			local cols = k == "mythic" and MYTHIC_CARD or k == "secret" and GOLD or normal
			paint(card.holder, known and cols or dimmed(cols))
			local mythic = k == "mythic"
			card.faceStroke.Enabled = not mythic
			card.depthStroke.Enabled = not mythic
			card.holder.Depth.BackgroundTransparency = mythic and 1 or 0
			card.damier.ImageColor3 = mythic and WHITE or BLACK
			card.damier.ImageTransparency = mythic and 0.93 or 0.9
			card.hl.Visible = k == "secret"
			card.disc.Visible = mythic
			card.secret.Visible = k == "secret"
			card.edge.Visible = mythic
			card.rib.Visible = mythic
			local display = known and upper(c.display) or "???"
			card.name.Text = display
			-- (review 5) a long name (over 14 letters) gets 0.09 of the card height: margin on both sides
			setCap(card.name, (utf8.len(display) or #display) > 14 and 12 or 14)
			setModel(card.img, c.name, not known)
			card.q.Visible = false -- (build review 1 N5: one "?" per silhouette = the ??? name plate)
			card.pillText.Text = pctText(odds[slot] or 0)
			if not mythic then
				card.faceStroke.Color = on and WHITE or OUT
				card.faceStroke.Thickness = on and 3.5 or 3
			end
			card.it.set(on and 1.04 or 1)
			card.selScale.Scale = on and 1.04 or 1
			card.ringScale.Scale = on and 1.04 or 1
			card.it.followers = mythic and {card.ringScale, card.selScale} or {}
		end
	end
	-- inspect
	local c = list[creatureSel]
	if c then
		local e = data.found[c.name]
		local known = e ~= nil
		local k = kind(c)
		local info = CreatureConfig.byName[c.name]
		setModel(bigImg, c.name, not known)
		iName.Text = known and upper(c.display) or "???"
		-- ring + disc: rainbow / gold / the area's light ice; undiscovered = a grey disc
		iRingGrad.Enabled = k == "mythic"
		iRing.BackgroundColor3 = k == "mythic" and WHITE or k == "secret" and SECRET_RING or (known and normal[1] or UNKNOWN_RING)
		local disc = not known and UNKNOWN_DISC or k == "mythic" and MYTHIC_DISC or k == "secret" and {GOLD[1], GOLD[2]} or discColors(areaSel)
		iDiscGrad.Color = ColorSequence.new(disc[1], disc[2])
		-- area / rarity pill + the rarity money bonus
		iEdge.Visible = k == "mythic"
		iPill.BackgroundColor3 = k == "mythic" and MYTHIC_INK or k == "secret" and SECRET_INK or tabCol[3]
		iPillStroke.Enabled = k ~= "mythic"
		local mult = info and info.rarityMult or 1
		local parts = {upper(area.name)}
		if known then -- (build review 1 N4: not found yet = only the area, the bonus stays a surprise)
			if k == "mythic" then table.insert(parts, "MYTHIC") elseif k == "secret" then table.insert(parts, "SECRET") end
			if mult > 1.005 then table.insert(parts, ("<font color='#7DFF6A'>$x%.1f</font>"):format(mult)) end
		end
		iPillText.Text = table.concat(parts, " · ")
		local rows = {
			known and ("<font color='#78EB5A'>" .. money(CreatureConfig.income(c.name, e.best or 1)) .. "/s</font>") or "???",
			known and (SpeedStat.Format(e.best or 0) .. " KG") or "???",
			known and ("x" .. tostring(e.n or 1)) or "x0",
			pctText(odds[creatureSel] or 0),
		}
		for i, s in stats do s.v.Text = rows[i] end
		fitStatLabels()
	end
	-- reward strip
	local done = IndexConfig.areaComplete(data, areaSel)
	local claimed = IndexConfig.isClaimed(data, areaSel)
	local again = IndexConfig.isUpdated(data, areaSel)
	rTitle.Text = (again and not claimed) and "NEW PET!<br/>COMPLETE AGAIN:" or ("COMPLETE<br/>" .. upper(area.name) .. ":")
	rMoney.Text = ("+%d%%"):format(math.floor(area.reward.pct * 100 + 0.5))
	rSpeed.Text = rMoney.Text
	local pots = area.reward.potions or {}
	rPotMoney.Text = "x" .. (pots.Money or 0)
	rPotHatch.Text = "x" .. (pots.Hatch or 0)
	rPotMoney.Parent.Visible = (pots.Money or 0) > 0
	rPotHatch.Parent.Visible = (pots.Hatch or 0) > 0
	evenChips()
	paint(claimH, claimed and SILVER or done and LIME or OFF)
	claimLabel.Text = claimed and "CLAIMED!" or done and (again and "CLAIM AGAIN!" or "CLAIM!") or (need - needFound) .. " LEFT"
	claimF.Active = done and not claimed
	-- totals
	local got, all = IndexConfig.discovered(data), IndexConfig.total()
	tText.Text = "DISCOVERED " .. got .. " / " .. all
	TweenService:Create(tFill, TweenInfo.new(0.35, Enum.EasingStyle.Quad), {Size = UDim2.fromScale(math.max(0.06, got / math.max(all, 1)), 1)}):Play()
	local n = claimable()
	allH.Visible = n > 0
	allCountText.Text = tostring(n)
	-- CLAIM ALL hidden: the trough takes the whole footer
	tBar.Size = UDim2.fromScale(n > 0 and 0.6 or 0.862, 0.48)
end

function selectArea(i)
	if not IndexConfig.AREAS[i] then return end
	areaSel = i
	creatureSel = nil
	refresh()
end
function selectCard(slot)
	if not IndexConfig.creatures(areaSel)[slot] then return end
	creatureSel = slot
	refresh()
end

local busy = false
local function claim(which)
	if busy then return end
	busy = true
	local ok, res = pcall(function() return Claim:InvokeServer(which) end)
	busy = false
	if ok and res then SFX.play("Rebirth") end
end
claimF.Activated:Connect(function() claim(areaSel) end)
allF.Activated:Connect(function() claim("all") end)

-- Studio tests (HatchRISTests.index_client v8*): press a tab / card / button by name
local testPress = Instance.new("BindableEvent")
testPress.Name = "TestPress"
testPress.Parent = page
testPress.Event:Connect(function(key)
	local what, n = tostring(key):match("^(%a+)_(%d+)$")
	if what == "Tab" then selectArea(tonumber(n))
	elseif what == "Card" then selectCard(tonumber(n))
	elseif key == "Claim" then task.spawn(claim, areaSel)
	elseif key == "ClaimAll" then task.spawn(claim, "all") end
end)

player:GetAttributeChangedSignal("IndexData"):Connect(function()
	data = IndexConfig.decode(player:GetAttribute("IndexData"))
	if page.Visible then refresh() end
end)
page:GetPropertyChangedSignal("Visible"):Connect(function() if page.Visible then fitCanvas() refresh() end end)
page:GetPropertyChangedSignal("AbsoluteSize"):Connect(function() if page.Visible then evenChips() end end)
refresh()
