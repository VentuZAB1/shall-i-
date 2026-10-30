-- hatch_shop_snapshot.lua (2026-10-21, RIS plan 8.6 + review SHOULD 11): "the Shop must not change".
-- The gift-snapshot recipe for the HATCH NIGHT Shop. Client datamodel of a TestFreshSave Play session (fresh save: no
-- Starter offer). Opens the Shop and dumps HatchBack, HatchFront and the ShopPage subtree (the gift snapshot's property
-- list). Volatile, not recorded: Text / TextSize of labels matching %d+:%d%d (timers), CanvasPosition, ButtonScale /
-- PopScale / BadgePulse scales, UIGradient Rotation / Offset, Rays Rotation, the Bats children's positions.
-- SHOULD 11: live prices replace the fallbacks ~0.3-1 s after the first open, so it dumps until 2 dumps 1 s apart are
-- identical (max 8 tries) and reports how many it took. Returns one FNV-1a hash per GROUP (section + 4 path levels,
-- sorted); the full dump stays in _G.HATCH_SHOP_SNAP, the groups' lines in _G.HATCH_SHOP_LINES.
-- BEFORE in Task 0 (hatch_shop_before_ris.txt), AFTER at the end (hatch_shop_after_ris.txt).
local p = game.Players.LocalPlayer
local mm = p.PlayerGui:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local page = body:WaitForChild("ShopPage")
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
	ScrollingFrame = {"CanvasSize"},
}
local VOLATILE_SCALE = {ButtonScale = true, PopScale = true, BadgePulse = true}
local function skipProp(o, prop, path)
	if (prop == "Text" or prop == "TextSize") and (o:IsA("TextLabel") or o:IsA("TextButton")) and o.Text:match("%d+:%d%d") then return true end
	if o.Parent and o.Parent.Name == "Bats" and (prop == "Position" or prop == "AbsolutePosition") then return true end
	if o.Name == "Rays" and prop == "Rotation" then return true end
	if o:IsA("UIGradient") and (prop == "Rotation" or prop == "Offset") then return true end
	if o:IsA("UIScale") and VOLATILE_SCALE[o.Name] and prop == "Scale" then return true end
	-- the scroll list: positions on screen follow CanvasPosition (volatile); the layout is in Position / Size
	if prop == "AbsolutePosition" and path:find("%.Scroll%.") then return true end
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
-- the daily auto-open (fresh save): wait for it, then close it so this run opens the window itself
local t0 = os.clock()
while not win.Visible and os.clock() - t0 < 25 do task.wait(0.2) end
if win.Visible then task.wait(0.8) close:Fire() task.wait(0.6) end
open:Fire("Shop")
task.wait(1)
page:SetAttribute("HatchTestPulse", 1)
frames(3)
local function dumpAll()
	local out = {}
	for _, root in {win.HatchBack, win.HatchFront, page} do
		local path = "Window." .. root.Name
		dumpOne(root, path, out)
		walk(root, path, out)
	end
	return table.concat(out, "\n"), out
end
local prev, lines = dumpAll()
local tries, stable = 1, false
while tries < 8 do
	task.wait(1)
	frames(2)
	local now, nl = dumpAll()
	tries += 1
	if now == prev then stable = true lines = nl break end
	prev, lines = now, nl
end
page:SetAttribute("HatchTestPulse", nil)
close:Fire()
task.wait(0.4)
local out = {"viewport " .. v(workspace.CurrentCamera.ViewportSize) .. (" | stable after %d dumps: %s"):format(tries, tostring(stable))}
table.insert(out, "=== SHOP")
for _, l in lines do table.insert(out, l) end
_G.HATCH_SHOP_SNAP = table.concat(out, "\n")
local function fnv(s)
	local h = 2166136261
	for i = 1, #s do h = bit32.bxor(h, s:byte(i)) h = (h * 16777619) % 4294967296 end
	return string.format("%08x", h)
end
local groups, order = {}, {}
local sec = ""
for _, line in out do
	if line:sub(1, 4) == "=== " then sec = line:sub(5)
	elseif line:sub(1, 8) ~= "viewport" then
		local parts = {}
		for seg in line:match("^(%S+)"):gmatch("[^%.]+") do table.insert(parts, seg) if #parts == 4 then break end end
		local key = sec .. ":" .. table.concat(parts, ".")
		if not groups[key] then groups[key] = {} table.insert(order, key) end
		table.insert(groups[key], line)
	end
end
table.sort(order)
local g = {out[1]}
local all = {}
for _, k in order do
	local h = fnv(table.concat(groups[k], "\n"))
	table.insert(g, k .. " " .. #groups[k] .. " " .. h)
	table.insert(all, h)
end
table.insert(g, 2, "ALL " .. fnv(table.concat(all, "")) .. " (" .. #order .. " groups)")
_G.HATCH_SHOP_LINES = groups
_G.HATCH_SHOP_GROUPS = table.concat(g, "\n")
return _G.HATCH_SHOP_GROUPS
