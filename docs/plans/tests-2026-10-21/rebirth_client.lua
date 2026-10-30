-- Task 2 client checks (paste into execute_luau, Client datamodel, during a TestFreshSave Play session).
-- Attributes are set LOCALLY on the LocalPlayer: that only drives this client's UI (the server never sees them).
-- Run it FIRST in a fresh session (the READY banner shows once per rebirth level per session). 13 checks since the
-- 2026-10-21 perf fix (canRebirth answers within the 0.5 s poll; the arrow loop reads the cached answer).
local p = game.Players.LocalPlayer
local pg = p.PlayerGui
local mm = pg:WaitForChild("MainMenu")
local pass, fail, lines = 0, 0, {}
local function check(name, ok, detail)
	if ok then pass += 1 else fail += 1 table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end
end
local function set(k, v) p:SetAttribute(k, v) task.wait() end
local function waitFor(fn, t)
	local t0 = os.clock()
	while os.clock() - t0 < t do if fn() then return true end task.wait(0.1) end
	return fn()
end
local function banner()
	local g = pg:FindFirstChild("RebirthReadyUI")
	return g and g:FindFirstChild("Banner", true)
end
local function bannerOn() local b = banner() return b ~= nil and b.Visible and b:FindFirstAncestorOfClass("ScreenGui").Enabled end

-- Banner_once
mm.CloseWindow:Fire()
set("TutorialDone", true) set("TutorialExtra", 0) set("Rebirths", 0) set("PetInventory", "[]") set("Money", 0)
task.wait(0.8)
mm.CloseWindow:Fire() -- (2026-10-21) the daily auto-open may have opened the Gift window meanwhile: the banner waits for windows
set("Money", 30000)
check("Banner_once shows", waitFor(bannerOn, 2), banner() and "hidden" or "RebirthReadyUI not found")
local b = banner()
local title = b and b:FindFirstChild("Title", true)
local sub = b and b:FindFirstChild("Sub", true)
check("Banner_once title", title and title.Text == "REBIRTH READY!", title and title.Text)
-- (2026-10-21 owner: smaller, no description line - just REBIRTH READY!)
check("Banner_once has no sub line", sub == nil, sub and sub.Text)
check("Banner_once is small (<= 440 x 70 before device scale)", b and b.Size.X.Offset <= 440 and b.Size.Y.Offset <= 70,
	b and tostring(b.Size))
task.wait(5)
check("Banner_once hides after 4 s", not bannerOn())
set("Money", 0) task.wait(0.8) set("Money", 30000)
task.wait(1.5)
check("Banner_once not again", not bannerOn())

-- Banner_waits_for_window
set("Money", 0)
set("Rebirths", 1)
set("PetInventory", '[{"id":"t_water","name":"Kappa","kg":5}]')
mm.OpenPage:Fire("Shop")
task.wait(0.8)
set("Money", 1200000)
task.wait(1.5)
check("Banner_waits hidden while window open", not bannerOn())
mm.CloseWindow:Fire()
check("Banner_waits shows after close", waitFor(bannerOn, 2))
task.wait(5)

-- Banner_never_in_tutorial + arrows
set("Money", 0) set("PetInventory", "[]") set("Rebirths", 0)
set("TutorialExtra", 3)
task.wait(0.8)
set("Money", 30000)
task.wait(1.5)
check("Tutorial: no banner", not bannerOn())
local tut = pg:FindFirstChild("RebirthTutorialUI")
local tile = tut and tut:FindFirstChild("TileArrow", true)
check("Tutorial: TileArrow visible", tile and tile.Visible and tut.Enabled, tut and "hidden" or "RebirthTutorialUI not found")
mm.OpenPage:Fire("Rebirth")
task.wait(1)
local page = mm.Window.Face.Body:FindFirstChild("RebirthPage")
local arrow = page and page:FindFirstChild("TutorialArrow")
check("Tutorial: TileArrow hidden with window", not (tile and tile.Visible))
check("Tutorial: page arrow visible", arrow and arrow.Visible, arrow and "hidden" or "TutorialArrow not found")
mm.CloseWindow:Fire()
set("TutorialExtra", 0) set("Money", 0)
-- (2026-10-21 perf review M-9) past step 11 the arrow RenderStepped hides both arrows and returns early
task.wait(0.3)
check("after step 11: both arrows hidden (M-9 early-out)", not tile.Visible and not (arrow and arrow.Visible))
return ("pass %d fail %d\n%s"):format(pass, fail, table.concat(lines, "\n"))
