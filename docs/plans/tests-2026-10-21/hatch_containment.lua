-- hatch_containment.lua v2 (2026-10-21; Gift plan 8.3 + review MUST 1/2 + SHOULD 13; popup/Shop plan 7.5 + review
-- SHOULD 19). Client datamodel. Defines _G.HatchContain(label, cfg) and runs it once (Gift, cfg = nil).
-- cfg = nil is exactly the Gift run (the Gift window open): roots Window.HatchBack / HatchFront / Body.GiftPage.
-- cfg fields (the Shop / the Starter Pack popup): root (the canvas: ShopPage / popup Canvas), win (Window / Holder),
-- back, front (the chrome layers), safe (the box for HatchShell = MainMenu), screen (the gui for onTop), hud (left-HUD
-- clearance at native scale), probes() (extra {button, x, y} hit probes), testRoot (where HatchTestPulse / HatchTestHover
-- are set), pulse (the pulse-pass value: 1.05 Gift, 1.02 Shop / popup), centred (the popup: Holder centre = MainMenu box
-- centre +-1), textClear (review SHOULD 19), allowOnTop (other guis allowed on top).
-- It walks every visible GuiObject under back / front / root (screen px; k(o) = product of UIScales; TOL = 1 px) in three
-- passes: layout (testRoot HatchTestPulse = 1), pulse (HatchTestPulse = cfg.pulse), hover (HatchTestHover = true).
-- Checks: contain (child + its Border stroke inside the parent; HatchHolder = union of its parts; HatchShell = inside the
-- safe box; v2: a ScrollingFrame's children are checked against its CANVAS box - the window width x the canvas
-- height), textV, tileOverlap, tileGap, hitInWindow / hitOverlap / hitFirst (v2: HatchBlocker objects are not hits;
-- hits inside a ScrollingFrame count only when their centre is in its visible box), textScaled / textFits / font /
-- textWidth / textMin, drawOrder, corner, hud, onTop, heroRim / heroChips / iconTop (Gift only), and v2:
-- scrollFit (a scroll's canvas child is no wider than its visible window), centred, priceGroup (every price button:
-- the visible Pre + Robux + Price group centred in its face +-1.5 px, its stroked glyphs inside the face), textClear
-- (no text glyph + stroke meets a gloss button holder in the same container, at rest and at hover).
-- v3 (2026-10-21, RIS plan 8.2: Settings / Index / Rebirth): _G.HatchRISCfg(name, opts) (root = Body.<name>Page, probes =
-- every shown GuiButton's centre under the page, pulse 1.04 Rebirth / 1.03 Index / none Settings); new checks nowNext
-- (inside every HatchTile "nn" group: Now < Arrow < Next in x order without overlap, the Arrow's centre y = the Now box's
-- +-1 logical) and barFill (every HatchBar trough's Fill sits 3 +-1 logical px inside it on top / bottom / left and ends
-- >= 3 - 1 px before its right edge); cfg.noOnTop skips onTop (review SHOULD 9: the forced big-PC scales, as the Shop
-- ledger ruled for 1.45). textFill stays a FAIL on every non-Gift page.
-- v4 (2026-10-22, UWF plan 8.2 + review MUST 1): _G.HatchUWFCfg(name, opts) for the standalone Free Gift / Welcome Back /
-- Upgrades windows (cfg.scaleGui = the gui's own HatchTestScale for hud()); new checks rightHud (clear of the PetsEggsUI right
-- tiles) and hotbar (no visible BackpackGui hotbar meets the stroked window).
_G.HatchContain = function(label, cfg)
	local p = game.Players.LocalPlayer
	local pg = p.PlayerGui
	local mm = pg.MainMenu
	local gift = cfg == nil
	cfg = cfg or {}
	local win = cfg.win or mm.Window
	local page = cfg.root or win.Face.Body.GiftPage
	local back, front = cfg.back or win.HatchBack, cfg.front or win.HatchFront
	local safe = cfg.safe or mm
	local screen = cfg.screen or mm
	local testRoot = cfg.testRoot or page
	local useHud = gift or cfg.hud == true
	local allow = {StreakFly = true}
	for _, n in cfg.allowOnTop or {} do allow[n] = true end
	local TS = game:GetService("TextService")
	local GOTHAM = Font.fromEnum(Enum.Font.GothamBlack).Family
	local TOL = 1
	local ws = back.SkinScale.Scale
	local lines, counts, notes = {}, {}, {}
	local total, fails = 0, 0
	local function path(o) return (o:GetFullName():gsub("^.-Window%.", ""):gsub("^.-Holder%.", "Holder.")) end
	local function check(kind, ok, o, msg)
		total += 1
		counts[kind] = counts[kind] or {0, 0}
		counts[kind][1] += 1
		if not ok then
			fails += 1
			counts[kind][2] += 1
			if #lines < 40 then table.insert(lines, ("FAIL %s %s %s"):format(kind, o and path(o) or "?", msg or "")) end
		end
	end
	local function scaleOf(o) local u = o:FindFirstChildOfClass("UIScale") return u and u.Scale or 1 end
	local function k(o)
		local s, x = 1, o
		while x and x:IsA("GuiObject") do s *= scaleOf(x) x = x.Parent end
		return s
	end
	local function shown(o)
		local x = o
		while x and x:IsA("GuiObject") do if not x.Visible then return false end x = x.Parent end
		local sg = o:FindFirstAncestorWhichIsA("LayerCollector")
		return sg == nil or sg.Enabled
	end
	local function strokeOf(o)
		for _, c in o:GetChildren() do
			if c:IsA("UIStroke") and c.Enabled and c.ApplyStrokeMode == Enum.ApplyStrokeMode.Border then return c.Thickness end
		end
		return 0
	end
	local function rawBox(o) local a, s = o.AbsolutePosition, o.AbsoluteSize return {a.X, a.Y, a.X + s.X, a.Y + s.Y} end
	local function rotBox(o)
		local b = rawBox(o)
		local r = math.rad(o.AbsoluteRotation)
		if math.abs(r) < 1e-4 or o:GetAttribute("HatchRadial") then return b end
		local cx, cy, hw, hh = (b[1] + b[3]) / 2, (b[2] + b[4]) / 2, (b[3] - b[1]) / 2, (b[4] - b[2]) / 2
		local c, s = math.abs(math.cos(r)), math.abs(math.sin(r))
		local w2, h2 = hw * c + hh * s, hw * s + hh * c
		return {cx - w2, cy - h2, cx + w2, cy + h2}
	end
	local function grow(b, d) return {b[1] - d, b[2] - d, b[3] + d, b[4] + d} end
	local function union(a, b) return {math.min(a[1], b[1]), math.min(a[2], b[2]), math.max(a[3], b[3]), math.max(a[4], b[4])} end
	local function sbox(o)
		local b = grow(rotBox(o), strokeOf(o) * k(o))
		if o:GetAttribute("HatchHolder") then
			for _, c in o:GetChildren() do
				if c:IsA("GuiObject") and c.Visible and not c:GetAttribute("HatchHit") then b = union(b, grow(rotBox(c), strokeOf(c) * k(c))) end
			end
		end
		return b
	end
	local function inside(a, b) return a[1] >= b[1] - TOL and a[2] >= b[2] - TOL and a[3] <= b[3] + TOL and a[4] <= b[4] + TOL end
	local function fb(b) return ("[%.1f %.1f %.1f %.1f]"):format(b[1], b[2], b[3], b[4]) end
	local function isText(o) return o:IsA("TextLabel") or o:IsA("TextBox") or (o:IsA("TextButton") and not o:GetAttribute("HatchHit") and not o:GetAttribute("HatchBlocker")) end
	-- (v2) the box a ScrollingFrame's child must stay in: its canvas (the visible width x the whole canvas height)
	local function canvasBox(sf)
		local a, cp = sf.AbsolutePosition, sf.CanvasPosition
		return {a.X - cp.X, a.Y - cp.Y, a.X - cp.X + sf.AbsoluteWindowSize.X, a.Y - cp.Y + sf.AbsoluteCanvasSize.Y}
	end
	local function parentBox(o)
		local par = o.Parent
		if par:IsA("ScrollingFrame") then return canvasBox(par) end
		return rawBox(par)
	end
	-- (v2) the nearest ScrollingFrame above o, if any
	local function scrollOf(o)
		local x = o.Parent
		while x and x:IsA("GuiObject") do
			if x:IsA("ScrollingFrame") then return x end
			x = x.Parent
		end
	end
	local function visibleInScroll(o)
		local sf = scrollOf(o)
		if not sf then return true end
		local b, v = rawBox(o), rawBox(sf)
		local cx, cy = (b[1] + b[3]) / 2, (b[2] + b[4]) / 2
		return cx >= v[1] and cx <= v[1] + sf.AbsoluteWindowSize.X and cy >= v[2] and cy <= v[2] + sf.AbsoluteWindowSize.Y
	end

	local objs = {}
	local function collect(o)
		for _, c in o:GetChildren() do
			if c:IsA("GuiObject") and c.Visible then table.insert(objs, c) collect(c) end
		end
	end
	for _, r in {back, front, page} do if r.Visible then table.insert(objs, r) collect(r) end end

	-- (fix round) claim shards / fly-texts are destroyed while a run is going: drop anything no longer parented
	local function prune()
		local live = {}
		for _, o in objs do if o.Parent then table.insert(live, o) end end
		objs = live
	end
	local function contain()
		prune()
		for _, o in objs do
			if not o.Parent then continue end
			if o:GetAttribute("HatchHit") or o:GetAttribute("HatchClipped") then continue end
			local parent = o.Parent
			if o:GetAttribute("HatchShell") then
				check("contain", inside(sbox(o), rawBox(safe)), o, "vs ScreenGui " .. fb(sbox(o)))
			elseif isText(o) then
				local b, pb = rawBox(o), parentBox(o)
				local st = o:FindFirstChildOfClass("UIStroke")
				local half = o.TextBounds.Y / 2 + (st and st.Thickness or 0) * k(o)
				local cy = (b[2] + b[4]) / 2
				check("textV", cy - half >= pb[2] - TOL and cy + half <= pb[4] + TOL, o, ("%.1f..%.1f in %.1f..%.1f"):format(cy - half, cy + half, pb[2], pb[4]))
			elseif parent:GetAttribute("HatchHolder") and (o.Name == "Side" or o.Name == "Face") then
				check("contain", inside(rotBox(o), rawBox(parent)), o, fb(rotBox(o)) .. " in " .. fb(rawBox(parent)))
			else
				check("contain", inside(sbox(o), parentBox(o)), o, fb(sbox(o)) .. " in " .. fb(parentBox(o)))
			end
		end
	end
	local function tiles(layout)
		local groups = {}
		for _, o in objs do
			local g = o:GetAttribute("HatchTile")
			if g then groups[g] = groups[g] or {} table.insert(groups[g], o) end
		end
		for g, list in groups do
			for i = 1, #list do
				for j = i + 1, #list do
					local a, b = sbox(list[i]), sbox(list[j])
					local over = a[1] < b[3] - TOL and b[1] < a[3] - TOL and a[2] < b[4] - TOL and b[2] < a[4] - TOL
					check("tileOverlap", not over, list[i], "x " .. list[j].Name .. " (" .. g .. ")")
					if layout then
						local ra, rb = rawBox(list[i]), rawBox(list[j])
						local gap = math.max(rb[1] - ra[3], ra[1] - rb[3], rb[2] - ra[4], ra[2] - rb[4])
						local need = (list[i]:GetAttribute("HatchGap") or 8) * k(list[i].Parent)
						check("tileGap", gap >= need - TOL, list[i], ("%.1f < %.1f vs %s"):format(gap, need, list[j].Name))
					end
				end
			end
		end
	end
	local function hits()
		local list = {}
		for _, o in objs do if o:GetAttribute("HatchHit") and visibleInScroll(o) then table.insert(list, o) end end
		local wb = rawBox(win)
		for _, h in list do check("hitInWindow", inside(rawBox(h), wb), h, fb(rawBox(h)) .. " in " .. fb(wb)) end
		for i = 1, #list do
			for j = i + 1, #list do
				local a, b = rawBox(list[i]), rawBox(list[j])
				local over = a[1] < b[3] - TOL and b[1] < a[3] - TOL and a[2] < b[4] - TOL and b[2] < a[4] - TOL
				check("hitOverlap", not over, list[i], "x " .. path(list[j]))
			end
		end
		-- the first GuiButton under each probe point is the expected one (AbsolutePosition coordinates, as they are)
		local function firstButton(x, y)
			for _, o in pg:GetGuiObjectsAtPosition(x, y) do
				if o:IsA("GuiButton") and shown(o) then return o end
			end
		end
		local function centre(o) local b = rawBox(o) return (b[1] + b[3]) / 2, (b[2] + b[4]) / 2 end
		local probes = {{front.CloseHit, centre(front.CloseHit)}}
		if gift then
			table.insert(probes, {page.Tabs.HitPlaytime, centre(page.Tabs.HitPlaytime)})
			local dv, pv = page:FindFirstChild("DailyView"), page:FindFirstChild("PlaytimeView")
			if dv and dv.Visible then
				local c1 = dv.Card1
				local s = k(c1)
				table.insert(probes, {c1.Face.Button.Face, centre(c1.Face.Button.Face)})
				table.insert(probes, {c1.Hit, c1.AbsolutePosition.X + 20 * s, c1.AbsolutePosition.Y + 20 * s})
				table.insert(probes, {dv.Card7.Face.Button.Face, centre(dv.Card7.Face.Button.Face)})
			end
			if pv and pv.Visible then
				local s1 = pv.Slot1
				local s = k(s1)
				table.insert(probes, {s1.Face.Button.Face, centre(s1.Face.Button.Face)})
				table.insert(probes, {s1.Hit, s1.AbsolutePosition.X + 20 * s, s1.AbsolutePosition.Y + 20 * s})
				local skipHit, skipAll = pv:FindFirstChild("SkipHit", true), pv:FindFirstChild("SkipAll", true)
				if skipHit and skipHit.Visible then table.insert(probes, {skipHit, centre(skipAll)}) end
			end
		end
		if cfg.probes then
			for _, pr in cfg.probes() do
				if pr[1] and shown(pr[1]) and visibleInScroll(pr[1]) then
					local x, y = pr[2], pr[3]
					if not x then x, y = centre(pr[1]) end
					table.insert(probes, {pr[1], x, y, pr[4]})
				end
			end
		end
		for _, pr in probes do
			local got = firstButton(pr[2], pr[3])
			check("hitFirst", got == pr[1], pr[1], (pr[4] and (pr[4] .. ": ") or "") .. "got " .. (got and path(got) or "nil"))
		end
	end
	local function glyphBox(o) -- a text's glyphs (TextBounds, screen px) placed by its alignment
		local b = rawBox(o)
		local tb = o.TextBounds
		local w, h = math.min(tb.X, b[3] - b[1]), math.min(tb.Y, b[4] - b[2])
		local x0 = o.TextXAlignment == Enum.TextXAlignment.Left and b[1] or o.TextXAlignment == Enum.TextXAlignment.Right and b[3] - w or (b[1] + b[3]) / 2 - w / 2
		local y0 = (b[2] + b[4]) / 2 - h / 2
		return {x0, y0, x0 + w, y0 + h}
	end
	local function texts()
		prune()
		for _, o in objs do
			if o:IsA("TextLabel") and o.Text ~= "" then
				check("textScaled", not o.TextScaled, o)
				-- (v2.1) a TextTruncate label (the gift picker's names, review MUST 7) may not fit by design: it ends
				-- in "..." inside its own box, so its drawn width is the box width
				local trunc = o.TextTruncate ~= Enum.TextTruncate.None
				if not trunc then check("textFits", o.TextFits, o, o.Text) end
				check("font", o.FontFace.Family == GOTHAM, o, o.FontFace.Family)
				local kk = k(o)
				local tw = TS:GetTextSize(o.Text, o.TextSize, Enum.Font.GothamBlack, Vector2.new(10000, 10000)).X * kk
				if trunc then tw = math.min(tw, o.AbsoluteSize.X) end
				local b, pb = rawBox(o), parentBox(o)
				local x0 = o.TextXAlignment == Enum.TextXAlignment.Left and b[1] or o.TextXAlignment == Enum.TextXAlignment.Right and b[3] - tw or (b[1] + b[3]) / 2 - tw / 2
				local st = o:FindFirstChildOfClass("UIStroke")
				local sw = (st and st.Thickness or 0) * kk
				check("textWidth", x0 - sw >= pb[1] - TOL and x0 + tw + sw <= pb[3] + TOL, o, ("'%s' %.1f..%.1f in %.1f..%.1f"):format(o.Text, x0 - sw, x0 + tw + sw, pb[1], pb[3]))
				local min = o:GetAttribute("HatchMin") or 16
				check("textMin", o.TextSize * kk >= min * ws - 0.01, o, ("%s: %.2f < %.2f"):format(o.Text, o.TextSize * kk, min * ws))
				-- (v2.2, popup/Shop fix round, visual review MUST 1) the spec's 83 % rule for every line of copy: its glyphs
				-- use at most 83 % of (box - 2 x stroke). Skipped: TextTruncate labels and boxes that hug their text
				-- (HatchHug: prices, now > next, section titles). The Gift window (cfg nil) is frozen: its lines are notes.
				if not trunc and not o:GetAttribute("HatchHug") then
					local fill = tw / math.max(1, (b[3] - b[1]) - 2 * sw)
					if gift then
						if fill > 0.83 + 0.005 then table.insert(notes, ("note: Gift textFill %s '%s' %.0f%%"):format(path(o), o.Text, fill * 100)) end
					else
						check("textFill", fill <= 0.83 + 0.005, o, ("'%s' %.0f%% of its box"):format(o.Text, fill * 100))
					end
				end
			end
		end
	end
	local function drawOrder()
		for _, o in objs do
			if (o.Name:match("^Card%d$") or o.Name:match("^Slot%d+$")) and o:GetAttribute("HatchHolder") then
				local face = o:FindFirstChild("Face")
				for _, rn in {"Ring", "RingGlow"} do
					local ring = o:FindFirstChild(rn, true)
					if ring then
						check("drawOrder", ring.Parent == face, ring, "parent " .. ring.Parent.Name)
						for _, other in {"DayPill", "TimePill", "Tag", "Chip1", "Chip2", "Button"} do
							local o2 = face:FindFirstChild(other)
							if o2 then check("drawOrder", ring.ZIndex < o2.ZIndex, ring, other .. " z " .. o2.ZIndex .. " <= ring z " .. ring.ZIndex) end
						end
					elseif rn == "Ring" then
						check("drawOrder", false, o, "no Ring")
					end
				end
			end
		end
	end
	local function cornerR(o)
		local c = o:FindFirstChildOfClass("UICorner")
		if not c then return 0 end
		local s = o.AbsoluteSize
		local r = math.min(s.X, s.Y) * c.CornerRadius.Scale + c.CornerRadius.Offset * k(o)
		return math.min(r, math.min(s.X, s.Y) / 2)
	end
	-- corners: pixel snapping moves both boxes, so a rounded outline that sits exactly ON the parent's arc (the inset
	-- rim frames of D11) may read up to ~1.4 px out: the corner check uses 1.5 px
	local CTOL = 1.5
	local function insideRR(px, py, b, R)
		if px < b[1] - CTOL or px > b[3] + CTOL or py < b[2] - CTOL or py > b[4] + CTOL then return false end
		local cx, cy = math.clamp(px, b[1] + R, b[3] - R), math.clamp(py, b[2] + R, b[4] - R)
		return (px - cx) ^ 2 + (py - cy) ^ 2 <= (R + CTOL) ^ 2
	end
	-- a Frame that draws nothing (no background, no stroke) is only a container: its box corners are invisible
	local function drawsNothing(o)
		return o:IsA("Frame") and o.BackgroundTransparency >= 1 and strokeOf(o) == 0 and not o:GetAttribute("HatchHolder")
	end
	local function corners()
		prune()
		for _, o in objs do
			if isText(o) or o:GetAttribute("HatchHit") or o:GetAttribute("HatchClipped") or o:GetAttribute("HatchRadial") or o:GetAttribute("HatchBlocker") then continue end
			if math.abs(o.AbsoluteRotation) > 0.01 or drawsNothing(o) then continue end
			if o:IsA("ImageLabel") and o.ScaleType ~= Enum.ScaleType.Fit then continue end -- glows: soft discs, transparent corners
			local parent = o.Parent
			if parent:GetAttribute("HatchHolder") and (o.Name == "Side" or o.Name == "Face") then continue end
			local ref = parent
			if parent == front then ref = back.Face elseif parent.Name == "Badges" then ref = parent.Parent:FindFirstChild("Face") end
			if not ref or drawsNothing(ref) then continue end
			local R = cornerR(ref)
			if R <= 0 then continue end
			local b = sbox(o)
			local part = o:GetAttribute("HatchHolder") and (o:FindFirstChild("Face") or o) or o
			local r = cornerR(part) + strokeOf(part) * k(part)
			r = math.min(r, (b[3] - b[1]) / 2, (b[4] - b[2]) / 2)
			local pb = rawBox(ref)
			local ok, worst = true, nil
			for _, cn in {{b[1] + r, b[2] + r, -1, -1}, {b[3] - r, b[2] + r, 1, -1}, {b[1] + r, b[4] - r, -1, 1}, {b[3] - r, b[4] - r, 1, 1}} do
				for a = 0, 90, 15 do
					local t = math.rad(a)
					local px, py = cn[1] + cn[3] * r * math.cos(t), cn[2] + cn[4] * r * math.sin(t)
					if not insideRR(px, py, pb, R) then ok = false worst = ("(%.1f,%.1f) R %.1f"):format(px - pb[1], py - pb[2], R) end
				end
			end
			check("corner", ok, o, worst)
		end
	end
	local function hud()
		if not useHud then return end
		local test = (cfg.scaleGui or mm):GetAttribute("HatchTestScale") -- (v4) a standalone window has its own switch
		if type(test) == "number" then return end
		local gs, ga = mm.AbsoluteSize, mm.AbsolutePosition
		local wb = rawBox(win)
		local s = ws
		local function right(o) return o and o.Visible and (o.AbsolutePosition.X - ga.X + o.AbsoluteSize.X) or 0 end
		local sp = pg:FindFirstChild("SpeedUI")
		local clear = math.max(right(mm.Menu), right(sp and sp.Enabled and sp:FindFirstChild("Holder"))) + 6
		check("hud", wb[1] - ga.X - 3.5 * s >= clear - TOL or (wb[1] - ga.X) >= clear - TOL, win, ("left %.1f < %.1f"):format(wb[1] - ga.X, clear))
		check("hud", wb[2] - ga.Y >= 6 - TOL and wb[4] - ga.Y <= gs.Y - 6 + TOL and wb[3] - ga.X <= gs.X - 8 + TOL, win, fb(wb) .. " gui " .. tostring(gs))
	end
	-- (v4, UWF plan 8.2) rightHud: a standalone window's stroked right edge <= the PetsEggsUI right tiles' left - 6 while
	-- they are on screen (native scale only); hotbar (review MUST 1): no visible BackpackGui hotbar meets the stroked window
	local function rightHud()
		if not cfg.uwf then return end
		local test = (cfg.scaleGui or mm):GetAttribute("HatchTestScale")
		if type(test) == "number" then return end
		local pe = pg:FindFirstChild("PetsEggsUI")
		local rt = pe and pe.Enabled and pe:FindFirstChild("RightTiles", true)
		if not (rt and rt:IsA("GuiObject") and rt.Visible) then return end
		local ga = mm.AbsolutePosition
		local x = rt.AbsolutePosition.X - ga.X
		if x >= mm.AbsoluteSize.X or x <= mm.AbsoluteSize.X / 2 then return end
		local wb = rawBox(win)
		local r = wb[3] - ga.X + 3.5 * ws
		check("rightHud", r <= x - 6 + TOL, win, ("stroked right %.1f > tiles %.1f - 6"):format(r, x))
	end
	local function hotbar()
		if not cfg.uwf then return end
		local bp = pg:FindFirstChild("BackpackGui")
		local ok = true
		local msg
		if bp and bp.Enabled then
			local wb = grow(rawBox(win), 3.5 * ws)
			for _, o in bp:GetDescendants() do
				if o:IsA("GuiObject") and shown(o) and o.Name ~= "Backpack" then
					local b = rawBox(o)
					local inset = game:GetService("GuiService"):GetGuiInset().Y
					local dy = (bp.IgnoreGuiInset and -inset or 0) + ((cfg.screen and cfg.screen.IgnoreGuiInset) and inset or 0)
					if b[1] < wb[3] and b[3] > wb[1] and b[2] + dy < wb[4] and b[4] + dy > wb[2] then ok = false msg = o:GetFullName() break end
				end
			end
		end
		check("hotbar", ok, win, msg or "")
	end
	local function onTop()
		if cfg.noOnTop then return end
		local s = ws
		local wb = grow(rawBox(win), 3.5 * s)
		local function drawn(o)
			if not shown(o) then return false end
			if o.BackgroundTransparency < 1 then return true end
			if (o:IsA("ImageLabel") or o:IsA("ImageButton")) and o.Image ~= "" and o.ImageTransparency < 1 then return true end
			if (o:IsA("TextLabel") or o:IsA("TextButton")) and o.Text ~= "" and o.TextTransparency < 1 then return true end
			if o:IsA("ViewportFrame") then return true end
			return false
		end
		local bad = {}
		local step = 24 * s
		local y = wb[2] + 1
		while y < wb[4] do
			local x = wb[1] + 1
			while x < wb[3] do
				for _, o in pg:GetGuiObjectsAtPosition(x, y) do
					if drawn(o) then
						local sg = o:FindFirstAncestorWhichIsA("LayerCollector")
						if not (sg == screen or (sg and allow[sg.Name])) then bad[sg and sg.Name or "?"] = (bad[sg and sg.Name or "?"] or 0) + 1 end
						break
					end
				end
				x += step
			end
			y += step
		end
		local n = 0
		local msg = {}
		for name, c in bad do n += c table.insert(msg, name .. " x" .. c) end
		check("onTop", n == 0, win, table.concat(msg, ", "))
	end

	-- (2026-10-21 visual review MUST 1) the Day 7 button's stroked box stays >= 1.5 LOGICAL px inside PrismRim's inner box
	-- (4, 4, 214, 327) and >= 1.5 px below the stroked chips, in every pass (at rest, at the 1.05 pulse, at hover 1.04)
	local function heroButton()
		local dv = page:FindFirstChild("DailyView")
		if not (dv and dv.Visible) then return end
		local face = dv:FindFirstChild("Card7") and dv.Card7:FindFirstChild("Face")
		local btn = face and face:FindFirstChild("Button")
		local rim = face and face:FindFirstChild("PrismRim")
		if not (btn and rim) then check("heroRim", false, face, "no Button / PrismRim") return end
		local kk = k(face)
		local b, r = sbox(btn), rawBox(rim)
		local m = math.min(b[1] - r[1], b[2] - r[2], r[3] - b[3], r[4] - b[4]) / kk
		check("heroRim", m >= 1.5 - 0.05, btn, ("%.2f logical px from the PrismRim inner edge"):format(m))
		for _, cn in {"Chip1", "Chip2"} do
			local ch = face:FindFirstChild(cn)
			if ch then
				local gap = (b[2] - sbox(ch)[4]) / kk
				check("heroChips", gap >= 1.5 - 0.05, btn, ("%.2f logical px below %s"):format(gap, cn))
			end
		end
	end
	-- (visual review MUST 2) Days 1-6: every Icons.Pop sticker's top is at y 28 or lower (DAY pill 26 + its 2 px outline)
	local function iconTops()
		local dv = page:FindFirstChild("DailyView")
		if not (dv and dv.Visible) then return end
		for d = 1, 6 do
			local card = dv:FindFirstChild("Card" .. d)
			local face, pop = card and card:FindFirstChild("Face"), card and card:FindFirstChild("Pop", true)
			if face and pop then
				local kk = k(face)
				for _, im in pop:GetChildren() do
					if im:IsA("ImageLabel") and not im.Name:match("Shadow$") then
						local top = (im.AbsolutePosition.Y - face.AbsolutePosition.Y) / kk
						check("iconTop", top >= 28 - 0.05, im, ("top %.2f < 28"):format(top))
					end
				end
			end
		end
	end

	---------------------------------------------------------------- v2 checks (the Shop / popup)
	local function scrollFit()
		for _, o in objs do
			if o:IsA("ScrollingFrame") then
				for _, c in o:GetChildren() do
					if c:IsA("GuiObject") and c.Visible and c.Name == "List" then
						check("scrollFit", c.AbsoluteSize.X <= o.AbsoluteWindowSize.X + TOL, c, ("%.1f > window %.1f"):format(c.AbsoluteSize.X, o.AbsoluteWindowSize.X))
					end
				end
			end
		end
	end
	local function centred()
		if not cfg.centred then return end
		local a, b = rawBox(win), rawBox(mm)
		local cx, cy = (a[1] + a[3]) / 2, (a[2] + a[4]) / 2
		local mx, my = (b[1] + b[3]) / 2, (b[2] + b[4]) / 2
		check("centred", math.abs(cx - mx) <= 1 + TOL and math.abs(cy - my) <= 1 + TOL, win, ("(%.1f, %.1f) vs (%.1f, %.1f)"):format(cx, cy, mx, my))
	end
	local function priceGroups()
		for _, o in objs do
			local face = o:GetAttribute("HatchHolder") and o:FindFirstChild("Face")
			local price = face and face:FindFirstChild("Price")
			local robux = face and face:FindFirstChild("Robux")
			local word = face and face:FindFirstChild("Word")
			if price and robux and word and o.Visible then
				local fbx = rawBox(face)
				local kk = k(face)
				if price.Visible then
					local g = grow(glyphBox(price), 2.5 * kk)
					local pre = face:FindFirstChild("Pre")
					if pre and pre.Visible then g = union(g, grow(glyphBox(pre), 2.5 * kk)) end
					g = union(g, rawBox(robux))
					local gc, fc = (g[1] + g[3]) / 2, (fbx[1] + fbx[3]) / 2
					check("priceGroup", math.abs(gc - fc) <= 1.5 * kk + TOL, o, ("group centre %.1f vs face %.1f ('%s')"):format(gc, fc, price.Text))
					check("priceGroup", inside(g, fbx), o, fb(g) .. " in " .. fb(fbx))
				elseif word.Visible then
					local g = grow(glyphBox(word), 2.5 * kk)
					check("priceGroup", inside(g, fbx), o, ("word '%s' %s in %s"):format(word.Text, fb(g), fb(fbx)))
				end
			end
		end
	end
	local function textClear()
		if not cfg.textClear then return end
		-- every gloss button holder (it has a ButtonScale) against the texts in the same container (the rail Pill is
		-- skipped: the active tab's label sits ON it by design)
		for _, b in objs do
			if b:GetAttribute("HatchHolder") and b:FindFirstChild("ButtonScale") and b.Name ~= "Pill" then
				local bb = sbox(b)
				for _, t in b.Parent:GetChildren() do
					if t:IsA("TextLabel") and t.Visible and t.Text ~= "" then
						local st = t:FindFirstChildOfClass("UIStroke")
						local g = grow(glyphBox(t), (st and st.Thickness or 0) * k(t))
						local over = g[1] < bb[3] - TOL and bb[1] < g[3] - TOL and g[2] < bb[4] - TOL and bb[2] < g[4] - TOL
						check("textClear", not over, t, ("'%s' %s meets %s %s"):format(t.Text, fb(g), b.Name, fb(bb)))
					end
				end
			end
		end
	end

	---------------------------------------------------------------- v3 checks (Settings / Index / Rebirth)
	local function nowNextCheck()
		local groups = {}
		for _, o in objs do
			if o.Parent and o:GetAttribute("HatchTile") == "nn" then
				groups[o.Parent] = groups[o.Parent] or {}
				groups[o.Parent][o.Name] = o
			end
		end
		for par, g in groups do
			local parts = {}
			for _, n in {"Now", "Arrow", "Next"} do if g[n] then table.insert(parts, g[n]) end end
			for i = 1, #parts - 1 do
				local a, b = rawBox(parts[i]), rawBox(parts[i + 1])
				check("nowNext", a[3] <= b[1] + TOL, parts[i], ("ends %.1f after %s starts %.1f"):format(a[3], parts[i + 1].Name, b[1]))
			end
			if g.Now and g.Arrow then
				local a, b = rawBox(g.Now), rawBox(g.Arrow)
				local d = math.abs((a[2] + a[4]) / 2 - (b[2] + b[4]) / 2)
				check("nowNext", d <= k(par) + TOL, g.Arrow, ("arrow centre y %.1f px off the Now box"):format(d))
			end
		end
	end
	local function barFill()
		for _, o in objs do
			if o.Parent and o:GetAttribute("HatchBar") then
				local fill = o:FindFirstChild("Fill")
				if fill and fill.Visible then
					local t, f = rawBox(o), rawBox(fill)
					local kk = k(o)
					local top, bottom, left, right = (f[2] - t[2]) / kk, (t[4] - f[4]) / kk, (f[1] - t[1]) / kk, (t[3] - f[3]) / kk
					check("barFill", math.abs(top - 3) <= 1 and math.abs(bottom - 3) <= 1 and math.abs(left - 3) <= 1 and right >= 2, fill,
						("insets top %.1f bottom %.1f left %.1f right %.1f (logical)"):format(top, bottom, left, right))
				end
			end
		end
	end

	local function frames(n) for _ = 1, n do game:GetService("RunService").RenderStepped:Wait() end end
	testRoot:SetAttribute("HatchTestHover", false)
	testRoot:SetAttribute("HatchTestPulse", 1)
	frames(3)
	contain() tiles(true) hits() texts() drawOrder() corners() hud() onTop() heroButton() iconTops()
	if not gift then scrollFit() centred() priceGroups() textClear() nowNextCheck() barFill() rightHud() hotbar() end
	testRoot:SetAttribute("HatchTestPulse", cfg.pulse or 1.05)
	frames(3)
	contain() tiles(false) hits() heroButton()
	testRoot:SetAttribute("HatchTestPulse", 1)
	testRoot:SetAttribute("HatchTestHover", true)
	frames(10) -- the hover tweens (0.08 s)
	contain() tiles(false) heroButton()
	if not gift then textClear() end
	testRoot:SetAttribute("HatchTestHover", false)
	testRoot:SetAttribute("HatchTestPulse", nil)
	frames(10)
	local parts = {}
	for kind, c in counts do table.insert(parts, kind .. " " .. (c[1] - c[2]) .. "/" .. c[1]) end
	table.sort(parts)
	local seenNote, uniq = {}, {}
	for _, n in notes do if not seenNote[n] then seenNote[n] = true table.insert(uniq, n) end end
	return ("[%s] scale %.4f  checks %d  fails %d\n  %s%s%s"):format(label, ws, total, fails, table.concat(parts, ", "),
		#lines > 0 and ("\n" .. table.concat(lines, "\n")) or "", #uniq > 0 and ("\n  " .. table.concat(uniq, "\n  ")) or "")
end
-- the Shop / popup configs (popup/Shop plan 7.5)
_G.HatchShopCfg = function()
	local pg = game.Players.LocalPlayer.PlayerGui
	local mm = pg.MainMenu
	local win = mm.Window
	local page = win.Face.Body.ShopPage
	return {root = page, win = win, back = win.HatchBack, front = win.HatchFront, safe = mm, screen = mm, hud = true,
		testRoot = page, pulse = 1.02, textClear = true, allowOnTop = {"GiftToast"},
		probes = function()
			local list = {}
			local pk = page:FindFirstChild("GiftPicker")
			-- (v2.1) the open picker is modal: its shade covers the rail and the list, so only its own buttons are probed
			if not (pk and pk.Visible) then
				for i = 1, 5 do local h = page.Rail:FindFirstChild("Hit" .. i) if h then table.insert(list, {h}) end end
				for _, c in page.Scroll.List:GetDescendants() do
					if c.Name == "BuyHit" then table.insert(list, {c, nil, nil, c.Parent.Parent.Name}) end
					if c.Name == "Face" and c:IsA("ImageButton") and c.Parent:GetAttribute("HatchHolder") then table.insert(list, {c, nil, nil, c.Parent.Parent.Parent.Name .. "." .. c.Parent.Name}) end
				end
			end
			if pk and pk.Visible then
				local box = pk.Box
				table.insert(list, {box.Face.CloseHit})
				for _, r in box.Face.Players:GetChildren() do
					local f = r:FindFirstChild("Gift") and r.Gift:FindFirstChild("Face")
					if f and f:IsA("ImageButton") and f.Active then table.insert(list, {f, nil, nil, r.Name}) end
				end
			end
			return list
		end}
end
_G.HatchPopupCfg = function()
	local pg = game.Players.LocalPlayer.PlayerGui
	local g = pg.StarterPackUI
	local h = g.Holder
	return {root = h.Canvas, win = h, back = h.HatchBack, front = h.HatchFront, safe = pg.MainMenu, screen = g, hud = false,
		testRoot = g, pulse = 1.02, centred = true, textClear = true, allowOnTop = {"GiftToast"},
		probes = function()
			return {{h.Canvas.NoThanks.Face}, {h.Canvas.Buy.Face}}
		end}
end
-- (v3, RIS plan 8.2) Settings / Index / Rebirth. opts: noOnTop (the forced big-PC runs, review SHOULD 9; HatchTestScale
-- already skips hud). The root must be the HATCH page (attribute HatchCanvas): a Check-UI fallback page is refused.
_G.HatchRISCfg = function(name, opts)
	opts = opts or {}
	local pg = game.Players.LocalPlayer.PlayerGui
	local mm = pg.MainMenu
	local win = mm.Window
	local page = win.Face.Body:FindFirstChild(name .. "Page")
	assert(page and page:GetAttribute("HatchCanvas") == true, name .. "Page is not the HATCH NIGHT page (no HatchCanvas)")
	return {root = page, win = win, back = win.HatchBack, front = win.HatchFront, safe = mm, screen = mm, hud = true,
		testRoot = page, textClear = true, pulse = ({Rebirth = 1.04, Index = 1.03})[name], allowOnTop = {"GiftToast"},
		noOnTop = opts.noOnTop,
		probes = function()
			local list = {}
			for _, d in page:GetDescendants() do
				if d:IsA("GuiButton") and d.Visible then table.insert(list, {d, nil, nil, d.Parent.Name .. "." .. d.Name}) end
			end
			return list
		end}
end
-- (v4, UWF plan 8.2) the standalone HATCH windows: Free Gift / Welcome Back / Upgrades. root = the gui's Holder.Canvas
-- (must be the HATCH canvas), win = the Holder, the gui's own HatchTestScale (scaleGui), checks + rightHud + hotbar.
_G.HatchUWFCfg = function(name, opts)
	opts = opts or {}
	local pg = game.Players.LocalPlayer.PlayerGui
	local mm = pg.MainMenu
	local gui = pg:FindFirstChild(({FreeGift = "FreeGiftUI", WelcomeBack = "OfflineUI", Upgrades = "UpgradeUI"})[name])
	local holder = gui and gui:FindFirstChild("Holder")
	local canvas = holder and holder:FindFirstChild("Canvas")
	assert(canvas and canvas:GetAttribute("HatchCanvas") == true, name .. " is not the HATCH NIGHT window (no Holder.Canvas HatchCanvas)")
	return {root = canvas, win = holder, back = holder.HatchBack, front = holder.HatchFront, safe = mm, screen = gui, hud = true,
		scaleGui = gui, uwf = true, testRoot = gui, textClear = true, pulse = ({FreeGift = 1.03, Upgrades = 1.04})[name],
		allowOnTop = {"GiftToast"}, noOnTop = opts.noOnTop,
		probes = function()
			local list = {{holder.HatchFront.CloseHit, nil, nil, "CloseHit"}}
			for _, d in canvas:GetDescendants() do
				if d:IsA("GuiButton") and d.Visible then table.insert(list, {d, nil, nil, d.Parent.Name .. "." .. d.Name}) end
			end
			return list
		end}
end
return _G.HatchContain("smoke")
