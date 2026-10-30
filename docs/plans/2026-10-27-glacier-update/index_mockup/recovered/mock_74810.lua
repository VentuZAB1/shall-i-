local pg = game.Players.LocalPlayer.PlayerGui
local canvas = pg.PhoneMock.Canvas
local w = canvas.Window
-- undo the forced text floor (it wrapped words like THUNDE-R)
for _, d in ipairs(w:GetDescendants()) do if d:IsA("UITextSizeConstraint") then d.MinTextSize = 1 end end
-- phone: below Roblox's 0..36 px top bar, bottom margin 8 px -> 342 px tall (0.877 of 390)
w.AnchorPoint = Vector2.new(0.5, 0)
w.Position = UDim2.new(0.5, 0, 0, 40)
w.Size = UDim2.fromScale(0.877, 0.877)
task.wait(0.5)
local out = {}
local function rr(o) local p, s = o.AbsolutePosition, o.AbsoluteSize return string.format("(%d, %d, %d, %d)", p.X, p.Y + 58, s.X, s.Y) end
for _, d in ipairs(w:GetDescendants()) do if d.Name == "Portrait" then table.insert(out, rr(d)) end end
local stage
for _, d in ipairs(w:GetDescendants()) do if d.Name == "Stage" then stage = d end end
local close = w.Face:FindFirstChild("Close")
return "WIN " .. rr(w) .. "\nRECTS " .. table.concat(out, ", ") .. "\nSTAGE " .. rr(stage) .. "\nCLOSE " .. rr(close)