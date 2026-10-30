-- hatch_pages_snapshot.lua (2026-10-22, UWF plan 8.6): "the built HATCH pages must not change" (Settings / Index /
-- Rebirth). The gift-snapshot recipe: Client datamodel of a FRESH TestFreshSave Play session; opens Settings -> Index ->
-- Rebirth in turn and dumps each <Name>Page subtree (the gift snapshot's property list). Volatile, not recorded: Rays
-- Rotation, ButtonScale / PopScale / PicScale / BadgePulse scales, UIGradient Rotation / Offset, the Index rail Pill's
-- Position (tween), the SKIP live price text. Dumps until 2 runs 1 s apart are identical (max 6). Returns
-- "ALL <fnv> (<n> groups)" + one FNV-1a hash per GROUP (page + the first 4 path levels, sorted); the full dump stays in
-- _G.HATCH_PAGES_SNAP. BEFORE in UWF Task 0 (hatch_pages_before_uwf.txt), AFTER after each run (_after_uwf.txt).
local p = game.Players.LocalPlayer
local mm = p.PlayerGui:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local open, close = mm:WaitForChild("OpenPage"), mm:WaitForChild("CloseWindow")
local RunService = game:GetService("RunService")
local function r(n) return math.floor(n * 100 + 0.5) / 100 end
local function v(x)
	local t = typeof(x)
	if t == "UDim2" then return ("{%s,%s,%s,%s}"):format(r(x.X.Scale), r(x.X.Offset), r(x.Y.Scale), r(x.Y.Offset)) end
	if t == "UDim" then return ("{%s,%s}"):format(r(x.Scale), r(x.Offset)) end
	if t == "Vector2" then return ("(%s,%s)"):format(r(x.X), r(x.Y)) end
	if t == "Color3" then return ("rgb(%d,%d,%d)"):format(math.floor(x.R * 255 + 0.5), math.floor(x.G * 255 + 0.5), math.floor(x.B * 255 + 0.5)) end
	if t == "number" then return tostring(r(x)) end
	if t == "ColorSequence" then
		local s = {}
		for _, k in x.Keypoints do table.insert(s, r(k.Time) .. ":" .. v(k.Value)) end
		return "CS[" .. table.concat(s, " ") .. "]"
	end
	if t == "NumberSequence" then
		local s = {}
		for _, k in x.Keypoints do table.insert(s, r(k.Time) .. ":" .. r(k.Value)) end
		return "NS[" .. table.concat(s, " ") .. "]"
	end
	return tostring(x)
end
local PROPS = {
	GuiObject = {"Visible", "Size", "Position", "AnchorPoint", "Rotation", "ZIndex", "BackgroundColor3", "BackgroundTransparency", "ClipsDescendants", "AbsolutePosition", "AbsoluteSize"},
	TextLabel = {"Text", "TextColor3", "TextSize", "TextScaled"}, TextButton = {"Text", "TextColor3", "TextSize", "TextScaled"},
	ImageLabel = {"Image", "ImageColor3", "ImageTransparency"}, ImageButton = {"Image", "ImageColor3", "ImageTransparency"},
	UIStroke = {"Enabled", "Thickness", "Color", "Transparency"},
	UICorner = {"CornerRadius"},
	UIGradient = {"Color", "Transparency", "Rotation"},
	UIAspectRatioConstraint = {"AspectRatio"},
	UIScale = {"Scale"},
}
local VOLATILE_SCALE = {ButtonScale = true, PopScale = true, PicScale = true, BadgePulse = true}
local function skipProp(o, prop, path)
	if o.Name == "Rays" and prop == "Rotation" then return true end
	if o:IsA("UIGradient") and (prop == "Rotation" or prop == "Offset") then return true end
	if o:IsA("UIScale") and VOLATILE_SCALE[o.Name] and prop == "Scale" then return true end
	if path:find("^IndexPage%.Rail%.Pill") and (prop == "Position" or prop == "AbsolutePosition") then return true end
	if path:find("^RebirthPage%.Skip%.Face%.") and (prop == "Text" or prop == "TextSize" or prop == "Position" or prop == "AbsolutePosition" or prop == "Size" or prop == "AbsoluteSize") then return true end
	return false
end
local function dumpOne(o, path, out)
	local parts = {path .. " [" .. o.ClassName .. "]"}
	local function add(list)
		for _, prop in list do
			if not skipProp(o, prop, path) then
				local ok, val = pcall(function() return o[prop] end)
				if ok then table.insert(parts, prop .. "=" .. v(val)) end
			end
		end
	end
	if o:IsA("GuiObject") then add(PROPS.GuiObject) end
	if PROPS[o.ClassName] then add(PROPS[o.ClassName]) end
	table.insert(out, table.concat(parts, " "))
end
local function walk(o, path, out)
	local kids = o:GetChildren()
	table.sort(kids, function(a, b) if a.Name ~= b.Name then return a.Name < b.Name end return a.ClassName < b.ClassName end)
	local seen = {}
	for _, c in kids do
		local key = c.Name .. "|" .. c.ClassName
		seen[key] = (seen[key] or 0) + 1
		local cp = path .. "." .. c.Name .. (seen[key] > 1 and ("#" .. seen[key]) or "")
		dumpOne(c, cp, out)
		walk(c, cp, out)
	end
end
local function frames(n) for _ = 1, n do RunService.RenderStepped:Wait() end end
local function fnv(s)
	local h = 2166136261
	for i = 1, #s do h = bit32.bxor(h, s:byte(i)) h = (h * 16777619) % 4294967296 end
	return string.format("%08x", h)
end
local function dumpAll()
	local out = {}
	if win.Visible then close:Fire() task.wait(0.5) end
	for _, name in {"Settings", "Index", "Rebirth"} do
		open:Fire(name)
		task.wait(0.9)
		local page = body:FindFirstChild(name .. "Page")
		if page then
			page:SetAttribute("HatchTestPulse", 1)
			frames(3)
			table.insert(out, "=== " .. name)
			dumpOne(page, page.Name, out)
			walk(page, page.Name, out)
			page:SetAttribute("HatchTestPulse", nil)
		end
		close:Fire()
		task.wait(0.5)
	end
	return out
end
local a, b, tries = nil, nil, 0
repeat
	tries += 1
	a = b or dumpAll()
	task.wait(1)
	b = dumpAll()
until table.concat(a, "\n") == table.concat(b, "\n") or tries >= 6
local stable = table.concat(a, "\n") == table.concat(b, "\n")
_G.HATCH_PAGES_SNAP = table.concat(b, "\n")
local groups, order = {}, {}
local sec = ""
for _, line in b do
	if line:sub(1, 4) == "=== " then sec = line:sub(5)
	else
		local parts = {}
		for seg in line:match("^(%S+)"):gmatch("[^%.]+") do table.insert(parts, seg) if #parts == 4 then break end end
		local key = sec .. ":" .. table.concat(parts, ".")
		if not groups[key] then groups[key] = {} table.insert(order, key) end
		table.insert(groups[key], line)
	end
end
table.sort(order)
local g = {}
for _, k in order do table.insert(g, k .. " " .. #groups[k] .. " " .. fnv(table.concat(groups[k], "\n"))) end
_G.HATCH_PAGES_LINES = groups
local head = ("viewport %s | stable after %d tries: %s\nALL %s (%d groups)"):format(v(workspace.CurrentCamera.ViewportSize), tries, tostring(stable), fnv(table.concat(g, "\n")), #g)
_G.HATCH_PAGES_GROUPS = head .. "\n" .. table.concat(g, "\n")
return _G.HATCH_PAGES_GROUPS
