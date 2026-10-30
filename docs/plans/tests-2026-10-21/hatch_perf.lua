-- hatch_perf.lua (2026-10-21, the owner's lag check on the HATCH NIGHT Gift window). Client datamodel, TestFreshSave Play.
-- Reads the Studio-only perf probes the scripts publish (every 30 working frames):
--   GiftPage.HatchPerfDaily (StreakClient), GiftPage.HatchPerfPlay (PlaytimeClient), HatchFront.HatchPerfBats (bat loop)
--   = "<total frames that did work> <sum ms of the last 30> <max ms of the last 30>";  HatchFront.BatLoop = connected?
-- 1 idle: window closed for 3 s -> the work counters must not move, BatLoop false
-- 2 cost: DAILY open ~300 frames, then PLAYTIME ~300 frames -> avg / max ms per frame per loop
-- 3 instances: GuiObjects / ViewportFrames / all instances the window built (+ StreakCelebrate, StreakFly)
-- 4 leaks: open / close + tab switch x30 -> instance counts, Lua heap and total memory before / after
local p = game.Players.LocalPlayer
local pg = p.PlayerGui
local mm = pg.MainMenu
local win = mm.Window
local page = win.Face.Body.GiftPage
local front = win.HatchFront
local Stats = game:GetService("Stats")
local RunService = game:GetService("RunService")
local out = {}
local function counters()
	local function n(o, a) local v = o:GetAttribute(a) return v and tonumber(v:match("^(%d+)")) or 0 end
	return {daily = n(page, "HatchPerfDaily"), play = n(page, "HatchPerfPlay"), bats = n(front, "HatchPerfBats")}
end
local function frames(k) for _ = 1, k do RunService.RenderStepped:Wait() end end
-- collect ~n frames of one probe: aggregate the 30-frame windows it publishes
local function sample(o, attr, windows)
	local sum, max, nfr, last = 0, 0, 0, o:GetAttribute(attr)
	local got = 0
	local t0 = os.clock()
	while got < windows and os.clock() - t0 < 30 do
		RunService.RenderStepped:Wait()
		local v = o:GetAttribute(attr)
		if v ~= last and v then
			last = v
			local _, s, m = v:match("^(%d+) ([%d%.]+) ([%d%.]+)$")
			sum += tonumber(s) nfr += 30 max = math.max(max, tonumber(m))
			got += 1
		end
	end
	return nfr > 0 and ("%d frames avg %.4f ms max %.4f ms"):format(nfr, sum / nfr, max) or "no data"
end
local function count()
	local gui, vpf, all = 0, 0, 0
	local roots = {win.HatchBack, win.HatchFront, page, pg:FindFirstChild("StreakCelebrate"), pg:FindFirstChild("StreakFly")}
	for _, r in roots do
		if r then
			for _, d in {r, unpack(r:GetDescendants())} do
				all += 1
				if d:IsA("GuiObject") then gui += 1 end
				if d:IsA("ViewportFrame") then vpf += 1 end
			end
		end
	end
	local pgAll = #pg:GetDescendants()
	return gui, vpf, all, pgAll
end
local function mem() return Stats:GetTotalMemoryUsageMb(), Stats:GetMemoryUsageMbForTag(Enum.DeveloperMemoryTag.LuaHeap), Stats:GetMemoryUsageMbForTag(Enum.DeveloperMemoryTag.Gui) end

-- make sure the window is open on DAILY
if not win.Visible then mm.OpenPage:Fire("Gift") task.wait(0.8) end
page:SetAttribute("Tab", "Daily")
task.wait(0.5)
-- 2 cost
table.insert(out, "DAILY  StreakClient " .. sample(page, "HatchPerfDaily", 10))
table.insert(out, "DAILY  bats " .. sample(front, "HatchPerfBats", 10))
page:SetAttribute("Tab", "Playtime")
task.wait(0.3)
table.insert(out, "PLAYTIME PlaytimeClient " .. sample(page, "HatchPerfPlay", 10))
table.insert(out, "PLAYTIME StreakClient (tabs/dots) " .. sample(page, "HatchPerfDaily", 10))
page:SetAttribute("Tab", "Daily")
-- 1 idle
mm.CloseWindow:Fire()
task.wait(0.6)
local c0 = counters()
local loop0 = front:GetAttribute("BatLoop")
task.wait(3)
local c1 = counters()
table.insert(out, ("IDLE 3 s closed: daily %d->%d play %d->%d bats %d->%d BatLoop %s"):format(c0.daily, c1.daily, c0.play, c1.play, c0.bats, c1.bats, tostring(loop0)))
local idleOk = c0.daily == c1.daily and c0.play == c1.play and c0.bats == c1.bats and loop0 == false
-- 3 instances
local gui, vpf, all, pgAll = count()
table.insert(out, ("INSTANCES window+pages+celebrate+fly: %d GuiObjects, %d ViewportFrames (bats), %d instances; PlayerGui %d"):format(gui, vpf, all, pgAll))
-- 4 leaks: 30 x (open, switch tabs, close)
local m0, l0, g0 = mem()
for i = 1, 30 do
	mm.OpenPage:Fire("Gift")
	task.wait(0.35)
	page:SetAttribute("Tab", i % 2 == 0 and "Daily" or "Playtime")
	task.wait(0.15)
	page:SetAttribute("Tab", i % 2 == 0 and "Playtime" or "Daily")
	task.wait(0.15)
	mm.CloseWindow:Fire()
	task.wait(0.25)
end
task.wait(1)
local gui2, vpf2, all2, pgAll2 = count()
local m1, l1, g1 = mem()
table.insert(out, ("LEAK x30: GuiObjects %d->%d, VPF %d->%d, instances %d->%d, PlayerGui %d->%d, BatLoop after close %s"):format(gui, gui2, vpf, vpf2, all, all2, pgAll, pgAll2, tostring(front:GetAttribute("BatLoop"))))
table.insert(out, ("MEMORY total %.1f->%.1f MB, LuaHeap %.1f->%.1f MB, Gui %.1f->%.1f MB"):format(m0, m1, l0, l1, g0, g1))
table.insert(out, "idle ok " .. tostring(idleOk) .. ", instances flat " .. tostring(gui == gui2 and all == all2))
return table.concat(out, "\n")
