-- revert_client.lua (2026-10-22, owner: "okay just return the old ui"): client checks for the RESTORED Check-UI windows.
-- Client datamodel of a FRESH TestFreshSave Play session. Paste checkui_contain.lua (tests-2026-10-21) first, then this
-- file once (stores _G.RevertTests); run: return _G.RevertTests("chrome") etc.
-- Sections (order used): chrome, gift, pages (containment, 4 scales, every MainMenu page), playrefuse, settings,
--   index (after the Server step "complete area 1"), starter (after StarterDebug "reset"), freegift, welcome (after the
--   Server step "pending 547000"), welcomex5 (after "pending 3000" + TestReceipt 3718679677), upgrades (after Money),
--   step11a / step11b (tutorial step 11 on the old Rebirth page, Server step first), shopdry (LAST: the Server stub on
--   Shop.Buy is armed first, so even a hook bug can't reach a real prompt).
-- No real prompt anywhere: Robux buys only through ShopPage TestDryRun / ServerStorage.TestReceipt; claims use the same
-- remotes the buttons use (as streak_client_v1 does); never a mouse click.
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local HttpService = game:GetService("HttpService")
local p = Players.LocalPlayer
local pg = p:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local face = win:WaitForChild("Face")
local body = face:WaitForChild("Body")
local SCALES = {1, 0.85, 0.7, 0.55}

local function waitFor(f, secs)
	local t0 = os.clock()
	while os.clock() - t0 < secs do
		if f() then return true end
		task.wait(0.05)
	end
	return f()
end
local function rect(o) local a, s = o.AbsolutePosition, o.AbsoluteSize return {a.X, a.Y, a.X + s.X, a.Y + s.Y} end
local function inside(a, b, tol) tol = tol or 1 return a[1] >= b[1] - tol and a[2] >= b[2] - tol and a[3] <= b[3] + tol and a[4] <= b[4] + tol end
local function hit(a, b) return a[1] < b[3] - 1 and b[1] < a[3] - 1 and a[2] < b[4] - 1 and b[2] < a[4] - 1 end
local function f(r) return ("[%.0f %.0f %.0f %.0f]"):format(r[1], r[2], r[3], r[4]) end
local function rotRect(o) -- the rotated box's bounds
	local a, s = o.AbsolutePosition, o.AbsoluteSize
	local r = math.rad(o.Rotation)
	local cx, cy = a.X + s.X / 2, a.Y + s.Y / 2
	local hw = (math.abs(math.cos(r)) * s.X + math.abs(math.sin(r)) * s.Y) / 2
	local hh = (math.abs(math.sin(r)) * s.X + math.abs(math.cos(r)) * s.Y) / 2
	return {cx - hw, cy - hh, cx + hw, cy + hh}
end
local function count(parent, name) local n = 0 for _, c in parent:GetChildren() do if c.Name == name then n += 1 end end return n end
local function openPage(name)
	if win.Visible then mm.CloseWindow:Fire() waitFor(function() return not win.Visible end, 1.5) task.wait(0.3) end
	mm.OpenPage:Fire(name)
	waitFor(function() return win.Visible end, 2)
	task.wait(0.6)
	return body:FindFirstChild(name .. "Page")
end
local function closePage() if win.Visible then mm.CloseWindow:Fire() waitFor(function() return not win.Visible end, 1.5) task.wait(0.3) end end
local function hotbar() local bp = pg:FindFirstChild("BackpackGui") return bp and bp.Enabled end
local function potions() return p:GetAttribute("Potion_Money") or 0, p:GetAttribute("Potion_Hatch") or 0, p:GetAttribute("Potion_Speed") or 0 end
local function moveTo(pos) p.Character:PivotTo(CFrame.new(pos)) end
local AWAY = Vector3.new(0, 5, -100)
local function containAll(check, label, box, root, setScale) -- setScale(k) at 1 / 0.85 / 0.7 / 0.55, then setScale(nil) restores
	for _, k in SCALES do
		setScale(k)
		task.wait(0.35)
		local r = _G.CUIContain(("%s x%.2f"):format(label, k), box, root, {})
		local fails = tonumber(r:match("fails (%d+)")) or -1
		check(("containment %s x%.2f"):format(label, k), fails == 0, fails ~= 0 and r:sub(1, 600) or nil)
	end
	setScale(nil)
	task.wait(0.2)
end
local function chrome(check, label)
	check(label .. ": Check-UI Header shown", face.Header.Visible)
	check(label .. ": HatchBack / HatchFront hidden", not win.HatchBack.Visible and not win.HatchFront.Visible)
	check(label .. ": face drawn (not transparent)", face.BackgroundTransparency < 1)
	check(label .. ": header icon inside the window", inside(rect(face.Icon), rect(face)), f(rect(face.Icon)) .. " vs " .. f(rect(face)))
end

local S = {}

function S.chrome(check)
	local ps = p:WaitForChild("PlayerScripts")
	for _, n in {"StreakClient", "PlaytimeClient", "StarterPackClient", "ShopClientLegacy", "IndexClientLegacy", "RebirthClientLegacy",
		"FreeGiftClientLegacy", "OfflineClientLegacy", "UpgradeClientLegacy", "StarterPackHud"} do
		local s = ps:FindFirstChild(n)
		check("running: " .. n, s ~= nil and s.Enabled)
	end
	for _, n in {"ShopClient", "SettingsClient", "IndexClient", "RebirthClient", "FreeGiftClient", "OfflineClient", "UpgradeClient"} do
		check("parked (absent): " .. n, ps:FindFirstChild(n) == nil)
	end
	check("StreakClient = the pre-HATCH copy", ps.StreakClient:GetAttribute("RestoredFrom") ~= nil, ps.StreakClient:GetAttribute("RestoredFrom"))
	waitFor(function() return body:FindFirstChild("SettingsPage") and body:FindFirstChild("IndexPage") and body:FindFirstChild("RebirthPage") end, 10)
	for _, n in {"GiftPage", "ShopPage", "SettingsPage", "IndexPage", "RebirthPage"} do
		check("exactly 1 " .. n, count(body, n) == 1, count(body, n))
		local pgx = body:FindFirstChild(n)
		check(n .. " has no HatchCanvas", pgx and pgx:GetAttribute("HatchCanvas") == nil)
	end
	for _, n in {"FreeGiftUI", "OfflineUI", "UpgradeUI", "StarterPackUI"} do check("exactly 1 " .. n, count(pg, n) == 1, count(pg, n)) end
	check("Free Gift = Check-UI Holder.Window", pg.FreeGiftUI.Holder:FindFirstChild("Window") ~= nil and pg.FreeGiftUI.Holder:FindFirstChild("HatchFront") == nil)
	check("Welcome Back = Check-UI Holder.Window", pg.OfflineUI.Holder:FindFirstChild("Window") ~= nil and pg.OfflineUI.Holder:FindFirstChild("HatchFront") == nil)
	check("Upgrades = Check-UI Root.Window", pg.UpgradeUI:FindFirstChild("Root") ~= nil and pg.UpgradeUI.Root:FindFirstChild("Window") ~= nil)
	check("Starter popup = old 540 x 430 Holder", pg.StarterPackUI.Holder.Size == UDim2.fromOffset(540, 430), tostring(pg.StarterPackUI.Holder.Size))
	check("Starter popup has no Canvas (HATCH)", pg.StarterPackUI.Holder:FindFirstChild("Canvas") == nil)
	check("StarterPackHud kept", pg:FindFirstChild("StarterPackHud", true) ~= nil or p.PlayerScripts:FindFirstChild("StarterPackHud") ~= nil)
end

-- the Gift window's 3 fixed defects + PLAYTIME 4x3
function S.gift(check)
	local page = openPage("Gift")
	check("Gift page open", page ~= nil and page.Visible)
	chrome(check, "Gift")
	page:SetAttribute("Tab", "Daily")
	task.wait(0.4)
	local tabs = page.Tabs
	local daily, play = tabs.TabDaily, tabs.TabPlaytime
	local dot = daily:FindFirstChild("Dot", true)
	check("Dot exists", dot ~= nil)
	if dot then
		local wasVis = dot.Visible
		dot.Visible = true
		task.wait(0.1)
		check("Dot inside the DAILY tab", inside(rect(dot), rect(daily.Face), 3), f(rect(dot)) .. " vs " .. f(rect(daily.Face)))
		check("Dot clear of the PLAYTIME tab", not hit(rect(dot), rect(play)), f(rect(dot)) .. " x " .. f(rect(play)))
		local lab = daily.Face:FindFirstChild("Label")
		if lab then
			local b, a, s = lab.TextBounds, lab.AbsolutePosition, lab.AbsoluteSize
			local tr = {a.X + (s.X - b.X) / 2, a.Y + (s.Y - b.Y) / 2, a.X + (s.X + b.X) / 2, a.Y + (s.Y + b.Y) / 2}
			check("Dot clear of the DAILY word", not hit(rect(dot), tr), f(rect(dot)) .. " x " .. f(tr))
		end
		dot.Visible = wasVis
	end
	local c7 = page.DailyView.Card7
	local cf = c7:FindFirstChild("Face") or c7
	local rib = cf:FindFirstChild("Ribbon")
	check("SECRET! ribbon inside Day 7 (rotated bounds)", rib and inside(rotRect(rib), rect(cf), 1), rib and (f(rotRect(rib)) .. " vs " .. f(rect(cf))))
	local sb = cf:FindFirstChild("Sunburst")
	check("Day 7 sunburst inside the card", sb and inside(rect(sb), rect(cf), 1), sb and (f(rect(sb)) .. " vs " .. f(rect(cf))))
	containAll(check, "Gift DAILY", face, face, function(k) _G.CUIScale(win, k) end)
	page:SetAttribute("Tab", "Playtime")
	task.wait(0.5)
	local xs, ys, n = {}, {}, 0
	for i = 1, 12 do
		local s = page.PlaytimeView.Grid.Cells:FindFirstChild("Slot" .. i)
		if s then n += 1 xs[math.floor(s.AbsolutePosition.X + 0.5)] = true ys[math.floor(s.AbsolutePosition.Y + 0.5)] = true end
	end
	local nx, ny = 0, 0 for _ in xs do nx += 1 end for _ in ys do ny += 1 end
	check("PLAYTIME: 12 slots in 4 columns x 3 rows", n == 12 and nx == 4 and ny == 3, n .. " slots, " .. nx .. " x " .. ny)
	containAll(check, "Gift PLAYTIME", face, face, function(k) _G.CUIScale(win, k) end)
	page:SetAttribute("Tab", "Daily")
	closePage()
end

-- containment (4 scales) + old chrome for the other MainMenu pages
function S.pages(check)
	for _, name in {"Shop", "Settings", "Index", "Rebirth"} do
		local page = openPage(name)
		check(name .. " page open", page ~= nil and page.Visible)
		chrome(check, name)
		containAll(check, name, face, face, function(k) _G.CUIScale(win, k) end)
	end
	local tabs = win:FindFirstChild("ShopTabs")
	closePage()
	check("ShopTabs hidden again after closing", tabs and not tabs.Visible)
end

-- a refused PLAYTIME cell: the server's word (the cell shows it for 1.3 s since this revert)
function S.playrefuse(check)
	local Claim = RS:WaitForChild("Playtime"):WaitForChild("Claim")
	local ok, why = Claim:InvokeServer(12)
	check("slot 12 (pet, 60 min) refused on a fresh save", ok == false, tostring(ok))
	check("refusal word 'Not ready' -> cell shows NOT READY", why == "Not ready", tostring(why))
end

-- the old Settings page: a change saves (then Server settings_save_server.lua)
function S.settings(check)
	local page = openPage("Settings")
	check("Settings page open", page ~= nil and page.Visible)
	chrome(check, "Settings")
	local function data() local ok, d = pcall(HttpService.JSONDecode, HttpService, p:GetAttribute("Settings") or "") return ok and type(d) == "table" and d or {} end
	local night0 = data().night == true
	RS.Settings.Set:FireServer("night", not night0) -- what the TIME toggle sends
	check("server wrote night = " .. tostring(not night0), waitFor(function() return (data().night == true) == not night0 end, 3), p:GetAttribute("Settings"))
	task.wait(0.3)
	local lab = page:FindFirstChild("night") and page.night:FindFirstChild("Toggle", true)
	lab = lab and lab:FindFirstChild("Label", true)
	check("TIME toggle label follows", lab and lab.Text == ((not night0) and "NIGHT" or "DAY"), lab and lab.Text)
	task.wait(0.5)
	RS.Settings.Set:FireServer("musicVol", 0.6)
	check("server wrote musicVol 0.6", waitFor(function() return data().musicVol == 0.6 end, 3), p:GetAttribute("Settings"))
	closePage()
	return p:GetAttribute("Settings")
end

-- the old Index page: a real claim of area 1 (after the Server step "complete area 1")
function S.index(check)
	local page = openPage("Index")
	check("Index page open", page ~= nil and page.Visible)
	chrome(check, "Index")
	local m0, h0 = potions()
	local ok = RS.Index.Claim:InvokeServer(1) -- what the area CLAIM button sends (areaSel = 1)
	check("Index claim area 1 ok", ok == true, tostring(ok))
	check("Money potion +1", waitFor(function() return (p:GetAttribute("Potion_Money") or 0) == m0 + 1 end, 2), m0 .. " -> " .. tostring(p:GetAttribute("Potion_Money")))
	check("Hatch potion +1", (p:GetAttribute("Potion_Hatch") or 0) == h0 + 1, h0 .. " -> " .. tostring(p:GetAttribute("Potion_Hatch")))
	local again = RS.Index.Claim:InvokeServer(1)
	check("a second claim of area 1 is refused", again ~= true, tostring(again))
	closePage()
end

-- the old Starter Pack popup (after Server StarterDebug "reset"); BUY is never pressed (old popup: no dry run)
function S.starter(check)
	local g = pg.StarterPackUI
	if not g.Enabled then g.TestOpen:Fire() end
	check("popup opens", waitFor(function() return g.Enabled end, 2))
	task.wait(0.4)
	local w = g.Holder.Window
	check("old 540 x 430 window (x device scale)", g.Holder.Size == UDim2.fromOffset(540, 430))
	local ends = w:FindFirstChild("EndsIn", true)
	check("ENDS IN timer", ends and ends.Text:match("^ENDS IN %d") ~= nil, ends and ends.Text)
	check("BUY + NO THANKS + X exist", w:FindFirstChild("Buy", true) ~= nil and w:FindFirstChild("NoThanks", true) ~= nil and w:FindFirstChild("CloseButton", true) ~= nil)
	local ws = g.Holder.WindowScale
	local base = ws.Scale
	containAll(check, "Starter popup", w, w, function(k) ws.Scale = k and base * k or base end)
	g.Enabled = false
	-- the Shop's Starter Pack card (old StarterPackClient adds it)
	local page = openPage("Shop")
	local card = page and page:FindFirstChild("StarterPack", true)
	check("old Shop has its Starter Pack card", card ~= nil and card.Visible)
	closePage()
end

function S.freegift(check)
	local g = pg.FreeGiftUI
	local zone = workspace.Map.Hub.FreeGift.FreeGiftZone
	moveTo(zone.Position + Vector3.new(0, 3, 0))
	check("walk in opens Free Gift", waitFor(function() return g.Enabled end, 2))
	task.wait(0.4)
	check("hotbar hidden while open (fix)", hotbar() == false)
	local ws = g.Holder.WindowScale
	local base = ws.Scale
	containAll(check, "Free Gift", g.Holder.Window, g.Holder.Window, function(k) ws.Scale = k and base * k or base end)
	local m0, h0, s0 = potions()
	local folder = RS:FindFirstChild("FreeGift")
	local ok, res, why = pcall(folder.Claim.InvokeServer, folder.Claim) -- what CLAIM sends
	check("claim ok", ok and res == true, tostring(res) .. " " .. tostring(why))
	check("FreeGift true", waitFor(function() return p:GetAttribute("FreeGift") == true end, 3))
	task.wait(0.5)
	local m1, h1, s1 = potions()
	check("3 potions +1 each", m1 == m0 + 1 and h1 == h0 + 1 and s1 == s0 + 1, ("%d/%d/%d -> %d/%d/%d"):format(m0, h0, s0, m1, h1, s1))
	local ok2, res2, why2 = pcall(folder.Claim.InvokeServer, folder.Claim)
	check("second claim refused (claimed)", ok2 and res2 ~= true and why2 == "claimed", tostring(res2) .. " " .. tostring(why2))
	moveTo(AWAY)
	check("walk out closes", waitFor(function() return not g.Enabled end, 2))
	task.wait(0.3)
	check("hotbar back", hotbar() == true)
end

function S.welcome(check)
	local g = pg.OfflineUI
	check("pending -> Welcome Back opens", waitFor(function() return g.Enabled end, 4))
	task.wait(0.5)
	check("hotbar hidden while open (fix)", hotbar() == false)
	local amt = g.Holder.Window:FindFirstChild("Amount", true)
	check("amount $547K", amt and amt.Text == "$547K", amt and amt.Text)
	local w = g.Holder.Window
	local ws = g.Holder.WindowScale
	local base = ws.Scale
	for _, k in SCALES do
		ws.Scale = base * k
		task.wait(0.3)
		local r = _G.CUIContain(("Welcome x%.2f"):format(k), w, w, {apart = {{w.Price, w.ClaimX5}}})
		check(("containment Welcome x%.2f (price tag off the x5 button)"):format(k), r:match("fails 0$") ~= nil, r:sub(1, 400))
	end
	ws.Scale = base
	local m0 = p:GetAttribute("Money") or 0
	local ok, res, got = pcall(RS.Offline.Claim.InvokeServer, RS.Offline.Claim) -- what CLAIM / X send
	check("claim ok", ok and res == true, tostring(res))
	check("Money +547000", waitFor(function() return (p:GetAttribute("Money") or 0) >= m0 + 547000 end, 3), m0 .. " -> " .. tostring(p:GetAttribute("Money")))
	g.Enabled = false -- (the X / CLAIM press closes it; the remote alone doesn't)
	task.wait(0.4)
	check("hotbar back", hotbar() == true)
end

function S.welcomex5(check)
	local g = pg.OfflineUI
	check("pending -> opens", waitFor(function() return g.Enabled end, 4) or p:GetAttribute("OfflineLastX5") == true)
	check("x5 receipt granted (OfflineLastX5)", waitFor(function() return p:GetAttribute("OfflineLastX5") == true end, 6))
	g.Enabled = false
	task.wait(0.3)
	check("hotbar back", hotbar() == true)
end

function S.upgrades(check)
	local g = pg.UpgradeUI
	local zone = workspace.Map.Hub.Stalls:FindFirstChild("UpgradeZone", true)
	moveTo(zone.Position + Vector3.new(0, 3, 0))
	check("walk in opens Upgrades", waitFor(function() return g.Enabled end, 2))
	task.wait(0.4)
	check("hotbar hidden while open (fix)", hotbar() == false)
	containAll(check, "Upgrades", g.Root.Window, g.Root, function(k) _G.CUIScale(g.Root, k) end)
	local l0 = p:GetAttribute("GrabLevel") or 0
	local ok, r = RS.Upgrades.Buy:InvokeServer("Grab") -- what the Grab money button sends
	check("money buy Grab ok", ok == true, tostring(r))
	check("GrabLevel +1", waitFor(function() return (p:GetAttribute("GrabLevel") or 0) == l0 + 1 end, 2), l0 .. " -> " .. tostring(p:GetAttribute("GrabLevel")))
	task.wait(0.3)
	local row = g.Root.Window:FindFirstChild("Grab", true)
	check("Grab row shows the new level", row ~= nil)
	moveTo(AWAY)
	check("walk out closes", waitFor(function() return not g.Enabled end, 2))
	task.wait(0.3)
	check("hotbar back", hotbar() == true)
	return "GrabLevel " .. tostring(p:GetAttribute("GrabLevel"))
end

-- tutorial step 11 on the old Rebirth page. Server first: TutorialDone true, Rebirths 0, Money 25000, TutorialExtra 3.
local function chainVis(d) local x = d while x and x:IsA("GuiObject") do if not x.Visible then return false end x = x.Parent end return true end
local function tutText() -- what the tutorial shows right now (visible chain, rich text stripped)
	local t = {}
	for _, g in pg:GetChildren() do
		if g:IsA("ScreenGui") and g.Enabled and g.Name:find("Tutorial") then
			for _, d in g:GetDescendants() do
				if d:IsA("TextLabel") and chainVis(d) and d.ContentText ~= "" and d.TextTransparency < 1 then table.insert(t, d.ContentText) end
			end
		end
	end
	return table.concat(t, " | ")
end
_G.TutText = tutText
local function guideBottom() -- the tutorial guide's lowest visible piece (title / line / pips), MainMenu space
	local tu = pg:FindFirstChild("TutorialUI")
	local guide = tu and tu.Enabled and tu:FindFirstChild("Guide")
	if not (guide and guide.Visible) then return nil end
	local b
	for _, n in {"Title", "Sub", "Pips"} do
		local o = guide:FindFirstChild(n, true)
		if o and o:IsA("GuiObject") and chainVis(o) then b = math.max(b or 0, o.AbsolutePosition.Y + o.AbsoluteSize.Y) end
	end
	local inset = game:GetService("GuiService"):GetGuiInset().Y
	return b and (b + (tu.IgnoreGuiInset and 0 or inset) - (mm.IgnoreGuiInset and 0 or inset))
end
function S.step11a(check)
	check("stage 3", p:GetAttribute("TutorialExtra") == 3, p:GetAttribute("TutorialExtra"))
	check("REBIRTH is READY! shown", waitFor(function() return tutText():find("READY") ~= nil end, 4), tutText())
	local page = openPage("Rebirth")
	check("old Rebirth page open", page ~= nil and page.Visible)
	chrome(check, "Rebirth (step 11)")
	check("Press REBIRTH! shown", waitFor(function() return tutText():find("Press REBIRTH") ~= nil end, 3), tutText())
	local gb = guideBottom()
	check("window under the tutorial guide (no pips over the header)", gb ~= nil and win.AbsolutePosition.Y >= gb - 1, tostring(gb) .. " vs window top " .. win.AbsolutePosition.Y)
	local btn = page:FindFirstChild("RebirthButton", true)
	check("REBIRTH button inside the window", btn and inside(rect(btn), rect(face), 1), btn and f(rect(btn)))
	page.TestPress:Fire()
	check("Tap AGAIN to confirm!", waitFor(function() return tutText():find("AGAIN") ~= nil end, 3), tutText())
	return tutText()
end
function S.step11b(check)
	local page = body.RebirthPage
	local r0, pm0 = p:GetAttribute("Rebirths") or 0, p:GetAttribute("Potion_Money") or 0
	if not tutText():find("AGAIN") then -- (the confirm expires after a few seconds: arm it again)
		page.TestPress:Fire()
		waitFor(function() return tutText():find("AGAIN") ~= nil end, 2)
	end
	page.TestPress:Fire()
	check("rebirth done (Rebirths 1)", waitFor(function() return (p:GetAttribute("Rebirths") or 0) == r0 + 1 end, 4), tostring(p:GetAttribute("Rebirths")))
	check("TUTORIAL COMPLETE shown", waitFor(function() return tutText():find("TUTORIAL COMPLETE") ~= nil end, 4), tutText())
	check("stage 0", waitFor(function() return p:GetAttribute("TutorialExtra") == 0 end, 3), p:GetAttribute("TutorialExtra"))
	check("Money potion +1 (tutorial reward)", (p:GetAttribute("Potion_Money") or 0) == pm0 + 1, pm0 .. " -> " .. tostring(p:GetAttribute("Potion_Money")))
	check("window closed", waitFor(function() return not win.Visible end, 3))
	return tutText()
end

-- the old Shop's buy paths, dry run (Server stub armed first; ShopPage TestDryRun records the remote args)
function S.shopdry(check)
	local ShopConfig = require(RS.ShopConfig)
	local page = openPage("Shop")
	check("Shop open", page ~= nil and page.Visible)
	check("legacy ShopPage (ScrollingFrame) + ShopTabs", page:IsA("ScrollingFrame") and win.ShopTabs.Visible)
	page:SetAttribute("TestDryRun", true)
	check("TestDryRun on", page:GetAttribute("TestDryRun") == true)
	if page:GetAttribute("TestDryRun") ~= true then return end
	local cases = {}
	for _, ps in ShopConfig.Passes or {} do table.insert(cases, {"pass:" .. ps.key, {"pass", ps.key}}) end
	table.insert(cases, {"speed", {"speed"}})
	for _, pk in ShopConfig.PotionPacks or {} do table.insert(cases, {"potion:" .. pk.key, {"potion", pk.key}}) end
	table.insert(cases, {"treadmillMoney", {"treadmillMoney"}})
	table.insert(cases, {"treadmillRobux", {"treadmillRobux"}})
	check("cases: passes + potions found in ShopConfig", #cases >= 6, #cases)
	for _, c in cases do
		page:SetAttribute("TestLastBuy", nil)
		page:SetAttribute("TestPress", c[1])
		local ok = waitFor(function() return page:GetAttribute("TestLastBuy") ~= nil end, 1.5)
		local got = page:GetAttribute("TestLastBuy")
		check("press " .. c[1] .. " -> Shop.Buy" .. HttpService:JSONEncode(c[2]), ok and got == HttpService:JSONEncode(c[2]), got)
	end
	page:SetAttribute("TestDryRunResult", "Not enough money")
	page:SetAttribute("TestPress", "treadmillMoney")
	local function shows(txt) for _, d in page:GetDescendants() do if d:IsA("TextLabel") and d.Text == txt then return true end end return false end
	check("refusal 'Not enough money' -> NEED MORE $!", waitFor(function() return shows("NEED MORE $!") end, 1.5))
	page:SetAttribute("TestDryRunResult", "Max")
	page:SetAttribute("TestPress", "speed")
	check("refusal word kept (MAX)", waitFor(function() return shows("MAX") end, 1.5))
	page:SetAttribute("TestDryRunResult", nil)
	page:SetAttribute("TestDryRun", nil)
	page:SetAttribute("TestLastBuy", nil)
	page:SetAttribute("TestPress", "speed") -- refused without TestDryRun: nothing recorded, nothing sent
	task.wait(0.4)
	check("TestPress refused without TestDryRun", page:GetAttribute("TestLastBuy") == nil)
	closePage()
end

_G.RevertTests = function(section)
	local pass, fail, lines = 0, 0, {}
	local function check(name, cond, detail)
		if cond then pass += 1 else fail += 1 table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end
	end
	local fn = S[section]
	if not fn then return "no section " .. tostring(section) end
	local ok, res = pcall(fn, check)
	if not ok then fail += 1 table.insert(lines, "ERROR " .. tostring(res)) end
	return ("%s: %d pass / %d fail%s%s"):format(section, pass, fail, (ok and res) and (" (" .. tostring(res) .. ")") or "", #lines > 0 and ("\n" .. table.concat(lines, "\n")) or "")
end
return "RevertTests ready"
