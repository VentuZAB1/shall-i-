-- PetsV2 Studio setup for one imported FBX (workspace.<name>) -> ReplicatedStorage.CreatureModels.<name>
-- CFG is filled from <name>_meta.json by the caller.
local RS = game.ReplicatedStorage
local CFG = __CFG__
local function clipFolders() -- clip rbxmx lands in whatever service was selected on import
	local t = {}
	for _, s in {game.ServerStorage, workspace} do for _, f in s:GetChildren() do
		if f.Name == "PetsV2Clips" then table.insert(t, f) end end end
	return t
end

local m = workspace:FindFirstChild(CFG.name)
assert(m, "imported model missing")
for _, n in {"InitialPoses", "AnimationController"} do
	local x = m:FindFirstChild(n)
	if x then x:Destroy() end
end
local _, size0 = m:GetBoundingBox()
local scale = CFG.height / size0.Y
m:ScaleTo(scale)
for _, p in m:GetDescendants() do
	if p:IsA("BasePart") then
		p.Anchored, p.CanCollide, p.CanQuery, p.CanTouch, p.Massless = true, false, false, false, false
	end
end
local lit = false
for _, hex in CFG.glow do
	local g = m:FindFirstChild("Glow_" .. hex)
	if g then
		local col = Color3.fromHex(hex)
		g.Material, g.Color, g.CastShadow = Enum.Material.Neon, col, false
		if not lit then
			lit = true
			local light = Instance.new("PointLight")
			light.Brightness, light.Range, light.Color = CFG.light or 1.2, 8, col
			light.Parent = g
		end
	end
end
m.RootPart.Transparency = 1
m.Body.CastShadow = true
local studsPerBU = 100 * scale
local _, size = m:GetBoundingBox()
m:SetAttribute("ClipSet", CFG.name)
m:SetAttribute("DisplayName", CFG.display)
m:SetAttribute("Height", math.floor(size.Y * 100 + 0.5) / 100)
m:SetAttribute("Motion", CFG.motion)
m:SetAttribute("Rig", CFG.rig)
m:SetAttribute("Source", "PetsV3")
if CFG.stride > 0 then
	m:SetAttribute("WalkSpeed", math.floor(CFG.stride * studsPerBU / CFG.walk_len * 100 + 0.5) / 100)
end
local old = RS.CreatureModels:FindFirstChild(CFG.name)
if old then old:Destroy() end -- (originals are in ServerStorage._Backup_PetsV1)
m.Parent = RS.CreatureModels
local mod
for _, f in clipFolders() do
	if f.Name == "PetsV2Clips" then
		mod = mod or f:FindFirstChild(CFG.name)
	end
end
if mod then
	local oldc = RS.CreatureClips:FindFirstChild(CFG.name)
	if oldc then oldc:Destroy() end
	mod.Parent = RS.CreatureClips
end
for _, f in clipFolders() do
	if f.Name == "PetsV2Clips" and #f:GetChildren() == 0 then f:Destroy() end
end
local head = m.RootPart.Root:FindFirstChild("Head", true)
return string.format("%s scale=%.5f size=%s WalkSpeed=%s clips=%s headZ-rootZ=%.2f (neg = faces -Z)", CFG.name, scale, tostring(size),
	tostring(m:GetAttribute("WalkSpeed")), tostring(RS.CreatureClips:FindFirstChild(CFG.name) ~= nil),
	head and (head.WorldPosition.Z - m.RootPart.Root.WorldPosition.Z) or 0)
