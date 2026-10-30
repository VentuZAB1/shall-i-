-- freegift_client.lua (2026-10-22, UWF plan 8.3 + review MUST 1 / 3 / 5): the HATCH NIGHT Free Gift window, Client
-- datamodel of a FRESH TestFreshSave Play session. _G.FreeGiftTests(section) -> "<section>: n pass / m fail" + FAIL lines.
-- Review MUST 3: every call first sets FreeGiftUI.TestDryRun = true (only joindry's negative half clears it, then puts it
-- back), so no real Join prompt can open; claim / once assert TestLastBuy unchanged. Server steps (potions, respawn) are
-- run by the builder with execute_luau (Server) between sections. Order: open, fit, walkin, hotbar, joined, notjoined,
-- joindry, refusal, lifecycle, claim, once, respawn (after the Server Health 0). Touch: section "touch" in a session with
-- workspace.TestTouchUI = true. Legacy: section "legacy" in a session with workspace.TestFreeGiftLegacy = true.
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local HttpService = game:GetService("HttpService")
local p = Players.LocalPlayer
local pg = p:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local function H()
	local B = require(game.ReplicatedStorage:WaitForChild("BrickUI"))
	return B.Hatch
end
local function gui() return pg:FindFirstChild("FreeGiftUI") end
local function near(a, b, t) return math.abs(a - b) <= t end
local function waitFor(f, secs)
	local t0 = os.clock()
	while os.clock() - t0 < secs do
		if f() then return true, os.clock() - t0 end
		task.wait(0.03)
	end
	return f(), os.clock() - t0
end
local function zone()
	local hub = workspace:FindFirstChild("Map") and workspace.Map:FindFirstChild("Hub")
	local fg = hub and hub:FindFirstChild("FreeGift")
	return fg and fg:FindFirstChild("FreeGiftZone")
end
local function hrp() return p.Character and p.Character:FindFirstChild("HumanoidRootPart") end
local function moveTo(pos)
	local c = p.Character
	if c then c:PivotTo(CFrame.new(pos)) end
end
local function away() local z = zone() if z then moveTo(z.Position + Vector3.new(0, 3, 22)) end end
local function open(g) away() task.wait(0.3) if not g.Enabled then g.TestOpen:Fire() end task.wait(0.45) end
local function close(g) if g.Enabled then g.TestClose:Fire() end task.wait(0.2) end
local function canvas(g) return g.Holder.Canvas end
local function claimBtn(g) return canvas(g).Claim end
local function claimLabel(g) return claimBtn(g).Face.Label end
local function claimTop(g)
	local gr = claimBtn(g).Face:FindFirstChildOfClass("UIGradient")
	return gr and gr.Color.Keypoints[1].Value
end
local function pal(name) return H().PAL[name].top end
local function potions()
	return (p:GetAttribute("Potion_Money") or 0), (p:GetAttribute("Potion_Hatch") or 0), (p:GetAttribute("Potion_Speed") or 0)
end
local function hotbar() local bp = pg:FindFirstChild("BackpackGui") return bp and bp.Enabled end

local S = {}
function S.open(g, check)
	open(g)
	check("Enabled", g.Enabled)
	local front = g.Holder:FindFirstChild("HatchFront")
	check("Title FREE GIFT!", front and front.Title.Text == "FREE GIFT!", front and front.Title.Text)
	local emerald = false
	for _, d in front.Crack:GetDescendants() do if d:IsA("GuiObject") and d.BackgroundColor3 == Color3.fromRGB(0, 160, 90) then emerald = true end end
	check("a tooth (0,160,90)", emerald)
	local a = g.Holder.AbsoluteSize
	check("Holder AR 560/460 +-0.01", near(a.X / a.Y, 560 / 460, 0.01), a.X / a.Y)
	local cs, ss = canvas(g).CanvasScale.Scale, front.SkinScale.Scale
	check("CanvasScale == SkinScale +-0.001", near(cs, ss, 0.001), cs .. " " .. ss)
	check("HatchCanvas", canvas(g):GetAttribute("HatchCanvas") == true)
	local n = 0 for _, c in pg:GetChildren() do if c.Name == "FreeGiftUI" then n += 1 end end
	check("exactly 1 FreeGiftUI", n == 1, n)
	local leg = p.PlayerScripts:FindFirstChild("FreeGiftClientLegacy")
	check("FreeGiftClientLegacy disabled", leg ~= nil and leg.Enabled == false)
	local touch = workspace:GetAttribute("TestTouchUI") == true or game:GetService("UserInputService").TouchEnabled
	check("Holder TextButton + HatchBlocker (mouse)", touch or (g.Holder:IsA("TextButton") and g.Holder:GetAttribute("HatchBlocker") == true), g.Holder.ClassName)
	check("no Bats", front:FindFirstChild("Bats") == nil)
end
function S.fit(g, check)
	open(g)
	local Hm = H()
	local size, pos = Hm.fitStandalone(g, mm, 560, 460)
	local a = g.Holder.AbsoluteSize
	check("Holder size = fitStandalone +-1", near(a.X, size.X.Offset, 1) and near(a.Y, size.Y.Offset, 1), ("%.1f x %.1f vs %.1f x %.1f"):format(a.X, a.Y, size.X.Offset, size.Y.Offset))
	local left = Hm.hudClear(pg, mm)
	local stroke = 3.5 * a.X / 560
	local wl = g.Holder.AbsolutePosition.X - mm.AbsolutePosition.X - stroke
	check("left >= hudClear left", wl >= left - 0.5, ("%.1f >= %.1f"):format(wl, left))
	local pe = pg:FindFirstChild("PetsEggsUI")
	local rt = pe and pe:FindFirstChild("RightTiles")
	local wr = g.Holder.AbsolutePosition.X + a.X + stroke
	check("right <= RightTiles left - 6", not rt or wr <= rt.AbsolutePosition.X - 6 + 0.5, rt and ("%.1f <= %.1f"):format(wr, rt.AbsolutePosition.X - 6))
	g:SetAttribute("HatchTestScale", 0.7261)
	task.wait(0.2)
	a = g.Holder.AbsoluteSize
	check("HatchTestScale 0.7261 -> 406.6 x 334 +-1", near(a.X, 406.6, 1) and near(a.Y, 334, 1), ("%.1f x %.1f"):format(a.X, a.Y))
	g:SetAttribute("HatchTestScale", nil)
	task.wait(0.2)
end
function S.walkin(g, check)
	close(g)
	away()
	task.wait(0.4)
	local z = zone()
	moveTo(z.Position + Vector3.new(0, 3, 0))
	local ok, t = waitFor(function() return g.Enabled end, 0.6)
	check("walk in -> open within 0.6 s", ok, ("%.2f s"):format(t))
	moveTo(z.Position + Vector3.new(0, 3, 12))
	ok, t = waitFor(function() return not g.Enabled end, 0.6)
	check("12 studs away -> closed within 0.6 s", ok, ("%.2f s"):format(t))
end
-- review MUST 1: no hotbar over the window
function S.hotbar(g, check)
	close(g)
	task.wait(0.3)
	check("hotbar shown while closed", hotbar() == true)
	open(g)
	check("hotbar hidden while open", hotbar() == false)
	close(g)
	check("hotbar back after close", waitFor(function() return hotbar() == true end, 0.5))
	-- a MainMenu window closes (MenuController re-enables the hotbar 0.15 s later) and the window opens straight after
	mm.OpenPage:Fire("Settings")
	task.wait(0.8)
	g.TestOpen:Fire() -- fires CloseWindow itself
	task.wait(0.6)
	check("still hidden after a MainMenu window closed under it", g.Enabled and hotbar() == false, tostring(g.Enabled) .. " " .. tostring(hotbar()))
	close(g)
	check("back after that close", waitFor(function() return hotbar() == true end, 0.5))
	-- walking away closes it: the hotbar comes back
	local z = zone()
	moveTo(z.Position + Vector3.new(0, 3, 0))
	waitFor(function() return g.Enabled end, 0.8)
	local hid = hotbar() == false
	away()
	local ok = waitFor(function() return not g.Enabled end, 0.8)
	check("walk-in hides it, walk-away shows it", hid and ok and waitFor(function() return hotbar() == true end, 0.5))
end
function S.joined(g, check)
	g:SetAttribute("TestJoined", nil)
	open(g)
	local w = canvas(g).Group.Face.Well
	check("Joined + Done visible", w.Joined.Visible and w.Done.Visible)
	check("Join hidden", not w.Join.Visible)
	check("CLAIM lime", claimTop(g) == pal("lime"), tostring(claimTop(g)))
	check("RaysLoop true", g:GetAttribute("RaysLoop") == true)
	local sc = claimBtn(g).ButtonScale
	local a = sc.Scale
	task.wait(0.6)
	check("CLAIM breathes (ButtonScale changes over 0.6 s)", sc.Scale ~= a, a .. " -> " .. sc.Scale)
end
function S.notjoined(g, check)
	open(g)
	g:SetAttribute("TestJoined", false)
	task.wait(0.1)
	local w = canvas(g).Group.Face.Well
	check("Join visible", w.Join.Visible)
	check("Joined hidden", not w.Joined.Visible)
	check("CLAIM palette off", claimTop(g) == pal("off"), tostring(claimTop(g)))
	check("label CLAIM!", claimLabel(g).Text == "CLAIM!", claimLabel(g).Text)
	g:SetAttribute("TestJoined", nil)
end
function S.joindry(g, check)
	open(g)
	g:SetAttribute("TestLastBuy", nil)
	g.TestPress:Fire("Join")
	task.wait(0.2)
	local want = HttpService:JSONEncode({"PromptJoinAsync", g.Parent and game.ReplicatedStorage.FreeGift:GetAttribute("GroupId") or 342252480})
	check("dry run: TestLastBuy = PromptJoinAsync, GROUP_ID", g:GetAttribute("TestLastBuy") == want, g:GetAttribute("TestLastBuy"))
	g:SetAttribute("TestLastBuy", nil)
	g:SetAttribute("TestDryRun", false)
	g.TestPress:Fire("Join") -- refused + warn: no prompt
	task.wait(0.3)
	g:SetAttribute("TestDryRun", true)
	check("TestDryRun off: TestPress Join refused (TestLastBuy unchanged)", g:GetAttribute("TestLastBuy") == nil, g:GetAttribute("TestLastBuy"))
end
function S.refusal(g, check)
	open(g)
	g:SetAttribute("TestLastBuy", nil)
	local card = canvas(g).Group
	local base = card.Position
	g:SetAttribute("TestClaimFail", "group")
	g.TestPress:Fire("Claim")
	local moved = waitFor(function() return card.Position ~= base end, 0.25)
	local ok = waitFor(function() local t = claimLabel(g).Text return t == "JOIN THE GROUP FIRST!" or t == "JOIN FIRST!" end, 0.5)
	check("group: CLAIM red JOIN THE GROUP FIRST! / JOIN FIRST! within 0.5 s", ok and claimTop(g) == pal("red"), claimLabel(g).Text)
	check("group: the Group card shakes within 0.25 s", moved)
	task.wait(0.4)
	local want = HttpService:JSONEncode({"PromptJoinAsync", game.ReplicatedStorage.FreeGift:GetAttribute("GroupId") or 342252480})
	check("group: auto-join is a dry run (TestLastBuy)", g:GetAttribute("TestLastBuy") == want, g:GetAttribute("TestLastBuy"))
	ok = waitFor(function() return claimLabel(g).Text == "CLAIM!" end, 2.1)
	check("group: back to CLAIM! after ~2 s", ok, claimLabel(g).Text)
	check("FreeGift still false", p:GetAttribute("FreeGift") ~= true)
	g:SetAttribute("TestClaimFail", "wait")
	g.TestPress:Fire("Claim")
	ok = waitFor(function() local t = claimLabel(g).Text return t == "LOADING... TRY AGAIN!" or t == "TRY AGAIN" end, 0.5)
	check("wait: LOADING... TRY AGAIN! / TRY AGAIN", ok, claimLabel(g).Text)
	waitFor(function() return claimLabel(g).Text == "CLAIM!" end, 1.6)
end
function S.lifecycle(g, check)
	open(g)
	task.wait(1.2)
	close(g)
	local ok = waitFor(function() return g:GetAttribute("RaysLoop") == false end, 0.3)
	check("close -> RaysLoop false within 0.3 s", ok)
	local a, r = g:GetAttribute("HatchPerfFreeGift"), g:GetAttribute("FreeGiftRefreshN")
	task.wait(2)
	check("HatchPerfFreeGift frozen 2 s", g:GetAttribute("HatchPerfFreeGift") == a, tostring(a))
	check("FreeGiftRefreshN frozen while closed", g:GetAttribute("FreeGiftRefreshN") == r, tostring(r))
end
function S.claim(g, check)
	open(g)
	g:SetAttribute("TestLastBuy", nil)
	local m0, h0, s0 = potions()
	g.TestPress:Fire("Claim")
	local ok = waitFor(function() return p:GetAttribute("FreeGift") == true end, 3)
	check("FreeGift true within 3 s", ok)
	task.wait(0.6)
	local m1, h1, s1 = potions()
	check("Money potion +1", m1 == m0 + 1, m0 .. " -> " .. m1)
	check("Hatch potion +1", h1 == h0 + 1, h0 .. " -> " .. h1)
	check("Speed potion +1", s1 == s0 + 1, s0 .. " -> " .. s1)
	check("CLAIM silver CLAIMED!", claimTop(g) == pal("silver") and claimLabel(g).Text == "CLAIMED!", claimLabel(g).Text)
	check("CLAIM face Active false", claimBtn(g).Face.Active == false)
	local z = zone()
	local sign = z and z:FindFirstChild("SignAnchor") and z.SignAnchor:FindFirstChild("FreeSign")
	local sp = z and z:FindFirstChild("Sparkles")
	local em = sp and sp:FindFirstChildOfClass("ParticleEmitter")
	check("FreeSign.Enabled false", sign ~= nil and sign.Enabled == false)
	check("Sparkles off", em ~= nil and em.Enabled == false)
	check("no join attempted (TestLastBuy unchanged)", g:GetAttribute("TestLastBuy") == nil, g:GetAttribute("TestLastBuy"))
end
function S.once(g, check)
	open(g)
	g:SetAttribute("TestLastBuy", nil)
	local calls = g:GetAttribute("FreeGiftClaimCalls")
	local m0, h0, s0 = potions()
	g.TestPress:Fire("Claim")
	task.wait(1.5)
	local m1, h1, s1 = potions()
	check("FreeGiftClaimCalls unchanged", g:GetAttribute("FreeGiftClaimCalls") == calls, tostring(calls))
	check("potions unchanged after 1.5 s", m1 == m0 and h1 == h0 and s1 == s0)
	close(g)
	local z = zone()
	away()
	task.wait(0.4)
	moveTo(z.Position + Vector3.new(0, 3, 0))
	task.wait(0.8)
	check("walk in after the claim: stays closed", not g.Enabled)
	away()
	check("no join attempted (TestLastBuy unchanged)", g:GetAttribute("TestLastBuy") == nil)
end
function S.respawn(g, check)
	local n = 0 for _, c in pg:GetChildren() do if c.Name == "FreeGiftUI" then n += 1 end end
	check("after respawn: exactly 1 FreeGiftUI", n == 1, n)
	g.TestOpen:Fire()
	task.wait(0.45)
	check("after respawn: TestOpen works", g.Enabled)
	check("after respawn: hotbar hidden while open", hotbar() == false)
	close(g)
	check("after respawn: hotbar back", waitFor(function() return hotbar() == true end, 0.5))
end
-- review MUST 5 (a session with workspace.TestTouchUI = true): the window doesn't sink touches, you can walk off the pad
function S.touch(g, check)
	check("TestTouchUI session", workspace:GetAttribute("TestTouchUI") == true)
	check("Holder is a plain Frame, Active false", g.Holder.ClassName == "Frame" and g.Holder.Active == false, g.Holder.ClassName)
	local z = zone()
	moveTo(z.Position + Vector3.new(0, 3, 0))
	waitFor(function() return g.Enabled end, 0.8)
	task.wait(0.4)
	-- the thumbstick zone (bottom-left of the screen) and the window's own background: no FreeGiftUI object takes input
	local hp, hs = g.Holder.AbsolutePosition, g.Holder.AbsoluteSize
	local pts = {Vector2.new(hp.X + hs.X * 0.25, hp.Y + hs.Y * 0.62), Vector2.new(hp.X + hs.X * 0.5, hp.Y + hs.Y * 0.45), Vector2.new(hp.X + 20, hp.Y + hs.Y - 20)}
	local sink = nil
	for _, pt in pts do
		for _, o in pg:GetGuiObjectsAtPosition(pt.X, pt.Y) do
			if o:IsDescendantOf(g) and (o:IsA("GuiButton") or o.Active) and not o:IsDescendantOf(g.Holder.Canvas.Claim) and not o:IsDescendantOf(g.Holder.Canvas.Group) then
				sink = o:GetFullName()
			end
		end
	end
	check("no FreeGiftUI object sinks input at the window background", sink == nil, sink)
	check("open on the pad", g.Enabled)
	-- walk off with the window open (the thumbstick's Humanoid:Move)
	local hum = p.Character:FindFirstChildOfClass("Humanoid")
	local t0 = os.clock()
	while g.Enabled and os.clock() - t0 < 4 do
		hum:Move(Vector3.new(0, 0, 1), false)
		task.wait(0.05)
	end
	hum:Move(Vector3.zero, false)
	check("walked off the pad with the window open: closed", not g.Enabled, ("%.2f s"):format(os.clock() - t0))
end
function S.legacy(g, check)
	local leg = p.PlayerScripts:FindFirstChild("FreeGiftClientLegacy")
	check("legacy: FreeGiftClientLegacy enabled", leg ~= nil and leg.Enabled == true)
	local n = 0 for _, c in pg:GetChildren() do if c.Name == "FreeGiftUI" then n += 1 end end
	check("legacy: exactly 1 FreeGiftUI", n == 1, n)
	check("legacy: Holder.Window (Check-UI), no HatchBack", g.Holder:FindFirstChild("Window") ~= nil and g.Holder:FindFirstChild("HatchBack") == nil)
end

_G.FreeGiftTests = function(section)
	local g = gui()
	if not g then return section .. ": 0 pass / 1 fail\nFAIL no FreeGiftUI" end
	if section ~= "legacy" then g:SetAttribute("TestDryRun", true) end -- review MUST 3
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
return "FreeGiftTests ready"
