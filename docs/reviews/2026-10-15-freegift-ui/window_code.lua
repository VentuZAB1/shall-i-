-- FreeGiftClient (Roblox LocalScript) - the FREE GIFT window, layout section only.
-- All positions are OFFSET pixels inside a 560x420 window; AnchorPoint (0.5,0.5) unless noted.
-- The Holder is scaled by a UIScale (viewport / (1050x620), clamped 0.52..1.18); the screenshots are at ~1.18x.
-- text(parent, props) = TextLabel, GothamBlack, TextScaled, AnchorPoint (0.5,0.5), black UIStroke (props.Stroke px).
-- standardButton(...) = Check-UI canonical iconless button (sharp, 3px #0C141A border, gradient, black damier,
-- triple inner highlight, GothamBlack label with a fixed TextSize).

Window   560x420, canvas (59,88,102), UICorner 4, UIStroke 3.5 #181E22; body damier (tile 22, colour (30,50,60), transp 0.55, fades down)
Header   560x60: Codes cyan gradient (0,205,255)->(0,130,245), damier fade, 2 px top highlight (180,240,255),
         2-tier divider (3 px (0,50,110) + 3 px black); title "FREE GIFT!" left-aligned at x 22, h 38, stroke 3.5; 3D [X] 38x38 at (1,-34, 0.5,-2)

Art      frame 180x150 centred (115, 140): sunburst 210x210 (tint (150,235,255), transp 0.25, rotates) + 3 potion icons:
         Money 80x80 at (-48,+6) rot -14 ; Speed 80x80 at (+48,+6) rot 14 ; Hatch 100x100 at (0,-6)
Tag      "~ ONE-TIME GIFT! ~" 320x34 centred (385, 100), red gradient (255,110,110)->(230,25,45), stroke 3
Headline "3 POTIONS!" 330x60 centred (385, 145), cyan->green gradient, stroke 3.5
What     "x2 MONEY • x2 HATCH • x2 SPEED" 330x22 centred (385, 185), stroke 2
Each     "30 minutes each - use them whenever you want!" 320x17 centred (385, 207), colour (200,235,255), stroke 1.6

Cards    255x112, bg (26,44,52), UICorner 4, 2 px black border + inner 1.2 px (75,125,145) highlight at 0.4 transp
  Like   centred (147, 295): title "1. Like the game!" (1,-20)x24 at y 20, stroke 2.4 ; 👍 emoji 54x54 at (42,66) ;
         "Click the 👍 on the game page" 160x44 at (160,68), stroke 1.8
  Group  centred (413, 295): title "2. Join the group!" ; group icon 58x58 at (46,68) ; JOIN cyan button 128x44 at (170,70) TS 26 ;
         "JOINED!" lime 130x34 at (170,70) (replaces JOIN when in the group) ; check mark 28x28 at (1,-20, 0,20) when joined

Hint     red text 420x20 centred (280, 360) (only after a failed claim)
Claim    CLAIM! lime canonical button 236x56 centred (280, 390), TS 34 -> becomes silver "CLAIMED!" after claiming
