local C = Color3.fromRGB
local WHITE = Color3.new(1, 1, 1)
local OUT = C(24, 30, 34)
local PANEL = C(26, 44, 52)
local HIGH = C(75, 125, 145)
local RAINBOW = ColorSequence.new{
	ColorSequenceKeypoint.new(0.00, C(255, 30, 80)), ColorSequenceKeypoint.new(0.18, C(255, 140, 0)),
	ColorSequenceKeypoint.new(0.35, C(255, 230, 0)), ColorSequenceKeypoint.new(0.52, C(40, 230, 50)),
	ColorSequenceKeypoint.new(0.70, C(0, 210, 255)), ColorSequenceKeypoint.new(0.85, C(90, 60, 255)),
	ColorSequenceKeypoint.new(1.00, C(220, 0, 230)),
}
local canvas = game.Players.LocalPlayer.PlayerGui.PhoneMock.Canvas
local win
for _, c in ipairs(canvas:GetChildren()) do if c:IsA("Frame") then win = c end end
local function corner(o, px) local c = Instance.new("UICorner") c.CornerRadius = UDim.new(0, px or 6) c.Parent = o end
local function stroke(o, t, col) local s = Instance.new("UIStroke") s.Thickness = t s.Color = col or OUT s.ApplyStrokeMode = Enum.ApplyStrokeMode.Border s.Parent = o return s end
local function grad(o, a, b, rot) local g = Instance.new("UIGradient") g.Color = typeof(a) == "ColorSequence" and a or ColorSequence.new(a, b) g.Rotation = rot or 90 g.Parent = o return g end
local function frame(parent, x, y, w, h, col, z)
	local f = Instance.new("Frame") f.BorderSizePixel = 0 f.Position = UDim2.fromScale(x, y) f.Size = UDim2.fromScale(w, h)
	f.BackgroundColor3 = col or PANEL f.ZIndex = z or 6 f.Parent = parent return f
end
local function text(parent, s, x, y, w, h, col, maxPx, z, align)
	local t = Instance.new("TextLabel") t.BackgroundTransparency = 1 t.Font = Enum.Font.GothamBlack t.Text = s t.RichText = true
	t.TextColor3 = col or WHITE t.TextScaled = true t.Position = UDim2.fromScale(x, y) t.Size = UDim2.fromScale(w, h) t.ZIndex = z or 9
	t.TextXAlignment = align or Enum.TextXAlignment.Center t.Parent = parent
	local c = Instance.new("UITextSizeConstraint") c.MaxTextSize = maxPx or 40 c.MinTextSize = 10 c.Parent = t
	local st = Instance.new("UIStroke") st.Thickness = math.clamp((maxPx or 20) / 10, 1.2, 2.5) st.Color = C(0, 0, 0) st.Parent = t
	return t
end
local old = win:FindFirstChild("Sheet") if old then old:Destroy() end
local dim = frame(win, 0, 0.15, 1, 0.85, C(0, 0, 0), 30) dim.Name = "Dim" dim.BackgroundTransparency = 0.45
local sheet = frame(win, 0.40, 0.12, 0.58, 0.81, PANEL, 31) sheet.Name = "Sheet" corner(sheet, 8) stroke(sheet, 3.5)
local sh = frame(sheet, 0, 0, 1, 1, PANEL, 31) sh.BackgroundTransparency = 1 corner(sh, 8) local shs = stroke(sh, 2, HIGH) shs.Transparency = 0.4
-- left: disc with rainbow ring
local ring = frame(sheet, 0.2, 0.42, 0, 0, WHITE, 32) ring.AnchorPoint = Vector2.new(0.5, 0.5) ring.Size = UDim2.new(0, 186, 0, 186) corner(ring, 1000) grad(ring, RAINBOW, nil, 45)
local disc = frame(sheet, 0.2, 0.42, 0, 0, WHITE, 33) disc.AnchorPoint = Vector2.new(0.5, 0.5) disc.Size = UDim2.new(0, 180, 0, 180) corner(disc, 1000) grad(disc, C(150, 140, 230), C(60, 52, 130), 90)
local stage = frame(sheet, 0.2, 0.42, 0, 0, WHITE, 34) stage.AnchorPoint = Vector2.new(0.5, 0.5) stage.Size = UDim2.new(0, 176, 0, 160) stage.BackgroundTransparency = 1
-- right: name, rarity pill, stats
text(sheet, "FROSTCROWN DRAGON", 0.41, 0.06, 0.5, 0.11, WHITE, 18, 35, Enum.TextXAlignment.Left)
local re = frame(sheet, 0.41, 0.19, 0.5, 0.11, WHITE, 34) corner(re, 12) grad(re, RAINBOW, nil, 0)
local rp = frame(sheet, 0.414, 0.197, 0.492, 0.096, C(20, 14, 40), 35) corner(rp, 11)
text(rp, "GLACIER · MYTHIC · <font color='#7DFF6A'>$x8.8</font>", 0.04, 0.14, 0.92, 0.72, WHITE, 14, 36)
local LBL = {"Income (best KG)", "Best weight", "Hatched", "Hatch chance"}
local VAL = {"<font color='#78EB5A'>$83.5M/s</font>", "1M KG", "x1", "0.1%"}
for i = 1, 4 do
	local row = frame(sheet, 0.41, 0.35 + (i - 1) * 0.135, 0.56, 0.115, C(24, 36, 44), 34) corner(row, 8) stroke(row, 2, C(12, 18, 22))
	text(row, LBL[i], 0.04, 0.22, 0.52, 0.56, C(190, 205, 255), 14, 35, Enum.TextXAlignment.Left)
	text(row, VAL[i], 0.56, 0.18, 0.4, 0.64, WHITE, 17, 35, Enum.TextXAlignment.Right)
end
-- own X
local xh = frame(sheet, 0.93, -0.04, 0, 0, C(115, 0, 16), 36) xh.Size = UDim2.fromOffset(40, 40) corner(xh, 4) stroke(xh, 2.5, C(0, 0, 0))
local xf = frame(xh, 0, 0, 1, 1, WHITE, 37) xf.Size = UDim2.new(1, 0, 1, -4) corner(xf, 4) grad(xf, C(255, 125, 175), C(255, 20, 40), 90)
text(xf, "X", 0.1, 0.06, 0.8, 0.86, WHITE, 24, 38)
-- selected card outline under the dim (frostcrown)
task.wait(0.4)
local p, s = stage.AbsolutePosition, stage.AbsoluteSize
return string.format("STAGE (%d, %d, %d, %d)", p.X, p.Y + 58, s.X, s.Y)