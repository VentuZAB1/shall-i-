-- hatch_ris_perf.lua (2026-10-21, RIS plan 8.7 + D8): "nothing runs while closed", the cost while open, instance counts
-- and 30 open / close cycles without leaks, for the HATCH NIGHT Settings / Index / Rebirth pages. Client datamodel of a
-- TestFreshSave Play session. Load once (stores _G.RISPerf), then: _G.RISPerf("idle"), ("canvasguard"), ("cost"),
-- ("counts"), ("leaks", 10) x3, ("summary").
-- A page that is not the HATCH page yet (no attribute HatchCanvas: Index / Rebirth before runs B / C) is reported as
-- "skipped (Check-UI)". Probes (Studio only): SettingsPage SettingsRefreshN + HatchPerfSettings "<refreshes> <sum ms of
-- the last 30> <max ms of the last 30>"; IndexPage IndexRefreshN + HatchPerfIndex; RebirthPage RebirthLoop + RebirthRefreshN
-- + HatchPerfRebirth "<frames> <sum ms of 30> <max ms>" + HatchPerfRebirthRefresh "<refreshes> <sum ms of the last 30>
-- <max ms of the last 30>" (run C).
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Stats = game:GetService("Stats")
local HttpService = game:GetService("HttpService")
local p = Players.LocalPlayer
local pg = p.PlayerGui
local mm = pg.MainMenu
local body = mm.Window.Face.Body
local R = _G.RIS_PERF_RESULTS or {}
_G.RIS_PERF_RESULTS = R
local PAGES = {"Settings", "Index", "Rebirth"}
local function pageOf(name) return body:FindFirstChild(name .. "Page") end
local function hatch(name) local pp = pageOf(name) return pp and pp:GetAttribute("HatchCanvas") == true end
local function heap() return Stats:GetMemoryUsageMbForTag(Enum.DeveloperMemoryTag.LuaHeap) end
local function count(root)
	local g, n, st = 0, 0, 0
	if not root then return 0, 0, 0 end
	for _, d in root:GetDescendants() do
		n += 1
		if d:IsA("GuiObject") then g += 1 end
		if d:IsA("UIStroke") then st += 1 end
	end
	return g, n, st
end
local function closeAll()
	if mm.Window.Visible then mm.CloseWindow:Fire() end
	task.wait(0.5)
end
local function perf(name, attr)
	local pp = pageOf(name)
	local v = (pp and pp:GetAttribute(attr)) or "0 0 0"
	local n, sum, mx = tostring(v):match("^(%d+) ([%d.]+) ([%d.]+)$")
	return tonumber(n) or 0, tonumber(sum) or 0, tonumber(mx) or 0
end
local function probes()
	local t = {}
	for _, name in PAGES do
		local pp = pageOf(name)
		if hatch(name) then
			t[name] = {}
			for _, a in {"SettingsRefreshN", "HatchPerfSettings", "IndexRefreshN", "HatchPerfIndex", "RebirthRefreshN", "HatchPerfRebirth", "HatchPerfRebirthRefresh", "RebirthLoop"} do
				local v = pp:GetAttribute(a)
				if v ~= nil then t[name][a] = tostring(v) end
			end
		end
	end
	return t
end
local S = {}
function S.idle()
	closeAll()
	local a = probes()
	task.wait(3)
	local b = probes()
	local lines = {}
	for _, name in PAGES do
		if not hatch(name) then table.insert(lines, name .. ": skipped (Check-UI)") continue end
		for k, v in a[name] do
			local ok = b[name][k] == v and (k ~= "RebirthLoop" or v == "false")
			table.insert(lines, ("%s %s %s -> %s (%s)"):format(name, k, v, tostring(b[name][k]), ok and "ok" or "FAIL"))
		end
	end
	R.idle = "idle (3 s, every window closed):\n  " .. table.concat(lines, "\n  ")
	return R.idle
end
-- (perf review I-4) while ANOTHER window opens / closes, no hidden page writes its CanvasScale
function S.canvasguard()
	closeAll()
	local all = {"Settings", "Index", "Rebirth", "Shop", "Gift"}
	local function watch(skip)
		local n, conns = {}, {}
		for _, name in all do
			local pp = pageOf(name)
			local cs = pp and pp:FindFirstChild("CanvasScale")
			if cs and name ~= skip then
				n[name] = 0
				table.insert(conns, cs:GetPropertyChangedSignal("Scale"):Connect(function() n[name] += 1 end))
			end
		end
		return n, conns
	end
	local lines = {}
	for _, opener in all do
		if pageOf(opener) and (opener == "Shop" or opener == "Gift" or hatch(opener)) then
			local n, conns = watch(opener)
			for _ = 1, 3 do
				mm.OpenPage:Fire(opener)
				task.wait(0.5)
				mm.CloseWindow:Fire()
				task.wait(0.4)
			end
			for _, c in conns do c:Disconnect() end
			local parts, bad = {}, 0
			for name, c in n do table.insert(parts, name .. " " .. c) bad += c end
			table.sort(parts)
			table.insert(lines, ("%s x3: hidden-page CanvasScale writes %s (%s)"):format(opener, table.concat(parts, ", "), bad == 0 and "ok" or "FAIL"))
		end
	end
	R.canvasguard = "canvasguard:\n  " .. table.concat(lines, "\n  ")
	return R.canvasguard
end
function S.cost()
	closeAll()
	local function frames(n)
		local sum, mx = 0, 0
		for _ = 1, n do
			local dt = RunService.RenderStepped:Wait()
			sum += dt
			if dt > mx then mx = dt end
		end
		return sum / n * 1000, mx * 1000
	end
	local lines = {}
	local baseAvg, baseMax = frames(150)
	table.insert(lines, ("frame time, all closed: avg %.2f ms, max %.2f ms (150 frames; the Studio unfocused throttle shows here)"):format(baseAvg, baseMax))
	if hatch("Settings") then
		mm.OpenPage:Fire("Settings")
		task.wait(0.7)
		local pp = pageOf("Settings")
		local was = p:GetAttribute("Settings")
		local n0 = perf("Settings", "HatchPerfSettings")
		-- 20 refreshes: a local Settings change (sfx flipped back and forth) while the page is open
		for i = 1, 20 do
			local ok, d = pcall(HttpService.JSONDecode, HttpService, was or "{}")
			d = ok and d or {}
			local orig = d.sfx ~= false
			d.sfx = (i % 2 == 1) ~= orig -- odd: flipped, even: back
			p:SetAttribute("Settings", HttpService:JSONEncode(d))
			task.wait(0.05)
		end
		p:SetAttribute("Settings", was)
		task.wait(0.2)
		local n1, sum30, max30 = perf("Settings", "HatchPerfSettings")
		local openAvg, openMax = frames(150)
		-- (run A ruling) the 0.3 ms target is the average refresh (as the Shop's); the max is reported (Studio jitter)
		local avg = sum30 / math.max(1, math.min(30, n1))
		table.insert(lines, ("Settings: %d refreshes; refresh cost (last %d) avg %.4f ms (target <= 0.3 ms) %s, max %.4f ms; frame time open avg %.2f ms, max %.2f ms")
			:format(n1 - n0, math.min(30, n1), avg, (avg <= 0.3) and "ok" or "FAIL", max30, openAvg, openMax))
		closeAll()
	end
	-- (run B) Index: one tab sweep x 6 + 5 card presses while open; target avg refresh <= 2 ms (plan 8.7)
	if hatch("Index") then
		mm.OpenPage:Fire("Index")
		task.wait(0.7)
		local pp = pageOf("Index")
		local n0 = perf("Index", "HatchPerfIndex")
		for i = 1, 6 do pp.TestPress:Fire("Tab_" .. i) task.wait(0.05) end
		for i = 1, 5 do pp.TestPress:Fire("Card_" .. i) task.wait(0.05) end
		pp.TestPress:Fire("Tab_1")
		task.wait(0.2)
		local n1, sum30, max30 = perf("Index", "HatchPerfIndex")
		local openAvg, openMax = frames(150)
		local avg = sum30 / math.max(1, math.min(30, n1))
		table.insert(lines, ("Index: %d refreshes; refresh cost (last %d) avg %.4f ms (target <= 2 ms) %s, max %.4f ms; frame time open avg %.2f ms, max %.2f ms")
			:format(n1 - n0, math.min(30, n1), avg, (avg <= 2) and "ok" or "FAIL", max30, openAvg, openMax))
		closeAll()
	end
	-- (run C) Rebirth: open + READY (local Money = the cost: rays, breathing, shine all run) 300 frames -> the
	-- RenderStepped cost (target avg <= 0.05 ms); then 20 refreshes (a local PetInventory flip to the same list + a
	-- space: the other scripts decode the same pets) -> the refresh cost (target avg <= 0.3 ms)
	if hatch("Rebirth") then
		local RC = require(game:GetService("ReplicatedStorage"):WaitForChild("RebirthConfig"))
		local wasMoney, wasPets = p:GetAttribute("Money"), p:GetAttribute("PetInventory") or "[]"
		p:SetAttribute("Money", RC.cost(p:GetAttribute("Rebirths") or 0))
		mm.OpenPage:Fire("Rebirth")
		task.wait(0.8)
		local f0 = perf("Rebirth", "HatchPerfRebirth")
		for _ = 1, 300 do RunService.RenderStepped:Wait() end
		local f1, fsum30, fmax30 = perf("Rebirth", "HatchPerfRebirth")
		local n0 = perf("Rebirth", "HatchPerfRebirthRefresh")
		for i = 1, 20 do
			p:SetAttribute("PetInventory", i % 2 == 1 and wasPets .. " " or wasPets)
			task.wait(0.05)
		end
		p:SetAttribute("PetInventory", wasPets)
		task.wait(0.2)
		local n1, rsum30, rmax30 = perf("Rebirth", "HatchPerfRebirthRefresh")
		local openAvg, openMax = frames(150)
		local fAvg = fsum30 / 30
		local rAvg = rsum30 / math.max(1, math.min(30, n1))
		table.insert(lines, ("Rebirth (ready): %d frames; RenderStepped cost (last 30) avg %.4f ms (target <= 0.05 ms) %s, max %.4f ms; %d refreshes; refresh cost (last %d) avg %.4f ms (target <= 0.3 ms) %s, max %.4f ms; frame time open avg %.2f ms, max %.2f ms")
			:format(f1 - f0, fAvg, (fAvg <= 0.05) and "ok" or "FAIL", fmax30, n1 - n0, math.min(30, n1), rAvg, (rAvg <= 0.3) and "ok" or "FAIL", rmax30, openAvg, openMax))
		closeAll()
		p:SetAttribute("Money", wasMoney)
	end
	for _, name in {"Index", "Rebirth"} do
		if not hatch(name) then table.insert(lines, name .. ": skipped (Check-UI)") end
	end
	R.cost = "cost:\n  " .. table.concat(lines, "\n  ")
	return R.cost
end
function S.counts()
	local lines = {}
	for _, name in PAGES do
		local g, n, st = count(pageOf(name))
		table.insert(lines, ("%sPage%s: %d GuiObjects / %d instances / %d UIStrokes"):format(name, hatch(name) and "" or " (Check-UI)", g, n, st))
	end
	R.counts = "counts:\n  " .. table.concat(lines, "\n  ")
	return R.counts
end
local function snapshot()
	local s = {heap = heap()}
	for _, name in PAGES do local g, n = count(pageOf(name)) s[name] = {g, n} end
	local cw, cn = count(mm.Window)
	s.win = {cw, cn}
	return s
end
function S.leaks(n)
	closeAll()
	if not R.leak0 then task.wait(1) R.leak0 = snapshot() R.cycles = 0 end
	for _ = 1, n or 10 do
		for _, name in PAGES do
			if hatch(name) then
				mm.OpenPage:Fire(name)
				task.wait(0.45)
				local pp = pageOf(name)
				if name == "Index" and pp:FindFirstChild("TestPress") then
					for i = 1, 6 do pp.TestPress:Fire("Tab_" .. i) task.wait(0.05) end
					for i = 1, 5 do pp.TestPress:Fire("Card_" .. i) task.wait(0.05) end
				end
				mm.CloseWindow:Fire()
				task.wait(0.35)
			end
		end
		R.cycles += 1
	end
	task.wait(1)
	local s0, s1 = R.leak0, snapshot()
	local parts = {}
	for _, name in PAGES do
		table.insert(parts, ("%sPage %d -> %d GuiObjects, %d -> %d instances"):format(name, s0[name][1], s1[name][1], s0[name][2], s1[name][2]))
	end
	R.leaks = ("leaks after %d cycles (open / close each HATCH page): %s; Window %d -> %d instances; LuaHeap %.1f -> %.1f MB (%+.1f, limit +3)")
		:format(R.cycles, table.concat(parts, "; "), s0.win[2], s1.win[2], s0.heap, s1.heap, s1.heap - s0.heap)
	return R.leaks
end
function S.summary()
	return table.concat({R.idle or "", R.canvasguard or "", R.cost or "", R.counts or "", R.leaks or ""}, "\n")
end
_G.RISPerf = function(section, ...)
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	local ok, res = pcall(f, ...)
	return ok and res or ("ERROR in " .. section .. ": " .. tostring(res))
end
return "loaded: _G.RISPerf(section)"
