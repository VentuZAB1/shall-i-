-- Tier9_x16 GALAXY "Star Gate" builder (Phase B). Idempotent: recolours the chassis, rebuilds Decor from the spec,
-- adds the lights, refreshes Bay9 and returns the validator report + rune order.
-- Run in Studio (Edit datamodel) via execute_luau. Belt-space coordinates: x = runner's right, -z = front (console).
local T = require(game.ServerStorage._TreadLabTools)
local m = game.ServerStorage.Assets.Treadmills.Tier9_x16
local bcf = m.Belt.CFrame

local C = {
	FRAME = Color3.fromRGB(30, 20, 62),
	VOID = Color3.fromRGB(16, 10, 36),
	VIOLET = Color3.fromRGB(118, 56, 222),
	MAGENTA = Color3.fromRGB(240, 50, 210),
	LAVENDER = Color3.fromRGB(196, 168, 255),
	STAR = Color3.fromRGB(255, 240, 178),
	BRIGHTVIOLET = Color3.fromRGB(165, 95, 255), -- Phase C: equalizer bars 2/4
}
local STARFIELD_WASH = false -- Phase C item 1: SurfaceLight off while testing the head-on wash

m:SetAttribute("Theme", "Galaxy")

------------------------------------------------------------------ chassis recolour (size/position untouched)
local function near(a, b, t) return math.abs(a - b) < (t or 0.03) end
local recoloured = 0
for _, p in m:GetChildren() do
	if p:IsA("BasePart") and p.Transparency < 1 then
		local s = p.Size
		local r = bcf:ToObjectSpace(p.CFrame).Position
		local role, var
		if near(s.Z, 15.56, 0.05) then role, var = "FRAME", "Studs" -- side frames
		elseif near(s.X, 1.30) and near(s.Y, 0.86) then -- belt strips
			local ax = math.abs(r.X)
			role = ax < 0.1 and "MAGENTA" or (ax > 3.5 and "VIOLET" or "FRAME")
			var = "Inlet"
		elseif near(s.X, 14.27, 0.05) then role, var = "FRAME", "Studs" -- front console bar
		elseif near(s.X, 1.30) and near(s.Y, 1.73) then role, var = "VIOLET", "Weld" -- console pillars
		elseif near(s.X, 9.08, 0.05) then role, var = "FRAME", "Studs" -- upper console bar
		elseif near(s.X, 2.16) then role, var = "MAGENTA", "Studs" -- screen bracket
		elseif near(s.X, 6.14, 0.05) then role, var = "VOID", "Universal" -- label FACE
		elseif near(s.X, 6.48, 0.05) then role, var = "VIOLET", "Studs" -- label FRAME (bezel)
		elseif near(s.X, 1.30) and near(s.Z, 2.59) then role, var = "FRAME", "Studs" -- handles
		elseif near(s.X, 1.21) then role, var = "MAGENTA", "Weld" -- grips
		elseif near(s.X, 12.71, 0.05) then role, var = "VIOLET", "Weld" -- base plate
		elseif near(s.X, 1.25) then role, var = "VIOLET", "Weld" -- front feet
		elseif near(s.X, 4.19, 0.05) then role, var = "VIOLET", "Weld" -- console centre piece
		elseif near(s.X, 1.30) and near(s.Z, 0.61) then role, var = "FRAME", "Studs" -- handle knobs
		end
		if role then
			p.Color = C[role]
			p.Material = Enum.Material.Plastic
			p.MaterialVariant = var
			recoloured += 1
		end
	end
end

------------------------------------------------------------------ decor spec
local D = {}
local function add(name, shape, size, cf, role, var, transp)
	table.insert(D, {name = name, shape = shape, size = size, cf = cf, role = role, var = var or "Universal", t = transp or 0})
end
local P = CFrame.new
local function Z(deg) return CFrame.Angles(0, 0, math.rad(deg)) end
local V3 = Vector3.new

-- A. Star Gate arch (on the front console bar ends)
local ZA = -8.475 -- arch depth centre (front console bar z -9.34..-7.61)
for _, sx in {-1, 1} do
	local tag = sx < 0 and "_L" or "_R"
	add("ArchPlinth" .. tag, "Block", V3(1.5, 0.5, 1.93), P(sx * 6.4875, 1.81, ZA), "FRAME", "Studs")
	add("ArchPost" .. tag, "Block", V3(1.295, 8.84, 1.73), P(sx * 6.4875, 6.48, ZA), "VIOLET", "Studs") -- y 2.06-10.9
	-- corner brace: right angle in the post/lintel corner, slope facing down + inward (turned about Y/Z only)
	local ez = V3(sx, 0, 0) -- wedge back face -> against the post
	local ey = V3(0, -1, 0) -- wedge bottom face -> against the lintel
	local ex = ey:Cross(ez)
	add("ArchCornerWedge" .. tag, "Wedge", V3(1.73, 1.3, 1.3), CFrame.fromMatrix(V3(sx * 5.19, 10.25, ZA), ex, ey, ez), "FRAME", "Studs") -- y 9.6-10.9
end
add("ArchLintel", "Block", V3(14.27, 1.3, 1.73), P(0, 11.55, ZA), "VIOLET", "Studs") -- y 10.9-12.2
-- Phase C item 5: capitals on the lintel ends, echoing the plinths (y 12.2-12.7)
add("ArchCap_L", "Block", V3(1.5, 0.5, 1.93), P(-6.4875, 12.45, ZA), "FRAME", "Studs")
add("ArchCap_R", "Block", V3(1.5, 0.5, 1.93), P(6.4875, 12.45, ZA), "FRAME", "Studs")
-- runes = chase order (Phase C item 4: 12 runes, two runner-face plates at x +-1.3 smooth the lintel crossing):
-- +X post up (1-4), lintel +3.9, +1.3, -1.3, -3.9 (5-8), -X post down (9-12)
local postY = {2.45, 5.65, 7.45, 9.25}
local n = 0
for i = 1, 4 do n += 1 add("rune_" .. n, "Block", V3(1.395, 0.45, 1.83), P(6.4875, postY[i], ZA), "MAGENTA") end
n += 1 add("rune_" .. n, "Block", V3(0.45, 1.4, 1.83), P(3.9, 11.55, ZA), "MAGENTA")
n += 1 add("rune_" .. n, "Block", V3(0.45, 1.4, 0.1), P(1.3, 11.55, -7.56), "MAGENTA")
n += 1 add("rune_" .. n, "Block", V3(0.45, 1.4, 0.1), P(-1.3, 11.55, -7.56), "MAGENTA")
n += 1 add("rune_" .. n, "Block", V3(0.45, 1.4, 1.83), P(-3.9, 11.55, ZA), "MAGENTA")
for i = 4, 1, -1 do n += 1 add("rune_" .. n, "Block", V3(1.395, 0.45, 1.83), P(-6.4875, postY[i], ZA), "MAGENTA") end

-- B. Tall console: the raised screen tower (hangs on the lintel's front face, rests on the label frame's top edge)
add("ScreenTower", "Block", V3(6.48, 3.65, 1.3), P(0, 10.375, -9.99), "FRAME", "Studs") -- y 8.55-12.2, z -10.64..-9.34
add("ScreenDisplayRunner", "Block", V3(5.88, 1.9, 0.2), P(0, 9.8, -9.29), "VOID") -- y 8.85-10.75
local barH = {0.9, 1.15, 1.4, 1.15, 0.9}
local barC = {"MAGENTA", "BRIGHTVIOLET", "LAVENDER", "BRIGHTVIOLET", "MAGENTA"} -- Phase C item 3: no cream bar
for i = 1, 5 do
	add("screen_bar_" .. i, "Block", V3(0.7, barH[i], 0.2), P((i - 3) * 1.1, 9.05 + barH[i] / 2, -9.14), barC[i])
end
add("sparkle_scr_1", "Block", V3(0.35, 0.35, 0.3), P(-2.65, 10.2, -9.19) * Z(45), "STAR")
add("sparkle_scr_2", "Block", V3(0.35, 0.35, 0.3), P(2.65, 10.2, -9.19) * Z(45), "STAR")
add("ScreenDisplayFront", "Block", V3(5.88, 3.05, 0.2), P(0, 10.375, -10.69), "VOID") -- y 8.85-11.9
add("StarRayH", "Block", V3(3.2, 0.22, 0.14), P(0, 10.4, -10.82), "LAVENDER")
add("StarRayV", "Block", V3(0.22, 2.6, 0.18), P(0, 10.4, -10.84), "LAVENDER")
add("screen_gem", "Block", V3(1.0, 1.0, 0.3), P(0, 10.4, -10.84) * Z(45), "MAGENTA")
local stars = {
	{0.5, -2.3, 11.4, "STAR"}, {0.35, 2.4, 11.5, "STAR"}, {0.4, 2.3, 9.3, "STAR"},
	{0.3, -2.4, 9.35, "LAVENDER"}, {0.3, 1.15, 11.55, "LAVENDER"},
}
for i, s in stars do
	add("sparkle_scr_" .. (i + 2), "Block", V3(s[1], s[1], 0.3), P(s[2], s[3], -10.79) * Z(45), s[4])
end

-- C. Planet topper (orb system)
local ZT = -9.125
add("TopperBase", "Block", V3(6.48, 0.3, 3.03), P(0, 12.35, ZT), "FRAME", "Studs") -- y 12.2-12.5
add("PlanetDish", "Cyl", V3(0.2, 2.0, 2.0), P(0, 12.6, ZT) * Z(90), "VIOLET", "Weld") -- y 12.5-12.7
add("orb_core", "Ball", V3(1.4, 1.4, 1.4), P(0, 13.7, ZT), "MAGENTA") -- 13.0-14.4
-- Phase C item 2: bigger, more opaque gold "Saturn" ring, 20 deg tilt; moons pushed out to r 2.35
add("orb_ring_a", "Cyl", V3(0.14, 3.6, 3.6), P(0, 13.7, ZT) * Z(110), "STAR", "Universal", 0.15)
local R = 2.35
add("orb_shard_0", "Ball", V3(0.45, 0.45, 0.45), P(R, 13.95, ZT), "STAR")
add("orb_shard_1", "Ball", V3(0.45, 0.45, 0.45), P(-R / 2, 13.45, ZT - R * 0.8660254), "STAR")
add("orb_shard_2", "Ball", V3(0.45, 0.45, 0.45), P(-R / 2, 13.75, ZT + R * 0.8660254), "LAVENDER")

-- D. Side rails (handrails from the grips back to z 7.6, low: top 3.85)
for _, sx in {-1, 1} do
	local tag = sx < 0 and "L" or "R"
	local x = sx * 5.185
	add("RailBar_" .. tag, "Block", V3(0.9, 0.65, 12.87), P(x, 3.525, 1.165), "VIOLET", "Inlet")
	for i, z in {-2.0, 2.3, 6.6} do
		add("RailPost_" .. tag .. i, "Block", V3(0.9, 2.325, 0.9), P(x, 2.0375, z), "FRAME", "Studs")
		add("sparkle_rail_" .. tag .. i, "Block", V3(0.5, 0.5, 0.5), P(x, 3.85, z) * Z(45), "STAR")
	end
	add("RailCap_" .. tag, "Block", V3(1.0, 0.75, 0.45), P(x, 3.525, 7.4), "MAGENTA", "Weld")
end

-- E. Front console bar face
add("FrontStripe", "Block", V3(10.2, 0.35, 0.2), P(0, 0.35, -9.39), "MAGENTA", "Weld")
for i, x in {-4.4, -1.5, 1.5, 4.4} do
	add("sparkle_front_" .. i, "Block", V3(0.45, 0.45, 0.45), P(x, 1.0, -9.34) * Z(45), "STAR")
end

------------------------------------------------------------------ build
local decor = m:FindFirstChild("Decor")
if not decor then
	decor = Instance.new("Model")
	decor.Name = "Decor"
	decor.Parent = m
end
decor:ClearAllChildren()
local made = {}
for _, e in D do
	local p = e.shape == "Wedge" and Instance.new("WedgePart") or Instance.new("Part")
	if e.shape == "Ball" then p.Shape = Enum.PartType.Ball elseif e.shape == "Cyl" then p.Shape = Enum.PartType.Cylinder end
	p.Name = e.name
	p.Size = e.size
	p.CFrame = bcf * e.cf
	p.Color = C[e.role]
	p.Material = Enum.Material.Plastic
	p.MaterialVariant = e.var
	p.Transparency = e.t
	p.Anchored = true
	p.CanCollide = false
	p.CanTouch = false
	p.CanQuery = false
	p.TopSurface = Enum.SurfaceType.Smooth
	p.BottomSurface = Enum.SurfaceType.Smooth
	p.Parent = decor
	made[e.name] = p
end

------------------------------------------------------------------ lights (3, Shadows off)
local function light(class, parent, props)
	local l = Instance.new(class)
	for k, v in props do l[k] = v end
	l.Shadows = false
	l.Parent = parent
end
light("PointLight", made.orb_core, {Name = "PlanetGlow", Color = Color3.fromRGB(255, 90, 225), Brightness = 2, Range = 10})
if STARFIELD_WASH then
	light("SurfaceLight", made.ScreenDisplayFront, {Name = "StarfieldWash", Face = Enum.NormalId.Front, Color = Color3.fromRGB(170, 120, 255), Brightness = 0.6, Range = 8, Angle = 110})
end
light("PointLight", made.ScreenDisplayRunner, {Name = "RunnerGlow", Color = Color3.fromRGB(200, 130, 255), Brightness = 0.8, Range = 7})

------------------------------------------------------------------ refresh + report
local report = T.refresh(9)
local runes = {}
for _, d in workspace._TreadmillLab.Bays.Bay9.Treadmill:GetDescendants() do
	local k = d:IsA("BasePart") and d.Name:match("^rune_(%d+)$")
	if k then table.insert(runes, {tonumber(k), d}) end
end
table.sort(runes, function(a, b) return a[1] < b[1] end)
local order = {}
local bb = workspace._TreadmillLab.Bays.Bay9.Treadmill.Belt.CFrame
for _, r in runes do
	local q = bb:ToObjectSpace(r[2].CFrame).Position
	table.insert(order, ("%d(%.1f,%.1f)"):format(r[1], q.X, q.Y))
end
return ("recoloured %d chassis parts, %d decor parts\n%s\nrune chase: %s"):format(recoloured, #D, report, table.concat(order, " > "))
