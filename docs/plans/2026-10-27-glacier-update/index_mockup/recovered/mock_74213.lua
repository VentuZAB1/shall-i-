local pg = game.Players.LocalPlayer.PlayerGui
local C = Color3.fromRGB
local WHITE = Color3.new(1, 1, 1)
-- phone mock off, PC back on
pg.PhoneMock.Enabled = false
for _, g in ipairs(_G.HiddenGuis or {}) do g.Enabled = true end
for _, n in ipairs({"AdminUI", "AdminBanner", "WaveBanner", "AreaTitle", "InventoryToast", "GiftToast", "ShieldToast"}) do local g = pg:FindFirstChild(n) if g then g.Enabled = false end end
local win = pg.MainMenu.Window
win.Depth.Visible = false
local root = win.Face.MockBody
-- re-select the mythic card (SetInspect left the lynx selected); rebuild selection the clean way
for _, h in ipairs(root:GetChildren()) do
	if h:IsA("Frame") then
		local sc = h:FindFirstChildOfClass("UIScale") if sc then sc:Destroy() end
		local f = h:FindFirstChild("Face")
		if f and f.UIStroke.Enabled then f.UIStroke.Color = C(24, 30, 34) f.UIStroke.Thickness = 3 end
	end
end
-- find the rainbow ring (ZIndex 7 frame with a UIGradient, Size has offset 4)
local ring, card
for _, h in ipairs(root:GetChildren()) do
	if h:IsA("Frame") and h.ZIndex == 7 and h.Size.X.Offset == 4 then ring = h end
end
for _, h in ipairs(root:GetChildren()) do
	local f = h:FindFirstChild("Face")
	if f then for _, t in ipairs(f:GetChildren()) do if t:IsA("TextLabel") and t.Text == "FROSTCROWN DRAGON" then card = h end end end
end
for _, s in ipairs(ring:GetChildren()) do if s:IsA("UIStroke") then s:Destroy() end end
local sel = ring:Clone() sel.Name = "SelectFrame" sel:ClearAllChildren() sel.ZIndex = 6 sel.BackgroundColor3 = WHITE
sel.Size = ring.Size + UDim2.fromOffset(6, 6) sel.Position = ring.Position - UDim2.fromOffset(3, 3)
local c = Instance.new("UICorner") c.CornerRadius = UDim.new(0, 10) c.Parent = sel
sel.Parent = root
for _, o in ipairs({sel, ring, card}) do local s = Instance.new("UIScale") s.Scale = 1.04 s.Parent = o end
-- inspect back to mythic
_G.SetInspectMythic = true
-- footer trough fill -> glacier blue
for _, d in ipairs(root:GetDescendants()) do
	if d:IsA("UIGradient") and d.Parent:IsA("Frame") and d.Parent.Parent and d.Parent.Parent:IsA("Frame") then
		local k = d.Color.Keypoints
		if #k == 2 and k[1].Value == C(255, 200, 0) and k[2].Value == C(255, 106, 0) then d.Color = ColorSequence.new(C(120, 200, 255), C(60, 140, 230)) end
	end
end
return tostring(ring ~= nil) .. " " .. tostring(card ~= nil)