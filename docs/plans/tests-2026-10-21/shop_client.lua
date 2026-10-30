-- shop_client.lua (2026-10-21, popup/Shop plan 7.3 + review MUST 1/2/3/5/7/8/9/10/11, SHOULD 3/7/25):
-- client checks for the HATCH NIGHT Shop (ShopClient). Client datamodel of a TestFreshSave Play session.
-- Paste once: it stores the runner in _G.ShopTests; then run sections: return _G.ShopTests("open")
-- Sections: open, layout, prices, override, buys, refusal, treadmoney, scroll, reopen, gift, toast, states, nosign,
-- analytics, legacy (own session with workspace TestShopLegacy = true, set in Edit before Play); fix round: pickerfit,
-- breaksection, canvasguard.
-- Server steps between sections (Server datamodel): the offer on = p:SetAttribute("Rebirths", 1);
-- ServerStorage.StarterDebug:Invoke("reset", p). Toasts: RS.Shop.Gifted:FireClient(p, "got", "VIP", name) /
-- RS.Shop.Granted:FireClient(p, "+1.2B SPEED!").
-- Never opens a real Robux prompt: every buy press runs with ShopPage.TestDryRun = true (the hooks refuse otherwise);
-- only TreadMoney (in-game money) is pressed for real, after asserting Money < the next tier's price (review MUST 9).
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local MarketplaceService = game:GetService("MarketplaceService")
local RS = game:GetService("ReplicatedStorage")
local player = Players.LocalPlayer
local pg = player:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local ShopConfig = require(RS.ShopConfig)
local SpeedBoostCards = require(RS.SpeedBoostCards)
local Boosts = require(RS.Boosts)
local H = require(RS.BrickUI).Hatch

local function report()
	local r = {pass = 0, fail = 0, lines = {}}
	function r.check(name, ok, detail)
		if ok then r.pass += 1 else r.fail += 1 end
		table.insert(r.lines, (ok and "ok   " or "FAIL ") .. name .. (detail ~= nil and (" [" .. tostring(detail) .. "]") or ""))
	end
	function r.note(s) table.insert(r.lines, "     " .. s) end
	function r.text(title) return ("%s: %d pass / %d fail\n%s"):format(title, r.pass, r.fail, table.concat(r.lines, "\n")) end
	return r
end
local function page() return body:FindFirstChild("ShopPage") end
local function list() return page().Scroll.List end
local function K() local sc = page().Scroll return sc.AbsoluteSize.Y / 386 end
local function scrollY() return page().Scroll.CanvasPosition.Y / K() end
local function pillTab()
	local y = page().Rail.Pill.Position.Y.Offset
	return ({[41] = "PASSES", [117] = "SPEED", [193] = "POTIONS", [269] = "TREADMILL", [345] = "EGGS"})[math.floor(y + 0.5)] or ("y" .. y)
end
local function waitFor(pred, timeout)
	local t0 = os.clock()
	while os.clock() - t0 < timeout do
		if pred() then return os.clock() - t0 end
		task.wait()
	end
	return pred() and (os.clock() - t0) or nil
end
local function openShop()
	if win.Visible then mm.CloseWindow:Fire() task.wait(0.4) end
	mm.OpenPage:Fire("Shop")
	task.wait(0.8)
end
local function closeShop() mm.CloseWindow:Fire() task.wait(0.4) end
local function decode(s) local ok, t = pcall(HttpService.JSONDecode, HttpService, s or "") return ok and t or nil end
local function same(a, b)
	if type(a) ~= "table" or type(b) ~= "table" or #a ~= #b then return false end
	for i = 1, #a do if a[i] ~= b[i] then return false end end
	return true
end
local function btnOf(cardName, btnName) return list():FindFirstChild(cardName, true).Face:FindFirstChild(btnName or "Buy") end
-- (fix round, visual review SHOULD 4) the treadmill money button shown: MoneyWide (no Robux skip / MAX) or Money
local function treadMoney() local f = list().Treadmill.Face return f.MoneyWide.Visible and f.MoneyWide or f.Money end
local function face(btn) return btn.Face end
local function priceOf(btn) local f = face(btn) return f.Price.Visible and f.Price.Text or nil, f.Word.Visible and f.Word.Text or nil end
local function gradTop(f) local g = f:FindFirstChildOfClass("UIGradient") return g and g.Color.Keypoints[1].Value end
local function isPal(btn, pal) return gradTop(face(btn)) == H.PAL[pal].top end
local PASS_KEYS = {}
for _, p in ShopConfig.Passes do table.insert(PASS_KEYS, p.key) end
local function setPasses(v) for _, k in PASS_KEYS do player:SetAttribute("Pass_" .. k, v) end end
local savedPasses
local function savePasses() savedPasses = {} for _, k in PASS_KEYS do savedPasses[k] = player:GetAttribute("Pass_" .. k) end end
local function restorePasses() if savedPasses then for k, v in savedPasses do player:SetAttribute("Pass_" .. k, v) end end end

local S = {}

-- 1 open (B1, MUST 1 / 10.4)
function S.open()
	local r = report()
	openShop()
	local pgp = page()
	r.check("HatchBack / HatchFront shown", win.HatchBack.Visible and win.HatchFront.Visible)
	r.check("title SHOP", win.HatchFront.Title.Text == "SHOP", win.HatchFront.Title.Text)
	r.check("magenta tooth (220,0,100)", win.HatchFront.Crack.Tooth1.BackgroundColor3 == Color3.fromRGB(220, 0, 100), tostring(win.HatchFront.Crack.Tooth1.BackgroundColor3))
	r.check("bats hidden", not win.HatchFront.Bats.Visible)
	local ar = win.AbsoluteSize.X / win.AbsoluteSize.Y
	r.check("window AR 740/470", math.abs(ar - 740 / 470) <= 0.01, ("%.4f"):format(ar))
	r.check("CanvasScale == SkinScale", math.abs(pgp.CanvasScale.Scale - win.HatchBack.SkinScale.Scale) <= 0.001, ("%.4f %.4f"):format(pgp.CanvasScale.Scale, win.HatchBack.SkinScale.Scale))
	r.check("no Window.ShopTabs", win:FindFirstChild("ShopTabs") == nil)
	r.check("no Body.GiftPicker", body:FindFirstChild("GiftPicker") == nil)
	local hits = 0
	for i = 1, 5 do if pgp.Rail:FindFirstChild("Hit" .. i) and pgp.Rail["Hit" .. i]:IsA("TextButton") then hits += 1 end end
	r.check("rail: 5 hits", hits == 5, hits)
	r.check("pill on FEATURED", pillTab() == "PASSES", pillTab())
	-- MUST 1: as big as the old Check-UI Shop (0.8148 of the gui height) on PC: s = min(pageCap, height fit) unless the
	-- width (left HUD clearance) limits it
	local gs = mm.AbsoluteSize
	local cap = H.pageCap("Shop", gs.Y)
	local want = math.min(cap, (gs.Y - 12) / 470)
	local got = win.AbsoluteSize.X / 740
	local widthLimited = (gs.X - 8 - 230) / 740 < want
	r.check("MUST 1: Shop scale = pageCap fit", math.abs(got - want) <= 0.005 or (widthLimited and got < want), ("s %.4f want %.4f cap %.4f, window H / gui H %.4f%s"):format(got, want, cap, win.AbsoluteSize.Y / gs.Y, widthLimited and " (width-limited)" or ""))
	r.check("MUST 1: bigger than the standard 1.18 fit (or equal)", got >= math.min(1.18, (gs.Y - 12) / 470, (gs.X - 8 - 230) / 740) - 0.005, ("%.4f"):format(got))
	-- MUST 10.4
	local legacy = player.PlayerScripts:FindFirstChild("ShopClientLegacy")
	r.check("ShopClientLegacy disabled", legacy ~= nil and legacy.Enabled == false)
	local nPage, nToast = 0, 0
	for _, c in body:GetChildren() do if c.Name == "ShopPage" then nPage += 1 end end
	for _, c in pg:GetChildren() do if c.Name == "GiftToast" then nToast += 1 end end
	r.check("one ShopPage, one GiftToast", nPage == 1 and nToast == 1, nPage .. " / " .. nToast)
	r.check("ShopLoop on", pgp:GetAttribute("ShopLoop") == true)
	return r.text("open")
end

-- 2 layout (4.3): the y table for the current slot state (shown / hidden)
function S.layout()
	local r = report()
	if not win.Visible then openShop() end
	local shown = list().StarterSlot.Visible
	local off = shown and 0 or 142
	local want = {Header_PASSES = 142, Pass_Growth2x = 178, Pass_VIP = 336, Header_SPEED = 504, Double = 540, Boost_Speed15m = 672,
		Header_POTIONS = 866, Pack_Money3 = 902, Pack_Money10 = 1086, Header_TREADMILL = 1280, Treadmill = 1316, Header_EGGS = 1458, Eggs = 1494}
	for name, y in want do
		local o = list():FindFirstChild(name)
		local got = o and (o.Position.Y.Offset - 4)
		r.check(("%s y %d"):format(name, y - off), got == y - off, got)
	end
	local ch = page().Scroll.CanvasSize.Y.Offset
	r.check("CanvasH " .. (shown and 1634 or 1492), ch == (shown and 1634 or 1492), ch)
	r.check("List width 584 <= window " .. page().Scroll.AbsoluteWindowSize.X / K(), list().AbsoluteSize.X <= page().Scroll.AbsoluteWindowSize.X + 1)
	r.note("slot shown: " .. tostring(shown))
	return r.text("layout")
end

-- 3 prices (B4, MUST 3): every price text = the live GetProductInfo price with the RIGHT InfoType (Studio: ids are real)
function S.prices()
	local r = report()
	savePasses()
	setPasses(false)
	openShop()
	task.wait(1.5) -- (the live price fetch)
	local function live(id, infoType, fallback)
		local ok, info = pcall(MarketplaceService.GetProductInfo, MarketplaceService, id, infoType)
		return ok and info and info.PriceInRobux and tostring(info.PriceInRobux) or tostring(fallback)
	end
	for _, p in ShopConfig.Passes do
		local pr = priceOf(btnOf("Pass_" .. p.key))
		r.check("pass " .. p.key .. " (GamePass)", pr == live(p.id, Enum.InfoType.GamePass, p.price), tostring(pr) .. " vs " .. live(p.id, Enum.InfoType.GamePass, p.price))
	end
	local step = ShopConfig.doubleSpeedStep(player:GetAttribute("SpeedBoosts") or 0)
	r.check("Double step (Product)", priceOf(btnOf("Double")) == live(step.id, Enum.InfoType.Product, step.price), tostring(priceOf(btnOf("Double"))))
	local boostLive
	for _, key in {"Speed15m", "Speed3", "Speed2h"} do
		local c = SpeedBoostCards.CARDS[key]
		local lv = live(c.id, Enum.InfoType.Product, c.price)
		boostLive = boostLive or lv
		r.check("boost " .. key .. " (Product)", priceOf(btnOf("Boost_" .. key)) == lv, tostring(priceOf(btnOf("Boost_" .. key))) .. " vs " .. lv)
	end
	for _, pk in ShopConfig.PotionPacks do
		r.check("pack " .. pk.key .. " (Product)", priceOf(btnOf("Pack_" .. pk.key)) == live(pk.id, Enum.InfoType.Product, pk.price), tostring(priceOf(btnOf("Pack_" .. pk.key))))
	end
	local tier = player:GetAttribute("TreadmillTier") or 1
	local tid = ShopConfig.TreadmillProducts[tier + 1]
	if tid and btnOf("Treadmill", "Robux").Visible then
		local tp = priceOf(btnOf("Treadmill", "Robux"))
		r.check("treadmill Robux (Product)", tp == live(tid, Enum.InfoType.Product, ShopConfig.TreadmillRobux[tier + 1]), tostring(tp))
	else
		r.note("treadmill Robux hidden at tier " .. tier)
	end
	local gp = priceOf(btnOf("Eggs"))
	local gl = live(ShopConfig.GrowAllProduct, Enum.InfoType.Product, ShopConfig.GrowAllPrice)
	r.check("Grow All (Product)", gp == gl, tostring(gp) .. " vs " .. gl)
	-- the review's point: the Asset lookup (no InfoType) would differ for a developer product
	local okA, infoA = pcall(MarketplaceService.GetProductInfo, MarketplaceService, ShopConfig.GrowAllProduct)
	r.note(("Grow All with NO InfoType (Asset): %s"):format(okA and tostring(infoA and infoA.PriceInRobux) or ("error " .. tostring(infoA))))
	-- B25: boost titles = CARDS[key].title() live; Double = Boosts.speed(player) / (player, 1)
	local t15 = list().Boost_Speed15m.Face.Title.Text
	r.check("B25 boost title = CARDS.Speed15m.title()", t15 == SpeedBoostCards.CARDS.Speed15m.title(), t15)
	-- (fix round, visual review MUST 1) the pack titles = the potion name, upper-cased
	for _, pk in ShopConfig.PotionPacks do
		local t = list()["Pack_" .. pk.key].Face.Title.Text
		r.check("pack " .. pk.key .. " title = upper(potion)", t == string.upper(pk.potion), t)
	end
	local nowT, nextT = list().Double.Face.Now.Text, list().Double.Face.Next.Text
	r.note("Double now/next: " .. nowT .. " > " .. nextT .. " | Boosts.speed " .. tostring(Boosts.speed(player)) .. " / " .. tostring(Boosts.speed(player, 1)))
	restorePasses()
	return r.text("prices")
end

-- 3b override (B4): TestPriceOverride "1499" re-centres every group (the containment priceGroup check does the rest)
function S.override()
	local r = report()
	savePasses()
	setPasses(false)
	openShop()
	page():SetAttribute("TestPriceOverride", "1499")
	task.wait(0.5)
	local n, ok = 0, 0
	local s = page().CanvasScale.Scale
	-- (fix round) only prices really on screen (every ancestor shown: the treadmill's 112 buttons hide at tier 1 behind
	-- MoneyWide) and only the Shop's own (the Starter card's BUY is StarterPackClient's live price, no override)
	local function onScreen(o) local x = o while x and x ~= list() do if x:IsA("GuiObject") and not x.Visible then return false end x = x.Parent end return true end
	for _, d in list():GetDescendants() do
		if d.Name == "Price" and d:IsA("TextLabel") and onScreen(d) and d.Parent.Name == "Face" and not d:IsDescendantOf(list().StarterSlot) then
			n += 1
			local f = d.Parent
			-- the price box = its text width + 6 (stroke room); the group keeps >= 8 px each side -> the box ends >= 4 px in
			local right = d.AbsolutePosition.X + d.AbsoluteSize.X
			local fr = f.AbsolutePosition.X + f.AbsoluteSize.X
			if d.Text == "1499" and d.TextFits and right <= fr - 4 * s + 1 then ok += 1 else r.note((d:GetFullName():gsub("^.-List%.", "")) .. (" right %.1f face %.1f fits %s"):format(right, fr, tostring(d.TextFits))) end
		end
	end
	r.check("every gold price shows 1499, fits, ends >= 4 px inside its face", n > 0 and ok == n, ok .. "/" .. n)
	_G.OVERRIDE_CONTAIN = _G.HatchContain and _G.HatchContain("S5 override 1499", _G.HatchShopCfg()) or "(containment not loaded)"
	page():SetAttribute("TestPriceOverride", nil)
	task.wait(0.3)
	restorePasses()
	return r.text("override") .. "\n" .. _G.OVERRIDE_CONTAIN
end

-- 4 every buy path, dry run (B2, MUST 11)
function S.buys()
	local r = report()
	savePasses()
	setPasses(false)
	openShop()
	local pgp = page()
	-- MUST 11: without TestDryRun a Robux key is refused (TestLastBuy unchanged)
	pgp:SetAttribute("TestDryRun", nil)
	pgp:SetAttribute("TestLastBuy", "none")
	pgp.TestPress:Fire("Pack_Money3")
	task.wait(0.2)
	r.check("MUST 11: no dry run -> refused", pgp:GetAttribute("TestLastBuy") == "none", pgp:GetAttribute("TestLastBuy"))
	pgp:SetAttribute("TestDryRun", true)
	pgp:SetAttribute("TestDryRunResult", nil)
	local cases = {}
	for _, k in PASS_KEYS do table.insert(cases, {"Pass_" .. k, {"pass", k}}) end
	table.insert(cases, {"Double", {"speed"}})
	table.insert(cases, {"Boost_Speed15m", {"speedPack", "Speed15m"}})
	table.insert(cases, {"Boost_Speed3", {"potion", "Speed3"}})
	table.insert(cases, {"Boost_Speed2h", {"speedPack", "Speed2h"}})
	for _, pk in ShopConfig.PotionPacks do table.insert(cases, {"Pack_" .. pk.key, {"potion", pk.key}}) end
	table.insert(cases, {"TreadMoney", {"treadmillMoney"}})
	table.insert(cases, {"TreadRobux", {"treadmillRobux"}})
	table.insert(cases, {"Eggs", {"SkipEgg", "all"}})
	for _, c in cases do
		pgp:SetAttribute("TestLastBuy", "none")
		pgp.TestPress:Fire(c[1])
		task.wait(0.1)
		local got = decode(pgp:GetAttribute("TestLastBuy"))
		r.check(c[1] .. " -> " .. HttpService:JSONEncode(c[2]), same(got, c[2]), pgp:GetAttribute("TestLastBuy"))
	end
	-- owned: a pass press does nothing (silver, not Active)
	player:SetAttribute("Pass_VIP", true)
	task.wait(0.5)
	pgp:SetAttribute("TestLastBuy", "none")
	pgp.TestPress:Fire("Pass_VIP")
	task.wait(0.1)
	r.check("owned VIP press: nothing sent", pgp:GetAttribute("TestLastBuy") == "none")
	pgp:SetAttribute("TestDryRun", nil)
	pgp:SetAttribute("TestLastBuy", nil)
	restorePasses()
	return r.text("buys")
end

-- 4b refusal words (B3, MUST 5)
function S.refusal()
	local r = report()
	openShop()
	local pgp = page()
	pgp:SetAttribute("TestDryRun", true)
	pgp:SetAttribute("TestDryRunResult", "Not enough money")
	local b = btnOf("Pack_Money3")
	pgp.TestPress:Fire("Pack_Money3")
	task.wait(0.15)
	local p0, w0 = priceOf(b)
	r.check("NEED MORE $! red", w0 == "NEED MORE $!" and isPal(b, "red"), tostring(w0))
	task.wait(1.45)
	local p1, w1 = priceOf(b)
	r.check("back to the gold price after 1.3 s", p1 ~= nil and w1 == nil and isPal(b, "gold"), tostring(p1) .. " / " .. tostring(w1))
	-- the treadmill money button shown (MoneyWide 160 at tier 1, Money 112 otherwise) takes a NEED variant that fits
	pgp.TestPress:Fire("TreadMoney")
	task.wait(0.15)
	local tm = treadMoney()
	local _, wt = priceOf(tm)
	r.check("treadmill money (" .. tm.Name .. "): a NEED word that fits", (wt == "NEED $!" or wt == "NEED MORE $!") and tm.Face.Word.TextFits, tostring(wt))
	task.wait(1.45)
	local _, wt2 = priceOf(tm)
	r.check("treadmill money back to lime $ after 1.3 s", wt2 ~= nil and wt2:sub(1, 1) == "$" and isPal(tm, "lime"), tostring(wt2))
	-- another reason: upper-cased
	pgp:SetAttribute("TestDryRunResult", "Owned")
	pgp.TestPress:Fire("Pack_Hatch3")
	task.wait(0.15)
	local _, w2 = priceOf(btnOf("Pack_Hatch3"))
	r.check("other reason upper-cased", w2 == "OWNED", tostring(w2))
	task.wait(1.45)
	-- "prompted" -> no word change
	pgp:SetAttribute("TestDryRunResult", "prompted")
	pgp.TestPress:Fire("Pack_Speed3")
	task.wait(0.15)
	local p3, w3 = priceOf(btnOf("Pack_Speed3"))
	r.check("prompted -> no word", p3 ~= nil and w3 == nil, tostring(w3))
	-- the Eggs failure flashes the reason
	pgp:SetAttribute("TestDryRunResult", "No eggs to hatch")
	pgp.TestPress:Fire("Eggs")
	task.wait(0.15)
	local _, w4 = priceOf(btnOf("Eggs"))
	r.check("Eggs refusal word", w4 == "NO EGGS TO HATCH" or w4 == "TRY AGAIN", tostring(w4))
	pgp:SetAttribute("TestDryRunResult", nil)
	pgp:SetAttribute("TestDryRun", nil)
	task.wait(1.4)
	return r.text("refusal")
end

-- 4c the REAL treadmill money press on a $0 save (in-game money, no prompt; MUST 9: only while Money < the price)
function S.treadmoney()
	local r = report()
	openShop()
	local tier = player:GetAttribute("TreadmillTier") or 1
	local cost = ShopConfig.TreadmillMoney[tier + 1]
	local money = player:GetAttribute("Money") or 0
	if not cost or money >= cost then
		r.check("MUST 9 guard: Money < next tier price", false, ("money %s cost %s: NOT pressed"):format(tostring(money), tostring(cost)))
		return r.text("treadmoney")
	end
	r.check("MUST 9 guard: Money < next tier price", true, ("%s < %s"):format(tostring(money), tostring(cost)))
	page():SetAttribute("TestDryRun", nil)
	page().TestPress:Fire("TreadMoney")
	local tm = treadMoney()
	local t = waitFor(function() local _, w = priceOf(tm) return w == "NEED $!" or w == "NEED MORE $!" end, 3)
	r.check("server reply: NEED $! (no prompt)", t ~= nil, t and ("%.2f s"):format(t))
	r.check("tier unchanged", (player:GetAttribute("TreadmillTier") or 1) == tier)
	task.wait(1.4)
	return r.text("treadmoney")
end

-- 5 scroll + tabs (B7, B8, MUST 8)
function S.scroll()
	local r = report()
	openShop()
	local shown = list().StarterSlot.Visible
	local off = shown and 0 or 142
	local pgp = page()
	pgp.TestPress:Fire("Tab_POTIONS")
	local t = waitFor(function() return math.abs(scrollY() - (866 - off)) <= 1 end, 0.6)
	r.check("Tab_POTIONS -> y " .. (866 - off) .. " within 0.6 s", t ~= nil, ("%.1f"):format(scrollY()))
	task.wait(0.1)
	r.check("pill POTIONS", pillTab() == "POTIONS", pillTab())
	pgp.TestPress:Fire("Tab_TREADMILL")
	task.wait(0.6)
	local maxS = pgp.Scroll.CanvasSize.Y.Offset - 386
	r.check("MUST 8: Tab_TREADMILL -> pill TREADMILL (clamped scroll)", pillTab() == "TREADMILL", pillTab() .. (" y %.1f max %d"):format(scrollY(), maxS))
	pgp.TestPress:Fire("Tab_EGGS")
	task.wait(0.6)
	r.check("Tab_EGGS -> max scroll", math.abs(scrollY() - maxS) <= 1, ("%.1f / %d"):format(scrollY(), maxS))
	r.check("pill EGGS", pillTab() == "EGGS", pillTab())
	-- a manual scroll away: the scroll rule again
	pgp.Scroll.CanvasPosition = Vector2.new(0, (504 - off + 10) * K())
	task.wait(0.2)
	r.check("manual scroll -> SPEED", pillTab() == "SPEED", pillTab())
	pgp.TestPress:Fire("Tab_FEATURED")
	task.wait(0.6)
	r.check("Tab_FEATURED -> top", scrollY() <= 1 and pillTab() == "PASSES", ("%.1f %s"):format(scrollY(), pillTab()))
	-- PetsEggsUI GET MORE: OpenPage + ScrollTo
	closeShop()
	mm.OpenPage:Fire("Shop")
	pgp:SetAttribute("ScrollTo", "POTIONS")
	local t2 = waitFor(function() return math.abs(scrollY() - (866 - off)) <= 1 end, 0.9)
	r.check("ScrollTo POTIONS within 0.9 s", t2 ~= nil, ("%.1f"):format(scrollY()))
	r.check("ScrollTo cleared", pgp:GetAttribute("ScrollTo") == nil)
	task.wait(0.2)
	r.check("ScrollTo -> pill POTIONS", pillTab() == "POTIONS", pillTab())
	closeShop()
	openShop()
	r.check("reopen -> top, FEATURED", scrollY() <= 1 and pillTab() == "PASSES", ("%.1f %s"):format(scrollY(), pillTab()))
	return r.text("scroll")
end

-- 5b MUST 2 / B21: X then reopen restarts everything
function S.reopen()
	local r = report()
	savePasses()
	setPasses(false)
	openShop()
	local pgp = page()
	pgp.TestPress:Fire("Tab_EGGS")
	task.wait(0.6)
	mm.CloseWindow:Fire()
	task.wait(0.5)
	r.check("closed: ShopLoop off", pgp:GetAttribute("ShopLoop") == false)
	mm.OpenPage:Fire("Shop")
	task.wait(0.6)
	r.check("reopen: ShopLoop on", pgp:GetAttribute("ShopLoop") == true)
	r.check("reopen: top + FEATURED", scrollY() <= 1 and pillTab() == "PASSES", ("%.1f %s"):format(scrollY(), pillTab()))
	player:SetAttribute("Pass_VIP", true)
	local t = waitFor(function() local _, w = priceOf(btnOf("Pass_VIP")) return w == "OWNED" end, 0.6)
	r.check("Pass_VIP toggle -> OWNED within 0.6 s", t ~= nil, t and ("%.2f s"):format(t))
	restorePasses()
	return r.text("reopen")
end

-- 6 gift picker (B6, MUST 6/7)
function S.gift()
	local r = report()
	savePasses()
	setPasses(false)
	workspace:SetAttribute("TestGiftSelf", true)
	openShop()
	local pgp = page()
	pgp.TestPress:Fire("Gift_VIP")
	task.wait(0.5)
	local pk = pgp.GiftPicker
	r.check("picker visible", pk.Visible)
	r.check("title GIFT VIP", pk.Box.Face.Title.Text == "GIFT VIP", pk.Box.Face.Title.Text)
	local row = pk.Box.Face.Players:FindFirstChild("P" .. player.UserId)
	r.check("own row (TestGiftSelf)", row ~= nil)
	r.check("PickerConns 1", pgp:GetAttribute("PickerConns") == 1, pgp:GetAttribute("PickerConns"))
	-- MUST 11: no dry run -> the row press is refused
	pgp:SetAttribute("TestLastBuy", "none")
	pgp.TestGiftRow:Fire(player.UserId)
	task.wait(0.1)
	r.check("MUST 11: TestGiftRow refused without dry run", pgp:GetAttribute("TestLastBuy") == "none")
	pgp:SetAttribute("TestDryRun", true)
	pgp.TestGiftRow:Fire(player.UserId)
	task.wait(0.1)
	r.check("gift row -> [gift, VIP, userId]", same(decode(pgp:GetAttribute("TestLastBuy")), {"gift", "VIP", player.UserId}), pgp:GetAttribute("TestLastBuy"))
	local picker1 = _G.HatchContain and _G.HatchContain("S6 picker 1 row", _G.HatchShopCfg()) or ""
	-- the owned target shows OWNED (silver)
	player:SetAttribute("Pass_VIP", true)
	task.wait(0.3)
	local row2 = pk.Box.Face.Players:FindFirstChild("P" .. player.UserId)
	r.check("owned target -> OWNED silver", row2 and row2.Gift.Face.Word.Visible and row2.Gift.Face.Word.Text == "OWNED", row2 and row2.Gift.Face.Word.Text)
	player:SetAttribute("Pass_VIP", false)
	task.wait(0.3)
	-- MUST 7: 20-character names stay in their boxes (8 fake rows)
	local b0 = pgp:GetAttribute("HatchButtons")
	pgp:SetAttribute("TestPickerRows", 8)
	task.wait(0.3)
	local nf, okf = 0, 0
	for _, rw in pk.Box.Face.Players:GetChildren() do
		if rw.Name:match("^Fake") then
			nf += 1
			local nmT, unT = rw:FindFirstChild("Name"), rw:FindFirstChild("User")
			local giftL = rw.Gift.AbsolutePosition.X
			local function endX(t) return t.AbsolutePosition.X + math.min(t.TextBounds.X, t.AbsoluteSize.X) end
			if nmT.TextTruncate == Enum.TextTruncate.AtEnd and unT.TextTruncate == Enum.TextTruncate.AtEnd and endX(nmT) <= giftL and endX(unT) <= giftL then okf += 1 end
		end
	end
	r.check("MUST 7: 8 fake 20-char rows, names truncated before the button", nf == 8 and okf == 8, okf .. "/" .. nf)
	_G.PICKER_CONTAIN = _G.HatchContain and _G.HatchContain("S6 picker + 8 fake rows", _G.HatchShopCfg()) or ""
	pgp:SetAttribute("TestPickerRows", nil)
	task.wait(0.3)
	-- MUST 6: rebuilding rows does not grow H.buttons
	for i = 1, 5 do pgp:SetAttribute("TestPickerRows", 8) task.wait(0.1) pgp:SetAttribute("TestPickerRows", nil) task.wait(0.1) end
	task.wait(0.2)
	local b1 = pgp:GetAttribute("HatchButtons")
	r.check("MUST 6: HatchButtons flat after 10 rebuilds", b1 == b0, tostring(b0) .. " -> " .. tostring(b1))
	-- close the Shop -> picker hidden, no connections
	closeShop()
	r.check("Shop closed -> picker hidden", not pk.Visible)
	r.check("PickerConns 0", pgp:GetAttribute("PickerConns") == 0, pgp:GetAttribute("PickerConns"))
	pgp:SetAttribute("TestDryRun", nil)
	pgp:SetAttribute("TestLastBuy", nil)
	workspace:SetAttribute("TestGiftSelf", nil)
	restorePasses()
	return r.text("gift") .. "\n" .. picker1 .. "\n" .. _G.PICKER_CONTAIN
end

-- 6b toasts (B6 / B10, MUST 7): call after the server fired Gifted ("got", "VIP", <name>) or Granted
function S.toast(kind, expect)
	local r = report()
	local tg = pg:FindFirstChild("GiftToast")
	local lab = tg and tg:FindFirstChild(kind == "granted" and "Granted" or "Toast")
	r.check("toast visible", lab and lab.Visible)
	r.check("text", lab and (expect == nil or lab.Text == expect), lab and lab.Text)
	r.check("fits (no scaling, >= 18)", lab and lab.TextFits and lab.TextSize >= 18 and not lab.TextScaled, lab and lab.TextSize)
	local tw = lab and H.textWidth(lab.Text, lab.TextSize)
	r.check("width inside the 600 box", lab and tw <= 600 - 6, tw)
	-- (fix round) the 83 % rule on the toast line
	local st = lab and lab:FindFirstChildOfClass("UIStroke")
	local fill = lab and tw / (lab.Size.X.Offset - 2 * (st and st.Thickness or 0))
	r.check("toast fills <= 83 % of its box", lab and fill <= 0.835, fill and ("%.0f%%"):format(fill * 100))
	r.check("WindowScale = the 1.18-capped fit", lab and math.abs(lab.WindowScale.Scale - (H.fitWindow(mm.AbsoluteSize.X, mm.AbsoluteSize.Y, 0))) <= 0.01 or kind == "granted", lab and lab.WindowScale.Scale)
	return r.text("toast " .. tostring(kind))
end

-- 7 states (B5)
function S.states()
	local r = report()
	savePasses()
	local sb, tt = player:GetAttribute("SpeedBoosts"), player:GetAttribute("TreadmillTier")
	openShop()
	player:SetAttribute("Pass_VIP", true)
	task.wait(0.5)
	local vb = btnOf("Pass_VIP")
	local _, w = priceOf(vb)
	r.check("VIP OWNED silver, not Active", w == "OWNED" and isPal(vb, "silver") and vb.Face.Active == false, tostring(w))
	player:SetAttribute("SpeedBoosts", ShopConfig.MaxSpeedBoosts)
	task.wait(0.5)
	local db = btnOf("Double")
	local _, wd = priceOf(db)
	r.check("Double MAX silver", wd == "MAX" and isPal(db, "silver"), tostring(wd))
	r.check("Double now 'x.. MAX', no arrow", list().Double.Face.Now.Text:find("MAX") ~= nil and not list().Double.Face.Arrow.Visible, list().Double.Face.Now.Text)
	player:SetAttribute("TreadmillTier", 1)
	task.wait(0.5)
	local tf = list().Treadmill.Face
	-- (fix round, visual review SHOULD 4 + 5) tier 1 (no Robux skip): ONE wide lime money button in the 404..564 slot
	local function wideOk() local w = tf.MoneyWide return w.Size.X.Offset == 160 and w.Position.X.Offset == 484 end
	local _, w1 = priceOf(tf.MoneyWide)
	r.check("tier 1: MoneyWide (160 at 404) lime $, Money + Robux hidden", tf.MoneyWide.Visible and wideOk() and not tf.Money.Visible and not tf.Robux.Visible
		and w1 ~= nil and w1:sub(1, 1) == "$" and isPal(tf.MoneyWide, "lime") and tf.MoneyWide.Face.Active == true, tostring(w1) .. " " .. tostring(tf.MoneyWide.Position))
	player:SetAttribute("TreadmillTier", 2)
	task.wait(0.5)
	r.check("tier 2: both 112 buttons, Money at 326 (centre 382), no MoneyWide", tf.Robux.Visible and tf.Money.Visible and not tf.MoneyWide.Visible and tf.Money.Position.X.Offset == 382, tostring(tf.Money.Position))
	player:SetAttribute("TreadmillTier", 11)
	task.wait(0.5)
	local _, w11 = priceOf(tf.MoneyWide)
	r.check("tier 11: one silver MAX pill (MoneyWide), not Active; MaxText hidden; Now keeps xN MAX", tf.MoneyWide.Visible and w11 == "MAX" and isPal(tf.MoneyWide, "silver")
		and tf.MoneyWide.Face.Active == false and not tf.MaxText.Visible and not tf.Money.Visible and not tf.Robux.Visible and tf.Now.Text:find("MAX") ~= nil, tostring(w11) .. " / " .. tf.Now.Text)
	-- a press at MAX does nothing (blocked)
	page():SetAttribute("TestDryRun", true)
	page():SetAttribute("TestLastBuy", "none")
	page().TestPress:Fire("TreadMoney")
	task.wait(0.2)
	r.check("tier 11: TreadMoney press blocked (no buy args)", page():GetAttribute("TestLastBuy") == "none", page():GetAttribute("TestLastBuy"))
	page():SetAttribute("TestDryRun", nil)
	page():SetAttribute("TestLastBuy", nil)
	player:SetAttribute("SpeedBoosts", sb)
	player:SetAttribute("TreadmillTier", tt)
	restorePasses()
	task.wait(0.4)
	return r.text("states") -- (the S3 containment runs from the matrix: Pass_* + SpeedBoosts 10 + TreadmillTier 11)
end

-- B26 / review SHOULD 3: no treadmill sign -> "x1 > ?", refresh keeps running
function S.nosign()
	local r = report()
	openShop()
	local id = player:GetAttribute("BaseId")
	player:SetAttribute("BaseId", -999)
	task.wait(0.6)
	local f = list().Treadmill.Face
	r.check("no sign -> x1 > ?", f.Now.Text == "x1" and f.Next.Text == "?", f.Now.Text .. " > " .. f.Next.Text)
	local n0 = tonumber((page():GetAttribute("HatchPerfShop") or "0"):match("^(%d+)"))
	task.wait(0.7)
	local n1 = tonumber((page():GetAttribute("HatchPerfShop") or "0"):match("^(%d+)"))
	r.check("refresh still runs", n1 > n0, n0 .. " -> " .. n1)
	player:SetAttribute("BaseId", id)
	task.wait(0.4)
	return r.text("nosign")
end

-- 9 analytics (B9): one fire per change, alternating; Rebirth after the Shop = exactly one false
function S.analytics()
	local r = report()
	if win.Visible then mm.CloseWindow:Fire() task.wait(0.5) end
	local function sent() local v = page():GetAttribute("ShopFunnelSent") or "0:false" local n, b = v:match("^(%d+):(%a+)$") return tonumber(n), b end
	local n0 = sent()
	local seq = {}
	for _ = 1, 3 do
		mm.OpenPage:Fire("Shop") task.wait(0.5)
		table.insert(seq, select(2, sent()))
		mm.CloseWindow:Fire() task.wait(0.5)
		table.insert(seq, select(2, sent()))
	end
	local n1 = sent()
	r.check("3 open / close -> +6", n1 - n0 == 6, n0 .. " -> " .. n1)
	r.check("alternating true/false", table.concat(seq, ",") == "true,false,true,false,true,false", table.concat(seq, ","))
	mm.OpenPage:Fire("Shop") task.wait(0.5)
	local n2 = sent()
	mm.OpenPage:Fire("Rebirth") task.wait(0.6)
	local n3, b3 = sent()
	r.check("Rebirth after the Shop: exactly one false", n3 - n2 == 1 and b3 == "false", (n3 - n2) .. " " .. tostring(b3))
	mm.CloseWindow:Fire() task.wait(0.5)
	local n4 = sent()
	r.check("closing Rebirth: no Shop fire", n4 == n3, n3 .. " -> " .. n4)
	return r.text("analytics")
end

-- 10 legacy (MUST 10.3): its own session, Edit workspace TestShopLegacy = true before Play
function S.legacy()
	local r = report()
	local legacy = player.PlayerScripts:FindFirstChild("ShopClientLegacy")
	r.check("ShopClientLegacy enabled", legacy and legacy.Enabled == true)
	local nPage, nToast = 0, 0
	for _, c in body:GetChildren() do if c.Name == "ShopPage" then nPage += 1 end end
	for _, c in pg:GetChildren() do if c.Name == "GiftToast" then nToast += 1 end end
	r.check("exactly one ShopPage + one GiftToast", nPage == 1 and nToast == 1, nPage .. " / " .. nToast)
	r.check("the ShopPage is the legacy ScrollingFrame", page() and page():IsA("ScrollingFrame"))
	openShop()
	r.check("Check-UI chrome (no night shell)", not win.HatchBack.Visible and win:FindFirstChild("ShopTabs") ~= nil and win.ShopTabs.Visible, tostring(win.HatchBack.Visible))
	-- (the test runs in its own Lua VM: its require(BrickUI) is a different table, so PAGE_SKIN.Shop is checked through
	-- its effect, the Check-UI chrome below)
	local p0 = page().CanvasPosition.Y
	page():SetAttribute("ScrollTo", "POTIONS")
	task.wait(0.9)
	r.check("a tab scroll works (ScrollTo POTIONS)", page().CanvasPosition.Y > p0 + 10, ("%.1f -> %.1f"):format(p0, page().CanvasPosition.Y))
	local sp = pg.StarterPackUI
	r.check("no Starter card in the legacy Shop (no slot)", page():FindFirstChild("StarterSlot", true) == nil)
	closeShop()
	return r.text("legacy")
end

-- 11 (fix round, visual review MUST 2) the gift picker fits its rows: box 79 + min(307, 8 + 68 n), centred in the page
-- body (y 66..452), the empty-state lines at y 80 / 104. Cases (TestGiftSelf, TestPickerRows) -> rows: 0, 1, 3, 6, 8
function S.pickerfit()
	local r = report()
	savePasses()
	setPasses(false)
	workspace:SetAttribute("TestGiftSelf", nil)
	openShop()
	local pgp = page()
	pgp:SetAttribute("TestPickerRows", 0)
	pgp:SetAttribute("TestDryRun", true)
	pgp.TestPress:Fire("Gift_VIP")
	task.wait(0.5)
	local pk = pgp.GiftPicker
	local bx = pk.Box
	r.check("picker open", pk.Visible)
	local K0 = K()
	local pageTop = pgp.AbsolutePosition.Y
	for _, case in {{nil, 0, 0}, {true, nil, 1}, {true, 2, 3}, {true, 5, 6}, {true, 7, 8}} do
		local selfOn, fake, n = case[1], case[2], case[3]
		workspace:SetAttribute("TestGiftSelf", selfOn)
		pgp:SetAttribute("TestPickerRows", fake)
		task.wait(0.35)
		local want = 79 + math.min(307, 8 + 68 * math.max(n, 1))
		local rows = 0
		for _, c in bx.Face.Players:GetChildren() do if c:IsA("GuiObject") then rows += 1 end end
		r.check(("%d rows: %d row objects"):format(n, n), rows == n, rows)
		r.check(("%d rows: PickerBoxH %d"):format(n, want), pgp:GetAttribute("PickerBoxH") == want and bx.Size.Y.Offset == want, tostring(pgp:GetAttribute("PickerBoxH")) .. " / " .. bx.Size.Y.Offset)
		local y0 = 66 + math.floor((386 - want) / 2 + 0.5)
		r.check(("%d rows: centred (y %d, x 160, 420 wide)"):format(n, y0), bx.Position.Y.Offset == y0 and bx.Position.X.Offset == 160 and bx.Size.X.Offset == 420, tostring(bx.Position))
		local face = bx:FindFirstChild("Face")
		r.check(("%d rows: Face %d tall, Players %d"):format(n, want - 5, math.min(307, 8 + 68 * math.max(n, 1))), face.Size.Y.Offset == want - 5 and bx.Face.Players.Size.Y.Offset == math.min(307, 8 + 68 * math.max(n, 1)), face.Size.Y.Offset .. " / " .. bx.Face.Players.Size.Y.Offset)
		-- inside the page body (screen px)
		local top = bx.AbsolutePosition.Y
		local bot = top + bx.AbsoluteSize.Y
		r.check(("%d rows: inside the body 66..452"):format(n), top >= pageTop + 66 * K0 - 1 and bot <= pageTop + 452 * K0 + 1, ("%.1f..%.1f vs %.1f..%.1f"):format(top, bot, pageTop + 66 * K0, pageTop + 452 * K0))
		if n == 0 then
			r.check("0 rows: empty lines shown at y 80 / 104", bx.Face.Empty1.Visible and bx.Face.Empty2.Visible and bx.Face.Empty1.Position.Y.Offset == 80 and bx.Face.Empty2.Position.Y.Offset == 104,
				bx.Face.Empty1.Position.Y.Offset .. " / " .. bx.Face.Empty2.Position.Y.Offset)
			local e2 = bx.Face.Empty2
			r.check("0 rows: the empty lines inside the face", e2.AbsolutePosition.Y + e2.AbsoluteSize.Y <= face.AbsolutePosition.Y + face.AbsoluteSize.Y + 1)
		else
			r.check(("%d rows: no empty lines"):format(n), not bx.Face.Empty1.Visible and not bx.Face.Empty2.Visible)
		end
		if _G.HatchContain then r.note((_G.HatchContain("S6 picker " .. n .. " rows", _G.HatchShopCfg()):gsub("\n", "\n     "))) end
	end
	pgp:SetAttribute("TestPickerRows", nil)
	closeShop()
	pgp:SetAttribute("TestDryRun", nil)
	workspace:SetAttribute("TestGiftSelf", nil)
	restorePasses()
	return r.text("pickerfit")
end

-- 12 (fix round, perf review I-2) each Shop section has its own error guard: ShopPage TestBreakSection = i breaks part i
-- (1 passes, 2 double, 3 boosts, 4 packs, 5 treadmill, 6 eggs); the other parts keep refreshing; ONE warning per part
function S.breaksection()
	local r = report()
	savePasses()
	setPasses(false)
	local tt = player:GetAttribute("TreadmillTier")
	player:SetAttribute("TreadmillTier", 2)
	openShop()
	local pgp = page()
	local warns = {}
	local conn = game:GetService("LogService").MessageOut:Connect(function(m) if m:find("[ShopClient] refresh part", 1, true) then table.insert(warns, m) end end)
	-- break the passes: a pass toggle does not show; the treadmill still follows the tier (11 -> the MAX pill)
	pgp:SetAttribute("TestBreakSection", 1)
	task.wait(0.7)
	player:SetAttribute("Pass_VIP", true)
	player:SetAttribute("TreadmillTier", 11)
	task.wait(0.8)
	local _, wv = priceOf(btnOf("Pass_VIP"))
	r.check("part 1 broken: VIP not refreshed (no OWNED)", wv ~= "OWNED", tostring(wv))
	local f = list().Treadmill.Face
	r.check("part 1 broken: the treadmill still refreshes (tier 11 -> MAX pill)", f.MoneyWide.Visible and f.Now.Text:find("MAX") ~= nil, f.Now.Text)
	local pp = priceOf(btnOf("Pack_Money3"))
	r.check("part 1 broken: pack prices still set", pp ~= nil and pp ~= "", tostring(pp))
	-- break the treadmill: the passes refresh again (VIP -> OWNED), the treadmill stays frozen at MAX on tier 2
	pgp:SetAttribute("TestBreakSection", 5)
	task.wait(0.7)
	player:SetAttribute("TreadmillTier", 2)
	task.wait(0.8)
	local _, wv2 = priceOf(btnOf("Pass_VIP"))
	r.check("part 5 broken: passes refresh (VIP OWNED)", wv2 == "OWNED", tostring(wv2))
	r.check("part 5 broken: the treadmill frozen (still the MAX pill on tier 2)", f.MoneyWide.Visible and not f.Robux.Visible, f.Now.Text)
	pgp:SetAttribute("TestBreakSection", nil)
	task.wait(0.8)
	r.check("unbroken: the treadmill catches up (tier 2: Money + Robux)", not f.MoneyWide.Visible and f.Money.Visible and f.Robux.Visible, f.Now.Text)
	conn:Disconnect()
	local n1, n5 = 0, 0
	for _, m in warns do
		if m:find("refresh part 1", 1, true) then n1 += 1 end
		if m:find("refresh part 5", 1, true) then n5 += 1 end
	end
	r.check("one warning per broken part (<= 1 each; 1 on the first run of the session)", n1 <= 1 and n5 <= 1, n1 .. " / " .. n5)
	r.note(("warnings this run: part 1 x%d, part 5 x%d (later runs of the same session: 0, warned once)"):format(n1, n5))
	player:SetAttribute("TreadmillTier", tt)
	restorePasses()
	closeShop()
	return r.text("breaksection")
end

-- 13 (fix round, perf review I-4) a hidden HATCH NIGHT page never rescales: ShopPage.CanvasScale gets 0 writes while the
-- Rebirth window opens / closes 3 times; the Shop opened again = Body px / 740
function S.canvasguard()
	local r = report()
	if win.Visible then mm.CloseWindow:Fire() task.wait(0.5) end
	local pgp = page()
	local cs = pgp:FindFirstChild("CanvasScale")
	local n = 0
	local c = cs:GetPropertyChangedSignal("Scale"):Connect(function() n += 1 end)
	for _ = 1, 3 do mm.OpenPage:Fire("Rebirth") task.wait(0.6) mm.CloseWindow:Fire() task.wait(0.5) end
	c:Disconnect()
	r.check("hidden ShopPage: 0 CanvasScale writes over 3 Rebirth open / close", n == 0, n)
	openShop()
	task.wait(0.3)
	r.check("Shop open: CanvasScale = Body px / 740", math.abs(cs.Scale - body.AbsoluteSize.X / 740) <= 0.002, ("%.4f vs %.4f"):format(cs.Scale, body.AbsoluteSize.X / 740))
	closeShop()
	return r.text("canvasguard")
end

_G.ShopTests = function(section, ...)
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	local ok, res = pcall(f, ...)
	return ok and res or ("ERROR in " .. section .. ": " .. tostring(res))
end
return "loaded: _G.ShopTests(section)"
