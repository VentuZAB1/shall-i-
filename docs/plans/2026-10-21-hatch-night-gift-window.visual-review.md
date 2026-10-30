# Visual review: HATCH NIGHT Gift window (2026-10-21)

Reviewer: visual reviewer (art director). Read-only: no game change, no Studio Play. In Edit I only read the source of `StreakClient` and `PlaytimeClient` so I could cite exact values.

**What I looked at:**
- **Mockups:** `B_hatchnight_pc.png`, `B_hatchnight_phone.png`, `B_hatchnight_sheet.png`.
- **Docs:** the spec, the plan and the plan review.
- **Build shots:** all 40 files in `docs/plans/hatch-night-build/`, plus my own 2x to 4x crops. Pixel samples were taken with PIL.
- **Starter Pack shots:** `starter_hud_v3_*` and `starter_popup_v3_*`.
- **Chrome snapshots:** `hatch_chrome_*.txt`.

**Capture artefact.** The no-world shots also have no header bats, because the bats are ViewportFrames (see SHOULD 10).

## Verdict: **FIX THEN SHIP**

**The DAILY tab is close to the mockup.**
- Side by side (`hatch_mockup_vs_build_pc.jpg`), it matches nearly element for element.
- Cards, tabs, streak bar, header, teeth and Close are all inside their boxes.

**Seven things stop me from signing it off as is:**
- Three are small overlaps of the exact kind the owner complained about: the hero button, the day stickers, and the celebration's flying shell half.
- One is a brightness slip: the week-done pet.
- Three are on the last-minute PLAYTIME tab:
  - an off-centre SKIP ALL;
  - an empty quarter of row 2;
  - a 2-hour pet slot that reads as nothing.

All seven are small, local edits. Nothing needs a redesign.

---

## MUST fixes

### 1. Day 7 hero button: it jams into the prism rim and the lime ring

**Evidence:**
- `hatch_pc_day7_claim_zoom.png` and `hatch_pc_flash_petsfull.jpg`: CLAIM! / PETS FULL! run edge to edge and sit on the rim.
- The builder's own note: 1.7 px under the rim at the pulse peak.

**Why, at rest:** `StreakClient` line 259 is `glossButton(face, "Button", 10, 300, 202, 29, ...)`.
- Its stroked bottom is 300 + 29 + 2.5 = **331.5**.
- PrismRim's inner edge is **331** (the frame is 4..331; its stroke is drawn outside).
- So the button is already 0.5 px into the rim at rest, and 1.7 px at 1.05.
- Sideways at 1.05 it reaches x 2.7, inside the lime Ring band (4..7) and the rim (0..4).

**Fix (Card7.Face):**

| Element | Now | New |
|---|---|---|
| `Button` | (10, 300, 202, 29) | **(16, 297, 190, 28)**, d 3, r 10, ol 2.5 |
| `Button.Face.LockIcon` | (40, 4, 19, 19) | **(34, 4, 19, 19)** |
| LOCKED label place (`setLabel`, d == 7) | (34, 3, 168, 18) | **(28, 3, 162, 18)** |
| `setLabel` width `W` for d == 7 | 202 | **190** (timerLayout re-centres the clock and timer) |
| `Chip1` | (10, 264, 74, 30) | **(10, 262, 74, 28)** |
| `Chip2` | (92, 264, 120, 30) | **(92, 262, 120, 28)** |
| Chip children | | every y minus 1: potion images y 3, Count y 5, Cash (5, 2, 24, 24), Value y 5. If `H.chip` has no height argument, add one. |

**Resulting clearances (logical px):**

| Edge | At rest | At pulse 1.05 |
|---|---|---|
| Top, from the chips' outline (292) | 2.5 | 1.8 |
| Bottom, from PrismRim (331) | 3.5 | 2.8 |
| Sides, from the Ring band (7) | 6.5 | 1.75 |
| Kg text bottom (about 257.5) to the chip outline (260) | 2.5 | |

**Test (`hatch_containment.lua`):** with `HatchTestPulse = 1.05`, at scales 1.18 and 0.6787:
- `Card7.Face.Button`'s stroked box is at least 1.5 px inside PrismRim's inner box (4, 4, 214, 327);
- and at least 1.5 px below the stroked boxes of Chip1 and Chip2.

### 2. Day stickers overlap the DAY pill (Days 1, 3, 4 and 6)

**Evidence:** `hatch_card_states_zoom.png`, `hatch_pc_mid_zoom_row1.png` and my 3x crop of Day 3.
- The game's cash brick (131724750673548) fills its box right to the top edge. At y 21 its top corner sits about 2 px **over** the DayPill's bottom outline (the pill is 6..26, the lime outline reaches 28).
- Day 4's thorn egg touches the pill.
- The mockup's banknote art had padding, which is why the mockup numbers didn't collide.

**Fix:** the `ICONS` table, `StreakClient` lines 160-167. Every centre is kept, and every bottom stays at 89 or above (89 is the value line).

| Day | Now | New |
|---|---|---|
| 1 | `{"cash", 45, 21, 68}` | **`{"cash", 48.5, 28, 61}`** |
| 3 | `{"cash", 45, 21, 68}` | **`{"cash", 48.5, 28, 61}`** |
| 4 | `{"egg", 46, 23, 66}` | **`{"egg", 49, 29, 60}`** |
| 6 | `{"cash", 37.5, 23, 66}` | **`{"cash", 40, 28, 61}`** |

The Money potion, the shoe, the counts and the Check stamp do not change.

**Test:** add a cousin check for Card1..6: every `Icons.Pop` sticker's top is at least **28** (DayPill bottom 26 + lime stroke 2). The current tile checks never compare `Icons.Pop` with `Face.DayPill`.

### 3. The week-done pet is too dark: 0.36 instead of 0.6

**Evidence:** `hatch_pc_weekdone.jpg`, measured against `hatch_pc_day7_tomorrow.jpg`.

| Area | Brightness vs TOMORROW | Matches |
|---|---|---|
| Pet | 0.46 | |
| Chip icons | 0.39 | |
| Golden shell in front of the pet | 0.63 | the intended 0.6 |

So the trophy the player just earned looks like it's sitting in shadow behind a brighter shell. It is also darker than every other CLAIMED icon (0.6).

**Cause.**
- The hero's Pet and chip images sit **under** `Dim`.
- `setCardState` (line 345) dims to 0.6, and line 346 also tints to 153.
- Small cards don't double-dim, because their icons sit above `Dim`.

**Fix:** line 346 `local v = done and 153 or 255` -> **`local v = 255`** (the hero only). The result is an effective 0.6, the same as all CLAIMED icons. Keep the Check stamp, the 0.6 Dim, and the rays, prism and shine.

**Check:** the mean luma of the pet box in week-done should be about 0.6 / 0.95 = 0.63 of TOMORROW's, not 0.46.

### 4. Day 7 celebration: the flying shell half crosses the pet

**Evidence:**
- `hatch_cel_realclaim.jpg` and `hatch_cel_2_topflies_petrises_zoom.png`: a translucent yellow wedge with a hard ink arc covers half the pet during the reveal.
- `TopHalf` is a child of `Egg` (ZIndex 4), so it always draws above `PetRoot` (ZIndex 3). Its path, egg (24, -96) then (24, 324), drops it straight through the pet.

**Fix (StreakCelebrate, Box.Pop):**
- Reparent `TopHalf` from `Egg` to **`Pop`**. Its rest Position becomes **(229, 144)** (Egg origin 235, 150 plus -6, -6).
- New Pop ZIndex order:

| Child | ZIndex |
|---|---|
| Rays | 1 |
| Halo | 2 |
| **TopHalf** | **3** |
| PetRoot | **4** |
| Egg (BottomHalf, teeth, WholeEgg, CrackLine) | **5** |
| TitleRoot, Name, Sub, Tap | 6 |

  The pet now rises in front of the lifting lid and behind the bottom half.
- **New lid path:**
  1. `Position (339, 74)`, `Rotation 30`, over 0.25 s, Quad Out (up and to the right, off the pet);
  2. then `Position (399, 474)`, `Rotation 110`, `GroupTransparency 1`, over 0.5 s, Quad In;
  3. then `Visible = false`.
- **Reset** (line 655): `Position (229, 144)`, Rotation 0, GroupTransparency 0.

### 5. PLAYTIME: SKIP ALL content is off-centre

**Evidence:** `hatch_pc_playtime_restored.jpg` and my 2x crop.
- "SKIP ALL [R] 48" occupies x 12..148 of a 207-wide gold button.
- That leaves **59 px of empty gold** on the right. It reads as broken.

**Fix (PlaytimeClient):** lay the group out from measured widths whenever the price text changes, and in the skip-flash restore. Use `tw = H.textWidth("SKIP ALL", 16)` (68) and `pw = H.textWidth(price, 16)`:

| Item | Value |
|---|---|
| Group width `G` | `tw + 6 + 20 + 4 + pw` |
| Start `x0` | `floor((207 - G) / 2)` |
| `SkipLabel` | (x0, 5, tw + 2, 16), left aligned |
| `Robux` | (x0 + tw + 6, 4.5, 20, 20) |
| `Price` | (x0 + tw + 30, 5, pw + 4, 16), left aligned |

For "48" (pw about 20, G = 118) this gives x0 = 44: label 44, Robux 118, price 142, about 44 px of padding on both sides.

The error flash keeps `(12, 5, 183, 16)`.

### 6. PLAYTIME: row 2's right half is an empty 400 x 38 hole

**Evidence:** `hatch_pc_playtime_restored*.jpg` and the phone shot.
- On DAILY, row 2 is tabs + streak bar.
- On PLAYTIME it is tabs + nothing. That one empty quarter is the main reason the tab looks unfinished next to DAILY.

**Fix.** Keep the owner's restored footer and grid. Fill the slot with a session bar that mirrors the streak bar and sells "LEAVING RESETS PROGRESS!".

**`PlaytimeView.PlayBar`** = `H.recess(view, "PlayBar", 330, 66, 400, 38, 2)` with `HatchPad 8`, `HatchTile "row2"`, `HatchGap 8`. It is the same recipe as `DailyView.Streak`.

| Child | rect | Look |
|---|---|---|
| `Label` | text ("PLAYED", 14, 11, 76, 16) | LAV, stroke 2, z 4 |
| `Track` | Frame (98, 11, 204, 16) | corner 8, BackgroundColor3 (11,8,32), stroke 2 INK, z 2 |
| `Track.Fill` | Frame (0, 0, w, 16), `w = max(16, 204 * p)`, hidden while p == 0 | white plus UIGradient 90 (180,255,74) -> (79,203,16), corner 8, z 1 |
| `Track.Fill.Gloss` | Frame (4, 2, w - 8, 5) | white, BackgroundTransparency 0.55, corner 3 |
| `Time` | text (fmt(elapsed), 310, 10, 80, 18) | WHITE, stroke 2.5, z 4 |

- `p = clamp(elapsed() / (C.SLOTS[#C.SLOTS].min * 60), 0, 1)`, so the bar fills toward the 2-hour pet.
- Update it in `refreshSlots`, so it does no work while the window is closed.
- "1:59:59" at 18 is 56 px, which is 70% of the 80 px box.

The alternative layout is owner's call 1.

### 7. PLAYTIME: the 2-hour pet slot (Slot12) needs the carrot treatment

**Evidence:**
- `hatch_pc_playtime_restored.jpg` and `hatch_phone_playtime_restored_zoom.png`: the bonus pet is the PLAYTIME tab's Day 7, but it is drawn as a generic slot at WAIT 0.85 x tint 217 (about 0.72).
- Its portrait is 34 logical, which is 24 px on a phone: a dark smudge.
- Its name "VENOM BASILISK" at 18 fills 87% of the slot (144 of 166 px).
- The old layout made this the gold cell (`hatch_playtime_OLD_layout.jpg`). The restore dropped that.

**Fix: Slot12 only, with no geometry change.**
- **Brightness:** WAIT `setBright` **0.95** and `tint` **255** (spec 2.4's carrot rule: "never darker than 0.92"). CLAIM and CLAIMED are unchanged.
- **Prism stroke:**
  - `Slot12.Face` and `Slot12.Side` UIStrokes become **Color WHITE + a UIGradient child = H.RAINBOW**, Thickness 2.5 (unchanged, so no containment change).
  - Gradient Rotation += 30 deg/s in the existing RenderStepped, only while `shown`.
  - In CLAIMED, restore INK and remove the gradient (the stroke is outside `Dim`).
- **Glow:** `Glow` ImageColor3 (255,214,90), ImageTransparency 0.6 -> **0.35**.
- **Name:** `Value` uses TextSize **16** in box (4, 5, 166, 18): 128 px = 77%. Keep the `{name, last word}` variants.

The bigger portrait is SHOULD 8.

---

## SHOULD fixes

1. **Refusals should look like refusals.**
   - Today "EGGS FULL!" / "PETS FULL!" / "NOT READY" show on a **pulsing lime** button (`hatch_pc_flash_*`), which still says "tap me".
   - While `flash[d]` (or `c.flash`, or `skipFlash`) is active:
     - call `btn.setPalette("red")` (label white);
     - skip `btn.pulse` in RenderStepped.
   - On expiry, restore `PALS[st]` (hero: lime/dusk/off as in `setCardState`) and let the pulse resume.
   - This applies to Card1..7, Slot1..12 and SkipAll.
2. **LOCKED label contrast.**
   - Measured (80,75,107) on (30,24,58), about **2.0:1**, which is illegible at 0.71.
   - The mockup was just as dark, but it's still too dark.
   - Set the small-card "off"-palette label TextColor3 to **WHITE**. Under the 0.45 Dim that gives (115,115,115), about 3.5:1.
   - The hero LOCKED label stays GOLD_TXT (its Dim is 0.95).
3. **Centre the TOMORROW timer group on small cards.**
   - Today it sits 6.3 logical left of centre, because `TIMER_W = textWidth("00:00:00", 17)` is wider than the live digits.
   - Use `tw = label.TextBounds.X / CanvasScale` after the fit: `gx = floor((W - (18 + 6 + tw)) / 2 + 0.5)`.
4. **Tab labels to match the mockup's weight.**
   - In the side-by-side, the build's DAILY / PLAYTIME read about 18% smaller.
   - Pill label and `LabelDaily` / `LabelPlaytime`: TextSize 18 -> **20**, label box y 10 -> **9**, height 22.
   - "PLAYTIME" at 20 is 93 px in 120 (78%).
5. **Day 2 / Day 6 speed copy.**
   - "+2.17M SPEED" at 20 is about 87% of its 150 px box, cramped on phones (`phone_mid` crop).
   - Round the card lines to 2 significant digits: "+2.2M SPEED", "+5.4M SPEED", via a local `short2()` around `SpeedStat.Format`. This brings them to 80% or less.
6. **PLAYTIME footer warning weight.**
   - The owner's reference made "Leaving Resets Progress!" the loudest line. The build's 16 px is the quietest.
   - `Warning`: TextSize **20**, box (14, 424, 340, 22). The text is about 268 px (79%) and ends at x 354, well clear of SkipHit (519).
7. **PLAYTIME WAIT timers.**
   - Use the DAILY TOMORROW treatment for consistency: a Clock ImageLabel (16 x 16, y 4) plus the lime digits as one centred group.
   - `gx = (150 - (16 + 6 + tw)) / 2`; State at gx + 22, left aligned.
8. **A bigger pet portrait in Slot12.**
   - Owner to approve: it breaks the old cell pattern for this one slot, as the old gold cell did.
   - Use a portrait-left layout:

| Element | Value |
|---|---|
| `Icons.Pop.Icon` | sticker (12, 2, 54); 56 + 3 shadow = 59, which is under the button outline at 59.5 |
| Name, line 1 | `NameTop` (70, 10, 98, 16) |
| Name, line 2 | `NameBottom` (70, 30, 98, 16) |
| Name split | at the last space; GOLD_TXT; `HatchMin 15` |
| `Glow` | (6, 2, 66, 58) |
| `Value` | hidden |

   - The portrait goes from 24 px to 38 px on a phone.
9. **SkipAll hover.**
   - The restored `glossButton(view, "SkipAll", ...)` call lost `hoverScale = 1`.
   - At 1.04 its right outline reaches x 736.1, which is 3.9 px from the window rim and breaks its own HatchPad 8.
   - Pass `hoverScale = 1`, with hover = gloss 0.58 -> 0.45, as review MUST 2 specified.
10. **Bats.** Both bats are missing in every no-world capture (phone, PLAYTIME, LOST), because they're ViewportFrames. Take one live 844x390 emulator capture to confirm they render at 0.71 and stay left of Close (x < 688).
11. **Celebration punch.** It reads (wobble, crack, pet, rainbow title) but has no impact beat.
    - At t = 1.45, add `Pop.Burst` = glow ImageLabel (white), centre (320, 250), size 60 -> 420, ImageTransparency 0.1 -> 1, over 0.25 s, Quad Out, ZIndex 3.
    - Add 14 shell shards from (320, 250): `H.shards` recipe, r 120-200, 0.7 s.
    - Add 6 star stickers (112780117360743, 18 px) around the pet.
      - Ring radius 120, centred (320, 170).
      - Idle twinkle: ImageTransparency 0.2 <-> 0.7, Rotation ±15, period 1.1 s, phase per star.
12. **Starter Pack consistency.**
    - The HUD sticker cluster already fits HATCH NIGHT (frameless stickers, ink stroke, no frame).
    - The **popup** is still Check-UI: pink checker header, slate canvas, checker BUY / grey NO THANKS. New players get both windows in their first minutes.
    - Make it the first phase-2 page:
      - night canvas plus `hatchHeader` keeping its pink band (spec: other pages keep their band colours);
      - BUY = `glossButton` gold + Robux;
      - NO THANKS = dusk-violet secondary with LAV text (sheet);
      - the odds row in an `H.recess`.
    - Pick one Robux glyph: SKIP ALL's grey 132185731364109 on gold is low-contrast; the HUD's lime glyph reads better.

## Owner's calls

1. **PLAYTIME footer.**
   - **(a)** Keep the restored footer and add the PlayBar (MUST 6). This is my default.
   - **(b)** Move the warning + SKIP ALL into row 2 (the original PlayBar) and grow the 4 x 3 slots to 174 x **108**:
     - rows y 112 / 228 / 344, face 103;
     - icons (65, 25, 44), pet (64, 24, 46), Button (12, 76, 150, 24).
     - The icons go from 32 to 44: a big readability win, but it drops the old footer position the owner asked for.
2. **Egg silhouettes.**
   - `UICorner 0.5` on 170 x 200 makes a **capsule** (30 px straight sides), not an egg: the celebration egg reads as a yellow pill. The pips show the same thing at 5 px.
   - Fix: one upload, a 256 x 320 white egg-silhouette PNG, group ZAB Studio.
     - Use it as an ImageLabel with the existing UIGradient fill and an INK copy at 108% behind it for the outline.
     - Use it for WholeEgg, the TopHalf and BottomHalf ovals, the hero Bowl, and `eggPip`.
   - There is no clean no-upload version.

---

## What's good

- **Mockup fidelity on DAILY is high.** Night shell, pumpkin band with the cracked-shell teeth, gift sticker and ink-copy title, segmented lime pill, egg pips with crack zig-zags and lime links, four readable card states, the hero's turning prism rim, rays, halo and golden half-shell. Side by side, it is the mockup.
- **Containment fixed at the root.**
  - One container (no box in a box).
  - 8 px gutters, 10 px edges, 11 px bottom.
  - Rings under the content.
  - No rotated ribbons.
  - Close and the bats inside the band.
  - Teeth stop above the tabs.
  - The owner's complaint is gone everywhere except the four overlaps above.
- **State reading.** The one lime card is unmistakable. CLAIMED at 0.6 with the check is clearly done. The TOMORROW timer reads. LOCKED keeps the reward preview at 0.78, as specified. The Day 7 carrot stays at 0.95.
- **Refusals now show real reasons** ("EGGS FULL!", "PETS FULL!", "NOT READY"). The TRY AGAIN bug is fixed.
- **PLAYTIME is the owner's 4 x 3 layout** in the new look: 174 x 94 slots (old cells were about 1.9:1), 8 px gaps, footer in the old place.
- **Other windows are untouched.**
  - Shop before/after is visually identical.
  - `hatch_chrome_after_s4.txt` is byte-identical to BEFORE.
  - Gift-first vs fresh runs match (0 of 792 lines differ).
- **Performance is clean.**
  - About 0.03-0.08 ms per frame.
  - Zero work while closed.
  - No instance or VPF growth over 30 open/close cycles.
- **The phone fit (0.7106) clears the left HUD.** CTA text is 12.8 px or more, and the minimum is 11.4 px.

## Answers to the brief

1. **Fidelity.** DAILY matches. These differences matter:
   - the cash art hits the pills (MUST 2);
   - the hero button is too wide (MUST 1);
   - labels are about 18% smaller (SHOULD 4);
   - pips and eggs are capsules (owner's call 2);
   - the live "+2.17M" copy is cramped (SHOULD 5).
2. **The owner's complaint.** Tabs, streak bar, header and bats are clean. The remaining overlaps:
   - the hero button vs the rim (MUST 1);
   - stickers vs the day pill (MUST 2);
   - the lid vs the pet (MUST 4);
   - SKIP ALL hover vs the rim (SHOULD 9).
   - The PLAYTIME grid itself is clean: 8 px gaps, slot buttons stay inside the face at pulse (88.5 at rest, 89.1 at peak, clipped by 0.1).
3. **Readability.**
   - PC is fine.
   - Phone: 11.4 px minimum is acceptable, but LOCKED labels (2:1) fail (SHOULD 2).
   - Dims: claimed 0.6 is right, locked 0.45 + preview 0.78 is right, tomorrow 0.85 is right. **Week-done 0.36 is too dark** (MUST 3).
4. **PLAYTIME.** It is the old 4 x 3 layout. It is less polished than DAILY because of the empty row-2 half (MUST 6), the off-centre SKIP ALL (MUST 5), the anonymous pet slot (MUST 7) and a too-quiet warning (SHOULD 6). The header height is the same as DAILY's, which is right.
5. **Celebration.** It reads: wobble, crack, pet, rainbow title. It needs the lid fix (MUST 4). More punch is SHOULD 11, and the true egg shape is owner's call 2.
6. **Other windows.** Unchanged (proved above).
7. **Starter Pack.** The HUD art is consistent. The popup is the old look and should be the first phase-2 page (SHOULD 12).
