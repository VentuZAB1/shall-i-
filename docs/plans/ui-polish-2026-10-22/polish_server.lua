-- polish_server.lua (2026-10-22 UI polish): the server half. Server datamodel of a FRESH TestFreshSave Play session
-- (refuses otherwise). _G.PolishServer(step, ...) -> text.
-- Steps: arm (Shop.Buy stub for shopdry), notInGroup (true/false), pending n, x5, money n, step8, step10, step11,
-- starterOnce (StarterEndsAt set once: Rebirths change, respawn, save round trip), starter59, suites (regression), restore.
local Players = game:GetService("Players")
local SS = game:GetService("ServerStorage")
local RS = game:GetService("ReplicatedStorage")
local HttpService = game:GetService("HttpService")
assert(workspace:GetAttribute("TestFreshSave") == true, "TestFreshSave session only")
local function P() return Players:GetPlayers()[1] end
local function waitFor(fn, secs) local t0 = os.clock() while os.clock() - t0 < secs do if fn() then return true end task.wait(0.05) end return fn() end
local saved = _G.PolishSaved or {}
_G.PolishSaved = saved
local function remember(p, keys) for _, k in keys do if saved[k] == nil then saved[k] = {p:GetAttribute(k)} end end end

local S = {}

function S.notInGroup(on)
	local p = P()
	p:SetAttribute("FreeGiftTestNotInGroup", on == true or nil)
	return "FreeGiftTestNotInGroup = " .. tostring(p:GetAttribute("FreeGiftTestNotInGroup"))
end

function S.pending(n)
	local p = P()
	p:SetAttribute("OfflinePending", n)
	local ok, r = pcall(SS.OfflineDebug.Invoke, SS.OfflineDebug, p, 0)
	return ("pending %d -> OfflineDebug %s %s, OfflineReady %s"):format(n, tostring(ok), tostring(r), tostring(p:GetAttribute("OfflineReady")))
end

function S.x5()
	local p = P()
	p:SetAttribute("OfflinePending", 3000)
	pcall(SS.OfflineDebug.Invoke, SS.OfflineDebug, p, 0)
	task.wait(0.5)
	local ok, r = pcall(SS.TestReceipt.Invoke, SS.TestReceipt, p, 3718679677)
	return "TestReceipt x5: " .. tostring(ok) .. " " .. tostring(r) .. ", OfflineLastX5 " .. tostring(p:GetAttribute("OfflineLastX5"))
end

function S.money(n)
	local p = P()
	remember(p, {"Money"})
	p:SetAttribute("Money", n)
	return "Money " .. tostring(p:GetAttribute("Money"))
end

function S.step8()
	local p = P()
	remember(p, {"FreeSling", "SlingLevel", "TutorialExtra", "TutorialDone"})
	p:SetAttribute("SlingLevel", 0)
	p:SetAttribute("FreeSling", true)
	return "FreeSling true, SlingLevel 0"
end

function S.step10()
	local p = P()
	remember(p, {"FreeSling", "SlingLevel", "TutorialExtra", "Money", "Rebirths"})
	local U = require(RS:WaitForChild("UpgradeConfig"))
	p:SetAttribute("FreeSling", false)
	p:SetAttribute("SlingLevel", 1)
	p:SetAttribute("Rebirths", 0)
	p:SetAttribute("TutorialExtra", 2)
	local cost = U.KINDS.Sling.cost(2)
	p:SetAttribute("Money", cost + 10)
	return "TutorialExtra 2, SlingLevel 1, Money " .. (cost + 10)
end

function S.step11()
	local p = P()
	remember(p, {"TutorialExtra", "TutorialDone", "Rebirths", "Money", "SlingLevel"})
	p:SetAttribute("TutorialDone", true)
	p:SetAttribute("SlingLevel", 1)
	p:SetAttribute("Rebirths", 0)
	p:SetAttribute("Money", 25000)
	task.wait(0.1)
	p:SetAttribute("TutorialExtra", 3)
	task.wait(0.3)
	return "stage " .. tostring(p:GetAttribute("TutorialExtra")) .. ", Money " .. tostring(p:GetAttribute("Money"))
end

-- StarterEndsAt is set ONCE per player (StarterPackServer.startOffer: Rebirths >= 1, not owned, StarterEndsAt == 0)
function S.starterOnce()
	local p = P()
	local lines, pass, fail = {}, 0, 0
	local function check(name, ok, d) if ok then pass += 1 else fail += 1 end table.insert(lines, (ok and "ok   " or "FAIL ") .. name .. (d ~= nil and (": " .. tostring(d)) or "")) end
	remember(p, {"Rebirths"})
	local e0 = p:GetAttribute("StarterEndsAt") or 0
	if e0 == 0 then
		p:SetAttribute("Rebirths", math.max(1, p:GetAttribute("Rebirths") or 0))
		waitFor(function() return (p:GetAttribute("StarterEndsAt") or 0) > 0 end, 2)
	end
	local e1 = p:GetAttribute("StarterEndsAt") or 0
	check("offer started (StarterEndsAt set)", e1 > os.time(), e1 - os.time())
	task.wait(1.5)
	p:SetAttribute("Rebirths", (p:GetAttribute("Rebirths") or 0) + 1)
	task.wait(0.5)
	check("a later rebirth does not restart it", p:GetAttribute("StarterEndsAt") == e1, p:GetAttribute("StarterEndsAt"))
	p:LoadCharacter()
	task.wait(2)
	check("respawn keeps it", p:GetAttribute("StarterEndsAt") == e1, p:GetAttribute("StarterEndsAt"))
	local ok = pcall(SS.SavePlayerNow.Invoke, SS.SavePlayerNow, p)
	local okR, stored = pcall(SS.PlayerDataDebug.Invoke, SS.PlayerDataDebug, "read", p)
	local se = okR and type(stored) == "table" and (stored.StarterEndsAt or (stored.data and stored.data.StarterEndsAt))
	check("saved (throwaway studiotest_ key) with the same StarterEndsAt", ok and se == e1, tostring(se) .. " vs " .. e1)
	local inStudioReset = workspace:GetAttribute("TestStarterPack") == true
	table.insert(lines, "note: TestStarterPack = " .. tostring(inStudioReset) .. " (Studio only: it restarts the offer on join / when switched on, on purpose)")
	saved.StarterE1 = e1
	return ("starterOnce: %d pass / %d fail\n%s"):format(pass, fail, table.concat(lines, "\n"))
end
function S.starterCheck() -- after the client's popup / Shop sections
	local p = P()
	return "StarterEndsAt " .. tostring(p:GetAttribute("StarterEndsAt")) .. (saved.StarterE1 and (p:GetAttribute("StarterEndsAt") == saved.StarterE1 and " = unchanged" or " CHANGED") or "")
end
function S.starter59()
	local p = P()
	SS.StarterDebug:Invoke("endsAt", p, os.time() + 3540)
	return "StarterEndsAt = now + 3540"
end
function S.starterBack()
	local p = P()
	if saved.StarterE1 then SS.StarterDebug:Invoke("endsAt", p, saved.StarterE1) end
	return "StarterEndsAt " .. tostring(p:GetAttribute("StarterEndsAt"))
end

function S.suites()
	local p = P()
	local out = {}
	for _, n in {"StreakTests", "StarterPackTests", "RebirthV6Tests", "TutorialV11Tests"} do
		local m = SS:FindFirstChild(n)
		if m then
			local ok, a, b, c = pcall(function() return require(m:Clone()).live(p) end)
			if type(a) == "string" then table.insert(out, n .. ": " .. a:sub(1, 400))
			else table.insert(out, n .. ": " .. tostring(ok) .. " pass " .. tostring(a) .. " fail " .. tostring(b) .. (type(c) == "table" and (" " .. table.concat(c, " | "):sub(1, 300)) or "")) end
		end
	end
	return table.concat(out, "\n")
end

function S.restore()
	local p = P()
	for k, v in saved do if type(v) == "table" then p:SetAttribute(k, v[1]) end end
	p:SetAttribute("FreeGiftTestNotInGroup", nil)
	table.clear(saved)
	return "restored"
end

_G.PolishServer = function(step, ...)
	local fn = S[step]
	if not fn then return "no step " .. tostring(step) end
	local ok, r = pcall(fn, ...)
	return ok and tostring(r) or ("ERROR " .. tostring(r))
end
return "PolishServer ready"
