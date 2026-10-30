-- checkui_contain.lua (2026-10-22, UI revert): a containment check for the restored Check-UI windows (the owner's
-- "overlooping and corners aren't even in the box"). Client datamodel of a TestFreshSave Play session. Paste once:
-- _G.CUIContain(label, box, root, opts) -> "<label> checks n fails m" + FAIL lines.
--   box  = the GuiObject whose rect is the window (MainMenu.Window.Face, FreeGiftUI.Holder.Window, OfflineUI.Holder.Window,
--          StarterPackUI.Holder.Window, UpgradeUI.Root.Window)
--   root = the subtree to check (a page, or the window itself)
--   opts.cards = {GuiObject}: every visible descendant of a card stays inside that card
--   opts.skip  = function(o) -> true to ignore an object
--   opts.apart = {{a, b}}: two objects that must not touch
-- Checks, 1 px tolerance: contain (inside the window box; rotation-aware; turning "Sunburst" / "Rays" art = its unrotated
-- rect, the rays' circle), card, textFits, overlap (no two texts' rendered TextBounds rects intersect). Everything is first clipped by its
-- ScrollingFrame / ClipsDescendants ancestors (fully clipped = skipped).
-- Scale emulation: Scale-laid-out windows (MainMenu.Window, UpgradeUI.Root): _G.CUIScale(win, k) sets the window size to
-- k x its size at the first call, _G.CUIScale(win) restores it. Offset-laid-out windows (Free Gift, Welcome Back, Starter
-- Pack popup): scale their Holder.WindowScale UIScale instead (CUIScale on an offset window only shrinks the frame).
-- 4 scales used: 1, 0.85, 0.7, 0.55.
local function rect(o, flat)
	local p, s = o.AbsolutePosition, o.AbsoluteSize
	local r = flat and 0 or math.rad(o.Rotation or 0)
	if r == 0 then return {p.X, p.Y, p.X + s.X, p.Y + s.Y} end
	local cx, cy = p.X + s.X / 2, p.Y + s.Y / 2
	local hw = (math.abs(math.cos(r)) * s.X + math.abs(math.sin(r)) * s.Y) / 2
	local hh = (math.abs(math.sin(r)) * s.X + math.abs(math.cos(r)) * s.Y) / 2
	return {cx - hw, cy - hh, cx + hw, cy + hh}
end
local function shown(o, top)
	while o and o ~= top and o:IsA("GuiObject") do
		if not o.Visible then return false end
		o = o.Parent
	end
	return true
end
local function textRect(t)
	local p, s, b = t.AbsolutePosition, t.AbsoluteSize, t.TextBounds
	local x = t.TextXAlignment == Enum.TextXAlignment.Left and p.X or t.TextXAlignment == Enum.TextXAlignment.Right and (p.X + s.X - b.X) or (p.X + (s.X - b.X) / 2)
	local y = t.TextYAlignment == Enum.TextYAlignment.Top and p.Y or t.TextYAlignment == Enum.TextYAlignment.Bottom and (p.Y + s.Y - b.Y) or (p.Y + (s.Y - b.Y) / 2)
	return {x, y, x + b.X, y + b.Y}
end
local function inside(a, b, tol) return a[1] >= b[1] - tol and a[2] >= b[2] - tol and a[3] <= b[3] + tol and a[4] <= b[4] + tol end
local function hit(a, b, tol) return a[1] < b[3] - tol and b[1] < a[3] - tol and a[2] < b[4] - tol and b[2] < a[4] - tol end
local function clipTo(a, c) return {math.max(a[1], c[1]), math.max(a[2], c[2]), math.min(a[3], c[3]), math.min(a[4], c[4])} end
local function f(r) return ("[%.0f %.0f %.0f %.0f]"):format(r[1], r[2], r[3], r[4]) end
local function short(o, top) local n, x = o.Name, o.Parent while x and x ~= top and #n < 70 do n = x.Name .. "." .. n x = x.Parent end return n end
-- the visible part of o after every clipping ancestor (ScrollingFrame / ClipsDescendants), nil = fully clipped
local function visibleRect(o, r, top)
	local x = o.Parent
	while x and x ~= top and x:IsA("GuiObject") do
		if x:IsA("ScrollingFrame") or x.ClipsDescendants then
			local c = rect(x, true)
			if not hit(r, c, 0) then return nil end
			if o.Rotation == 0 then r = clipTo(r, c) end
		end
		x = x.Parent
	end
	return r
end
_G.CUIContain = function(label, box, root, opts)
	opts = opts or {}
	local n, fails, lines = 0, 0, {}
	local function check(kind, ok, what)
		n += 1
		if not ok then fails += 1 if #lines < 25 then table.insert(lines, "FAIL " .. kind .. " " .. what) end end
	end
	local W = rect(box)
	local texts, cardOf = {}, {}
	for _, c in opts.cards or {} do for _, d in c:GetDescendants() do cardOf[d] = c end end
	for _, o in root:GetDescendants() do
		if o:IsA("GuiObject") and shown(o, root.Parent) and o.AbsoluteSize.X > 0 and not (opts.skip and opts.skip(o)) then
			local round = o.Name:find("Sunburst") ~= nil or o.Name == "Rays" -- round (turning) art: the rays' circle, not the rotated square
			local r = visibleRect(o, rect(o, round), root.Parent)
			if r then
				local tr = (o:IsA("TextLabel") or o:IsA("TextButton")) and o.Text ~= "" and o.TextTransparency < 1 and textRect(o) or nil
				if tr then tr = visibleRect(o, tr, root.Parent) end
				check("contain", inside(tr or r, W, 1) and (tr ~= nil or inside(r, W, 1)), short(o, root) .. " " .. f(tr or r) .. " vs " .. f(W))
				local card = cardOf[o]
				if card then check("card", inside(tr or r, rect(card), 1), short(o, root) .. " " .. f(tr or r) .. " vs " .. card.Name .. " " .. f(rect(card))) end
				if tr then
					check("textFits", o.TextFits, short(o, root) .. " '" .. o.Text:sub(1, 30) .. "'")
					table.insert(texts, {o = o, r = tr})
				end
			end
		end
	end
	for i = 1, #texts do
		for j = i + 1, #texts do
			local a, b = texts[i], texts[j]
			if not (a.o:IsAncestorOf(b.o) or b.o:IsAncestorOf(a.o)) and not (a.o.Name:find("Shadow") or b.o.Name:find("Shadow")) then
				check("overlap", not hit(a.r, b.r, 1), short(a.o, root) .. " '" .. a.o.Text:sub(1, 14) .. "' x " .. short(b.o, root) .. " '" .. b.o.Text:sub(1, 14) .. "'")
			end
		end
	end
	for _, pr in opts.apart or {} do
		if pr[1] and pr[2] and shown(pr[1], root.Parent) and shown(pr[2], root.Parent) then
			check("apart", not hit(rect(pr[1]), rect(pr[2]), 1), pr[1].Name .. " " .. f(rect(pr[1])) .. " x " .. pr[2].Name .. " " .. f(rect(pr[2])))
		end
	end
	return ("%s: checks %d fails %d%s"):format(label, n, fails, #lines > 0 and ("\n  " .. table.concat(lines, "\n  ")) or "")
end
local base = {}
_G.CUIScale = function(win, k)
	if not base[win] then base[win] = win.Size end
	if k == nil then win.Size = base[win] base[win] = nil return end
	local s = base[win]
	win.Size = UDim2.new(s.X.Scale * k, s.X.Offset * k, s.Y.Scale * k, s.Y.Offset * k)
end
return "CUIContain ready"
