-- index_client.lua (2026-10-22, RIS plan 8.4 + review MUST 2 / 4, SHOULD 5 / 6 / 12 / 16; run B): the HATCH NIGHT
-- Creature Index page (IndexClient). Client datamodel of a FRESH TestFreshSave Play session (0 / 30 discovered).
-- Load once (stores _G.IndexTests), then run sections in this order:
--   open, tabs, cards, names, secret, inspect, again, tile          (client only; local IndexData, restored)
--   Server "complete area 1" -> claim
--   Server "complete areas 2 + 3" -> claimall
--   Server "complete area 4" -> refusal
--   lifecycle1 (closes) -> Server: PetIndex.record (a hatch) + "complete area 5" -> lifecycle2
--   legacy: own session with Edit workspace TestIndexLegacy = true
-- Server step "complete area i" (Server datamodel):
--   local PI = require(game.ServerScriptService.PetIndex) local p = game.Players:GetPlayers()[1] local d = PI.read(p)
--   for _, c in require(game.ReplicatedStorage.IndexConfig).creatures(i) do d.found[c.name] = {n = 1, best = 5} end
--   PI.write(p, d)
-- Claims are real (in-game rewards) on the TestFreshSave save. Every local IndexData change is restored.
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local RS = game:GetService("ReplicatedStorage")
local player = Players.LocalPlayer
local pg = player:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local IndexConfig = require(RS:WaitForChild("IndexConfig"))
local CreatureConfig = require(RS:WaitForChild("CreatureConfig"))
local SpeedStat = require(RS:WaitForChild("SpeedStat"))
local H
do
	local ok, B = pcall(require, RS.BrickUI)
	H = ok and B.Hatch or nil
end
local TOOTH = Color3.fromRGB(0, 120, 235)
local LIME = Color3.fromRGB(184, 255, 106)

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
local function page() return body:FindFirstChild("IndexPage") end
local function count()
	local n = 0
	for _, c in body:GetChildren() do if c.Name == "IndexPage" then n += 1 end end
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
		mm.OpenPage:Fire("Index")
	end
	task.wait(0.7)
end
local function close() if win.Visible then mm.CloseWindow:Fire() task.wait(0.5) end end
local function press(key) page().TestPress:Fire(key) task.wait(0.25) end
local function pctText(chance)
	local v = chance * 100
	if math.abs(v - math.floor(v + 0.5)) > 0.05 then return ("%.1f%%"):format(v) end
	return ("%d%%"):format(math.floor(v + 0.5))
end
local function data() return IndexConfig.decode(player:GetAttribute("IndexData")) end
local function setLocal(d) player:SetAttribute("IndexData", HttpService:JSONEncode(d)) task.wait(0.15) end
local function gradTop(f) local g = f and f:FindFirstChildOfClass("UIGradient") return g and g.Color.Keypoints[1].Value end
local function same(a, b) return a and b and math.abs(a.R - b.R) < 0.004 and math.abs(a.G - b.G) < 0.004 and math.abs(a.B - b.B) < 0.004 end
local function palOf(holder)
	local top = gradTop(holder.Face)
	for name, p in H.PAL do if same(top, p.top) then return name end end
	return tostring(top)
end
local function card(slot) return page()["Card" .. slot] end
local function claimBtn() return page().Reward.Face.Claim end
local function claimText() return claimBtn().Face.Label.Text end
local function allBtn() return page().Total.ClaimAll end
local function insp() return page().Inspect end
local function stat(k) return insp().Face["Stat" .. k] end
local function tileBadge()
	local t = mm:FindFirstChild("Menu") and mm.Menu:FindFirstChild("Index")
	return t and t.Face:FindFirstChild("Badge")
end
local function bonus() return player:GetAttribute("IndexBonus") or 0 end
local function pot(k) return player:GetAttribute("Potion_" .. k) or 0 end
local function money(n) return "$" .. SpeedStat.Format(n) end
local function upper(s) return (s:upper():gsub("\u{16B}", "\u{16A}")) end -- (Raiju's u-macron)

local S = {}

-- 1 open: chrome, canvas, the zones, the legacy copy disabled, MUST 2 rings, names off
function S.open()
	local r = report()
	open()
	local pp = page()
	r.check("HatchBack / HatchFront shown", win.HatchBack.Visible and win.HatchFront.Visible)
	r.check("title CREATURE INDEX", win.HatchFront.Title.Text == "CREATURE INDEX", win.HatchFront.Title.Text)
	r.check("cyan tooth (0,120,235)", same(win.HatchFront.Crack.Tooth1.BackgroundColor3, TOOTH), tostring(win.HatchFront.Crack.Tooth1.BackgroundColor3))
	local ar = win.AbsoluteSize.X / win.AbsoluteSize.Y
	r.check("window AR 740/470", math.abs(ar - 740 / 470) <= 0.01, ("%.4f"):format(ar))
	r.check("CanvasScale == SkinScale", pp and pp:FindFirstChild("CanvasScale") and math.abs(pp.CanvasScale.Scale - win.HatchBack.SkinScale.Scale) <= 0.001,
		pp and pp:FindFirstChild("CanvasScale") and ("%.4f %.4f"):format(pp.CanvasScale.Scale, win.HatchBack.SkinScale.Scale))
	r.check("HatchCanvas + exactly 1 IndexPage", pp and pp:GetAttribute("HatchCanvas") == true and count() == 1, count())
	if not (pp and pp:GetAttribute("HatchCanvas")) then return r.text("open") end
	local hits = 0
	for i = 1, 6 do local h = pp.Rail:FindFirstChild("Hit" .. i) if h and h:IsA("TextButton") then hits += 1 end end
	r.check("rail: 6 hits", hits == 6, hits)
	r.check("pill on slot 1 (centre y 31)", math.abs(pp.Rail.Pill.Position.Y.Offset - 31) <= 0.5, pp.Rail.Pill.Position.Y.Offset)
	local zones = 0
	for _, n in {"Card1", "Card2", "Card3", "Card4", "Card5", "AreaHead", "Reward", "Total", "Inspect"} do if pp:FindFirstChild(n) then zones += 1 end end
	r.check("zones: 5 cards, AreaHead, Reward, Total, Inspect", zones == 9, zones)
	local legacy = player.PlayerScripts:FindFirstChild("IndexClientLegacy")
	r.check("IndexClientLegacy disabled", legacy ~= nil and legacy.Enabled == false)
	-- review MUST 2: the Ring is in Card.Face at ZIndex 1, after Glow, on all 5 cards; Badges empty
	local bad = {}
	for slot = 1, 5 do
		local c = card(slot)
		local ring, glow = c.Face:FindFirstChild("Ring"), c.Face:FindFirstChild("Glow")
		local kids = c.Face:GetChildren()
		local ok = ring and ring.Parent == c.Face and ring.ZIndex == 1 and glow and table.find(kids, ring) > table.find(kids, glow) and #c.Badges:GetChildren() == 0
		if not ok then table.insert(bad, "Card" .. slot) end
	end
	r.check("MUST 2: Ring in Face, Z1, after Glow, Badges empty (5 cards)", #bad == 0, table.concat(bad, " "))
	r.check("header icon = the Index tile icon", win.HatchFront.Icon.Image == mm.Menu.Index.Face.Icon.Image and win.HatchFront.Icon.Image ~= "", win.HatchFront.Icon.Image)
	-- MUST 1 / plan D4: as big as today (pageCap Index) on PC
	local gs = mm.AbsoluteSize
	local want = math.min(H.pageCap("Index", gs.Y), (gs.Y - 12) / 470)
	local got = win.AbsoluteSize.X / 740
	local widthLimited = (gs.X - 8 - 230) / 740 < want
	r.check("window scale = pageCap fit", math.abs(got - want) <= 0.005 or (widthLimited and got < want), ("s %.4f want %.4f"):format(got, want))
	local named = 0
	for slot = 1, 5 do local n = card(slot).Face:FindFirstChild("Name") if n and n.Visible then named += 1 end end
	r.check("SHOW_CARD_NAMES = false: no name on the cards", named == 0, named)
	return r.text("open")
end

-- 2 tabs: the pill moves, the header + chances follow
function S.tabs()
	local r = report()
	open()
	press("Tab_3")
	task.wait(0.1)
	local pp = page()
	r.check("Tab_3: pill centre y 143", math.abs(pp.Rail.Pill.Position.Y.Offset - 143) <= 0.5, pp.Rail.Pill.Position.Y.Offset)
	r.check("AreaHead title THUNDER", pp.AreaHead.Face.Title.Text == "THUNDER", pp.AreaHead.Face.Title.Text)
	r.check("AreaHead sub STORM EGG", pp.AreaHead.Face.Sub.Text == "STORM EGG", pp.AreaHead.Face.Sub.Text)
	local odds = CreatureConfig.odds("StormEgg", 1)
	local okP, got = true, {}
	for slot = 1, 5 do
		local t = card(slot).Face.Pct.Text
		table.insert(got, t)
		if t ~= pctText(odds[slot] or 0) then okP = false end
	end
	r.check("Pct1..5 = the StormEgg chances", okP, table.concat(got, " "))
	r.check("active rail name WHITE, others in their area colour", same(pp.Rail.Name3.TextColor3, H.WHITE) and same(pp.Rail.Name1.TextColor3, IndexConfig.AREAS[1].colors[1]),
		tostring(pp.Rail.Name3.TextColor3) .. " / " .. tostring(pp.Rail.Name1.TextColor3))
	r.check("rail Prog3 0/5", pp.Rail.Prog3.Text == "0/5", pp.Rail.Prog3.Text)
	press("Tab_1")
	task.wait(0.1)
	r.check("Tab_1: pill centre y 31, title GRASS", math.abs(pp.Rail.Pill.Position.Y.Offset - 31) <= 0.5 and pp.AreaHead.Face.Title.Text == "GRASS", pp.AreaHead.Face.Title.Text)
	return r.text("tabs")
end

-- 3 cards: one Ring, the inspect follows
function S.cards()
	local r = report()
	open()
	press("Tab_1")
	press("Card_3")
	local rings = {}
	for slot = 1, 5 do if card(slot).Face.Ring.Visible then table.insert(rings, slot) end end
	r.check("Ring visible only on Card3", #rings == 1 and rings[1] == 3, table.concat(rings, ","))
	local known = data().found.Treant ~= nil
	local want = known and "TREANT" or "???"
	r.check("Inspect Name1 = " .. want, insp().Face.Name1.Text == want and not insp().Face.Name2.Visible, insp().Face.Name1.Text)
	press("Card_1")
	r.check("Card_1: Ring moves to Card1", card(1).Face.Ring.Visible and not card(3).Face.Ring.Visible)
	return r.text("cards")
end

-- 4 names: the 1- or 2-line rule (local IndexData)
function S.names()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	open()
	local d = data()
	for _, n in {"BlackDragon", "Treant", "SeaTurtleWarrior", "ThornbladeMantis"} do d.found[n] = {n = 1, best = 10} end
	setLocal(d)
	press("Tab_5") press("Card_3")
	local f = insp().Face
	r.check("BLACK EASTERN / DRAGON", f.Name1.Text == "BLACK EASTERN" and f.Name2.Visible and f.Name2.Text == "DRAGON", f.Name1.Text .. " / " .. f.Name2.Text)
	press("Tab_1") press("Card_3")
	r.check("TREANT one line at y 204, Name2 hidden", f.Name1.Text == "TREANT" and not f.Name2.Visible and f.Name1.Position.Y.Offset == 204, f.Name1.Text .. " y " .. f.Name1.Position.Y.Offset)
	press("Tab_2") press("Card_2")
	r.check("SEA TURTLE / WARRIOR", f.Name1.Text == "SEA TURTLE" and f.Name2.Text == "WARRIOR", f.Name1.Text .. " / " .. f.Name2.Text)
	press("Tab_1") press("Card_5")
	r.check("THORNBLADE / MANTIS", f.Name1.Text == "THORNBLADE" and f.Name2.Text == "MANTIS", f.Name1.Text .. " / " .. f.Name2.Text)
	player:SetAttribute("IndexData", saved)
	task.wait(0.15)
	press("Card_1")
	return r.text("names")
end

-- 5 secret: locked and unlocked (Grass card 5 = Thornblade Mantis, x3.1)
function S.secret()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	open()
	local d = data()
	d.found.ThornbladeMantis = nil
	setLocal(d)
	press("Tab_1") press("Card_5")
	local c5, f = card(5), insp().Face
	r.check("locked: dark gold face (74,58,34)", same(gradTop(c5.Face), Color3.fromRGB(74, 58, 34)), tostring(gradTop(c5.Face)))
	r.check("locked: star shown, silhouette (black), ? shown", c5.Icons.Pop.Star.Visible and same(c5.Icons.Pop.Portrait.ImageColor3, H.BLACK) and c5.Icons.Pop.Q.Visible)
	r.check("locked: card Glow hidden", not c5.Face.Glow.Visible)
	r.check("locked inspect: ???, SECRET! tag, bonus x3.1", f.Name1.Text == "???" and f.SecretTag.Visible and f.Bonus.Visible and f.Bonus.Text.Text == "x3.1",
		f.Name1.Text .. " " .. tostring(f.SecretTag.Visible) .. " " .. f.Bonus.Text.Text)
	r.check("locked inspect: glow (70,75,100), big silhouette + ?", same(f.Glow.ImageColor3, Color3.fromRGB(70, 75, 100)) and same(insp().Icons.Pop.BigPortrait.ImageColor3, H.BLACK) and insp().Icons.Pop.Q.Visible)
	d.found.ThornbladeMantis = {n = 2, best = 1200}
	setLocal(d)
	r.check("unlocked: gold face (140,106,30)", same(gradTop(c5.Face), Color3.fromRGB(140, 106, 30)), tostring(gradTop(c5.Face)))
	r.check("unlocked: star shown, portrait in colour, ? hidden, Glow shown", c5.Icons.Pop.Star.Visible and same(c5.Icons.Pop.Portrait.ImageColor3, H.WHITE) and not c5.Icons.Pop.Q.Visible and c5.Face.Glow.Visible)
	r.check("unlocked inspect: THORNBLADE / MANTIS, gold glow, tag + bonus", f.Name1.Text == "THORNBLADE" and same(f.Glow.ImageColor3, Color3.fromRGB(255, 214, 90)) and f.SecretTag.Visible and f.Bonus.Visible)
	r.check("a normal card has no star, no gold face", not card(1).Icons.Pop.Star.Visible and not same(gradTop(card(1).Face), Color3.fromRGB(74, 58, 34)))
	-- the tag + bonus group is centred in the 222 face with an 8 gap (review: one group)
	local tg, bn = f.SecretTag, f.Bonus
	local l, rr = tg.Position.X.Offset, bn.Position.X.Offset + bn.Size.X.Offset
	r.check("tag + bonus centred, gap 8", math.abs((l + rr) / 2 - 111) <= 1 and math.abs(bn.Position.X.Offset - (l + tg.Size.X.Offset) - 8) <= 1, ("%d..%d"):format(l, rr))
	player:SetAttribute("IndexData", saved)
	task.wait(0.15)
	press("Card_1")
	return r.text("secret")
end

-- 6 inspect: the stats (review SHOULD 5: L (8, 4, 94, 16): at 92 "HATCHED" is 84 %, see the ledger ruling)
function S.inspect()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	open()
	local d = data()
	d.found.Treant = {n = 3, best = 2400}
	d.found.MossbackTortoise = nil
	setLocal(d)
	press("Tab_1") press("Card_3")
	local L = {}
	for k = 1, 4 do table.insert(L, stat(k).L.Text) end
	r.check("labels INCOME / BEST KG / HATCHED / CHANCE", table.concat(L, "|") == "INCOME|BEST KG|HATCHED|CHANCE", table.concat(L, "|"))
	r.check("L box (8, 4, 94, ...) ends before V (104)", stat(1).L.Position.X.Offset == 8 and stat(1).L.Size.X.Offset == 94 and stat(1).V.Position.X.Offset == 104, stat(1).L.Size.X.Offset)
	local inc = money(CreatureConfig.income("Treant", 2400))
	r.check("INCOME " .. inc .. "/s (lime)", (stat(1).V.Text == inc .. "/s" or stat(1).V.Text == inc) and same(stat(1).V.TextColor3, LIME), stat(1).V.Text)
	r.check("BEST KG 2.4K KG", stat(2).V.Text == "2.4K KG" or stat(2).V.Text == "2.4K", stat(2).V.Text)
	r.check("HATCHED x3", stat(3).V.Text == "x3", stat(3).V.Text)
	r.check("CHANCE 13%", stat(4).V.Text == "13%", stat(4).V.Text)
	local f = insp().Face
	r.check("bonus x1.6, no SECRET! tag", f.Bonus.Visible and f.Bonus.Text.Text == "x1.6" and not f.SecretTag.Visible, f.Bonus.Text.Text)
	press("Card_1")
	local V = {}
	for k = 1, 4 do table.insert(V, stat(k).V.Text) end
	r.check("unknown: ??? / ??? / x0 / 52%", table.concat(V, "|") == "???|???|x0|52%", table.concat(V, "|"))
	r.check("x1.0 creature: no bonus chip", not f.Bonus.Visible)
	player:SetAttribute("IndexData", saved)
	task.wait(0.15)
	return r.text("inspect")
end

-- 7 again: an area claimed at an older version, complete again (local)
function S.again()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	open()
	local d = data()
	for _, c in IndexConfig.creatures(4) do d.found[c.name] = {n = 1, best = 5} end
	d.claimed["4"] = 2
	d.claims["4"] = 1
	setLocal(d)
	press("Tab_4")
	local t = page().Reward.Face.Title.Text
	r.check("title NEW PET! CLAIM AGAIN:", t == "NEW PET! CLAIM AGAIN:" or t == "NEW PET!", t)
	r.check("Claim CLAIM! lime + rail Dot4", claimText() == "CLAIM!" and palOf(claimBtn()) == "lime" and page().Rail.Dot4.Visible, claimText() .. " " .. palOf(claimBtn()))
	player:SetAttribute("IndexData", saved)
	task.wait(0.15)
	press("Tab_1")
	return r.text("again")
end

-- 8 tile + counter: the left-menu Index tile badge and DISCOVERED x / 30 follow the data (local)
function S.tile()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	open()
	local n0 = IndexConfig.discovered(data())
	r.check("counter DISCOVERED " .. n0 .. " / 30", page().Total.Bar.Text.Text == ("DISCOVERED %d / %d"):format(n0, IndexConfig.total()), page().Total.Bar.Text.Text)
	r.check("tile badge exists, hidden with nothing to claim", tileBadge() ~= nil and not tileBadge().Visible)
	local d = data()
	for _, c in IndexConfig.creatures(2) do d.found[c.name] = {n = 1, best = 5} end
	d.claimed["2"] = nil
	setLocal(d)
	local n1 = IndexConfig.discovered(data())
	r.check("counter follows: DISCOVERED " .. n1 .. " / 30", page().Total.Bar.Text.Text == ("DISCOVERED %d / %d"):format(n1, IndexConfig.total()), page().Total.Bar.Text.Text)
	r.check("tile badge shown (Water complete, unclaimed)", tileBadge() and tileBadge().Visible)
	r.check("rail Dot2 + CLAIM ALL (1)", page().Rail.Dot2.Visible and allBtn().Visible and allBtn().Face.Label.Text == "CLAIM ALL (1)", allBtn().Face.Label.Text)
	close()
	player:SetAttribute("IndexData", saved)
	task.wait(0.2)
	r.check("closed + data back: tile badge hidden (HUD follows while closed)", tileBadge() and not tileBadge().Visible)
	return r.text("tile")
end

-- 9 claim: after Server "complete area 1"
function S.claim()
	local r = report()
	open()
	press("Tab_1")
	local pp = page()
	r.check("Dot1 shown, Star1 hidden", pp.Rail.Dot1.Visible and not pp.Rail.Star1.Visible)
	r.check("Claim CLAIM! lime", claimText() == "CLAIM!" and palOf(claimBtn()) == "lime", claimText() .. " " .. palOf(claimBtn()))
	r.check("CLAIM ALL (1)", allBtn().Visible and allBtn().Face.Label.Text == "CLAIM ALL (1)", allBtn().Face.Label.Text)
	r.check("tile badge shown", tileBadge() and tileBadge().Visible)
	r.check("CLAIM! breathes: IndexLoop on while open", page():GetAttribute("IndexLoop") == true)
	local b0, m0, h0 = bonus(), pot("Money"), pot("Hatch")
	press("Claim")
	local ok = waitFor(function() return IndexConfig.claimedVersion(data(), 1) == IndexConfig.version(1) end, 3)
	r.check("claimed[1] = version(1) within 3 s", ok, IndexConfig.claimedVersion(data(), 1))
	waitFor(function() return pot("Hatch") > h0 end, 2)
	r.check("IndexBonus +0.05", math.abs(bonus() - b0 - 0.05) < 1e-6, ("%.3f -> %.3f"):format(b0, bonus()))
	r.check("Potion_Money +1, Potion_Hatch +1", pot("Money") == m0 + 1 and pot("Hatch") == h0 + 1, ("%d->%d %d->%d"):format(m0, pot("Money"), h0, pot("Hatch")))
	task.wait(0.2)
	r.check("Claim CLAIMED! silver, Active false", claimText() == "CLAIMED!" and palOf(claimBtn()) == "silver" and claimBtn().Face.Active == false, claimText() .. " " .. palOf(claimBtn()))
	r.check("Star1 shown, Dot1 hidden", pp.Rail.Star1.Visible and not pp.Rail.Dot1.Visible)
	r.check("CLAIM ALL hidden", not allBtn().Visible)
	r.check("tile badge hidden", tileBadge() and not tileBadge().Visible)
	local b1, m1 = bonus(), pot("Money")
	press("Claim")
	task.wait(1)
	r.check("2nd press: nothing sent (bonus + potions unchanged)", bonus() == b1 and pot("Money") == m1)
	return r.text("claim")
end

-- 10 claimall: after Server "complete areas 2 + 3" (review SHOULD 12: potions +2)
function S.claimall()
	local r = report()
	open()
	r.check("CLAIM ALL (2) gold", allBtn().Visible and allBtn().Face.Label.Text == "CLAIM ALL (2)" and palOf(allBtn()) == "gold", allBtn().Face.Label.Text)
	local b0, m0, h0 = bonus(), pot("Money"), pot("Hatch")
	press("ClaimAll")
	local ok = waitFor(function() local d = data() return IndexConfig.isClaimed(d, 2) and IndexConfig.isClaimed(d, 3) end, 3)
	r.check("areas 2 + 3 claimed within 3 s", ok)
	waitFor(function() return pot("Hatch") >= h0 + 2 end, 2)
	r.check("IndexBonus +0.10", math.abs(bonus() - b0 - 0.10) < 1e-6, ("%.3f -> %.3f"):format(b0, bonus()))
	r.check("Potion_Money +2, Potion_Hatch +2", pot("Money") == m0 + 2 and pot("Hatch") == h0 + 2, ("%d->%d %d->%d"):format(m0, pot("Money"), h0, pot("Hatch")))
	task.wait(0.2)
	r.check("CLAIM ALL hidden, Star2 + Star3 shown", not allBtn().Visible and page().Rail.Star2.Visible and page().Rail.Star3.Visible)
	return r.text("claimall")
end

-- 11 refusal: after Server "complete area 4" (review SHOULD 6: nil-safe message)
function S.refusal()
	local r = report()
	open()
	press("Tab_4")
	r.check("Tab_4: CLAIM! lime", claimText() == "CLAIM!" and palOf(claimBtn()) == "lime", claimText())
	local b0 = bonus()
	page():SetAttribute("TestClaimFail", "Nothing to claim")
	press("Claim")
	r.check("refusal NOTHING TO CLAIM red", claimText() == "NOTHING TO CLAIM" and palOf(claimBtn()) == "red", claimText() .. " " .. palOf(claimBtn()))
	task.wait(1.4)
	r.check("back to CLAIM! lime after 1.3 s", claimText() == "CLAIM!" and palOf(claimBtn()) == "lime", claimText())
	page():SetAttribute("TestClaimFail", "")
	press("Claim")
	r.check("an empty message -> TRY AGAIN", claimText() == "TRY AGAIN" and palOf(claimBtn()) == "red", claimText())
	task.wait(1.4)
	r.check("server state unchanged (area 4 not claimed, bonus same)", not IndexConfig.isClaimed(data(), 4) and bonus() == b0)
	press("Tab_1")
	return r.text("refusal")
end

-- 12 lifecycle: closed = no refresh, even when a pet hatches (plan D8); reopen = 1 refresh with the new data
function S.lifecycle1()
	open()
	close()
	task.wait(0.3)
	_G.IndexLife = {n = page():GetAttribute("IndexRefreshN") or 0}
	return "lifecycle1: closed, IndexRefreshN " .. _G.IndexLife.n .. " (now the Server step: a hatch + complete area 5)"
end
function S.lifecycle2()
	local r = report()
	local n0 = _G.IndexLife and _G.IndexLife.n or -1
	task.wait(0.5)
	r.check("closed: IndexRefreshN frozen through the hatch + IndexData changes", (page():GetAttribute("IndexRefreshN") or 0) == n0, n0 .. " -> " .. tostring(page():GetAttribute("IndexRefreshN")))
	r.check("closed: the tile badge still follows (areas 4 + 5 claimable)", tileBadge() and tileBadge().Visible)
	r.check("closed: no per-frame loop (IndexLoop false)", page():GetAttribute("IndexLoop") ~= true)
	open()
	local n1 = page():GetAttribute("IndexRefreshN") or 0
	r.check("reopen: exactly 1 refresh", n1 == n0 + 1, n0 .. " -> " .. n1)
	r.check("reopen: Dot5 shown, Prog5 5/5, CLAIM ALL (2)", page().Rail.Dot5.Visible and page().Rail.Prog5.Text == "5/5" and allBtn().Face.Label.Text == "CLAIM ALL (2)", page().Rail.Prog5.Text .. " " .. allBtn().Face.Label.Text)
	close()
	return r.text("lifecycle")
end

-- 13 legacy: own session (Edit workspace TestIndexLegacy = true before Play)
function S.legacy()
	local r = report()
	local legacy = player.PlayerScripts:FindFirstChild("IndexClientLegacy")
	r.check("IndexClientLegacy enabled", waitFor(function() return legacy and legacy.Enabled end, 10))
	waitFor(function() return page() ~= nil end, 10)
	r.check("exactly 1 IndexPage, no HatchCanvas", count() == 1 and page():GetAttribute("HatchCanvas") ~= true, count())
	open()
	r.check("open: Check-UI chrome (Header shown, HatchBack hidden)", win.Face.Header.Visible and not win.HatchBack.Visible)
	close()
	return r.text("legacy")
end

_G.IndexTests = function(section, ...)
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	local ok, res = pcall(f, ...)
	return ok and res or ("ERROR in " .. section .. ": " .. tostring(res))
end
return "loaded: _G.IndexTests(section)"
