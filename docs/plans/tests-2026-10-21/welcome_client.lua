-- welcome_client.lua (2026-10-22, UWF plan 8.4 + review MUST 2 / SHOULD 4 / 5): the HATCH NIGHT Welcome Back window, Client
-- datamodel of a FRESH TestFreshSave Play session. _G.WelcomeTests(section, n) -> "<section>: n pass / m fail" + FAIL lines.
-- Every call first sets OfflineUI.TestDryRun = true (only x5dry's negative half clears it, then puts it back): no real
-- Robux prompt can open. Server steps by the builder (execute_luau Server) before the client part:
--   pending n:  p:SetAttribute("OfflinePending", n); game.ServerStorage.OfflineDebug:Invoke(p, 0)
--   receipt:    game.ServerStorage.TestReceipt:Invoke(p, 3718679677)
-- Sections: open (after "pending 547000"), claim, close (after "pending 1000"), other (after "pending 2000"), x5dry (after
-- "pending 3000"), x5receipt (after "pending 10000", then the builder fires the receipt within 3 s), x5after, none, lifecycle,
-- base (the frozen $X/Day line), legacy (own session, workspace.TestWelcomeLegacy = true). Money = player attribute Money.
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
local function money() return p:GetAttribute("Money") or 0 end
local function canvas(g) return g.Holder.Canvas end
local function count(name) local n = 0 for _, c in pg:GetChildren() do if c.Name == name then n += 1 end end return n end
local function x5Top(g)
	local gr = canvas(g).ClaimX5.Face:FindFirstChildOfClass("UIGradient")
	return gr and gr.Color.Keypoints[1].Value
end
local function hotbar() local bp = pg:FindFirstChild("BackpackGui") return bp and bp.Enabled end

local S = {}
function S.open(g, check)
	local ok = waitFor(function() return g.Enabled end, 3.5)
	check("pending -> open within 3.5 s", ok)
	task.wait(0.45)
	local front = g.Holder:FindFirstChild("HatchFront")
	check("Title WELCOME BACK!", front and front.Title.Text == "WELCOME BACK!", front and front.Title.Text)
	local gold = false
	for _, d in front.Crack:GetDescendants() do if d:IsA("GuiObject") and d.BackgroundColor3 == Color3.fromRGB(255, 168, 0) then gold = true end end
	check("a tooth (255,168,0)", gold or workspace:GetAttribute("HatchBand") ~= nil)
	check("Amount $547K", canvas(g).Amount.Text == "$547K", canvas(g).Amount.Text)
	local f = canvas(g).ClaimX5.Face
	check("Price = live / fallback", f.Price.Visible and tonumber(f.Price.Text) ~= nil, f.Price.Text)
	check("Pre CLAIM x5!", f.Pre.Text == "CLAIM x5!", f.Pre.Text)
	local a = g.Holder.AbsoluteSize
	check("AR 540/430 +-0.01", near(a.X / a.Y, 540 / 430, 0.01), a.X / a.Y)
	check("CanvasScale == SkinScale", near(canvas(g).CanvasScale.Scale, front.SkinScale.Scale, 0.001))
	check("HatchCanvas", canvas(g):GetAttribute("HatchCanvas") == true)
	local leg = p.PlayerScripts:FindFirstChild("OfflineClientLegacy")
	check("OfflineClientLegacy disabled", leg ~= nil and leg.Enabled == false)
	check("exactly 1 OfflineUI + 1 OfflineBaseUI", count("OfflineUI") == 1 and count("OfflineBaseUI") == 1, count("OfflineUI") .. " " .. count("OfflineBaseUI"))
	local base = pg:FindFirstChild("OfflineBaseUI")
	check("OfflineBaseUI.PerDay exists (MUST 2)", base and base:FindFirstChild("PerDay") ~= nil)
	check("hotbar hidden while open (MUST 1)", hotbar() == false)
end
function S.claim(g, check)
	g:SetAttribute("_m0", money())
	g.TestPress:Fire("Claim")
	local ok = waitFor(function() return not g.Enabled end, 1.2)
	check("claimed -> closed within 1.2 s", ok)
	check("hotbar back", waitFor(function() return hotbar() == true end, 0.6))
end
S.close = S.claim
function S.other(g, check)
	waitFor(function() return g.Enabled end, 3.5)
	task.wait(0.5)
	g:SetAttribute("_m0", money())
	mm.OpenPage:Fire("Shop")
	local ok = waitFor(function() return not g.Enabled end, 2)
	check("another window: OfflineUI closed", ok)
	check("Shop open", waitFor(function() return mm.Window.Visible end, 1))
	task.wait(0.5)
	mm.CloseWindow:Fire()
	task.wait(0.4)
end
function S.x5dry(g, check)
	waitFor(function() return g.Enabled end, 3.5)
	task.wait(0.5)
	g:SetAttribute("TestLastBuy", nil)
	g:SetAttribute("TestDryRunResult", "Test save only")
	g.TestPress:Fire("ClaimX5")
	task.wait(0.15)
	check("dry: TestLastBuy = PromptProductPurchase 3718679677", g:GetAttribute("TestLastBuy") == HttpService:JSONEncode({"PromptProductPurchase", 3718679677}), g:GetAttribute("TestLastBuy"))
	local w = canvas(g).ClaimX5.Face.Word
	check("dry: red TEST SAVE ONLY", w.Visible and (w.Text == "TEST SAVE ONLY" or w.Text == "TRY AGAIN"), w.Text)
	check("dry: price back after 1.5 s", waitFor(function() return canvas(g).ClaimX5.Face.Price.Visible end, 1.7))
	check("dry: WelcomePrompting false (SHOULD 4)", g:GetAttribute("WelcomePrompting") ~= true)
	g:SetAttribute("TestDryRunResult", nil)
	g:SetAttribute("TestLastBuy", nil)
	g:SetAttribute("TestDryRun", false)
	g.TestPress:Fire("ClaimX5")
	task.wait(0.3)
	g:SetAttribute("TestDryRun", true)
	check("TestDryRun off: ClaimX5 refused (TestLastBuy unchanged)", g:GetAttribute("TestLastBuy") == nil)
	check("window still open", g.Enabled)
	S.claim(g, check)
end
-- after "pending 10000": the builder fires TestReceipt on the Server; this waits for the celebration
function S.x5receipt(g, check)
	waitFor(function() return g.Enabled end, 3.5)
	local ok = waitFor(function() return canvas(g).Amount.Text == "$50K" end, 6)
	check("x5: Amount $50K", ok, canvas(g).Amount.Text)
	local shards = waitFor(function() return #canvas(g).Fx:GetChildren() > 0 end, 0.5)
	check("x5: shards seen", shards)
	check("x5: OfflineLastX5 true", p:GetAttribute("OfflineLastX5") == true)
	check("x5: closed within 2.5 s", waitFor(function() return not g.Enabled end, 2.5))
end
function S.none(g, check)
	local ok = waitFor(function() return g.Enabled end, 4)
	check("pending 0 / not ready: no window in 4 s", not ok)
end
function S.lifecycle(g, check)
	if g.Enabled then g.TestClose:Fire() task.wait(0.3) end
	g.TestOpen:Fire(547000)
	task.wait(1.2)
	g.TestClose:Fire()
	local ok = waitFor(function() return g:GetAttribute("RaysLoop") == false end, 0.3)
	check("closed: RaysLoop false", ok)
	local a = g:GetAttribute("HatchPerfWelcome")
	task.wait(2)
	check("HatchPerfWelcome frozen 2 s", g:GetAttribute("HatchPerfWelcome") == a, tostring(a))
end
-- review MUST 2: the frozen "$X/Day" base line still works (stand on your own base)
function S.base(g, check)
	local id = p:GetAttribute("BaseId")
	local hub = workspace:FindFirstChild("Map") and workspace.Map:FindFirstChild("Hub")
	local base = id and hub and hub:FindFirstChild("Bases") and hub.Bases:FindFirstChild("Base" .. id)
	local floor = base and base:FindFirstChild("Plot") and base.Plot:FindFirstChild("Floor")
	check("own base floor found", floor ~= nil, id)
	if not floor then return end
	p.Character:PivotTo(floor.CFrame + Vector3.new(0, 4, 0))
	local line = pg.OfflineBaseUI.PerDay
	local ok = waitFor(function() return line.TextTransparency < 0.05 and line.Text:find("/Day offline!") ~= nil end, 2)
	check("PerDay shows 'You earn $X/Day offline!' on the base", ok, line.Text)
	return line.Text
end
function S.legacy(g, check)
	local leg = p.PlayerScripts:FindFirstChild("OfflineClientLegacy")
	check("legacy: OfflineClientLegacy enabled", leg ~= nil and leg.Enabled == true)
	check("legacy: 1 OfflineUI + 1 OfflineBaseUI", count("OfflineUI") == 1 and count("OfflineBaseUI") == 1, count("OfflineUI") .. " " .. count("OfflineBaseUI"))
	check("legacy: Check-UI Holder.Window, no HatchBack", g.Holder:FindFirstChild("Window") ~= nil and g.Holder:FindFirstChild("HatchBack") == nil)
end

_G.WelcomeTests = function(section)
	local g = pg:FindFirstChild("OfflineUI")
	if not g then return section .. ": 0 pass / 1 fail\nFAIL no OfflineUI" end
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
return "WelcomeTests ready"
