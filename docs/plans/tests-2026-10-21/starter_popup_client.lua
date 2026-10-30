-- starter_popup_client.lua (2026-10-21, popup/Shop plan 7.4 + review MUST 2/9/11): client checks for the HATCH NIGHT
-- Starter Pack popup (StarterPackClient). Replaces starter_hud_client.lua S.popup (it tested the old popup tree).
-- HOW TO RUN (Studio, Play, TestFreshSave session ONLY):
--   Edit: workspace TestFreshSave = true (read it back), Play. Server: p:SetAttribute("Rebirths", 1);
--   ServerStorage.StarterDebug:Invoke("reset", p). Client: paste this file once (stores _G.PopupTests), then
--   return _G.PopupTests("open") etc. Sections: open, inside, seen, timer, buy, odds, restricted, owned, expiry, auto.
--   Close paths (CloseHit / NoThanks / Backdrop) are driven by the MCP mouse tool between "closeprep" calls:
--   _G.PopupTests("closeprep") opens it and returns the 3 instance paths; after each click "closed" reports.
--   Server steps (Server datamodel): local p = game.Players:GetPlayers()[1]; local D = game.ServerStorage.StarterDebug
--     D:Invoke("endsAt", p, os.time() + 1800)  (last hour)   D:Invoke("restricted", p, true / nil)
--     D:Invoke("grant", p)  (owned, no prompt)              D:Invoke("reset", p)  (a fresh 24 h)
--     D:Invoke("endsAt", p, os.time() + 8)  (expiry)
--   NEVER D:Invoke("buy") while the offer is live (review MUST 9). Every BUY press here is a dry run (MUST 11).
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local RS = game:GetService("ReplicatedStorage")
local player = Players.LocalPlayer
local pg = player:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local P = require(RS.StarterPackConfig)
local CreatureConfig = require(RS.CreatureConfig)
local H = require(RS.BrickUI).Hatch
local gui = pg:WaitForChild("StarterPackUI")
local holder = gui.Holder
local canvas = holder.Canvas

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
local function waitFor(pred, timeout)
	local t0 = os.clock()
	while os.clock() - t0 < timeout do
		if pred() then return os.clock() - t0 end
		task.wait()
	end
	return pred() and (os.clock() - t0) or nil
end
local function box(o) local p, s = o.AbsolutePosition, o.AbsoluteSize return {p.X, p.Y, p.X + s.X, p.Y + s.Y} end
local function inside(a, b, tol) tol = tol or 1 return a[1] >= b[1] - tol and a[2] >= b[2] - tol and a[3] <= b[3] + tol and a[4] <= b[4] + tol end
local function fmt(b) return ("%.1f,%.1f..%.1f,%.1f"):format(b[1], b[2], b[3], b[4]) end
local function close()
	if gui.Enabled then gui.Enabled = false task.wait(0.1) end
end
local function decode(s) local ok, t = pcall(HttpService.JSONDecode, HttpService, s or "") return ok and t or nil end
local function gradTop(f) local g = f:FindFirstChildOfClass("UIGradient") return g and g.Color.Keypoints[1].Value end
local function lastKey(g) local k = g.Color.Keypoints return k[#k].Value end
local function same3(a, b) return math.abs(a.R - b.R) < 0.002 and math.abs(a.G - b.G) < 0.002 and math.abs(a.B - b.B) < 0.002 end
local buyFace = function() return canvas.Buy.Face end
local function buyWord() local f = buyFace() return f.Word.Visible and f.Word.Text or nil end

-- the plan 3.2 fit: modal, centred in MainMenu's box, leftClear 0
local function fitCheck(r, label)
	local gs = mm.AbsoluteSize
	local s = H.fitWindow(gs.X, gs.Y, 0)
	local test = gui:GetAttribute("HatchTestScale")
	if type(test) == "number" then s = test end
	r.check(label .. ": Holder width = 740 x fit", math.abs(holder.AbsoluteSize.X - 740 * s) <= 1, ("%.1f vs %.1f (s %.4f)"):format(holder.AbsoluteSize.X, 740 * s, s))
	-- (fix round, visual review SHOULD 3) the height: 470 x fit, or 374 x fit when restricted (no odds band)
	local ph = player:GetAttribute("StarterRestricted") ~= false and 374 or 470
	r.check(label .. ": Holder height = " .. ph .. " x fit", math.abs(holder.AbsoluteSize.Y - ph * s) <= 1, ("%.1f vs %.1f"):format(holder.AbsoluteSize.Y, ph * s))
	local hc = holder.AbsolutePosition + holder.AbsoluteSize / 2
	local mc = mm.AbsolutePosition + mm.AbsoluteSize / 2
	r.check(label .. ": centred in MainMenu's box", (hc - mc).Magnitude <= 1.5, ("%.1f,%.1f vs %.1f,%.1f"):format(hc.X, hc.Y, mc.X, mc.Y))
	r.check(label .. ": SkinScale == CanvasScale == Holder px / 740", math.abs(holder.HatchBack.SkinScale.Scale - canvas.CanvasScale.Scale) <= 0.001
		and math.abs(canvas.CanvasScale.Scale - holder.AbsoluteSize.X / 740) <= 0.002, ("%.4f %.4f %.4f"):format(holder.HatchBack.SkinScale.Scale, canvas.CanvasScale.Scale, holder.AbsoluteSize.X / 740))
	r.check(label .. ": title STARTER PACK!", string.upper(holder.HatchFront.Title.Text) == "STARTER PACK!", holder.HatchFront.Title.Text)
	r.check(label .. ": magenta tooth (220,0,100)", holder.HatchFront.Crack.Tooth1.BackgroundColor3 == Color3.fromRGB(220, 0, 100))
	r.check(label .. ": no Bats", holder.HatchFront:FindFirstChild("Bats") == nil)
	r.check(label .. ": no UIScale on the Holder (D11)", holder:FindFirstChildOfClass("UIScale") == nil)
end

local S = {}

-- 1 open paths: TestOpen, Open (the HUD), the Shop card's TestPress (dry run only, MUST 11)
function S.open()
	local r = report()
	close()
	mm.CloseWindow:Fire()
	task.wait(0.3)
	gui.TestOpen:Fire()
	task.wait(0.35)
	r.check("TestOpen -> Enabled", gui.Enabled)
	fitCheck(r, "TestOpen")
	close()
	gui.Open:Fire()
	task.wait(0.35)
	r.check("Open (HUD path) -> Enabled", gui.Enabled)
	fitCheck(r, "Open")
	close()
	-- the Shop card: its BUY only opens the popup
	mm.OpenPage:Fire("Shop")
	task.wait(0.8)
	local slot = mm.Window.Face.Body.ShopPage.Scroll.List.StarterSlot
	r.check("Shop card shown (offer active)", slot.Visible and slot:FindFirstChild("Card") ~= nil)
	gui:SetAttribute("TestDryRun", nil)
	slot.TestPress:Fire()
	task.wait(0.3)
	r.check("MUST 11: card TestPress refused without dry run", not gui.Enabled)
	gui:SetAttribute("TestDryRun", true)
	gui:SetAttribute("TestLastBuy", "none")
	slot.TestPress:Fire()
	task.wait(0.35)
	r.check("card BUY -> popup Enabled", gui.Enabled)
	r.check("card BUY never buys (TestLastBuy unchanged)", gui:GetAttribute("TestLastBuy") == "none", gui:GetAttribute("TestLastBuy"))
	fitCheck(r, "card")
	r.check("popup over the Shop: DisplayOrder 22 > MainMenu", gui.DisplayOrder > mm.DisplayOrder, gui.DisplayOrder .. " vs " .. mm.DisplayOrder)
	close()
	mm.CloseWindow:Fire()
	gui:SetAttribute("TestDryRun", nil)
	gui:SetAttribute("TestLastBuy", nil)
	task.wait(0.3)
	return r.text("open")
end

-- 2a close paths: opens the popup and returns the instance paths to click (the MCP mouse tool clicks them)
function S.closeprep()
	close()
	mm.CloseWindow:Fire()
	task.wait(0.3)
	gui.TestOpen:Fire()
	task.wait(0.4)
	-- clicked with the MCP mouse tool: instance paths LocalPlayer.PlayerGui.StarterPackUI.Holder.HatchFront.CloseHit and
	-- ...Holder.Canvas.NoThanks.Face; the Backdrop at screen (60, 420) (left of the window); inside clicks on
	-- ...Canvas.PotionRow / ...Canvas.Odds must NOT close it (2026-10-21: all four passed)
	return HttpService:JSONEncode({enabled = gui.Enabled})
end
function S.closed()
	local r = report()
	r.check("closed", waitFor(function() return not gui.Enabled end, 0.6) ~= nil)
	return r.text("closed")
end

-- 2b the hit order: inside the window the first GuiButton is the Holder (or a child), never the Backdrop
function S.inside()
	local r = report()
	close()
	gui.TestOpen:Fire()
	task.wait(0.4)
	local s = canvas.CanvasScale.Scale
	local cp = canvas.AbsolutePosition
	local function firstButton(x, y)
		for _, o in pg:GetGuiObjectsAtPosition(x, y) do
			if o:IsA("GuiButton") and o.Visible then return o end
		end
	end
	for _, pt in {{600, 300}, {155, 196}, {370, 40}, {700, 250}} do
		local o = firstButton(cp.X + pt[1] * s, cp.Y + pt[2] * s)
		r.check(("canvas (%d,%d): first button is in the Holder"):format(pt[1], pt[2]), o ~= nil and (o == holder or o:IsDescendantOf(holder)), o and o:GetFullName())
	end
	local o = firstButton(mm.AbsolutePosition.X + 6, mm.AbsolutePosition.Y + mm.AbsoluteSize.Y / 2)
	r.check("outside the window: the Backdrop", o == gui.Backdrop, o and o:GetFullName())
	local function centreOf(g) local b = box(g) return (b[1] + b[3]) / 2, (b[2] + b[4]) / 2 end
	local cx, cy = centreOf(holder.HatchFront.CloseHit)
	local c = firstButton(cx, cy)
	r.check("CloseHit centre: CloseHit first", c == holder.HatchFront.CloseHit, c and c:GetFullName())
	local nx, ny = centreOf(canvas.NoThanks.Face)
	local n = firstButton(nx, ny)
	r.check("NoThanks centre: NoThanks first", n == canvas.NoThanks.Face, n and n:GetFullName())
	close()
	return r.text("inside")
end

-- 3 Seen: the first open marks the offer seen on the server (needs a fresh reset: StarterPopup false)
function S.seen()
	local r = report()
	close()
	r.check("precondition: StarterPopup false (server reset)", player:GetAttribute("StarterPopup") ~= true, tostring(player:GetAttribute("StarterPopup")))
	gui.TestOpen:Fire()
	local t = waitFor(function() return player:GetAttribute("StarterPopup") == true end, 2)
	r.check("StarterPopup true within 2 s", t ~= nil, t and ("%.2f s"):format(t))
	close()
	return r.text("seen")
end

-- 4 timer (mode "normal" or "urgent": the server set endsAt os.time() + 1800 first)
function S.timer(mode)
	local r = report()
	close()
	gui.TestOpen:Fire()
	task.wait(0.8)
	local e = canvas.EndsIn
	r.check("EndsIn text", e.Text:match("^ENDS IN %d+:%d%d") ~= nil, e.Text)
	r.check("EndsIn has no background", e.BackgroundTransparency == 1)
	local want = mode == "urgent" and Color3.fromRGB(255, 60, 50) or Color3.fromRGB(255, 170, 0)
	r.check("EndsIn gradient last key " .. tostring(mode), same3(lastKey(e:FindFirstChildOfClass("UIGradient")), want), tostring(lastKey(e:FindFirstChildOfClass("UIGradient"))))
	local t0 = e.Text
	task.wait(1.1)
	r.check("ticks", e.Text ~= t0, t0 .. " -> " .. e.Text)
	r.check("StarterTicker on while open", gui:GetAttribute("StarterTicker") == true)
	close()
	task.wait(0.7)
	r.check("StarterTicker off when closed", gui:GetAttribute("StarterTicker") == false)
	-- the Shop card timer
	mm.OpenPage:Fire("Shop")
	task.wait(1)
	local tm = mm.Window.Face.Body.ShopPage.Scroll.List.StarterSlot.Card.Face.Timer
	r.check("card Timer ends with LEFT", tm.Text:match("LEFT$") ~= nil, tm.Text)
	r.check("card Timer gradient " .. tostring(mode), same3(lastKey(tm:FindFirstChildOfClass("UIGradient")), want))
	mm.CloseWindow:Fire()
	task.wait(0.3)
	return r.text("timer " .. tostring(mode))
end

-- 5 dry-run buy (MUST 11): TestBuy refused without TestDryRun; the args; a refusal word for 1.4 s; Price attribute
function S.buy()
	local r = report()
	close()
	gui.TestOpen:Fire()
	task.wait(0.5)
	gui:SetAttribute("TestDryRun", nil)
	gui:SetAttribute("TestLastBuy", "none")
	gui.TestBuy:Fire()
	task.wait(0.2)
	r.check("MUST 11: TestBuy refused without dry run", gui:GetAttribute("TestLastBuy") == "none")
	gui:SetAttribute("TestDryRun", true)
	gui:SetAttribute("TestDryRunResult", nil)
	gui.TestBuy:Fire()
	task.wait(0.2)
	local got = decode(gui:GetAttribute("TestLastBuy"))
	r.check("TestLastBuy == [StarterBuy, Popup]", got and got[1] == "StarterBuy" and got[2] == "Popup" and #got == 2, gui:GetAttribute("TestLastBuy"))
	r.check("prompted -> still the gold BUY", buyWord() == nil and same3(gradTop(buyFace()), H.PAL.gold.top))
	gui:SetAttribute("TestDryRunResult", "Offer ended")
	gui.TestBuy:Fire()
	task.wait(0.2)
	r.check("refusal: OFFER ENDED red", buyWord() == "OFFER ENDED" and same3(gradTop(buyFace()), H.PAL.red.top), tostring(buyWord()))
	r.check("refusal word fits", buyFace().Word.TextFits)
	task.wait(1.5)
	local f = buyFace()
	r.check("after 1.4 s: gold BUY + price", buyWord() == nil and f.Pre.Visible and f.Pre.Text == "BUY" and f.Price.Visible and same3(gradTop(f), H.PAL.gold.top), f.Pre.Text .. " " .. f.Price.Text)
	r.check("Price attribute == the label", gui:GetAttribute("Price") == f.Price.Text, tostring(gui:GetAttribute("Price")) .. " / " .. f.Price.Text)
	gui:SetAttribute("TestDryRunResult", nil)
	gui:SetAttribute("TestDryRun", nil)
	gui:SetAttribute("TestLastBuy", nil)
	close()
	return r.text("buy")
end

-- 6 odds visible (the paid random item rule): (a)-(g); n = HatchTestOdds (nil, 6, 7)
function S.odds(n)
	local r = report()
	close()
	gui:SetAttribute("HatchTestOdds", n)
	gui.TestOpen:Fire()
	task.wait(0.5)
	local odds, cap = canvas.Odds, canvas.OddsCaption
	r.check("(a) Odds + caption visible", odds.Visible and cap.Visible)
	local lines = P.odds(player:GetAttribute("StarterEgg") or "TideEgg", player:GetAttribute("StarterKg") or P.EGG_KG[2], CreatureConfig)
	local want = {}
	if type(n) == "number" then for i = 1, n do want[i] = lines[(i - 1) % #lines + 1] end else want = lines end
	local cells = {}
	for i = 1, 20 do local c = odds:FindFirstChild("Odds" .. i) if c then table.insert(cells, c) end end
	r.check("(b) cell count == #P.odds" .. (n and (" x" .. n) or ""), #cells == #want, #cells .. " vs " .. #want)
	local pctOk, secretOk, secrets = true, true, 0
	for i, c in cells do
		local o = want[i]
		if not o or c.Pct.Text ~= P.pctText(o.pct) then pctOk = false r.note(("cell %d: %s vs %s"):format(i, c.Pct.Text, o and P.pctText(o.pct) or "-")) end
		if o and o.secret then
			secrets += 1
			local q = c:FindFirstChild("Secret")
			if not (c.Pet.ImageColor3 == Color3.new(0, 0, 0) and q and q.Visible) then secretOk = false end
		end
	end
	r.check("(c) every Pct == P.pctText, in order", pctOk)
	r.check("(d) secret cells: black silhouette + ?", secretOk and secrets > 0, secrets .. " secret")
	local hb, mb = box(holder), box(mm)
	local inOk = true
	for _, c in cells do
		for _, d in c:GetDescendants() do
			if d:IsA("GuiObject") and d.Visible then
				local b = box(d)
				if not (inside(b, hb) and inside(b, mb)) then inOk = false r.note(d.Name .. " " .. fmt(b)) end
			end
		end
		if not (inside(box(c), hb) and inside(box(c), mb)) then inOk = false end
	end
	r.check("(e) every cell inside the Holder and MainMenu's box", inOk)
	-- (f) a 6 x 3 grid over the recess: the first drawn object is StarterPackUI's
	local ob = box(odds)
	local bad = 0
	for gx = 1, 6 do
		for gy = 1, 3 do
			local x = ob[1] + (ob[3] - ob[1]) * (gx - 0.5) / 6
			local y = ob[2] + (ob[4] - ob[2]) * (gy - 0.5) / 3
			local first
			for _, o in pg:GetGuiObjectsAtPosition(x, y) do
				local drawn = o.Visible and (o.BackgroundTransparency < 1 or (o:IsA("ImageLabel") and o.Image ~= "") or (o:IsA("TextLabel") and o.Text ~= ""))
				if drawn then first = o break end
			end
			if not (first and first:IsDescendantOf(gui)) then bad += 1 r.note(("grid %d,%d: %s"):format(gx, gy, first and first:GetFullName() or "nothing")) end
		end
	end
	r.check("(f) 18 samples over the odds: StarterPackUI on top", bad == 0, bad .. " bad")
	local sf = 0
	for _, d in holder:GetDescendants() do if d:IsA("ScrollingFrame") then sf += 1 end end
	r.check("(g) Buy visible with no scrolling (no ScrollingFrame)", canvas.Buy.Visible and sf == 0 and inside(box(canvas.Buy), mb), sf)
	gui:SetAttribute("HatchTestOdds", nil)
	return r.text("odds " .. tostring(n))
end

-- 6b restricted (the server set D:Invoke("restricted", p, true) first)
function S.restricted()
	local r = report()
	close()
	gui.TestOpen:Fire()
	task.wait(0.5)
	r.check("restricted attribute", player:GetAttribute("StarterRestricted") ~= false)
	r.check("no Odds / caption / EggRow", not canvas.Odds.Visible and not canvas.OddsCaption.Visible and not canvas.EggRow.Visible)
	r.check("PotionRow 10x EVERY POTION", canvas.PotionRow.Line1.Text == P.RESTRICTED_POTION_COUNT .. "x EVERY POTION", canvas.PotionRow.Line1.Text)
	r.check("hero = the cash art", canvas.Hero.Egg.Image == "rbxassetid://88694661500877" and not canvas.Hero.Cash.Visible)
	S.layoutCheck(r, true)
	fitCheck(r, "restricted")
	if _G.HatchContain and _G.HatchPopupCfg then r.note(_G.HatchContain("P restricted", _G.HatchPopupCfg())) end
	close()
	return r.text("restricted")
end

-- 6c (fix round, visual review SHOULD 3 / B23) the layout for the restricted state (true) or the full offer (false), read
-- live while the popup is open: 374 / 470 tall, the buttons at 288 / 384, the rows at 101, 175 / 140, 214, the hero at
-- (155, 184 / 196)
function S.layoutCheck(r, rr)
	local tag = rr and "restricted" or "full"
	local function y(o) return o.Position.Y.Offset end
	r.check(tag .. ": chrome HatchBack / HatchFront " .. (rr and 374 or 470) .. " tall", holder.HatchBack.Size.Y.Offset == (rr and 374 or 470) and holder.HatchFront.Size.Y.Offset == (rr and 374 or 470), holder.HatchBack.Size.Y.Offset .. " / " .. holder.HatchFront.Size.Y.Offset)
	r.check(tag .. ": canvas " .. (rr and 367 or 463) .. " tall", canvas.Size.Y.Offset == (rr and 367 or 463), canvas.Size.Y.Offset)
	r.check(tag .. ": buttons centre y " .. (rr and 318 or 414), y(canvas.Buy) == (rr and 318 or 414) and y(canvas.NoThanks) == (rr and 318 or 414), y(canvas.Buy) .. " / " .. y(canvas.NoThanks))
	r.check(tag .. ": PotionRow y " .. (rr and 101 or 140), y(canvas.PotionRow) == (rr and 101 or 140), y(canvas.PotionRow))
	r.check(tag .. ": CashRow y " .. (rr and 175 or 214), y(canvas.CashRow) == (rr and 175 or 214), y(canvas.CashRow))
	r.check(tag .. ": Hero (155, " .. (rr and 184 or 196) .. ")", canvas.Hero.Position.X.Offset == 155 and y(canvas.Hero) == (rr and 184 or 196), tostring(canvas.Hero.Position))
	r.check(tag .. ": Odds " .. (rr and "hidden" or "shown"), canvas.Odds.Visible == not rr and canvas.OddsCaption.Visible == not rr)
	local hb, bb = box(holder), box(canvas.Buy)
	r.check(tag .. ": Buy inside the Holder", inside(bb, hb), fmt(bb) .. " in " .. fmt(hb))
end
-- B23: "relayoutprep" opens it (full offer: D:Invoke("restricted", p, nil) first); the server flips the policy
-- (D:Invoke("restricted", p, true)) while it is open; "relayout" (true) checks the live re-layout; flip back, "relayout" (false)
function S.relayoutprep()
	close()
	gui.TestOpen:Fire()
	task.wait(0.5)
	local r = report()
	S.layoutCheck(r, false)
	fitCheck(r, "relayoutprep")
	return r.text("relayoutprep")
end
function S.relayout(rr)
	local r = report()
	local t = waitFor(function() return (canvas.Size.Y.Offset == 367) == rr end, 2)
	r.check("re-laid out live within 2 s", t ~= nil, t and ("%.2f s"):format(t))
	r.check("still open", gui.Enabled)
	task.wait(0.4)
	S.layoutCheck(r, rr)
	fitCheck(r, "relayout " .. tostring(rr))
	return r.text("relayout " .. tostring(rr))
end

-- 6d (fix round, perf review I-1) the Shop card's BUY breathes only while the card is in the scroll's visible box
function S.cardpulse()
	local r = report()
	close()
	mm.CloseWindow:Fire()
	task.wait(0.4)
	r.check("closed: RaysLoop false", gui:GetAttribute("RaysLoop") == false, tostring(gui:GetAttribute("RaysLoop")))
	mm.OpenPage:Fire("Shop")
	task.wait(0.8)
	local sp = mm.Window.Face.Body.ShopPage
	local function frames() return tonumber(((gui:GetAttribute("HatchPerfPopup") or "0"):match("^(%d+)"))) or 0 end
	r.check("Shop at the top, card in view: RaysLoop true", gui:GetAttribute("RaysLoop") == true and sp.Scroll.List.StarterSlot.Visible)
	local f0 = frames()
	task.wait(2.5) -- (the probe updates every 30 frames; an unfocused Studio runs ~15 fps)
	r.check("card in view: frames counted", frames() > f0, f0 .. " -> " .. frames())
	sp.TestPress:Fire("Tab_POTIONS")
	task.wait(0.9)
	r.check("scrolled past the card: RaysLoop false", gui:GetAttribute("RaysLoop") == false, tostring(gui:GetAttribute("RaysLoop")))
	local f1 = frames()
	task.wait(2.5)
	r.check("scrolled past the card: no frames (0 work)", frames() == f1, f1 .. " -> " .. frames())
	local cb = sp.Scroll.List.StarterSlot:FindFirstChild("Buy", true)
	local sc = cb and cb:FindFirstChildWhichIsA("UIScale", true)
	r.check("card BUY pulse stopped (scale 1)", sc == nil or math.abs(sc.Scale - 1) < 0.001, sc and sc.Scale)
	sp.TestPress:Fire("Tab_FEATURED")
	task.wait(0.9)
	r.check("back at the top: RaysLoop true", gui:GetAttribute("RaysLoop") == true)
	-- a manual scroll just past the card (y 150) and back to y 100 (the card partly shown)
	local K = sp.Scroll.AbsoluteSize.Y / 386
	sp.Scroll.CanvasPosition = Vector2.new(0, 150 * K)
	task.wait(0.3)
	r.check("manual scroll y 150 (card gone): RaysLoop false", gui:GetAttribute("RaysLoop") == false)
	sp.Scroll.CanvasPosition = Vector2.new(0, 100 * K)
	task.wait(0.3)
	r.check("manual scroll y 100 (card partly shown): RaysLoop true", gui:GetAttribute("RaysLoop") == true)
	mm.CloseWindow:Fire()
	task.wait(0.5)
	r.check("Shop closed: RaysLoop false", gui:GetAttribute("RaysLoop") == false)
	-- (the bug this caught: the in-view test read AbsolutePosition, still the last layout's right after a reopen)
	mm.OpenPage:Fire("Shop")
	task.wait(0.3)
	sp.TestPress:Fire("Tab_EGGS")
	task.wait(0.8)
	mm.CloseWindow:Fire()
	task.wait(0.5)
	mm.OpenPage:Fire("Shop")
	task.wait(0.5)
	r.check("reopen (was scrolled to EGGS): RaysLoop true at once", gui:GetAttribute("RaysLoop") == true)
	mm.CloseWindow:Fire()
	task.wait(0.5)
	return r.text("cardpulse")
end

-- 7 owned: call "ownedprep" (opens), then the server D:Invoke("grant", p), then "owned"
function S.ownedprep()
	close()
	gui:SetAttribute("TestThanksHold", nil)
	gui.TestOpen:Fire()
	task.wait(0.5)
	_G.POPUP_GRANT_T = os.clock()
	return "open: " .. tostring(gui.Enabled)
end
function S.owned()
	local r = report()
	local t = waitFor(function() return player:GetAttribute("StarterPack") == true end, 2)
	r.check("StarterPack true", t ~= nil)
	-- (the grant -> onOwned -> 1.6 s -> the 0.12 s close; the prep-to-grant gap is the tool round trip)
	local closedT = waitFor(function() return not gui.Enabled end, 2.6)
	r.check("closed within 2.2 s of the grant", closedT ~= nil, ("%.2f s since prep"):format(os.clock() - _G.POPUP_GRANT_T))
	local slot = mm.Window.Face.Body.ShopPage.Scroll.List.StarterSlot
	r.check("Shop slot hidden", slot.Visible == false)
	local hud = pg:FindFirstChild("StarterPackHud")
	local vis = 0
	if hud and hud.Enabled then
		for _, d in hud:GetDescendants() do
			if d:IsA("GuiObject") and d.AbsoluteSize.X > 0 then
				local x, ok = d, true
				while x and x:IsA("GuiObject") do if not x.Visible then ok = false end x = x.Parent end
				if ok then vis += 1 end
			end
		end
	end
	r.check("StarterPackHud art hidden", vis == 0, vis .. " visible objects")
	gui.TestOpen:Fire()
	task.wait(0.3)
	r.check("owned: TestOpen does nothing", not gui.Enabled)
	return r.text("owned")
end
-- 7b the frozen thank-you state (P3 / screenshots): TestThanksHold keeps it open
function S.thanksprep()
	close()
	gui:SetAttribute("TestThanksHold", true)
	gui.TestOpen:Fire()
	task.wait(0.5)
	return "open: " .. tostring(gui.Enabled) .. " (TestThanksHold)"
end
function S.thanks()
	local r = report()
	task.wait(1.8)
	local f = buyFace()
	r.check("held open", gui.Enabled)
	r.check("THANK YOU!", string.upper(holder.HatchFront.Title.Text) == "THANK YOU!", holder.HatchFront.Title.Text)
	r.check("Buy OWNED! lime", buyWord() == "OWNED!" and same3(gradTop(f), H.PAL.lime.top), tostring(buyWord()))
	r.check("NoThanks + EndsIn hidden", not canvas.NoThanks.Visible and not canvas.EndsIn.Visible)
	return r.text("thanks")
end

-- 8 expiry: call "expiryprep" (opens), then the server D:Invoke("endsAt", p, os.time() + 8), then "expiry"
function S.expiryprep()
	close()
	gui.TestOpen:Fire()
	task.wait(0.4)
	_G.POPUP_EXPIRY_T = os.clock()
	return "open: " .. tostring(gui.Enabled)
end
function S.expiry()
	local r = report()
	local t = waitFor(function() return not gui.Enabled end, 12)
	r.check("closed by the offer's end", t ~= nil, ("%.2f s since prep"):format(os.clock() - _G.POPUP_EXPIRY_T))
	r.check("slot hidden", mm.Window.Face.Body.ShopPage.Scroll.List.StarterSlot.Visible == false)
	gui.TestOpen:Fire()
	task.wait(0.3)
	r.check("ended: TestOpen does nothing", not gui.Enabled)
	return r.text("expiry")
end

-- 9 auto-popup: the server set Rebirths 1 + reset (StarterPopup false), tutorial done; nothing on screen
function S.auto()
	local r = report()
	close()
	mm.CloseWindow:Fire()
	r.check("precondition: StarterPopup false", player:GetAttribute("StarterPopup") ~= true)
	local t = waitFor(function() return gui.Enabled end, 15)
	r.check("auto-popup within 15 s", t ~= nil, t and ("%.1f s"):format(t))
	task.wait(0.5)
	close()
	local again = waitFor(function() return gui.Enabled end, 20)
	r.check("does not reappear within 20 s", again == nil)
	return r.text("auto")
end

_G.PopupTests = function(section, ...)
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	local ok, res = pcall(f, ...)
	return ok and res or ("ERROR in " .. section .. ": " .. tostring(res))
end
return "loaded: _G.PopupTests(section)"
