-- hatch_shop_perf.lua (2026-10-21, popup/Shop plan 7.7 + D13, review MUST 6): "nothing runs while closed", the cost while
-- open, instance counts and 30 open/close cycles without leaks. Client datamodel of a TestFreshSave Play session with the
-- Starter Pack offer running (Server: p:SetAttribute("Rebirths", 1); StarterDebug "reset" then "seen").
-- Paste once (stores _G.ShopPerf), then: _G.ShopPerf("idle"), ("cost"), ("counts"), ("leaks", 10) x3, ("summary").
-- Probes (Studio only): ShopPage HatchPerfShop "<refreshes> <sum ms of the last 30> <max ms of the last 30>", ShopLoop,
-- ShopFunnelSent, PickerConns, HatchButtons; StarterPackUI HatchPerfPopup "<frames> <sum ms of 30> <max ms of 30>",
-- RaysLoop, StarterTicker.
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Stats = game:GetService("Stats")
local p = Players.LocalPlayer
local pg = p.PlayerGui
local mm = pg.MainMenu
local page = mm.Window.Face.Body.ShopPage
local gui = pg.StarterPackUI
local R = _G.SHOP_PERF_RESULTS or {}
_G.SHOP_PERF_RESULTS = R
local function heap() return Stats:GetMemoryUsageMbForTag(Enum.DeveloperMemoryTag.LuaHeap) end
local function count(root)
	local g, n = 0, 0
	for _, d in root:GetDescendants() do n += 1 if d:IsA("GuiObject") then g += 1 end end
	return g, n
end
local function closeAll()
	if mm.Window.Visible then mm.CloseWindow:Fire() end
	gui.Enabled = false
	task.wait(0.5)
end
local function perf(attr, obj)
	local v = (obj or page):GetAttribute(attr) or "0 0 0"
	local n, sum, mx = v:match("^(%d+) ([%d.]+) ([%d.]+)$")
	return tonumber(n) or 0, tonumber(sum) or 0, tonumber(mx) or 0
end
local S = {}
function S.idle()
	closeAll()
	local a = {(perf("HatchPerfShop")), (perf("HatchPerfPopup", gui)), page:GetAttribute("ShopFunnelSent")}
	task.wait(3)
	local b = {(perf("HatchPerfShop")), (perf("HatchPerfPopup", gui)), page:GetAttribute("ShopFunnelSent")}
	local lines = {
		("Shop refresh counter %d -> %d (%s)"):format(a[1], b[1], a[1] == b[1] and "ok" or "FAIL"),
		("popup frame counter %d -> %d (%s)"):format(a[2], b[2], a[2] == b[2] and "ok" or "FAIL"),
		("ShopFunnelSent %s -> %s (%s)"):format(tostring(a[3]), tostring(b[3]), a[3] == b[3] and "ok" or "FAIL"),
		("ShopLoop %s, RaysLoop %s, StarterTicker %s (%s)"):format(tostring(page:GetAttribute("ShopLoop")), tostring(gui:GetAttribute("RaysLoop")),
			tostring(gui:GetAttribute("StarterTicker")), (page:GetAttribute("ShopLoop") == false and gui:GetAttribute("RaysLoop") == false and gui:GetAttribute("StarterTicker") == false) and "ok" or "FAIL"),
	}
	R.idle = "idle (3 s, Shop + popup closed):\n  " .. table.concat(lines, "\n  ")
	return R.idle
end
function S.cost()
	closeAll()
	-- frame time with everything closed (the baseline), then with the Shop open + tab presses, then the popup open
	local function frames(n, during)
		local sum, mx = 0, 0
		local t0 = os.clock()
		for i = 1, n do
			local dt = RunService.RenderStepped:Wait()
			sum += dt
			if dt > mx then mx = dt end
			if during then during(i) end
		end
		return sum / n * 1000, mx * 1000, os.clock() - t0
	end
	local baseAvg, baseMax = frames(300)
	mm.OpenPage:Fire("Shop")
	task.wait(0.8)
	local n0 = perf("HatchPerfShop")
	local tabs = {"Tab_SPEED", "Tab_POTIONS", "Tab_TREADMILL", "Tab_EGGS", "Tab_FEATURED"}
	local k, last = 0, os.clock()
	local shopAvg, shopMax, secs = frames(300, function()
		if os.clock() - last >= 0.5 then last = os.clock() k = k % #tabs + 1 page.TestPress:Fire(tabs[k]) end
	end)
	local n1, sum30, max30 = perf("HatchPerfShop")
	closeAll()
	gui.TestOpen:Fire()
	task.wait(0.5)
	local popAvg, popMax = frames(300)
	local f, psum, pmax = perf("HatchPerfPopup", gui)
	closeAll()
	R.cost = ("cost:\n  frame time, all closed: avg %.2f ms, max %.2f ms (300 frames)\n  Shop open + a tab press every 0.5 s: avg %.2f ms, max %.2f ms; %d refreshes in %.1f s; refresh cost (last 30) avg %.4f ms, max %.4f ms (target <= 0.3 ms)\n  popup open: avg %.2f ms, max %.2f ms; its RenderStepped work (last 30 frames) avg %.4f ms, max %.4f ms (target avg <= 0.05 ms)")
		:format(baseAvg, baseMax, shopAvg, shopMax, n1 - n0, secs, sum30 / 30, max30, popAvg, popMax, psum / 30, pmax)
	return R.cost
end
function S.counts()
	local sg, sn = count(page)
	local pgc, pn = count(gui)
	local tg = pg:FindFirstChild("GiftToast")
	local tgc, tn = count(tg)
	R.counts = ("instances: ShopPage %d GuiObjects / %d instances; StarterPackUI %d / %d; GiftToast %d / %d; H.buttons (probe) %s")
		:format(sg, sn, pgc, pn, tgc, tn, tostring(page:GetAttribute("HatchButtons")))
	return R.counts
end
local function snapshot()
	local sg, sn = count(page)
	local pgc, pn = count(gui)
	return {sg = sg, sn = sn, pg = pgc, pn = pn, btn = page:GetAttribute("HatchButtons"), conns = page:GetAttribute("PickerConns"), heap = heap()}
end
function S.leaks(n)
	workspace:SetAttribute("TestGiftSelf", true)
	closeAll()
	if not R.leak0 then task.wait(1) R.leak0 = snapshot() R.cycles = 0 end
	for _ = 1, n or 10 do
		mm.OpenPage:Fire("Shop")
		task.wait(0.5)
		for _, t in {"Tab_SPEED", "Tab_POTIONS", "Tab_TREADMILL", "Tab_EGGS", "Tab_FEATURED"} do page.TestPress:Fire(t) task.wait(0.1) end
		page.TestPress:Fire("Gift_VIP") -- (opens the picker: not a buy)
		task.wait(0.3)
		mm.CloseWindow:Fire() -- (closes the picker with the Shop)
		task.wait(0.4)
		gui.TestOpen:Fire()
		task.wait(0.3)
		gui.Enabled = false
		task.wait(0.2)
		R.cycles += 1
	end
	workspace:SetAttribute("TestGiftSelf", nil)
	task.wait(1)
	local s0, s1 = R.leak0, snapshot()
	R.leaks = ("leaks after %d cycles (Shop + 5 tabs + picker + popup): ShopPage GuiObjects %d -> %d, instances %d -> %d; StarterPackUI %d -> %d / %d -> %d; HatchButtons %s -> %s; PickerConns %s; LuaHeap %.1f -> %.1f MB (%+.1f, limit +3)")
		:format(R.cycles, s0.sg, s1.sg, s0.sn, s1.sn, s0.pg, s1.pg, s0.pn, s1.pn, tostring(s0.btn), tostring(s1.btn), tostring(s1.conns), s0.heap, s1.heap, s1.heap - s0.heap)
	return R.leaks
end
function S.summary()
	return table.concat({R.idle or "", R.cost or "", R.counts or "", R.leaks or ""}, "\n")
end
_G.ShopPerf = function(section, ...)
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	local ok, res = pcall(f, ...)
	return ok and res or ("ERROR in " .. section .. ": " .. tostring(res))
end
return "loaded: _G.ShopPerf(section)"
