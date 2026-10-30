return function(MODE, MOSS, WALLD, FLOOR)
-- HUB GRIME ROLLOUT (lead, 2026-10-14). Run in Studio (Edit) via MCP execute_luau.
-- MODE "check": validate only, print a report. MODE "build": rebuild Workspace.HalloweenDecor.Grime.Rollout.
-- The owner-approved test patch (Grime.Bay_B7, back-wall bay B7) is kept as-is and counted in the overlap checks.
-- Rules: HubGrime\NOTES.md sections 2-3. Every part gets attribute GrimeTex = texture name (for id swaps).

local IDS = {
	G_Crack_A = "rbxassetid://137551757590672", G_Crack_B = "rbxassetid://90724625204487",
	G_Crack_C = "rbxassetid://136824660006081", G_Moss_A = "rbxassetid://94826008826257",
	G_Moss_B = "rbxassetid://76779321971991", G_Slime_A = "rbxassetid://112566164185505",
	G_Stain_A = "rbxassetid://129340407392813", G_Stain_B = "rbxassetid://103485799190659",
	W_Crack_A = "rbxassetid://136078386816680", W_Crack_B = "rbxassetid://121416257104947",
	W_Crack_C = "rbxassetid://117463755768673", W_Drip_A = "rbxassetid://73657998408348",
	W_Drip_B = "rbxassetid://114991262128221", W_MossBase_A = "rbxassetid://118137575258215",
	W_MossBase_B = "rbxassetid://74507928133875", W_MossBase_EndL = "rbxassetid://75538290985834",
	W_MossBase_EndR = "rbxassetid://85227963323276",
}
local SIZE = {
	G_Crack_A = {14, 7}, G_Crack_B = {10, 10}, G_Crack_C = {12, 8}, G_Moss_A = {8, 8}, G_Moss_B = {10, 6},
	G_Stain_A = {10, 10}, G_Stain_B = {12, 8}, G_Slime_A = {6, 6},
	W_Crack_A = {5, 10}, W_Crack_B = {8, 10}, W_Crack_C = {6, 12.375}, W_Drip_A = {4, 11.35}, W_Drip_B = {4, 8.35},
	W_MossBase_EndL = {6, 6.375}, W_MossBase_EndR = {6, 6.375},
}
local function cat(tex)
	if tex:find("Crack") then return "crack" end
	if tex:find("Moss") then return "moss" end
	if tex:find("Stain") then return "stain" end
	if tex:find("Slime") then return "slime" end
	return "drip"
end
local LAYER = {stain = 0.03, crack = 0.04, moss = 0.05, slime = 0.05, drip = 0.05}

-- ---------- walls ----------
local HUBC = Vector3.new(0, 0, 25)
local W = {}
for _, w in workspace.Map.Hub.Walls:GetChildren() do
	if w:IsA("BasePart") then
		local cf, sz = w.CFrame, w.Size
		local thin, long, n
		if sz.X < sz.Z then n = cf.RightVector; thin = sz.X; long = sz.Z else n = cf.LookVector; thin = sz.Z; long = sz.X end
		n = Vector3.new(n.X, 0, n.Z).Unit
		if (HUBC - w.Position):Dot(n) < 0 then n = -n end
		W[w.Name] = {n = n, Q = Vector3.new(w.Position.X, 0, w.Position.Z) + n * thin / 2, L = -Vector3.yAxis:Cross(n),
			half = long / 2, trimBottom = w.Position.Y + sz.Y / 2 - 1.1}
	end
end
local function wp(wall, s, d)
	local w = W[wall]
	return w.Q + w.L * (w.half - s) + w.n * d
end

-- ---------- geometry helpers ----------
local function obb2(cf, sx, sz) -- 2D oriented box: centre, axis u (x), axis v (z), half sizes
	local r = cf.RightVector; local l = cf.LookVector
	return {c = Vector2.new(cf.X, cf.Z), u = Vector2.new(r.X, r.Z).Unit, v = Vector2.new(l.X, l.Z).Unit, hu = sx / 2, hv = sz / 2}
end
local function sat(a, b)
	for _, ax in {a.u, a.v, b.u, b.v} do
		local function proj(o) return math.abs(o.u:Dot(ax)) * o.hu + math.abs(o.v:Dot(ax)) * o.hv end
		if math.abs((b.c - a.c):Dot(ax)) > proj(a) + proj(b) then return false end
	end
	return true
end
local function circleHit(o, centre, r)
	local d = Vector2.new(centre.X, centre.Z) - o.c
	local lu = math.clamp(d:Dot(o.u), -o.hu, o.hu); local lv = math.clamp(d:Dot(o.v), -o.hv, o.hv)
	return (d - o.u * lu - o.v * lv).Magnitude < r
end

-- exclusion boxes
local EX = {}
for i = 1, 3 do
	local s = workspace.Map.Hub.Bases["Base" .. i].Slot
	table.insert(EX, {"Base" .. i, obb2(s.CFrame, s.Size.X + 8, s.Size.Z + 8)})
end
local function addModelBox(m, pad)
	local cf, sz = m:GetBoundingBox()
	table.insert(EX, {m.Name, obb2(cf, sz.X + pad * 2, sz.Z + pad * 2)})
end
for _, f in {workspace.Map.Hub.Treadmills} do for _, m in f:GetChildren() do addModelBox(m, 1) end end
for _, f in {workspace.Map.Hub.Leaderboards, workspace.Map.Hub.Stalls, workspace.Map.Hub.UpgradeSigns} do for _, m in f:GetChildren() do addModelBox(m, 0.5) end end
addModelBox(workspace.Map.Hub.Slingshot, 2)
table.insert(EX, {"LaunchPlatform", obb2(workspace.Map.Hub.LaunchPlatform.CFrame, workspace.Map.Hub.LaunchPlatform.Size.X + 4, workspace.Map.Hub.LaunchPlatform.Size.Z + 4)})
local CIRC = {{"Spawn", Vector3.new(0, 0, -22), 8}, {"PlazaCentre", Vector3.new(0, 0, -33), 12}}
for _, l in workspace.HalloweenDecor.StreetLamps:GetChildren() do table.insert(CIRC, {l.Name, l:GetPivot().Position, 2}) end

local groundSet = {workspace.Map.Hub.Floor, workspace.Map.Hub.FloorSides, workspace.Map.Hub.Decor.Plaza, workspace.Map.Hub.MarketCorners,
	workspace.Map.Hub.Decor.Path_Base1, workspace.Map.Hub.Decor.Path_Base2, workspace.Map.Hub.Decor.Path_Base3}
local rp = RaycastParams.new(); rp.FilterType = Enum.RaycastFilterType.Include; rp.FilterDescendantsInstances = groundSet
local creamSet = {}
for _, m in {workspace.Map.Hub.Decor.Plaza, workspace.Map.Hub.Decor.Path_Base1, workspace.Map.Hub.Decor.Path_Base2, workspace.Map.Hub.Decor.Path_Base3} do
	for _, p in m:GetDescendants() do if p:IsA("BasePart") then creamSet[p] = true end end
end

-- ---------- resolve floor placements ----------
local report, placed = {}, {}
local fixedFloor = {}
for _, p in workspace.HalloweenDecor.Grime.Bay_B7:GetChildren() do
	if p.Size.Y < 0.1 then
		local tex = p.Name:find("Moss") and "G_Moss" or p.Name:find("Stain") and "G_Stain" or "G_Crack"
		table.insert(fixedFloor, {id = "TP_" .. p.Name, cat = cat(tex), tex = p.Name, box = obb2(p.CFrame, p.Size.X, p.Size.Z), pos = p.Position})
	end
end

local function floorCF(f)
	if f.wall then
		local p = wp(f.wall, f.s, f.d)
		return CFrame.lookAt(p, p + W[f.wall].n)
	elseif f.plaza then
		local th = math.rad(f.plaza)
		local dir = Vector3.new(math.cos(th), 0, math.sin(th))
		local p = Vector3.new(0, 0, -33) + dir * f.r
		return CFrame.lookAt(p, p + dir)
	elseif f.path then
		local path = workspace.Map.Hub.Decor[f.path].Path
		local cf = path.CFrame * CFrame.new(f.lat, 0, f.along) * CFrame.Angles(0, math.rad(90), 0)
		return CFrame.new(cf.X, 0, cf.Z) * cf.Rotation
	else
		return CFrame.new(f.x, 0, f.z) * CFrame.Angles(0, math.rad(f.yaw), 0)
	end
end

local allFloor = {}
for _, f in fixedFloor do table.insert(allFloor, f) end
for _, f in FLOOR do
	local sz = SIZE[f.tex]; local sc = f.scale or 1
	local w, h = sz[1] * sc, sz[2] * sc
	local cf = floorCF(f)
	local errs = {}
	-- ground samples
	local base, centrePart
	local rc = workspace:Raycast(Vector3.new(cf.X, 5, cf.Z), Vector3.new(0, -10, 0), rp)
	if rc then base = rc.Position.Y; centrePart = rc.Instance else table.insert(errs, "no ground at centre") end
	local wantCream = f.plaza ~= nil or f.path ~= nil
	if base then
		local lo, hi, cream, green, none = 0, 0, 0, 0, 0
		for i = 0, 6 do for j = 0, 6 do
			local pt = cf:PointToWorldSpace(Vector3.new((i / 6 - 0.5) * w * 0.9, 0, (j / 6 - 0.5) * h * 0.9))
			local r = workspace:Raycast(Vector3.new(pt.X, 5, pt.Z), Vector3.new(0, -10, 0), rp)
			-- samples under a wall are hidden: skip if behind any wall face
			local hidden = false
			for _, ww in W do if (Vector3.new(pt.X, 0, pt.Z) - ww.Q):Dot(ww.n) < 0 and math.abs((Vector3.new(pt.X, 0, pt.Z) - ww.Q):Dot(ww.L)) < ww.half then hidden = true end end
			if not hidden then
				if not r then none += 1
				else
					if r.Position.Y < base - 0.05 then lo += 1 end
					if r.Position.Y > base + 0.15 then hi += 1 end
					if creamSet[r.Instance] then cream += 1 else green += 1 end
				end
			end
		end end
		if none > 0 then table.insert(errs, none .. " samples over no ground") end
		if lo > 0 then table.insert(errs, lo .. " samples lower (floats)") end
		if hi > 0 then table.insert(errs, hi .. " samples higher (step)") end
		if wantCream and green > 0 then table.insert(errs, green .. " samples off cream") end
		if not wantCream and cream > 0 then table.insert(errs, cream .. " samples on cream") end
	end
	local box = obb2(cf, w, h)
	local inner = obb2(cf, w * 0.9, h * 0.9)
	for _, e in EX do if sat(inner, e[2]) then table.insert(errs, "in " .. e[1]) end end
	for _, c in CIRC do if circleHit(inner, c[2], c[3]) then table.insert(errs, "near " .. c[1]) end end
	local me = {id = f.id, cat = cat(f.tex), tex = f.tex, box = inner, pos = Vector3.new(cf.X, 0, cf.Z)}
	for _, o in allFloor do
		if sat(inner, o.box) then
			local a, b = me.cat, o.cat
			local ok = (a == "stain" and b ~= "slime") or (b == "stain" and a ~= "slime")
			if not ok then table.insert(errs, "overlaps " .. o.id .. " (" .. a .. "/" .. b .. ")") end
		end
		if me.cat == "crack" and o.tex == f.tex and (o.pos - me.pos).Magnitude < 30 then table.insert(errs, "same crack " .. o.id .. " within 30") end
	end
	table.insert(allFloor, me)
	f._cf, f._w, f._h, f._base, f._errs = cf, w, h, base or 0, errs
	table.insert(report, ("%s %s %s"):format(#errs == 0 and "OK  " or "FAIL", f.id, table.concat(errs, "; ")))
end

-- ---------- wall checks ----------
local wallItems = {}
for _, m in MOSS do table.insert(wallItems, {id = m[1], wall = m[2], cat = "moss", s0 = m[4], s1 = m[5], y0 = -0.375, y1 = 6.0}) end
for _, d in WALLD do
	local sz = SIZE[d[3]]
	local y0 = d[5] == "drip" and (W[d[2]].trimBottom + 0.35 - sz[2]) or d[5]
	table.insert(wallItems, {id = d[1], wall = d[2], tex = d[3], cat = d[3]:find("MossBase") and "moss" or cat(d[3]), s0 = d[4] - sz[1] / 2, s1 = d[4] + sz[1] / 2, y0 = y0, y1 = y0 + sz[2]})
end
for i, a in wallItems do
	for j = i + 1, #wallItems do
		local b = wallItems[j]
		if a.wall == b.wall and a.s0 < b.s1 - 0.01 and b.s0 < a.s1 - 0.01 and a.y0 < b.y1 and b.y0 < a.y1 then
			local pair = a.cat .. "/" .. b.cat
			local okPair = (a.tex == "W_Crack_C" and b.cat == "moss") or (b.tex == "W_Crack_C" and a.cat == "moss")
				or ((a.tex == "W_Crack_A" or a.tex == "W_Crack_B") and b.cat == "moss" and a.y0 >= 4.25)
				or ((b.tex == "W_Crack_A" or b.tex == "W_Crack_B") and a.cat == "moss" and b.y0 >= 4.25)
				or (a.id:find("EndR") and b.cat == "moss" and math.abs(a.s0 - b.s1) < 0.02) or (b.id:find("EndR") and a.cat == "moss" and math.abs(b.s0 - a.s1) < 0.02)
			if not okPair then table.insert(report, ("WALL overlap %s x %s (%s)"):format(a.id, b.id, pair)) end
		end
	end
end

local counts = {}
for _, f in FLOOR do counts[cat(f.tex)] = (counts[cat(f.tex)] or 0) + 1 end
local c = {}
for k, v in counts do table.insert(c, k .. "=" .. v) end
table.insert(report, "floor counts: " .. table.concat(c, " ") .. " | wall items " .. #wallItems)

-- ---------- build ----------
if MODE == "build" then
	local grime = workspace.HalloweenDecor.Grime
	local old = grime:FindFirstChild("Rollout"); if old then old:Destroy() end
	local root = Instance.new("Folder"); root.Name = "Rollout"
	local fw = Instance.new("Folder"); fw.Name = "Walls"; fw.Parent = root
	local ff = Instance.new("Folder"); ff.Name = "Floor"; ff.Parent = root
	local function carrier(name, cf, size, tex, parent)
		local p = Instance.new("Part")
		p.Name = name; p.Anchored = true; p.CanCollide = false; p.CanTouch = false; p.CanQuery = false
		p.CastShadow = false; p.Transparency = 1; p.Size = size; p.CFrame = cf
		p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
		p:SetAttribute("GrimeTex", tex)
		p.Parent = parent
		return p
	end
	for _, m in MOSS do
		local w = W[m[2]]
		local width = m[5] - m[4]
		local sMid = (m[4] + m[5]) / 2
		local p0 = wp(m[2], sMid, LAYER.moss - 0.025) + Vector3.new(0, -0.375 + 6.375 / 2, 0)
		local tex = "W_MossBase_" .. m[3]
		local p = carrier(m[1], CFrame.lookAt(p0, p0 + w.n), Vector3.new(width, 6.375, 0.05), tex, fw)
		local t = Instance.new("Texture"); t.Texture = IDS[tex]; t.Face = Enum.NormalId.Front
		t.StudsPerTileU = 24; t.StudsPerTileV = 6.375; t.OffsetStudsU = m[6]; t.Parent = p
	end
	for _, d in WALLD do
		local w = W[d[2]]; local sz = SIZE[d[3]]
		local y0 = d[5] == "drip" and (w.trimBottom + 0.35 - sz[2]) or d[5]
		local layer = d[3]:find("MossBase") and LAYER.moss or LAYER[cat(d[3])]
		local p0 = wp(d[2], d[4], layer - 0.025) + Vector3.new(0, y0 + sz[2] / 2, 0)
		local p = carrier(d[1], CFrame.lookAt(p0, p0 + w.n), Vector3.new(sz[1], sz[2], 0.05), d[3], fw)
		local dc = Instance.new("Decal"); dc.Texture = IDS[d[3]]; dc.Face = Enum.NormalId.Front; dc.Parent = p
	end
	for _, f in FLOOR do
		if #f._errs == 0 then
			local y = f._base + LAYER[cat(f.tex)] - 0.025
			local cf = CFrame.new(f._cf.X, y, f._cf.Z) * f._cf.Rotation
			local p = carrier(f.id, cf, Vector3.new(f._w, 0.05, f._h), f.tex, ff)
			local dc = Instance.new("Decal"); dc.Texture = IDS[f.tex]; dc.Face = Enum.NormalId.Top
			dc.Transparency = f.transp or 0; dc.Parent = p
		end
	end
	root.Parent = grime
	table.insert(report, "BUILT Rollout: walls " .. #fw:GetChildren() .. ", floor " .. #ff:GetChildren())
end
return table.concat(report, "\n")
end
