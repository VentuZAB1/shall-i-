-- starter_hud_client.lua (2026-10-21): client checks for StarterPackHud (the Starter Pack HUD offer, v3 after the visual review)
-- + the popup hero (S.popup).
-- Plan + review: docs/plans/2026-10-21-starter-pack-hud-icon.md (+ .review.md).
--
-- HOW TO RUN (Studio, Play, TestFreshSave session ONLY - never on a real save):
--   1. Edit: workspace:SetAttribute("TestFreshSave", true), read it back true, then Play.
--   2. Server datamodel: the countdown starts at Rebirths >= 1 (StarterPackServer), a fresh test save has 0:
--        local p = game.Players:GetPlayers()[1]; p:SetAttribute("Rebirths", 1); game.ServerStorage.StarterDebug:Invoke("reset", p)
--      (a fresh 24 h; the art only shows while it runs). Last hour: StarterDebug:Invoke("endsAt", p, os.time() + 1800).
--   3. Client datamodel: close the auto windows: PlayerGui.MainMenu.CloseWindow:Fire(); PlayerGui.StarterPackUI.Enabled = false
--   4. Client datamodel: paste this whole file once; it stores the runner in _G.StarterHudTests. Then run sections:
--        return _G.StarterHudTests("placement")
--      Sections: layout, placement, envelope, motion, states, flicker, hover, content, overlaps, timer, expiry, popup (each returns
--      a report; "overlaps" "admin" needs the server to fire the admin banner first, "timer" "urgent" needs StarterDebug
--      "endsAt" os.time() + 1800, "expiry" needs "endsAt" os.time() + 20 - see those sections; "envelope" (13, "compact")
--      = the phone layout forced with TestScale 0.56 + TestCompact).
--   Server-side steps (Server datamodel), used between client sections:
--        local p = game.Players:GetPlayers()[1]; local D = game.ServerStorage.StarterDebug
--        D:Invoke("restricted", p, true) / D:Invoke("restricted", p, nil)     -- cash hero / back
--        p:SetAttribute("StarterEgg", "StormEgg")                             -- egg swap + pop
--        D:Invoke("grant", p)  /  D:Invoke("reset", p)                        -- owned (gone) / back (a fresh 24 h)
--        D:Invoke("endsAt", p, os.time() + 1800)                              -- the last hour (urgent)
--        game.ReplicatedStorage.Admin.Banner:FireClient(p, {kind = "message", from = "TEST", text = string.rep("LONG ADMIN MESSAGE ", 8)})
--   5. Stop Play, then Edit: workspace:SetAttribute("TestFreshSave", false).
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local GuiService = game:GetService("GuiService")
local CollectionService = game:GetService("CollectionService")

local player = Players.LocalPlayer
local pg = player:WaitForChild("PlayerGui")

local function report()
	local r = {pass = 0, fail = 0, lines = {}}
	function r.check(name, ok, detail)
		if ok then r.pass += 1 else r.fail += 1 end
		table.insert(r.lines, (ok and "ok   " or "FAIL ") .. name .. (detail ~= nil and (" [" .. tostring(detail) .. "]") or ""))
	end
	function r.note(s) table.insert(r.lines, "     " .. s) end
	function r.text(title) return ("%s: %d pass / %d fail\n%s"):format(title, r.pass, r.fail, table.concat(r.lines, "\n")) end
	return r
end

local function hud() return pg:FindFirstChild("StarterOfferHud") end
local function state() return hud().TestState:Invoke() end
local function root() return hud().Root end
local function boxOf(o) local p, z = o.AbsolutePosition, o.AbsoluteSize return {p.X, p.Y, p.X + z.X, p.Y + z.Y} end
local function hit(a, b) return a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4] end
local function fmt(r) return ("x %.1f..%.1f y %.1f..%.1f"):format(r[1], r[3], r[2], r[4]) end
local function deviceScale()
	local vp = workspace.CurrentCamera.ViewportSize
	return math.clamp(math.min(vp.X / 1050, vp.Y / 620), 0.52, 1.18)
end
local function uiScaleOf(o) -- the UIScale product above o (strokes scale with it; TextBounds are ALREADY screen px)
	local f = 1
	while o and not o:IsA("LayerCollector") do
		local sc = o:FindFirstChildOfClass("UIScale")
		if sc then f *= sc.Scale end
		o = o.Parent
	end
	return f
end
local function textBox(l)
	local p, z, tb = l.AbsolutePosition, l.AbsoluteSize, l.TextBounds -- (screen px: measured 2026-10-21, 20 at UIScale 2 -> 40)
	local w, h = math.min(tb.X, z.X), math.min(tb.Y, z.Y)
	local x = l.TextXAlignment == Enum.TextXAlignment.Left and p.X
		or (l.TextXAlignment == Enum.TextXAlignment.Right and p.X + z.X - w) or p.X + (z.X - w) / 2
	local y = l.TextYAlignment == Enum.TextYAlignment.Top and p.Y
		or (l.TextYAlignment == Enum.TextYAlignment.Bottom and p.Y + z.Y - h) or p.Y + (z.Y - h) / 2
	return {x, y, x + w, y + h}
end
local function isUp() local st = state() return st.shown and root().Visible end
local function waitFor(pred, timeout) -- -> seconds it took, or nil
	local t0 = os.clock()
	while os.clock() - t0 < timeout do
		if pred() then return os.clock() - t0 end
		task.wait()
	end
	return pred() and (os.clock() - t0) or nil
end

-- the art's motion envelope, per frame (visual review MUST 7). NOTE: a child's AbsolutePosition ALREADY includes its
-- ancestors' rotation (measured 2026-10-21: a child at its parent's right edge moves to the bottom at parent Rotation 90),
-- so the centres are used as they are; only the box orientations add the rotations.
--   c0 = the conservative envelope: the plan's 10.3 half-diagonal circles, except the egg trio (Egg / EggOutline /
--        EggShadow) = the rotated square of 0.86 x its size (half-extent 0.43 s (|cos| + |sin|): the frame is mostly
--        transparent), the Timer = its TextBounds + 3 px of stroke (x the UIScales), sunbursts radius size/2. Used for
--        on screen / above the column / the neighbours.
--   j0 = the JUDGE envelope ("judge the real pixels"): the same egg trio / Timer / sunburst boxes, everything else its own
--        rotated box (as the v2 judge did).
local EGG_TRIO = {Egg = true, EggOutline = true, EggShadow = true}
local function artBoxes()
	local float = root().Body.Float
	local a = math.rad(float.Rotation)
	local ca, sa = math.cos(a), math.sin(a)
	local c0 = {math.huge, math.huge, -math.huge, -math.huge}
	local j0 = {math.huge, math.huge, -math.huge, -math.huge}
	local function add(t, c, hx, hy)
		t[1], t[2], t[3], t[4] = math.min(t[1], c.X - hx), math.min(t[2], c.Y - hy), math.max(t[3], c.X + hx), math.max(t[4], c.Y + hy)
	end
	for _, o in float:GetChildren() do
		if o:IsA("GuiObject") and o.Visible then
			local c = o.AbsolutePosition + o.AbsoluteSize / 2
			local th = math.rad(o.Rotation) + a
			local ct, st = math.abs(math.cos(th)), math.abs(math.sin(th))
			if EGG_TRIO[o.Name] then
				local h = 0.43 * o.AbsoluteSize.X * (ct + st)
				add(c0, c, h, h) add(j0, c, h, h)
			elseif o.Name == "Timer" and o:IsA("TextLabel") then
				local s3 = 3 * uiScaleOf(o) -- (TextBounds include every UIScale, the label's own TimerScale too: measured)
				local w, h = o.TextBounds.X / 2 + s3, o.TextBounds.Y / 2 + s3
				local hx, hy = w * math.abs(ca) + h * math.abs(sa), w * math.abs(sa) + h * math.abs(ca)
				add(c0, c, hx, hy) add(j0, c, hx, hy)
			elseif o.Name:match("^Sun") then
				local rad = o.AbsoluteSize.X / 2
				add(c0, c, rad, rad) add(j0, c, rad, rad)
			else
				local rad = o.AbsoluteSize.Magnitude / 2
				add(c0, c, rad, rad)
				local w, h = o.AbsoluteSize.X / 2, o.AbsoluteSize.Y / 2
				add(j0, c, w * ct + h * st, w * st + h * ct)
			end
		end
	end
	return c0, j0
end

local S = {}

---------------------------------------------------------------- layout: the review's MUST 10 rows through TestLayout
function S.layout()
	local r = report()
	local tl = hud():FindFirstChild("TestLayout")
	r.check("TestLayout exists (Studio only)", tl ~= nil)
	if not tl then return r.text("layout") end
	-- v3 (visual review MUST 2): FULL 150x170, COMPACT 150x156 - the full rows = the plan review's, the compact rows smaller
	local rows = { -- name, viewport, gui size, colTop, colRight, s, compact, x0, x1, y0, y1
		{"1050x620", 1050, 620, 1050, 562, 190.0, 1040.1, 1.000, false, 890.1, 1040.1, 14.0, 184.0},
		{"1920x1080", 1920, 1080, 1920, 1022, 345.4, 1902.0, 1.180, false, 1725.0, 1902.0, 137.7, 338.3},
		{"1519x753", 1519, 753, 1519, 695, 234, 1504, 1.180, false, 1327.0, 1504.0, 26.3, 226.9},
		{"744x435 (col 1.3)", 744, 435, 744, 377, 109.1, 737, 0.636, true, 641.5, 737.0, 5.6, 104.9},
		{"844x390 phone", 844, 390, 750, 332, 96.1, 743, 0.560, true, 659.1, 743.0, 5.0, 92.3},
		{"667x375 phone", 667, 375, 667, 317, 92, 661, 0.535, true, 580.7, 661.0, 4.8, 88.4},
		{"1440x900 16:10", 1440, 900, 1440, 842, 289.7, 1426.5, 1.180, false, 1249.5, 1426.5, 82.0, 282.6},
		{"1024x768 iPad", 1024, 768, 1024, 710, 261.6, 1014.4, 0.975, false, 868.1, 1014.4, 90.0, 255.7},
		{"2560x1080 21:9", 2560, 1080, 2560, 1022, 345.4, 2536, 1.180, false, 2359.0, 2536.0, 137.7, 338.3},
	}
	for _, row in rows do
		local name, vx, vy, gx, gy, colTop, colRight, es, ecomp, ex0, ex1, ey0, ey1 = table.unpack(row)
		local k = math.clamp(math.min(vx / 1050, vy / 620), 0.52, 1.18)
		local s, comp, x0, y0, x1, y1 = tl:Invoke(Vector2.new(gx, gy), k, colTop, colRight, 58)
		local ok = math.abs(s - es) <= 0.01 and comp == ecomp and math.abs(x0 - ex0) <= 1 and math.abs(x1 - ex1) <= 1
			and math.abs(y1 - ey1) <= 1 and math.abs(y0 - ey0) <= 1
		r.check(name .. " Root rect", ok, ("s %.3f %s x %.1f..%.1f y %.1f..%.1f"):format(s, comp and "compact" or "full", x0, x1, y0, y1))
		local inset = (vx - gx) / 2
		local rr = {0.5 * vx - 341 * k - inset, 0.22 * vy - 66 * k - 58, 0.5 * vx + 341 * k - inset, 0.22 * vy + 66 * k - 58}
		r.check(name .. " clear of REBIRTH READY (1.1 pop)", not hit({x0, y0, x1, y1}, rr), ("banner right %.0f"):format(rr[3] + inset))
		r.check(name .. " clear of the $/Day band (screen y 8..58)", y0 + 58 >= 58, y0 + 58)
	end
	return r.text("layout")
end

---------------------------------------------------------------- placement (10.3.1) + gui settings + HOME_X sanity
function S.placement()
	local r = report()
	local g = hud()
	local st = state()
	r.check("art is up", st.shown and root().Visible, st.why)
	r.check("ScreenGui: DisplayOrder 1", g.DisplayOrder == 1, g.DisplayOrder)
	r.check("ScreenGui: IgnoreGuiInset false, CoreUISafeInsets, ResetOnSpawn false, Sibling",
		g.IgnoreGuiInset == false and g.ScreenInsets == Enum.ScreenInsets.CoreUISafeInsets and g.ResetOnSpawn == false
			and g.ZIndexBehavior == Enum.ZIndexBehavior.Sibling)
	local tiles = pg.PetsEggsUI.RightTiles
	r.check("HOME_X sanity: RightTiles at home = 1 - Menu X", math.abs(tiles.Position.X.Scale - st.homeX) < 1e-4,
		("%.5f vs %.5f"):format(tiles.Position.X.Scale, st.homeX))
	local gp, gs = g.AbsolutePosition, g.AbsoluteSize
	local colTop = tiles.AbsolutePosition.Y - gp.Y
	local colRight = gs.X * st.homeX
	local s, comp, x0, y0, x1, y1 = g.TestLayout:Invoke(gs, deviceScale(), colTop, colRight, GuiService:GetGuiInset().Y)
	local rb = boxOf(root())
	r.note(("viewport %s  gui %s at %s  inset %d  k %.3f"):format(tostring(workspace.CurrentCamera.ViewportSize), tostring(gs), tostring(gp),
		GuiService:GetGuiInset().Y, deviceScale()))
	r.note(("solve: s %.3f %s Root %s (gui px)"):format(s, comp and "compact" or "full", fmt({x0, y0, x1, y1})))
	r.note(("live Root: %s (abs)  screen y %.0f..%.0f"):format(fmt(rb), rb[2] + GuiService:GetGuiInset().Y, rb[4] + GuiService:GetGuiInset().Y))
	r.check("Root rect = solve() (+-1 px)", math.abs(rb[1] - (gp.X + x0)) <= 1 and math.abs(rb[3] - (gp.X + x1)) <= 1
		and math.abs(rb[2] - (gp.Y + y0)) <= 1 and math.abs(rb[4] - (gp.Y + y1)) <= 1)
	r.check("state rect = live Root (+-1)", st.rect and math.abs(st.rect[1] - rb[1]) <= 1 and math.abs(st.rect[4] - rb[4]) <= 1)
	r.check("bottom <= column top - 5", rb[4] <= tiles.AbsolutePosition.Y - 5, tiles.AbsolutePosition.Y - rb[4])
	r.check("right edge <= gui width", rb[3] <= gp.X + gs.X + 0.5)
	local colR = tiles.AbsolutePosition.X + tiles.AbsoluteSize.X
	r.check("Root right edge = column right edge (+-1)", math.abs(rb[3] - colR) <= 1, ("%.1f vs %.1f"):format(rb[3], colR))
	r.check("caption shown in FULL", (not comp) == root().Body.Caption.Visible)
	-- one AbsolutePosition space for every ScreenGui (IgnoreGuiInset true guis start at -inset)
	local rr = pg:FindFirstChild("RebirthReadyUI")
	if rr then r.note(("RebirthReadyUI (IgnoreGuiInset) AbsolutePosition %s; ours %s"):format(tostring(rr.AbsolutePosition), tostring(gp))) end
	return r.text("placement")
end

---------------------------------------------------------------- envelope (10.3.2 + MUST 1 judge), 13 s = 2 pops
function S.envelope(seconds, mode)
	local r = report()
	local g = hud()
	if mode == "compact" then -- the phone layout (visual review MUST 7): TestScale 0.56 + TestCompact
		g:SetAttribute("TestScale", 0.56)
		g:SetAttribute("TestCompact", true)
		task.wait(0.6)
	end
	local st0 = state()
	r.check("art is up", st0.shown and root().Visible, st0.why)
	r.note(("mode %s: s %.3f compact %s"):format(mode or "full", st0.s, tostring(st0.compact)))
	local C = {math.huge, math.huge, -math.huge, -math.huge}
	local J = {math.huge, math.huge, -math.huge, -math.huge}
	local frames = 0
	local conn = RunService.RenderStepped:Connect(function()
		local c, q = artBoxes()
		frames += 1
		C = {math.min(C[1], c[1]), math.min(C[2], c[2]), math.max(C[3], c[3]), math.max(C[4], c[4])}
		J = {math.min(J[1], q[1]), math.min(J[2], q[2]), math.max(J[3], q[3]), math.max(J[4], q[4])}
	end)
	local pops0 = state().pops
	task.wait(seconds or 13)
	conn:Disconnect()
	-- (measure the Root / caption / column BEFORE the forced compact layout is released)
	local st = state()
	local rb = boxOf(root())
	local cap = root().Body.Caption
	local capVis, capY = cap.Visible, cap.AbsolutePosition.Y
	local tilesTop = pg.PetsEggsUI.RightTiles.AbsolutePosition.Y
	if mode == "compact" then
		g:SetAttribute("TestScale", nil)
		g:SetAttribute("TestCompact", nil)
	end
	r.note(("%d frames, %d pops; countdown %s"):format(frames, st.pops - pops0, tostring(st.timer)))
	r.check("2+ pops in 13 s", st.pops - pops0 >= 2, st.pops - pops0)
	r.check("stayed up the whole time", st.shown, st.why)
	local vp = workspace.CurrentCamera.ViewportSize
	r.note("conservative envelope (10.3 circles + MUST 7 egg / timer): " .. fmt(C))
	r.note("judge envelope (MUST 7: real pixels):                       " .. fmt(J))
	-- MUST 7's pass list (on screen, above the column, inside the Root) uses the judge envelope; the neighbours keep the
	-- conservative one
	r.check("on screen (judge)", J[1] >= 0 and J[3] <= vp.X and J[2] >= -2, fmt(J))
	r.check("above the column (judge)", J[4] <= tilesTop, ("%.1f px"):format(tilesTop - J[4]))
	local s = st.s
	r.note(("Root %s (Root %dx%d); judge envelope in Root px: left %.1f top %.1f right %.1f bottom %.1f"):format(fmt(rb), root().Size.X.Offset,
		root().Size.Y.Offset, (J[1] - rb[1]) / s, (J[2] - rb[2]) / s, (J[3] - rb[1]) / s, (J[4] - rb[2]) / s))
	r.check("judge: the art inside the Root (+-1 px)", J[1] >= rb[1] - 1 and J[2] >= rb[2] - 1 and J[3] <= rb[3] + 1 and J[4] <= rb[4] + 1,
		("margin L %.1f T %.1f R %.1f B %.1f px"):format(J[1] - rb[1], J[2] - rb[2], rb[3] - J[3], rb[4] - J[4]))
	-- the art may slip behind the caption, never over it
	local float = root().Body.Float
	local maxZ = 0
	for _, d in float:GetDescendants() do if d:IsA("GuiObject") then maxZ = math.max(maxZ, d.ZIndex) end end
	r.check("every Float descendant ZIndex < the Caption's", float.ZIndex < cap.ZIndex and maxZ < cap.ZIndex, ("max %d, caption %d"):format(maxZ, cap.ZIndex))
	if capVis then r.note(("judge art bottom vs caption top: %.1f px (positive = slips behind the caption)"):format(J[4] - capY)) end
	if mode == "compact" then return r.text("envelope compact") end -- (a forced scale: the neighbours are the real layout's)
	-- neighbours (plan + review lists): the conservative envelope vs their current rects
	local function n(o) return o and o:IsA("GuiObject") and o.AbsoluteSize.X > 0 and o end
	local list = {
		Column = n(pg.PetsEggsUI.RightTiles), Menu = n(pg.MainMenu:FindFirstChild("Menu")),
		Pills = n(pg.SpeedUI:FindFirstChild("Holder")),
		PotionTimers = n(pg.SpeedUI:FindFirstChild("Holder") and pg.SpeedUI.Holder:FindFirstChild("Potions")),
		PerDay = n(pg:FindFirstChild("OfflineBaseUI") and pg.OfflineBaseUI:FindFirstChild("PerDay")),
		WeatherRow = n(pg:FindFirstChild("WeatherTiles") and pg.WeatherTiles:FindFirstChild("Row")),
		SpeedOffer = n(pg:FindFirstChild("SpeedOffer") and pg.SpeedOffer:FindFirstChild("Offer")),
		RebirthReady = n(pg:FindFirstChild("RebirthReadyUI") and pg.RebirthReadyUI:FindFirstChild("Banner")),
		AdminBanner = n(pg:FindFirstChild("AdminBanner") and pg.AdminBanner:FindFirstChild("Banner")),
		SlingExit = n(pg:FindFirstChild("SlingUI") and pg.SlingUI:FindFirstChild("Exit", true)),
		AdminButton = n(pg:FindFirstChild("AdminUI") and pg.AdminUI:FindFirstChild("AdminButton", true)),
		AutoReconnect = n(pg:FindFirstChild("AutoReconnect") and pg.AutoReconnect:FindFirstChild("Label")),
	}
	-- only on screen in states where the art is hidden by rule (wanted(): SlingUI on / slingshot phase)
	local EXCLUSIVE = {SlingExit = "SlingUI on = art hidden (states: SlingUI.Enabled / SlingLocalPhase)"}
	for name, o in list do
		if o then
			local touching = hit(C, boxOf(o))
			if touching and EXCLUSIVE[name] then
				r.check(name .. " never on screen together", true, "box touches; " .. EXCLUSIVE[name])
			else
				r.check(name .. " no overlap", not touching, fmt(boxOf(o)))
			end
		else r.note(name .. ": not present / zero size") end
	end
	local at = pg:FindFirstChild("AreaTitle")
	local title = at and at:FindFirstChild("Banner") and at.Banner:FindFirstChild("Title")
	if title and title.Text ~= "" then r.check("AreaTitle text no overlap", not hit(C, textBox(title)), fmt(textBox(title))) end
	local tb = pg:FindFirstChild("TopbarStandard")
	if tb then
		for _, d in tb:GetDescendants() do
			if d.Name == "IconButton" and d:IsA("GuiObject") and d.AbsoluteSize.X > 0 then r.check("Topbar icon no overlap", not hit(C, boxOf(d))) end
		end
	end
	return r.text("envelope " .. (mode or "full"))
end

---------------------------------------------------------------- motion (MUST 2): visible figure-8, smooth (sub-pixel) steps
function S.motion(seconds)
	local r = report()
	r.check("art is up", isUp(), state().why)
	local float = root().Body.Float
	local seen, distinct, frames = {}, 0, 0
	local x0, x1, y0, y1, a0, a1 = math.huge, -math.huge, math.huge, -math.huge, math.huge, -math.huge
	local outlineOff = 0 -- v3: the black twin rides exactly with the egg (bob + hop + tilt)
	local conn = RunService.RenderStepped:Connect(function()
		frames += 1
		local e, o = float.Egg, float.EggOutline
		local ec, oc = e.AbsolutePosition + e.AbsoluteSize / 2, o.AbsolutePosition + o.AbsoluteSize / 2
		outlineOff = math.max(outlineOff, (ec - oc).Magnitude, math.abs(e.Rotation - o.Rotation))
		local c = float.AbsolutePosition + float.AbsoluteSize / 2
		local key = ("%.3f,%.3f"):format(float.Position.X.Scale + float.Position.X.Offset, float.Position.Y.Scale + float.Position.Y.Offset)
		if not seen[key] then seen[key] = true distinct += 1 end
		x0, x1, y0, y1 = math.min(x0, c.X), math.max(x1, c.X), math.min(y0, c.Y), math.max(y1, c.Y)
		a0, a1 = math.min(a0, float.Rotation), math.max(a1, float.Rotation)
	end)
	task.wait(seconds or 4.2)
	conn:Disconnect()
	local s = state().s
	r.note(("%d frames, %d distinct Float positions; drift %.1f px, bob %.1f px (screen), sway %.1f deg; s %.3f"):format(frames, distinct, x1 - x0, y1 - y0, a1 - a0, s))
	r.check("smooth: a new Float position on most frames (no whole-pixel stair-steps)", distinct >= frames * 0.8, ("%d / %d"):format(distinct, frames))
	r.check("left-right drift ~ 8 x s px (+-4)", math.abs((x1 - x0) - 8 * s) <= 1.5, ("%.1f vs %.1f"):format(x1 - x0, 8 * s))
	r.check("up-down bob ~ 10 x s px (+-5)", math.abs((y1 - y0) - 10 * s) <= 1.5, ("%.1f vs %.1f"):format(y1 - y0, 10 * s))
	r.check("sway ~ 6 deg (+-3)", math.abs((a1 - a0) - 6) <= 0.6, ("%.2f"):format(a1 - a0))
	r.check("EggOutline rides exactly with the Egg (centre + rotation)", outlineOff < 0.05, ("max diff %.3f"):format(outlineOff))
	return r.text("motion")
end

---------------------------------------------------------------- countdown (scope change 2026-10-21: StarterEndsAt)
-- Owner 2026-10-21: no background - bold stroked text ON the egg (Float.Timer, rides the egg's bob / hop / tilt).
-- Server first: player:SetAttribute("StarterEndsAt", os.time() + 86400) ("long") or os.time() + 3000 ("urgent").
local function rotV(v, a) return Vector2.new(v.X * math.cos(a) - v.Y * math.sin(a), v.X * math.sin(a) + v.Y * math.cos(a)) end
local function corners(c, hw, hh, a)
	local t = {}
	for _, k in {{-1, -1}, {1, -1}, {1, 1}, {-1, 1}} do table.insert(t, c + rotV(Vector2.new(k[1] * hw, k[2] * hh), a)) end
	return t
end
local function sat(A, B) -- two convex polygons overlap?
	for _, P in {A, B} do
		for i = 1, #P do
			local p1, p2 = P[i], P[i % #P + 1]
			local n = Vector2.new(p2.Y - p1.Y, p1.X - p2.X)
			local amin, amax, bmin, bmax = math.huge, -math.huge, math.huge, -math.huge
			for _, q in A do local d = q:Dot(n) amin, amax = math.min(amin, d), math.max(amax, d) end
			for _, q in B do local d = q:Dot(n) bmin, bmax = math.min(bmin, d), math.max(bmax, d) end
			if amax < bmin or bmax < amin then return false end
		end
	end
	return true
end
local function gapCirclePoly(c, r, P) -- distance from the circle's edge to the polygon (negative = overlap)
	local pos, neg = false, false
	local best = math.huge
	for i = 1, #P do
		local p1, p2 = P[i], P[i % #P + 1]
		local e = p2 - p1
		local t = math.clamp((c - p1):Dot(e) / e:Dot(e), 0, 1)
		best = math.min(best, (p1 + e * t - c).Magnitude)
		local cr = e.X * (c.Y - p1.Y) - e.Y * (c.X - p1.X)
		if cr > 0 then pos = true elseif cr < 0 then neg = true end
	end
	if not (pos and neg) then return -r - best end -- (centre inside the polygon)
	return best - r
end
function S.timer(mode, layout)
	local r = report()
	local g = hud()
	if layout == "compact" then -- the phone layout: TestScale 0.56 + TestCompact (its timer is x1.25)
		g:SetAttribute("TestScale", 0.56)
		g:SetAttribute("TestCompact", true)
		task.wait(0.6)
	end
	local st = state()
	r.check("art is up while the countdown runs", isUp(), st.why)
	local float = root().Body.Float
	local timer = float.Timer
	r.check("rides the egg: a Float child (the motion group), no background", timer.Parent == float and timer.BackgroundTransparency == 1
		and #timer:GetChildren() == 3) -- UIStroke + UIGradient + TimerScale only
	if mode == "urgent" then
		r.check("under 1 h: m:ss", timer.Text:match("^%d+:%d%d$") ~= nil, timer.Text)
		r.check("urgent flag", st.urgent == true)
	else
		r.check("h:mm:ss", timer.Text:match("^%d+:%d%d:%d%d$") ~= nil, timer.Text)
		r.check("not urgent: no pulse", st.urgent == false)
	end
	r.note(("left %.1f s -> %s"):format(st.left, timer.Text))
	local strokeObj = timer:FindFirstChildOfClass("UIStroke")
	r.check("GothamBlack + thick black stroke (3 at base size)", timer.Font == Enum.Font.GothamBlack and strokeObj and strokeObj.Thickness >= 3
		and strokeObj.Color == Color3.new(0, 0, 0))
	local changes = 0
	local c1 = timer:GetPropertyChangedSignal("Text"):Connect(function() changes += 1 end)
	local minS, maxS = math.huge, -math.huge
	-- [1] = the TextBounds line box, [2] = the ink (cap height ~0.72 em); both + the 3 px stroke. (AbsolutePosition already
	-- includes the ancestors' rotation: centres as they are, orientations = own + Float (+ Price) rotation.)
	local gIcon, gL, gM, aHit = {math.huge, math.huge}, {math.huge, math.huge}, {math.huge, math.huge}, {false, false}
	local offX, offY = {math.huge, -math.huge}, {math.huge, -math.huge}
	local c2 = RunService.RenderStepped:Connect(function()
		local sc = timer.TimerScale.Scale
		minS, maxS = math.min(minS, sc), math.max(maxS, sc)
		local fa = math.rad(float.Rotation)
		local function centre(o) return o.AbsolutePosition + o.AbsoluteSize / 2 end
		local k = uiScaleOf(timer)
		local stroke = 3 * k
		local price = float.Price
		local pa = math.rad(price.Rotation) + fa
		local ro, am = price.RobuxOutline, price.Amount
		local aw, ak = math.min(am.TextBounds.X, am.AbsoluteSize.X), uiScaleOf(am)
		-- the amount is Left-aligned: its text centre = the label's left edge + aw / 2 along the price's (rotated) x axis
		local amC = centre(am) + rotV(Vector2.new(aw / 2 - am.AbsoluteSize.X / 2, 0), pa)
		for i, hh in {timer.TextBounds.Y / 2, 0.36 * timer.TextSize * k} do
			local T = corners(centre(timer), timer.TextBounds.X / 2 + stroke, hh + stroke, fa)
			gIcon[i] = math.min(gIcon[i], gapCirclePoly(centre(ro), ro.AbsoluteSize.X * 0.46, T))
			local ah = i == 1 and am.TextBounds.Y / 2 or 0.36 * am.TextSize * ak
			local A = corners(amC, aw / 2 + 3 * ak, ah + 3 * ak, pa)
			if sat(T, A) then aHit[i] = true end
			gL[i] = math.min(gL[i], gapCirclePoly(centre(float.PotionL), float.PotionL.AbsoluteSize.X * 0.42, T))
			gM[i] = math.min(gM[i], gapCirclePoly(centre(float.PotionM), float.PotionM.AbsoluteSize.X * 0.42, T))
		end
		-- the timer's offset from the egg centre in Float px (un-rotate the screen difference)
		local d = rotV(centre(timer) - centre(float.Egg), -fa) / uiScaleOf(float.Egg)
		offX = {math.min(offX[1], d.X), math.max(offX[2], d.X)}
		offY = {math.min(offY[1], d.Y), math.max(offY[2], d.Y)}
	end)
	task.wait(6.6) -- one full pop cycle (6 s) + margin
	c1:Disconnect()
	c2:Disconnect()
	local fontPx = timer.TextSize * uiScaleOf(timer) -- the font size on screen (read before the forced layout is released)
	if layout == "compact" then
		g:SetAttribute("TestScale", nil)
		g:SetAttribute("TestCompact", nil)
		task.wait(0.6)
	end
	r.check("text writes <= 1 per second (6.6 s)", changes >= 6 and changes <= 8, changes)
	if mode == "urgent" then
		r.check("last hour: pulse (x1.00..x1.10)", maxS / minS > 1.07 and maxS / minS < 1.11, ("%.3f..%.3f"):format(minS, maxS))
		local c0 = timer.UIGradient.Color.Keypoints
		r.check("last hour: a real red (-> 255, 60, 50)", c0[#c0].Value == Color3.fromRGB(255, 60, 50), tostring(c0[#c0].Value))
	else
		r.check("no pulse above 1 h", maxS - minS < 1e-3, ("%.3f..%.3f"):format(minS, maxS))
	end
	r.check("TextFits", timer.TextFits)
	local px = timer.TextBounds.Y
	r.note(("time text %.1f px tall on screen (s %.3f, compact %s)"):format(px, st.s, tostring(st.compact)))
	r.check("on the shell's lower band: egg centre + (0, 33) in Float px, every frame (+-0.5)", offX[1] >= -0.5 and offX[2] <= 0.5
		and offY[1] >= 32.5 and offY[2] <= 33.5, ("x %.2f..%.2f, y %.2f..%.2f"):format(offX[1], offX[2], offY[1], offY[2]))
	r.note(("neighbours over a full pop cycle, screen px (line box / ink): Robux icon gap %.1f / %.1f, amount touched %s / %s, Money potion gap %.1f / %.1f, Hatch potion gap %.1f / %.1f")
		:format(gIcon[1], gIcon[2], tostring(aHit[1]), tostring(aHit[2]), gL[1], gL[2], gM[1], gM[2]))
	r.check("price: the timer's ink + stroke never reaches the Robux icon", gIcon[2] > 0, ("%.1f px"):format(gIcon[2]))
	r.check("price: the amount's ink never touched", not aHit[2])
	-- the Money / Hatch potions sit BEHIND the egg (ZIndex 3) and the timer is drawn over them: the accepted timer band
	-- (coordinator ruling 2026-10-21) crosses their peeking parts - notes, not checks
	r.note(("Money potion vs the timer (ink): %.1f px, Hatch: %.1f px (negative = the timer runs over the potion's peeking part)"):format(gL[2], gM[2]))
	r.check("readable: font >= 10.5 px on screen", fontPx >= 10.5, ("font %.1f px, TextBounds.Y %d"):format(fontPx, px))
	return r.text("timer " .. tostring(mode or "long") .. " " .. (layout or "full"))
end
-- Server: os.time() + 20 first; this waits for the end: hides by itself at 0 and stays hidden
function S.expiry()
	local r = report()
	local st = state()
	r.note(("left %.1f s, shown %s"):format(st.left, tostring(st.shown)))
	local t = waitFor(function() return not root().Visible end, st.left + 3)
	local st2 = state()
	r.check("hid by itself at 0", t ~= nil and st2.why == "countdown", ("after %.1f s, why %s"):format(t or -1, tostring(st2.why)))
	r.check("hid within 0.5 s of the end", t ~= nil and t <= st.left + 0.5, t and ("%.2f s vs %.2f s left"):format(t, st.left))
	local back = false
	local conn = RunService.RenderStepped:Connect(function() if root().Visible then back = true end end)
	pg.MainMenu.OpenPage:Fire("Shop")
	task.wait(0.6)
	pg.MainMenu.CloseWindow:Fire()
	task.wait(4)
	conn:Disconnect()
	r.check("stays hidden after the end (5 s, window open/close)", not back, state().why)
	return r.text("expiry")
end

---------------------------------------------------------------- states (10.3.3 + MUST 11.3)
function S.states()
	local r = report()
	local cam = workspace.CurrentCamera
	r.check("start: art is up", isUp(), state().why)
	local mm = pg.MainMenu
	local function toggle(name, on, off, backTimeout)
		on()
		task.wait(0.5)
		local st = state()
		r.check(name .. " -> hidden", not root().Visible and not st.shown, st.why)
		off()
		if cam.CameraType ~= Enum.CameraType.Custom then r.note("CameraType is " .. tostring(cam.CameraType) .. " before asserting visible") end
		local back = waitFor(isUp, backTimeout or 1.2)
		r.check(name .. " undone -> back", back ~= nil, back and ("%.2f s"):format(back) or state().why)
		task.wait(0.3)
	end
	toggle("MainMenu Shop window", function() mm.OpenPage:Fire("Shop") end, function() mm.CloseWindow:Fire() end, 1.5)
	toggle("Potions side panel (column away)", function() pg.PetsEggsUI.OpenPanel:Fire("Potions") end,
		function() mm.OpenPage:Fire("Shop") task.wait(0.4) mm.CloseWindow:Fire() end, 1.5)
	toggle("SlingLocalPhase Aiming", function() player:SetAttribute("SlingLocalPhase", "Aiming") end, function() player:SetAttribute("SlingLocalPhase", nil) end)
	toggle("InHatchCinematic", function() player:SetAttribute("InHatchCinematic", true) end, function() player:SetAttribute("InHatchCinematic", nil) end)
	toggle("IntroPlaying", function() player:SetAttribute("IntroPlaying", true) end, function() player:SetAttribute("IntroPlaying", nil) end)
	toggle("InWeatherCutscene", function() player:SetAttribute("InWeatherCutscene", true) end, function() player:SetAttribute("InWeatherCutscene", nil) end)
	toggle("CameraType Scriptable", function() cam.CameraType = Enum.CameraType.Scriptable end, function() cam.CameraType = Enum.CameraType.Custom end)
	if pg:FindFirstChild("SlingUI") then
		toggle("SlingUI.Enabled (launch / flight)", function() pg.SlingUI.Enabled = true end, function() pg.SlingUI.Enabled = false end)
	else r.note("SlingUI not present") end
	if pg:FindFirstChild("InventoryUI") then
		toggle("InventoryUI.Enabled", function() pg.InventoryUI.Enabled = true end, function() pg.InventoryUI.Enabled = false end)
	else r.note("InventoryUI not present") end
	toggle("StarterPackUI popup (TestOpen)", function() pg.StarterPackUI.TestOpen:Fire() end, function() pg.StarterPackUI.Enabled = false end)
	if pg:FindFirstChild("OfflineUI") then
		toggle("OfflineUI.Enabled", function() pg.OfflineUI.Enabled = true end, function() pg.OfflineUI.Enabled = false end)
	end
	for _, n in {"FreeGiftUI", "UpgradeUI", "SellUI", "StreakCelebrate"} do
		local g = pg:FindFirstChild(n)
		if g and g:IsA("ScreenGui") and not g.Enabled then
			toggle(n .. ".Enabled", function() g.Enabled = true end, function() g.Enabled = false end)
		end
	end
	-- PC: the Speed offer is bottom-left - the art stays up
	local so = pg:FindFirstChild("SpeedOffer")
	if so then
		local was = so.Enabled
		so.Enabled = true
		task.wait(0.5)
		r.check("SpeedOffer on (PC) -> stays VISIBLE", isUp(), state().why)
		so.Enabled = was
		task.wait(0.3)
	end
	-- last: the tutorial switch (TutorialClient listens to it)
	toggle("TutorialExtra 3", function() player:SetAttribute("TutorialExtra", 3) end, function() player:SetAttribute("TutorialExtra", 0) end)
	return r.text("states")
end

---------------------------------------------------------------- flicker (MUST 4 / 11.4)
function S.flicker()
	local r = report()
	local off = pg:FindFirstChild("OfflineUI")
	r.check("OfflineUI exists", off ~= nil)
	if not off then return r.text("flicker") end
	r.check("start: art is up", isUp(), state().why)
	-- fast: hidden first, then toggling every 0.1 s for 2 s must never show it
	off.Enabled = true
	task.wait(0.5)
	r.check("hidden before the fast toggles", not root().Visible)
	local everVisible, maxScale = false, 0
	local conn = RunService.RenderStepped:Connect(function()
		if root().Visible then everVisible = true end
		maxScale = math.max(maxScale, root().Body.ShowScale.Scale)
	end)
	for i = 1, 20 do off.Enabled = not off.Enabled task.wait(0.1) end
	conn:Disconnect()
	r.check("fast toggles: Root.Visible never true", not everVisible)
	r.check("fast toggles: ShowScale never > 0.05", maxScale <= 0.05, maxScale)
	off.Enabled = false
	local back = waitFor(isUp, 1.5)
	r.check("back after the fast toggles", back ~= nil, back)
	task.wait(0.6)
	-- slow: 1 s on, 1 s off = exactly one hide + one show; the show starts >= 0.30 s after the close, no snap
	local hides, shows, lastShown = 0, 0, state().shown
	local closedAt, showAt
	-- (Studio can run at 15 fps when unfocused: the per-frame step is judged at 60 fps = max rate x 1/60 s)
	local maxStep, maxRate, showFrames, lastScale, showing = 0, 0, 0, root().Body.ShowScale.Scale, false
	local frames = 0
	local conn2 = RunService.RenderStepped:Connect(function(dt)
		frames += 1
		local sh = state().shown
		if sh ~= lastShown then
			if sh then shows += 1 showAt = showAt or os.clock() showing = true else hides += 1 end
			lastShown = sh
		end
		local sc = root().Body.ShowScale.Scale
		if showing then
			showFrames += 1
			maxStep = math.max(maxStep, sc - lastScale)
			maxRate = math.max(maxRate, (sc - lastScale) / math.max(dt, 1e-3))
		end
		if showing and sc >= 0.999 then showing = false end
		lastScale = sc
	end)
	local t0 = os.clock()
	off.Enabled = true
	task.wait(1)
	off.Enabled = false
	closedAt = os.clock()
	task.wait(1.2)
	conn2:Disconnect()
	local fps = frames / (os.clock() - t0)
	r.check("slow cycle: exactly one hide", hides == 1, hides)
	r.check("slow cycle: exactly one show", shows == 1, shows)
	r.check("show starts >= 0.30 s after the modal closed", showAt and showAt - closedAt >= 0.30, showAt and ("%.3f s"):format(showAt - closedAt))
	r.check("show: ShowScale step < 0.2 per frame (at 60 fps)", maxRate / 60 < 0.2,
		("max rate %.2f/s = %.3f per 60-fps frame; raw %.3f per frame at %.0f fps"):format(maxRate, maxRate / 60, maxStep, fps))
	r.check("show: no snap (the show spans more than 1 frame)", showFrames > 1, showFrames)
	return r.text("flicker")
end

---------------------------------------------------------------- hover / press (MUST 9 / 11.5)
function S.hover()
	local r = report()
	local ti = hud().TestInput
	local T = Enum.UserInputType
	r.check("start: art is up", isUp(), state().why)
	-- touch: MouseEnter + press + release never leave it "hovered"
	ti:Invoke("Enter", T.Touch)
	r.check("touch Enter: not hovered, target 1", state().hovered == false and state().hoverTarget == 1)
	ti:Invoke("Down", T.Touch)
	r.check("Down: target 0.94", state().hoverTarget == 0.94)
	ti:Invoke("Up", T.Touch)
	local st = state()
	r.check("touch Up: hoverTarget == 1 (not 1.05)", st.hoverTarget == 1 and st.hovered == false, st.hoverTarget)
	local pops0 = st.pops
	local took = waitFor(function() return state().pops > pops0 end, 6.5)
	r.check("a pop within 6 s after the touch", took ~= nil, took and ("%.2f s"):format(took))
	-- mouse: hover 1.05, the pop pauses while hovered, leave = 1
	ti:Invoke("Enter", T.MouseMovement)
	st = state()
	r.check("mouse Enter: hovered, target 1.05", st.hovered == true and st.hoverTarget == 1.05)
	task.wait(0.4)
	r.check("hover spring reached ~1.05", math.abs(state().hoverCur - 1.05) < 0.01, state().hoverCur)
	ti:Invoke("Down", T.MouseButton1)
	ti:Invoke("Up", T.MouseButton1)
	r.check("mouse Up while hovered: 1.05", state().hoverTarget == 1.05)
	local pp = state().pops
	task.wait(6.6)
	r.check("no pop while hovered (6.6 s)", state().pops == pp, state().pops - pp)
	ti:Invoke("Leave", T.MouseMovement)
	r.check("Leave: target 1, not hovered", state().hoverTarget == 1 and state().hovered == false)
	-- hide / show resets the spring (the popup opening over a hovered art)
	ti:Invoke("Enter", T.MouseMovement)
	local off = pg.OfflineUI
	off.Enabled = true
	task.wait(0.3)
	st = state()
	r.check("hide resets hover", st.hoverTarget == 1 and st.hovered == false and st.hoverCur == 1)
	off.Enabled = false
	waitFor(isUp, 1.5)
	-- Activate (the art's tap / click handler) opens the popup
	ti:Invoke("Activate")
	task.wait(0.3)
	r.check("Activate opens the popup", pg.StarterPackUI.Enabled == true)
	pg.StarterPackUI.Enabled = false
	waitFor(isUp, 1.5)
	return r.text("hover")
end

---------------------------------------------------------------- content (10.3.4 / 10.3.8, client part)
function S.content()
	local r = report()
	local body = root().Body
	local float = body.Float
	local amount = float.Price.Amount
	local cap = body.Caption
	local EGG = require(game.ReplicatedStorage.StreakConfig).EGG_ICONS
	local restricted = player:GetAttribute("StarterRestricted") ~= false
	r.note(("StarterEgg %s, restricted %s, egg image %s"):format(tostring(player:GetAttribute("StarterEgg")), tostring(restricted), float.Egg.Image))
	if restricted then
		r.check("restricted: cash hero, CashBack hidden", float.Egg.Image:find("88694661500877") ~= nil and not float.CashBack.Visible)
	else
		r.check("egg hero = EGG_ICONS[StarterEgg]", float.Egg.Image == EGG[player:GetAttribute("StarterEgg") or "TideEgg"], float.Egg.Image)
		r.check("CashBack shown", float.CashBack.Visible)
	end
	r.check("shadow = egg image", float.EggShadow.Image == float.Egg.Image)
	-- v3 (visual review MUST 1-3): the hero on top, a black outline twin, the halo tinted per egg
	local ol = float.EggOutline
	r.check("EggOutline = the hero's image, black, hero size + 8", ol.Image == float.Egg.Image and ol.ImageColor3 == Color3.new(0, 0, 0)
		and ol.ImageTransparency == 0 and ol.Size.X.Offset == float.Egg.Size.X.Offset + 8,
		("%d vs %d"):format(ol.Size.X.Offset, float.Egg.Size.X.Offset))
	r.check("hero size: egg 96 / restricted cash 86", float.Egg.Size.X.Offset == (restricted and 86 or 96), float.Egg.Size.X.Offset)
	local z = {}
	for _, n in {"SunA", "SunB", "PotionBack", "CashBack", "PotionL", "PotionM", "EggShadow", "EggOutline", "Egg", "Star1", "Star2", "Timer", "Price"} do
		z[n] = float[n].ZIndex
	end
	r.check("ZIndex: suns 1-2 < side items 3 < shadow 4 < outline 5 < egg 6 < stars 7 < timer 8 < price 9",
		z.SunA == 1 and z.SunB == 2 and z.PotionBack == 3 and z.CashBack == 3 and z.PotionL == 3 and z.PotionM == 3 and z.EggShadow == 4
			and z.EggOutline == 5 and z.Egg == 6 and z.Star1 == 7 and z.Star2 == 7 and z.Timer == 8 and z.Price == 9)
	local TINT = {MagmaEgg = Color3.fromRGB(255, 120, 40), VoidEgg = Color3.fromRGB(180, 100, 255)}
	local want = (not restricted and TINT[player:GetAttribute("StarterEgg") or ""]) or Color3.fromRGB(255, 110, 200)
	r.check("SunB tinted per egg (Magma orange / Void violet / else pink)", float.SunB.ImageColor3 == want, tostring(float.SunB.ImageColor3))
	r.check("halo: SunB 0.30, SunA ~0.14 (+-0.04)", math.abs(float.SunB.ImageTransparency - 0.3) < 1e-3 and math.abs(float.SunA.ImageTransparency - 0.14) <= 0.041,
		("%.3f / %.3f"):format(float.SunA.ImageTransparency, float.SunB.ImageTransparency))
	local popup = pg.StarterPackUI
	local was = popup:GetAttribute("Price")
	r.check("popup publishes Price", was ~= nil, was)
	r.check("Amount = popup Price", amount.Text == tostring(was), amount.Text)
	popup:SetAttribute("Price", "45")
	task.wait()
	r.check("Price attribute 45 -> Amount 45", amount.Text == "45", amount.Text)
	popup:SetAttribute("Price", "149")
	task.wait(0.1)
	r.check("3-digit price fits (TextSize 16)", amount.TextSize == 16 and amount.TextFits and amount.TextBounds.X <= amount.AbsoluteSize.X + 0.5,
		("%s / %s"):format(tostring(amount.TextBounds), tostring(amount.AbsoluteSize)))
	popup:SetAttribute("Price", "1499")
	task.wait(0.1)
	r.check("4-digit price fits (TextSize 13)", amount.TextSize == 13 and amount.TextFits and amount.TextBounds.X <= amount.AbsoluteSize.X + 0.5,
		("%s / %s"):format(tostring(amount.TextBounds), tostring(amount.AbsoluteSize)))
	popup:SetAttribute("Price", was)
	task.wait(0.1)
	r.check("Amount.TextFits", amount.TextFits)
	r.check("Amount TextBounds.X <= AbsoluteSize.X", amount.TextBounds.X <= amount.AbsoluteSize.X + 0.5, ("%s / %s"):format(tostring(amount.TextBounds), tostring(amount.AbsoluteSize)))
	r.check("no TextScaled under the UIScales (MaxTextSize would cap the SCREEN size: text would not grow with the art)", (function()
		for _, d in root():GetDescendants() do if d:IsA("TextLabel") and d.TextScaled then return false end end
		return true
	end)())
	if cap.Visible then
		r.check("Caption.TextFits", cap.TextFits)
		r.check("Caption TextBounds.X <= AbsoluteSize.X", cap.TextBounds.X <= cap.AbsoluteSize.X + 0.5, ("%s / %s"):format(tostring(cap.TextBounds), tostring(cap.AbsoluteSize)))
		r.note(("caption text %d px, price text %d px tall on screen (layout scale %.3f)"):format(cap.TextBounds.Y, amount.TextBounds.Y, state().s))
	end
	r.check("the v1 tile is gone", pg.PetsEggsUI.RightTiles:FindFirstChild("StarterPackTile") == nil)
	-- every text: GothamBlack + a black stroke; every image: Fit
	local okFont, okFit = true, true
	for _, d in root():GetDescendants() do
		if d:IsA("TextLabel") and (d.Font ~= Enum.Font.GothamBlack or not d:FindFirstChildOfClass("UIStroke")) then okFont = false end
		if d:IsA("ImageLabel") and d.ScaleType ~= Enum.ScaleType.Fit then okFit = false end
	end
	r.check("Check-UI: GothamBlack + stroke on every text", okFont)
	r.check("Check-UI: every image Fit", okFit)
	-- the popup shows the same price as the art
	popup.TestOpen:Fire()
	task.wait(0.4)
	local bp = popup:FindFirstChild("Price", true)
	local buyPrice
	for _, d in popup:GetDescendants() do if d:IsA("TextLabel") and d.Name == "Price" then buyPrice = d end end
	r.check("popup price = art price", buyPrice and buyPrice.Text == amount.Text, buyPrice and buyPrice.Text)
	popup.Enabled = false
	waitFor(isUp, 1.5)
	return r.text("content")
end

---------------------------------------------------------------- overlaps: transients forced visible (MUST 11.1)
-- art yielded = hidden; else its rect must not touch the transient's rect
function S.overlaps(part)
	local r = report()
	local function verdict(name, rectOf)
		task.wait(0.5)
		local st = state()
		local b = rectOf()
		local touching = st.rect and b and hit(st.rect, b)
		r.check(name .. ": no overlap or yielded", (not touching) or not root().Visible,
			("%s art %s %s"):format(touching and "touching" or "clear", root().Visible and "up" or "hidden", b and fmt(b) or "?"))
		return touching
	end
	if part == nil or part == "rebirth" then
		local rr = pg.RebirthReadyUI.Banner
		local pop = rr:FindFirstChild("Pop")
		local sc = pop and pop:FindFirstChildOfClass("UIScale")
		local oldVis, oldScale = rr.Visible, sc and sc.Scale
		rr.Visible = true
		if sc then sc.Scale = 1.1 end
		verdict("REBIRTH READY (pop 1.1)", function() return boxOf(pop or rr) end)
		rr.Visible = oldVis
		if sc then sc.Scale = oldScale end
		task.wait(0.4)
	end
	if part == nil or part == "area" then
		local at = pg.AreaTitle
		local banner, title = at.Banner, at.Banner.Title
		local longest = ""
		for _, z in CollectionService:GetTagged("Area") do
			local n = tostring(z:GetAttribute("AreaName") or "") .. (z:GetAttribute("Emoji") and (" " .. z:GetAttribute("Emoji")) or "")
			if #n > #longest then longest = n end
		end
		local old = {banner.Visible, title.Text, title.TextTransparency, banner.Position}
		banner.Visible = true
		title.Text = longest ~= "" and longest or "CELESTIAL SKY"
		title.TextTransparency = 0
		r.note("AreaTitle text: " .. title.Text)
		verdict("AreaTitle text (TextBounds)", function() return textBox(title) end)
		r.note(("AreaTitle full strip %s (passes under the art at DisplayOrder 0 < 1)"):format(fmt(boxOf(banner))))
		banner.Visible, title.Text, title.TextTransparency, banner.Position = old[1], old[2], old[3], old[4]
		task.wait(0.4)
	end
	if part == nil or part == "admin" then -- fire the server's banner first (see the header), then run this part
		local bar = pg.AdminBanner.Banner
		local t = waitFor(function() return bar.Visible end, 3)
		r.check("admin banner on screen", t ~= nil)
		if t then
			verdict("AdminBanner long message", function() return boxOf(bar) end)
			r.note(("admin text: %d chars, bar %s"):format(#bar.Text.Text, fmt(boxOf(bar))))
		end
	end
	if part == nil or part == "reconnect" then
		-- stand-in for AutoReconnect.Label (the real one needs AutoReconnectTest before Play, which also arms real
		-- reconnect requests): the same path, size and DisplayOrder, placed where AutoReconnectConfig.place pushes it on
		-- a phone (right above the column), then where it sits on PC (above the weather row)
		local real = pg:FindFirstChild("AutoReconnect")
		r.check("no real AutoReconnect gui in this session (stand-in safe)", real == nil)
		if real == nil then
			local g = Instance.new("ScreenGui")
			g.Name = "AutoReconnect"
			g.DisplayOrder = 4
			g.IgnoreGuiInset = false
			g.ResetOnSpawn = false
			local l = Instance.new("TextLabel")
			l.Name = "Label"
			l.AnchorPoint = Vector2.new(1, 1)
			l.BackgroundTransparency = 1
			l.Font = Enum.Font.GothamBlack
			l.TextSize = 26
			l.TextColor3 = Color3.new(1, 1, 1)
			l.Text = "Auto Reconnect: 14:29"
			local k = deviceScale()
			l.Size = UDim2.fromOffset(math.floor(292 * k), math.floor(32 * k))
			l.Visible = false
			l.Parent = g
			g.Parent = pg
			local tiles = pg.PetsEggsUI.RightTiles
			local gy = g.AbsolutePosition.Y
			local right = tiles.AbsolutePosition.X + tiles.AbsoluteSize.X
			l.Position = UDim2.fromOffset(right, tiles.AbsolutePosition.Y - gy - 6 * k) -- the phone push: right above the column
			l.Visible = true
			local touching = verdict("AutoReconnect label above the column (phone push)", function() return boxOf(l) end)
			r.check("  ...and the art YIELDED (hidden)", not root().Visible, touching and "touching" or "clear")
			local row = pg:FindFirstChild("WeatherTiles") and pg.WeatherTiles:FindFirstChild("Row")
			if row then
				l.Position = UDim2.fromOffset(row.AbsolutePosition.X + row.AbsoluteSize.X, row.AbsolutePosition.Y - gy - 6 * k)
			else
				l.Position = UDim2.new(1, -14, 1, -14)
			end
			local back = waitFor(isUp, 1.5)
			r.check("AutoReconnect label at its PC spot -> art back", back ~= nil, back)
			g:Destroy()
			waitFor(isUp, 1.5)
		end
	end
	if part == nil or part == "hatchcard" then
		local hc = pg:FindFirstChild("HatchCard")
		r.note("HatchCard: " .. (hc and hc.ClassName or "not present"))
	end
	return r.text("overlaps " .. tostring(part or "all"))
end

---------------------------------------------------------------- the POPUP hero (visual review SHOULD 1 + owner: "no background on timer")
-- StarterPackClient's pack art: the BIG egg on top with a black twin, the potions + cash BEHIND it, the "ENDS IN" countdown
-- as plain stroked text covering no egg; everything inside the left area x 20-250, y 66-268 (window px, 540x430)
function S.popup(keepOpen)
	local r = report()
	local popup = pg.StarterPackUI
	if not popup.Enabled then popup.TestOpen:Fire() task.wait(0.6) end
	r.check("popup open", popup.Enabled)
	local win = popup.Holder.Window
	local k = win.AbsoluteSize.X / 540
	local wp = win.AbsolutePosition
	local function loc(b) return {(b[1] - wp.X) / k, (b[2] - wp.Y) / k, (b[3] - wp.X) / k, (b[4] - wp.Y) / k} end
	local function rotBox(o, frac) -- the rotated frame's AABB (frac of the size), window px
		local c = o.AbsolutePosition + o.AbsoluteSize / 2
		local th = math.rad(o.Rotation)
		local h = (frac or 1) * o.AbsoluteSize.X / 2 * (math.abs(math.cos(th)) + math.abs(math.sin(th)))
		return loc({c.X - h, c.Y - h, c.X + h, c.Y + h})
	end
	local restricted = player:GetAttribute("StarterRestricted") ~= false
	local egg, outline, cash, sun = win.Egg, win.EggOutline, win.Cash, win.Sunburst
	local ends = win:FindFirstChild("EndsIn")
	r.note(("StarterEgg %s, restricted %s, window scale %.3f"):format(tostring(player:GetAttribute("StarterEgg")), tostring(restricted), k))
	r.check("the old amber tag frame is gone", win:FindFirstChild("OneTime") == nil)
	r.check("ENDS IN: plain text - a TextLabel, no background, GothamBlack, black stroke >= 3",
		ends and ends:IsA("TextLabel") and ends.BackgroundTransparency == 1 and ends.Font == Enum.Font.GothamBlack
			and ends:FindFirstChildOfClass("UIStroke") and ends:FindFirstChildOfClass("UIStroke").Thickness >= 3
			and ends:FindFirstChildOfClass("UIStroke").Color == Color3.new(0, 0, 0))
	if not ends then return r.text("popup") end
	r.check("ENDS IN text format", ends.Text:match("^ENDS IN %d+:%d%d") ~= nil, ends.Text)
	local left = (player:GetAttribute("StarterEndsAt") or 0) - workspace:GetServerTimeNow()
	local kp = ends:FindFirstChildOfClass("UIGradient").Color.Keypoints
	local last = kp[#kp].Value
	if left < 3600 then
		r.check("last hour: a real red gradient (-> 255, 60, 50)", last == Color3.fromRGB(255, 60, 50), tostring(last))
	else
		r.check("warm gold gradient (-> 255, 170, 0)", last == Color3.fromRGB(255, 170, 0), tostring(last))
	end
	r.check("ENDS IN TextFits", ends.TextFits)
	local tb = loc(textBox(ends))
	local st = 3
	tb = {tb[1] - st, tb[2] - st, tb[3] + st, tb[4] + st}
	r.note("ENDS IN ink (+ stroke) " .. fmt(tb))
	-- the hero on top
	local hero = restricted and cash or egg
	r.check(restricted and "restricted: no egg, the cash is the hero" or "the egg is shown", egg.Visible == not restricted)
	r.check("outline twin: the hero's image, black, hero + 8", outline.Image == hero.Image and outline.ImageColor3 == Color3.new(0, 0, 0)
		and math.abs(outline.AbsoluteSize.X - hero.AbsoluteSize.X - 8 * k) < 1)
	local zOk = outline.ZIndex < hero.ZIndex and sun.ZIndex < outline.ZIndex
	for _, d in win:GetChildren() do
		if d.Name:match("^Potion") or (d == cash and not restricted) then zOk = zOk and d.ZIndex < outline.ZIndex end
	end
	r.check("ZIndex: sun < potions + cash < outline < hero < ENDS IN", zOk and ends.ZIndex > hero.ZIndex)
	if not restricted then r.check("the egg ~15% bigger (160 vs 140)", math.abs(egg.AbsoluteSize.X / k - 160) < 1, egg.AbsoluteSize.X / k) end
	-- the egg's ink starts ~8% below its frame top (flame tips): the text must end above it
	local hb = rotBox(outline)
	local inkTop = hb[2] + (restricted and 0.2 or 0.08) * (hb[4] - hb[2])
	r.check("ENDS IN covers no hero (text bottom above the hero's ink top)", tb[4] <= inkTop, ("text bottom %.1f, ink top %.1f"):format(tb[4], inkTop))
	-- inside the left area, clear of the rows / odds caption / header
	local AREA = {20, 66, 250, 268}
	local function inside(b) return b[1] >= AREA[1] - 0.5 and b[2] >= AREA[2] - 0.5 and b[3] <= AREA[3] + 0.5 and b[4] <= AREA[4] + 0.5 end
	local items = {EndsIn = tb, Sunburst = (function() local c = sun.AbsolutePosition + sun.AbsoluteSize / 2 local h = sun.AbsoluteSize.X / 2
		return loc({c.X - h, c.Y - h, c.X + h, c.Y + h}) end)(), Outline = hb, Hero = rotBox(hero)}
	if not restricted then items.Cash = rotBox(cash) end
	for _, d in win:GetChildren() do if d.Name:match("^Potion") and d:IsA("ImageLabel") then items[d.Name] = rotBox(d) end end
	for name, b in items do r.check(name .. " inside x 20-250, y 66-268", inside(b), fmt(b)) end
	local function box(o) return o and o.Visible and loc(boxOf(o)) end
	local others = {EggRow = box(win:FindFirstChild("EggRow")), PotionRow = box(win:FindFirstChild("PotionRow")), CashRow = box(win:FindFirstChild("CashRow")),
		OddsCaption = win.OddsCaption.Visible and loc(textBox(win.OddsCaption)), Header = box(win:FindFirstChild("Header"))}
	for on, ob in others do
		if ob then
			local any = false
			for _, b in items do if hit(b, ob) then any = true end end
			r.check("art clear of " .. on, not any, fmt(ob))
		end
	end
	if not keepOpen then popup.Enabled = false end
	return r.text("popup " .. (restricted and "restricted" or tostring(player:GetAttribute("StarterEgg"))))
end

local function run(section, ...)
	if workspace:GetAttribute("TestFreshSave") ~= true then return "REFUSED: TestFreshSave is not true" end
	if not hud() then return "StarterOfferHud missing" end
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	return f(...)
end
_G.StarterHudTests = run
_G.StarterHudSections = S -- (patch one section without re-pasting the file)
return run
