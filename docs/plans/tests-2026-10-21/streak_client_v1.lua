-- Task 5 client checks (paste into execute_luau, Client datamodel, right after a TestFreshSave Play session starts:
-- the fresh save has Day 1 waiting, TutorialDone true, no Welcome Back).
local p = game.Players.LocalPlayer
local pg = p.PlayerGui
local pass, fail, lines = 0, 0, {}
local function check(name, ok, detail)
	if ok then pass += 1 else fail += 1 table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end
end
local function waitFor(fn, t)
	local t0 = os.clock()
	while os.clock() - t0 < t do if fn() then return true end task.wait(0.2) end
	return fn()
end
local t0 = os.clock() while p:GetAttribute("DataLoaded") ~= true and os.clock() - t0 < 15 do task.wait(0.2) end
local mm = pg:WaitForChild("MainMenu")
local win = mm.Window
local page = win.Face.Body:WaitForChild("GiftPage", 10)
local function title() return win.Face.Title.Text end
local function state(d)
	local card = page and page:FindFirstChild("DailyView") and page.DailyView:FindFirstChild("Card" .. d)
	local s = card and card:FindFirstChild("State", true)
	return s and s.ContentText or "?"
end

-- 1 auto_open
check("auto_open window", waitFor(function() return win.Visible end, 20))
check("auto_open tab Daily", page and page:GetAttribute("Tab") == "Daily", page and page:GetAttribute("Tab"))
check("auto_open title", title() == "Daily Rewards", title())
check("Tabs exist", page and page:FindFirstChild("Tabs") ~= nil, "Tabs not found")

-- 2 states
task.wait(0.5)
check("states card1 CLAIM", state(1) == "CLAIM", state(1))
check("states card2 LOCKED", state(2) == "LOCKED", state(2))
local badge = mm.Menu.Gift.Face:FindFirstChild("Badge")
check("states tile badge", badge and badge.Visible)

-- 3 claim (the same remote the CLAIM button uses)
local ok, day = game.ReplicatedStorage.Streak.Claim:InvokeServer()
check("claim ok", ok == true and day == 1, tostring(ok) .. " " .. tostring(day))
check("claim card1 CLAIMED", waitFor(function() return state(1) == "CLAIMED" end, 2), state(1))
check("claim card2 TOMORROW", state(2) == "TOMORROW", state(2))
local right = page and page.DailyView:FindFirstChild("Status") and page.DailyView.Status:FindFirstChild("Right")
check("claim countdown", right and right.ContentText:match("^Next reward in %d%d:%d%d:%d%d$") ~= nil, right and right.ContentText)

-- 4 playtime_tab
page:SetAttribute("Tab", "Playtime")
task.wait(0.3)
check("playtime_tab views", page.PlaytimeView.Visible and not page.DailyView.Visible)
check("playtime_tab title", title() == "Playtime Rewards", title())
page:SetAttribute("Tab", "Daily")
return ("pass %d fail %d\n%s"):format(pass, fail, table.concat(lines, "\n"))
