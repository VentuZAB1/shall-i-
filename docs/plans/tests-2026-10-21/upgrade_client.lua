-- upgrade_client.lua (2026-10-22, UWF plan 8.5 + review MUST 1 / 6, SHOULD 3): the HATCH NIGHT Upgrades window, Client
-- datamodel of a FRESH TestFreshSave Play session. _G.UpgradeTests(section) -> "<section>: n pass / m fail" + FAIL lines.
-- Every call first sets UpgradeUI.TestDryRun = true (only robuxdry's negative half clears it, then puts it back): no Robux
-- prompt can open. Server steps by the builder: Money (p:SetAttribute("Money", n)), receipts
-- (game.ServerStorage.TestReceipt:Invoke(p, ShopConfig.upgradeProduct(kind, level + 1).id)).
-- Sections: open, walkin, hotbar, buy (after the server gave Money), robuxdry, states (local attributes), step8, step10,
-- lifecycle, legacy (own session, workspace.TestUpgradesLegacy = true).
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local p = Players.LocalPlayer
local pg = p:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local function near(a, b, t) return math.abs(a - b) <= t end
local function waitFor(f, secs)
	local t0 = os.clock()
	while os.clock() - t0 < secs do
		if f() then return true, os.clock() - t0 end
		task.wait(0.03)
	end
	return f(), os.clock() - t0
end
local function H() return require(game.ReplicatedStorage.BrickUI).Hatch end
local function zone()
	local st = workspace:FindFirstChild("Map") and workspace.Map:FindFirstChild("Hub") and workspace.Map.Hub:FindFirstChild("Stalls")
	return st and st:FindFirstChild("UpgradeZone", true)
end
local function moveTo(pos) if p.Character then p.Character:PivotTo(CFrame.new(pos)) end end
local function away() local z = zone() if z then moveTo(z.Position + Vector3.new(0, 3, 24)) end end
local function open(g) if not g.Enabled then g.TestOpen:Fire() end task.wait(0.45) end
local function close(g) if g.Enabled then g.TestClose:Fire() end task.wait(0.2) end
local function row(g, kind) return g.Holder.Canvas["Row_" .. kind].Face end
local function top(btnHolder)
	local gr = btnHolder.Face:FindFirstChildOfClass("UIGradient")
	return gr and gr.Color.Keypoints[1].Value
end
local function pal(n) return H().PAL[n].top end
local function hotbar() local bp = pg:FindFirstChild("BackpackGui") return bp and bp.Enabled end
local function setLocal(t) for k, v in t do p:SetAttribute(k, v) end task.wait(0.15) end

local S = {}
function S.open(g, check)
	open(g)
	check("Enabled", g.Enabled)
	local front = g.Holder.HatchFront
	check("Title UPGRADES", front.Title.Text == "UPGRADES", front.Title.Text)
	local blue = false
	for _, d in front.Crack:GetDescendants() do if d:IsA("GuiObject") and d.BackgroundColor3 == Color3.fromRGB(30, 60, 220) then blue = true end end
	check("a tooth (30,60,220)", blue)
	check("RebirthPill REBIRTH n", front.RebirthPill.Label.Text:find("^REBIRTH %d+$") ~= nil, front.RebirthPill.Label.Text)
	local a = g.Holder.AbsoluteSize
	check("AR 740/470", near(a.X / a.Y, 740 / 470, 0.01), a.X / a.Y)
	check("CanvasScale == SkinScale", near(g.Holder.Canvas.CanvasScale.Scale, front.SkinScale.Scale, 0.001))
	check("3 rows", row(g, "Sling") and row(g, "Grab") and row(g, "Shield") and true)
	check("UpgradeClientLegacy disabled", p.PlayerScripts.UpgradeClientLegacy.Enabled == false)
	local n = 0 for _, c in pg:GetChildren() do if c.Name == "UpgradeUI" then n += 1 end end
	check("exactly 1 UpgradeUI + ShieldToast", n == 1 and pg:FindFirstChild("ShieldToast") ~= nil, n)
	check("hotbar hidden (MUST 1)", hotbar() == false)
	check("UpgradeLoop true", g:GetAttribute("UpgradeLoop") == true)
end
function S.walkin(g, check)
	close(g) away() task.wait(0.4)
	local z = zone()
	moveTo(z.Position + Vector3.new(0, 3, 0))
	check("walk in -> open within 0.6 s", waitFor(function() return g.Enabled end, 0.6))
	check("hotbar hidden", waitFor(function() return hotbar() == false end, 0.3))
	away()
	check("walk out -> closed within 0.6 s", waitFor(function() return not g.Enabled end, 0.6))
	check("hotbar back", waitFor(function() return hotbar() == true end, 0.5))
end
-- after the server set Money (the test's Money attribute): a real $ buy of Slingshot Power
function S.buy(g, check)
	open(g)
	local lv = p:GetAttribute("SlingLevel") or 0
	local m0 = p:GetAttribute("Money") or 0
	check("Sling $ button lime (affordable)", top(row(g, "Sling").Buy) == pal("lime"), tostring(top(row(g, "Sling").Buy)))
	g.TestPress:Fire("Buy_Sling")
	check("SlingLevel +1", waitFor(function() return (p:GetAttribute("SlingLevel") or 0) == lv + 1 end, 2), p:GetAttribute("SlingLevel"))
	check("Money spent", waitFor(function() return (p:GetAttribute("Money") or 0) < m0 end, 1))
	task.wait(0.3)
	check("bar shows the new level", row(g, "Sling").Bar.Text.Text == ("LV %d/%d"):format(lv + 1, 25), row(g, "Sling").Bar.Text.Text)
end
function S.robuxdry(g, check)
	open(g)
	g:SetAttribute("TestLastBuy", nil)
	g.TestPress:Fire("Robux_Grab")
	task.wait(0.2)
	check("dry: TestLastBuy = Upgrades.Buy Grab robux", g:GetAttribute("TestLastBuy") == HttpService:JSONEncode({"Upgrades.Buy", "Grab", "robux"}), g:GetAttribute("TestLastBuy"))
	g:SetAttribute("TestDryRunResult", "Test save only")
	g.TestPress:Fire("Robux_Shield")
	task.wait(0.2)
	local w = row(g, "Shield").Robux.Face.Word
	check("dry refusal: red word on +1 LV", w.Visible and (w.Text == "TEST SAVE ONLY" or w.Text == "TEST!"), w.Text)
	g:SetAttribute("TestDryRunResult", nil)
	check("price back after 1.2 s", waitFor(function() return row(g, "Shield").Robux.Face.Price.Visible end, 2))
	g:SetAttribute("TestLastBuy", nil)
	g:SetAttribute("TestDryRun", false)
	g.TestPress:Fire("Robux_Grab")
	task.wait(0.3)
	g:SetAttribute("TestDryRun", true)
	check("TestDryRun off: refused (TestLastBuy unchanged)", g:GetAttribute("TestLastBuy") == nil)
end
-- local attribute states (UI only): locked / can't afford / MAX
function S.states(g, check)
	open(g)
	local save = {}
	for _, k in {"Money", "Rebirths", "SlingLevel", "GrabLevel", "ShieldLevel"} do save[k] = p:GetAttribute(k) end
	setLocal({Money = 0, Rebirths = 0, SlingLevel = 3, GrabLevel = 0})
	check("can't afford: off", top(row(g, "Sling").Buy) == pal("off"), tostring(top(row(g, "Sling").Buy)))
	setLocal({SlingLevel = 24, Rebirths = 0, Money = 1e15})
	local pr = row(g, "Sling").Buy.Face.Price
	check("locked: off + REBIRTH n + lock glyph", top(row(g, "Sling").Buy) == pal("off") and pr.Text:find("^REBIRTH") ~= nil and row(g, "Sling").Buy.Face.Robux.Image == H().ICON.lock, pr.Text)
	setLocal({SlingLevel = 25, GrabLevel = 5, ShieldLevel = 1})
	local w = row(g, "Sling").Buy.Face.Word
	check("MAX: silver word, Robux hidden", w.Visible and w.Text == "MAX" and not row(g, "Sling").Robux.Visible, w.Text)
	check("MAX stat gold, no arrow", not row(g, "Sling").Stat.Next.Visible)
	setLocal(save)
end
function S.step8(g, check)
	open(g)
	local save = {FreeSling = p:GetAttribute("FreeSling"), SlingLevel = p:GetAttribute("SlingLevel")}
	setLocal({FreeSling = true, SlingLevel = 0})
	local f = row(g, "Sling")
	check("FREE!: lime word", f.Buy.Face.Word.Visible and f.Buy.Face.Word.Text == "FREE!" and top(f.Buy) == pal("lime"), f.Buy.Face.Word.Text)
	check("FREE: Robux hidden", not f.Robux.Visible)
	check("FREE: arrow visible + UpgradeMotion", f.FreeArrow.Visible and g:GetAttribute("UpgradeMotion") == true)
	local a = f.Buy.ButtonScale.Scale
	task.wait(0.5)
	check("FREE: the button breathes", f.Buy.ButtonScale.Scale ~= a)
	setLocal(save)
	check("after FREE: arrow gone, motion off", waitFor(function() return not f.FreeArrow.Visible and g:GetAttribute("UpgradeMotion") == false end, 0.5))
end
function S.step10(g, check)
	open(g)
	local save = {TutorialExtra = p:GetAttribute("TutorialExtra"), Money = p:GetAttribute("Money"), SlingLevel = p:GetAttribute("SlingLevel"), Rebirths = p:GetAttribute("Rebirths")}
	setLocal({TutorialExtra = 2, Money = 1e6, SlingLevel = 1, Rebirths = 0})
	local f = row(g, "Sling")
	check("step 10: arrow visible", f.FreeArrow.Visible)
	check("step 10: Sling +1 LV hidden (HIDE_ROBUX_IN_TUTORIAL)", not f.Robux.Visible)
	check("step 10: Grab +1 LV still shown", row(g, "Grab").Robux.Visible)
	check("step 10: lime price", top(f.Buy) == pal("lime") and f.Buy.Face.Price.Visible)
	setLocal(save)
	check("after step 10: +1 LV back", waitFor(function() return f.Robux.Visible end, 0.5))
end
function S.lifecycle(g, check)
	open(g)
	task.wait(0.6)
	close(g)
	check("closed: UpgradeLoop false", waitFor(function() return g:GetAttribute("UpgradeLoop") == false end, 0.8))
	check("closed: UpgradeMotion false", g:GetAttribute("UpgradeMotion") ~= true)
	local n = g:GetAttribute("UpgradeRefreshN")
	for i = 1, 20 do p:SetAttribute("Money", (p:GetAttribute("Money") or 0) + 1) end
	task.wait(1.5)
	check("closed: 20 Money changes -> UpgradeRefreshN frozen", g:GetAttribute("UpgradeRefreshN") == n, tostring(n))
end
function S.legacy(g, check)
	check("legacy: UpgradeClientLegacy enabled", p.PlayerScripts.UpgradeClientLegacy.Enabled == true)
	check("legacy: Check-UI Root, no HatchBack", g:FindFirstChild("Root") ~= nil and g:FindFirstChild("Holder") == nil)
end

_G.UpgradeTests = function(section)
	local g = pg:FindFirstChild("UpgradeUI")
	if not g then return section .. ": 0 pass / 1 fail\nFAIL no UpgradeUI" end
	if section ~= "legacy" then g:SetAttribute("TestDryRun", true) end
	local pass, fail, lines = 0, 0, {}
	local function check(name, cond, detail)
		if cond then pass += 1 else fail += 1 table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end
	end
	local f = S[section]
	if not f then return "no section " .. tostring(section) end
	local ok, err = pcall(f, g, check)
	if not ok then fail += 1 table.insert(lines, "ERROR " .. tostring(err)) end
	return ("%s: %d pass / %d fail%s"):format(section, pass, fail, #lines > 0 and ("\n" .. table.concat(lines, "\n")) or "")
end
return "UpgradeTests ready"
