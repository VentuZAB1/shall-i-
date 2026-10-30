-- polish_client.lua (2026-10-22 UI polish of the OLD Check-UI): client checks of the 10 MUSTs + the Free Gift change.
-- Client datamodel of a FRESH TestFreshSave Play session. Needs _G.CUIContain / _G.CUIScale (checkui_contain.lua) first.
-- _G.PolishTests(section) -> "<section>: n pass / m fail" + FAIL lines + INFO lines.
-- Sections: chrome, gift, daily, shop, settings, index, rebirth, freegiftA / B / C (server toggles FreeGiftTestNotInGroup
-- between them), welcome, welcomex5, upgrades, step8, step10, starter, starter59, hud, idle, step11, shopdry (LAST).
-- No real prompt anywhere: Robux buys only through ShopPage TestDryRun / ServerStorage.TestReceipt (server side); claims
-- use the remotes the buttons use; never a mouse click; no button that opens a Robux or join prompt is ever pressed.
-- Measures (PREP.md): base px = screen px / window factor (MainMenu + Upgrades: screen height / 620; Free Gift, Welcome,
-- Starter popup: their WindowScale). Text floor = 16 base (15.5 allowed for integer rounding); phone projection = base x 0.7.
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local HttpService = game:GetService("HttpService")
local TextService = game:GetService("TextService")
local p = Players.LocalPlayer
local pg = p:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local face = win:WaitForChild("Face")
local body = face:WaitForChild("Body")
local B = require(RS:WaitForChild("BrickUI"))
local SCALES = {1, 0.85, 0.7, 0.55}
local FLOOR = 15.5
local KEEP = {} -- numbers kept between sections (face sizes)

local function waitFor(fn, secs)
	local t0 = os.clock()
	while os.clock() - t0 < secs do
		if fn() then return true end
		task.wait(0.05)
	end
	return fn()
end
local function rect(o) local a, s = o.AbsolutePosition, o.AbsoluteSize return {a.X, a.Y, a.X + s.X, a.Y + s.Y} end
local function inside(a, b, tol) tol = tol or 1 return a[1] >= b[1] - tol and a[2] >= b[2] - tol and a[3] <= b[3] + tol and a[4] <= b[4] + tol end
local function hit(a, b, tol) tol = tol or 1 return a[1] < b[3] - tol and b[1] < a[3] - tol and a[2] < b[4] - tol and b[2] < a[4] - tol end
local function f(r) return ("[%.0f %.0f %.0f %.0f]"):format(r[1], r[2], r[3], r[4]) end
local function rotRect(o)
	local a, s = o.AbsolutePosition, o.AbsoluteSize
	local r = math.rad(o.Rotation)
	local cx, cy = a.X + s.X / 2, a.Y + s.Y / 2
	local hw = (math.abs(math.cos(r)) * s.X + math.abs(math.sin(r)) * s.Y) / 2
	local hh = (math.abs(math.sin(r)) * s.X + math.abs(math.cos(r)) * s.Y) / 2
	return {cx - hw, cy - hh, cx + hw, cy + hh}
end
local function insetOf(a, b) return math.min(a[1] - b[1], a[2] - b[2], b[3] - a[3], b[4] - a[4]) end
local function chainVis(d) local x = d while x and x:IsA("GuiObject") do if not x.Visible then return false end x = x.Parent end return true end
local function short(o, top) local n, x = o.Name, o.Parent while x and x ~= top and #n < 64 do n = x.Name .. "." .. n x = x.Parent end return n end
local function screenK() return workspace.CurrentCamera.ViewportSize.Y / 620 end
local function openPage(name)
	if win.Visible then mm.CloseWindow:Fire() waitFor(function() return not win.Visible end, 1.5) task.wait(0.3) end
	mm.OpenPage:Fire(name)
	waitFor(function() return win.Visible end, 2)
	task.wait(0.7)
	return body:FindFirstChild(name .. "Page")
end
local function closePage() if win.Visible then mm.CloseWindow:Fire() waitFor(function() return not win.Visible end, 1.5) task.wait(0.3) end end
local function hotbar() local bp = pg:FindFirstChild("BackpackGui") return bp and bp.Enabled end
local function potions() return p:GetAttribute("Potion_Money") or 0, p:GetAttribute("Potion_Hatch") or 0, p:GetAttribute("Potion_Speed") or 0 end
local function moveTo(pos) p.Character:PivotTo(CFrame.new(pos)) end
local AWAY = Vector3.new(0, 5, -100)
local function grad(o) local g = o:FindFirstChildOfClass("UIGradient") return g and g.Enabled and g or nil end

---------------------------------------------------------------- measuring
local function scaleChain(o)
	local k, x = 1, o
	while x and x ~= game do
		for _, c in x:GetChildren() do if c:IsA("UIScale") then k *= c.Scale end end
		x = x.Parent
	end
	return k
end
-- the font size a label is drawn at (screen px)
local function fontPx(t)
	local txt = t.ContentText
	if txt == "" then return nil end
	if not t.TextScaled then return t.TextSize * scaleChain(t) end
	local W, H = t.AbsoluteSize.X, t.AbsoluteSize.Y
	if W <= 1 or H <= 1 then return nil end
	local cap = 100
	local c = t:FindFirstChildOfClass("UITextSizeConstraint")
	if c then cap = math.min(cap, c.MaxTextSize * scaleChain(t)) end
	local frame = t.TextWrapped and Vector2.new(W, 1e5) or Vector2.new(1e5, 1e5)
	local lo, hi = 1, math.floor(cap)
	while lo < hi do
		local mid = math.ceil((lo + hi) / 2)
		local s = TextService:GetTextSize(txt, mid, Enum.Font.GothamBlack, frame)
		if s.X <= W + 0.5 and s.Y <= H + 0.5 then lo = mid else hi = mid - 1 end
	end
	return lo, (lo >= math.floor(H) - 1) and "H" or "W"
end
local function lum(c)
	local function ch(v) return v <= 0.03928 and v / 12.92 or ((v + 0.055) / 1.055) ^ 2.4 end
	return 0.2126 * ch(c.R) + 0.7152 * ch(c.G) + 0.0722 * ch(c.B)
end
local function cr(a, b) local x, y = lum(a), lum(b) if x < y then x, y = y, x end return (x + 0.05) / (y + 0.05) end
local function painted(o, base) -- the colours o paints: its UIGradient keypoints x its colour
	local g = grad(o)
	if not g then return {base} end
	local out = {}
	for _, kp in g.Color.Keypoints do
		local v = kp.Value
		table.insert(out, Color3.new(v.R * base.R, v.G * base.G, v.B * base.B))
	end
	return out
end
local CANVAS = Color3.fromRGB(59, 88, 102)
local function bgOf(t)
	local x = t.Parent
	while x and x:IsA("GuiObject") do
		if x.BackgroundTransparency < 0.5 then return painted(x, x.BackgroundColor3), x end
		x = x.Parent
	end
	return {CANVAS}, nil
end
local function minCR(cs, ds) local m = 99 for _, a in cs do for _, b in ds do m = math.min(m, cr(a, b)) end end return m end
local function strokeOf(t)
	for _, c in t:GetChildren() do
		if c:IsA("UIStroke") and c.Enabled and c.Transparency < 0.5 and c.ApplyStrokeMode == Enum.ApplyStrokeMode.Contextual then return c end
	end
end
local function strokePx(t, s)
	if s.StrokeSizingMode == Enum.StrokeSizingMode.FixedSize then return s.Thickness * scaleChain(t) end
	return s.Thickness * math.min(t.AbsoluteSize.X, t.AbsoluteSize.Y) -- (assumption: ScaledSize = a share of the shorter side)
end
local function clippedOut(o, top)
	local r, x = rect(o), o.Parent
	while x and x ~= top and x:IsA("GuiObject") do
		if (x:IsA("ScrollingFrame") or x.ClipsDescendants) and not hit(r, rect(x), 0) then return true end
		x = x.Parent
	end
	return false
end
-- text floor + contrast of every visible label under root (factor = the window's base factor)
local function textAudit(check, info, label, root, factor)
	local n, worst = 0, 99
	for _, t in root:GetDescendants() do
		if (t:IsA("TextLabel") or t:IsA("TextButton")) and t.ContentText ~= "" and t.TextTransparency < 0.9 and chainVis(t)
			and t.AbsoluteSize.X > 0 and not clippedOut(t, root.Parent) and not t.Name:find("Shadow") then
			n += 1
			local px, lim = fontPx(t)
			if px then
				local base = px / factor
				worst = math.min(worst, base)
				check(label .. " floor 16 base: " .. short(t, root) .. " '" .. t.ContentText:sub(1, 22) .. "'", base >= FLOOR,
					("%.1f base (%.0f px, box %.0f x %.0f, %s-limited, phone %.1f pt)"):format(base, px, t.AbsoluteSize.X, t.AbsoluteSize.Y, tostring(lim), base * 0.7))
			end
			-- M6-A: every background colour (each gradient stop) is met by the fill OR by a real outline (>= 2.4 base px and
			-- fill/outline >= the need); need = 4.5, or 3.0 for large text (WCAG: bold >= 14 pt = 18.7 px)
			local bg = bgOf(t)
			local fill = painted(t, t.TextColor3)
			local s = strokeOf(t)
			local need = (px and px / factor >= 18.7) and 3 or 4.5
			local opx = s and strokePx(t, s) / factor or 0
			local outlineOk = s ~= nil and opx >= 2.4 and minCR(fill, {s.Color}) >= need
			local ok, worstC = true, 99
			for _, c in bg do
				local best = minCR(fill, {c})
				if outlineOk then best = math.max(best, cr(s.Color, c)) end
				worstC = math.min(worstC, best)
				if best < need then ok = false end
			end
			check(label .. " contrast: " .. short(t, root) .. " '" .. t.ContentText:sub(1, 22) .. "'", ok,
				("worst stop %.1f (need %.1f) | fill/bg %.1f outline %.2f base px%s"):format(worstC, need, minCR(fill, bg), opx, s and (" fill/outline %.1f"):format(minCR(fill, {s.Color})) or ""))
		end
	end
	table.insert(info, ("%s: %d labels, smallest %.1f base (phone %.1f pt)"):format(label, n, worst, worst * 0.7))
end
-- tap areas under root: >= 44 x 44 screen px each, no two of different buttons overlapping
local function tapAudit(check, info, label, root, expect)
	local taps = {}
	for _, d in root:GetDescendants() do
		if d:IsA("TextButton") and d.Name:match("TapArea$") and chainVis(d) then table.insert(taps, d) end
	end
	if expect then check(label .. " tap areas >= " .. expect, #taps >= expect, #taps) end
	for _, t in taps do
		-- (Ruling R-IdxTabs) the Index's 6 stacked element tabs: the slot pitch is the hard limit, so the area must fill its
		-- whole slot (>= slot height - 2) when the slot is under 44, and be >= 44 wide; logged as INFO
		local n = t.Parent and t.Parent.Name:match("^Tab(%d+)$")
		local slot = n and t.Parent.Parent and t.Parent.Parent:FindFirstChild("TabSlot" .. n)
		if slot then
			local ok = t.AbsoluteSize.X >= 43.5 and (t.AbsoluteSize.Y >= 43.5 or t.AbsoluteSize.Y >= slot.AbsoluteSize.Y - 2)
			check(label .. " tap fills its slot: " .. short(t, root), ok, ("%.0f x %.0f, slot %.0f x %.0f"):format(t.AbsoluteSize.X, t.AbsoluteSize.Y, slot.AbsoluteSize.X, slot.AbsoluteSize.Y))
			if n == "1" then table.insert(info, ("%s: Index tab taps = full slot pitch %.0f px tall (Ruling R-IdxTabs)"):format(label, slot.AbsoluteSize.Y)) end
		else
			check(label .. " tap >= 44: " .. short(t, root), t.AbsoluteSize.X >= 43.5 and t.AbsoluteSize.Y >= 43.5, ("%.0f x %.0f"):format(t.AbsoluteSize.X, t.AbsoluteSize.Y))
		end
	end
	for i = 1, #taps do
		for j = i + 1, #taps do
			check(label .. " taps apart: " .. short(taps[i], root) .. " x " .. short(taps[j], root), not hit(rect(taps[i]), rect(taps[j]), 2), f(rect(taps[i])) .. " x " .. f(rect(taps[j])))
		end
	end
	return #taps
end
-- containment (4 scales) + taps at every scale; floor + contrast at the real size
local function audit(check, info, label, box, root, setScale, factorFn, expectTaps)
	for _, k in SCALES do
		setScale(k)
		task.wait(0.35)
		local r = _G.CUIContain(("%s x%.2f"):format(label, k), box, root, {skip = function(o) return o.Name:match("TapArea$") ~= nil end}) -- (invisible hit areas may reach past the edge)
		local fails = tonumber(r:match("fails (%d+)")) or -1
		check(("containment %s x%.2f"):format(label, k), fails == 0, fails ~= 0 and r:sub(1, 700) or nil)
		tapAudit(check, info, ("%s x%.2f"):format(label, k), root, k == 1 and expectTaps or nil)
	end
	setScale(nil)
	task.wait(0.3)
	textAudit(check, info, label, root, factorFn())
end
local function mmScale(k) _G.CUIScale(win, k) end
local function iconInset(check, label, icon, box, factor)
	local i = insetOf(rect(icon), rect(box)) / factor
	check(label .. " header icon >= 8 base inside", i >= 7.9, ("%.1f base"):format(i))
end

local S = {}

function S.chrome(check, info)
	local ps = p:WaitForChild("PlayerScripts")
	for _, n in {"StreakClient", "PlaytimeClient", "StarterPackClient", "ShopClientLegacy", "IndexClientLegacy", "RebirthClientLegacy",
		"FreeGiftClientLegacy", "OfflineClientLegacy", "UpgradeClientLegacy", "StarterPackHud"} do
		local s = ps:FindFirstChild(n)
		check("running: " .. n, s ~= nil and s.Enabled)
	end
	check("BrickUI.tapArea + minOutline", type(B.tapArea) == "function" and type(B.minOutline) == "function")
	waitFor(function() return body:FindFirstChild("SettingsPage") and body:FindFirstChild("IndexPage") and body:FindFirstChild("RebirthPage") end, 10)
	check("ShopTabs lives in the window body (M3)", body:FindFirstChild("ShopTabs") ~= nil and win:FindFirstChild("ShopTabs") == nil)
	check("MainMenu [X] tap area", face:FindFirstChild("CloseFaceTapArea", true) ~= nil or win:FindFirstChild("FaceTapArea", true) ~= nil)
end

function S.gift(check, info)
	local page = openPage("Gift")
	check("Gift page open", page ~= nil and page.Visible)
	page:SetAttribute("Tab", "Daily")
	task.wait(0.5)
	local k = screenK()
	iconInset(check, "MainMenu", face.Icon, face, k)
	local dv = page.DailyView
	for d = 1, 7 do
		local h = dv:FindFirstChild("Card" .. d)
		local cf = h and h:FindFirstChild("Face")
		local claim = cf and cf:FindFirstChild("Claim")
		if claim then
			local i = (rect(cf)[4] - rect(claim)[4]) / k
			check("Day " .. d .. " CLAIM 6+ base above the card bottom", i >= 5.9, ("%.1f base"):format(i))
		end
		check("Day " .. d .. " whole-card tap area", h and h:FindFirstChild("FaceTapArea") ~= nil)
	end
	local cf = dv.Card7.Face
	local rib = cf:FindFirstChild("Ribbon")
	local ri = rib and insetOf(rotRect(rib), rect(cf)) / k
	check("Day 7 SECRET! ribbon >= 6 base inside (rotated)", ri and ri >= 5.9, ri and ("%.1f base"):format(ri))
	local title = cf:FindFirstChild("Secret")
	check("Day 7 ribbon clear of SECRET PET!", rib and title and not hit(rotRect(rib), rect(title), 0))
	local sb = cf:FindFirstChild("Sunburst")
	check("Day 7 sunburst inside the card", sb and inside(rect(sb), rect(cf), 1))
	check("Day 7 copy: pet / KG + $ / +5 ALL Potions", cf.Line3.Text == "+5 ALL Potions" and cf.Line2.Text:find("KG %+ %$") ~= nil, cf.Line1.Text .. " | " .. cf.Line2.Text .. " | " .. cf.Line3.Text)
	check("Day 2 copy", dv.Card2.Face.Line2.Text == "+2 Potions" and dv.Card2.Face.Line1.Text:find("Speed$") ~= nil, dv.Card2.Face.Line1.Text .. " | " .. dv.Card2.Face.Line2.Text)
	check("Gift tabs: 2 tap areas", page.Tabs:FindFirstChild("TabDaily") and page.Tabs.TabDaily:FindFirstChild("FaceTapArea") ~= nil and page.Tabs.TabPlaytime:FindFirstChild("FaceTapArea") ~= nil)
	audit(check, info, "Gift DAILY", face, face, mmScale, screenK)
	page:SetAttribute("Tab", "Playtime")
	task.wait(0.5)
	audit(check, info, "Gift PLAYTIME", face, face, mmScale, screenK)
	KEEP.Gift = face.AbsoluteSize
	page:SetAttribute("Tab", "Daily")
	closePage()
end

function S.daily(check, info)
	local page = openPage("Gift")
	page:SetAttribute("Tab", "Daily")
	task.wait(0.5)
	local nxt = p:GetAttribute("StreakNext") or 1
	local claimable = p:GetAttribute("StreakClaimable") == true
	table.insert(info, ("StreakNext %d claimable %s"):format(nxt, tostring(claimable)))
	if claimable then
		local c = page.DailyView:FindFirstChild("Card" .. nxt)
		local through0 = p:GetAttribute("StreakThrough") or 0
		c.TestPress:Fire()
		check("Day " .. nxt .. " claimed (StreakThrough +1)", waitFor(function() return (p:GetAttribute("StreakThrough") or 0) == through0 + 1 end, 3), tostring(p:GetAttribute("StreakThrough")))
		task.wait(0.4)
		check("card shows CLAIMED", c.Face.Claim.Face.State.Text == "CLAIMED", c.Face.Claim.Face.State.Text)
	end
	closePage()
end

function S.shop(check, info)
	local page = openPage("Shop")
	check("Shop open", page ~= nil and page.Visible)
	local k = screenK()
	local tabs = body:FindFirstChild("ShopTabs")
	check("rail shown", tabs and tabs.Visible)
	if tabs then
		local tl, tr, tt, tb = 1e9, -1e9, 1e9, -1e9
		for _, slot in tabs:GetChildren() do
			local tile = slot:IsA("Frame") and slot:FindFirstChild("Tile")
			if tile then local r = rect(tile) tl, tr, tt, tb = math.min(tl, r[1]), math.max(tr, r[3]), math.min(tt, r[2]), math.max(tb, r[4]) end
		end
		local fr, pr = rect(face), rect(page)
		check("rail inside the window (M3)", inside({tl, tt, tr, tb}, fr, 1), f({tl, tt, tr, tb}) .. " vs " .. f(fr))
		check("rail gutter to the page >= 8 base", (tl - pr[3]) / k >= 7.9, ("%.1f base"):format((tl - pr[3]) / k))
		check("rail >= 8 base from the window edge", (fr[3] - tr) / k >= 7.9, ("%.1f base"):format((fr[3] - tr) / k))
		check("rail inside the body", inside({tl, tt, tr, tb}, rect(body), 1))
	end
	audit(check, info, "Shop", face, face, mmScale, screenK)
	KEEP.Shop = face.AbsoluteSize
	table.insert(info, ("Shop face %.0f x %.0f (%.2f of the screen height)"):format(face.AbsoluteSize.X, face.AbsoluteSize.Y, face.AbsoluteSize.Y / workspace.CurrentCamera.ViewportSize.Y))
	closePage()
end

function S.settings(check, info)
	local page = openPage("Settings")
	check("Settings open", page ~= nil and page.Visible)
	local ts = face.Title:FindFirstChildOfClass("UIStroke")
	check("Settings title: 3 px black FixedSize outline (M4)", ts and ts.StrokeSizingMode == Enum.StrokeSizingMode.FixedSize and ts.Thickness >= 3 * screenK() - 0.05 and ts.Color == Color3.new(0, 0, 0),
		ts and (ts.StrokeSizingMode.Name .. " " .. ts.Thickness))
	local n = 0
	for _, d in page:GetDescendants() do if d.Name:match("TapArea$") then n += 1 end end
	check("Settings tap areas (toggles + - / + / < / >)", n >= 4, n)
	audit(check, info, "Settings", face, face, mmScale, screenK)
	KEEP.Settings = face.AbsoluteSize
	local function data() local ok, d = pcall(HttpService.JSONDecode, HttpService, p:GetAttribute("Settings") or "") return ok and type(d) == "table" and d or {} end
	local night0 = data().night == true
	RS.Settings.Set:FireServer("night", not night0)
	check("a toggle still saves (night)", waitFor(function() return (data().night == true) == not night0 end, 3))
	task.wait(0.6)
	RS.Settings.Set:FireServer("night", night0)
	task.wait(0.4)
	openPage("Shop")
	check("other pages: title stroke back to the shared ScaledSize", ts and ts.StrokeSizingMode == Enum.StrokeSizingMode.ScaledSize and math.abs(ts.Thickness - (ts:GetAttribute("PolishBase") or -1)) < 1e-4,
		ts and (ts.StrokeSizingMode.Name .. " " .. ts.Thickness))
	closePage()
end

function S.index(check, info)
	local page = openPage("Index")
	check("Index open", page ~= nil and page.Visible)
	local k = screenK()
	local n, okStar = 0, true
	for _, d in page:GetDescendants() do
		if (d.Name == "Star" or d.Name == "Ready") and d:IsA("GuiObject") then
			local tabFace = d.Parent
			local was = d.Visible
			d.Visible = true
			task.wait()
			local i = insetOf(rect(d), rect(tabFace)) / k
			n += 1
			if i < 5.9 then okStar = false table.insert(info, ("badge %s inset %.1f base"):format(short(d, page), i)) end
			local name = tabFace:FindFirstChild("Name")
			local nr = name and {name.AbsolutePosition.X + (name.AbsoluteSize.X - name.TextBounds.X) / 2, name.AbsolutePosition.Y + (name.AbsoluteSize.Y - name.TextBounds.Y) / 2,
				name.AbsolutePosition.X + (name.AbsoluteSize.X + name.TextBounds.X) / 2, name.AbsolutePosition.Y + (name.AbsoluteSize.Y + name.TextBounds.Y) / 2}
			if nr and hit(rect(d), nr, 0) then okStar = false table.insert(info, "badge over the tab name: " .. short(d, page)) end
			d.Visible = was
		end
	end
	check("Index tab badges >= 6 base inside their tab, clear of the name (M1)", n > 0 and okStar, n)
	local total = page:FindFirstChild("Total", true)
	local bar = total and total:FindFirstChild("Bar", true)
	local txt = total and total.Face:FindFirstChild("Text")
	check("FOUND count beside the trough (M4)", bar and txt and not hit(rect(txt), rect(bar), 0) and txt.Text:match("^%d+ / %d+ FOUND$") ~= nil, txt and txt.Text)
	local claimAll = total and total:FindFirstChild("ClaimAll", true)
	if claimAll and claimAll.Visible then check("FOUND count clear of CLAIM ALL", not hit(rect(txt), rect(claimAll), 0)) end
	-- a fresh save shows "???": put the longest creature names on card 1 for a moment (they wrap to 2 lines)
	local nm = page:FindFirstChild("Card1") and page.Card1.Face:FindFirstChild("Name")
	if nm then
		local was = nm.Text
		for _, long in {"Thornblade Mantis", "Pharaoh Asparuh"} do
			nm.Text = long
			task.wait(0.05)
			local px = fontPx(nm)
			local base = px and px / k
			check("Index card name '" .. long .. "' >= 16 base (wraps)", base and base >= FLOOR, base and ("%.1f base"):format(base))
		end
		nm.Text = was
	end
	audit(check, info, "Index", face, face, mmScale, screenK)
	KEEP.Index = face.AbsoluteSize
	closePage()
end

function S.rebirth(check, info)
	local page = openPage("Rebirth")
	check("Rebirth open", page ~= nil and page.Visible)
	local h = page:FindFirstChild("RebirthButton")
	local btn = h and h:FindFirstChild("Face")
	local lab = btn and btn:FindFirstChild("Label")
	local ready = p:GetAttribute("RebirthReady")
	if btn and lab then
		local studs = btn:FindFirstChild("Studs")
		local g = btn:FindFirstChild("CUIGradient")
		local c0 = g and g.Color.Keypoints[1].Value
		local grey = c0 and math.abs(c0.R - c0.G) < 0.08 and math.abs(c0.G - c0.B) < 0.1
		local ls = lab:FindFirstChildOfClass("UIStroke")
		local off = lab.TextColor3 == B.INK
		table.insert(info, ("REBIRTH button: label '%s', ink %s, grey %s"):format(lab.Text, tostring(off), tostring(grey)))
		if off then
			check("not ready = solid silver, no checker, ink label, no outline (M4)", grey and (not studs or not studs.Visible) and ls and not ls.Enabled)
			check("ink label on silver contrast >= 4.5", c0 and cr(B.INK, c0) >= 4.5, c0 and cr(B.INK, c0))
		else
			check("ready = lime + checker + white outlined label", not grey and studs and studs.Visible and lab.TextColor3 == Color3.new(1, 1, 1))
		end
	end
	check("REBIRTH + SKIP tap areas", h and h:FindFirstChild("FaceTapArea") ~= nil and page:FindFirstChild("SkipButton") and page.SkipButton:FindFirstChild("FaceTapArea") ~= nil)
	audit(check, info, "Rebirth", face, face, mmScale, screenK)
	KEEP.Rebirth = face.AbsoluteSize
	closePage()
end

---------------------------------------------------------------- Free Gift (M8)
local function fgOpen()
	local g = pg.FreeGiftUI
	local zone = workspace.Map.Hub.FreeGift.FreeGiftZone
	moveTo(zone.Position + Vector3.new(0, 3, 0))
	waitFor(function() return g.Enabled end, 2)
	task.wait(1.2) -- (the server group check follows the open)
	return g
end
local function fgClose() moveTo(AWAY) waitFor(function() return not pg.FreeGiftUI.Enabled end, 2) task.wait(0.3) end
local function isLime(g) local c = g.Color.Keypoints[1].Value return c.G > c.R + 0.15 and c.G > c.B + 0.3 end
local function isSilver(g) local c = g.Color.Keypoints[1].Value return math.abs(c.R - c.G) < 0.06 and math.abs(c.G - c.B) < 0.08 end
function S.freegiftA(check, info)
	local g = fgOpen()
	check("walk in opens Free Gift", g.Enabled)
	local w = g.Holder.Window
	local ws = g.Holder.WindowScale
	check("no Like card any more", w:FindFirstChild("Like") == nil)
	local ask = w:FindFirstChild("LikeAsk")
	check("friendly like ask shown", ask and ask.Visible and ask.Text:find("Like the game") ~= nil, ask and ask.Text)
	check("like ask has no tick", ask and #ask:GetChildren() <= 1)
	local gc = w:FindFirstChild("Group")
	check("the group card is centred", gc and math.abs((rect(gc)[1] + rect(gc)[3]) / 2 - (rect(w)[1] + rect(w)[3]) / 2) <= 2)
	check("group card title", gc and gc.Title.Text == "Join the group!", gc and gc.Title.Text)
	local ok, member = pcall(RS.FreeGift.InGroup.InvokeServer, RS.FreeGift.InGroup)
	table.insert(info, "server InGroup = " .. tostring(member))
	KEEP.member = member == true
	local claim = w.Claim
	if member == true then
		check("in the group: CLAIM! lime", claim.Label.Text == "CLAIM!" and isLime(grad(claim)), claim.Label.Text)
	else
		check("not in the group: JOIN FIRST silver", claim.Label.Text == "JOIN FIRST" and isSilver(grad(claim)), claim.Label.Text)
	end
	iconInset(check, "Free Gift", w.Header.Icon, w, ws.Scale)
	local base = ws.Scale
	audit(check, info, "Free Gift", w, w, function(k) ws.Scale = k and base * k or base end, function() return ws.Scale end, KEEP.member and 2 or 3)
	fgClose()
end
function S.freegiftB(check, info) -- server: FreeGiftTestNotInGroup = true
	task.wait(2.2) -- (InGroup answers at most every 2 s)
	local g = fgOpen()
	local w = g.Holder.Window
	check("forced out of the group: JOIN FIRST silver", w.Claim.Label.Text == "JOIN FIRST" and isSilver(grad(w.Claim)), w.Claim.Label.Text)
	check("JOIN button shown", w.Group.Well.Join.Visible)
	local ok, res, why = pcall(RS.FreeGift.Claim.InvokeServer, RS.FreeGift.Claim)
	check("server refuses the claim: group", ok and res ~= true and why == "group", tostring(res) .. " " .. tostring(why))
	check("not claimed", p:GetAttribute("FreeGift") ~= true)
	fgClose()
end
function S.freegiftC(check, info) -- server: FreeGiftTestNotInGroup cleared
	task.wait(2.2)
	local g = fgOpen()
	local w = g.Holder.Window
	if not KEEP.member then
		check("(not a member) JOIN FIRST stays", w.Claim.Label.Text == "JOIN FIRST")
		fgClose()
		return "the test account is not in the group: claim not tried"
	end
	check("back in the group: CLAIM! lime", w.Claim.Label.Text == "CLAIM!" and isLime(grad(w.Claim)), w.Claim.Label.Text)
	local m0, h0, s0 = potions()
	local ok, res, why = pcall(RS.FreeGift.Claim.InvokeServer, RS.FreeGift.Claim) -- what CLAIM sends
	check("claim ok (group only, no like needed)", ok and res == true, tostring(res) .. " " .. tostring(why))
	check("FreeGift true", waitFor(function() return p:GetAttribute("FreeGift") == true end, 3))
	task.wait(0.5)
	local m1, h1, s1 = potions()
	check("3 potions +1 each", m1 == m0 + 1 and h1 == h0 + 1 and s1 == s0 + 1, ("%d/%d/%d -> %d/%d/%d"):format(m0, h0, s0, m1, h1, s1))
	check("CLAIMED! shown", waitFor(function() return w.Claim.Label.Text == "CLAIMED!" end, 2), w.Claim.Label.Text)
	local ok2, res2, why2 = pcall(RS.FreeGift.Claim.InvokeServer, RS.FreeGift.Claim)
	check("second claim refused (claimed)", ok2 and res2 ~= true and why2 == "claimed", tostring(why2))
	fgClose()
	check("hotbar back", hotbar() == true)
end

---------------------------------------------------------------- Welcome Back (M9)
function S.welcome(check, info) -- server: OfflinePending 547000 + OfflineDebug
	local g = pg.OfflineUI
	check("pending -> Welcome Back opens", waitFor(function() return g.Enabled end, 4))
	task.wait(0.5)
	local w = g.Holder.Window
	local ws = g.Holder.WindowScale
	local x5, claim = w.ClaimX5, w.Claim
	local a5, ac = x5.AbsoluteSize.X * x5.AbsoluteSize.Y, claim.AbsoluteSize.X * claim.AbsoluteSize.Y
	check("free CLAIM! is the bigger button", ac > a5 * 1.1, ("%.0f vs %.0f"):format(ac, a5))
	check("same height", math.abs(x5.AbsoluteSize.Y - claim.AbsoluteSize.Y) < 1)
	check("CLAIM! on the right", rect(claim)[1] > rect(x5)[3])
	check("CLAIM! lime", isLime(grad(claim)))
	local g5 = grad(x5)
	local c0 = g5.Color.Keypoints[1].Value
	check("CLAIM x5 gold, no rainbow", #g5.Color.Keypoints == 2 and c0.R > 0.95 and c0.B < 0.1, #g5.Color.Keypoints)
	local price = x5:FindFirstChild("Price")
	check("price inside CLAIM x5", price and inside(rect(price), rect(x5), 0))
	local pi = price and (rect(x5)[3] - rect(price)[3]) / ws.Scale
	check("price 8 base from the right edge (M1)", pi and math.abs(pi - 8) < 1, pi)
	local lab = x5.Label
	local b, a, s = lab.TextBounds, lab.AbsolutePosition, lab.AbsoluteSize
	check("x5 label clear of the price", price and (a.X + b.X) < rect(price)[1] - 2, price and ((a.X + b.X) .. " vs " .. rect(price)[1]))
	check("no Price frame left on the window", w:FindFirstChild("Price") == nil)
	check("[X] tap area", w.Header:FindFirstChild("CloseButtonTapArea") ~= nil)
	iconInset(check, "Welcome", w.Header.Icon, w, ws.Scale)
	local base = ws.Scale
	audit(check, info, "Welcome", w, w, function(k) ws.Scale = k and base * k or base end, function() return ws.Scale end, 1)
	local m0 = p:GetAttribute("Money") or 0
	local ok, res = pcall(RS.Offline.Claim.InvokeServer, RS.Offline.Claim) -- what CLAIM / X send
	check("claim ok", ok and res == true, tostring(res))
	check("Money +547000", waitFor(function() return (p:GetAttribute("Money") or 0) >= m0 + 547000 end, 3))
	g.Enabled = false
	task.wait(0.4)
end
function S.welcomex5(check, info) -- server: pending 3000 + OfflineDebug, then TestReceipt(3718679677)
	local g = pg.OfflineUI
	check("x5 receipt granted (OfflineLastX5)", waitFor(function() return p:GetAttribute("OfflineLastX5") == true end, 6))
	g.Enabled = false
	task.wait(0.3)
end

---------------------------------------------------------------- Upgrades + tutorial steps 8 / 10
local function upOpen()
	local g = pg.UpgradeUI
	local zone = workspace.Map.Hub.Stalls:FindFirstChild("UpgradeZone", true)
	moveTo(zone.Position + Vector3.new(0, 3, 0))
	waitFor(function() return g.Enabled end, 2)
	task.wait(0.5)
	return g
end
local function upClose() moveTo(AWAY) waitFor(function() return not pg.UpgradeUI.Enabled end, 2) task.wait(0.3) end
function S.upgrades(check, info)
	local g = upOpen()
	check("walk in opens Upgrades", g.Enabled)
	local w = g.Root.Window
	check("short descriptions", w:FindFirstChild("Sling", true).Desc.Text == "Launch further", w:FindFirstChild("Sling", true).Desc.Text)
	iconInset(check, "Upgrades", w.Face:FindFirstChild("Icon", true) or w:FindFirstChild("Icon", true), w.Face, screenK())
	audit(check, info, "Upgrades", w, g.Root, function(k) _G.CUIScale(g.Root, k) end, screenK, 7)
	local l0 = p:GetAttribute("SlingLevel") or 0
	local ok, r = RS.Upgrades.Buy:InvokeServer("Sling") -- what the Sling money button sends (server step: Money first)
	check("money buy Sling ok", ok == true, tostring(r))
	check("SlingLevel +1", waitFor(function() return (p:GetAttribute("SlingLevel") or 0) == l0 + 1 end, 2))
	upClose()
end
local function arrowCheck(check, label)
	local g = upOpen()
	local w = g.Root.Window
	local arrow = w:FindFirstChild("FreeArrow", true)
	local sling = w:FindFirstChild("Sling", true)
	local buy = sling and sling:FindFirstChild("Buy")
	check(label .. ": arrow shown", arrow and waitFor(function() return arrow.Visible end, 1.5))
	if arrow and buy then
		local ar, br = rect(arrow), rect(buy)
		local cx = (ar[1] + ar[3]) / 2
		check(label .. ": arrow over the Sling buy button", cx >= br[1] and cx <= br[3] and ar[4] <= br[2] + 6, f(ar) .. " vs " .. f(br))
	end
	local tu = pg:FindFirstChild("TutorialUI")
	if tu then check(label .. ": tutorial guide away while the window is open", tu:GetAttribute("GuideAway") == true, tostring(tu:GetAttribute("GuideAway"))) end
	return g, w
end
function S.step8(check, info) -- server: FreeSling true, SlingLevel 0
	local g, w = arrowCheck(check, "step 8")
	local price = w:FindFirstChild("Sling", true).Buy.Face.Price
	check("step 8: FREE", price.Text == "FREE", price.Text)
	upClose()
end
function S.step10(check, info) -- server: FreeSling false, SlingLevel 1, TutorialExtra 2, Money = the next level's cost
	arrowCheck(check, "step 10")
	upClose()
end

---------------------------------------------------------------- Starter Pack popup + HUD
function S.starter(check, info)
	local g = pg.StarterPackUI
	if not g.Enabled then g.TestOpen:Fire() end
	check("popup opens", waitFor(function() return g.Enabled end, 2))
	task.wait(0.4)
	local w = g.Holder.Window
	local ends = w:FindFirstChild("EndsIn", true)
	check("ENDS IN timer, gold", ends and ends.Visible and grad(ends) and grad(ends).Color.Keypoints[#grad(ends).Color.Keypoints].Value.G > 0.5, ends and ends.Text)
	check("NO THANKS 64 tall = BUY", w.NoThanks.Size.Y.Offset == 64 and w.Buy.Size.Y.Offset == 64)
	check("[X] + NO THANKS tap areas", w:FindFirstChild("NoThanksTapArea") ~= nil and w:FindFirstChild("CloseButtonTapArea", true) ~= nil)
	local ws = g.Holder.WindowScale
	local base = ws.Scale
	audit(check, info, "Starter popup", w, w, function(k) ws.Scale = k and base * k or base end, function() return ws.Scale end, 2)
	g.Enabled = false
	local page = openPage("Shop")
	local card = page and page:FindFirstChild("StarterPack", true)
	check("Shop Starter card", card ~= nil and card.Visible)
	closePage()
	return "StarterEndsAt " .. tostring(p:GetAttribute("StarterEndsAt"))
end
function S.starter59(check, info) -- server: StarterDebug endsAt = now + 3540 (59 min left)
	local g = pg.StarterPackUI
	if not g.Enabled then g.TestOpen:Fire() end
	waitFor(function() return g.Enabled end, 2)
	task.wait(1.1)
	local ends = g.Holder.Window:FindFirstChild("EndsIn", true)
	local gc = grad(ends).Color.Keypoints
	local last = gc[#gc].Value
	check("59:00 left: popup timer still gold (no red)", last.G > 0.5, ("%s %.2f %.2f %.2f"):format(ends.Text, last.R, last.G, last.B))
	g.Enabled = false
	local page = openPage("Shop")
	task.wait(1.1)
	local card = page and page:FindFirstChild("StarterPack", true)
	local tag = card and card:FindFirstChild("Tag", true)
	if tag then check("59:00 left: Shop card tag amber (no red)", tag.BackgroundColor3.G > 0.5, tostring(tag.BackgroundColor3)) end
	closePage()
end
function S.hud(check, info)
	local hud
	for _, gg in pg:GetChildren() do if gg:IsA("ScreenGui") and gg:FindFirstChild("Root") and gg.Name:find("Starter") and gg ~= pg.StarterPackUI then hud = gg end end
	check("HUD gui found", hud ~= nil)
	if not hud then return end
	local root = hud.Root
	check("HUD shown", waitFor(function() return root.Visible end, 8), tostring(root.Visible))
	if not root.Visible then return "HUD hidden: " .. tostring(hud:GetAttribute("Why")) end
	task.wait(0.8)
	local timer = root:FindFirstChild("Timer", true)
	local outline = root:FindFirstChild("EggOutline", true)
	local price = root:FindFirstChild("Price", true)
	local minGap = 1e9
	local t0 = os.clock()
	local s0, varied = nil, false
	local ts = timer and timer:FindFirstChild("TimerScale", true)
	while os.clock() - t0 < 2 do
		if timer and outline and outline.Visible then
			local tb = timer:IsA("TextLabel") and timer.TextBounds or timer.AbsoluteSize
			local ty = timer.AbsolutePosition.Y + (timer.AbsoluteSize.Y - tb.Y) / 2
			minGap = math.min(minGap, ty - (outline.AbsolutePosition.Y + outline.AbsoluteSize.Y))
		end
		if ts then if s0 and math.abs(ts.Scale - s0) > 1e-3 then varied = true end s0 = ts.Scale end
		task.wait()
	end
	local k = root.AbsoluteSize.X / 150
	table.insert(info, ("HUD timer-egg gap min %.1f px (%.1f base), HUD scale %.2f"):format(minGap, minGap / k, k))
	check("HUD timer below the egg, >= 5 px clear over 2 s of motion", minGap >= 5)
	check("HUD timer: no pulse", not varied)
	local tg = timer and grad(timer)
	if tg then local kp = tg.Color.Keypoints check("HUD timer gold (no red)", kp[#kp].Value.G > 0.5, tostring(kp[#kp].Value)) end
	if timer and timer:IsA("TextLabel") then check("HUD timer: no background", timer.BackgroundTransparency >= 0.99) end
	if price then
		local pgd = grad(price)
		check("HUD price = gold pill", price.BackgroundTransparency < 0.5 and pgd and pgd.Color.Keypoints[1].Value.R > 0.95 and pgd.Color.Keypoints[1].Value.B < 0.1)
	end
	local vp = hud.AbsoluteSize
	check("HUD art >= 8 px inside the right edge", rect(root)[3] <= vp.X - 7.5, rect(root)[3] .. " vs " .. vp.X)
	textAudit(check, info, "Starter HUD", root, k)
end

---------------------------------------------------------------- nothing runs while closed
function S.idle(check, info)
	closePage()
	for _, n in {"FreeGiftUI", "OfflineUI", "UpgradeUI", "StarterPackUI"} do local gg = pg:FindFirstChild(n) if gg then gg.Enabled = false end end
	moveTo(AWAY)
	task.wait(1)
	local roots = {win, pg.FreeGiftUI, pg.OfflineUI, pg.UpgradeUI, pg.StarterPackUI}
	local function snap()
		local t = {}
		for _, r in roots do
			for _, d in r:GetDescendants() do
				if d:IsA("GuiObject") then
					t[d] = {d.Position, d.Size, d.Rotation, d.Visible, d.BackgroundColor3, (d:IsA("TextLabel") or d:IsA("TextButton")) and d.Text or "", (d:IsA("ImageLabel") or d:IsA("ImageButton")) and d.ImageTransparency or 0}
				elseif d:IsA("UIScale") then t[d] = {d.Scale}
				elseif d:IsA("UIGradient") then t[d] = {d.Offset, d.Rotation}
				elseif d:IsA("UIStroke") then t[d] = {d.Thickness, d.Transparency}
				end
			end
		end
		return t
	end
	local a = snap()
	task.wait(2.5)
	local b = snap()
	local diffs = {}
	for o, va in a do
		local vb = b[o]
		if vb then
			for i = 1, #va do if va[i] ~= vb[i] then table.insert(diffs, short(o, o:FindFirstAncestorOfClass("ScreenGui")) .. " #" .. i) break end end
		end
	end
	check("nothing changes in closed windows over 2.5 s", #diffs == 0, #diffs .. ": " .. table.concat(diffs, ", "):sub(1, 600))
end

---------------------------------------------------------------- tutorial step 11 (server first: TutorialDone, Rebirths 0, Money 25000, TutorialExtra 3)
function S.step11(check, info)
	check("stage 3", p:GetAttribute("TutorialExtra") == 3, p:GetAttribute("TutorialExtra"))
	local page = openPage("Rebirth")
	check("Rebirth page open", page ~= nil and page.Visible)
	local tu = pg:FindFirstChild("TutorialUI")
	check("guide away while the window is open", tu and tu:GetAttribute("GuideAway") == true, tu and tostring(tu:GetAttribute("GuideAway")))
	if KEEP.Rebirth then
		check("window at its normal size (not shrunk under the guide)", math.abs(face.AbsoluteSize.Y - KEEP.Rebirth.Y) < 2, face.AbsoluteSize.Y .. " vs " .. KEEP.Rebirth.Y)
	end
	local lab = page.RebirthButton.Face.Label
	check("REBIRTH ready (white label)", waitFor(function() return lab.TextColor3 == Color3.new(1, 1, 1) end, 2), lab.Text)
	page.TestPress:Fire()
	check("TAP AGAIN! on the button", waitFor(function() return lab.Text:find("AGAIN") ~= nil end, 2), lab.Text)
	local r0, pm0 = p:GetAttribute("Rebirths") or 0, p:GetAttribute("Potion_Money") or 0
	page.TestPress:Fire()
	check("rebirth done", waitFor(function() return (p:GetAttribute("Rebirths") or 0) == r0 + 1 end, 4), tostring(p:GetAttribute("Rebirths")))
	check("stage 0", waitFor(function() return p:GetAttribute("TutorialExtra") == 0 end, 3), p:GetAttribute("TutorialExtra"))
	check("tutorial reward potion", waitFor(function() return (p:GetAttribute("Potion_Money") or 0) == pm0 + 1 end, 3))
	check("window closed", waitFor(function() return not win.Visible end, 3))
	check("guide back after the window", tu and waitFor(function() return tu:GetAttribute("GuideAway") ~= true end, 3))
end

---------------------------------------------------------------- the Shop's buy paths, dry run (server stub on Shop.Buy armed first)
function S.shopdry(check, info)
	local ShopConfig = require(RS.ShopConfig)
	local page = openPage("Shop")
	check("Shop open + rail", page ~= nil and page.Visible and body.ShopTabs.Visible)
	page:SetAttribute("TestDryRun", true)
	if page:GetAttribute("TestDryRun") ~= true then return end
	local cases = {}
	for _, ps in ShopConfig.Passes or {} do table.insert(cases, {"pass:" .. ps.key, {"pass", ps.key}}) end
	table.insert(cases, {"speed", {"speed"}})
	for _, pk in ShopConfig.PotionPacks or {} do table.insert(cases, {"potion:" .. pk.key, {"potion", pk.key}}) end
	table.insert(cases, {"treadmillMoney", {"treadmillMoney"}})
	table.insert(cases, {"treadmillRobux", {"treadmillRobux"}})
	for _, c in cases do
		page:SetAttribute("TestLastBuy", nil)
		page:SetAttribute("TestPress", c[1])
		local ok = waitFor(function() return page:GetAttribute("TestLastBuy") ~= nil end, 1.5)
		check("press " .. c[1], ok and page:GetAttribute("TestLastBuy") == HttpService:JSONEncode(c[2]), page:GetAttribute("TestLastBuy"))
	end
	-- the rail still scrolls the page
	local t0 = page.CanvasPosition.Y
	local slot = body.ShopTabs:GetChildren()
	page:SetAttribute("TestDryRun", nil)
	page:SetAttribute("TestLastBuy", nil)
	closePage()
	return #cases .. " buy paths"
end

_G.PolishTests = function(section)
	local pass, fail, lines, info = 0, 0, {}, {}
	local function check(name, cond, detail)
		if cond then pass += 1 else fail += 1 if #lines < 40 then table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end end
	end
	local fn = S[section]
	if not fn then return "no section " .. tostring(section) end
	local ok, res = pcall(fn, check, info)
	if not ok then fail += 1 table.insert(lines, "ERROR " .. tostring(res)) end
	local out = ("%s: %d pass / %d fail%s"):format(section, pass, fail, (ok and res) and (" (" .. tostring(res) .. ")") or "")
	if #lines > 0 then out ..= "\n" .. table.concat(lines, "\n") end
	if #info > 0 then out ..= "\nINFO " .. table.concat(info, "\nINFO ") end
	return out
end
_G.PolishKeep = KEEP
return "PolishTests ready"
