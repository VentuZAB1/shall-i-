-- streak_client.lua v2 (2026-10-21, HATCH NIGHT Gift window; plan 8.2 + review SHOULD 16; sections 7-8 = the visual
-- review fix round: PlayBar, pet slot, SKIP ALL centred, celebration lid order / burst / stars). Also stored as
-- ServerStorage.StreakTests.CLIENT_SRC. Paste into execute_luau, Client datamodel, right after a TestFreshSave Play
-- session starts (the fresh save has Day 1 waiting, TutorialDone true, no Welcome Back). v1 = streak_client_v1.lua.
local p = game.Players.LocalPlayer
local pg = p.PlayerGui
local pass, fail, lines = 0, 0, {}
local function check(name, ok, detail)
	if ok then pass += 1 else fail += 1 table.insert(lines, "FAIL " .. name .. (detail ~= nil and (": " .. tostring(detail)) or "")) end
end
local function waitFor(fn, t)
	local t0 = os.clock()
	while os.clock() - t0 < t do if fn() then return true end task.wait(0.1) end
	return fn()
end
local t0 = os.clock() while p:GetAttribute("DataLoaded") ~= true and os.clock() - t0 < 15 do task.wait(0.2) end
local mm = pg:WaitForChild("MainMenu")
local win = mm.Window
local face = win.Face
local page = face.Body:WaitForChild("GiftPage", 10)
local daily = page and page:FindFirstChild("DailyView")
local back, front = win:FindFirstChild("HatchBack"), win:FindFirstChild("HatchFront")
local function card(d) return daily and daily:FindFirstChild("Card" .. d) end
local function state(d) local c = card(d) return c and c:GetAttribute("State") or "?" end
local function label(d)
	local c = card(d)
	local s = c and c:FindFirstChild("State", true)
	return s and s.ContentText or "?"
end
local function pip(i)
	local s = daily and daily:FindFirstChild("Streak")
	local pp = s and s:FindFirstChild("Pip" .. i)
	return pp and pp:GetAttribute("State") or "?"
end
local function count()
	local s = daily and daily:FindFirstChild("Streak")
	return s and s:FindFirstChild("Count") and s.Count.ContentText or "?"
end

-- 1 auto_open: the window opens itself on DAILY, in the HATCH NIGHT shell
check("auto_open window", waitFor(function() return win.Visible end, 20))
task.wait(0.6)
check("auto_open tab Daily", page and page:GetAttribute("Tab") == "Daily", page and page:GetAttribute("Tab"))
check("auto_open title", face.Title.Text == "Daily Rewards", face.Title.Text)
check("auto_open hatch title", front and front.Title.Text == "DAILY REWARDS", front and front.Title.Text)
check("auto_open shell shown", back and back.Visible and front and front.Visible)
local header = face:FindFirstChild("Header")
check("auto_open check-ui chrome hidden", header and not header.Visible and not face.Title.Visible and not win.Depth.Visible,
	tostring(header and header.Visible) .. " " .. tostring(face.Title.Visible) .. " " .. tostring(win.Depth.Visible))
check("auto_open close+icon hidden", not face.Close.Visible and not face.Icon.Visible, tostring(face.Close.Visible) .. " " .. tostring(face.Icon.Visible))
local ar = win.AbsoluteSize.X / win.AbsoluteSize.Y
check("auto_open aspect 740/470", math.abs(ar - 740 / 470) <= 0.01, ar)
local cs, ss = page and page:FindFirstChild("CanvasScale"), back and back:FindFirstChild("SkinScale")
check("auto_open canvas = skin scale", cs and ss and math.abs(cs.Scale - ss.Scale) <= 0.001, cs and ss and (cs.Scale .. " " .. ss.Scale))
check("Tabs exist", page and page:FindFirstChild("Tabs") ~= nil)

-- 2 states (fresh save: Day 1 claimable)
check("states card1 CLAIM", state(1) == "CLAIM" and label(1) == "CLAIM!", state(1) .. " " .. label(1))
check("states card2 LOCKED", state(2) == "LOCKED" and label(2) == "LOCKED", state(2) .. " " .. label(2))
check("states card7 LOCKED", state(7) == "LOCKED" and label(7) == "IN 6 DAYS", state(7) .. " " .. label(7))
check("states pip1 today", pip(1) == "today" and count() == "1/7", pip(1) .. " " .. count())
local ring = card(1) and card(1).Face:FindFirstChild("Ring")
check("states card1 ring (in Face)", ring and ring.Visible)
local badge = mm.Menu.Gift.Face:FindFirstChild("Badge")
check("states tile badge", badge and badge.Visible)

-- 3 claim through the card's real press() (TestPress). REGRESSION (owner 2026-10-21, "it says try again but its
-- available"): the server says claimable (fresh save, no client-side attribute overrides anywhere in this test), the
-- whole-card hit and the button fire in the SAME frame -> exactly one claim, and no error text ever shows
local ERR = {["TRY AGAIN"] = true, ["TOMORROW!"] = true, ["WAIT..."] = true, ["PETS FULL!"] = true, ["EGGS FULL!"] = true, ["NOT READY"] = true}
local function watchErrors(getLabel, secs)
	local seen
	local t1 = os.clock()
	while os.clock() - t1 < secs do
		local l = getLabel()
		if ERR[l] then seen = l end
		task.wait()
	end
	return seen
end
local flew = false
local fly = pg:FindFirstChild("StreakFly")
local conn = fly and fly.ChildAdded:Connect(function() flew = true end)
local claimable0 = p:GetAttribute("StreakClaimable")
card(1).TestPress:Fire()
card(1).TestPress:Fire() -- (same frame: hit + button)
local err1 = watchErrors(function() return label(1) end, 1.5)
check("claim server-claimable before press", claimable0 == true, claimable0)
check("claim double press: no error text", err1 == nil, err1)
check("claim card1 CLAIMED", waitFor(function() return state(1) == "CLAIMED" and label(1) == "CLAIMED" end, 3), state(1) .. " " .. label(1))
check("claim double press: claimed once", p:GetAttribute("StreakThrough") == 1 and p:GetAttribute("StreakNext") == 2, tostring(p:GetAttribute("StreakThrough")) .. " " .. tostring(p:GetAttribute("StreakNext")))
check("claim card1 check", card(1).Badges.Check.Visible)
check("claim card2 TOMORROW", state(2) == "TOMORROW" and label(2):match("^%d%d:%d%d:%d%d$") ~= nil, state(2) .. " " .. label(2))
check("claim pip1 done", pip(1) == "done" and count() == "1/7", pip(1) .. " " .. count())
check("claim fly-text", flew or waitFor(function() return flew end, 1))
if conn then conn:Disconnect() end

-- 4 playtime_tab
page:SetAttribute("Tab", "Playtime")
task.wait(0.4)
check("playtime_tab views", page.PlaytimeView.Visible and not page.DailyView.Visible)
check("playtime_tab titles", face.Title.Text == "Playtime Rewards" and front.Title.Text == "PLAYTIME REWARDS", face.Title.Text .. " / " .. front.Title.Text)
local slots = 0
for i = 1, 12 do if page.PlaytimeView:FindFirstChild("Slot" .. i) then slots += 1 end end
check("playtime_tab 12 slots", slots == 12, slots)
local px = page.Tabs.Pill.Position.X.Offset
check("playtime_tab pill slot B", math.abs(px - 231) <= 0.5, px)
page:SetAttribute("Tab", "Daily")
task.wait(0.3)

-- 5 other windows (RIS run C, 2026-10-22: Rebirth is a HATCH NIGHT page now, like every MainMenu page; the Check-UI
-- chrome is only the fallback): Rebirth opens in the night shell with its own violet band
mm.OpenPage:Fire("Rebirth")
task.wait(0.7)
check("rebirth hatch shell", back.Visible and front.Visible)
check("rebirth title REBIRTH", front.Title.Text == "REBIRTH", front.Title.Text)
check("rebirth violet tooth (112,0,214)", front.Crack.Tooth1.BackgroundColor3 == Color3.fromRGB(112, 0, 214), tostring(front.Crack.Tooth1.BackgroundColor3))
local arc = win:FindFirstChildOfClass("UIAspectRatioConstraint")
check("rebirth aspect 740/470", arc and math.abs(arc.AspectRatio - 740 / 470) <= 0.01, arc and arc.AspectRatio)
mm.CloseWindow:Fire()
task.wait(0.4)

-- 6 REGRESSION, PLAYTIME: slot 1 (1 min) once the SERVER's clock says ready (PlaytimeStart as the server set it, no
-- client override); a double tap in one frame -> one claim, CLAIMED, no error text
mm.OpenPage:Fire("Gift")
task.wait(0.5)
page:SetAttribute("Tab", "Playtime")
local pv = page.PlaytimeView
local s1 = pv.Slot1
local function slotLabel() return s1.Face.Button.Face.State.ContentText end
check("playtime slot1 ready (server clock)", waitFor(function() return s1:GetAttribute("State") == "CLAIM" end, 75), tostring(s1:GetAttribute("State")))
s1.TestPress:Fire()
s1.TestPress:Fire() -- (same frame: hit + button)
local err2 = watchErrors(slotLabel, 1.5)
check("playtime double tap: no error text", err2 == nil, err2)
check("playtime slot1 CLAIMED", waitFor(function() return s1:GetAttribute("State") == "CLAIMED" end, 3), tostring(s1:GetAttribute("State")) .. " " .. slotLabel())
local n = 0
for v in (p:GetAttribute("PlaytimeClaimed") or ""):gmatch("%d+") do if v == "1" then n += 1 end end
check("playtime claimed once (server)", n == 1, p:GetAttribute("PlaytimeClaimed"))

-- 7 (2026-10-21 visual review MUST 5 / 6 / 7) PLAYTIME row 2 = the PlayBar, the 2-hour pet slot, SKIP ALL centred
local bar = pv:FindFirstChild("PlayBar")
check("playbar shown", bar ~= nil and bar.Visible)
local fill = bar and bar:FindFirstChild("Fill", true)
check("playbar fill", fill ~= nil and fill.Visible and fill.Size.X.Offset >= 16 and fill.Size.X.Offset <= 204, fill and tostring(fill.Size))
local ptime = bar and bar:FindFirstChild("Time")
check("playbar time", ptime ~= nil and ptime.ContentText:match("^%d+:%d%d") ~= nil, ptime and ptime.ContentText)
local s12 = pv.Slot12
local prism = s12.Face:FindFirstChildOfClass("UIStroke") and s12.Face:FindFirstChildOfClass("UIStroke"):FindFirstChild("Prism")
check("slot12 prism outline", prism ~= nil and prism.Enabled)
check("slot12 waits bright (0.95)", s12:GetAttribute("State") ~= "WAIT" or s12.Dim.BackgroundTransparency >= 0.94, s12.Dim.BackgroundTransparency)
local Hh = require(game.ReplicatedStorage.BrickUI).Hatch
local sf = pv.SkipAll.Face
local padL = sf.SkipLabel.Position.X.Offset
local padR = 207 - (sf.Price.Position.X.Offset + Hh.textWidth(sf.Price.Text, sf.Price.TextSize))
check("skip all centred", math.abs(padL - padR) <= 2, ("left %.1f right %.1f"):format(padL, padR))
page:SetAttribute("Tab", "Daily")
mm.CloseWindow:Fire()
task.wait(0.4)

-- 8 (visual review MUST 4 + SHOULD 11) the Day 7 celebration: the lid is in Pop under the pet, the impact burst and the
-- star arc show, nothing is left behind
local cel = pg:FindFirstChild("StreakCelebrate")
cel.TestCelebrate:Fire()
task.wait(2.6)
local popF = cel.Box.Pop
local lid, petRoot, egg = popF:FindFirstChild("TopHalf"), popF:FindFirstChild("PetRoot"), popF:FindFirstChild("Egg")
check("cel lid in Pop", lid ~= nil and egg ~= nil and egg:FindFirstChild("TopHalf") == nil)
check("cel order lid < pet < egg", lid and petRoot and egg and lid.ZIndex < petRoot.ZIndex and petRoot.ZIndex < egg.ZIndex,
	lid and petRoot and egg and (lid.ZIndex .. " " .. petRoot.ZIndex .. " " .. egg.ZIndex))
local stars = 0
for i = 1, 6 do local s = popF:FindFirstChild("Star" .. i) if s and s.Visible then stars += 1 end end
check("cel 6 stars", stars == 6, stars)
check("cel burst made + done", popF:FindFirstChild("Burst") ~= nil and not popF.Burst.Visible)
check("cel lid gone", lid ~= nil and not lid.Visible)
local shards = 0
for _, o in popF:GetChildren() do if o.Name == "Shard" then shards += 1 end end
check("cel shards cleaned", shards == 0, shards)
cel.Enabled = false
return ("pass %d fail %d\n%s"):format(pass, fail, table.concat(lines, "\n"))
