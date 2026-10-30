-- CreatureVFX (2026-10-08): particle effects for the higher-tier pets (owner's idea). The meshes never glow (the
-- owner dislikes Neon parts), so fire / sparks / auras are ParticleEmitters parented to the pet's Bones (a Bone is an
-- Attachment, so the effect follows the animation). Numbers come from STYLE_BIBLE.md section 2d; sizes and speeds
-- are fractions of the pet's height H in studs, so a 10M KG giant gets proportionally big effects.
-- Usage (client): CreatureVFX.attach(model, creatureName, heightStuds); CreatureVFX.setEnabled(model, bool)
local CreatureVFX = {}

local TEX = {
	spark = "rbxasset://textures/particles/sparkles_main.dds",
	fire = "rbxasset://textures/particles/fire_main.dds",
	smoke = "rbxasset://textures/particles/smoke_main.dds",
}

local function cs(...)
	local t = {...}
	if #t == 1 then return ColorSequence.new(t[1]) end
	local kps = {}
	for i, c in t do table.insert(kps, ColorSequenceKeypoint.new((i - 1) / (#t - 1), c)) end
	return ColorSequence.new(kps)
end
local function ns(...)
	local t = {...}
	if #t == 1 then return NumberSequence.new(t[1]) end
	local kps = {}
	for i, v in t do table.insert(kps, NumberSequenceKeypoint.new((i - 1) / (#t - 1), v)) end
	return NumberSequence.new(kps)
end
local rgb = Color3.fromRGB

-- kind -> function(H) returning ParticleEmitter properties
local KINDS = {
	sparks = function(H) return {
		Texture = TEX.spark, Rate = 3, Lifetime = NumberRange.new(0.15, 0.3), Size = ns(0.05 * H, 0),
		Speed = NumberRange.new(0.5 * H, 0.7 * H), SpreadAngle = Vector2.new(180, 180), Drag = 4,
		Color = cs(rgb(255, 236, 110), rgb(150, 200, 255)), LightEmission = 0.8, Transparency = ns(0, 1),
		Rotation = NumberRange.new(0, 360) } end,
	embers = function(H) return {
		Texture = TEX.spark, Rate = 6, Lifetime = NumberRange.new(1.0, 1.6), Size = ns(0.02 * H, 0),
		Speed = NumberRange.new(0.2 * H, 0.3 * H), SpreadAngle = Vector2.new(25, 25), Acceleration = Vector3.new(0, 0.05 * H, 0),
		Color = cs(rgb(255, 200, 60), rgb(255, 80, 20)), LightEmission = 0.6, Transparency = ns(0, 0.2, 1),
		EmissionDirection = Enum.NormalId.Top } end,
	smoke = function(H) return {
		Texture = TEX.smoke, Rate = 2, Lifetime = NumberRange.new(2, 3), Size = ns(0.06 * H, 0.14 * H),
		Speed = NumberRange.new(0.08 * H, 0.12 * H), SpreadAngle = Vector2.new(20, 20), Color = cs(rgb(60, 50, 56)),
		Transparency = ns(0.55, 1), RotSpeed = NumberRange.new(-30, 30), Rotation = NumberRange.new(0, 360),
		EmissionDirection = Enum.NormalId.Top } end,
	flame = function(H) return {
		Texture = TEX.fire, Rate = 18, Lifetime = NumberRange.new(0.35, 0.55), Size = ns(0.07 * H, 0.01 * H),
		Speed = NumberRange.new(0.12 * H, 0.18 * H), SpreadAngle = Vector2.new(12, 12),
		Color = cs(rgb(255, 230, 110), rgb(255, 90, 20), rgb(120, 20, 10)), LightEmission = 0.7,
		Transparency = ns(0.1, 0.3, 1), ZOffset = 0.3, Rotation = NumberRange.new(0, 360),
		EmissionDirection = Enum.NormalId.Top } end,
	wisps = function(H) return {
		Texture = TEX.smoke, Rate = 4, Lifetime = NumberRange.new(1.0, 1.5), Size = ns(0.05 * H, 0),
		Speed = NumberRange.new(0.04 * H, 0.07 * H), SpreadAngle = Vector2.new(40, 40),
		Color = cs(rgb(170, 100, 255), rgb(40, 20, 90)), LightEmission = 0.35, Transparency = ns(0.35, 1),
		RotSpeed = NumberRange.new(-60, 60), EmissionDirection = Enum.NormalId.Top } end,
	sparkles = function(H) return {
		Texture = TEX.spark, Rate = 3, Lifetime = NumberRange.new(1.2, 1.8), Size = ns(0, 0.035 * H, 0),
		Speed = NumberRange.new(0.02 * H, 0.04 * H), SpreadAngle = Vector2.new(180, 180),
		Color = cs(rgb(255, 244, 180), rgb(200, 220, 255)), LightEmission = 0.7, Rotation = NumberRange.new(0, 360),
		RotSpeed = NumberRange.new(-90, 90) } end,
	bubbles = function(H) return {
		Texture = TEX.smoke, Rate = 2, Lifetime = NumberRange.new(1.2, 1.8), Size = ns(0.015 * H, 0.03 * H),
		Speed = NumberRange.new(0.06 * H, 0.1 * H), SpreadAngle = Vector2.new(15, 15), Color = cs(rgb(200, 235, 255)),
		LightEmission = 0.2, Transparency = ns(0.3, 1), EmissionDirection = Enum.NormalId.Top } end,
}

-- creature -> { {kind, {bone candidates...}, rateMul?}, ... }; first bone found is used. Tier 1 (Grass) has none.
local PRESETS = {
	-- Tier 2 Water: bubbles
	Kappa = {{"bubbles", {"Head"}}},
	SeaTurtleWarrior = {{"bubbles", {"Head", "Chest"}}},
	Kraken = {{"bubbles", {"Head", "Body", "Mantle", "Spine"}, 1.5}},
	-- Tier 3 Storm: sparks
	Raiju = {{"sparks", {"Tail3", "Tail2"}}, {"sparks", {"Leg_FL", "Foot_FL"}, 0.5}},
	ThunderBull = {{"sparks", {"Cloud", "Spine", "Chest"}, 1.3}},
	StormWyvern = {{"sparks", {"WingTip_L", "Wing_L"}}, {"sparks", {"WingTip_R", "Wing_R"}}},
	-- Tier 4 Magma: embers + smoke (+ flames)
	MoltenBoar = {{"embers", {"Spine", "Chest"}}, {"smoke", {"Chest", "Spine"}}},
	LavaGolem = {{"embers", {"Chest", "Spine"}, 1.3}, {"smoke", {"Head", "Chest"}}},
	Cerberus = {{"flame", {"Tail3", "Tail2", "Tail1"}}, {"embers", {"Chest"}}},
	Ivonrath = {{"flame", {"Tail4", "Tail3", "Tail2"}}, {"embers", {"Chest", "Spine"}}, {"smoke", {"Jaw", "Head"}}},
	-- Tier 5 Void: wisps
	ShadePanther = {{"wisps", {"Foot_FL", "Leg_FL"}}, {"wisps", {"Foot_BR", "Leg_BR"}}},
	NightmareStallion = {{"wisps", {"Foot_FL", "Leg_FL"}}, {"smoke", {"Foot_BR", "Leg_BR"}}, {"wisps", {"Neck"}}},
	BlackDragon = {{"wisps", {"Body3", "Spine2", "Chest", "Spine"}, 1.3}, {"wisps", {"Body7", "Tail2", "Tail1"}}},
	PharaohAsparuh = {{"sparkles", {"Head"}}, {"wisps", {"Spine", "Chest"}}, {"sparkles", {"Tail3", "Tail2"}}},
	-- Tier 6 Celestial: sparkles
	SolarLion = {{"sparkles", {"Head"}, 1.5}, {"embers", {"Tail3", "Tail2"}, 0.4}},
	Griffin = {{"sparkles", {"WingTip_L", "Wing_L"}}, {"sparkles", {"WingTip_R", "Wing_R"}}},
	CelestialDragon = {{"sparkles", {"Chest", "Spine"}, 1.5}, {"sparkles", {"Tail4", "Tail3", "Tail2"}}},
	Cvetibara = {{"sparkles", {"Halo", "Head"}, 1.5}, {"sparkles", {"Wing_L"}}, {"sparkles", {"Wing_R"}}},
}

local function findBone(model, names)
	for _, n in names do
		local b = model:FindFirstChild(n, true)
		if b and b:IsA("Attachment") then return b end
	end
	return nil
end

function CreatureVFX.has(name)
	return PRESETS[name] ~= nil
end

function CreatureVFX.attach(model, name, H)
	local preset = PRESETS[name]
	if not preset or model:GetAttribute("VFX") then return 0 end
	H = math.max(H or 6, 1)
	local n = 0
	for i, p in preset do
		local bone = findBone(model, p[2])
		if bone then
			local e = Instance.new("ParticleEmitter")
			e.Name = "PetVFX_" .. p[1] .. i
			for k, v in KINDS[p[1]](H) do e[k] = v end
			e.Rate *= (p[3] or 1)
			e.LightInfluence = 0
			e.LockedToPart = false
			e.Parent = bone
			n += 1
		end
	end
	model:SetAttribute("VFX", n)
	return n
end

function CreatureVFX.setEnabled(model, on)
	for _, d in model:GetDescendants() do
		if d:IsA("ParticleEmitter") and d.Name:sub(1, 7) == "PetVFX_" then d.Enabled = on end
	end
end

return CreatureVFX
