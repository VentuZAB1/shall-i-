-- rebirth_page_client.lua (2026-10-22, RIS plan 8.5 + review MUST 3 / 4 / 5, SHOULD 1 / 2 / 4 / 8 / 16; run C): the
-- HATCH NIGHT Rebirth page (RebirthClient page region). Client datamodel of a FRESH TestFreshSave Play session.
-- Load once (stores _G.RebirthPageTests), then run sections in this order:
--   open, states (local attributes, restored), lifecycle, tutorial (local TutorialExtra 3, restored)
--   Server "flow before" (Money 25000, record base size / SpeedMultiplier) -> confirm -> Server "flow after"
--   Server "refusal setup" (Money 0 + a Water pet) -> refusal (NEED MORE $!) ; Server "pet setup" (Money 1.2M, no pet)
--     -> refusalpet (NEED A PET!) ; Server: Money 0
--   skipdry (never a real Robux prompt: TestDryRun; TestSkip refuses without it)
--   Server "receipt" (ServerStorage.TestReceipt:Invoke(p, ShopConfig.SkipRebirthProduct)) is fired FROM skipreceipt1/2:
--     skipreceipt1 (arms the celebrate watch) -> Server TestReceipt -> skipreceipt2
--   legacy: own session with Edit workspace TestRebirthLegacy = true
-- MUST 5: the REBIRTH button is 476 x 60 in every state; its holder centre x is 492 (not ready) or 370 (ready / MAX).
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local MarketplaceService = game:GetService("MarketplaceService")
local RS = game:GetService("ReplicatedStorage")
local player = Players.LocalPlayer
local pg = player:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local RebirthConfig = require(RS:WaitForChild("RebirthConfig"))
local IndexConfig = require(RS:WaitForChild("IndexConfig"))
local ShopConfig = require(RS:WaitForChild("ShopConfig"))
local H
do
	local ok, B = pcall(require, RS.BrickUI)
	H = ok and B.Hatch or nil
end
local CHECK_ICON = "rbxassetid://78526516923039"
local X_ICON = "rbxassetid://71044264112125"

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
local function page() return body:FindFirstChild("RebirthPage") end
local function count(gui, name)
	local n = 0
	for _, c in gui:GetChildren() do if c.Name == name then n += 1 end end
	return n
end
local function waitFor(f, t)
	local t0 = os.clock()
	while os.clock() - t0 < (t or 2) do
		if f() then return true, os.clock() - t0 end
		task.wait(0.05)
	end
	return f(), os.clock() - t0
end
local function open()
	if not (win.Visible and page() and page().Visible) then
		if win.Visible then mm.CloseWindow:Fire() task.wait(0.4) end
		mm.OpenPage:Fire("Rebirth")
	end
	task.wait(0.8)
end
local function close() if win.Visible then mm.CloseWindow:Fire() task.wait(0.5) end end
local function gradTop(f) local g = f and f:FindFirstChildOfClass("UIGradient") return g and g.Color.Keypoints[1].Value end
local function same(a, b) return a and b and math.abs(a.R - b.R) < 0.004 and math.abs(a.G - b.G) < 0.004 and math.abs(a.B - b.B) < 0.004 end
local function palOf(holder)
	local top = gradTop(holder.Face)
	for name, p in H.PAL do if same(top, p.top) then return name end end
	return tostring(top)
end
local function btn() return page().Rebirth end
local function label() return btn().Face.Label.Text end
local function skipB() return page().Skip end
local function headNow() return page().Head.Now.Text end
local function headNext() return page().Head.Next.Visible and page().Head.Next.Text or nil end
local function setL(k, v) player:SetAttribute(k, v) end
local SAVED = {}
local function save() for _, k in {"Rebirths", "Money", "PetInventory", "TutorialExtra", "TutorialDone"} do SAVED[k] = player:GetAttribute(k) end end
local function restore() for k, v in SAVED do player:SetAttribute(k, v) end task.wait(0.6) end
local function liveSkipPrice()
	local ok, info = pcall(MarketplaceService.GetProductInfo, MarketplaceService, ShopConfig.SkipRebirthProduct, Enum.InfoType.Product)
	return ok and info and info.PriceInRobux and tostring(info.PriceInRobux) or tostring(ShopConfig.SkipRebirthPrice)
end
-- a gui object's box in SCREEN space (each ScreenGui's inset setting)
local function screenBox(o)
	local sg = o:FindFirstAncestorWhichIsA("ScreenGui")
	local inset = game:GetService("GuiService"):GetGuiInset().Y
	local dy = (sg and sg.IgnoreGuiInset) and 0 or inset
	local a, s = o.AbsolutePosition, o.AbsoluteSize
	return {a.X, a.Y + dy, a.X + s.X, a.Y + s.Y + dy}
end

local S = {}

-- 1 open: chrome, canvas, the zones, the legacy copy disabled, the HUD objects exactly once, MUST 5 width
function S.open()
	local r = report()
	open()
	local pp = page()
	r.check("HatchBack / HatchFront shown", win.HatchBack.Visible and win.HatchFront.Visible)
	r.check("title REBIRTH", win.HatchFront.Title.Text == "REBIRTH", win.HatchFront.Title.Text)
	r.check("violet tooth (112,0,214)", same(win.HatchFront.Crack.Tooth1.BackgroundColor3, Color3.fromRGB(112, 0, 214)), tostring(win.HatchFront.Crack.Tooth1.BackgroundColor3))
	local ar = win.AbsoluteSize.X / win.AbsoluteSize.Y
	r.check("window AR 740/470", math.abs(ar - 740 / 470) <= 0.01, ("%.4f"):format(ar))
	r.check("CanvasScale == SkinScale", pp and pp:FindFirstChild("CanvasScale") and math.abs(pp.CanvasScale.Scale - win.HatchBack.SkinScale.Scale) <= 0.001)
	r.check("HatchCanvas + exactly 1 RebirthPage", pp and pp:GetAttribute("HatchCanvas") == true and count(body, "RebirthPage") == 1, count(body, "RebirthPage"))
	if not (pp and pp:GetAttribute("HatchCanvas")) then return r.text("open") end
	local zones = 0
	for _, n in {"Medallion", "Head", "LineA", "LineB", "GetLabel", "Reward_slots", "Reward_speed", "Reward_money", "Reward_base", "NeedPet", "NeedMoney", "Skip", "Rebirth", "TutorialArrow", "Flash", "Rays"} do
		if pp:FindFirstChild(n) then zones += 1 end
	end
	r.check("zones (16)", zones == 16, zones)
	local legacy = player.PlayerScripts:FindFirstChild("RebirthClientLegacy")
	r.check("RebirthClientLegacy disabled", legacy ~= nil and legacy.Enabled == false)
	r.check("exactly 1 RebirthReadyUI + 1 RebirthTutorialUI", count(pg, "RebirthReadyUI") == 1 and count(pg, "RebirthTutorialUI") == 1, count(pg, "RebirthReadyUI") .. " / " .. count(pg, "RebirthTutorialUI"))
	r.check("MUST 5: REBIRTH 476 x 60", btn().Size.X.Offset == 476 and btn().Size.Y.Offset == 60, tostring(btn().Size))
	r.check("header icon = the Rebirth tile icon", win.HatchFront.Icon.Image == mm.Menu.Rebirth.Face.Icon.Image and win.HatchFront.Icon.Image ~= "", win.HatchFront.Icon.Image)
	local gs = mm.AbsoluteSize
	local want = math.min(H.pageCap("Rebirth", gs.Y), (gs.Y - 12) / 470)
	local got = win.AbsoluteSize.X / 740
	r.check("window scale = pageCap fit (no tutorial)", math.abs(got - want) <= 0.005, ("s %.4f want %.4f"):format(got, want))
	return r.text("open")
end

-- 2 states (local attributes; restored)
function S.states()
	local r = report()
	save()
	open()
	setL("TutorialExtra", 0) setL("PetInventory", "[]") setL("Rebirths", 0) setL("Money", 0)
	task.wait(0.7)
	local pp = page()
	r.check("R0: Head REBIRTH 0 > 1", headNow() == "REBIRTH 0" and headNext() == "1" and pp.Head.Arrow.Visible, headNow() .. " " .. tostring(headNext()))
	r.check("R0: medallion 1", pp.Medallion.Face.Num.Text == "1", pp.Medallion.Face.Num.Text)
	r.check("R0: no pet card, money card centred at x 192", not pp.NeedPet.Visible and pp.NeedMoney.Visible and pp.NeedMoney.Position.X.Offset == 192, pp.NeedMoney.Position.X.Offset)
	local ct = pp.NeedMoney.CostBar.Text.Text
	r.check("R0: CostBar $0 / $25K, status X", ct == "$0 / $25K" and pp.NeedMoney.Status.Image == X_ICON, ct)
	local price = liveSkipPrice()
	r.check("R0: SKIP gold, price " .. price, skipB().Visible and palOf(skipB()) == "gold" and skipB().Face.Price.Text == price and skipB().Face.Pre.Text == "SKIP", skipB().Face.Price.Text)
	r.check("R0: REBIRTH off at centre x 492 (MUST 5)", palOf(btn()) == "off" and btn().Position.X.Offset == 492 and label() == "REBIRTH!", palOf(btn()) .. " " .. btn().Position.X.Offset)
	r.check("R0: lines reset / keep", pp.LineA.Text == "MONEY + SPEED RESET!" and pp.LineB.Text == "YOU KEEP EVERYTHING ELSE!", pp.LineA.Text)
	r.check("R0: reward lines 3 > 4, x1 > x1.25, 0/5 > 1/5", pp.Reward_slots.Face.Line.Now.Text == "3" and pp.Reward_slots.Face.Line.Next.Text == "4"
		and pp.Reward_speed.Face.Line.Now.Text == "x1" and pp.Reward_speed.Face.Line.Next.Text == "x1.25" and pp.Reward_base.Face.Line.Next.Text == "1/5",
		pp.Reward_slots.Face.Line.Now.Text .. ">" .. pp.Reward_slots.Face.Line.Next.Text)
	setL("Money", 25000)
	local ok, t = waitFor(function() return palOf(btn()) == "lime" end, 0.7)
	r.check("Money 25K: REBIRTH lime within 0.6 s (dirty + the 0.5 s token loop)", ok and t <= 0.6 + 0.05, ("%.2f s"):format(t))
	r.check("ready: centre x 370, 476 wide, SKIP hidden, status check", btn().Position.X.Offset == 370 and btn().Size.X.Offset == 476 and not skipB().Visible and pp.NeedMoney.Status.Image == CHECK_ICON, btn().Position.X.Offset)
	-- R3 + no pet: the pet card (Thunder 100+ KG)
	setL("Money", 0) setL("Rebirths", 3)
	task.wait(0.6)
	local req = RebirthConfig.requirement(3)
	local area = IndexConfig.AREAS[req.area]
	r.check("R3: pet card " .. area.name:upper() .. " PET, X, money card at 374", pp.NeedPet.Visible and pp.NeedPet.Title.Text == area.name:upper() .. " PET" and pp.NeedPet.Status.Image == X_ICON and pp.NeedMoney.Position.X.Offset == 374,
		pp.NeedPet.Title.Text)
	r.check("R3: sub NEEDS 100+ KG, silhouette", (pp.NeedPet.Sub.Text == "NEEDS 100+ KG" or pp.NeedPet.Sub.Text == "100+ KG") and same(pp.NeedPet.Ring.Pet.ImageColor3, Color3.fromRGB(16, 16, 28)), pp.NeedPet.Sub.Text)
	r.check("R3: Head REBIRTH 3 > 4, slots 6 > 7, speed x1.75 > x2", headNow() == "REBIRTH 3" and headNext() == "4" and pp.Reward_slots.Face.Line.Now.Text == "6"
		and pp.Reward_speed.Face.Line.Next.Text == "x2", headNow())
	setL("PetInventory", '[{"id":"t_raiju","name":"Raiju","kg":150}]')
	task.wait(0.4)
	r.check("R3 + a qualifying pet: check, YOU HAVE ONE", pp.NeedPet.Status.Image == CHECK_ICON and pp.NeedPet.Sub.Text:sub(1, 12) == "YOU HAVE ONE" and same(pp.NeedPet.Ring.Pet.ImageColor3, H.WHITE), pp.NeedPet.Sub.Text)
	-- R5+: the base at max size
	setL("Rebirths", 6)
	task.wait(0.4)
	r.check("R6: base card MAX / BIGGEST BASE", pp.Reward_base.Face.Value.Text == "MAX" and pp.Reward_base.Face.Line.Now.Text == "BIGGEST BASE" and not pp.Reward_base.Face.Line.Next.Visible,
		pp.Reward_base.Face.Value.Text .. " " .. pp.Reward_base.Face.Line.Now.Text)
	-- MAX
	setL("Rebirths", RebirthConfig.MAX_REBIRTH)
	task.wait(0.4)
	r.check("MAX: medallion MAX, Head MAX REBIRTH 20 (no chevron)", pp.Medallion.Face.Num.Text == "MAX" and headNow() == "MAX REBIRTH" and headNext() == "20" and not pp.Head.Arrow.Visible, headNow() .. " " .. tostring(headNext()))
	r.check("MAX: silver MAX at centre x 370, needs + SKIP hidden", palOf(btn()) == "silver" and label() == "MAX" and btn().Position.X.Offset == 370 and not pp.NeedPet.Visible and not pp.NeedMoney.Visible and not skipB().Visible,
		palOf(btn()) .. " " .. label())
	r.check("MAX: YOUR REWARDS, YOU REACHED THE TOP! / LEGEND!", pp.GetLabel.Text == "YOUR REWARDS" and pp.LineA.Text == "YOU REACHED THE TOP!" and pp.LineB.Text == "LEGEND!", pp.GetLabel.Text)
	restore()
	return r.text("states")
end

-- 3 lifecycle (plan D8 / D9): closed = no loop, no frame work, no refresh; reopen = loop on + 1 refresh
function S.lifecycle()
	local r = report()
	save()
	open()
	task.wait(0.3)
	local pp = page()
	r.check("open: RebirthLoop on", pp:GetAttribute("RebirthLoop") == true)
	close()
	local off = waitFor(function() return pp:GetAttribute("RebirthLoop") == false end, 0.6)
	r.check("closed: RebirthLoop off within 0.6 s", off)
	local f0, n0 = pp:GetAttribute("HatchPerfRebirth"), pp:GetAttribute("RebirthRefreshN")
	setL("Money", (player:GetAttribute("Money") or 0) + 7)
	task.wait(1)
	setL("Money", SAVED.Money)
	task.wait(1)
	r.check("closed 2 s: HatchPerfRebirth frozen", pp:GetAttribute("HatchPerfRebirth") == f0, tostring(f0) .. " -> " .. tostring(pp:GetAttribute("HatchPerfRebirth")))
	r.check("closed: Money changes do not refresh", pp:GetAttribute("RebirthRefreshN") == n0, tostring(n0) .. " -> " .. tostring(pp:GetAttribute("RebirthRefreshN")))
	open()
	r.check("reopen: RebirthLoop on, exactly 1 refresh", pp:GetAttribute("RebirthLoop") == true and pp:GetAttribute("RebirthRefreshN") == n0 + 1, tostring(n0) .. " -> " .. tostring(pp:GetAttribute("RebirthRefreshN")))
	close()
	restore()
	return r.text("lifecycle")
end

-- 4 tutorial step 11 (review MUST 3): the guide's text stays above the window (shift first, shrink only the rest); the
-- arrow points at the REBIRTH button from its right. Native, forced 1.0982, forced 0.7106 (the guide keeps the PC size
-- in Studio: the real 1050x620 / phone rows are the hatch_pure R10 geometry).
function S.tutorial()
	local r = report()
	save()
	close()
	setL("TutorialDone", true) setL("Rebirths", 0) setL("PetInventory", "[]") setL("Money", 25000) setL("TutorialExtra", 3)
	task.wait(1.2)
	local tu = pg:FindFirstChild("TutorialUI")
	local guide = tu and tu:FindFirstChild("Guide")
	r.check("the guide is on screen (step 11)", tu and tu.Enabled and guide and guide.Visible)
	local function guideBottom()
		local b = -math.huge
		for _, n in {"Title", "Sub", "Pips"} do
			local o = guide:FindFirstChild(n, true)
			if o and o:IsA("GuiObject") and o.Visible then b = math.max(b, screenBox(o)[4]) end
		end
		return b
	end
	for _, s in {false, 1.0982, 0.7106} do
		mm:SetAttribute("HatchTestScale", s or nil)
		close()
		mm.OpenPage:Fire("Rebirth")
		task.wait(1.0)
		local pp = page()
		local wb, gb = screenBox(win), guideBottom()
		local gsB = screenBox(mm)
		local lbl = s and ("@" .. s) or "@native"
		r.check("guide text bottom <= window top - 4 " .. lbl, gb <= wb[2] - 4 + 0.5, ("guide %.1f, window top %.1f, s %.4f"):format(gb, wb[2], win.AbsoluteSize.X / 740))
		r.check("window inside the gui " .. lbl, wb[4] <= gsB[4] - 6 + 1 and wb[2] >= gsB[2] - 1, ("%.1f..%.1f in %.1f..%.1f"):format(wb[2], wb[4], gsB[2], gsB[4]))
		pp:SetAttribute("HatchTestPulse", 1.04)
		task.wait(0.15)
		local arrow = pp:FindFirstChild("TutorialArrow")
		local ab, fb = screenBox(arrow), screenBox(btn().Face)
		local acy = (ab[2] + ab[4]) / 2
		local k = win.AbsoluteSize.X / 740
		r.check("arrow on the REBIRTH button " .. lbl, arrow.Visible and acy >= fb[2] and acy <= fb[4] and ab[1] >= fb[3] + 8 * k - 1 and ab[3] <= screenBox(win)[3],
			("arrow %.1f..%.1f y %.1f, face %.1f..%.1f"):format(ab[1], ab[3], acy, fb[1], fb[3]))
		pp:SetAttribute("HatchTestPulse", nil)
	end
	mm:SetAttribute("HatchTestScale", nil)
	close()
	restore()
	return r.text("tutorial")
end

-- 5 confirm (Server "flow before": Rebirths 0, Money 25000 on the TestFreshSave save)
function S.confirm()
	local r = report()
	open()
	local pp = page()
	r.check("ready before the press", palOf(btn()) == "lime" and label() == "REBIRTH!", label())
	pp.TestPress:Fire()
	task.wait(0.2)
	r.check("1st press: Confirming, TAP AGAIN!, lines", pp:GetAttribute("Confirming") == true and label() == "TAP AGAIN!" and pp.LineA.Text == "TAP AGAIN TO REBIRTH!" and pp.LineB.Text == "MONEY + SPEED RESET!", label() .. " / " .. pp.LineA.Text)
	task.wait(2.7)
	r.check("no 2nd press in 2.5 s: back to REBIRTH!", pp:GetAttribute("Confirming") == false and label() == "REBIRTH!", label())
	local minFlash = 1
	local conn = pp.Flash:GetPropertyChangedSignal("BackgroundTransparency"):Connect(function() minFlash = math.min(minFlash, pp.Flash.BackgroundTransparency) end)
	local r0 = player:GetAttribute("Rebirths") or 0
	local m0 = player:GetAttribute("SpeedMultiplier")
	pp.TestPress:Fire()
	task.wait(0.3)
	pp.TestPress:Fire()
	local ok = waitFor(function() return (player:GetAttribute("Rebirths") or 0) == r0 + 1 end, 3)
	r.check("2 presses: server Rebirths " .. r0 .. " -> " .. r0 + 1, ok, player:GetAttribute("Rebirths"))
	r.check("Money + Speed reset", (player:GetAttribute("Money") or 0) == 0 and (player:GetAttribute("Speed") or 0) == RebirthConfig.START_SPEED, tostring(player:GetAttribute("Money")) .. " / " .. tostring(player:GetAttribute("Speed")))
	waitFor(function() return player:GetAttribute("SpeedMultiplier") ~= m0 end, 1)
	r.check("multiplier up (SpeedMultiplier)", (player:GetAttribute("SpeedMultiplier") or 0) > (m0 or 0), tostring(m0) .. " -> " .. tostring(player:GetAttribute("SpeedMultiplier")))
	task.wait(0.4)
	conn:Disconnect()
	r.check("medallion 2, Head REBIRTH 1 > 2", pp.Medallion.Face.Num.Text == "2" and headNow() == "REBIRTH 1", pp.Medallion.Face.Num.Text .. " " .. headNow())
	r.check("celebrate flash seen", minFlash < 1, minFlash)
	return r.text("confirm")
end

-- 6 refusal (review SHOULD 8: Server gives a qualifying pet first, so money is the only thing missing)
function S.refusal()
	local r = report()
	open()
	local pp = page()
	pp.TestPress:Fire()
	local ok = waitFor(function() return (label() == "NEED MORE $!" or label() == "NEED $!") and palOf(btn()) == "red" end, 1)
	r.check("NEED MORE $! red within 1 s", ok, label() .. " " .. palOf(btn()))
	task.wait(1.4)
	r.check("back to REBIRTH! off after 1.3 s", label() == "REBIRTH!" and palOf(btn()) == "off", label() .. " " .. palOf(btn()))
	return r.text("refusal")
end
function S.refusalpet()
	local r = report()
	open()
	page().TestPress:Fire()
	local ok = waitFor(function() return (label() == "NEED A PET!" or label() == "NEED PET!") and palOf(btn()) == "red" end, 1)
	r.check("NEED A PET! red within 1 s", ok, label())
	task.wait(1.4)
	r.check("back to REBIRTH! after 1.3 s", label() == "REBIRTH!", label())
	return r.text("refusalpet")
end

-- 7 skipdry (plan D11): a dry run records the buy; TestSkip refuses without TestDryRun (never a real prompt)
function S.skipdry()
	local r = report()
	open()
	local pp = page()
	r.check("SKIP visible (not ready)", skipB().Visible)
	pp:SetAttribute("TestLastBuy", nil)
	pp:SetAttribute("TestDryRunResult", nil)
	pp:SetAttribute("TestDryRun", true)
	pp.TestSkip:Fire()
	task.wait(0.3)
	r.check("dry run: TestLastBuy = [RebirthRequest, skip]", pp:GetAttribute("TestLastBuy") == HttpService:JSONEncode({"RebirthRequest", "skip"}), pp:GetAttribute("TestLastBuy"))
	pp:SetAttribute("TestDryRunResult", "Test save only")
	pp.TestSkip:Fire()
	task.wait(0.3)
	r.check("refusal TEST SAVE ONLY red", skipB().Face.Word.Visible and skipB().Face.Word.Text == "TEST SAVE ONLY" and palOf(skipB()) == "red", skipB().Face.Word.Text)
	task.wait(1.4)
	r.check("price back after 1.3 s", skipB().Face.Price.Visible and not skipB().Face.Word.Visible and palOf(skipB()) == "gold")
	pp:SetAttribute("TestDryRun", nil)
	pp:SetAttribute("TestDryRunResult", nil)
	pp:SetAttribute("TestLastBuy", "none")
	pp.TestSkip:Fire()
	task.wait(0.3)
	r.check("no TestDryRun: TestSkip refused (nothing recorded, no prompt)", pp:GetAttribute("TestLastBuy") == "none")
	pp:SetAttribute("TestLastBuy", nil)
	return r.text("skipdry")
end

-- 8 skipreceipt: the receipt side through ServerStorage.TestReceipt (Server step between 1 and 2)
function S.skipreceipt1()
	open()
	local pp = page()
	_G.RebirthCel = {r0 = player:GetAttribute("Rebirths") or 0, maxScale = 1}
	local sc = pp.Medallion:FindFirstChild("ButtonScale")
	_G.RebirthCel.conn = sc:GetPropertyChangedSignal("Scale"):Connect(function() _G.RebirthCel.maxScale = math.max(_G.RebirthCel.maxScale, sc.Scale) end)
	return "skipreceipt1: armed at Rebirths " .. _G.RebirthCel.r0 .. " (now the Server TestReceipt step)"
end
function S.skipreceipt2()
	local r = report()
	local c = _G.RebirthCel
	local ok = waitFor(function() return (player:GetAttribute("Rebirths") or 0) == c.r0 + 1 end, 2)
	r.check("receipt: Rebirths " .. c.r0 .. " -> " .. c.r0 + 1, ok, player:GetAttribute("Rebirths"))
	task.wait(0.4)
	r.check("Head REBIRTH " .. c.r0 + 1, headNow() == "REBIRTH " .. (c.r0 + 1), headNow())
	r.check("celebrate: medallion pop > 1.1", c.maxScale > 1.1, c.maxScale)
	c.conn:Disconnect()
	close()
	return r.text("skipreceipt")
end

-- 9 legacy: own session (Edit TestRebirthLegacy = true before Play)
function S.legacy()
	local r = report()
	local legacy = player.PlayerScripts:FindFirstChild("RebirthClientLegacy")
	r.check("RebirthClientLegacy enabled", waitFor(function() return legacy and legacy.Enabled end, 10))
	waitFor(function() return page() ~= nil end, 10)
	r.check("exactly 1 RebirthPage, no HatchCanvas", count(body, "RebirthPage") == 1 and page():GetAttribute("HatchCanvas") ~= true, count(body, "RebirthPage"))
	task.wait(1)
	r.check("exactly 1 RebirthReadyUI + 1 RebirthTutorialUI", count(pg, "RebirthReadyUI") == 1 and count(pg, "RebirthTutorialUI") == 1)
	open()
	r.check("open: Check-UI chrome", win.Face.Header.Visible and not win.HatchBack.Visible)
	close()
	return r.text("legacy")
end

_G.RebirthPageTests = function(section, ...)
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	local ok, res = pcall(f, ...)
	return ok and res or ("ERROR in " .. section .. ": " .. tostring(res))
end
return "loaded: _G.RebirthPageTests(section)"
