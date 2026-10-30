-- hatch_uwf_perf.lua (2026-10-22, UWF plan 8.7): Free Gift / Welcome Back / Upgrades perf, Client datamodel of a
-- TestFreshSave Play session. Paste once (stores _G.UWFPerf), then _G.UWFPerf("idle") / ("leaks").
--   idle:  all three closed 3 s + 20 local Money changes -> no RaysLoop / UpgradeLoop / UpgradeMotion, every probe frozen.
--   leaks: 30 x TestOpen / TestClose per window (Upgrades + 2 dry-run Robux presses per round, TestDryRun on) ->
--          PlayerGui GuiObjects / descendants flat (+-0 after the first round), H.buttons flat, Lua heap <= +3 MB.
local p = game.Players.LocalPlayer
local pg = p.PlayerGui
local H = require(game.ReplicatedStorage.BrickUI).Hatch
local NAMES = {FreeGift = "FreeGiftUI", WelcomeBack = "OfflineUI", Upgrades = "UpgradeUI"}
local function counts()
	local g, d = 0, 0
	for _, o in pg:GetDescendants() do d += 1 if o:IsA("GuiObject") then g += 1 end end
	return g, d, #H.buttons
end
local function heapMB() return gcinfo() / 1024 end
local S = {}
function S.idle(check)
	for _, n in NAMES do local g = pg[n] if g.Enabled then g.TestClose:Fire() end end
	task.wait(0.5)
	local before = {}
	for k, n in NAMES do
		local g = pg[n]
		before[k] = {g:GetAttribute("FreeGiftRefreshN"), g:GetAttribute("HatchPerfFreeGift"), g:GetAttribute("HatchPerfWelcome"), g:GetAttribute("UpgradeRefreshN"), g:GetAttribute("HatchPerfUpgrades")}
	end
	for i = 1, 20 do p:SetAttribute("Money", (p:GetAttribute("Money") or 0) + 1) task.wait(0.05) end
	task.wait(2)
	for k, n in NAMES do
		local g = pg[n]
		local a = {g:GetAttribute("FreeGiftRefreshN"), g:GetAttribute("HatchPerfFreeGift"), g:GetAttribute("HatchPerfWelcome"), g:GetAttribute("UpgradeRefreshN"), g:GetAttribute("HatchPerfUpgrades")}
		local same = true
		for i = 1, 5 do if a[i] ~= before[k][i] then same = false end end
		check("idle " .. k .. ": every probe frozen", same)
		check("idle " .. k .. ": no loop", g:GetAttribute("RaysLoop") ~= true and g:GetAttribute("UpgradeLoop") ~= true and g:GetAttribute("UpgradeMotion") ~= true)
	end
end
function S.leaks(check, report)
	local up = pg.UpgradeUI
	up:SetAttribute("TestDryRun", true)
	for k, n in NAMES do
		local g = pg[n]
		local function round()
			if k == "WelcomeBack" then g.TestOpen:Fire(547000) else g.TestOpen:Fire() end
			task.wait(0.25)
			if k == "Upgrades" then g.TestPress:Fire("Robux_Grab") g.TestPress:Fire("Robux_Shield") task.wait(0.05) end
			g.TestClose:Fire()
			task.wait(0.1)
		end
		round()
		task.wait(0.3)
		local g0, d0, b0 = counts()
		local m0 = heapMB()
		for i = 1, 30 do round() end
		task.wait(0.6)
		local g1, d1, b1 = counts()
		local m1 = heapMB()
		table.insert(report, ("%s x30: GuiObjects %d -> %d, descendants %d -> %d, H.buttons %d -> %d, heap %.1f -> %.1f MB"):format(k, g0, g1, d0, d1, b0, b1, m0, m1))
		check(k .. " x30: GuiObjects flat", g1 == g0, g0 .. " -> " .. g1)
		check(k .. " x30: descendants flat", d1 == d0, d0 .. " -> " .. d1)
		check(k .. " x30: H.buttons flat", b1 == b0, b0 .. " -> " .. b1)
		check(k .. " x30: heap <= +3 MB", m1 - m0 <= 3, ("%.2f"):format(m1 - m0))
	end
	up:SetAttribute("TestLastBuy", nil)
end
_G.UWFPerf = function(section)
	local pass, fail, lines, report = 0, 0, {}, {}
	local function check(name, ok, detail)
		if ok then pass += 1 else fail += 1 table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end
	end
	local ok, err = pcall(S[section], check, report)
	if not ok then fail += 1 table.insert(lines, "ERROR " .. tostring(err)) end
	return ("%s: %d pass / %d fail\n%s%s"):format(section, pass, fail, table.concat(report, "\n"), #lines > 0 and ("\n" .. table.concat(lines, "\n")) or "")
end
return "UWFPerf ready"
