# Shop window size facts (lead, 2026-10-28)

## Owner report
"Doesn't the Shop UI feel VERY BIG and off-centred?" Then: "on the published game it is too big and large, here [Studio] it looks normal".

The owner's live screenshot is 1920x1080, Roblox Player, full screen, chat panel open top-left:
- The Shop window spans x 335..1580 (1245 px = 65 % of width), y 65..845 (780 px = 72 % of height).
- Its centre is y ≈ 455; the screen centre is 540, so it sits ~85 px HIGH.
- The big shop icon (top-left of the header) overlaps the open chat panel.
- The side tabs (Featured/Speed/Potions/Treadmill/Eggs) sit outside the right edge, x ≈ 1605..1715.
- The money/speed pills are bottom-left, x 15..372, y ≈ 860..1005; the left tile column (Shop/Claim/Rebirth/Index) is x 25..240, y 455..680.

The Studio capture `studio_1519x753_shop_now.jpg` is a Play test with a 1519x753 viewport (2.02:1, wider than 16:9):
- The window spans x 304..1216 (60 %), y 120..690.
- It is centred; it does not hit the pills.

## Code (StarterGui.MainMenu.MenuController)
- **The window** (`MainMenu.Window`):
  - AnchorPoint (0.5, 0.5) at Position (0.5, 0.5);
  - BaseSize = Size = {0.3229, 0}, {0.4074, 0};
  - UIAspectRatioConstraint DominantAxis = Height. So the HEIGHT is set from the screen height and the width = height x aspect.
  - MainMenu IgnoreGuiInset = false (topbar inset 58 px).
- **L293:** `LAYOUT = {Shop = {2.0, 1.6, 0.11}, Index = {2.0, 1.75}, Gift = {1.95, 1.2}, Rebirth = {1.95, 1.25}, Sell = {1.5, 1.05}, Settings = {1.55, 1.3}}` = {size x BaseSize, aspect, title box height}.
  - Shop height = 2.0 x 0.4074 = 81.5 % of the GUI height.
  - Shop width = height x 1.6.
- **L304-312:** `size = mul(winSize, lay[1])`, then `size = mul(size, fitScale(size))`, then a 0.32 s Back tween from 0.6x.
- **L160-201 `fitScale(size)`:**
  - `limitTop` = 6;
  - `limitBottom` = screen height - inset - 6;
  - if the window's LEFT edge is left of the pills' RIGHT edge and the pills are below the window top, then `limitBottom` = pills top - 6;
  - then it FIRST SLIDES THE WINDOW UP (`shift`) as far as the top allows, and only then shrinks it (`k`, minimum 0.5).
- **L140-147 `applySmall`:** viewport height < 520 (phones) → a UIScale 1.3 on the whole MainMenu (tiles, etc.). The window size itself still comes from LAYOUT + fitScale.

## Why the live game looks different from Studio
- On 16:9 (1920x1080, GUI height 1022) the Shop height = 0.815 x 1022 = 833 px and width = 1332 px.
- The left edge at 294 is left of the pills' right edge (~372), so `limitBottom` drops to the pills' top.
- The window slides UP to the top and shrinks to ~0.935, which gives the 1245x780 window at y 65..845: big AND high.
- On Studio's wider 2:1 viewport, the left edge (306) clears the pills (278), so there is no slide.

## Owner rules for this fix
- ONE layout for all devices: the phone = the PC layout scaled, never a separate phone arrangement.
- Phone size: "it must not be small on phone, but it shouldn't be very big on the phone".
- Check-UI is THE approved look. Do not restyle anything: size and position only.
- Any visible change is shown to the owner as a screenshot before it ships.
