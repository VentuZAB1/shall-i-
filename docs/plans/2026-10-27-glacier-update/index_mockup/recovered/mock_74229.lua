local C = Color3.fromRGB
local root = game.Players.LocalPlayer.PlayerGui.MainMenu.Window.Face.MockBody
local RAINBOW = ColorSequence.new{
	ColorSequenceKeypoint.new(0.00, C(255, 30, 80)), ColorSequenceKeypoint.new(0.18, C(255, 140, 0)),
	ColorSequenceKeypoint.new(0.35, C(255, 230, 0)), ColorSequenceKeypoint.new(0.52, C(40, 230, 50)),
	ColorSequenceKeypoint.new(0.70, C(0, 210, 255)), ColorSequenceKeypoint.new(0.85, C(90, 60, 255)),
	ColorSequenceKeypoint.new(1.00, C(220, 0, 230)),
}
local ip
for _, f in ipairs(root:GetChildren()) do if f:IsA("Frame") and math.abs(f.Position.X.Scale - 0.73) < 0.001 then ip = f end end
local vals = {"$83.5M/s", "1M KG", "x1", "0.1%"}
for _, c in ipairs(ip:GetChildren()) do
	if c:IsA("Frame") and c.AnchorPoint == Vector2.new(0.5, 0.5) then
		if c.ZIndex == 7 then c.BackgroundColor3 = Color3.new(1, 1, 1) local g = Instance.new("UIGradient") g.Color = RAINBOW g.Rotation = 45 g.Parent = c end
		if c.ZIndex == 8 then c.UIGradient.Color = ColorSequence.new(C(150, 140, 230), C(60, 52, 130)) end
	elseif c:IsA("Frame") and math.abs(c.Position.Y.Scale - 0.527) < 0.001 then c.Visible = true
	elseif c:IsA("Frame") and math.abs(c.Position.Y.Scale - 0.531) < 0.001 then
		c.BackgroundColor3 = C(20, 14, 40)
		local s = c:FindFirstChildOfClass("UIStroke") if s then s:Destroy() end
		c:FindFirstChildOfClass("TextLabel").Text = "GLACIER · MYTHIC · <font color='#7DFF6A'>$x8.8</font>"
	elseif c:IsA("TextLabel") and math.abs(c.Position.Y.Scale - 0.452) < 0.001 then c.Text = "FROSTCROWN DRAGON"
	elseif c:IsA("Frame") and c.Position.Y.Scale >= 0.6 then
		local i = math.floor((c.Position.Y.Scale - 0.62) / 0.088 + 0.5) + 1
		local labels = {}
		for _, t in ipairs(c:GetChildren()) do if t:IsA("TextLabel") then table.insert(labels, t) end end
		table.sort(labels, function(a, b) return a.Position.X.Scale < b.Position.X.Scale end)
		labels[2].Text = i == 1 and ("<font color='#78EB5A'>" .. vals[1] .. "</font>") or vals[i]
	end
end
task.wait(0.4)
return "ok"