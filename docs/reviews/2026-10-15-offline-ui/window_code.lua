-- OfflineClient (Roblox LocalScript) - the Welcome Back / Offline Earnings window, layout section only.
-- All positions are OFFSET pixels inside a 540x400 window (AnchorPoint 0.5,0.5 on most children unless noted).
-- The whole Holder is scaled by a UIScale (deviceScale: viewport / (1050x620), clamped 0.52..1.18).
-- Helper notes: text(parent, props) = TextLabel, GothamBlack, TextScaled, AnchorPoint (0.5,0.5), black UIStroke (props.Stroke px).
-- standardButton(parent, name, size, pos, label, gradient, textSize, rotation) = Check-UI canonical iconless button
-- (sharp, 3px #0C141A border, gradient, black damier, triple inner highlight, GothamBlack label, fixed TextSize).

local gui = new("ScreenGui", {Name = "OfflineUI", ResetOnSpawn = false, IgnoreGuiInset = true, DisplayOrder = 20, Enabled = false}, player.PlayerGui)
local holder = new("Frame", {Name = "Holder", Size = UDim2.fromOffset(540, 400), Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5), BackgroundTransparency = 1}, gui)
local win = new("Frame", {Name = "Window", Size = UDim2.fromScale(1, 1), Position = UDim2.fromScale(0.5, 0.5), AnchorPoint = Vector2.new(0.5, 0.5), BackgroundColor3 = CANVAS (59,88,102)}, holder)
-- UICorner 4, UIStroke 3.5 #181E22, body damier fade under the header

-- header (60 px): gold gradient (255,208,0)->(255,140,0), damier fade, top highlight, 2-tier divider
-- cash icon 44x44 at (40, 28) ; title "WELCOME BACK!" left-aligned, x from 70, height 36, width 66% ; 3D [X] 38x38 at (1,-34 , 0.5,-2)

-- body
Heading  "OFFLINE EARNINGS"   size 420x38  centre (270, 94)   stroke 3.5
Sunburst image 230x230         centre (270, 172) colour (255,220,120) transparency 0.3, rotates 20 deg/s
Cash     icon 132x132          centre (270, 172)
Amount   "$1.22M"  green gradient (180,255,25)->(60,205,0), size 380x62, centre (270, 256), stroke 4
Away     "You were away for 3h 12m - your pets kept earning!"  size 380x18, centre (270, 294), colour (205,232,245), stroke 1.8

-- buttons
ClaimX5  "CLAIM x5!"  236x58  centre (152, 356)  Day-7 rainbow gradient rotated 20 deg, TextSize 32
Price    frame 84x26, AnchorPoint (0,0.5) at (42, 316): "39" green-gradient text 46x26 right-aligned at x 0, + robux icon 24x24 tinted lime at x 50
Claim    "CLAIM!"     200x58  centre (398, 356)  lime gradient, TextSize 34
