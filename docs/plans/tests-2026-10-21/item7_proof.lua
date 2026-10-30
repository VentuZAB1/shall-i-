-- item7_proof.lua (2026-10-21, popup/Shop fix round, perf review item 7: the startup viewport race). Client datamodel.
-- Reports the numbers the race used to change: the viewport, BrickUI.deviceScale(), the left menu's UIScale and right
-- edge, and the Check-UI outlines (Window.Face / Window strokes, a menu tile stroke) with Rebirth, Index and Settings
-- open. On a PC (1519 x 753): deviceScale 1.18, Face stroke 3.5 x 1.18 = 4.13, menu UIScale 1 (or none), never 1.3.
-- Forced case: Edit workspace TestViewport1x1 = n (seconds) before Play: BrickUI reads (1, 1) for n s.
local p = game.Players.LocalPlayer
local mm = p.PlayerGui:WaitForChild("MainMenu")
local B = require(game.ReplicatedStorage.BrickUI)
local win = mm:WaitForChild("Window")
local menu = mm:FindFirstChild("Menu")
local function r2(n) return n and ("%.2f"):format(n) or "nil" end
local us = menu and menu:FindFirstChildOfClass("UIScale")
local tileStroke
if menu then for _, d in menu:GetDescendants() do if d:IsA("UIStroke") then tileStroke = d break end end end
local out = {("viewport %s | deviceScale %s | menu UIScale %s | menu right %s | menu tile stroke %s (%s)"):format(
	tostring(workspace.CurrentCamera.ViewportSize), r2(B.deviceScale()), us and r2(us.Scale) or "none",
	menu and r2(menu.AbsolutePosition.X + menu.AbsoluteSize.X - mm.AbsolutePosition.X) or "nil",
	tileStroke and r2(tileStroke.Thickness) or "nil", tileStroke and tileStroke:GetFullName():gsub("^.-MainMenu%.", "") or "")}
if not _G.ITEM7_NO_OPEN then
	if win.Visible then mm.CloseWindow:Fire() task.wait(0.5) end
	for _, name in {"Rebirth", "Index", "Settings"} do
		mm.OpenPage:Fire(name)
		task.wait(0.7)
		local fs = win.Face:FindFirstChildOfClass("UIStroke")
		local ws = win:FindFirstChildOfClass("UIStroke")
		local hd = win:FindFirstChild("Header", true)
		table.insert(out, ("%s: Face stroke %s | Window stroke %s | Window %s"):format(name, fs and r2(fs.Thickness) or "none",
			ws and r2(ws.Thickness) or "none", tostring(win.AbsoluteSize)))
		mm.CloseWindow:Fire()
		task.wait(0.4)
	end
end
return table.concat(out, "\n")
