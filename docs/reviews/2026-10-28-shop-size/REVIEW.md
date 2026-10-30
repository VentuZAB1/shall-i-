# Shop window size and centring: UI review (2026-10-28)

Read-only review. Inputs: `FACTS.md`, `studio_1519x753_shop_now.jpg`, the vault notes (Check-UI Rules, Check-UI Skill section 4 responsive engine, Screen Layout and Windows, Phone UI, UI Library Menus / Mobile / Anti-patterns), and the 10-22 payload drafts in `docs/plans/ui-polish-2026-10-22/payloads/`. Studio was not touched and no code was edited. The MenuController source is not in the repo (only the payload edits), so every code claim below comes from FACTS.md and must be re-read live (M0) before editing.

## 1. Verdict

**Today's Shop: 4/10** against the 8.5 ship bar.

- Off-centre: window centre at y 455 (live 1080p). The centre of the GUI area is y 569 (topbar inset 58), so the window sits 114 px high; against the full screen centre (540) it is 85 px high.
- Jammed to the top: top edge at y 65, under the topbar and beside the open chat.
- Dominant: 1245 x 780 = 65 % of the width and 72 % of the height.
- Cause (FACTS code, reproduced in outline): the pills test compares the pills' TOP with the window's TOP, which is nearly always true, so any window whose left edge is left of the pills' right edge gets its bottom limit moved to the pills' top. The fit then slides the window UP to the top edge and only then shrinks it.
- What is fine: side tabs stay on screen, tiles are clear, the 2-card rows read, and the aspect is 1.6 (1245 / 780 = 1.596).

**Proposed (sections 3-4): 8/10 on paper.** It fixes the verified faults but is not ship-ready: the card-row sizing, the phone UIScale and the 4:3 tablet are unresolved (M0, M2b, N2). Owner rule: 8 = another round. Target 8.5+ after the M0 checks and the owner's screenshot.

## 2. Facts I checked

- **Live aspect is 1.6.** 1245 / 780 = 1.596. The 10-22 drafts with Shop aspect 1.82 (`apply_1`) and 1.55 (`round2`) are not live. Round 2's Shop 2.28 would be about 14 % taller nominally. Do not apply any of these drafts.
- **The FACTS LAYOUT line does not match any payload.** Rebirth is 1.95 in FACTS and 1.55 / 2.0 / 2.15 across the drafts. Read the live line before editing.
- **Side-tab formula confirmed on the Studio capture.** Tab x = window left + 1.022 w (measured 1236, image about 1230); tab width 0.09 w (82 px); tab top = window top + 0.2 h (234 px, matches the image).
- **The approved Studio window is centred on the GUI area.** 912 x 570, not slid (k = 1). Its centre is y 405, the GUI-area centre is 405.5, and the viewport centre is 376.5. The owner called this "normal", so a centre 29 px low on the viewport is accepted.
- **The left tile column is centred on the GUI area too.** Live tiles span y 455-680 (centre 567, GUI centre 569). The GUI-area centre is the design's centre.
- **Pills model.** Right edge about 15 + 0.33 Vy; top about 0.80 Vy. It fits both measured points (1080p: right 372 / top 860; Studio: right 257 / top 604). Used for the 1366, tablet and phone estimates. The code reads real positions at runtime, so only the judgement numbers depend on this model.
- **Live Shop rect vs model.** The FACTS code gives 1208 x 755 at 1080p; the measured rect is 1245 x 780 (3 % off). The shape of the failure matches.

Conventions below: pixels on the viewport, y from the top of the screen. GUI-area centre = inset + (Vy - inset) / 2. "GUI" offset = window centre minus GUI-area centre; "vp" offset = minus viewport centre. Test (a) is read against the GUI-area centre (see M3).

## 3. Geometry

### 3.1 Shop (LAYOUT {2.0, 1.6, 0.11}, BaseSize height 0.4074)

| Screen (GUI height) | Today | Proposed | Centre offset | (b) pills / tiles | (c) side tabs right edge | (d) 2-card rows read |
|---|---|---|---|---|---|---|
| PC 1920x1080 (1022) | measured 1245x780, x 335-1580, y 65-845 | **1114x696**, x 403-1517, y 221-917 | today GUI -114 / vp -85; new **0 / +29** (2.7 %) | clear by 31 px sideways (pills 372) | 1642 of 1920 | PASS: Studio image x1.22 |
| PC 1366x768 (710) | model 816x510, x 275-1091, pinned at y 64-574 | **792x495**, x 287-1079, y 166-661 | today GUI -94 / vp -65; new **0 / +29** (3.8 %) | clear by 13 px sideways (pills model 268) | 1168 of 1366 | PASS if the card row is Scale-sized (text ~13 % smaller); RISK if Offset (M0-3) |
| Studio 1519x753 (695) | measured 912x570, x 304-1216, y 120-690 | **881x551**, x 319-1200, y 130-681 | today GUI -0.5 / vp +28.5; new **0 / +29** | clear by 56 px | 1299 of 1519 | PASS: x0.97 (-3 % size change, needs owner look) |
| Phone 844x390 (354, inset 36) | model 462x288, x 191-653, y 69-357 (no slide) | unchanged 462x288 before M2b; **487x304 rendered** after M2b | today GUI 0 / vp +18 (4.6 %) | clear by 47 px | 704 of 844 | UNVERIFIED: at S 0.63 the body text is about 0.53x Studio, below the 16 px floor (M2b) |
| Tablet 1024x768 (710) | model 816x510 pinned at top, x 104-920, y 64-574 | **594x371**, x 215-809, y 227-599 | today GUI -58 (pinned); new **0 / +29** | x overlaps pills (268), but the window bottom (599) is 15 px ABOVE the pills top (614): clear | 875 of 1024 | FAIL-ish: at Studio card size the 2-card row is about 911 px, so at 594 px the cards and text must shrink to about 0.65x (N2) |

### 3.2 Other big windows

| Window | 1920x1080 today | 1920x1080 proposed | Tablet 1024x768 today -> proposed | Studio 1519x753 today -> proposed | Same off-centre bug? |
|---|---|---|---|---|---|
| Index {2.0, 1.75} | model 1322x755, x 299-1621, pinned top (centre 441, GUI -128) | **1114x636**, x 403-1517, y 251-887 | 893x510 pinned -> 594x339 centred | 991x566 (264 px from pills vs 263 threshold) -> 881x503 | **YES on 16:9 and Studio** (cap + fitScale fix) |
| Gift {1.95, 1.2} | 974x812, x 473-1447, centred, no slide | unchanged | 630x525 pinned at top (GUI -87) -> 475x396 centred | 663x552 unchanged | Tablet only (fitScale fix; no LAYOUT change). Cap does not bind. |
| Rebirth {1.95, 1.25} | 1015x812, x 453-1467, centred, no slide | unchanged | 656x525 pinned -> 489x391 centred | 690x552 unchanged | Tablet only; same as Gift |

Gift and Rebirth at 1366x768 are also unchanged (677x564 and 705x564, centred). Sell and Settings are far under the 58 % cap; they change only when the pills rule binds (4:3).

## 4. Proposal

### M0. Read-only checks before any edit (blocking)
1. Read the live LAYOUT line, `applySmall` (L140-147), the fitScale body (L160-201) and the size / tween block (L304-312). Confirm whether the window's top edge is pinned or its centre shifted. The FACTS model (centre-anchored shift) would put the live top near y 91, but the measured top is y 65 (GUI 7). Either the code pins the top or the FACTS are off. The fix removes the shift, so the result does not depend on this, but the builder must read the code first.
2. Phone: does `MainMenu` (FACTS: "the whole MainMenu") or only the tiles (brief: "the menu tiles") carry a UIScale 1.3? If the whole menu does, the Shop already renders about 1.3x its fitted size on phones (about 600x374, taller than the 354 px GUI), and fitScale's AbsoluteSize reads are off by that factor. Check in the phone emulator (733x392).
3. Shop card row: are the card widths Scale or Offset? In the Studio capture, two cards (380 px each) + a 19 px gap + 66 px margins each side = 911 px, i.e. the full 912 px window. If the widths are Offset, any window narrower than about 910 px clips the second column; if Scale, the cards shrink with the window. This decides whether the 792 px and 881 px sizes are acceptable.
4. Coordinate convention: print `win.AbsolutePosition.Y` and `pills.AbsolutePosition.Y` once, and make sure the new pills test uses the same space as the window.

### M1. LAYOUT: no change
- Shop stays `{2.0, 1.6, 0.11}`; Index stays `{2.0, 1.75}`; Gift and Rebirth unchanged.
- The size comes from the new width cap, not the multiplier. The nominal size only binds on phones, where it is the approved size.
- Do not apply the 10-22 drafts (aspect 1.82 or 1.55 would change the look).

### M2. fitScale: centred, shrink-only, width cap (L160-201)
Replace the slide logic with this shape (placeholder names; adapt to the live code):

```lua
-- fitScale: centred, shrink-only, width cap (proposal 2026-10-28)
local WIDTH_CAP = 0.58   -- next to LAYOUT (L293): window never wider than 58 % of the screen
local PILL_GAP = 6
local function fitScale(size)
	local vp = workspace.CurrentCamera.ViewportSize
	local inset = GuiService:GetGuiInset().Y
	local guiH = vp.Y - inset
	local h0 = size.Y.Scale * guiH              -- nominal height, no shift
	local w0 = h0 * aspect.AspectRatio          -- aspect = the window's UIAspectRatioConstraint (1.6 for Shop)
	local k = math.min(1, WIDTH_CAP * vp.X / w0)
	local hud = player.PlayerGui:FindFirstChild("SpeedUI")
	local pills = hud and hud:FindFirstChild("Holder")
	if pills then
		local pRight = pills.AbsolutePosition.X + pills.AbsoluteSize.X + PILL_GAP
		local pTop = pills.AbsolutePosition.Y - inset - PILL_GAP
		local bottom = guiH / 2 + k * h0 / 2     -- window is centred
		if vp.X / 2 - k * w0 / 2 < pRight and bottom > pTop then   -- overlaps in BOTH axes
			local kSide = 2 * (vp.X / 2 - pRight) / w0      -- narrow until clear sideways
			local kAbove = 2 * (pTop - guiH / 2) / h0       -- or shorten until clear above
			k = math.min(k, math.max(kSide, kAbove))
		end
	end
	win.Position = basePos                      -- never slide off-centre
	return math.max(k, 0.5)
end
```

Rules:
- **No `shift`, no slide.** The window stays at Position (0.5, 0.5). Remove the top / bottom limit values; a centred window with k <= 1 cannot exceed the GUI.
- **Width cap** `WIDTH_CAP = 0.58` on every MenuController window. It binds on Shop and Index at 16:9 and only shrinks Studio's Shop by 3 %.
- **Pills test is a rect overlap in both axes** with a 6 px gap. Only then act: take the larger of "narrow until clear sideways" and "shorten until clear above".
- Keep the floor at 0.5.
- **Keep the tutorial-guide lines L166-184 intact.** They sit inside this function. Delete only the slide / shift lines and the old pills block.

Result (model): 1080p Shop 1114x696; Studio 881x551; 1366 792x495; tablet 594x371 (clear of pills); phone unchanged 462x288.

### M2b. Phone (conditional on M0-2)
- If the window has no UIScale: add a UIScale 1.3 on the Shop window when the viewport height is below 520 (same threshold as `applySmall`). Limit the pre-scale height to 0.66 x GUI so the rendered height stays under 0.86 x GUI. Rendered result about 487x304 (the same as the Check-UI-scaled value in N1). This follows the vault rule "big windows look small on phones: bump their scale on short viewports".
- If the whole MainMenu already has the 1.3: check that the rendered rect is inside the GUI and fix the fit to divide by that scale.
- Either way, the phone is the PC layout scaled (owner rule), not a separate arrangement.

### M3. Centring
- Centre on the GUI area (Position unchanged). This is the design's centre, matches the approved Studio capture, and matches the tile column.
- Test (a): at 1080p the window is 0 px off the GUI-area centre and 29 px (2.7 %) low against the full screen centre (540). It fails the strict 2 % test against 540 by 8 px. Owner's call (N4).

### M4. Verify and show the owner before shipping (owner rule: visible change = screenshot first)
- Studio Play 1519x753: expect 881x551 at y 130-681, a 3 % shrink.
- Roblox Player 1920x1080: expect 1114x696 at x 403-1517, y 221-917. Check the header icon (about x 439, y 189) against the open chat panel; the chat's width is not in the folder.
- Phone emulator 733x392 and 844x390: check the Shop and Index rects are inside the GUI and the text is readable.
- Test the tutorial guide end to end (TestTutorial) and open / close Index, Gift and Rebirth.

## 5. NICE

- **N1. Structural fix (next round, after the owner has seen M2).** Size windows as design pixels x the Check-UI responsive scale, clamp(min(Vx / 1050, Vy / 620), 0.52, 1.18), not as GUI fractions. The approved Studio window is 912x570 at scale 1.18 (base 773x483 px). At 1080p and 1366x768 this gives the same 912x570 before the cap (the cap then gives 792 at 1366). The phone gives about 487x304. This makes "phone = PC scaled" literal and makes 1080p look like the approved Studio capture. Needs M0-3 first.
- **N2. Tablet 4:3 (1024x768) decision.** The pills (right edge about 268) and a centred 1.6-aspect window cannot both have two-card width. Options: (a) accept 594x371 (the current proposal); (b) on screens with Vx / Vy below 1.5, use aspect about 1.8 sitting above the pills (about 700x390); (c) move the pills on 4:3. Recommendation: (a) for now; owner chooses (b) or (c).
- **N3. Phone bump** is in M2b; this entry is only the owner's preference between a 1.3 bump and the N1 structural value.
- **N4. True viewport centring (owner option).** Position Y = 0.5 with offset -inset / 2 (-29 px on PC, -18 px on phone). This moves the Studio capture up 29 px too, so it is a visible change.
- **N5. Debug attribute.** Write the final k, width and height to a test attribute so the emulator tests can read the result without a screenshot.

## 6. Risks

- **R1. Slide model ambiguity** (M0-1). FACTS says the window's centre shifts; the measured live top is at the GUI top edge. Irrelevant once the shift is removed, but read the code first.
- **R2. Tutorial guide fit (L166-184)** sits inside fitScale. If the guide reads the window's top or the fit result, removing the slide can move the arrow. Test the tutorial end to end.
- **R3. Hatch skin path (L267-289)** is not used now. If re-enabled it has its own sizing and would double the cap. Leave it parked; do not reuse fitScale there without a check.
- **R4. Card-row sizing** (M0-3). A fixed-width row clips at 792 px and 881 px. A Scale row shrinks the text (about 0.87x at 1366). The Studio capture's row fills the window exactly, so this is the single biggest unknown.
- **R5. Tablet readability.** 594x371 gives body text about 0.65x Studio, below the 16 px floor. Owner decision N2. Gift and Rebirth on the tablet shrink to about 0.7x (475x396, 489x391).
- **R6. Pills model** is fitted to two screens. The 1366 Shop clears the pills by only 13 px in the model; a 10 px error would move it into the pills. Check on the 1366 screen.
- **R7. Phone UIScale ambiguity** (M0-2). A 1.3 applied to a window that is already 1.3x would overflow the 354 px GUI.
- **R8. Index at 1080p** becomes 636 px tall (62 % of the GUI height). Check that the portrait grid still shows its rows; if not, give Index its own cap of 0.60 (no LAYOUT change).
- **R9. Chat panel.** The Shop header icon would sit at about x 439, y 189 at 1080p. An open chat wider than about 400 px would touch it. Check on the owner's live screenshot.
- **R10. Toasts** sit below the window. At 1080p the bottom moves from 845 to 917 (163 px left below); re-check toast placement.
- **R11. Studio change** (912 to 881, -3 %). Small, but it is a visible change to the approved look; the owner sees it in the M4 screenshot.

## 7. Next step

Run M0 (read-only), then M1-M3 (and M2b if M0-2 says so), then the M4 screenshots. Send the screenshots to the owner. Re-rate after N2 is decided; ship at 8.5+ only.
