-- hatch_chrome_snapshot.lua v2 (2026-10-21, popup/shop plan 7.6 + D16): "every other window unchanged".
-- v2: the walker also skips Window.ShopTabs and Body.GiftPicker (Shop content that moves into ShopPage); PRE may be
-- nil, "Gift" or "Shop"; the header records the HUD edges (review SHOULD 22: if they differ, re-capture BEFORE).
-- Client datamodel of a TestFreshSave Play session. Opens Shop, Rebirth, Index and Settings in turn and dumps the
-- window CHROME (Window + descendants, minus HatchBack / HatchFront and Body.<x>Page / Body.Message = page content).
-- PRE = "Gift" opens the Gift window first (the AFTER-gift run). Compare the outputs with a text diff.
local PRE = _G.HATCH_SNAP_PRE -- nil, "Gift" or "Shop" (set _G.HATCH_SNAP_PRE before running)
local p = game.Players.LocalPlayer
local mm = p.PlayerGui:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local open, close = mm:WaitForChild("OpenPage"), mm:WaitForChild("CloseWindow")
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
local function dumpOne(o, path, out)
	local parts = {path .. " [" .. o.ClassName .. "]"}
	local function add(list)
		for _, prop in list do
			local ok, val = pcall(function() return o[prop] end)
			if ok then table.insert(parts, prop .. "=" .. v(val)) end
		end
	end
	if o:IsA("GuiObject") then add(PROPS.GuiObject) end
	if PROPS[o.ClassName] and o.ClassName ~= "GuiObject" then add(PROPS[o.ClassName]) end
	table.insert(out, table.concat(parts, " "))
end
local function walk(o, path, out)
	local kids = o:GetChildren()
	table.sort(kids, function(a, b) if a.Name ~= b.Name then return a.Name < b.Name end return a.ClassName < b.ClassName end)
	local seen = {}
	for _, c in kids do
		if c.Name == "HatchBack" or c.Name == "HatchFront" then continue end
		if o == body and (c.Name:match("Page$") or c.Name == "Message" or c.Name == "GiftPicker") then continue end
		if o == win and c.Name == "ShopTabs" then continue end
		local key = c.Name .. "|" .. c.ClassName
		seen[key] = (seen[key] or 0) + 1
		local cp = path .. "." .. c.Name .. (seen[key] > 1 and ("#" .. seen[key]) or "")
		dumpOne(c, cp, out)
		walk(c, cp, out)
	end
end
local out = {"viewport " .. v(workspace.CurrentCamera.ViewportSize)}
do -- (review SHOULD 22) the HUD edges the Hatch fit depends on
	local ga = mm.AbsolutePosition
	local menu = mm:FindFirstChild("Menu")
	local sp = p.PlayerGui:FindFirstChild("SpeedUI")
	local h = sp and sp:FindFirstChild("Holder")
	out[1] = out[1] .. (" | Menu right %s | SpeedUI.Holder %s"):format(menu and r(menu.AbsolutePosition.X - ga.X + menu.AbsoluteSize.X) or "nil",
		h and ("(%s,%s %sx%s)"):format(r(h.AbsolutePosition.X - ga.X), r(h.AbsolutePosition.Y - ga.Y), r(h.AbsoluteSize.X), r(h.AbsoluteSize.Y)) or "nil")
end
-- the once-per-session daily auto-open must not fire in the middle of a dump: wait for it (fresh save = Day 1 waiting)
local t0 = os.clock()
while not win.Visible and os.clock() - t0 < 25 do task.wait(0.2) end
if win.Visible then task.wait(0.8) close:Fire() task.wait(0.6) end
if PRE == "Gift" then open:Fire(PRE) task.wait(1) end -- then Shop opens straight over it (a direct page switch)
for _, name in {"Shop", "Rebirth", "Index", "Settings"} do
	-- PRE "Shop": every other window opens straight over the HATCH NIGHT Shop (a direct skin switch, no close between)
	if PRE == "Shop" and name ~= "Shop" then open:Fire("Shop") task.wait(0.7) end
	open:Fire(name)
	task.wait(0.7)
	table.insert(out, "=== " .. name)
	dumpOne(win, "Window", out)
	walk(win, "Window", out)
	close:Fire()
	task.wait(0.4)
end
-- (fix round, perf review item 7) _G.HATCH_SNAP_MENU = true: the left menu (MainMenu.Menu + its UIScale) too
if _G.HATCH_SNAP_MENU then
	local menu = mm:FindFirstChild("Menu")
	table.insert(out, "=== Menu")
	if menu then dumpOne(menu, "Menu", out) walk(menu, "Menu", out) end
end
-- the full dump is ~140K chars: keep it in _G.HATCH_SNAP (query lines from it when a hash differs) and return one
-- FNV-1a hash per object line, in the dump's sorted order (8 hex chars per line; the path list stays in _G.HATCH_SNAP);
-- the saved before/after files are these hash lists
_G.HATCH_SNAP = table.concat(out, "\n")
local function fnv(s)
	local h = 2166136261
	for i = 1, #s do h = bit32.bxor(h, s:byte(i)) h = (h * 16777619) % 4294967296 end
	return string.format("%08x", h)
end
local hashes = {out[1]}
for i = 2, #out do
	local line = out[i]
	if line:sub(1, 4) == "=== " then table.insert(hashes, line) else table.insert(hashes, fnv(line)) end
end
_G.HATCH_HASH = table.concat(hashes, "\n")
return _G.HATCH_HASH
