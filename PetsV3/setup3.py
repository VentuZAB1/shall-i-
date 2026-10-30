# python setup3.py A B C > out.lua  -> Luau that sets up imported PetsV3 models (single Body mesh, bones in Body).
# Scales by the TRUE world height (GetBoundingBox is oriented by the import pivot on single-mesh imports and swaps Y/Z),
# PrimaryPart = Body, attributes (ClipSet, DisplayName, Height, Motion, Rig, Source, WalkSpeed), replaces the model in
# ReplicatedStorage.CreatureModels and the clip module in CreatureClips (clip rbxmx lands in Workspace or ServerStorage).
import sys, os, json
here = os.path.dirname(os.path.abspath(__file__))
cfgs = []
for n in sys.argv[1:]:
    m = json.load(open(os.path.join(here, n, n + "_meta.json"), encoding="utf-8"))
    bu = json.load(open(os.path.join(here, n, n + "_bu.json"), encoding="utf-8"))["height"]
    cfgs.append('{name = "%s", display = "%s", height = %s, bu_height = %.4f, motion = "%s", rig = "%s", stride = %.5f, walk_len = %.4f}'
                % (m["name"], m["display"], m["height"], bu, m["motion"], m["rig"], m["stride"] or 0, m["walk_len"] or 1))
print('''local RS = game.ReplicatedStorage
local function clipFolders()
	local t = {}
	for _, s in {game.ServerStorage, workspace} do for _, f in s:GetChildren() do
		if f.Name == "PetsV2Clips" then table.insert(t, f) end end end
	return t
end
local function worldExt(m)
	local mn, mx = Vector3.one * 1e9, -Vector3.one * 1e9
	for _, p in m:GetDescendants() do
		if p:IsA("BasePart") and p.Transparency < 1 then
			local c, s = p.CFrame, p.Size / 2
			for _, sx in {-1, 1} do for _, sy in {-1, 1} do for _, sz in {-1, 1} do
				local w = c * Vector3.new(sx * s.X, sy * s.Y, sz * s.Z)
				mn, mx = mn:Min(w), mx:Max(w)
			end end end
		end
	end
	return mx - mn
end
local function setup(CFG)
	local m = workspace:FindFirstChild(CFG.name)
	assert(m, CFG.name .. ": imported model missing")
	for _, n in {"InitialPoses", "AnimationController"} do local x = m:FindFirstChild(n) if x then x:Destroy() end end
	m.PrimaryPart = m:FindFirstChild("RootPart") or m.Body
	-- the importer now gives the pivot the Z-up -> Y-up turn (+90 X): PivotTo(yaw) then laid pets on their side.
	-- Keep the pivot at the feet but upright (2026-10-08 fix).
	m.PrimaryPart.PivotOffset = CFrame.new(m.PrimaryPart.PivotOffset.Position)
	for _, p in m:GetDescendants() do
		if p:IsA("BasePart") then p.Anchored, p.CanCollide, p.CanQuery, p.CanTouch, p.Massless = true, false, false, false, false end
	end
	local rp = m:FindFirstChild("RootPart")
	if rp then rp.Transparency = 1 end
	m.Body.CastShadow = true
	local e0 = worldExt(m)
	m:ScaleTo(m:GetScale() * CFG.height / e0.Y)
	local e = worldExt(m)
	m:SetAttribute("ClipSet", CFG.name)
	m:SetAttribute("DisplayName", CFG.display)
	m:SetAttribute("Height", math.floor(e.Y * 100 + 0.5) / 100)
	m:SetAttribute("Motion", CFG.motion)
	m:SetAttribute("Rig", CFG.rig)
	m:SetAttribute("Source", "PetsV3")
	if CFG.stride > 0 then
		m:SetAttribute("WalkSpeed", math.floor(CFG.stride * (e.Y / CFG.bu_height) / CFG.walk_len * 100 + 0.5) / 100)
	end
	local old = RS.CreatureModels:FindFirstChild(CFG.name)
	if old then old:Destroy() end
	m.Parent = RS.CreatureModels
	local mod
	for _, f in clipFolders() do mod = mod or f:FindFirstChild(CFG.name) end
	if mod then
		local oldc = RS.CreatureClips:FindFirstChild(CFG.name)
		if oldc then oldc:Destroy() end
		mod.Parent = RS.CreatureClips
	end
	local nb = 0
	for _, d in m:GetDescendants() do if d:IsA("Bone") then nb += 1 end end
	return string.format("%s ok ext=%s bones=%d WalkSpeed=%s clips=%s", CFG.name, tostring(e), nb, tostring(m:GetAttribute("WalkSpeed")),
		tostring(mod ~= nil))
end
local out = {}
for _, CFG in {''' + ", ".join(cfgs) + '''} do
	local ok, r = pcall(setup, CFG)
	table.insert(out, ok and r or (CFG.name .. " ERROR " .. tostring(r)))
end
for _, f in clipFolders() do if #f:GetChildren() == 0 then f:Destroy() end end
return table.concat(out, "\\n")''')
