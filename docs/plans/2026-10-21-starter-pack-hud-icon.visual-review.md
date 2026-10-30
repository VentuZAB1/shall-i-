# Visual review: Starter Pack HUD offer v2 (2026-10-21)

**Reviewed:**
- The live shots `starter_hud_v2_live_magma_1519.jpg` and `_live_magma_zoom.png`
- Every builder shot in `tests-2026-10-21/`: timer magma / void / tide and urgent, idle, pop, the motion sheet, column, compact, restricted, rebirth, hidden
- The popup shot `starter_popup_v2_timer_magma.jpg`
- v1 (`starter_hud_v1_*`, `starter_tile_zoom1.png`) and both owner references
- The plan, the plan review, and the Check-UI `SKILL.md` + `DESIGN_SYSTEM.md`
- The live script `StarterPlayer.StarterPlayerScripts.StarterPackHud` (640 lines), read only in the owner's Studio (Edit). Nothing was written.

## Verdict: FIX THEN SHIP

**What already works:**
- The placement, the frameless idea, the caption, the price style, the states and the motion system are all right.
- With the light, full-frame **Tide** egg (`_idle_zoom`, `_pop_zoom`) the art already reads like reference 1.

**What fails: the egg players will actually see, MAGMA or VOID.**
- Your concern is confirmed. In `_live_magma_zoom` the art reads as **"3 potions + cash + a clock"**. The Magma egg shows only as some flames poking out between them.
- The causes are measurable (section A). All of them are layout and contrast values; no redesign is needed.

---

## A. Why the egg disappears (measured)

1. **The Magma icon is not a full-frame egg.**
   - In the popup row icon and the hotbar icons, the egg is a round, dark lava ball. It sits in the **lower ~55%** of its frame and is only **~50% of the frame wide**.
   - Flames and red drips fill the top 45%.
   - So in the 80 px Egg layer at (0, -4), the shell is a ~40 px ball centred at about (0, +14) in Float px.
2. **The Float's lower half is exactly where the front layers were put** (review MUST 1). That only worked with the Tide egg in the mock.
   - PotionM (Hatch) 38 px at (-6, 34), ZIndex 7, covers x -25..13, y 15..53: the whole lower shell.
   - PotionL (Money) 36 px at (-32, 26), ZIndex 6, covers the shell's left flank.
   - The Robux icon of the Price (32, 38), ZIndex 9, covers the shell's lower right.
3. **The timer at egg centre + (3, -3)** runs straight across the flame/drip junction (ink about x -29..35, y -14..0). That band is the only part of the egg the potions left visible.
   - On the Void egg it covers the eyes (`_timer_void_urgent_zoom`).
4. **Contrast.**
   - Magma and Void are dark icons with no dark outline.
   - The glow behind them is too weak: SunA at ImageTransparency 0.34 and SunB at 0.50 are hardly visible on the live shot.
   - So on the blue wall the dark shell melts into the background.
5. **Green on green.** The lime "49" sits right against the green Hatch potion, so the price loses its edge (`_live_magma_zoom`).

**Result:** about 60-70% of the Magma shell is covered, and the rest is dark on dark. The hero is the weakest thing in the art.

---

## MUST fixes

All values are baseline px at the 1050x620 design size (WindowScale scales them). "Offset" means offset from the Float centre; in code, Position = 50 + offset. Line numbers refer to the live script.

### MUST 1: Hero on top. Every side item goes BEHIND the egg

This is what reference 1 does: the potion, the bolt and the rebirth icon peek out from behind the unicorn, and nothing sits in front of it. It fixes the egg being hidden under the potions.

New ZIndex order inside Float (lines 104-117, 121-122, 150-151):

| ZIndex | Layers |
|---|---|
| 1 | SunA |
| 2 | SunB |
| 3 | PotionBack (Speed), CashBack, **PotionL (Money), PotionM (Hatch)**. The last two were 6 and 7 |
| 4 | EggShadow |
| 5 | **EggOutline** (new, MUST 3) |
| 6 | **Egg** (was 5) |
| 7 | Star1, Star2 (was 8) |
| 8 | Timer (unchanged) |
| 9 | Price (unchanged; its children stay 9 and 10) |

Caption 20, Hit and CaptionHit 30: unchanged.

### MUST 2: Re-lay out the Float around a bigger hero

This fixes the shell being covered, the price beside the green potion, and the items reading as clutter on top of the egg. The potions fan out on the left, the cash peeks top right, and the price sits clear at the lower right.

| Layer | Size | Offset (was) | Rest rot (was) | Notes |
|---|---|---|---|---|
| SunA | **112** (108) | **(0, 4)** (0, 0) | spins +20°/s | Centred between the flames and the shell |
| SunB | **90** (86) | **(0, 4)** (0, 0) | spins -14°/s | |
| PotionBack (Speed) | **28** (32) | **(-30, -30)** (-27, -27) | -20 | Upper left, beside the flames |
| PotionL (Money) | **30** (36) | **(-37, 2)** (-32, 26) | -14 | Left flank, about 1/4 behind the shell |
| PotionM (Hatch) | **30** (38) | **(-32, 34)** (-6, 34) | **10** (6) | Lower left, peeking out under the shell |
| CashBack | **42** (44) | **(34, -26)** (28, -28) | 14 | Upper right, behind the flames |
| EggShadow | **96** (80) | Egg + (3, 6) | = Egg | Follows the bob, not the hop (as now) |
| EggOutline (new) | **104** | = Egg, including the hop | = Egg | See MUST 3 |
| **Egg** | **96** (80) | **(0, -6)** (0, -4) | -6 | Shell becomes about 48 px, centred at about (0, +16) |
| Star1 | 14 | **(46, 14)** (44, 4) | spins | Right-middle gap |
| Star2 | 11 | **(-44, -42)** (-46, -8) | spins | Above the Speed potion (it sat on the Money potion) |
| Price | **52x24** (64x25) | **(34, 44)** (32, 38) | -8 | Inside: see MUST 5 |

**Restricted (cash hero), in refreshHero, line 168:**
- The cash goes from 74 to **86**; EggOutline = 86 + 8.
- CashBack stays hidden.

**Keep these in sync:**
- `ITEMS` (lines 469-474): `off` and `rot` from the table above.
- `EGG_OFF = V(0, -6)`, `SHADOW_OFF = V(3, 6)` (line 108).
- `PRICE_OFF = V(34, 44)` (line 120).

**Root, caption and hit areas** (lines 45-47, 84-87). The Root grows only in height, for the bigger egg's flames.

| Constant | New value |
|---|---|
| FULL | `V(150, 170)` (was 162) |
| COMPACT | `V(150, 156)` (was 146) |
| REST | `V(72, 82)` (was (72, 73)) |
| CAPTION_Y | `156` (was 138) |
| Hit | Size 124x128 at (72, 80) (was 120x112 at (73, 73)) |
| CaptionHit | Position (75, 156) |

At rest the gap from the art (price bottom, Root y 138) to the caption glyphs (about y 150) is about 12 px, close to the current tight look.

**Slot check with `solve()`:**
- 1519x753: slot 218, so s = 1.18, full. Root 177x201, screen y 84..285. It still fits.
- 1050x620: slot 176, so s = 1.00, full.
- Phones: 844x390 has s = 87/156 = **0.56** compact (was 0.60); 667x375 has **0.53** (was 0.57). Both are still well above the 0.45 floor.
- Net effect on phones: the hero egg is about **12% bigger on screen** than now (96 x 0.56 = 54 px, against 80 x 0.60 = 48 px).

### MUST 3: Make a dark egg pop on any background (outline twin + a real halo)

This fixes the dark Magma and Void shells melting into the wall or sky, and the weak glow.

**1. EggOutline (new ImageLabel in Float):**
- The same image as Egg, **ImageColor3 (0, 0, 0)**, ImageTransparency 0, ScaleType Fit, AnchorPoint (0.5, 0.5), Size egg + 8 (104, or 94 for the restricted cash), **ZIndex 5**.
- Set its Image and Size in `refreshHero()` next to `egg` and `shadow`.
- In the loop (after line 518) give it **exactly the Egg's Position (bob + hop) and Rotation**.
- This makes the review's SHOULD 10 a MUST: the black sticker edge the potions and the cash already have.
- (ImageColor3 only multiplies, so a white rim is not possible this way. A black twin is.)

**2. Halo:**

| Layer | Setting | Value |
|---|---|---|
| SunA | ImageColor3 | **(255, 226, 120)** (was (255, 214, 90)) |
| SunA | Base transparency (loop line 530) | `sunA.ImageTransparency = 0.14 + wave(0.04, 2.0, 0, t)` (was 0.34) |
| SunB | ImageTransparency | **0.30** (was 0.50) |
| SunB | ImageColor3 | Per egg, set in `refreshHero()`; see below |

SunB colour per egg:

| StarterEgg | ImageColor3 | Why |
|---|---|---|
| MagmaEgg | **(255, 120, 40)** | Hot orange; echoes the flames |
| VoidEgg | **(180, 100, 255)** | Violet; with SunA's gold this gives a complementary rim behind the dark purple |
| Anything else, and the restricted cash | (255, 110, 200) | As now |

Both suns sit behind the egg, so their bright cores are hidden and only the rays frame the silhouette. That is what makes a dark shell read.

### MUST 4: Timer ON the egg, at the shell's lower band (not across the middle)

The owner asked for the timer on the egg and easy to see, with no background. This keeps that, and frees the flames, the drips and the Void egg's eyes.

| Setting | New value (was) |
|---|---|
| `TIMER_OFF` (line 146) | `V(0, 33)` from the egg centre, so Float (0, 27) (was (3, -3)) |
| `TIMER_OFF_COMPACT` | `V(0, 33)` too (was (3, -6)) |
| `TIMER_COMPACT` (line 145) | **1.25** (was 1.2) |
| Timer label Size | **76x22** (was 84x22) |
| TextSize | 16 (unchanged) |
| UIStroke | 3, black (unchanged) |
| Gold gradient | Unchanged |
| ZIndex | 8 (unchanged) |

- The text reads as a label on the egg's base, and the shell's upper half plus all the flames stay clear.
- The ends of the text overhang the shell by about 6 px on each side. That's fine: the stroke carries it.
- It no longer touches the gold Money potion, which is now higher up.
- Compact text height is 16 x 1.25 x 0.56 = **11.2 px** on an 844x390 phone. Its bottom (y 36) clears the price icon (y 35..53) by about 1 px.
- Keep it riding the egg's bob and hop (line 522) as now.

### MUST 5: Price frame tight to its content

This fixes the conservative envelope test (the old 64 px box needed scaling down) and keeps the lime price off the egg.

Inside Price (lines 121-132):
- **Price:** Size **52x24**, AnchorPoint (0.5, 0.5), rest rotation -8.
- **RobuxOutline:** 22x22 at **(10, 12)**. **Robux:** 18x18 at **(10, 12)**.
- **Amount:** AnchorPoint (0, 0.5), Position **(20, 12)**, Size **32x24**, TextSize by length: **2 characters = 22, 3 = 16, 4 or more = 13**. This replaces line 178.
- Gradient and stroke 3 unchanged.

### MUST 6: An urgent state that reads as "urgent", not pink

At < 1 h, `49:54` in (255, 255, 255) → (255, 125, 125) reads salmon/pink (`_timer_magma_urgent_zoom`).

| Setting | New value |
|---|---|
| `TIMER_RED` (line 149) | `ColorSequence.new(C(255, 235, 225), C(255, 60, 50))` |
| Pulse (line 537) | Amplitude 0.05 → **0.10**: `1 + 0.10 * (0.5 - 0.5 * math.cos(TAU * t))` |

Still once a second, and still off with Reduced Motion.

### MUST 7: Update the envelope test so it judges the real pixels

The big egg's frame is mostly transparent (flame tip at about 8% from the top, shell 50% wide). The half-diagonal test from plan section 10.3 would fail it for nothing.

**In `artBox()`:**
- **Egg, EggOutline, EggShadow:** use the rotated rectangle of **0.86 × the layer's AbsoluteSize**: half-extent = 0.43·size·(|cos θ| + |sin θ|), with θ = the layer's Rotation + Float.Rotation.
- **Timer:** use its `TextBounds` rect plus 3 px of stroke, scaled by `TimerScale`.
- **Everything else:** as before.

**Pass:**
- On screen.
- Above the column.
- Every Float descendant has a ZIndex below the Caption's.
- Inside the Root ±1 px.
- 13 s of samples, in both full and compact (`TestScale` 0.56 + `TestCompact`).

**If it fails by more than 1 px:**
- First apply the existing rule: scale all Float **offsets** by 0.96.
- If the egg group alone still fails: Egg/Shadow **92**, Outline **100**, EGG_OFF **(0, -5)**.

### MUST 8: Re-shoot the evidence with the eggs players will see

None of the current shots show the final look on Magma or Void at phone scale, and the motion sheet uses Tide. Save them in `tests-2026-10-21/`:

| File | Content |
|---|---|
| `starter_hud_v3_magma.jpg` + `_zoom.png` | Normal timer |
| `starter_hud_v3_magma_urgent_zoom.png` | Urgent timer |
| `starter_hud_v3_void_zoom.png` | Normal timer |
| `starter_hud_v3_void_urgent_zoom.png` | Urgent timer |
| `starter_hud_v3_compact_magma.jpg` + `_zoom.png` | TestScale 0.56, TestCompact, **with the timer running** |
| `starter_hud_v3_restricted_zoom.png` | Restricted (cash hero) |
| `starter_hud_v3_motion_sheet.png` | On **Magma**: idle, drift extreme, pop p = 0.1 |
| `starter_hud_v3_magma_bright.jpg` | One shot against **bright sky**, as well as the usual dark blue wall |

**Acceptance (judge it from the zoom shots):**
- The Magma shell is ≥ 85% visible: only the timer's band crosses it.
- The Void face (eyes and grin) is visible.
- The timer is readable at the full-screen size.

---

## SHOULD fixes

1. **The popup hero has the same problem** (`starter_popup_v2_timer_magma.jpg`).
   - The three potions in a row cover the fire egg's lower half, and the "ENDS IN 23:59:48" tag covers its upper left.
   - The "BIG FIRE EGG" row is fine. The hero is not.
   - Apply the same pattern there: potions BEHIND the egg (lower ZIndex), fanned left and right, the egg about 15% bigger, plus a black outline twin (+8 px).
   - **Owner question:** does "remove the background on the timer" also apply to the popup's yellow "ENDS IN" tag? Today the HUD and the popup timers look different.
2. **Digit jitter.** GothamBlack digits aren't fixed-width. While the timer is centred, look in the motion capture for the text shifting by 1-2 px when a "1" appears. If it's visible, set `TextXAlignment Left` and offset the label so that "00:00:00" is centred.
3. **Compact noise.** At s ≈ 0.53-0.56, hide Star1 and Star2 (`Visible = not compact`): at about 6-8 px they read as specks.
4. **Left-right drift.** The owner said "left n right up n down". If he still calls it stiff after v3, raise only Float X to `wave(5, 4.0, 0, t)` (±5.9 px at 1080p) and re-run the envelope test. The left side has about 0.8 px of slack, so apply the 0.96 rule if needed.
5. **R9, if it still reads "basic".** The stock egg icons are dark and only half-frame. A dedicated bright "big egg" render per area (Blender, full-frame, a lit rim), uploaded through the group FBX carrier, would make the hero pop without tricks. It needs the owner's go-ahead for the upload.
6. **The player-list screenshot** (plan review section 0, `starter_hud_v2_playerlist.jpg`) is still missing.

---

## What's good (keep it)

- **Placement.** It is right-aligned to the Eggs / Pets / Potions column, about 7 px above it, with nothing else in that zone.
  - It is clear of the top bar, the $/Day line, REBIRTH READY (`_rebirth.jpg`) and the left menu in every shot. v1's "hovers over text" problem is gone.
  - Hidden states work: the window shot (`_hidden_window.jpg`) and the panel shot (`_hidden_panel.jpg`).
- **Scale.** At 1519x753 (s = 1.18) the art is about 120 px of ink, the same size as reference 1's 110-130 px at 1080p. It is proportionally larger on phones. The size is right. Coverage and contrast were the problem.
- **Frameless.** No tile, ribbon or card. It reads like both references.
- **Caption.** "STARTER PACK" in GothamBlack 16, white, 2.2 black stroke: crisp and readable at 19 px. That is the right Check-UI pairing.
- **Price style.** A lime gradient "49" with a 3 px black stroke and a black-twin Robux icon. It is the loudest text, which is the right hierarchy. Only its position was wrong.
- **Timer style.** No background, cream gradient, 3 px stroke, 19 px on screen: readable at a glance. The "59:12" format under an hour is good.
- **Motion system.**
  - One loop, idle while hidden.
  - Positions are set in Scale, so it never stair-steps.
  - A 1:2 figure-8 with ±3° sway, per-item bob and tilt, and a pop every 6 s that doesn't overshoot.
  - Reduced Motion is respected, and the touch-hover bug is fixed.
  - It is lively without being nauseating (`_motion_sheet.png`). It is what the owner described.
- **States.** One tween, a 0.3 s debounce, the scripted-camera / slingshot / modal / column-away / overlap rules, and the countdown hide at 0. All solid.
- **Tide / fallback composition.** It already reads like reference 1, which shows the frameless approach is right. The fixes above make Magma and Void reach the same read.
