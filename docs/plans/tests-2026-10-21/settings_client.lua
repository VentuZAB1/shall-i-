-- settings_client.lua (2026-10-21, RIS plan 8.3 + review SHOULD 7): the HATCH NIGHT Settings page (SettingsClient).
-- Client datamodel of a TestFreshSave Play session. Load once (stores _G.SettingsTests), then run sections:
--   return _G.SettingsTests("open")      chrome + canvas + rows
--   ("toggles")  music / sfx / night: the press flips the SERVER-written Settings attribute and back; the label +
--                palette follow; GameSounds (MusicGroup / SFXGroup volume) and DayNightClient (Lighting NightMode +
--                ClockTime) apply it
--   ("volume")   - / + / the bar (TestVolAt = the drag-end path): musicVol 0.9 / 1 / 0.3 / 0; MusicGroup follows
--   ("song")     < / > wrap through 0 (ALL SONGS) .. #TRACKS; every song name fits its box at <= 83 %
--   ("reopen")   closed = no refresh (SettingsRefreshN frozen, a Settings change only marks it dirty); reopen = saved values
--   ("respawn")  run after the Server step `p.Character.Humanoid.Health = 0`: still exactly 1 HATCH SettingsPage, it opens
--   ("save", combo) sets a known combination through the page and returns the JSON the server must have saved; then
--                the Server step settings_save_server.lua (SavePlayerNow + the stored save, read back) compares
--   ("legacy")   own session with Edit workspace TestSettingsLegacy = true: MenuController's Check-UI page, no HatchCanvas
-- Presses are 0.4 s apart (SettingsServer allows 30 changes per 10 s). Every section restores what it changed.
local Players = game:GetService("Players")
local HttpService = game:GetService("HttpService")
local RS = game:GetService("ReplicatedStorage")
local Lighting = game:GetService("Lighting")
local SoundService = game:GetService("SoundService")
local player = Players.LocalPlayer
local pg = player:WaitForChild("PlayerGui")
local mm = pg:WaitForChild("MainMenu")
local win = mm:WaitForChild("Window")
local body = win.Face.Body
local GEAR = "rbxassetid://98060718033874"
local DEFAULTS = {music = true, sfx = true, night = false}
local LABELS = {music = {"ON", "OFF", "lime", "off"}, sfx = {"ON", "OFF", "lime", "off"}, night = {"NIGHT", "DAY", "violet", "gold"}}
local H
do
	local b = RS.BrickUI
	local ok, B = pcall(require, b)
	H = ok and B.Hatch or nil
end

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
local function data()
	local ok, d = pcall(HttpService.JSONDecode, HttpService, player:GetAttribute("Settings") or "")
	return (ok and type(d) == "table") and d or {}
end
local function val(key)
	local v = data()[key]
	if v == nil then v = DEFAULTS[key] end
	return v
end
local function page() return body:FindFirstChild("SettingsPage") end
local function count()
	local n = 0
	for _, c in body:GetChildren() do if c.Name == "SettingsPage" then n += 1 end end
	return n
end
local function waitFor(f, t)
	local t0 = os.clock()
	while os.clock() - t0 < (t or 2) do
		if f() then return true, os.clock() - t0 end
		task.wait(0.05)
	end
	return f(), os.clock() - t0
end
local function open()
	if not (win.Visible and page() and page().Visible) then
		if win.Visible then mm.CloseWindow:Fire() task.wait(0.4) end
		mm.OpenPage:Fire("Settings")
	end
	task.wait(0.7)
end
-- the song names, upper case (SettingsClient's Studio-only page attribute TestTracks = "NAME1|NAME2|...")
local function tracks()
	local list = {}
	for n in ((page() and page():GetAttribute("TestTracks")) or ""):gmatch("[^|]+") do table.insert(list, n) end
	return list
end
local function row(key) return page():FindFirstChild("Row_" .. key) end
local function btnOf(key) -- the Toggle holder of a switch row
	local r = row(key)
	return r and r.Face:FindFirstChild("Toggle")
end
local function palOf(holder) -- the palette name from the Side colour (glossButton.setPalette writes p.side)
	local side = holder and holder:FindFirstChild("Side")
	if not (side and H) then return "?" end
	for name, p in H.PAL do if side.BackgroundColor3 == p.side then return name end end
	return "?"
end
local function labelOf(holder) return holder and holder.Face:FindFirstChild("Label") and holder.Face.Label.Text end
local function press(key)
	page().TestPress:Fire(key)
	task.wait(0.4)
end
local function fillOf(label)
	local st = label:FindFirstChildOfClass("UIStroke")
	return H.textWidth(label.Text, label.TextSize) / (label.Size.X.Offset - 2 * (st and st.Thickness or 0))
end

local S = {}
function S.open()
	local r = report()
	open()
	local front, back = win.HatchFront, win.HatchBack
	local p = page()
	r.check("HatchBack + HatchFront visible", back.Visible and front.Visible)
	r.check("title SETTINGS", front.Title.Text == "SETTINGS", front.Title.Text)
	local tooth = front.Crack:FindFirstChild("Tooth1")
	r.check("band tooth steel-lilac (104,96,176)", tooth and tooth.BackgroundColor3 == Color3.fromRGB(104, 96, 176), tooth and tostring(tooth.BackgroundColor3))
	r.check("header icon = the top-bar gear", front.Icon.Image == GEAR, front.Icon.Image)
	local ar = win.AbsoluteSize.X / math.max(1, win.AbsoluteSize.Y)
	r.check("window AR 740/470 +-0.01", math.abs(ar - 740 / 470) <= 0.01, ("%.4f"):format(ar))
	local cs = p and p:FindFirstChild("CanvasScale")
	r.check("CanvasScale == SkinScale +-0.001", cs and math.abs(cs.Scale - back.SkinScale.Scale) <= 0.001, cs and ("%.4f vs %.4f"):format(cs.Scale, back.SkinScale.Scale))
	r.check("HatchCanvas == true", p and p:GetAttribute("HatchCanvas") == true)
	r.check("exactly 1 SettingsPage in Body", count() == 1, count())
	local ys = {}
	local ok = true
	for i, key in {"music", "volume", "song", "sfx", "night"} do
		local rr = row(key)
		local y = rr and rr.Position.Y.Offset
		table.insert(ys, tostring(y))
		if y ~= 66 + 78 * (i - 1) or rr.Position.X.Offset ~= 10 or rr.Size ~= UDim2.fromOffset(720, 70) then ok = false end
	end
	r.check("rows Row_music..Row_night at y 66 / 144 / 222 / 300 / 378 (720 x 70 at x 10)", ok, table.concat(ys, " "))
	r.check("Check-UI header hidden", not win.Face.Header.Visible and not win.Face.Title.Visible)
	return r.text("open")
end
function S.toggles()
	local r = report()
	open()
	local mg = SoundService:FindFirstChild("MusicGroup")
	local sg = SoundService:FindFirstChild("SFXGroup")
	for _, key in {"music", "sfx", "night"} do
		local old = val(key)
		local clock0 = Lighting.ClockTime
		press(key)
		local ok, t = waitFor(function() return val(key) == not old end, 2)
		r.check(key .. ": press flips the saved value " .. tostring(old) .. " -> " .. tostring(not old), ok, ("%.2f s"):format(t))
		task.wait(0.1)
		local b = btnOf(key)
		local L = LABELS[key]
		local now = val(key)
		r.check(key .. ": label + palette", labelOf(b) == (now and L[1] or L[2]) and palOf(b) == (now and L[3] or L[4]), labelOf(b) .. " " .. palOf(b))
		if key == "music" and mg then r.check("music: MusicGroup.Volume follows", (now and mg.Volume > 0) or (not now and mg.Volume == 0), mg.Volume) end
		if key == "sfx" and sg then r.check("sfx: SFXGroup.Volume follows", (now and sg.Volume == 1) or (not now and sg.Volume == 0), sg.Volume) end
		if key == "night" then
			local okN = waitFor(function() return Lighting:GetAttribute("NightMode") == now and (Lighting.ClockTime ~= clock0 or now == false) end, 2)
			r.check("night: DayNightClient applied (NightMode " .. tostring(now) .. ", ClockTime " .. ("%.1f"):format(Lighting.ClockTime) .. ")", okN)
		end
		press(key)
		local back = waitFor(function() return val(key) == old end, 2)
		task.wait(0.1)
		r.check(key .. ": press again -> back to " .. tostring(old), back and labelOf(b) == (old and L[1] or L[2]) and palOf(b) == (old and L[3] or L[4]), labelOf(b) .. " " .. palOf(b))
		if key == "night" then r.check("night: back to day (ClockTime " .. ("%.1f"):format(Lighting.ClockTime) .. ")", Lighting:GetAttribute("NightMode") == old and math.abs(Lighting.ClockTime - clock0) < 0.01) end
	end
	return r.text("toggles")
end
local function volText() return page().Row_volume.Face.VolBar.Text.Text end
local function volFill() return page().Row_volume.Face.VolBar.Fill end
function S.volume()
	local r = report()
	open()
	local mg = SoundService:FindFirstChild("MusicGroup")
	local function vol() return tonumber(data().musicVol) or 1 end
	if vol() ~= 1 then page().TestVolAt:Fire(1) waitFor(function() return vol() == 1 end, 2) task.wait(0.4) end
	press("volMinus")
	r.check("- : musicVol 0.9, bar 90%", waitFor(function() return vol() == 0.9 end, 2) and volText() == "90%", tostring(vol()) .. " " .. volText())
	press("volPlus")
	r.check("+ : musicVol 1, bar 100%", waitFor(function() return vol() == 1 end, 2) and volText() == "100%", tostring(vol()) .. " " .. volText())
	page().TestVolAt:Fire(0.34)
	task.wait(0.4)
	r.check("bar at 0.34 -> 0.3, 30%", waitFor(function() return vol() == 0.3 end, 2) and volText() == "30%", tostring(vol()) .. " " .. volText())
	local f = volFill()
	-- (UDim offsets are integers: 52.2 is stored as UDim2.fromOffset gives it)
	r.check("30%: Fill width (180 - 6) x 0.3 = 52.2 (as an offset)", f.Visible and f.Size.X.Offset == UDim2.fromOffset(52.2, 0).X.Offset, f.Size.X.Offset)
	if mg and val("music") then r.check("MusicGroup.Volume 0.3", math.abs(mg.Volume - 0.3) < 1e-6, mg.Volume) end
	page().TestVolAt:Fire(0)
	task.wait(0.4)
	r.check("bar at 0 -> 0, Fill hidden, 0%", waitFor(function() return vol() == 0 end, 2) and not volFill().Visible and volText() == "0%", tostring(vol()) .. " " .. volText())
	press("volMinus")
	r.check("- at 0 stays 0", vol() == 0 and volText() == "0%")
	page().TestVolAt:Fire(0.7)
	task.wait(0.4)
	r.check("bar at 0.7 -> 70%", waitFor(function() return vol() == 0.7 end, 2) and volText() == "70%", volText())
	page().TestVolAt:Fire(1)
	task.wait(0.4)
	press("volPlus")
	r.check("restored 1, + at 1 stays 100%", waitFor(function() return vol() == 1 end, 2) and volText() == "100%", volText())
	return r.text("volume")
end
local function songName() return page().Row_song.Face.NameBox.SongName end
function S.song()
	local r = report()
	open()
	local TRACKS = tracks()
	r.check("TestTracks lists the songs", #TRACKS >= 1, #TRACKS)
	local function track() return math.floor(tonumber(data().track) or 0) end
	local guard = 0
	while track() ~= 0 and guard < 12 do press("songNext") guard += 1 end
	r.check("start at 0 ALL SONGS", track() == 0 and songName().Text == "ALL SONGS", songName().Text)
	local f0 = fillOf(songName())
	press("songNext")
	r.check("> : track 1, " .. tostring(TRACKS[1]), waitFor(function() return track() == 1 end, 2) and songName().Text == TRACKS[1], songName().Text)
	local worst = math.max(f0, fillOf(songName()))
	for t = 2, #TRACKS do
		press("songNext")
		waitFor(function() return track() == t end, 2)
		local fill = fillOf(songName())
		worst = math.max(worst, fill)
		r.check(("> : track %d %s fits (%.0f%% of its box, size %d)"):format(t, songName().Text, fill * 100, songName().TextSize), track() == t and songName().Text == TRACKS[t] and fill <= 0.835)
	end
	press("songNext")
	r.check("> from the last wraps to 0 ALL SONGS", waitFor(function() return track() == 0 end, 2) and songName().Text == "ALL SONGS", songName().Text)
	press("songPrev")
	r.check("< from 0 wraps to #TRACKS (" .. #TRACKS .. ")", waitFor(function() return track() == #TRACKS end, 2) and songName().Text == TRACKS[#TRACKS], songName().Text)
	press("songNext")
	r.check("> back to 0", waitFor(function() return track() == 0 end, 2) and songName().Text == "ALL SONGS")
	r.note(("widest song name fill %.0f%%"):format(worst * 100))
	return r.text("song")
end
function S.reopen()
	local r = report()
	open()
	mm.CloseWindow:Fire()
	task.wait(0.5)
	local n0 = page():GetAttribute("SettingsRefreshN")
	task.wait(1)
	r.check("closed, no change: SettingsRefreshN frozen", page():GetAttribute("SettingsRefreshN") == n0, tostring(n0) .. " -> " .. tostring(page():GetAttribute("SettingsRefreshN")))
	-- a Settings change while closed (local attribute) only marks the page dirty
	local was = player:GetAttribute("Settings")
	local d = data()
	d.sfx = not val("sfx")
	player:SetAttribute("Settings", HttpService:JSONEncode(d))
	task.wait(0.3)
	r.check("closed, a Settings change: no refresh while closed", page():GetAttribute("SettingsRefreshN") == n0, page():GetAttribute("SettingsRefreshN"))
	mm.OpenPage:Fire("Settings")
	task.wait(0.7)
	local b = btnOf("sfx")
	r.check("reopen: one refresh, the label shows the new value", page():GetAttribute("SettingsRefreshN") == (n0 or 0) + 1 and labelOf(b) == (d.sfx and "ON" or "OFF"), tostring(page():GetAttribute("SettingsRefreshN")) .. " " .. labelOf(b))
	player:SetAttribute("Settings", was)
	task.wait(0.2)
	local ok = true
	for key, L in LABELS do if labelOf(btnOf(key)) ~= (val(key) and L[1] or L[2]) then ok = false end end
	r.check("restored: every label = the saved value", ok)
	return r.text("reopen")
end
function S.respawn()
	local r = report()
	r.check("exactly 1 SettingsPage after the respawn", count() == 1, count())
	r.check("it is the HATCH page", page() and page():GetAttribute("HatchCanvas") == true)
	open()
	r.check("it opens on the night shell", win.HatchBack.Visible and page().Visible and win.HatchFront.Title.Text == "SETTINGS")
	r.check("MainMenu kept (ResetOnSpawn false)", mm.ResetOnSpawn == false)
	return r.text("respawn")
end
-- combo = {music = bool, sfx = bool, night = bool, musicVol = 0..1, track = 0..n}: pressed through the page; returns the
-- JSON the server must have saved (the Settings attribute after the presses)
function S.save(combo)
	local r = report()
	open()
	combo = combo or {music = false, sfx = false, night = true, musicVol = 0.3, track = #tracks()}
	for _, key in {"music", "sfx", "night"} do
		if val(key) ~= combo[key] then press(key) waitFor(function() return val(key) == combo[key] end, 2) end
	end
	page().TestVolAt:Fire(combo.musicVol)
	task.wait(0.4)
	local function track() return math.floor(tonumber(data().track) or 0) end
	local guard = 0
	while track() ~= combo.track and guard < 12 do press("songNext") waitFor(function() return false end, 0.1) guard += 1 end
	waitFor(function() return (tonumber(data().musicVol) or 1) == combo.musicVol end, 2)
	local d = data()
	local ok = d.music == combo.music and d.sfx == combo.sfx and d.night == combo.night and d.musicVol == combo.musicVol and track() == combo.track
	r.check("the page set the combination", ok, player:GetAttribute("Settings"))
	_G.SettingsExpect = player:GetAttribute("Settings")
	r.note("expected saved JSON: " .. tostring(_G.SettingsExpect))
	return r.text("save")
end
function S.legacy()
	local r = report()
	local okP = waitFor(function() return count() == 1 end, 12)
	r.check("within 12 s exactly 1 SettingsPage", okP and count() == 1, count())
	r.check("it is the Check-UI page (no HatchCanvas)", page() and page():GetAttribute("HatchCanvas") == nil)
	open()
	r.check("open: Check-UI header visible, HatchBack hidden", win.Face.Header.Visible and not win.HatchBack.Visible)
	-- the Check-UI page reads the same saved attribute (its MUSIC row label follows the server-written value)
	local p = page()
	local lab = p:FindFirstChild("music") and p.music:FindFirstChild("Toggle", true)
	lab = lab and lab:FindFirstChild("Label", true)
	r.check("Check-UI MUSIC label = the saved value", lab and lab.Text == (val("music") and "ON" or "OFF"), lab and lab.Text)
	return r.text("legacy")
end
_G.SettingsTests = function(section, ...)
	local f = S[section]
	if not f then return "unknown section " .. tostring(section) end
	local ok, res = pcall(f, ...)
	return ok and res or ("ERROR in " .. section .. ": " .. tostring(res))
end
return "loaded: _G.SettingsTests(section)"
