local pg = game.Players.LocalPlayer.PlayerGui
local canvas = pg.PhoneMock.Canvas
local w = canvas.Window
w.Size = UDim2.fromScale(0.86, 0.86)
-- phone text floor: nothing under 10 px (labels that were max 12-16 get min 10-11)
local n = 0
for _, d in ipairs(w:GetDescendants()) do
	if d:IsA("UITextSizeConstraint") then
		if d.MaxTextSize <= 16 then d.MinTextSize = 10 n += 1 elseif d.MaxTextSize <= 20 then d.MinTextSize = 11 n += 1 end
	end
end
task.wait(0.5)
local out = {}
local function rr(o) local p, s = o.AbsolutePosition, o.AbsoluteSize return string.format("(%d, %d, %d, %d)", p.X, p.Y + 58, s.X, s.Y) end
for _, d in ipairs(w:GetDescendants()) do if d.Name == "Portrait" then table.insert(out, rr(d)) end end
local stage
for _, d in ipairs(w:GetDescendants()) do if d.Name == "Stage" then stage = d end end
local close
for _, d in ipairs(w.Face:GetChildren()) do if d.Name == "Close" then close = d end end
return "n=" .. n .. "\nWIN " .. rr(w) .. "\nRECTS " .. table.concat(out, ", ") .. "\nSTAGE " .. rr(stage) .. "\nCLOSE " .. rr(close)