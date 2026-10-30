local C = Color3.fromRGB
local pg = game.Players.LocalPlayer.PlayerGui
local n = 0
for _, root in ipairs({pg.PhoneMock.Canvas.Window, pg.MainMenu.Window}) do
	for _, d in ipairs(root:GetDescendants()) do
		if d:IsA("UIGradient") then
			local k = d.Color.Keypoints
			if #k == 2 and k[1].Value == C(255, 208, 0) and k[2].Value == C(255, 140, 0) then
				d.Color = ColorSequence.new(C(214, 98, 0), C(190, 68, 0)) n += 1
				local holder = d.Parent.Parent
				local depth = holder:FindFirstChild("Depth") if depth then depth.BackgroundColor3 = C(110, 40, 0) end
			end
		end
	end
end
task.wait(0.3)
return n