-- hatch_gift_snapshot.lua (2026-10-21, popup/shop plan 7.6 + D17): "the Gift window must not change".
-- Client datamodel of a FRESH TestFreshSave Play session (fresh save = Day 1 claimable). Opens the Gift window and dumps
-- HatchBack, HatchFront and the GiftPage subtree (the 8.6 property list) on DAILY, then on PLAYTIME.
-- Playtime is frozen for the dump: the player's PlaytimeStart is set LOCALLY to "now - 5 s" (every slot waiting, the
-- first timer counting; timers are volatile) and restored after. Volatile, not recorded: Text / TextSize of labels
-- matching %d+:%d%d, the PlayBar Time + Fill sizes, Bats children positions, Rays rotation, UIGradient Rotation /
-- Offset, TodayGlow ImageTransparency, ButtonScale / PopScale / BadgePulse scales.
-- The DAILY dump skips the hidden PlaytimeView's descendants (they keep whatever state the view last showed: run 1 vs
-- run 2 of the same session differed there only). Returns one FNV-1a hash per GROUP (path prefix, 4 levels, sorted;
-- "<section>:<path> <lines> <hash>"); the full dump stays in _G.HATCH_GIFT_SNAP. BEFORE in Task 0, AFTER at the end.
local p = game.Players.LocalPlayer
local mm = p.PlayerGui:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local page = body:WaitForChild("GiftPage")
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
local VOLATILE_SCALE = {ButtonScale = true, PopScale = true, BadgePulse = true}
local function skipProp(o, prop, path)
	if (prop == "Text" or prop == "TextSize") and (o:IsA("TextLabel") or o:IsA("TextButton")) and o.Text:match("%d+:%d%d") then return true end
	if path:find("%.PlayBar%.") and (o.Name == "Time" or o.Name == "Fill" or path:find("%.Fill%.")) and
		(prop == "Size" or prop == "AbsoluteSize" or prop == "Text" or prop == "TextSize" or prop == "Position" or prop == "AbsolutePosition") then return true end
	if o.Parent and o.Parent.Name == "Bats" and (prop == "Position" or prop == "AbsolutePosition") then return true end
	if o.Name == "Rays" and prop == "Rotation" then return true end
	if o:IsA("UIGradient") and (prop == "Rotation" or prop == "Offset") then return true end
	if o.Name == "TodayGlow" and prop == "ImageTransparency" then return true end
	if o:IsA("UIScale") and VOLATILE_SCALE[o.Name] and prop == "Scale" then return true end
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
local out = {"viewport " .. v(workspace.CurrentCamera.ViewportSize)}
-- the daily auto-open (fresh save): wait for it, then close it so this run opens the window itself
local t0 = os.clock()
while not win.Visible and os.clock() - t0 < 25 do task.wait(0.2) end
if win.Visible then task.wait(0.8) close:Fire() task.wait(0.6) end
local start0 = p:GetAttribute("PlaytimeStart")
p:SetAttribute("PlaytimeStart", workspace:GetServerTimeNow() - 5)
open:Fire("Gift")
task.wait(1)
page:SetAttribute("Tab", "Daily")
task.wait(0.5)
page:SetAttribute("HatchTestPulse", 1)
frames(3)
local function dumpAll(label)
	table.insert(out, "=== " .. label)
	for _, root in {win.HatchBack, win.HatchFront, page} do
		local path = "Window." .. root.Name
		local lines = {}
		dumpOne(root, path, lines)
		walk(root, path, lines)
		for _, line in lines do
			-- DAILY: the hidden PlaytimeView's descendants keep whatever state the view last showed (history): not recorded
			if not (label == "DAILY" and line:match("^Window%.GiftPage%.PlaytimeView%.")) then table.insert(out, line) end
		end
	end
end
dumpAll("DAILY")
page:SetAttribute("Tab", "Playtime")
task.wait(0.5)
frames(3)
dumpAll("PLAYTIME")
page:SetAttribute("Tab", "Daily")
page:SetAttribute("HatchTestPulse", nil)
p:SetAttribute("PlaytimeStart", start0)
close:Fire()
task.wait(0.4)
_G.HATCH_GIFT_SNAP = table.concat(out, "\n")
local function fnv(s)
	local h = 2166136261
	for i = 1, #s do h = bit32.bxor(h, s:byte(i)) h = (h * 16777619) % 4294967296 end
	return string.format("%08x", h)
end
-- one hash per group (section + the first 4 path levels), sorted: a differing group points at the subtree to inspect
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
for _, k in order do table.insert(g, k .. " " .. #groups[k] .. " " .. fnv(table.concat(groups[k], "\n"))) end
_G.HATCH_GIFT_LINES = groups
_G.HATCH_GIFT_GROUPS = table.concat(g, "\n")
return _G.HATCH_GIFT_GROUPS
