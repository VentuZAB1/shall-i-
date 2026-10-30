local pg = game.Players.LocalPlayer.PlayerGui
local canvas = pg.PhoneMock.Canvas
for _, c in ipairs(canvas:GetChildren()) do if c.Name == "Win" or c.Name == "Window" then c:Destroy() end end
local src = pg.MainMenu.Window
local w = src:Clone()
w.Name = "Window"
for _, d in ipairs(w:GetDescendants()) do if d:IsA("LocalScript") or d:IsA("Script") then d:Destroy() end end
w.AnchorPoint = Vector2.new(0.5, 0.5)
w.Position = UDim2.fromScale(0.5, 0.5)
w.Size = UDim2.fromScale(0.94, 0.94)
w.Visible = true
w.Parent = canvas
task.wait(0.5)
local out = {}
local function rr(o) local p, s = o.AbsolutePosition, o.AbsoluteSize return string.format("(%d, %d, %d, %d)", p.X, p.Y + 58, s.X, s.Y) end
for _, d in ipairs(w:GetDescendants()) do if d.Name == "Portrait" then table.insert(out, rr(d)) end end
local stage
for _, d in ipairs(w:GetDescendants()) do if d.Name == "Stage" then stage = d end end
return "WIN " .. rr(w) .. "\nRECTS " .. table.concat(out, ", ") .. "\nSTAGE " .. rr(stage)