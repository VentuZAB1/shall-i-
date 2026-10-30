---------------------------------------------------------------- v8 (2026-10-28 Glacier update): the Check-UI Index page
-- (IndexClientLegacy rebuilt to the approved v8 mockup; the live client). Client datamodel of a TestFreshSave Play session.
-- Order: v8open, v8tabs, v8cards, v8inspect, v8claimui (client only, local IndexData restored), then
-- Server "complete area 7" (non-mythic creatures only, see the header) -> v8claim (a real claim on the TestFreshSave save).
local function v8text(o) return o and (o.Text:gsub("<[^>]->", "")) or "?" end
local function v8kid(o, n) return o and o:FindFirstChild(n) end
local function v8face(holder) return holder and holder:FindFirstChild("Face") end
local function v8top(holder) local f = v8face(holder) local g = f and f:FindFirstChildOfClass("UIGradient") return g and g.Color.Keypoints[1].Value end
local function v8open()
	if not (win.Visible and page() and page().Visible) then
		if win.Visible then mm.CloseWindow:Fire() task.wait(0.4) end
		mm.OpenPage:Fire("Index")
	end
	task.wait(0.7)
end
local V8_LIME, V8_SILVER, V8_OFF = Color3.fromRGB(180, 255, 25), Color3.fromRGB(216, 222, 228), Color3.fromRGB(80, 85, 90)
local V8_GOLD, V8_MYTHIC = Color3.fromRGB(255, 224, 96), Color3.fromRGB(40, 34, 84)
local V8_AMBER_M1 = Color3.fromRGB(214, 98, 0)

-- v8 1: one page, the v8 chrome, the window shape, 7 tabs + 6 cards, everything inside the face
function S.v8open()
	local r = report()
	v8open()
	local pp = page()
	local face = win.Face
	r.check("exactly 1 IndexPage, IndexV8", count() == 1 and pp and pp:GetAttribute("IndexV8") == true, count())
	local legacy = player.PlayerScripts:FindFirstChild("IndexClientLegacy")
	r.check("IndexClientLegacy enabled (the live client)", legacy ~= nil and legacy.Enabled == true)
	r.check("chrome: header 0.15 of the face", face.Header.Size.Y.Scale == 0.15, face.Header.Size.Y.Scale)
	r.check("chrome: no bottom bevel block, Body card hidden", win.Depth.Visible == false and face.Body.BackgroundTransparency == 1)
	local ps, fs = pp.AbsoluteSize, face.AbsoluteSize
	r.check("page fills the face (+-2 px)", math.abs(ps.X - fs.X) <= 2 and math.abs(ps.Y - fs.Y) <= 2, tostring(ps) .. " vs " .. tostring(fs))
	local ar = win.AbsoluteSize.X / win.AbsoluteSize.Y
	r.check("window aspect 1.575", math.abs(ar - 1.575) <= 0.01, ("%.4f"):format(ar))
	local vp = workspace.CurrentCamera.ViewportSize
	if vp.Y >= 520 then
		r.check("PC: window <= 58 % of the screen width", win.AbsoluteSize.X <= 0.58 * vp.X + 1, ("%.1f %%"):format(100 * win.AbsoluteSize.X / vp.X))
	end
	local n = 0
	for i = 1, #IndexConfig.AREAS do if pp:FindFirstChild("Tab" .. i) then n += 1 end end
	r.check("tabs: one per area (" .. #IndexConfig.AREAS .. ")", n == #IndexConfig.AREAS and #IndexConfig.AREAS == 7, n)
	local c = 0
	for slot = 1, 6 do if pp:FindFirstChild("Card" .. slot) then c += 1 end end
	r.check("cards: 6 slots (2 rows of 3)", c == 6 and not pp:FindFirstChild("Card7"), c)
	r.check("rows: Card4 under Card1, same x", math.abs(pp.Card4.AbsolutePosition.X - pp.Card1.AbsolutePosition.X) <= 1 and pp.Card4.AbsolutePosition.Y > pp.Card1.AbsolutePosition.Y + pp.Card1.AbsoluteSize.Y)
	local zones = 0
	for _, z in {"Header", "Grid", "Reward", "Total", "Inspect"} do if pp:FindFirstChild(z) then zones += 1 end end
	r.check("zones Header, Grid, Reward, Total, Inspect", zones == 5, zones)
	local last = pp["Tab" .. #IndexConfig.AREAS]
	local lastBottom = last.AbsolutePosition.Y + last.AbsoluteSize.Y
	local faceBottom = face.AbsolutePosition.Y + face.AbsoluteSize.Y
	r.check("tab column fits the face", lastBottom <= faceBottom and pp.Tab1.AbsolutePosition.Y >= face.Header.AbsolutePosition.Y + face.Header.AbsoluteSize.Y,
		("last tab bottom %d, face bottom %d"):format(lastBottom, faceBottom))
	local names = {}
	for i, a in IndexConfig.AREAS do if v8text(v8kid(v8face(pp["Tab" .. i]), "AreaName")) ~= upper(a.name) then table.insert(names, i) end end
	r.check("tab names = the area names", #names == 0, table.concat(names, ","))
	-- the GLACIER ! clears the R (review 5 NICE): the badge's left edge is right of the name's text
	local tn = v8kid(v8face(pp.Tab7), "AreaName")
	local bang = pp.Tab7.Ready
	local textRight = tn.AbsolutePosition.X + tn.AbsoluteSize.X / 2 + tn.TextBounds.X / 2
	r.note(("GLACIER text right %d, ! left %d (overlap %d px)"):format(textRight, bang.AbsolutePosition.X, math.max(0, textRight - bang.AbsolutePosition.X)))
	r.check("CLAIM ALL = review 5 M1 amber (214,98,0)", same(v8top(pp.Total.ClaimAll), V8_AMBER_M1), tostring(v8top(pp.Total.ClaimAll)))
	r.check("CLAIM ALL label 3 px black stroke", v8kid(v8face(pp.Total.ClaimAll), "Label").UIStroke.Thickness == 3)
	return r.text("v8open")
end

-- v8 2: every tab: header, card count, chances, BONUS pip only where a mythic lives, the selected tab's white rim
function S.v8tabs()
	local r = report()
	v8open()
	local pp = page()
	for i, a in IndexConfig.AREAS do
		press("Tab_" .. i)
		local list = IndexConfig.creatures(i)
		local shown = 0
		for slot = 1, 6 do if pp["Card" .. slot].Visible then shown += 1 end end
		local odds = CreatureConfig.odds(a.egg, 1)
		local okP, got = true, {}
		for slot = 1, #list do
			local t = v8text(v8kid(v8face(pp["Card" .. slot]), "Chance").Face.Text)
			table.insert(got, t)
			if t ~= pctText(odds[slot] or 0) then okP = false end
		end
		local mythic = false
		for _, c in list do if c.mythic then mythic = true end end
		local others = true
		for j = 1, #IndexConfig.AREAS do
			local s = pp["Tab" .. j].Face.UIStroke
			if (j == i) ~= same(s.Color, Color3.new(1, 1, 1)) then others = false end
		end
		r.check(("tab %d %s: header, %d cards, chances, pip %s, white rim"):format(i, a.name, #list, tostring(mythic)),
			v8text(pp.Header.Face.Area) == upper(a.name) .. " CREATURES" and shown == #list and okP and pp.Header.Face.Bonus.Visible == mythic and others,
			v8text(pp.Header.Face.Area) .. " | " .. shown .. " | " .. table.concat(got, " "))
	end
	press("Tab_1")
	return r.text("v8tabs")
end

-- v8 3: card kinds + found / not found (local IndexData)
function S.v8cards()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	v8open()
	local pp = page()
	local d = data()
	for _, c in IndexConfig.creatures(7) do if not c.mythic then d.found[c.name] = {n = 2, best = 1e6} else d.found[c.name] = nil end end
	d.claimed["7"] = nil
	d.found.CinderOverlord = {n = 1, best = 4e5}
	setLocal(d)
	press("Tab_7")
	local c5, c6, c1 = pp.Card5, pp.Card6, pp.Card1
	r.check("Card6 MYTHIC: rainbow ring + MYTHIC badge, no SECRET badge", pp.Ring6.Visible and c6.Mythic.Visible and c6.MythicEdge.Visible and not c6.Secret.Visible)
	r.check("Card6 not found: ???, ?, black silhouette", v8text(c6.Face.PetName) == "???" and c6.Face.Q.Visible and same(c6.Face.View.ImageColor3, Color3.new(0, 0, 0)))
	r.check("Card5 SECRET: gold card + SECRET badge, no ring", c5.Secret.Visible and not pp.Ring5.Visible and same(v8top(c5), V8_GOLD), tostring(v8top(c5)))
	r.check("Card5 found: PERMAFROST TITAN, no ?, colour portrait", v8text(c5.Face.PetName) == "PERMAFROST TITAN" and not c5.Face.Q.Visible and same(c5.Face.View.ImageColor3, Color3.new(1, 1, 1)))
	r.check("Card1 normal: no badge, no ring", not c1.Secret.Visible and not c1.Mythic.Visible and not pp.Ring1.Visible)
	r.check("portrait crop on Card1 (FrostfangLynx)", c1.Face.View.ImageRectSize.X > 0 and c1.Face.View.ImageRectSize.X < 512, tostring(c1.Face.View.ImageRectSize))
	r.check("tab 7: 5/6, ! (complete without the mythic), no star", v8text(pp.Tab7.Face.Prog) == "5/6" and pp.Tab7.Ready.Visible and not pp.Tab7.Star.Visible, v8text(pp.Tab7.Face.Prog))
	r.check("header 5 / 5 + BONUS 0/1", v8text(pp.Header.Face.Bar.Text) == "5 / 5" and v8text(pp.Header.Face.Bonus.Face.Text) == "BONUS 0/1",
		v8text(pp.Header.Face.Bar.Text) .. " " .. v8text(pp.Header.Face.Bonus.Face.Text))
	r.check("CLAIM! lime (mythic not needed)", v8text(pp.Reward.Claim.Face.Label) == "CLAIM!" and same(v8top(pp.Reward.Claim), V8_LIME), v8text(pp.Reward.Claim.Face.Label))
	press("Card_6")
	task.wait(0.3)
	r.check("select the mythic: white select frame, card / ring / frame at 1.04", pp.Select6.Visible and math.abs(c6.UIScale.Scale - 1.04) < 0.01
		and math.abs(pp.Ring6.UIScale.Scale - 1.04) < 0.01 and math.abs(pp.Select6.UIScale.Scale - 1.04) < 0.01, c6.UIScale.Scale)
	local i = pp.Inspect
	r.check("inspect mythic (not found): ??? / rainbow edge / x0 / 0.1%", v8text(i.PetName) == "???" and i.RarityEdge.Visible and v8text(i.Stat3.V) == "x0" and v8text(i.Stat4.V) == "0.1%",
		v8text(i.PetName) .. " " .. v8text(i.Stat4.V))
	r.check("inspect pill GLACIER · MYTHIC · $x..", v8text(i.Rarity.Text):match("^GLACIER · MYTHIC · %$x%d") ~= nil, v8text(i.Rarity.Text))
	press("Card_5")
	r.check("select the secret: Select6 hidden, Card5 rim white", not pp.Select6.Visible and same(c5.Face.UIStroke.Color, Color3.new(1, 1, 1)))
	press("Tab_4")
	r.check("Fire Card6 = CINDER OVERLORD (found) with the rainbow ring", v8text(pp.Card6.Face.PetName) == "CINDER OVERLORD" and pp.Ring6.Visible and same(v8top(pp.Card6), V8_MYTHIC))
	r.check("Fire header BONUS 1/1, CLAIM shows what is LEFT", v8text(pp.Header.Face.Bonus.Face.Text) == "BONUS 1/1" and v8text(pp.Reward.Claim.Face.Label):match("LEFT$") ~= nil
		and same(v8top(pp.Reward.Claim), V8_OFF), v8text(pp.Reward.Claim.Face.Label))
	press("Tab_5")
	r.check("Shadow (no mythic): no BONUS pip, no ring", not pp.Header.Face.Bonus.Visible and not pp.Ring6.Visible)
	player:SetAttribute("IndexData", saved)
	task.wait(0.15)
	press("Tab_1")
	return r.text("v8cards")
end

-- v8 4: the inspect numbers (Treant found, Bramble Badger not)
function S.v8inspect()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	v8open()
	local pp = page()
	local d = data()
	d.found.Treant = {n = 3, best = 2400}
	d.found.BrambleBadger = nil
	setLocal(d)
	local list = IndexConfig.creatures(1)
	local ti, bi = 0, 0
	for k, c in list do if c.name == "Treant" then ti = k elseif c.name == "BrambleBadger" then bi = k end end
	local odds = CreatureConfig.odds("WoodEgg", 1)
	press("Tab_1") press("Card_" .. ti)
	local i = pp.Inspect
	local inc = money(CreatureConfig.income("Treant", 2400)) .. "/s"
	local V = {}
	for k = 1, 4 do table.insert(V, v8text(i["Stat" .. k].V)) end
	r.check("Treant: " .. inc .. " | 2.4K KG | x3 | " .. pctText(odds[ti]), table.concat(V, "|") == table.concat({inc, "2.4K KG", "x3", pctText(odds[ti])}, "|"), table.concat(V, "|"))
	local mult = CreatureConfig.byName.Treant.rarityMult
	r.check(("pill GRASS · $x%.1f, no SECRET / MYTHIC"):format(mult), v8text(i.Rarity.Text) == ("GRASS · $x%.1f"):format(mult) and not i.RarityEdge.Visible, v8text(i.Rarity.Text))
	r.check("Treant name + labels", v8text(i.PetName) == "TREANT" and v8text(i.Stat1.L) == "Income (best KG)" and v8text(i.Stat4.L) == "Hatch chance")
	press("Card_" .. bi)
	V = {}
	for k = 1, 4 do table.insert(V, v8text(i["Stat" .. k].V)) end
	r.check("Bramble Badger unknown: ??? | ??? | x0 | " .. pctText(odds[bi]), table.concat(V, "|") == "???|???|x0|" .. pctText(odds[bi]), table.concat(V, "|"))
	r.check("unknown: big portrait black", same(i.View.ImageColor3, Color3.new(0, 0, 0)))
	player:SetAttribute("IndexData", saved)
	task.wait(0.15)
	return r.text("v8inspect")
end

-- v8 5: the claim button states + DISCOVERED + CLAIM ALL (local)
function S.v8claimui()
	local r = report()
	local saved = player:GetAttribute("IndexData")
	v8open()
	local pp = page()
	local d = data()
	for _, c in IndexConfig.creatures(1) do d.found[c.name] = {n = 1, best = 5} end
	d.claimed["1"] = nil d.claims["1"] = nil
	setLocal(d)
	press("Tab_1")
	local n = 0
	for k in IndexConfig.AREAS do if IndexConfig.areaComplete(data(), k) and not IndexConfig.isClaimed(data(), k) then n += 1 end end
	r.check("complete: CLAIM! lime, tab ! shown", v8text(pp.Reward.Claim.Face.Label) == "CLAIM!" and same(v8top(pp.Reward.Claim), V8_LIME) and pp.Tab1.Ready.Visible)
	r.check("CLAIM ALL shown, count " .. n, pp.Total.ClaimAll.Visible and v8text(pp.Total.ClaimAll.Count.T) == tostring(n), v8text(pp.Total.ClaimAll.Count.T))
	r.check("DISCOVERED x / " .. IndexConfig.total(), v8text(pp.Total.Bar.Text) == ("DISCOVERED %d / %d"):format(IndexConfig.discovered(data()), IndexConfig.total()), v8text(pp.Total.Bar.Text))
	d.claimed["1"] = IndexConfig.version(1) d.claims["1"] = 1
	setLocal(d)
	r.check("claimed: CLAIMED! silver, star, no !", v8text(pp.Reward.Claim.Face.Label) == "CLAIMED!" and same(v8top(pp.Reward.Claim), V8_SILVER) and pp.Tab1.Star.Visible and not pp.Tab1.Ready.Visible)
	d.claimed["1"] = IndexConfig.version(1) - 1
	setLocal(d)
	r.check("older version: CLAIM AGAIN! + NEW PET! title", v8text(pp.Reward.Claim.Face.Label) == "CLAIM AGAIN!" and v8text(pp.Reward.Title):match("^NEW PET!") ~= nil, v8text(pp.Reward.Title))
	local e = data()
	for k in IndexConfig.AREAS do e.claimed[tostring(k)] = nil end
	e.found = {}
	setLocal(e)
	r.check("nothing claimable: CLAIM ALL hidden, trough takes the footer", not pp.Total.ClaimAll.Visible and pp.Total.Bar.Size.X.Scale > 0.8)
	player:SetAttribute("IndexData", saved)
	task.wait(0.15)
	return r.text("v8claimui")
end

-- v8 6: a real claim through Index.Claim, after the Server step "complete area 7" (non-mythic only):
--   local PI = require(game.ServerScriptService.PetIndex) local p = game.Players:GetPlayers()[1] local d = PI.read(p)
--   for _, c in require(game.ReplicatedStorage.IndexConfig).creatures(7) do if not c.mythic then d.found[c.name] = {n = 1, best = 5} end end
--   PI.write(p, d)
function S.v8claim()
	local r = report()
	v8open()
	local pp = page()
	press("Tab_7")
	r.check("Glacier complete without its mythic: CLAIM! lime", v8text(pp.Reward.Claim.Face.Label) == "CLAIM!" and IndexConfig.areaComplete(data(), 7) and not data().found.FrostcrownDragon)
	local b0, m0, h0 = bonus(), pot("Money"), pot("Hatch")
	press("Claim")
	local ok = waitFor(function() return IndexConfig.claimedVersion(data(), 7) == IndexConfig.version(7) end, 3)
	r.check("claimed[7] = version(7) within 3 s", ok, IndexConfig.claimedVersion(data(), 7))
	waitFor(function() return pot("Hatch") > h0 end, 2)
	r.check("IndexBonus +0.05", math.abs(bonus() - b0 - 0.05) < 1e-6, ("%.3f -> %.3f"):format(b0, bonus()))
	r.check("Potion_Money +1, Potion_Hatch +1", pot("Money") == m0 + 1 and pot("Hatch") == h0 + 1, ("%d->%d %d->%d"):format(m0, pot("Money"), h0, pot("Hatch")))
	task.wait(0.2)
	r.check("CLAIMED! silver + Glacier star", v8text(pp.Reward.Claim.Face.Label) == "CLAIMED!" and same(v8top(pp.Reward.Claim), V8_SILVER) and pp.Tab7.Star.Visible)
	local b1, m1 = bonus(), pot("Money")
	press("Claim")
	task.wait(1)
	r.check("2nd press: nothing paid", bonus() == b1 and pot("Money") == m1)
	return r.text("v8claim")
end
