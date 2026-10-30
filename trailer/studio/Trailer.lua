-- Trailer (2026-10-15): the owner's in-game cinematic TRAILER for the experience page video (Creator Hub > Videos).
-- (2026-10-21) redesigned hub: S6 hatch on the own plot's Floor facing the plaza, S8 = the own treadmill filmed from
-- its plaza side, S10 glide relative to the moved giant pumpkin (PUMPKIN_AT).
-- Owner: "animate it in Roblox Studio and add it into the admin panel; when I click it I run it; black screen 2 s so I
-- can turn on OBS; I record it in-game at full resolution". Started from AdminClient (SERVER tab > PLAY TRAILER).
-- Everything is LOCAL (only on the owner's screen): a puppet copy of the avatar (Intro.Poses) acts it out; the waves,
-- meteor, UFO, eggs, treadmill and pets are local copies of the game's own models + VFX; the HUD and other players hide.
-- Music: "Race To Finish" (APM via the Roblox catalog, already in SFX.MUSIC_TRACKS) from 142.4 s, so the drop at 144.4 s
-- is the slingshot release (t = 2.0) and the last hit at 172.2 s is the title (t = 29.8). The music is the master clock.
-- Roblox video rules (checked 2026-10-15): <= 60 s, 16:9, <= 1920x1080, no voice / lyrics, no subjective claims in text.
-- Backspace stops it. Studio review: player attribute TrailerDebugT = n freezes it at n s.
-- Shot list + plan: Desktop/SLINGSHOT Creatures/trailer/SHOTLIST.md
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local StarterGui = game:GetService("StarterGui")
local SoundService = game:GetService("SoundService")
local Lighting = game:GetService("Lighting")
local UserInputService = game:GetService("UserInputService")
local RS = game:GetService("ReplicatedStorage")

local P = require(RS:WaitForChild("Intro"):WaitForChild("Poses"))
local CreatureAnimator = require(RS:WaitForChild("CreatureAnimator"))
local SFX = require(RS:WaitForChild("SFX"))
local PetEventFX = nil
pcall(function() PetEventFX = require(RS:WaitForChild("PetEventFX", 5)) end)
local WaveModels = RS:WaitForChild("WaveModels")
local FX = RS:WaitForChild("WeatherFX")
local WA = RS:WaitForChild("WeatherAssets")
local CreatureModels = RS:WaitForChild("CreatureModels")
local IntroAssets = RS:WaitForChild("Intro"):WaitForChild("Assets")
local SlingSounds = RS:WaitForChild("Slingshot"):WaitForChild("Sounds")
local Assets = script:WaitForChild("Assets")

local player = Players.LocalPlayer
local V = Vector3.new
local smooth, ramp = P.smooth, P.ramp
local function lerp(a, b, x) return a + (b - a) * x end
local function noise(t, seed) return math.noise(t, seed, 0.5) end
local function yawOf(d) return math.atan2(-d.X, -d.Z) end
local function lerpAngle(a, b, x)
	local d = (b - a + math.pi) % (2 * math.pi) - math.pi
	return a + d * x
end

local M = {}
M.running = false

local MUSIC_ID = "rbxassetid://9041814167"
local MUSIC_AT = 142.4 -- track time at t = 0
local MUSIC_VOL = 0.55
local BLACK_IN, BLACK_OUT = 2, 1.5

---------------------------------------------------------------- the timeline (content seconds; t = 0 right after the black)
local T = {
	pull0 = 0.25, release = 2.0, cut1 = 2.45, cut2 = 4.9, rise = 5.55, eggGo = 5.8, reach = 6.25, held = 6.75,
	cut3 = 7.2, cut4 = 9.0, cut5 = 11.2, gate = 11.65, crash = 12.05,
	cut6 = 12.4, wob1 = 12.85, wob2 = 13.4, wob3 = 13.9, burst = 14.6,
	cut7 = 16.2, cut8 = 18.4, cut9 = 20.6, strike = 21.55, cut10 = 22.6, cut11 = 24.4, cut12 = 27.4, money = 28.35,
	title = 29.8, fade0 = 32.5, fade1 = 33.4,
}
local FLY = 3.2 -- seconds from the release to the landing
T.land = T.release + FLY
local LENGTH = T.fade1

---------------------------------------------------------------- the stage (world studs; floors at y = 0)
local LAND = V(18, 0, -318) -- beyond the Grass trench (z -266..-254, bottom y -6); x 18 = a lane with no ground decor
local EGG = V(17, 0, -306)
local GRAB = EGG + V(-0.6, 0, -3.2) -- stand on the runway side of the egg, facing the hub
local TRENCH_RIM, TRENCH_FAR, TRENCH_FLOOR = -266.5, -253.5, -6
local GATE_Z, END_Z = -61, -62
local RUN_V = 21
local REX_YAW = 0 -- CreatureModels face -Z like any model (measured in Studio: head bone towards the yaw)
local WAVE = {H = 34, L = 30, speed = 150, accent = Color3.fromRGB(120, 230, 255)}
local PET_SPOTS = {
	{name = "InfernoPhoenix", pos = V(-8, 0, -1440), t0 = T.cut7, act = "act_rebirth", air = true},
	-- (Shadow / Celestial are too far to stream in from the hub, so Thunder + Water host the other two)
	{name = "AbyssWeaver", pos = V(-4, 0, -1050), t0 = T.cut7 + 0.73, act = "act_riftweave"},
	{name = "CosmicLeviathan", pos = V(2, 0, -660), t0 = T.cut7 + 1.46, act = "act_sounding", air = true, mode = "swim"},
}

-- slow motion while the tsunami rolls over the trench: w(t) = the scene clock of that stretch
local function rate(t)
	local a0, a1 = 9.72, 10.4
	return lerp(1, 0.28, math.min(ramp(t, a0 - 0.15, a0), 1 - ramp(t, a1, a1 + 0.2)))
end
local WDT = 1 / 240
local WARP = {}
do
	local w = T.cut3
	for i = 0, math.ceil((T.cut5 - T.cut3) / WDT) + 2 do
		WARP[i] = w
		w += rate(T.cut3 + i * WDT) * WDT
	end
end
local function warp(t)
	if t <= T.cut3 then return t end
	local f = (t - T.cut3) / WDT
	local i = math.floor(f)
	local a = WARP[i] or WARP[#WARP]
	local b = WARP[i + 1] or a
	return a + (b - a) * (f - i)
end
-- warped times of the tsunami stretch
local W = {}
W.rim = T.cut3 + (TRENCH_RIM - 0.8 - GRAB.Z) / RUN_V -- the runner reaches the trench edge
W.bottom = W.rim + 0.42
W.front = W.rim + 0.72 -- the wave front passes over the far rim
W.out0 = W.front + 0.32
W.out1 = W.out0 + 0.38
local function waveFront(w) return TRENCH_FAR + WAVE.speed * (w - W.front) end

---------------------------------------------------------------- small helpers
local function clonePS(path, props)
	local src = FX
	for _, n in path do src = src and src:FindFirstChild(n) end
	if not src then return nil end
	local e = src:Clone()
	if e:IsA("ParticleEmitter") then e.Enabled = false end
	for k, v in props or {} do e[k] = v end
	return e
end
local function scaleNS(ns, k)
	local kps = {}
	for _, p in ns.Keypoints do table.insert(kps, NumberSequenceKeypoint.new(p.Time, p.Value * k, p.Envelope * k)) end
	return NumberSequence.new(kps)
end
local function slingSound(name, vol)
	local s = SlingSounds:FindFirstChild(name)
	if not s then return end
	s = s:Clone()
	s.Volume = s.Volume * (vol or 1)
	s.Parent = SoundService
	s:Play()
	task.delay(8, function() s:Destroy() end)
end
local function sfx(name, vol, pitch) pcall(SFX.play, name, {volume = vol, pitch = pitch}) end
local function strip(model)
	for _, d in model:GetDescendants() do
		if d:IsA("BaseScript") or d:IsA("ModuleScript") or d:IsA("ProximityPrompt") or d:IsA("ClickDetector") then d:Destroy() end
		if d:IsA("BasePart") then d.Anchored, d.CanCollide, d.CanQuery, d.CanTouch = true, false, false, false end
	end
	return model
end

---------------------------------------------------------------- the run
local cleanup = {}
local function onEnd(fn) table.insert(cleanup, fn) end
local function runCleanup()
	for i = #cleanup, 1, -1 do pcall(cleanup[i]) end
	table.clear(cleanup)
end

local function run()
	local cam = workspace.CurrentCamera
	local char = player.Character
	local realRoot = char and char:FindFirstChild("HumanoidRootPart")
	local realHum = char and char:FindFirstChildOfClass("Humanoid")
	if not (realRoot and realHum) then return end
	local pg = player:WaitForChild("PlayerGui")
	local stopped = false

	local scene = Instance.new("Folder")
	scene.Name = "TrailerScene"
	scene.Parent = workspace
	onEnd(function() scene:Destroy() end)
	local PARK = CFrame.new(0, -600, 0)

	------------------------------------------------ UI: black screen first (the owner starts OBS), then hide the HUD
	local gui = Instance.new("ScreenGui")
	gui.Name = "TrailerGui"
	gui.IgnoreGuiInset = true
	gui.ScreenInsets = Enum.ScreenInsets.None
	gui.ResetOnSpawn = false
	gui.DisplayOrder = 200
	gui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling
	gui.Parent = pg
	onEnd(function() gui:Destroy() end)
	local black = Instance.new("Frame")
	black.Name = "Black"
	black.BackgroundColor3 = Color3.new(0, 0, 0)
	black.BorderSizePixel = 0
	black.Size = UDim2.fromScale(1, 1)
	black.ZIndex = 50
	black.Parent = gui
	local flash = Instance.new("Frame")
	flash.Name = "Flash"
	flash.BackgroundColor3 = Color3.new(1, 1, 1)
	flash.BackgroundTransparency = 1
	flash.BorderSizePixel = 0
	flash.Size = UDim2.fromScale(1, 1)
	flash.ZIndex = 40
	flash.Parent = gui
	local flashAt, flashLen = -10, 0.2
	local function doFlash(len) flashAt, flashLen = os.clock(), len or 0.2 end

	local hidden = {}
	local function hideHud()
		for _, g in pg:GetChildren() do
			if g:IsA("ScreenGui") and g ~= gui and g.Enabled then hidden[g] = true g.Enabled = false end
		end
	end
	hideHud()
	local coreWas = {}
	for _, ct in Enum.CoreGuiType:GetEnumItems() do
		if ct ~= Enum.CoreGuiType.All then
			local ok, v = pcall(StarterGui.GetCoreGuiEnabled, StarterGui, ct)
			if ok then coreWas[ct] = v end
		end
	end
	pcall(function() StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.All, false) end)
	local topbarWas = true
	pcall(function() topbarWas = StarterGui:GetCore("TopbarEnabled") end)
	pcall(function() StarterGui:SetCore("TopbarEnabled", false) end)
	onEnd(function()
		for g in hidden do if g.Parent then g.Enabled = true end end
		for ct, v in coreWas do pcall(StarterGui.SetCoreGuiEnabled, StarterGui, ct, v) end
		pcall(function() StarterGui:SetCore("TopbarEnabled", topbarWas ~= false) end)
	end)

	------------------------------------------------ the real character waits hidden + frozen; other players hide too
	local wasAnchored = realRoot.Anchored
	realRoot.Anchored = true
	local wasDisplay = realHum.DisplayDistanceType
	realHum.DisplayDistanceType = Enum.HumanoidDisplayDistanceType.None
	local ghosted = {}
	local function ghost(model)
		for _, d in model:GetDescendants() do
			if (d:IsA("BasePart") or d:IsA("Decal")) and not ghosted[d] then
				ghosted[d] = d.LocalTransparencyModifier
				d.LocalTransparencyModifier = 1
			elseif (d:IsA("BillboardGui") or d:IsA("SurfaceGui")) and d.Enabled and not ghosted[d] then
				ghosted[d] = true
				d.Enabled = false
			end
		end
	end
	local function ghostPlayers()
		for _, p in Players:GetPlayers() do if p.Character then ghost(p.Character) end end
	end
	onEnd(function()
		for d, v in ghosted do
			if d.Parent then
				if d:IsA("BillboardGui") or d:IsA("SurfaceGui") then d.Enabled = true else d.LocalTransparencyModifier = v == true and 0 or v end
			end
		end
		if realRoot.Parent then realRoot.Anchored = wasAnchored end
		if realHum.Parent then realHum.DisplayDistanceType = wasDisplay end
	end)

	------------------------------------------------ the world: park the real waves, hide the runway eggs, day light
	local parked = {}
	local function parkWaves()
		for _, m in workspace:GetChildren() do
			if m.Name == "WaveVisual" and m:IsA("Model") then parked[m] = true m.Parent = nil end
		end
	end
	parkWaves()
	onEnd(function() for m in parked do pcall(function() m.Parent = workspace end) end end)
	local hideZ = {}
	local function hideZoneEggs()
		local ze = workspace:FindFirstChild("ZoneEggs")
		if not ze then return end
		for _, d in ze:GetDescendants() do
			if (d:IsA("BasePart") or d:IsA("Decal")) and not hideZ[d] then hideZ[d] = true d.LocalTransparencyModifier = 1 end
			if d:IsA("BillboardGui") and d.Enabled and not hideZ[d] then hideZ[d] = true d.Enabled = false end
		end
	end
	hideZoneEggs()
	-- the owner name cards on the bases + treadmills (headshot + name) hide for the whole trailer
	local cardsHidden = {}
	local function hideCards()
		local hub = workspace.Map:FindFirstChild("Hub")
		local roots = {hub and hub:FindFirstChild("Bases"), hub and hub:FindFirstChild("Treadmills")}
		local function under(inst)
			if not inst then return false end
			for _, r in roots do if r and inst:IsDescendantOf(r) then return true end end
			return false
		end
		for _, src in {roots[1], roots[2], pg} do
			if src then
				for _, d in src:GetDescendants() do
					if d:IsA("BillboardGui") and d.Enabled and (under(d) or under(d.Adornee)) then cardsHidden[d] = true d.Enabled = false end
				end
			end
		end
	end
	hideCards()
	onEnd(function() for d in cardsHidden do if d.Parent then d.Enabled = true end end end)
	onEnd(function()
		for d in hideZ do if d.Parent then if d:IsA("BillboardGui") then d.Enabled = true else d.LocalTransparencyModifier = 0 end end end
	end)
	-- base pets/eggs hide during the base shots (a clean plot for the hatch)
	local baseHidden, baseHiddenOn = {}, false
	local function hideBases(on)
		if on == baseHiddenOn then return end
		baseHiddenOn = on
		local bc = workspace:FindFirstChild("BaseContent")
		local cards = workspace.Map.Hub:FindFirstChild("Bases")
		if on and bc then
			if cards then
				for _, d in cards:GetDescendants() do
					if (d:IsA("BillboardGui") or d:IsA("SurfaceGui")) and d.Enabled and d:IsA("BillboardGui") then baseHidden[d] = true d.Enabled = false end
				end
			end
			for _, d in bc:GetDescendants() do
				if (d:IsA("BasePart") or d:IsA("Decal")) and d.LocalTransparencyModifier < 1 then baseHidden[d] = true d.LocalTransparencyModifier = 1 end
				if (d:IsA("BillboardGui") or d:IsA("SurfaceGui")) and d.Enabled then baseHidden[d] = true d.Enabled = false end
			end
		elseif not on then
			for d in baseHidden do
				if d.Parent then if d:IsA("BillboardGui") or d:IsA("SurfaceGui") then d.Enabled = true else d.LocalTransparencyModifier = 0 end end
			end
			table.clear(baseHidden)
		end
	end
	onEnd(function() hideBases(false) end)
	local clockWas = Lighting.ClockTime
	local clockWant = 14.6
	onEnd(function() Lighting.ClockTime = clockWas end)
	local storm = Instance.new("ColorCorrectionEffect")
	storm.Name = "TrailerTint"
	storm.Enabled = false
	storm.Parent = Lighting
	onEnd(function() storm:Destroy() end)
	-- the game's own music + wind go quiet; its sound effects stay
	local groupVol = {}
	for _, n in {"MusicGroup"} do
		local g = SoundService:FindFirstChild(n)
		if g and g:IsA("SoundGroup") then groupVol[g] = g.Volume g.Volume = 0 end
	end
	for _, n in {"Music", "SpeedWind"} do
		local s = SoundService:FindFirstChild(n)
		if s and s:IsA("Sound") then groupVol[s] = s.Volume s.Volume = 0 end
	end
	onEnd(function() for g, v in groupVol do if g.Parent then g.Volume = v end end end)

	------------------------------------------------ streaming: ask for every stage now (and keep asking)
	local streamSpots = {LAND, V(0, 0, -180), V(0, 0, -90)}
	for _, s in PET_SPOTS do table.insert(streamSpots, s.pos) end
	local streaming = 0
	local function requestStreams()
		if streaming > 0 then return end
		for _, p in streamSpots do
			streaming += 1
			task.spawn(function()
				pcall(function() player:RequestStreamAroundAsync(p, 3) end)
				streaming -= 1
			end)
		end
	end
	requestStreams()

	local rayParams = RaycastParams.new()
	rayParams.FilterType = Enum.RaycastFilterType.Exclude
	local function groundAt(pos, default)
		local ex = {scene, cam}
		for _, p in Players:GetPlayers() do if p.Character then table.insert(ex, p.Character) end end
		rayParams.FilterDescendantsInstances = ex
		local hit = workspace:Raycast(V(pos.X, pos.Y + 60, pos.Z), V(0, -160, 0), rayParams)
		return hit and hit.Position.Y or default
	end

	-- the music (master clock) loads while the props build; it starts at "go"
	local music = Instance.new("Sound")
	music.Name = "TrailerMusic"
	music.SoundId = MUSIC_ID
	music.Volume = 0
	music.Parent = SoundService
	onEnd(function() music:Destroy() end)

	------------------------------------------------ the puppet
	local rig = P.makePuppet(char)
	if not rig then return end
	rig.model.Name = "TrailerPuppet"
	rig.model.Parent = scene
	rig.hrp.CFrame = PARK
	local H0 = rig.h0
	local head = rig.model:FindFirstChild("Head")
	ghostPlayers() -- the real avatar + everyone else hide (the puppet is a copy made just before)
	local CYCLE = 9.5 * (H0 / 3)
	local phase, lastPos = 0, nil
	local function runPhase(pos, cycle)
		if lastPos then phase += (V(pos.X, 0, pos.Z) - V(lastPos.X, 0, lastPos.Z)).Magnitude / cycle * 2 * math.pi end
		lastPos = pos
		return phase
	end
	-- wind ribbons on the hands + feet while flying (the meteor trail ribbon, recoloured; same as the intro)
	local trails = {}
	do
		local src = FX:FindFirstChild("MeteorTrail") and FX.MeteorTrail:FindFirstChild("A0") and FX.MeteorTrail.A0:FindFirstChild("Ribbon")
		for _, n in {"RightHand", "LeftHand", "RightFoot", "LeftFoot"} do
			local p = rig.model:FindFirstChild(n)
			if src and p then
				local a0, a1 = Instance.new("Attachment"), Instance.new("Attachment")
				a0.Position, a1.Position = V(0, 0.25, 0), V(0, -0.25, 0)
				a0.Parent, a1.Parent = p, p
				local tr = src:Clone()
				tr.Attachment0, tr.Attachment1 = a0, a1
				tr.Texture = ""
				tr.Color = ColorSequence.new(Color3.fromRGB(255, 255, 255), Color3.fromRGB(170, 230, 255))
				tr.Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0, 0.3), NumberSequenceKeypoint.new(1, 1)})
				tr.WidthScale = NumberSequence.new({NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(1, 0.1)})
				tr.LightEmission = 0.5
				tr.Lifetime = 0.1
				tr.Enabled = false
				tr.Parent = p
				table.insert(trails, tr)
			end
		end
	end
	local function setTrails(on) for _, tr in trails do if tr.Enabled ~= on then tr.Enabled = on end end end

	------------------------------------------------ props (built now, during the black, so nothing hitches later)
	local function simplePart(props)
		local p = Instance.new("Part")
		p.Anchored, p.CanCollide, p.CanQuery, p.CanTouch, p.CastShadow = true, false, false, false, false
		p.Material = Enum.Material.SmoothPlastic
		p.TopSurface, p.BottomSurface = Enum.SurfaceType.Smooth, Enum.SurfaceType.Smooth
		for k, v in props do p[k] = v end
		p.Parent = scene
		return p
	end
	-- effects host: clones of the game's VFX emitters
	local fxHost = simplePart({Size = V(1, 1, 1), Transparency = 1, CFrame = PARK})
	local fxAtt = Instance.new("Attachment") fxAtt.Parent = fxHost
	local dust = clonePS({"MeteorImpact", "Dust"}, {Color = ColorSequence.new(Color3.fromRGB(214, 200, 168))})
	local ring = clonePS({"MeteorImpact", "Ring"}, {Color = ColorSequence.new(Color3.new(1, 1, 1)), LightEmission = 0.4})
	local sparkle = clonePS({"TractorBeam", "Bottom", "Sparkles"}, {Color = ColorSequence.new(Color3.fromRGB(255, 220, 90)), Speed = NumberRange.new(8, 18), SpreadAngle = Vector2.new(180, 180)})
	local zap = clonePS({"MeteorLightning", "Spider"}, {Color = ColorSequence.new(Color3.fromRGB(150, 230, 255))})
	for _, e in {dust, ring, sparkle, zap} do if e then e.Parent = fxAtt end end
	if ring then ring.Size = scaleNS(ring.Size, 0.55) end
	if dust then dust.Size = scaleNS(dust.Size, 0.6) end
	local function burst(e, pos, n, sizeK)
		if not e then return end
		fxHost.CFrame = CFrame.new(pos)
		local old = e.Size
		if sizeK then e.Size = scaleNS(old, sizeK) end
		e:Emit(n)
		if sizeK then e.Size = old end
	end

	-- slingshot: our own pouch + bands (the real ones hide meanwhile)
	local sling = workspace:FindFirstChild("Map") and workspace.Map:FindFirstChild("Hub") and workspace.Map.Hub:FindFirstChild("Slingshot")
	local realPouch = sling and sling:FindFirstChild("LivePouch")
	local anchor = sling and sling:FindFirstChild("BandAnchor")
	local pouch, pouchRest, ties, tubes = nil, nil, {}, {}
	if realPouch and anchor then
		pouchRest = anchor:GetAttribute("PouchRest") or realPouch.CFrame
		pouch = realPouch:Clone()
		for _, d in pouch:GetChildren() do if not d:IsA("Attachment") and not d:IsA("SurfaceAppearance") then d:Destroy() end end
		pouch.Anchored, pouch.CanCollide, pouch.CanQuery, pouch.CanTouch = true, false, false, false
		pouch.CFrame = pouchRest
		pouch.Parent = scene
		ties = {anchor:FindFirstChild("TieL"), anchor:FindFirstChild("TieR")}
		for i = 1, 4 do
			tubes[i] = simplePart({Shape = Enum.PartType.Cylinder, Material = Enum.Material.Neon, Color = Color3.fromRGB(40, 215, 255), CFrame = PARK})
		end
	end
	local POUCH0 = pouchRest and pouchRest.Position or V(0.53, 25.31, -39.87)
	local PULL = V(0, -1.6, 8)
	local SEAT_UP = 2.6
	local restLen = {}
	local function drawSling(pouchPos)
		if not pouch then return end
		pouch.CFrame = pouchRest - pouchRest.Position + pouchPos
		local edges = {pouch:FindFirstChild("EdgeL"), pouch:FindFirstChild("EdgeR")}
		for b = 1, 2 do
			local tie = ties[b]
			if not (tie and edges[1]) then continue end
			local e = edges[1]
			if edges[2] and (edges[2].WorldPosition - tie.WorldPosition).Magnitude < (edges[1].WorldPosition - tie.WorldPosition).Magnitude then e = edges[2] end
			local p0, p1 = tie.WorldPosition, e.WorldPosition
			local span = p1 - p0
			local len = span.Magnitude
			restLen[b] = restLen[b] or len
			local thick = 0.62 * math.clamp(math.sqrt(restLen[b] / math.max(len, 0.1)), 0.45, 1)
			local side = span.Unit:Cross(Vector3.yAxis)
			local up = side.Magnitude > 0.01 and side.Unit:Cross(span.Unit) or Vector3.zAxis
			for k = 1, 2 do
				local tube = tubes[(b - 1) * 2 + k]
				local mid = (p0 + p1) / 2 + up * 0.42 * (k == 1 and 0.5 or -0.5)
				tube.Size = V(len, thick, thick)
				tube.CFrame = CFrame.lookAt(mid, mid + span) * CFrame.Angles(0, math.pi / 2, 0)
			end
		end
	end
	local function hideRealSling(on)
		if realPouch then realPouch.LocalTransparencyModifier = on and 1 or 0 end
		local bf = cam:FindFirstChild("SlingBands")
		if bf then for _, t in bf:GetChildren() do if t:IsA("BasePart") then t.LocalTransparencyModifier = on and 1 or 0 end end end
	end
	hideRealSling(true)
	onEnd(function() hideRealSling(false) end)
	drawSling(POUCH0)

	-- the runway egg (the intro's wood egg shell)
	local EGG_K = 0.5
	local egg = IntroAssets.EggShell:Clone()
	egg:ScaleTo(EGG_K)
	strip(egg)
	egg.Parent = scene
	local eggCF, eggSize = egg:GetBoundingBox()
	local eggOff = eggCF.Position - egg:GetPivot().Position
	local function placeEgg(center) egg:PivotTo(CFrame.new(center - eggOff)) end
	placeEgg(PARK.Position)
	local eggRest = EGG + V(0, eggSize.Y / 2, 0)

	-- waves: local copies of the real wave meshes (built like WaveClient / the intro)
	local WIDTH = 120
	local waves = {}
	local function makeWave(typeName, H, L)
		local model = Instance.new("Model")
		model.Name = "TrailerWave"
		model.Parent = scene
		local body = (WaveModels:FindFirstChild(typeName) or WaveModels:FindFirstChild("Normal")):Clone()
		body.Size = V(WIDTH, H, L)
		local label = body:FindFirstChild("Label")
		if label then label:Destroy() end
		body.Anchored, body.CanCollide, body.CanQuery, body.CanTouch = true, false, false, false
		body.CFrame = PARK
		body.Parent = model
		local lip = simplePart({Size = V(WIDTH, 1, 1), Transparency = 1, CFrame = PARK})
		lip.Parent = model
		local e = Instance.new("ParticleEmitter")
		e.Texture = "rbxasset://textures/particles/smoke_main.dds"
		e.Color = ColorSequence.new(Color3.fromRGB(235, 248, 255), WAVE.accent)
		e.Size = NumberSequence.new({NumberSequenceKeypoint.new(0, 4), NumberSequenceKeypoint.new(1, 9)})
		e.Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0, 0.3), NumberSequenceKeypoint.new(1, 1)})
		e.Lifetime = NumberRange.new(0.5, 0.9)
		e.Rate = 90
		e.Speed = NumberRange.new(6, 16)
		e.SpreadAngle = Vector2.new(25, 25)
		e.EmissionDirection = Enum.NormalId.Top
		e.Enabled = false
		e.Parent = lip
		local w = {model = model, body = body, lip = lip, spray = e, H = H, L = L, base = body.Transparency, tex = {}}
		for _, d in body:GetChildren() do if d:IsA("Texture") then table.insert(w.tex, {d, d.Transparency}) end end
		table.insert(waves, w)
		return w
	end
	local function drawWave(w, front, endZ)
		if not front then
			w.body.CFrame, w.lip.CFrame, w.spray.Enabled = PARK, PARK, false
			if w.roar then w.roar.Volume = 0 end
			return
		end
		local z = math.min(front, endZ or 1e9) - w.L / 2
		w.body.CFrame = CFrame.new(0, 0.05, z) * CFrame.new(0, w.H / 2, 0) * CFrame.Angles(0, math.pi, 0)
		w.lip.CFrame = CFrame.new(0, w.H * 0.95, z + w.L * 0.3)
		local a = endZ and math.clamp((front - endZ) / (WAVE.speed * 0.5), 0, 1) or 0
		w.body.Transparency = w.base + (1 - w.base) * a
		for _, tx in w.tex do tx[1].Transparency = tx[2] + (1 - tx[2]) * a end
		w.spray.Enabled = a < 0.5
		if w.roar then w.roar.Volume = (w.roarBase or 0.5) * (1 - a) end
	end
	local wave1 = makeWave("Normal", WAVE.H, WAVE.L)
	local wave2 = makeWave("Normal", WAVE.H * 0.8, WAVE.L)
	wave1.roar = SFX.loop("WaveRoar", wave1.lip, {volume = 1.5, pitch = 0.85})
	wave2.roar = SFX.loop("WaveRoar", wave2.lip, {volume = 1.3, pitch = 0.95})
	for _, w in waves do if w.roar then w.roarBase = w.roar.Volume w.roar.Volume = 0 end end

	-- the hatch: a Storm egg + Thunder Rex (the 1% secret of the Storm egg)
	local base
	do
		local bases = workspace.Map.Hub:FindFirstChild("Bases")
		local id = player:GetAttribute("BaseId")
		base = bases and (bases:FindFirstChild("Base" .. tostring(id)) or bases:FindFirstChild("Base2"))
	end
	-- (2026-10-21) redesigned hub: the giant pumpkin moved (S10 is relative to it); read it once per play
	local pumpkinPivot = workspace:FindFirstChild("HalloweenDecor") and workspace.HalloweenDecor:FindFirstChild("GiantPumpkin")
	pumpkinPivot = pumpkinPivot and pumpkinPivot:FindFirstChild("Pivot")
	local PUMPKIN_AT = pumpkinPivot and pumpkinPivot.Position or V(0, 64, 230)
	local hatchPos, hatchFront = V(-6, 0, 60), V(0, 0, -1)
	if base then
		-- (2026-10-21) the hatch stands on the fenced floor's centre (Plot now also holds Look.SlotBed, so the plot's
		-- bounding box is the whole 60x90 slot) and faces the plaza along the slot's facing (any of the 6 plots)
		local plot = base:FindFirstChild("Plot")
		local floor = plot and plot:FindFirstChild("Floor")
		local slot = base:FindFirstChild("Slot")
		if floor then
			hatchPos = (floor.CFrame * CFrame.new(0, floor.Size.Y / 2, 0)).Position
		end
		local look = slot and slot.CFrame.LookVector * V(1, 0, 1)
		if look and look.Magnitude > 0.1 then
			hatchFront = look.Unit
		else
			hatchFront = (V(0, 0, 20) - V(hatchPos.X, 0, hatchPos.Z)).Unit -- towards the plaza
		end
	end
	local hatchYaw = yawOf(hatchFront)
	local stormEgg = strip(Assets.StormEgg:Clone())
	stormEgg:ScaleTo(1.25)
	stormEgg.Parent = scene
	local seCF, seSize = stormEgg:GetBoundingBox()
	local seOff = seCF.Position - stormEgg:GetPivot().Position
	local seParts = {}
	for _, d in stormEgg:GetDescendants() do if d:IsA("BasePart") then seParts[d] = d.Transparency end end
	local function placeStormEgg(cf) stormEgg:PivotTo(cf * CFrame.new(-seOff)) end
	placeStormEgg(PARK)
	local eggGlow = Instance.new("PointLight")
	eggGlow.Color = Color3.fromRGB(120, 210, 255)
	eggGlow.Range = 16
	eggGlow.Brightness = 0
	eggGlow.Parent = fxHost

	local pets = {}
	local function makePet(name, scale)
		local src = CreatureModels:FindFirstChild(name)
		if not src then return nil end
		local m = strip(src:Clone())
		if scale and scale ~= 1 then m:ScaleTo(scale) end
		m.Parent = scene
		m:PivotTo(PARK)
		local ok, anim = pcall(CreatureAnimator.new, m)
		if not ok then anim = nil end
		local H = (m:GetAttribute("Height") or 10) * (scale or 1)
		if anim and PetEventFX then pcall(PetEventFX.bind, anim, m, name, H) end
		local pet = {model = m, anim = anim, H = H, name = name}
		pets[name] = pet
		return pet
	end
	-- real size: ScaleTo after import breaks CreatureAnimator's bone rest pose (the mesh explodes to 400 studs)
	local rex = makePet("ThunderRex")
	for _, s in PET_SPOTS do makePet(s.name) end

	-- the treadmill: the top tier (x20 Diamond Rainbow) on the middle hub treadmill's spot
	local tread = strip(Assets.Tier11_x20:Clone())
	tread.Parent = scene
	-- (2026-10-21) the player's own plot treadmill (else plot 1's)
	local treads = workspace.Map.Hub:FindFirstChild("Treadmills")
	local realTread = treads and (treads:FindFirstChild("Treadmill_B" .. tostring(player:GetAttribute("BaseId"))) or treads:FindFirstChild("Treadmill_B1"))
	local treadCF = realTread and realTread:GetPivot() or CFrame.lookAt(V(-107.7, 0.65, -46), V(-106.7, 0.65, -46))
	-- (2026-10-21) S8 films the treadmill from its plaza side (review SHOULD 8: plot 6 / plot 4 put the camera off the
	-- floor or inside a leaderboard when it always used the treadmill's +Right side)
	local treadSide = treadCF.RightVector:Dot(V(0, 0, 20) - treadCF.Position) >= 0 and 1 or -1
	tread:PivotTo(PARK)
	local treadHidden = {}
	local function showTread(on)
		tread:PivotTo(on and treadCF or PARK)
		if realTread then
			for _, d in realTread:GetDescendants() do
				if d:IsA("BasePart") or d:IsA("Decal") or d:IsA("Texture") then
					if on and not treadHidden[d] then treadHidden[d] = d.LocalTransparencyModifier d.LocalTransparencyModifier = 1
					elseif not on and treadHidden[d] then d.LocalTransparencyModifier = treadHidden[d] treadHidden[d] = nil end
				end
			end
		end
	end
	onEnd(function() showTread(false) end)
	local BELT_TOP = (treadCF.Position.Y + 0.6)

	-- the meteor shower: storm cloud + a big meteor (+ its trail) + impact
	local cloud = WA.Meteor.StormCloud:Clone()
	strip(cloud)
	cloud.Parent = scene
	cloud:PivotTo(PARK)
	local CLOUD_AT = CFrame.new(0, 96, -430)
	local meteor = WA.Meteor.MeteorBig:Clone()
	meteor.Anchored, meteor.CanCollide, meteor.CanQuery, meteor.CanTouch = true, false, false, false
	meteor.Size = meteor.Size * (9 / meteor.Size.X)
	meteor.CFrame = PARK
	meteor.Parent = scene
	local trailHead = FX.MeteorTrail:FindFirstChild("Head")
	local mHead
	if trailHead then
		mHead = trailHead:Clone()
		mHead.Parent = meteor
		for _, e in mHead:GetChildren() do if e:IsA("ParticleEmitter") then e.Enabled = false e.Size = scaleNS(e.Size, 2.4) end end
		local ml = Instance.new("PointLight") ml.Color = Color3.fromRGB(255, 150, 60) ml.Range = 34 ml.Brightness = 4 ml.Parent = meteor
	end
	local impact = simplePart({Size = V(1, 1, 1), Transparency = 1, CFrame = PARK})
	local impactAtt = Instance.new("Attachment") impactAtt.Parent = impact
	for _, e in FX.MeteorImpact:GetChildren() do
		local c = e:Clone()
		if c:IsA("ParticleEmitter") then c.Enabled = false elseif c:IsA("Light") then c.Enabled = false end
		c.Parent = impactAtt
	end
	local scorch = FX.MeteorScorch:Clone()
	local scorchPart = simplePart({Size = V(26, 0.2, 26), Transparency = 1, CFrame = PARK})
	if scorch:IsA("SurfaceGui") then scorch.Face = Enum.NormalId.Top scorch.Parent = scorchPart
	else for _, d in scorch:GetChildren() do if d:IsA("SurfaceGui") then d.Face = Enum.NormalId.Top d.Parent = scorchPart end end end
	local bolt = simplePart({Size = V(1, 1, 1), Transparency = 1, CFrame = PARK})
	local boltAtt = Instance.new("Attachment") boltAtt.Parent = bolt
	for _, e in FX.MeteorLightning:GetChildren() do
		local c = e:Clone()
		if c:IsA("ParticleEmitter") then c.Enabled = false elseif c:IsA("Light") then c.Enabled = false end
		c.Parent = boltAtt
	end
	local function emitAll(att, k)
		for _, e in att:GetChildren() do
			if e:IsA("ParticleEmitter") then e:Emit(math.max(1, math.floor((e.Rate > 0 and e.Rate * 0.15 or 12) * (k or 1)))) end
		end
	end
	local function lightPulse(att, len)
		for _, l in att:GetChildren() do
			if l:IsA("Light") then
				l.Enabled = true
				local b = l.Brightness
				task.delay(len, function() l.Enabled = false l.Brightness = b end)
			end
		end
	end

	-- the UFO: a saucer beams a wood egg up
	local saucer = WA.UFO.Saucer:Clone()
	strip(saucer)
	saucer:ScaleTo(1.9)
	saucer.Parent = scene
	saucer:PivotTo(PARK)
	local ufoEgg = IntroAssets.EggShell:Clone()
	ufoEgg:ScaleTo(0.75)
	strip(ufoEgg)
	ufoEgg.Parent = scene
	ufoEgg:PivotTo(PARK)
	local ufoEggCF, ufoEggSize = ufoEgg:GetBoundingBox()
	local ufoEggOff = ufoEggCF.Position - ufoEgg:GetPivot().Position
	local beamTop = simplePart({Size = V(1, 1, 1), Transparency = 1, CFrame = PARK})
	local beamBot = simplePart({Size = V(1, 1, 1), Transparency = 1, CFrame = PARK})
	local tb = FX.TractorBeam
	local topA, botA = tb.Top:Clone(), tb.Bottom:Clone()
	topA.Parent, botA.Parent = beamTop, beamBot
	for _, d in topA:GetChildren() do
		if d:IsA("Beam") then d.Attachment0 = topA d.Attachment1 = botA d.Enabled = false end
		if d:IsA("ParticleEmitter") then d.Enabled = false end
	end
	for _, d in botA:GetChildren() do if d:IsA("ParticleEmitter") then d.Enabled = false end end
	local function setBeam(on)
		for _, d in topA:GetChildren() do if d:IsA("Beam") or d:IsA("ParticleEmitter") then d.Enabled = on end end
		for _, d in botA:GetChildren() do if d:IsA("ParticleEmitter") then d.Enabled = on end end
	end

	-- the big-numbers egg: a Celestial egg at 1,000,000 KG
	local bigEgg = strip(Assets.CelestialEgg:Clone())
	bigEgg:ScaleTo(1.4)
	bigEgg.Parent = scene
	bigEgg:PivotTo(PARK)
	local beCF, beSize = bigEgg:GetBoundingBox()
	local beOff = beCF.Position - bigEgg:GetPivot().Position
	local beLabel = Instance.new("BillboardGui")
	beLabel.Name = "KgLabel"
	beLabel.Size = UDim2.fromScale(13, 4.4)
	beLabel.StudsOffsetWorldSpace = V(0, beSize.Y / 2 + 2.6, 0)
	beLabel.LightInfluence = 0
	beLabel.AlwaysOnTop = true
	beLabel.Enabled = false
	beLabel.Adornee = fxHost
	beLabel.Parent = pg -- (a BillboardGui inside a ScreenGui never draws)
	onEnd(function() beLabel:Destroy() end)
	do
		local function line(text, y, h, c1, c2, stroke)
			local l = Instance.new("TextLabel")
			l.BackgroundTransparency = 1
			l.AnchorPoint = Vector2.new(0.5, 0)
			l.Position = UDim2.fromScale(0.5, y)
			l.Size = UDim2.fromScale(1, h)
			l.Font = Enum.Font.GothamBlack
			l.TextScaled = true
			l.Text = text
			l.TextColor3 = Color3.new(1, 1, 1)
			l.Parent = beLabel
			local g = Instance.new("UIGradient") g.Rotation = 90 g.Color = ColorSequence.new(c1, c2) g.Parent = l
			local s = Instance.new("UIStroke") s.Thickness = stroke s.Color = Color3.fromRGB(15, 20, 30) s.LineJoinMode = Enum.LineJoinMode.Round s.Parent = l
			return l
		end
		line("CELESTIAL EGG", 0, 0.36, Color3.fromRGB(255, 250, 220), Color3.fromRGB(255, 205, 90), 3)
		line("1,000,000 KG", 0.38, 0.62, Color3.fromRGB(255, 255, 255), Color3.fromRGB(150, 230, 255), 4)
	end

	------------------------------------------------ captions + title
	local LUCKY = Font.fromEnum(Enum.Font.LuckiestGuy)
	local captions = {}
	local function makeCaption(text, t0, dur, sub, subColor)
		local holder = Instance.new("Frame")
		holder.BackgroundTransparency = 1
		holder.AnchorPoint = Vector2.new(0.5, 0.5)
		holder.Position = UDim2.fromScale(0.5, 0.8)
		holder.Size = UDim2.fromScale(0.9, 0.13)
		holder.Visible = false
		holder.ZIndex = 20
		holder.Parent = gui
		local l = Instance.new("TextLabel")
		l.BackgroundTransparency = 1
		l.Size = UDim2.fromScale(1, 1)
		l.FontFace = LUCKY
		l.TextScaled = true
		l.Text = text
		l.TextColor3 = Color3.new(1, 1, 1)
		l.ZIndex = 21
		l.Parent = holder
		local g = Instance.new("UIGradient")
		g.Rotation = 90
		g.Color = ColorSequence.new(Color3.fromRGB(255, 255, 255), Color3.fromRGB(255, 226, 120))
		g.Parent = l
		local s = Instance.new("UIStroke")
		s.Thickness = 6
		s.Color = Color3.fromRGB(16, 22, 34)
		s.LineJoinMode = Enum.LineJoinMode.Round
		s.Parent = l
		local subL
		if sub then
			subL = Instance.new("TextLabel")
			subL.BackgroundTransparency = 1
			subL.AnchorPoint = Vector2.new(0.5, 0)
			subL.Position = UDim2.fromScale(0.5, 1.02)
			subL.Size = UDim2.fromScale(1, 0.42)
			subL.FontFace = LUCKY
			subL.TextScaled = true
			subL.Text = sub
			subL.TextColor3 = subColor or Color3.fromRGB(255, 214, 80)
			subL.ZIndex = 21
			subL.Parent = holder
			local s2 = Instance.new("UIStroke") s2.Thickness = 4 s2.Color = Color3.fromRGB(16, 22, 34) s2.LineJoinMode = Enum.LineJoinMode.Round s2.Parent = subL
		end
		local sc = Instance.new("UIScale") sc.Scale = 1 sc.Parent = holder
		table.insert(captions, {holder = holder, label = l, stroke = s, sub = subL, scale = sc, t0 = t0, t1 = t0 + dur})
	end
	makeCaption("LAUNCH", T.cut1 + 0.05, 1.6)
	makeCaption("GRAB AN EGG", T.cut2 + 0.7, 1.55)
	makeCaption("OUTRUN THE TSUNAMI", T.cut3 + 0.25, 2.3)
	makeCaption("HATCH FIERCE PETS", T.burst + 0.12, 1.45, "THUNDER REX  -  SECRET", Color3.fromRGB(255, 214, 80))
	makeCaption("TRAIN YOUR SPEED", T.cut8 + 0.1, 1.95)
	makeCaption("METEOR SHOWERS", T.cut9 + 0.15, 1.8)
	makeCaption("UFO INVASIONS", T.cut10 + 0.1, 1.7)
	makeCaption("HALLOWEEN HUB", T.cut11 + 0.25, 2.5)
	local function drawCaptions(t)
		for _, c in captions do
			local on = t >= c.t0 and t < c.t1
			c.holder.Visible = on
			if on then
				local a = t - c.t0
				local out = math.max(0, t - (c.t1 - 0.22)) / 0.22
				c.scale.Scale = (a < 0.16 and lerp(1.55, 0.94, P.easeOut(a / 0.16)) or lerp(0.94, 1, ramp(a, 0.16, 0.3))) + 0.06 * out
				c.holder.Rotation = lerp(-6, -2, ramp(a, 0, 0.2))
				local tr = out
				c.label.TextTransparency, c.stroke.Transparency = tr, tr
				if c.sub then c.sub.TextTransparency = math.max(tr, 1 - ramp(a, 0.12, 0.3)) end
			end
		end
	end

	-- money counter (big numbers shot)
	local money = Instance.new("Frame")
	money.BackgroundTransparency = 1
	money.AnchorPoint = Vector2.new(0.5, 0.5)
	money.Position = UDim2.fromScale(0.5, 0.8)
	money.Size = UDim2.fromScale(0.6, 0.15)
	money.Visible = false
	money.ZIndex = 20
	money.Parent = gui
	local moneyL = Instance.new("TextLabel")
	moneyL.BackgroundTransparency = 1
	moneyL.Size = UDim2.fromScale(1, 1)
	moneyL.FontFace = LUCKY
	moneyL.TextScaled = true
	moneyL.TextColor3 = Color3.new(1, 1, 1)
	moneyL.ZIndex = 21
	moneyL.Parent = money
	do
		local g = Instance.new("UIGradient") g.Rotation = 90 g.Color = ColorSequence.new(Color3.fromRGB(200, 255, 140), Color3.fromRGB(60, 200, 40)) g.Parent = moneyL
		local s = Instance.new("UIStroke") s.Thickness = 6 s.Color = Color3.fromRGB(14, 40, 10) s.LineJoinMode = Enum.LineJoinMode.Round s.Parent = moneyL
	end
	local moneySc = Instance.new("UIScale") moneySc.Parent = money
	local function fmtMoney(v)
		local units = {{1e12, "T"}, {1e9, "B"}, {1e6, "M"}, {1e3, "K"}}
		for _, u in units do if v >= u[1] then return ("$%.2f%s"):format(v / u[1], u[2]) end end
		return ("$%d"):format(v)
	end

	local title = Instance.new("Frame")
	title.BackgroundTransparency = 1
	title.Size = UDim2.fromScale(1, 1)
	title.Visible = false
	title.ZIndex = 25
	title.Parent = gui
	local shade = Instance.new("Frame")
	shade.BackgroundColor3 = Color3.new(0, 0, 0)
	shade.BorderSizePixel = 0
	shade.Size = UDim2.fromScale(1, 1)
	shade.ZIndex = 25
	shade.Parent = title
	do
		local g = Instance.new("UIGradient")
		g.Rotation = 90
		g.Transparency = NumberSequence.new({NumberSequenceKeypoint.new(0, 1), NumberSequenceKeypoint.new(0.45, 0.75), NumberSequenceKeypoint.new(1, 0.25)})
		g.Parent = shade
	end
	local icon = Instance.new("ImageLabel")
	icon.BackgroundTransparency = 1
	icon.AnchorPoint = Vector2.new(0.5, 0.5)
	icon.Position = UDim2.fromScale(0.5, 0.36)
	icon.Size = UDim2.fromScale(0.15, 0.15)
	icon.SizeConstraint = Enum.SizeConstraint.RelativeXX
	icon.Image = ("rbxthumb://type=GameIcon&id=%d&w=512&h=512"):format(game.GameId)
	icon.ZIndex = 27
	icon.Parent = title
	do
		local c = Instance.new("UICorner") c.CornerRadius = UDim.new(0.18, 0) c.Parent = icon
		local s = Instance.new("UIStroke") s.Thickness = 6 s.Color = Color3.fromRGB(16, 22, 34) s.Parent = icon
	end
	local iconSc = Instance.new("UIScale") iconSc.Parent = icon
	local logo = Instance.new("TextLabel")
	logo.BackgroundTransparency = 1
	logo.AnchorPoint = Vector2.new(0.5, 0.5)
	logo.Position = UDim2.fromScale(0.5, 0.66)
	logo.Size = UDim2.fromScale(0.82, 0.2)
	logo.FontFace = LUCKY
	logo.TextScaled = true
	logo.Text = "SLINGSHOT"
	logo.TextColor3 = Color3.new(1, 1, 1)
	logo.ZIndex = 27
	logo.Parent = title
	do
		local g = Instance.new("UIGradient") g.Rotation = 90 g.Color = ColorSequence.new(Color3.fromRGB(255, 248, 200), Color3.fromRGB(255, 170, 30)) g.Parent = logo
		local s = Instance.new("UIStroke") s.Thickness = 9 s.Color = Color3.fromRGB(16, 22, 34) s.LineJoinMode = Enum.LineJoinMode.Round s.Parent = logo
	end
	local logoSc = Instance.new("UIScale") logoSc.Parent = logo
	local sub = Instance.new("TextLabel")
	sub.BackgroundTransparency = 1
	sub.AnchorPoint = Vector2.new(0.5, 0.5)
	sub.Position = UDim2.fromScale(0.5, 0.81)
	sub.Size = UDim2.fromScale(0.5, 0.09)
	sub.FontFace = LUCKY
	sub.TextScaled = true
	sub.Text = "FOR EGGS"
	sub.TextColor3 = Color3.new(1, 1, 1)
	sub.ZIndex = 27
	sub.Parent = title
	do
		local g = Instance.new("UIGradient") g.Rotation = 90 g.Color = ColorSequence.new(Color3.fromRGB(200, 245, 255), Color3.fromRGB(40, 190, 255)) g.Parent = sub
		local s = Instance.new("UIStroke") s.Thickness = 6 s.Color = Color3.fromRGB(16, 22, 34) s.LineJoinMode = Enum.LineJoinMode.Round s.Parent = sub
	end

	------------------------------------------------ line of sight: props between the camera and the subject fade (as the intro)
	local occluders = {}
	do
		local roots = {workspace:FindFirstChild("HalloweenDecor")}
		local runway = workspace.Map:FindFirstChild("Runway")
		local grass = runway and runway:FindFirstChild("Area1_Grass")
		if grass then table.insert(roots, grass:FindFirstChild("Ground")) table.insert(roots, grass:FindFirstChild("Decor")) end
		local hub = workspace.Map:FindFirstChild("Hub")
		if hub then table.insert(roots, hub:FindFirstChild("Decor")) table.insert(roots, hub:FindFirstChild("MarketCorners")) end
		local groups = {}
		for _, r in roots do
			for _, d in r:GetDescendants() do
				if d:IsA("BasePart") and d.Transparency < 1 and d.Size.Magnitude < 40 then
					local top = d
					while top.Parent and top.Parent ~= r and not top.Parent:IsA("Folder") do top = top.Parent end
					local g = groups[top]
					if not g then g = {parts = {}, mn = d.Position, mx = d.Position} groups[top] = g end
					table.insert(g.parts, d)
					local h = d.Size / 2
					g.mn, g.mx = g.mn:Min(d.Position - h), g.mx:Max(d.Position + h)
				end
			end
		end
		for _, g in groups do
			local size = g.mx - g.mn
			if size.Y > 0.8 and size.Magnitude < 45 then
				table.insert(occluders, {parts = g.parts, pos = (g.mn + g.mx) / 2, r = size.Magnitude / 2})
			end
		end
	end
	local faded = {}
	local function clearView(camPos, target)
		local dir = target - camPos
		local dist = dir.Magnitude
		if dist < 0.1 then return end
		dir /= dist
		for _, o in occluders do
			local rel = o.pos - camPos
			local s = rel:Dot(dir)
			local block = rel.Magnitude < o.r + 2.5
			if not block and s > -o.r and s < dist - 1.5 then block = (rel - dir * s).Magnitude < o.r + 0.6 end
			if block ~= (faded[o] == true) then
				faded[o] = block or nil
				for _, p in o.parts do p.LocalTransparencyModifier = block and 1 or 0 end
			end
		end
	end
	onEnd(function() for o in faded do for _, p in o.parts do if p.Parent then p.LocalTransparencyModifier = 0 end end end end)

	------------------------------------------------ the performance: puppet + props at content time t
	local fired = {}
	local function once(key) if fired[key] then return false end fired[key] = true return true end
	local shakeAmt = 0
	local function shake(a) shakeAmt = math.max(shakeAmt, a) end

	local function flyAt(s) -- s = seconds since the release
		local a, b = POUCH0 + PULL + V(0, SEAT_UP, 0), LAND + V(0, H0, 0)
		local u = math.clamp(s / FLY, 0, 1)
		local hA = 55
		local pos = a:Lerp(b, u) + V(0, 4 * hA * u * (1 - u), 0)
		local vel = ((b - a) + V(0, 4 * hA * (1 - 2 * u), 0)) / FLY
		return pos, vel, u
	end

	local puppetCF, eggMode = PARK, "park"
	local function perform(t, dt)
		local pose, root = P.STAND, nil
		local egg = "park"
		setTrails(false)
		if t < T.cut2 then
			-- S1 + S2: in the pouch, pulled back, RELEASE on the drop, flight
			if t < T.release then
				local u = ramp(t, T.pull0, T.release - 0.1)
				local tremble = V(noise(t * 9, 3), noise(t * 9, 4), 0) * 0.14 * ramp(t, 1.0, T.release)
				local pp = POUCH0 + PULL * P.easeOut(u) + tremble
				drawSling(pp)
				pose = P.add(P.POUCH, P.breath(t, 1.5 * ramp(t, 0.8, 2), 3))
				root = CFrame.new(pp + V(0, SEAT_UP, 0))
				if t > T.pull0 and once("stretch") then slingSound("Stretch", 1.2) end
			else
				local s = t - T.release
				local pos, vel, u = flyAt(s)
				local yA = vel.Unit
				local zA = (Vector3.yAxis - yA * Vector3.yAxis:Dot(yA))
				zA = zA.Magnitude > 1e-3 and zA.Unit or Vector3.zAxis
				local fly = CFrame.fromMatrix(pos, yA:Cross(zA), yA, zA)
				root = CFrame.new(pos):Lerp(fly, math.min(ramp(u, 0, 0.05), 1 - ramp(u, 0.85, 0.98)))
				local flap = P.add(P.SUPERMAN, {LeftKnee = V(10 * math.sin(t * 9), 0, 0), RightShoulder = V(0, 0, 3 * math.sin(t * 13)), LeftShoulder = V(0, 0, -3 * math.sin(t * 11))})
				pose = P.blend(P.POUCH, flap, ramp(u, 0, 0.06))
				setTrails(u > 0.02)
				drawSling(POUCH0 + PULL * math.exp(-6 * s) * math.cos(20 * s))
				if once("release") then
					slingSound("Release", 1.3) slingSound("Whoosh", 1.2)
					shake(1.2)
				end
			end
		elseif t < T.cut3 then
			-- S3: superhero landing, grab the egg
			drawSling(POUCH0)
			if t < T.land then
				local s = t - T.release
				local pos, vel, u = flyAt(s)
				local yA = vel.Unit
				local zA = (Vector3.yAxis - yA * Vector3.yAxis:Dot(yA))
				zA = zA.Magnitude > 1e-3 and zA.Unit or Vector3.zAxis
				root = CFrame.new(pos):Lerp(CFrame.fromMatrix(pos, yA:Cross(zA), yA, zA), 1 - ramp(u, 0.8, 0.97))
				pose = P.blend(P.SUPERMAN, P.LAND3, ramp(u, 0.85, 1))
				setTrails(u < 0.92)
				egg = "ground"
			else
				if once("land") then
					slingSound("Land", 1.4)
					burst(dust, LAND + V(0, 0.4, 0), 40, 1.4) burst(ring, LAND + V(0, 0.3, 0), 3)
					shake(1.6)
				end
				local squash = P.add(P.LAND3, {off = V(0, -0.35, 0), Root = V(-6, 0, 0)}, math.exp(-(t - T.land) * 9))
				if t < T.eggGo then
					pose = P.blend(squash, P.add(P.STAND, {Neck = V(-6, 0, 0)}), ramp(t, T.rise, T.eggGo))
					root = CFrame.new(LAND + V(0, H0, 0)) * CFrame.Angles(0, lerpAngle(0, yawOf(GRAB - LAND), ramp(t, T.rise, T.eggGo)), 0)
					egg = "ground"
				elseif t < T.reach then
					local u = (t - T.eggGo) / (T.reach - T.eggGo)
					local pos = LAND:Lerp(GRAB, smooth(u))
					local ph = runPhase(pos, CYCLE * 0.8)
					pose = P.blend(P.run(ph, 0.75), P.REACH, ramp(u, 0.7, 1))
					root = CFrame.new(pos + V(0, H0, 0)) * CFrame.Angles(0, yawOf(EGG - GRAB), 0)
					egg = "ground"
				else
					local liftU = ramp(t, T.reach + 0.1, T.held)
					pose = P.blend(P.REACH, P.LIFT, liftU)
					if t > T.held then pose = P.add(P.LIFT, P.breath(t, 1, 0.8)) end
					root = CFrame.new(GRAB + V(0, H0, 0)) * CFrame.Angles(0, yawOf(EGG - GRAB), 0)
					egg = liftU < 1 and "lift" or "held"
					if liftU > 0.3 and once("pickup") then sfx("Pickup", 0.9) end
					eggMode = liftU
				end
			end
		elseif t < T.cut5 then
			-- S4: sprint for the trench with the tsunami behind, drop in, the wave rolls over, climb out
			local w = warp(t)
			local z
			if w < W.rim then
				z = GRAB.Z + RUN_V * (w - T.cut3)
				local pos = V(GRAB.X, 0, z)
				local ph = runPhase(pos, CYCLE)
				pose = P.layer(P.run(ph, 1), P.carry(math.cos(ph * 2)), 1, P.ARMS)
				local lb = math.min(ramp(w, 8.0, 8.15), 1 - ramp(w, 8.45, 8.6))
				if lb > 0 then pose = P.add(pose, P.lookBack(1), lb) end
				root = CFrame.new(pos + V(0, H0, 0)) * CFrame.Angles(0, math.pi, 0)
			elseif w < W.out0 then
				local u = math.clamp((w - W.rim) / (W.bottom - W.rim), 0, 1)
				local zz = lerp(TRENCH_RIM - 0.8, -262.5, u)
				local y = lerp(0, TRENCH_FLOOR, u * u) + 2.2 * 4 * u * (1 - u)
				pose = P.blend(P.JUMP_TUCK, P.add(P.LAND_SOFT, {off = V(0, -0.5, 0), Root = V(-12, 0, 0), Neck = V(20, 0, 0)}), ramp(u, 0.6, 1))
				if w > W.bottom then pose = P.add(pose, P.breath(w, 2.5, 1.6)) end
				root = CFrame.new(V(GRAB.X, y + H0, zz)) * CFrame.Angles(0, math.pi, 0)
				if u >= 1 and once("trenchland") then burst(dust, V(GRAB.X, TRENCH_FLOOR + 0.4, -262.5), 14) end
			else
				local u = math.clamp((w - W.out0) / (W.out1 - W.out0), 0, 1)
				local zz = lerp(-262.5, TRENCH_FAR + 1.5, u)
				local y = lerp(TRENCH_FLOOR, 0, smooth(u)) + 2.5 * 4 * u * (1 - u)
				if w > W.out1 then zz = TRENCH_FAR + 1.5 + RUN_V * (w - W.out1) y = 0 end
				local pos = V(GRAB.X, y, zz)
				local ph = runPhase(pos, CYCLE)
				pose = P.blend(P.JUMP_PUSH, P.layer(P.run(ph, 1), P.carry(math.cos(ph * 2)), 1, P.ARMS), ramp(w, W.out1 - 0.1, W.out1 + 0.1))
				root = CFrame.new(pos + V(0, H0, 0)) * CFrame.Angles(0, math.pi, 0)
			end
			egg = "held"
			drawWave(wave1, waveFront(w))
			if w > W.front - 0.05 and once("over") then shake(1.4) sfx("Splash", 1.2, 0.8) end
		elseif t < T.cut6 then
			-- S5: through the gate, the egg banks, the second wave crashes behind
			drawWave(wave1, nil)
			local z = GATE_Z - 24 * (T.gate - t)
			local pos = V(-2, 0, z)
			local ph = runPhase(pos, CYCLE)
			pose = P.run(ph, 1)
			local carryW = 1 - ramp(t, T.gate, T.gate + 0.25)
			if carryW > 0 then pose = P.layer(pose, P.carry(math.cos(ph * 2)), carryW, P.ARMS) end
			root = CFrame.new(pos + V(0, H0, 0)) * CFrame.Angles(0, math.pi, 0)
			egg = t < T.gate and "held" or (t < T.gate + 0.3 and "bank" or "park")
			eggMode = (t - T.gate) / 0.3
			if t > T.gate and once("bank") then sfx("Bank", 1) end
			drawWave(wave2, GATE_Z - 1 + WAVE.speed * (t - T.crash), END_Z)
			if t > T.crash and once("crash") then shake(1.3) sfx("Splash", 1.3) end
		elseif t >= T.cut8 and t < T.cut9 then
			-- S8: the treadmill
			drawWave(wave2, nil)
			local pos = treadCF.Position + V(0, BELT_TOP - treadCF.Position.Y, 0)
			phase += dt * 2 * math.pi * 2.3
			pose = P.add(P.run(phase, 1), {Neck = V(-4, 0, 0)})
			root = CFrame.new(pos + V(0, H0, 0)) * (treadCF - treadCF.Position)
		elseif t >= T.title then
			-- S12: the hero on the launch pad, under the slingshot
			local padY = groundAt(V(0.5, 10, -50), 1)
			pose = P.add(P.RELIEF, P.breath(t, 1.2, 0.45))
			root = CFrame.new(V(0.5, padY + H0, -50))
		end
		if root then rig.hrp.CFrame = root P.apply(rig, pose) else rig.hrp.CFrame = PARK end
		puppetCF = root or PARK
		-- the runway egg
		if egg == "ground" then
			placeEgg(eggRest)
		elseif egg == "lift" or egg == "held" or egg == "bank" then
			local headCF = P.fk(rig, head, root)
			local over = headCF.Position + V(0, 1.2 + eggSize.Y / 2, 0)
			if egg == "lift" then over = eggRest:Lerp(over, smooth(eggMode)) end
			if egg == "bank" then
				local k = math.clamp(eggMode, 0, 1)
				over += V(0, 3 * k, 0)
				egg = k < 1 and "held" or "park"
			end
			if egg ~= "park" then placeEgg(over) end
		end
		if egg == "park" then placeEgg(PARK.Position) end
		return root
	end

	------------------------------------------------ the shots: camera at time t -> CFrame, fov, focus point
	local function look(pos, at, roll) return CFrame.lookAt(pos, at) * CFrame.Angles(0, 0, roll or 0) end
	local hookCam = V(3.2, 24, -51) -- in front of the fork, on the flight line: the launch goes right over the lens
	local function camAt(t)
		local root = puppetCF.Position
		if t < T.cut1 then -- S1 HOOK: in front of the slingshot, on the flight line, looking back at the pouch
			local at = POUCH0 + PULL * 0.8 + V(0, SEAT_UP + 0.6, 0)
			if t > T.release then at = at:Lerp(root, 0.35 * ramp(t, T.release, T.release + 0.3)) end
			local fov = lerp(46, 36, ramp(t, 0, T.release)) + 26 * ramp(t, T.release, T.release + 0.18)
			local p = hookCam + V(noise(t * 2, 7) * 0.25, noise(t * 2, 8) * 0.2, 0)
			return look(p, at, 0.04 * math.sin(t * 0.7)), fov, at
		elseif t < T.cut2 then -- S2 FLIGHT: chase cam behind + above, the runway ahead
			local s = t - T.release
			local pos, vel = flyAt(s)
			local dir = vel.Unit
			local flat = V(dir.X, 0, dir.Z).Unit
			local p = pos - flat * 15 + V(3.5, 6.5, 0)
			local at = pos + flat * 30 + V(0, -10 - 6 * ramp(t, T.cut1, T.cut2), 0)
			return look(p, at, -0.08 + 0.05 * math.sin(t * 2.2)), 74, pos
		elseif t < T.cut3 then -- S3: low wide at the landing, dolly in for the grab
			local u = ramp(t, T.cut2, T.cut3)
			local p = LAND + V(11 + 4 * u, 1.6 + 1.2 * u, 13 + 4 * u)
			local at = (t < T.land) and LAND + V(0, 4 + 10 * (1 - ramp(t, T.cut2, T.land)), 0) or root + V(0, 0.8, 0)
			if t > T.land - 0.05 then at = (LAND + V(0, 3, 0)):Lerp(GRAB + V(0, 4.5, 0), ramp(t, T.land, T.held)) end
			return look(p, at), 56, at
		elseif t < T.cut4 then -- S4a: low in front of the runner, the tsunami growing behind
			local p = root + V(-4.5, -0.4, 15)
			local at = root + V(1, 1.5, -18)
			return look(p, at, 0.03), 66, root
		elseif t < T.cut5 then -- S4b: high crane over the trench as the wave rolls across
			local w = warp(t)
			local u = ramp(w, W.rim - 0.2, W.out1 + 0.4)
			local p = V(46, 40, -206) + V(0, 2 * u, 3 * u)
			local at = V(GRAB.X, -1, -264)
			return look(p, at, -0.04), lerp(50, 42, u), at
		elseif t < T.cut6 then -- S5: in the hub, low at the gate, the runner bursts through towards us
			local p = V(5, 2.2, -50 + 3 * ramp(t, T.cut5, T.cut6))
			local at = V(-2, 3.2, -70)
			if t > T.gate then at = at:Lerp(root + V(0, 2, 0), ramp(t, T.gate, T.cut6)) end
			return look(p, at), 70, root
		elseif t < T.cut7 then -- S6 HATCH: slow push-in on the egg, pull back + low on the burst
			local fwd = hatchFront
			local side = fwd:Cross(Vector3.yAxis)
			local center = hatchPos + V(0, 3, 0)
			if t < T.burst then
				local u = ramp(t, T.cut6, T.burst)
				local p = hatchPos + fwd * lerp(12, 8.5, u) + side * lerp(3, 2, u) + V(0, lerp(3, 2.6, u), 0)
				return look(p, center), lerp(55, 46, u), center
			else
				local u = ramp(t, T.burst, T.burst + 1.6)
				local p = hatchPos + fwd * lerp(11, 13.5, u) + side * lerp(-4, -5.5, u) + V(0, 1.4, 0)
				return look(p, hatchPos + V(0, 5.5, 0)), 58, center
			end
		elseif t < T.cut8 then -- S7: three secret pets in their own worlds
			local i = t < PET_SPOTS[2].t0 and 1 or (t < PET_SPOTS[3].t0 and 2 or 3)
			local spot = PET_SPOTS[i]
			local pet = pets[spot.name]
			local H = pet and pet.H or 10
			local c = spot.at or spot.pos
			local a = 0.6 + (t - spot.t0) * 0.35 + i
			local r = H * 2.4
			local p = c + V(math.sin(a) * r, H * 0.4, math.cos(a) * r)
			local at = c + V(0, H * 0.6, 0)
			return look(p, at), 58, at
		elseif t < T.cut9 then -- S8 TREADMILL: low side tracking
			local u = ramp(t, T.cut8, T.cut9)
			local c = treadCF.Position + V(0, 4, 0)
			local p = c + treadCF:VectorToWorldSpace(V(treadSide * (16 - 2 * u), 5, -8 + 3 * u))
			return look(p, c + V(0, -0.2, 0)), 46, c
		elseif t < T.cut10 then -- S9a METEOR: low on the runway, the storm overhead
			local u = ramp(t, T.cut9, T.cut10)
			local p = V(30, 5, -128 + 4 * u)
			local at = V(-4, 20 - 14 * ramp(t, T.strike - 0.7, T.strike), -195)
			return look(p, at, 0.02), 62, at
		elseif t < T.cut11 then -- S9b UFO: under the saucer, the egg rising
			local u = ramp(t, T.cut10, T.cut11)
			local p = V(12, 2.2, -150 + 2 * u)
			local at = V(-2, 9 + 8 * u, -176)
			return look(p, at, -0.03), 60, at
		elseif t < T.cut12 then -- S10 HALLOWEEN: drone glide across the plaza up to the giant jack-o'-lantern
			-- (2026-10-21) relative to the giant pumpkin (it moved with the redesigned hub); with the old pivot (0, 64, 169) this
			-- is exactly the old path (-14,7,-44) -> (8,16,26) looking at (0, 18..58, 169)
			local u = smooth(ramp(t, T.cut11, T.cut12))
			local p = PUMPKIN_AT + V(-14 + 22 * u, -57 + 9 * u, -213 + 70 * u)
			local at = PUMPKIN_AT + V(0, lerp(-46, -6, u), 0)
			return look(p, at, 0.06 * (1 - u)), lerp(70, 58, u), at
		elseif t < T.title then -- S11 BIG NUMBERS: orbit the 1,000,000 KG egg
			local u = ramp(t, T.cut12, T.title)
			local c = hatchPos + V(0, beSize.Y / 2, 0)
			local a = hatchYaw + 0.5 - 0.8 * u
			local r = 16 - 2 * u
			local p = c + V(-math.sin(a) * r, 1.5 + 1.5 * u, -math.cos(a) * r)
			return look(p, c + V(0, 2.4, 0)), 56, c
		else -- S12 TITLE: rise + pull back from the hero on the pad, the slingshot + the giant pumpkin behind
			local u = smooth(ramp(t, T.title, T.fade1))
			local p = V(16, 11, -70):Lerp(V(24, 30, -104), u)
			local at = V(0, 13, -12):Lerp(V(0, 24, 26), u)
			return look(p, at), 62, V(0.5, 4, -50)
		end
	end

	------------------------------------------------ the per-shot world (props in/out at the cuts)
	local function stepPet(pet, dt, mode)
		if pet and pet.anim then pcall(pet.anim.step, pet.anim, dt, {mode = mode, dist = 0, speed = 0, climb = 0}) end
	end
	local gate = workspace.Map:FindFirstChild("Runway") and workspace.Map.Runway:FindFirstChild("LaunchGate")
	local gateWas = gate and gate.LocalTransparencyModifier or 0
	onEnd(function() if gate and gate.Parent then gate.LocalTransparencyModifier = gateWas end end)
	local function world(t, dt)
		-- the gate opens up while the runner bursts through it; the waves leave after their shots
		if gate then gate.LocalTransparencyModifier = ((t >= T.cut5 and t < T.cut6) or t >= T.title) and 1 or gateWas end
		if t >= T.cut6 and not fired.wavesOff then
			fired.wavesOff = true
			drawWave(wave1, nil) drawWave(wave2, nil)
		end
		-- the hatch
		if t >= T.cut6 and t < T.cut7 then
			hideBases(true)
			local base = CFrame.new(hatchPos + V(0, seSize.Y / 2, 0)) * CFrame.Angles(0, hatchYaw, 0)
			if t < T.burst then
				local wob = 0
				for i, tw in {T.wob1, T.wob2, T.wob3} do
					local s = t - tw
					if s > 0 and s < 0.5 then wob += math.sin(s * 34) * math.exp(-s * 6) * (0.16 + 0.05 * i) end
					if s > 0 and once("crack" .. i) then sfx("Crack", 1, 0.9 + 0.1 * i) burst(sparkle, hatchPos + V(0, seSize.Y * 0.6, 0), 8 + 6 * i) end
				end
				placeStormEgg(base * CFrame.Angles(wob, 0, wob * 0.6))
				eggGlow.Brightness = 3 * ramp(t, T.wob1, T.burst)
				fxHost.CFrame = CFrame.new(hatchPos + V(0, 3, 0))
				if once("heart") then sfx("Heartbeat", 1) end
				rex.model:PivotTo(PARK)
			else
				if once("burst") then
					placeStormEgg(PARK)
					eggGlow.Brightness = 0
					doFlash(0.28)
					shake(1.8)
					burst(ring, hatchPos + V(0, 1, 0), 4, 1.4) burst(sparkle, hatchPos + V(0, 4, 0), 60) burst(zap, hatchPos + V(0, 5, 0), 6)
					burst(dust, hatchPos + V(0, 0.5, 0), 30)
					sfx("HatchWin", 1) sfx("Crack", 1.2, 0.7)
					if rex.anim then rex.anim:play("roar") end
				end
				-- the pet appears under the flash (no scale pop: scaling an animated rig mid-clip is unsafe)
				local toCam = hatchFront * 12 - hatchFront:Cross(Vector3.yAxis) * 5 -- where the post-burst camera stands
				rex.model:PivotTo(CFrame.new(hatchPos) * CFrame.Angles(0, yawOf(toCam) + REX_YAW, 0)) -- faces the camera
				stepPet(rex, dt, "ground")
			end
		elseif t >= T.cut7 then
			if t < T.cut12 then hideBases(false) end
			rex.model:PivotTo(PARK)
			stormEgg:PivotTo(PARK)
		end
		-- the pet cuts (pre-roll their acts 1.2 s before they're seen)
		for i, s in PET_SPOTS do
			local pet = pets[s.name]
			if pet then
				local on = t >= s.t0 - 1.2 and t < (PET_SPOTS[i + 1] and PET_SPOTS[i + 1].t0 or T.cut8)
				if on then
					if not s.at then
						local y = groundAt(s.pos, nil)
						s.at = y and V(s.pos.X, y, s.pos.Z) or V(0, 0, -150)
						local a0 = 0.6 + 0.13 + i -- the camera's angle mid-cut (camAt S7): the pet faces the camera
						s.yaw = yawOf(V(math.sin(a0), 0, math.cos(a0)))
					end
					if once("act" .. i) and pet.anim then pet.anim:play(s.act) end
					local lift = s.air and pet.H * 0.25 or 0
					pet.model:PivotTo(CFrame.new(s.at + V(0, lift, 0)) * CFrame.Angles(0, (s.yaw or 0) + REX_YAW, 0))
					stepPet(pet, dt, s.mode or (s.air and "air" or "ground"))
				else
					pet.model:PivotTo(PARK)
				end
			end
		end
		-- the treadmill
		if t >= T.cut8 and t < T.cut9 then
			if once("treadOn") then showTread(true) end
			if math.floor(t * 6) ~= math.floor((t - dt) * 6) then
				local bb = Instance.new("BillboardGui")
				bb.Size = UDim2.fromScale(5, 1.6)
				bb.StudsOffsetWorldSpace = V(math.random(-12, 12) / 10, 2.2, 0)
				bb.LightInfluence = 0
				bb.AlwaysOnTop = true
				bb.Adornee = rig.hrp
				bb.Parent = pg
				local l = Instance.new("TextLabel")
				l.BackgroundTransparency = 1
				l.Size = UDim2.fromScale(1, 1)
				l.FontFace = LUCKY
				l.TextScaled = true
				l.Text = "+2M"
				l.TextColor3 = Color3.new(1, 1, 1)
				l.Parent = bb
				local g = Instance.new("UIGradient") g.Rotation = 90 g.Color = ColorSequence.new(Color3.fromRGB(200, 255, 140), Color3.fromRGB(60, 200, 40)) g.Parent = l
				local st = Instance.new("UIStroke") st.Thickness = 3 st.Color = Color3.fromRGB(14, 40, 10) st.Parent = l
				TweenService:Create(bb, TweenInfo.new(0.9, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {StudsOffsetWorldSpace = bb.StudsOffsetWorldSpace + V(0, 4.5, 0)}):Play()
				TweenService:Create(l, TweenInfo.new(0.9, Enum.EasingStyle.Quad, Enum.EasingDirection.In), {TextTransparency = 1}):Play()
				TweenService:Create(st, TweenInfo.new(0.9, Enum.EasingStyle.Quad, Enum.EasingDirection.In), {Transparency = 1}):Play()
				task.delay(1, function() bb:Destroy() end)
				sfx("Tick", 0.35, 1.2)
			end
		elseif fired.treadOn and not fired.treadOff then
			fired.treadOff = true
			showTread(false)
		end
		-- the meteor shower
		if t >= T.cut9 and t < T.cut10 then
			storm.Enabled = true
			storm.TintColor = Color3.fromRGB(205, 205, 230)
			storm.Brightness = -0.06
			storm.Saturation = -0.18
			cloud:PivotTo(CLOUD_AT)
			if once("thunder") then sfx("MeteorThunder1", 1) end
			local from, to = V(-30, 62, -262), V(-4, 0.5, -182)
			local m0 = T.strike - 0.75
			if t > m0 - 0.15 and once("glow") then boltAtt.Parent.CFrame = CFrame.new(from + V(0, 4, 0)) emitAll(boltAtt, 1) lightPulse(boltAtt, 0.35) sfx("MeteorRoar", 1) end
			if t >= m0 and t < T.strike then
				local u = (t - m0) / (T.strike - m0)
				local pos = from:Lerp(to, u * u)
				meteor.CFrame = CFrame.new(pos) * CFrame.Angles(t * 3, t * 2, 0)
				if mHead then mHead.WorldCFrame = CFrame.new(pos) for _, e in mHead:GetChildren() do if e:IsA("ParticleEmitter") then e.Enabled = true end end end
				if once("fall") then sfx("MeteorFall", 1) end
			else
				meteor.CFrame = PARK
				if mHead then for _, e in mHead:GetChildren() do if e:IsA("ParticleEmitter") then e.Enabled = false end end end
			end
			if t >= T.strike and once("impact") then
				impact.CFrame = CFrame.new(to)
				emitAll(impactAtt, 1.6)
				lightPulse(impactAtt, 0.4)
				scorchPart.CFrame = CFrame.new(to - V(0, 0.35, 0))
				doFlash(0.18)
				shake(2.4)
				sfx("MeteorImpact", 1.3)
			end
		elseif t >= T.cut10 and fired.thunder and not fired.stormOff then
			fired.stormOff = true
			storm.Enabled = false
			cloud:PivotTo(PARK)
			scorchPart.CFrame = PARK
		end
		-- the UFO
		if t >= T.cut10 and t < T.cut11 then
			local u = ramp(t, T.cut10, T.cut11)
			local sp = V(-2, 30 + math.sin(t * 2.2) * 0.8, -176)
			saucer:PivotTo(CFrame.new(sp) * CFrame.Angles(0, t * 1.4, math.sin(t * 1.7) * 0.05))
			beamTop.CFrame = CFrame.new(sp - V(0, 3.5, 0)) * CFrame.Angles(0, 0, math.pi)
			beamBot.CFrame = CFrame.new(V(-2, 0.3, -176)) * CFrame.Angles(0, 0, math.pi)
			if once("beam") then setBeam(true) sfx("UFOBeam", 1) sfx("UFOHum", 0.8) end
			local ey = lerp(ufoEggSize.Y / 2 + 0.2, 24, P.easeIn(ramp(t, T.cut10 + 0.25, T.cut11 + 0.4)))
			ufoEgg:PivotTo(CFrame.new(V(-2, ey, -176) - ufoEggOff) * CFrame.Angles(math.sin(t * 3) * 0.2, t * 2.5, 0))
		elseif fired.beam and not fired.ufoOff then
			fired.ufoOff = true
			setBeam(false)
			saucer:PivotTo(PARK)
			ufoEgg:PivotTo(PARK)
			beamTop.CFrame, beamBot.CFrame = PARK, PARK
		end
		-- the Halloween hub at golden hour
		clockWant = (t >= T.cut11 and t < T.cut12) and 17.55 or 14.6
		if Lighting.ClockTime ~= clockWant then Lighting.ClockTime = clockWant end
		-- big numbers
		if t >= T.cut12 and t < T.title then
			hideBases(true)
			bigEgg:PivotTo(CFrame.new(hatchPos + V(0, beSize.Y / 2, 0) - beOff) * CFrame.Angles(0, hatchYaw + 0.6, 0))
			fxHost.CFrame = CFrame.new(hatchPos + V(0, beSize.Y / 2, 0))
			beLabel.Enabled = true
			if once("bigEgg") then sfx("Place", 1) burst(sparkle, hatchPos + V(0, beSize.Y, 0), 40) end
			money.Visible = t >= T.money
			if money.Visible then
				local u = ramp(t, T.money, T.money + 0.9)
				moneyL.Text = fmtMoney(math.floor(1.25e12 * u * u))
				moneySc.Scale = lerp(1.4, 1, P.easeOut(ramp(t, T.money, T.money + 0.2))) + 0.05 * math.sin(math.max(0, t - T.money - 0.9) * 18) * math.exp(-math.max(0, t - T.money - 0.9) * 5)
				if math.floor(t * 12) ~= math.floor((t - dt) * 12) and u < 1 then sfx("Tick", 0.4, 0.9 + u) end
				if u >= 1 and once("cash") then sfx("Bank", 1.2) burst(sparkle, hatchPos + V(0, beSize.Y + 2, 0), 50) end
			end
		elseif t >= T.title and not fired.bigOff then
			fired.bigOff = true
			hideBases(false)
			bigEgg:PivotTo(PARK)
			beLabel.Enabled = false
			money.Visible = false
		end
		-- the title
		if t >= T.title then
			title.Visible = true
			local a = t - T.title
			shade.BackgroundTransparency = 1 - ramp(a, 0, 0.3)
			logoSc.Scale = a < 0.18 and lerp(1.7, 0.95, P.easeOut(a / 0.18)) or lerp(0.95, 1, ramp(a, 0.18, 0.35)) + 0.012 * a
			iconSc.Scale = P.easeOutBack(ramp(a, 0.12, 0.45), 2)
			logo.TextTransparency = 0
			sub.TextTransparency = 1 - ramp(a, 0.25, 0.5)
			if once("titleHit") then doFlash(0.22) shake(1) sfx("Rebirth", 0.8) end
		end
	end

	------------------------------------------------ go
	local cs = Instance.new("Folder") -- marker for other scripts
	cs.Name = "TrailerPlaying"
	cs.Parent = player
	onEnd(function() cs:Destroy() end)
	local abortConn = UserInputService.InputBegan:Connect(function(input)
		if input.KeyCode == Enum.KeyCode.Backspace then stopped = true end
	end)
	onEnd(function() abortConn:Disconnect() end)

	local t0w = os.clock()
	while not music.IsLoaded and os.clock() - t0w < 4 do task.wait() end
	music.TimePosition = MUSIC_AT - BLACK_IN
	music:Play()
	local clock0 = os.clock() + BLACK_IN -- content t = os.clock() - clock0 (2 s of black first: start OBS)

	local CAM_KEY = "TrailerCam"
	local lastT = -BLACK_IN
	local done = false
	RunService:BindToRenderStep(CAM_KEY, Enum.RenderPriority.Last.Value + 60, function(dtR)
		if done then return end
		local now = os.clock()
		-- Studio review: player attribute TrailerDebugT = n freezes the scene at n seconds
		local dbg = RunService:IsStudio() and player:GetAttribute("TrailerDebugT")
		if typeof(dbg) == "number" then clock0 = now - dbg music.Volume = 0 end
		-- the music is the master clock: pull our clock towards it when it drifts
		if music.IsPlaying and typeof(dbg) ~= "number" then
			local mt = music.TimePosition - MUSIC_AT
			local err = mt - (now - clock0)
			if math.abs(err) > 0.06 and math.abs(err) < 1.5 then clock0 -= err * 0.25 end
		end
		local t = now - clock0
		local dt = math.clamp(t - lastT, 0, 0.1)
		lastT = t
		-- black at the start (OBS), the fade at the end
		if t < 0 then
			black.BackgroundTransparency = 0
			music.Volume = MUSIC_VOL * ramp(t, -0.6, 0)
		else
			black.BackgroundTransparency = math.min(ramp(t, 0, 0.3), 1 - ramp(t, T.fade0, T.fade1))
			music.Volume = MUSIC_VOL * (1 - ramp(t, T.fade0 - 0.8, T.fade1 + BLACK_OUT * 0.6))
		end
		local ok, err = pcall(function()
			local tt = math.max(t, 0)
			perform(tt, dt)
			world(tt, dt)
			local cf, fov, focus = camAt(tt)
			-- handheld drift + impact shake
			local s = shakeAmt
			local hh = CFrame.Angles(noise(tt * 1.3, 11) * 0.006, noise(tt * 1.3, 12) * 0.008, 0)
			local sh = CFrame.Angles(noise(tt * 22, 1) * 0.035 * s, noise(tt * 22, 2) * 0.035 * s, noise(tt * 22, 3) * 0.02 * s)
			shakeAmt = math.max(0, shakeAmt - dt * 3)
			cam.CameraType = Enum.CameraType.Scriptable
			cam.CFrame = cf * hh * sh
			cam.FieldOfView = fov
			if focus then clearView(cf.Position, focus) end
			drawCaptions(tt)
			flash.BackgroundTransparency = 1 - (1 - ramp(now, flashAt, flashAt + flashLen)) * (now - flashAt < flashLen and 0.85 or 0)
		end)
		if not ok then warn("[Trailer] " .. tostring(err)) end
	end)
	onEnd(function() RunService:UnbindFromRenderStep(CAM_KEY) end)

	-- keep the far stages streamed + other players hidden while it plays
	task.spawn(function()
		while not done do
			requestStreams()
			ghostPlayers()
			parkWaves()
			hideZoneEggs()
			hideCards()
			hideHud()
			task.wait(0.5)
		end
	end)

	while not stopped and os.clock() - clock0 < LENGTH + BLACK_OUT do task.wait() end
	done = true
	-- hand the camera back (behind the real character)
	cam.CameraType = Enum.CameraType.Custom
	cam.CameraSubject = realHum
	cam.FieldOfView = 70
	cam.CFrame = CFrame.lookAt(realRoot.Position + V(0, 6, 14), realRoot.Position)
end

function M.play()
	if M.running then return false end
	M.running = true
	local ok, err = pcall(run)
	if not ok then warn("[Trailer] " .. tostring(err)) end
	runCleanup()
	M.running = false
	return ok
end

return M
