# SLINGSHOT signature UI style (2026-10-21)

Art-direction spec. Nothing in the game was changed. The Studio scripts were only read.

The owner's ask, word for word:
- "it looks so ugly overlooping and corners aren't even in the box."
- "Why don't we come up with our style? To look unique and cool?"

**Mockups:** `docs/plans/style-2026-10-21/`

| File | What |
|---|---|
| `compare_now_A_B.png` | the current window next to both directions |
| `A_studbox_pc.png` / `A_studbox_phone.png` / `A_studbox_sheet.png` | Direction A: window on PC 1920x1080, phone 844x390, component sheet |
| `B_hatchnight_pc.png` / `B_hatchnight_phone.png` / `B_hatchnight_sheet.png` | Direction B: same three |
| `dirA_studbox.html`, `dirB_hatchnight.html`, `common.js`, `render.sh` | sources. `bash render.sh all qa` re-renders and prints the containment report |

**States shown:**
- The PC renders show mid-week: Days 1-2 CLAIMED, Day 3 CLAIM, Days 4-7 LOCKED.
- The phone renders show the day after: Days 1-3 CLAIMED, Day 4 TOMORROW with its timer.
- Each sheet shows all four card states side by side.

**QA:** every render passes the automated check in `common.js`:
- Every element, outline included, sits inside its parent.
- Cards, tabs and chips never overlap.
- No text overflows its box.
- Measured minimum text: 18.9 px on PC, 11.4 pt on the phone.
- Every text line fills at most 83% of its box.

**Recommendation: Direction B, HATCH NIGHT** (reasons in section 5).

---

## 1. Why the current window looks broken (root causes in StreakClient)

| Symptom | Cause in `StarterPlayerScripts.StreakClient` / MenuController |
|---|---|
| Cards poke out of the panel | `DailyView` is the full page width and the cards sit at `COL_X = 0 ... 0.765 + 0.235 = 1.0`, flush with both edges. UIStroke in Border mode draws outside the frame, so every card's 2.6 px outline (times device scale) and its bottom bevel hang past the Body box. |
| Cards overlap each other | The CLAIM card pulses its whole holder (`pulse.Scale 1 -> 1.04`) and pops to 1.15 on claim. The gap between cards is about 2% of the width, so a pulsing card covers its neighbours' outlines. |
| Ribbon outside the box | The "SECRET!" brick is rotated 10° at x 0.9 of the Day 7 face, so its rotated corners leave the card. |
| Header too tall | The Gift header is `title bottom + 0.02` of a 1.2-aspect window, about 21% of the window height. |
| Cramped, tiny text | The copy is long ("+1 Hatch & Speed Potion" is 23 characters) in fixed boxes, so TextScaled shrinks it to about 9 px. |
| Two nested boxes | The window canvas holds the recessed Body card, which holds the cards. Three borders compete. |

Both directions below fix all six problems with the same layout rules (section 2). They differ only in the look.

---

## 2. Shared foundations (both directions)

### 2.1 Containment rules (the answer to "corners aren't even in the box")

1. **One container.** On the Gift page the window canvas is the only box. Body becomes transparent with no stroke, so there is no box inside a box.
2. **Gutters hold the outlines.** Every brick, card or button sits at least 8 logical px inside its parent and at least 8 px from its siblings.
   - UIStroke draws outside the frame, so a 2.5 px outline needs at least 3 px of that gap.
   - If the Studio build has `UIStroke.BorderStrokePosition = Inner`, use it on cards. Keep the 8 px gap anyway.
3. **Depth lives inside the box.** Every 3D element is a holder of a fixed size containing a Side (the depth) and a Face.
   - The Face is the holder height minus the depth.
   - The Side is the full holder.
   - Nothing hangs below the holder.
   - This is BrickUI's existing `holder{Depth, Face}`; keep using it.
4. **Pulse the button, never the card.** A button may scale to at most 1.06.
   - Its side margin inside the card must be at least (scale - 1) / 2 x its width + its outline. With an 8 px margin and a 142 px button this holds.
   - The claim pop scales the ICON inside the clipped face, not the card.
5. **Badges are not rotated past their box.**
   - Ribbons and tags sit inside the card's top band, not rotated.
   - A sticker rotated for fun, like the check stamp at -8°, must keep its rotated bounding box inside the card.
6. **Highlights go inward.**
   - The "today" ring is an inner stroke or an inset frame, never an outer glow.
   - Glows are radial images sized inside the face.
7. **Rotating art keeps its visible pixels inside.**
   - Sunbursts and rays use radially faded art no wider than the face.
   - Don't rely on ClipsDescendants for rotated children.

### 2.2 Grid (logical units, window 740 x 470, depth 7 included)

| Part | Rect (x, y, w, h), logical | Notes |
|---|---|---|
| Window | 0, 0, 740, 470 | Face 740 x 463 plus a 7 px depth slab |
| Header | A: brick 10, 10, 720, 44. B: full-bleed band 0, 0, 740, 46 plus crack teeth down to y of about 60 | Half the current height |
| Row 2 | tabs 10, 62 (A) / 10, 66 (B), 308 x 38; streak bar 330, 62 / 330, 66, 400 x 38 | Replaces the old status line |
| Small cards | columns x 10 / 176 / 342; rows y 108 / 284 (A) or 112 / 286 (B); 158 x 168 (A) or 158 x 166 (B) | 3 x 2 grid of Days 1-6 |
| Day 7 hero | 508, 108 (A) / 112 (B); 222 x 344 / 340 | Tall card on the right |
| Margins | 10 window edge, 8 between cards, 11 at the bottom | |

- **Aspect:** 740 / 470 = 1.574. MenuController's `LAYOUT.Gift` aspect goes from 1.2 to 1.574.
- **The PLAYTIME tab** reuses the same window and grid area (a 6 x 2 grid of 12 slots, 113 x 165 each).

**Inside a small card** (A uses face height 163; B is 2 px shorter):

| Item | Rows (logical) |
|---|---|
| Day label | 5-23 |
| Icon box | 140 x 68 at y 21 |
| Value line (20-22 px) | 89-111 |
| Sub line (16 px) | 111-129 |
| Button | 142 x 28 at y 131 |

**Inside the hero card:**

| Item | Size and position (logical) |
|---|---|
| Header row | "DAY 7" plus the SECRET! tag |
| Title | 24-28 px |
| Pet portrait | 148-150 px |
| Name and KG | 16 px |
| Chips | 2 chips, 98 x 30 each |
| Button | 202 x 29-32 |

### 2.3 Scale, sizes, phone rules

- **Window scale:** `min(1.18, (safeW - 16) / 740, (safeH - topInset - 12) / 470)`.
  - On PC 1920x1080 this gives 1.18, so the window is 873 x 555 px.
  - On a phone (844x390, safe area 732, top inset 44) it gives 0.71, so the window is 526 x 334.
  - Check-UI's 0.52 clamp stays for HUD pieces. Windows fit the safe area instead, because 0.52 would put 16 px text at 8 pt.
  - MenuController's `fitScale` already slides and shrinks windows; it only needs this fit rule and the new aspect.
- **Minimum text** is 16 logical (11.4 pt on the phone, 18.9 px on PC). No TextScaled on copy: use fixed TextSize times the scale, so text can never silently shrink.
- **Type scale (logical):**

| Role | Size | Stroke |
|---|---|---|
| Title | 26-29 | 3 |
| Value | 20-22 | 2.5-3 |
| Button | 18-20 | 2.5 |
| Body / label | 16 | 2.5 |
| Badge | 16 | 2.5 |

  - All text: white or tinted fill, black (ink) UIStroke.
  - Titles add an ink copy 3 px lower for depth.
- **Copy:** at most 11 characters per line at 16 px, at most 10 at the value size.
  - Nouns become icons: the potion TYPE is the potion's colour, not words.
  - New lines for StreakClient's `lineTexts`:

| Day | Line 1 | Line 2 |
|---|---|---|
| 1 | `$9K` | `+1 POTION` |
| 2 | `+2M SPEED` | `+2 POTIONS` |
| 3 | `$18K` | `+2 POTIONS` |
| 4 | `BIG EGG` | `30K KG` |
| 5 | `3x ALL` | `POTIONS` |
| 6 | `$36K` | `+5M SPEED` |
| 7 | pet name (up to 18 characters, otherwise 2 lines) | `15K KG` |

  - Day 7 also has the chips `x5` (potions) and `$72K`.
  - Measured headroom: every line uses at most 83% of its box, which leaves room for GothamBlack being about 5% wider than the mockup's stand-in font.
- **Tap targets (phone):**
  - **The whole card is the button on touch:** an invisible full-card ImageButton behind the CLAIM button calls the same `press()`. At 0.71 a card is 112 x 119 pt.
  - **Tabs:** 148 x 38 logical. Their hit box extends into the 8 px gutters above and below (about 38 pt tall).
  - **Close [X]:** 34 px art, 46 x 46 hit box inside the header.
  - **No overlap:** hit boxes never overlap each other.
- **Safe margins:**
  - The window clears the top bar inset and the notch insets by at least 6 px.
  - On phones the left HUD tiles (UIScale 1.3) stay visible; the centred window clears them by about 7 px at 0.71.
  - The right tiles slide away while a window is open, as they already do. The phone backdrop is a raw PC capture, so it still shows them.

### 2.4 States (one rule set for every reward window)

| State | Card | Button | Badge |
|---|---|---|---|
| CLAIM (today) | Full brightness plus an inward ring (A white, B lime) | Lime, breathing 1.00-1.05 | Day pill turns lime (B) |
| CLAIMED | Content at 0.6 brightness (overlay frame, black at 0.4) | Silver "CLAIMED" | Check sticker 58 px at -8°, above the dim |
| TOMORROW | 0.82-0.85 | Dark plus clock plus live countdown `09:41:27` in lime | none |
| LOCKED | 0.45 (black overlay at 0.55). B keeps the reward preview at 0.78 so it still reads | Dark "LOCKED" | Lock 22-24 px in the top-right, above the dim |
| Day 7 locked | Never darker than 0.92: it is the carrot | "IN n DAYS" with a lock | SECRET! tag |

Where the old status line's messages go:
- **"DAY n OF 7"** becomes the streak bar's `n/7`.
- **"READY!"** is the lime card itself.
- **"Next reward in ..."** moves onto the TOMORROW card's button.
- **"Streak lost"** becomes the streak label turning red as `STREAK LOST!` for 4 s, with the pips shaking.
- **The "CLAIMED: ..." toast** becomes a `+$18K` fly-text from the card to the money pill.

### 2.5 Motion (both; per-direction flavour in sections 3 and 4)

**Idle:**
- The CLAIM button breathes 1.00 -> 1.05 (sine, 1.2 s).
- Day 7 rays turn 12°/s.
- The Day 7 shine sweep runs every 3 s.
- The "today" pip glows (transparency 0.3 <-> 0.6, 0.9 s).
- Everything pauses while the window is hidden.

**Hover (PC):**
- Buttons and tabs go to UIScale 1.04 (Quad Out, 0.08 s), centre-anchored.
- Cards don't scale: their icon tilts -6° (Back, 0.15 s) and a 6% white overlay fades in.

**Press:**
- The face drops onto its depth (Position +d, 0.05 s) and UIScale goes to 0.95.
- Release springs back with Back, 0.18 s.

**Claim celebration, in order (about 0.9 s):**
1. The button flashes white for 0.08 s.
2. The icon pops 1 -> 1.25 -> 1 (Back, 0.35 s) inside the clipped face.
3. The check stamp slams 1.8 -> 1.0 while rotating -20° -> -8° (Back, 0.22 s).
4. The card fades to the CLAIMED dim over 0.3 s.
5. 8-10 confetti pieces burst from the icon and fade in 0.6 s, kept inside the window canvas.
6. The next pip fills with a pop.
7. `+$18K` flies to the money pill (its own top layer; that is motion, not layout).
8. HatchWin SFX plays, as it does now.

**Day 7:** the existing full-screen StreakCelebrate, restyled per direction.

---

## 3. Direction A: STUDBOX

> **Everything is a toy brick on a studded baseplate.** Bright area-coloured studded cards, LuckiestGuy numbers, and a streak made of 7 studs.

### Palette

| Role | Colour |
|---|---|
| Ink | `#14162A` |
| Baseplate | `#33427C` -> `#27315F`, side `#181E3F` |
| Recess | `#1A2147` |
| Claim lime | face `#62C91C`, top `#8EE83A`, side `#2F7A0C` |
| Claimed silver | `#A9B2C8` |
| Off | `#2A3158` |
| Buy gold | `#F5A800` |
| Close red | `#E8243A` |

- **Areas** set the day-card bricks, in area order:

| Day | Area | Colour |
|---|---|---|
| 1 | Grass | `#43B91F` |
| 2 | Water | `#1987EA` |
| 3 | Thunder | `#E9AA00` |
| 4 | Fire | `#E5501A` |
| 5 | Shadow | `#7C34E0` |
| 6 | Celestial | star-night `#3445C6` with gold specks |
| 7 | all of them | a prism rim on a dark star-night face |

  - Celestial's brick is star-night rather than its gold text colour, so it doesn't clash with Thunder.
- **Halloween skin:** the header brick turns pumpkin (`#F2700F`) and gets one pumpkin sticker. Off-season the Daily header is the lime brick.

### Shapes and depth

- **Window:** a studded baseplate, radius 14, 3.5 ink outline, 7 px side. Every element is a brick at least 10 px in from the plate edge.
- **Header:** an inset brick (radius 10, side 4) holding the gift sticker, the LuckiestGuy 29 title and a red brick [X] (34 px).
- **Cards:** bricks, radius 11, side 5, 2.5 outline, studs at about 17% contrast, a 2 px light top rim.
- **Buttons:** brick, radius 7-8, side 3-4. Primary lime, purchase gold plus Robux, secondary slate, disabled silver, locked off plus lock, timer off plus clock.
- **Tabs:** the active tab is a raised lime brick; the inactive tab is sunk (no side visible) in slate with `#AEB9E6` text. The "!" dot sits inside the tab.
- **Badges:** gold price tag, dark timer pill, red ribbon (not rotated), count "x2" sticker text, red alert dot.
- **Progress:** the streak is 7 studs on a recessed plate (lime done, gold plus ring today, dark locked, prism plus star on Day 7). The generic bar is a recessed trough with a studded lime fill.

### Type, texture, icons

- **Fonts:** LuckiestGuy for display (title, values, buttons) and GothamBlack for labels.
  - LuckiestGuy breaks Check-UI's "GothamBlack only" rule; that is part of A's toy feel.
- **Texture:** studs on every face.
- **Icons:** frameless stickers with an ink drop shadow (a black copy at 0.5, offset +3 px).

### Motion flavour

- Presses sink brick-into-plate.
- Claim confetti is coloured studs.
- Day 7 celebration: the prism brick bursts into studs and the pet pops out.

### Signature

The studded baseplate and the stud streak.

**Risk:** studs are exactly what the owner's reference games use (studded +1M / Base / Jump buttons). A would make SLINGSHOT look like them, not unlike them.

---

## 4. Direction B: HATCH NIGHT (recommended)

> **Every window is a night-sky egg that has just cracked open.** A pumpkin (seasonal) band with a cracked-eggshell edge, calm dark cards where only today's reward glows, and on Day 7 the secret pet climbs out of a cracked golden shell.

### Palette

| Role | Colour |
|---|---|
| Ink | `#0D0B1C` |
| Night canvas | `#2E2566` -> `#1B1642`, depth `#0F0B28`, inner rim `#6153C2` at 0.55 |
| Card | `#3A3082` -> `#29215F`, depth `#151032`, top highlight `#7062D8` |
| Today card | `#4C3FAA` -> `#30267A` |
| Recess | `#120E30` -> `#1C1746` |
| Lavender text | `#D2CAFF` (dim `#A79FE0`) |
| Claim lime | `#B4FF4A` -> `#4FCB10`, depth `#2A7608` |
| Claimed silver | `#DEDAF4` -> `#9F98C8` |
| Off | `#463E88` -> `#352D6C` |
| Gold | `#FFE070` -> `#F59A00` |
| Shell gold | `#FFE680` |
| Close red | `#FF5A6E` -> `#E01A34` |

- **Area colours** keep their game values (Inventory/Sell `AREA_COLOR`). They appear only as the glow behind a reward, egg tints and name text, so they never fight the state colours.
- **Halloween skin:** a pumpkin band `#FFB43C` -> `#F2620A` plus a bat sticker.
  - Off-season the Daily band is HATCH GOLD (`#FFD84A` -> `#FFA800`). Other pages keep their own band colours.
  - The night canvas stays all year.

### Shapes and depth

- **Window:** solid night canvas, radius 18, 3.5 ink outline, 7 px depth, a soft violet sheen in the top-left.
- **Header:** a full-bleed band, 46 tall. Its bottom edge is a cracked eggshell: about 40 rotated squares in irregular sizes 11-17.4, each with an ink copy 5 px larger underneath.
  - The band covers the squares' upper halves, so you see an outlined zig-zag.
  - Every tooth stays inside the canvas: the first and last centres sit 16 px from the edges, so no clipping is needed.
- **Header contents:** gift sticker 38 px, GothamBlack 26 title, bats, red gloss [X] 34 px.
- **Cards:** shell cards, radius 14, depth 5, 2.5 outline. A radial glow in the reward's colour sits behind the stickers (cash green, potion colour, egg = area colour, speed cyan). The "DAY n" pill is dark and turns lime on the claimable card.
- **Buttons:** rounded radius 9-10, depth 3-4, 2.5 outline, a gloss band (top 42%, white 0.42 -> 0.08). No studs, no checkerboard.
  - Primary lime, purchase gold plus Robux, secondary dusk-violet with lavender text, disabled silver-lilac, locked dark plus lock, timer dark plus clock plus lime digits.
- **Tabs:** a segmented pill in a recessed track (radius 19). The active segment is a lime gloss pill; the inactive one is text only. The "!" dot sits inside the track.
- **Badges:** gold price pill, dark timer pill, red tag, count "x2", red alert dot, day pill.
- **Progress:**
  - The streak is 7 egg pips on a recessed pill: cracked lime eggs (a white zig-zag) are done, a glowing gold egg is today, dark eggs are locked, a prism egg is Day 7.
  - The generic bar is a pill trough with a lime gloss fill.
- **Day 7:**
  - A dark violet face with a rotating prism rim (UIStroke plus a rainbow UIGradient, Rotation +30°/s) and gold rays.
  - An egg-shaped halo behind the pet.
  - In front of the pet's feet, the lower half of a golden egg: an oval clipped to its lower half by a ClipsDescendants frame, with the same crack-teeth recipe pointing UP.
  - Title "SECRET PET!" with a gold UIGradient fill.

### Type, texture, icons

- **Font:** GothamBlack only, the Check-UI rule kept as is.
- **Texture:** none. Depth comes from the depth slab, the gloss band and the glows.
- **Icons:** frameless stickers with an ink drop shadow (a black copy at 0.55, +3 px).

### Motion flavour

- **Pips:** a done pip "cracks" (the zig-zag appears with a 2-frame wobble).
- **Claim confetti:** shell shards (small rotated gold squares) plus sparkles.
- **Day 7 celebration:** in StreakCelebrate, the golden egg wobbles 3 times, the crack runs across it, the top half flies off (rotation plus a fall tween), and the pet springs up in front of the rays while the prism title sweeps.
- **Header teeth:** no animation (they are structure).

### Signature

The cracked-shell header edge, the egg pips, and the Day 7 hatch. All three come from the game's own loop: "Slingshot for **Eggs**", grab, bank, **hatch** fierce pets.

---

## 5. Recommendation: B, HATCH NIGHT

1. **Unique to SLINGSHOT.** Studs (A) are the references' look; every studded simulator owns them. B's motifs (the cracked shell, egg pips, the pet hatching out of the card) can only belong to an egg-hatching game, and they still feel toy-like because of the chunky outlines.
2. **Reads faster.** The cards are calm and neutral, so the eye lands on the one lime card ("tap here") and the Day 7 carrot. In A, six area colours compete with the state colours.
3. **Fits the content.** The fierce, semi-realistic pets and the Halloween season both sit better on a night canvas than on bright toy bricks. Off-season, swapping the band colour is all it takes.
4. **Safe with the current HUD.**
   - The night canvas has a similar value to Check-UI's slate, so the studded Check-UI HUD tiles still match: tiles = world-facing bricks, windows = the night shell.
   - It keeps every Check-UI engineering rule, including GothamBlack only.
5. **Cheapest to build.** No new font and no texture. Everything is Frames, UICorner, UIStroke and UIGradient plus art that is already uploaded (section 6).

**Borrow from A:** nothing is required. Both share the containment rules in section 2, which fix the owner's complaint by themselves.

---

## 6. Build notes (for B; A's differences at the end)

### 6.1 How it maps onto MainMenu

The window is `StarterGui.MainMenu.Window{Depth, Face{Title, Icon, Close(hidden), Body{GiftPage{Tabs, DailyView, PlaytimeView}}}}`. The header comes from `B.header(panel, ...)` in MenuController; the red [X] comes from `B.closeButton`.

**MenuController changes:**
- `LAYOUT.Gift = {k, 1.574, titleH}`.
  - Choose `k` so that 1080p gives about 873 x 555, then let `fitScale` handle smaller screens. On phones, fit the safe area (section 2.3).
  - Choose `titleH` so the header band is 46/470 = 9.8% of the window height.
- For the Gift page only (phase 1): make Body transparent, remove its UIStroke, and set its insets to 0 so the canvas is the only box.

**GiftPage layout:**
- Build the content as an Offset canvas, `GiftCanvas` (740 x 470 logical, below the header), with a `UIScale = Window.AbsoluteSize.X / 740`.
- All numbers in section 2.2 then apply 1:1, and text sizes and stroke widths scale with it.
- Size UIStrokes in logical px. Don't also multiply them by `deviceScale()` inside this canvas; that would double the scaling.

**StreakClient changes:**
- Rebuild the tab row, DailyView and cards with the new helpers.
- Keep its logic as is: `stateOf`, `press`, attributes, auto-open, TestPress.
- Change `lineTexts` to the short copy, and route the status texts as listed in section 2.4.
- Move the pulse from `holder` to the button face.
- Make the whole card an ImageButton hit area on touch.

**PlaytimeClient:** the 12 slots reuse the card recipe (6 x 2, 113 x 165).

### 6.2 Helpers

**Reuse (BrickUI):**
- `B.brick(...)`, which builds holder{Depth, Face} with the right outlines. Pass `gradient` and `radius`.
- `B.text`, `B.image` (ScaleType Fit), `B.corner`, `B.pxStroke`, `B.closeButton`.
- `B.innerHighlight` for the 1.5 px top rim.

**New helpers** (add them to BrickUI behind a third style switch `BrickUI.STYLE = "Hatch"`, so phase 2 can restyle every window by changing one line; `"CheckUI"` stays the fallback):

| Helper | What it builds |
|---|---|
| `B.crackEdge(parent, x0, x1, yLine, color, seed, base, pointUp)` | Two rows of rotated square Frames (ink copy +5 px under each), sizes `base + ((i*7 + seed) % 5) * 1.6`, step `size * 1.386`. The caller draws the band or shell body after them. About 40 Frames per header. |
| `B.nightWindow(holder)` | Canvas gradient, inner rim stroke, 7 px depth |
| `B.hatchHeader(panel, theme)` | Full-bleed band plus `crackEdge` (themes: `Pumpkin`, `HatchGold` and the existing page colours) |
| `B.glossButton(parent, name, size, pos, palette)` | `B.brick` plus a gloss Frame (top 42%, UIGradient transparency 0.58 -> 0.92). No damier. |
| `B.shellCard(parent, ...)` | Card face, depth, top rim, glow ImageLabel, dim overlay Frame, badge layer above the dim |
| `B.eggPip(parent, state)` | An oval Frame (UICorner 0.5 plus UIAspectRatio 0.78) with a radial-looking UIGradient, and a crack ImageLabel (or 3 tiny rotated Frames) for done eggs |
| `B.segTabs(parent, names)` | The segmented pill |
| `B.prismRim(face)` | A UIStroke (Border, 4 px) with a rainbow UIGradient child, rotated in RenderStepped while visible |
| `B.dim(face, level)` | A black overlay at 1 - level. Badges are parented to the card holder above it. |

### 6.3 Assets

**No upload is required.** Reuse:

| Asset | ID / source |
|---|---|
| Cash | 131724750673548 |
| Speed shoe | 80829076123513 |
| Egg | `StreakConfig.EGG_ICONS[kind]`, fallback 135711525932647 |
| Potions | `PotionConfig.byKey.*.icon` |
| Lock | 124356037818343 |
| Check | 78526516923039 |
| Clock | Check-UI pack `Item/Clock/Clock 1st` = 106606523697579. Confirm it loads; otherwise reuse any timer glyph in the game. |
| Robux | 132185731364109 |
| Gift | 128336310005291 |
| Star | 112780117360743 |
| Rays | 76624006953375 |
| Glow | RebirthClient GLOW 121438949090215, tinted with ImageColor3 |
| Sunburst | 130563114903838 |
| Pet portrait | `IndexConfig.PORTRAITS[name]` |

**Optional (flagged; one upload each, group-owned by ZAB Studio):**
- The **bat sticker** for the Halloween band. The SVG is inside `dirB_hatchnight.html`.
- A **soft radial glow disc**, only if the halo 121438949090215 turns out to be a ring. The art already exists: `SLINGSHOT Icons/products/upload/glow.png`.

**No 9-slice is needed.** Every shape is a Frame, a UICorner or a rotated Frame.

### 6.4 Test checklist (in Studio, TestFreshSave first)

- Run a **containment script** over GiftPage:
  - Every visible GuiObject's AbsolutePosition and AbsoluteSize, grown by its Border UIStroke thickness times the scale, lies inside its parent.
  - Card, tab and chip siblings don't intersect.
  - No TextLabel has `TextFits == false`.
  - It mirrors `qa()` in `common.js`.
- Render all states with `ServerStorage.StreakDebug` (set day / claim) at 1920x1080 and in the 844x390 phone emulator.
  - Compare the result with `B_hatchnight_pc.png` and `B_hatchnight_phone.png`.
  - Also check the Studio phone emulator at 733 x 392 safe.
- Check PLAYTIME in the same window: 12 slots, no overlap.

### 6.5 If A is chosen instead

- Use `B.brick` as it is with `studsTile` (studs asset 80410732886567 already exists) for every face.
- Use LuckiestGuy (`rbxasset://fonts/families/LuckiestGuy.json`) for display text.
- The inset header brick replaces `B.header`.
- Day colours come from the area list in section 3.
- The streak is studs.

No new assets, except the optional pumpkin sticker.
