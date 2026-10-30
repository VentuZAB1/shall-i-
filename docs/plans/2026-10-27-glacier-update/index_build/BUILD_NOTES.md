# Index v8 build notes (Glacier update, 2026-10-28)

The approved Index v8 mockup is now the real Creature Index in Studio, with live data. Built by the Opus UI builder.

**Not done by me:**
- Nothing was saved or published.
- The command bar and Studio dialogs were not touched.
- `Camera.CameraType` was never set.
- `TestFreshSave` is back to **false**.

## Review 5 MUST: long card names (2026-10-29, round 6)

- **Phones only:** a card name that would render under 9 px on its card drops words from the end until it fits at 9 px, measured with `TextService:GetTextSize` against the label's own width.
  - Examples: FROSTCROWN DRAGON → FROSTCROWN, PERMAFROST TITAN → PERMAFROST, BLACK EASTERN DRAGON → BLACK EASTERN.
  - The inspect panel and PC always show the full name. No pet is renamed. `SHORT_CARD_NAMES = false` (IndexClientLegacy) turns it off.
  - The check runs again after every phone re-layout (`applyCardNames` in the applyPhoneText wrapper). The label keeps a `FullName` attribute for the tests.
- **Shortened with all 42 found:**
  - S22 Ultra: 14 names (BRAMBLE, MOSSBACK, THORNBLADE, SEA TURTLE, HAMMERJAW, INFERNO, CINDER, NIGHTMARE, BLACK EASTERN, PHARAOH, CELESTIAL, COSMIC, PERMAFROST, FROSTCROWN).
  - iPhone 13 and 17 Pro: FROSTCROWN only (Glacier).
  - iPhone 16 Pro Max: none.
- **Badge clearance:** the bigger names touched the SECRET/MYTHIC badges. On phones the card name now sits 0.005 lower (phoneBox y 0.12) and its outline scales: 1.56 → max(1.2, 1.56 × scale).
- **Tests:** `v8legible` adds three checks: Glacier card names ≥ 9 px, the inspect panel keeps "FROSTCROWN DRAGON", and every area's found names ≥ 9 px. The last one was RED with all 42 found (BLACK EASTERN DRAGON 5 px) before the fix.
  - PC suite 61/61.
  - v8device 12/12 and v8legible 6/6 on the S22 Ultra, iPhone 13, iPhone 17 Pro and iPhone 16 Pro Max.
- **Labels under 9 px (v8 seed):** S22 Ultra 10, all exactly 8; the other three phones 0.
- **Captures:** 31 / 31b S22 Ultra, 32 iPhone 13, 33 iPhone 17 Pro, 34 iPhone 16 Pro Max (all full screen), 35 PC full viewport.

## Phone legibility round 5 (2026-10-29, owner: "at least 8.5/8.3" on every device)

One layout everywhere; the phone is still the PC layout scaled.

### Changes
- **MenuController (phones, viewport height < 520):**
  - The Index window aspect is 1.9 (PC 1.575); the height is unchanged (size B).
  - The size box is widened to fit the aspect. Without that, FitWithinMaxSize shrank a 749 x 389 phone's window to 289 of 307 px.
  - The window slides right of the money/speed pills. Where it can't fit beside them, it narrows, never below the PC aspect (iPhone 16 Pro Max: 1.867).
- **IndexClientLegacy, all devices:**
  - Chance pill 0.12 -> 0.16 of the card (y 0.80, x 0.2-0.8), cap 13 -> 15.
  - SECRET / MYTHIC badges 0.13 -> 0.15 tall, 0.52 -> 0.58 wide. They grow upward: y -0.055 to 0.095 (bottom was 0.10). Cap 12 -> 14.
  - BONUS pill 0.16 -> 0.175 wide at x 0.80; the progress bar is 0.015 narrower.
- **IndexClientLegacy, phones only:**
  - The "!" text fills its dot (phoneBox 0.96).
  - Subtitle box 0.33 -> 0.38.
  - Card name box 0.02 lower (0.115-0.265).
  - The SECRET badge's 2 px Border outlines scale like the chip strokes.
- **IndexClientLegacy, the wide phone window only** (canvas >= 1.8 x DESIGN_H):
  - KEEP fits: CLAIM ALL 1.12, count 1.15, BONUS 1.15.
  - The count dot is 0.62 -> 0.75 tall.
  - A phone window at the PC aspect (v8phone on PC) keeps fit 1.
- **Bug found:** the SECRET badge covered the top of the card name on phones, in the old build too. The gap was -1.7 px, counting the badge outline and the name stroke. It is now +0.6 px on the S22 Ultra and more on the other phones.

### Tests (ServerStorage.HatchRISTests.index_client)
- New `v8legible(floor, maxSmall, hardMin)`: lists every on-screen label under `floor` px (TextBounds.Y), reports the smallest, and checks that SECRET/MYTHIC clear the name glyphs (outlines counted) and the header. The badge check FAILED on the old badge geometry and PASSES now.
- `v8device`: re-opens the Index first (for a device switched during Play) and runs the shared `keepClear` (CLAIM!, CLAIM ALL, count, chips, BONUS). Pill margin 4.5 px.
- Results:

| Device (emulator) | Viewport | Window | v8device | Labels < 9 px | Smallest |
|---|---|---|---|---|---|
| PC (Current device) | 1519 x 753 | 881 x 559 | suite 61/61 | - | - |
| Samsung S22 Ultra | 677 x 338 | 486 x 256 | 12/12 | 12 (19 before) | FROSTCROWN DRAGON 6 |
| iPhone 13 | 749 x 389 | 583 x 307 | 12/12 | 1 | FROSTCROWN DRAGON 8 |
| iPhone 17 Pro | 749 x 381 | 568 x 299 | 12/12 | 1 | FROSTCROWN DRAGON 7 |
| iPhone 16 Pro Max | 831 x 439 | 666 x 357 | 12/12 | 0 | 9 |

- S22 Ultra labels still at 8 px: 4 chips, "!", SECRET, CLAIM ALL, subtitle, BONUS and count. PERMAFROST TITAN is 7 px. Both long card names are width-bound in their card.

### Captures
26 / 26b S22 Ultra, 27 iPhone 13, 28 / 28b iPhone 16 Pro Max, 29 PC, 30 iPhone 17 Pro.

### Backup
`ServerStorage._Backup_GlacierS2.IndexPhoneBoxes` holds the client, MenuController and tests from before this round. The earlier `.IndexPhoneWide` holds MenuController from before the wide window.

## Build review 2 round (2026-10-29)

Review 2 scored PC 8.8 (pass) and phone 7.5. It had one MUST: on the phone, the CLAIM! and CLAIM ALL labels touched their button edges, and the count badge sat on the last "L" of CLAIM ALL. This was a regression from the review 1 text floor. The owner-decision items (MYTHIC in the pill, "Income", wider plates, taller pills, bigger "!") were **not** touched.

### Changes

**`IndexClientLegacy`** (41313 → 50466 chars, hash 1926401873; before: `_Backup_GlacierS2.IndexBuild3`)
- **Phone clearance (phones only).** Every label the floor grew is trimmed to its box after layout: its text, black outline included, keeps **3 screen px** from the box's left and right edges.
  - **Boxes:** the label's own button, pill, badge, plate, chip or tab. The header title and subtitle end at the progress bar. The strip title ends at the first chip. A stat label ends at its value's text.
  - **Chip texts:** keep 3 px from the chip's right edge and 1 px from the icon's picture on the left.
  - **CLAIM! and CLAIM ALL:** also keep 3 px above and below their letters.
  - **Count badge digit:** not trimmed; it is a badge, not a button label.
  - **How it trims:** only the label's rect shrinks; TextScaled then fits the text, one step smaller where needed. A settle pass measures the shown labels a frame later and trims again where TextScaled still drew a few tenths of a px past the rect. The trims stay until the window size changes.
- **CLAIM ALL vertical allowance (`padV` 0.5).** On the pixels of a 299 px window, the 3 px outline's anti-aliasing on the orange showed above the letters: at text size 9 there were only 2 px clear above. The allowance steps CLAIM ALL down to size 8, which leaves 4 px above and 3 below. CLAIM! keeps size 10, since its pixels already clear 4 px above and 3 below.
- **Count badge.** On a phone, the CLAIM ALL count badge moves 2.5 screen px up and 2.5 px right. On PC it stays at the v8 spot.
- **`IndexPage.PhoneClear:Invoke()`** returns every shown phone label's clearance. The tests and this note use it.
- **Finding:** under the page's UIScale, `UITextSizeConstraint.MaxTextSize` and `TextBounds` are both in screen px; UIStroke thickness does scale with the UIScale. As a result `evenChips` (which divides by `CanvasScale`) only evens the chips on PC. On a phone, "+5%" stays as small as its width allows while "x1" reaches about 11 px. I left this as is for the owner, because evening the chips would shrink "x1" to the "+5%" size. The comments in the script say so.
- **PC:** unchanged. Every rect and cap is v8 (checked by `v8phone`, and visible in capture 20).

**`index_client` tests** (41023 → 42388 chars, hash 907712311)
- `v8phone` now checks three window sizes: 299 px (the iPhone 17 Pro emulator), 330 px (a 36 px bar) and 308 px (844 × 390). At each, every shown label must have at least 3 px of clearance (at least 1 px from a chip's icon). The CLAIM labels must also clear 3 px vertically, and the count badge must be clear of the CLAIM ALL letters.
- The v8open check is renamed "CLAIM ALL = review 5 M1 burnt orange".

### Clearance per label (299 px window = the emulator's size, scale 0.528)

Clearance is screen px between the text (outline included) and the box's left / right edges; "cap" is the cap height including the outline.

| Label | Left / right | Above / below | Cap |
|---|---|---|---|
| CLAIM! | 6.7 / 6.7 | 3.1 / 3.1 | 9.5 |
| CLAIM ALL | 7.3 / 7.3 | 3.0 / 3.0 | 8.9 (was 9.6, one step down) |
| Count badge ring to the CLAIM ALL letters | 3.0 gap | | |
| "+5%" chips | 1.2 from the icon / 3.2 | | 6.1 |
| "x1" chips | 1.7 from the icon / 3.7 | | 9.7 |
| Card names (ICE MAMMOTH, BLIZZARD ROC) | 3.0 / 3.0 | | 8.8 |
| FROSTFANG LYNX | 3.5 / 3.5 | | 7.4 |
| FROSTCROWN DRAGON | 3.6 / 3.6 | | 6.0 |
| PERMAFROST TITAN | 5.0 / 5.0 | | 6.7 |
| GLACIER YETI | 6.5 / 6.5 | | 8.8 |
| Stat labels | 3.0 on the left / 5.9-42.9 before the value | | 5.2-9.5 |
| Stat values | 3.0 on the right | | 9.1-10.5 |
| Tab names | 3.4 to 11.9 on the left / 4.8 to 13.3 on the right | | 8.1 (CELESTIAL) to 11.7 |
| Tab progress | 18.5 or more | | 8.8 |
| SECRET / MYTHIC badges | 3.4 / 3.8 | | 8.1 |
| Chance pills | 13.0 or more | | 7.3 |
| Rarity pill | 5.2 / 5.2 | | 6.7 |
| Inspect name | 6.7 | | 8.6 |
| Header title / subtitle | 6.7 / 8.7, 7.1 / 13.1 | | 11.2, 7.5 |
| BONUS 1/1 | 8.0 | | 11.8 |
| COMPLETE GLACIER: | 3.1 / 6.3 | | 9.7 |
| 5 / 5, DISCOVERED | 21 or more | | 10.5, 10.8 |
| Count digit "1" (not trimmed) | 3.4 inside its circle | | 6.5 |

- **Pixels (299 px capture):** CLAIM! has 9 / 6 px of fill clear left / right and 4 / 3 above / below. CLAIM ALL has 8 / 6 and 3 / 3. The badge ring is 5.2 px from the nearest letter pixel.
- **308 px:** CLAIM! 7.5 / 3.3; CLAIM ALL 8.2 / 3.2 (cap 9.0); badge gap 3.7.
- **330 px:** CLAIM! 6.2 / 3.0 (cap 11.2); CLAIM ALL 8.9 / 3.3 (cap 10.0); badge gap 4.0.
- **No label exceeds its box minus 3 px** at 299, 308 or 330 px (49 labels each, `v8phone`).
- **Cost of the fix:** the "+5%" chips drop to a 6.1 px cap. The chip is 32 px wide with a 12 px icon, which leaves 13 px for the text. Before, they read 8.3 px but ran to within about 1 px of the chip's edge. CLAIM ALL drops from 9.6 to 8.9.
- **PC (unchanged v8):** CLAIM! 12.8 / 5.3 px, CLAIM ALL 15.3 / 5.7 px. The tightest PC label is the v8 "+5%" chip at 1.8 px from its edge; I left it alone because PC must not change.

### Tests (TestFreshSave Play sessions, viewport 1519 × 753)

| Section | Result |
|---|---|
| v8open | 16 / 16 |
| v8tabs | 7 / 7 |
| v8cards | 17 / 17 |
| v8inspect | 5 / 5 |
| v8claimui | 6 / 6 |
| v8phone | 8 / 8 |
| v8claim | 6 / 6 (after the documented server step) |
| legacy | 3 / 3 |

**Total: 68 / 68.** The console shows no script errors or warnings.

### Captures

| File | What |
|---|---|
| `19_r2_phone_mock_749x381_topbar58.png` | Phone mock at the emulator's size: 749 × 381, 58 px bar, window y 64.0 to 362.4 (capture 18: 63.5 to 362.5), Glacier with Frostcrown selected |
| `19b_r2_phone_mock_strip_footer_zoom4x.png` | Its reward strip and footer at 4× |
| `20_r2_pc_reward_strip_footer_2x.png` | PC reward strip and footer at 2× (unchanged v8) |
| `20b_r2_pc_full_glacier_frostcrown.jpg` | The full PC frame |

### Exports and backups

- **Exports (`src/`):** `IndexClientLegacy.lua` is the full live script (hash 1926401873, same as Studio). `review2_index_client_patch.json` holds the exact test edits; applied to the `IndexBuild3` backup it reproduces the live module (checked by hash).
- **Backups:** `ServerStorage._Backup_GlacierS2.IndexBuild3` holds the review-1 `IndexClientLegacy` and `index_client`, as disabled clones with tags stripped.
- `MenuController` was not changed in this round.

## Build review 1 round (2026-10-29)

Reviewer scores were PC 8.7 and phone 7.5, so the build went to REVISE. This round was redone from scratch in Studio `3bf21205-...` after the crash; Studio had been restored to the first-build state. The earlier copy of this round (captures 09-13) was lost with the crash and is superseded by 14-17.

**Status per item:**
- **Done:** M1 (with exceptions listed below), M2, N3, N4, N5.
- **M3:** done by the lead (capture 18, see below), not by me.
- **Report only:** N2.
- CLAIM ALL keeps its burnt orange fill (the review 5 M1 colour).

### Changes

**`IndexClientLegacy`** (37177 → 41313 chars, hash 1933766780)
- **M1 phone text floor.** When `CanvasScale` < 0.75 (phones only), each registered label gets two changes:
  - Its cap becomes `max(PC cap, ceil(13 / CanvasScale))`. (Review 2 found that this cap is in **screen** px, not design px, so on a phone it never binds; the text is as big as its box allows.)
  - It gets a slightly larger box inside its own parent, up to the full pill or plate.
  - No zone moves, so there is still one layout. `PhoneText` is set on the page as an attribute.
  - Stat labels are fitted so their text ends before the value text (`fitStatLabels`).
  - On PC, every rect and cap is exactly the v8 one (checked by `v8phone`).
- **N3.** "GLACIER CREATURES" now uses box 0.47 × 0.47 with cap 22, and the subtitle uses box 0.47 × 0.33 with cap 15. At PC they measure 218 and 212 px wide; v8 was 219 and 213.
- **N4.** An unfound creature's pill shows the area name only, with no SECRET / MYTHIC word and no `$x` bonus.
- **N5.** The centre "?" on a silhouette is hidden; only the "???" name plate stays.

**`MenuController`** (28857 → 29149 chars)
- **M2.** On phones (viewport height < 520), the Index window height is the gui height − 24, with its top 6 px under the top bar. That gives 308 px with a 58 px bar (y 64 to 372) and 330 px with a 36 px bar (y 42 to 372). The width cap is 92 %.

**`index_client` tests** (38954 → 41023 chars)
- Card6 must have no centre "?".
- An unfound mythic's pill must read "GLACIER".
- A found secret's pill must read "GLACIER · SECRET · $x..".
- An unknown Bramble's pill must read "GRASS".
- New section `S.v8phone`: the real window resized to 308 px. It checks that `PhoneText` turns on, no zone moves, stat labels clear their values and the caps are raised. Then it resizes back to PC and checks that the v8 rects and caps are restored.

### Tests (Play session with TestFreshSave on, viewport 1519 × 753)

| Section | Result |
|---|---|
| v8open | 16 / 16 |
| v8tabs | 7 / 7 |
| v8cards | 17 / 17 |
| v8inspect | 5 / 5 |
| v8claimui | 6 / 6 |
| v8phone | 5 / 5 |
| v8claim | 6 / 6 |
| legacy | 3 / 3 (earlier run in the same Studio) |

**Total: 65 / 65.**

v8claim failed its first check once in the final run. The capture data I had seeded had the Frostcrown found, which breaks the test's precondition. I re-ran the documented server step (Glacier non-mythics found, area 7 unclaimed), and it then passed 6 / 6.

The console shows no script errors.

### Phone cap heights (on screen; cap height incl. outline ≈ 0.72 × font + 2 × stroke)

**308 px window (58 px bar, `CanvasScale` 0.544): 21 of 52 labels are below 9 px.**

| Label | px | Limited by |
|---|---|---|
| Income (best KG) | 6.0 | row width, shared with the value |
| FROSTCROWN DRAGON (card name) | 6.0 | card width |
| count badge "1" | 6.5 | badge circle |
| rarity pill "GLACIER · MYTHIC · $x8.8" | 6.7 | pill width |
| PERMAFROST TITAN (card name) | 6.7 | card width |
| chance pills (6) | 7.4 | pill height (~9 px pill) |
| "Hatched from the Glacier Egg" | 7.6 | header height |
| BONUS 1/1 | 7.6 | pip size |
| "!" badge | 7.9 | badge circle |
| MYTHIC / SECRET badges (2) | 8.1 | badge height |
| FROSTFANG LYNX (card name) | 8.2 | card width |
| +5% chips (2) | 8.3 | chip width |
| Best weight | 8.8 | row width |
| CELESTIAL tab | 8.9 | tab width |

**Passing at 308 px:**

| Label | px |
|---|---|
| $83.5M/s | 9.1 |
| inspect name | 9.4 |
| Hatched | 9.6 |
| Hatch chance | 9.6 |
| ICE MAMMOTH / BLIZZARD ROC / GLACIER YETI | 9.6 |
| tab progress | 9.6 |
| COMPLETE GLACIER | 9.7 |
| 5 / 5 | 10.6 |
| DISCOVERED | 10.8 |
| stat values | 11.3 |
| GLACIER CREATURES | 11.3 |
| CLAIM! | 12.5 |

**330 px window (36 px bar, scale 0.583): 17 below 9 px.**

| Label | px |
|---|---|
| Income | 6.1 |
| rarity pill | 6.9 |
| FROSTCROWN | 6.9 |
| count "1" | 7.2 |
| PERMAFROST | 7.6 |
| "!" | 8.1 |
| chance pills (6) | 8.2 |
| FROSTFANG | 8.3 |
| BONUS | 8.4 |
| subtitle | 8.4 |
| SECRET / MYTHIC | 8.9 |

**PC (559 px window): 0 of 52 below 9 px.**

Before this round (capture 07, 58 px bar), stat labels were 6-9 px font and card names 7-9 px font.

**Owner / lead decision.** The rest can only reach 9 px with bigger containers, which means changes to the layout itself:
- longer card plates or shorter names;
- a taller chance pill;
- a shorter rarity string;
- "Income" in place of "Income (best KG)".

### M3 (emulator capture): done by the lead

My own attempt was stopped by a user interrupt, so I did not drive the emulator. The lead then took the real capture: `18_emulator_iphone17pro_glacier_frostcrown.jpg` (iPhone 17 Pro emulator, 749 × 381 viewport, 58 px top bar).

It shows the window at y 63.5 to 362.5, which meets M2 on a real device: 18.5 px clear of the bottom edge.

### N2 (portraits, report only; no uploads)

The uploaded `P_IceMammoth.png` and `P_FrostfangLynx.png` are byte-identical to `PetsV3/<name>/<name>_portrait_raw.png`. They are not semi-transparent:

| Portrait | Interior semi-alpha pixels | Overall semi-alpha (edge anti-aliasing) |
|---|---|---|
| Ice Mammoth | 105 of 60,864 (0.17 %) | 4.7 % |
| Frostfang Lynx | 86 of 44,698 | 8.1 % |

On magenta neither shows any translucency. They look washed out for three reasons:
- the light-blue palette sits on the pale ice card;
- Roblox's downscale softens the dark stud grooves;
- the 12 Glacier portraits lack the black outline the 30 older portraits have.

**Fix for the lead:** add the same black outline (about 6 px at 512) and/or a contrast / sharpen pass, or upload a pre-downscaled 256 px version.

### Captures (new names)

| File | What |
|---|---|
| `14_r1b_phone_mock_topbar58.png` | 844 × 390 mock, 58 px bar: window y 64-371, 307-308 px (79 %), 485 px wide, PhoneText on |
| `15_r1b_phone_mock_topbar36.png` | 36 px bar: y 42-371, 329-330 px (84.5 %), 519 px wide |
| `16_r1b_pc_glacier_mythic.jpg` | PC, Glacier tab, Frostcrown selected |
| `17_r1b_pc_celestial_unfound.jpg` | PC, Celestial: unfound cards (one "???" each, no centre ?), unknown pill = area only |

### Exports (`src/`, crash-safe)

| File | Contents |
|---|---|
| `IndexClientLegacy.lua` | the full live script |
| `review1_MenuController_patch.json` | exact old → new edits against the first-build backups |
| `review1_index_client_patch.json` | exact old → new edits against the first-build backups |

Applying each patch to its `IndexBuild2` backup reproduces the live source exactly (checked by hash).

### Backups

`ServerStorage._Backup_GlacierS2.IndexBuild2` holds the first-build `IndexClientLegacy`, `MenuController` and `index_client`. All are disabled clones with tags stripped, taken before this round's edits.

## What changed (first build, 2026-10-28)

### 1. `StarterPlayer.StarterPlayerScripts.IndexClientLegacy` (rebuilt, 744 lines)

**Approach:** the page is rebuilt from the recovered mockup code: `mock_73374` for the layout, `mock_74213` for the white select frame on the mythic and the blue footer trough, `mock_74229` for the mythic inspect. It uses the mockup's own helpers (`frame`, `brick`, `text`, `damier`) and its numbers. An exact copy is in `src/IndexClientLegacy.lua`, hash-checked against Studio.

**Scaling (one layout on every device):**
- `Body.IndexPage` is drawn in the mockup's pixels: the face is 562 px tall (`DESIGN_H`, L102).
- A `CanvasScale` UIScale is set to face height / 562 (L200-221). Strokes, corners, bevels and text caps all scale with the window, so a phone shows the PC page scaled down.

**Line map:**

| Lines | What |
|---|---|
| L39-101 | v8 colours |
| L64 | `CLAIM_ALL` = review 5 M1: (214,98,0) → (190,68,0), bevel (120,48,0); its label has a 3 px black stroke |
| L75 | Tab colours from the mockup |
| L144 | `brick` |
| L230 | `PORTRAIT_CROP` (see note below) |
| L319-344 | 7 tabs, data-driven: one per `IndexConfig.AREAS`. Each shows x/N, a gold star when claimed and a red ! when claimable. Badges moved 4 px right and 4 px up (review 5 NICE) |
| L346-358 | Area header. The "5 / 5" bar counts only the cards the claim needs. The BONUS x/y pip shows only when the area has a mythic; otherwise the bar widens |
| L360-423 | 2 × 3 card slots, data-driven: rows = ceil(max creatures / 3). See card types below |
| L425-472 | Reward strip (title, 4 chips that share the smallest fitted text size, CLAIM) |
| L474-500 | Footer: DISCOVERED x/N with a blue fill, CLAIM ALL with a count badge. When nothing is claimable, CLAIM ALL hides and the trough takes the whole footer |
| L502-541 | Inspect panel (ring + disc, portrait, name, area / rarity pill with the money bonus, 4 stat rows) |
| L554 | `refresh()` |
| L702, L708 | `selectArea` / `selectCard` |
| L715 | `claim` (see behaviour below) |
| L726 | `TestPress` |

**Card types:**
- **Normal:** in the area's colours. Glacier uses the mockup's exact light-ice colours.
- **SECRET:** gold card, pale inner rim and the pink SECRET badge.
- **MYTHIC:** the Day-7 rainbow ring, a navy card, a disc and the MYTHIC badge (rainbow edge). When selected it also gets the white select frame; the frame, ring and card scale 1.04 together.
- **Not found:** black silhouette, "?" and "???", on a dimmed card.
- Names longer than 14 letters are capped at 12 px, which gives FROSTCROWN DRAGON its margin (review 5).

**Behaviour kept:**
- Tabs and cards are clickable, with Check-UI hover and press feedback on a centre-anchored UIScale.
- The default selection is the first discovered creature.
- **Inspect:** income at the best KG, best weight, times hatched and hatch chance (`CreatureConfig.odds(egg, 1)`).
- `CLAIM AGAIN!` and the "NEW PET!" title for areas that grew since they were claimed.
- **Claim:** `Claim:InvokeServer(areaIndex | "all")` as before; it is now wrapped in `pcall` with a client busy flag. A successful claim plays `SFX "Rebirth"`.
- **Refresh:** only while the page is visible, on `IndexData` changes, or when the page opens.
- **Names other scripts or tests use:** `Body.IndexPage`, `Tab1-7`, `Card1-6`, `Header`, `Grid`, `Reward.Claim`, `Total.ClaimAll`, `Inspect.Stat1-4`.
- **New attributes:** `IndexV8` and `IndexRefreshN`. `TestPress` is new (a Studio test hook).

**No rarity names:** the common pill says "GLACIER" (plus `$xN` when the creature has a money bonus), not "GLACIER · COMMON". The vault's Don't Repeat list bans rarity names. The v7 states image showed "COMMON".

**Portrait crop (`PORTRAIT_CROP`):**
- The uploaded portraits have wide margins, so the new pets looked about 60 % of their mockup size.
- I measured every `IndexConfig.PORTRAITS` image as it is uploaded. Each was drawn on magenta in Studio and its alpha box read from a screen capture, at about 2 px precision with 6 px of padding. EditableImage pixel reads are disabled in this experience's security settings, so I did not use them.
- Each image is cropped with `ImageRectOffset` / `ImageRectSize`.
- The first try, using the bounding boxes of the local `PetsV3` raw PNGs, cut off the Fire pets. Several uploads are different renders from those files.
- A portrait that is re-uploaded later needs a new entry; until it gets one, it shows the full image.

### 2. `StarterGui.MainMenu.MenuController` (owner-approved `fitScale` kept)

| Lines | Change |
|---|---|
| L161-162, L194 | `fitScale(size, widthCap)`: an optional per-page width cap. The default is still the 58 % `WIDTH_CAP`. The window stays centred and only shrinks |
| L233-273 | `CHROME.Index` + `applyChrome(name)`: header 0.15; book (0.065, 0.07, 0.075, 0.14); title (0.5, 0.075, 0.6 w); [X] (0.955, 0.075, 0.046, 0.073); `Depth` hidden; face 0.993 tall and centred; `Body` = the full face with its card hidden (transparent, no stroke, ZIndex 2). Every other page gets its saved defaults back. I checked this live: Shop, Rebirth and Gift opened after the Index have their old chrome |
| L337 | `LAYOUT.Index = {2.013, 1.575, 0.105}` (v8: aspect 1.575, about 0.82 height) |
| L339-343 | Calls `applyChrome`; the header height comes from CHROME when a page has an entry |
| L353-362 | Phone size B: when viewport height < 520, the Index height = 0.88 × screen height. `fitScale` keeps it inside the gui area, which starts under the top bar, with 6 px clear. Width cap is 92 % there; at 58 % it would shrink the window to about 80 % |

### 3. `ServerStorage.HatchRISTests.index_client` (428 → 665 lines)

- The old sections test the HATCH NIGHT client, which has been parked in `_Backup_HatchNight.Disabled` since 10-22. I updated their counts:
  - "rail: 7 hits" (L117)
  - zones with 6 cards
  - `for slot = 1, 6`
  - Pct1..6
  - Prog "0/6" and "6/6"
  - DISCOVERED "/ " .. `IndexConfig.total()`
- **They can't run until that client is back.** A header note says so.
- New sections for the live page: `v8open` (L444), `v8tabs` (L497), `v8cards` (L529), `v8inspect` (L574), `v8claimui` (L607), `v8claim` (L642, a real claim after a Server "complete area 7" step without the mythic).
- **How to run:** the client can't see ServerStorage. Clone the module into ReplicatedStorage from the Server datamodel, then `require` it on the Client.

## Tests (TestFreshSave Play sessions, Studio viewport 1519 × 753)

| Section | Result |
|---|---|
| v8open | **16 / 16** (final run, after the badge move) |
| v8tabs | **7 / 7** (all 7 areas: header, 6 cards, the chances, BONUS pip only on Fire / Celestial / Glacier, selected rim) |
| v8cards | **16 / 16** |
| v8inspect | **5 / 5** |
| v8claimui | **6 / 6** |
| v8claim | **6 / 6** (a real `Index.Claim` for Glacier without the Frostcrown: claimed[7] = 1, IndexBonus 0.05, +1 Money and +1 Hatch potion, CLAIMED! silver + star, a 2nd press pays nothing) |
| legacy | **3 / 3** |

**Fails fixed along the way:**
- **Two test bugs in the first run** (now fixed): a float comparison on the header height, and Card4's x read while Card1 was scaled up by its selection.
- **v8claim, first session:** IndexBonus jumped 0 → 0.15. The save I seeded already held claims for areas 2 and 3, so 3 claims × 0.05 = 0.15. That is correct behaviour; the check is now "0.05 × all claims".
- **GLACIER "!":** the 2 px move still touched the R, measured from the text bounds. Moved to 4 px; it now passes.

## Captures (this folder)

| File | What |
|---|---|
| `00_compare_v8_mockup_top_vs_build_bottom.png` | v8 mockup (top) vs the live build (bottom), same selection |
| `01_glacier_mythic_frostcrown.jpg` | Glacier tab, Frostcrown (mythic) selected |
| `02_glacier_secret_permafrost.jpg` | SECRET selected |
| `03_glacier_common_icemammoth.jpg` | A common selected (pill "GLACIER · $x1.3") |
| `04_fire_cinder_mythic.jpg` | Fire tab, Cinder mythic card selected; 2 unfound silhouettes, "2 LEFT" |
| `05_celestial_unfound_silhouettes.jpg` | Celestial: 4 unfound cards (incl. the unfound mythic), unknown inspect |
| `06_water_claimed.jpg` | A claimed area (CLAIMED! silver, star) |
| `07_phone_844x390_topbar58.png` | Phone mock with a 58 px top bar |
| `08_phone_844x390_topbar36.png` | Phone mock with a 36 px top bar |

**Test save:** Grass 5/6, Water and Thunder 6/6 claimed, Fire 4/6 (Cinder found), Shadow 3/6, Celestial 2/6, Glacier 6/6 unclaimed. That is 32 of 42 discovered.

**PC window:** 881 × 559 = exactly the 58 % width cap (v8 was 903 px wide before the cap).

## Phone check (computed, plus a PhoneMock canvas)

**Method:**
- The real window was cloned into an 844 × 390 canvas, sized by the same arithmetic as MenuController size B, with the top-bar band drawn in.
- The page `CanvasScale` and the device-scaled chrome strokes were set as on a phone.
- The Studio Device-emulator check was not done: my first click in Studio was stopped by a user interrupt, so I did not retry computer use. Review 5 wants an emulator check with the real top bar.

| Top bar | Window top | Height | Width | Below the bar? | Text ≥ 12 px |
|---|---|---|---|---|---|
| 58 px (today's top bar) | y 64 | 320 px = **82 %** (fitScale: 390 − 58 − 12) | 504 px (60 %) | yes | 8 of 54 labels |
| 36 px | y 42 | 342 px = **87.7 %** | 539 px (64 %) | yes | 10 of 54 labels; smallest 7 px |

**Layout around the window:** on touch phones the money / speed pills move to the top-left (x ≤ 140) and the menu tiles end before x ≈ 110. The window starts at x 170, so `fitScale`'s pill-dodge does not shrink it.

**Not met: text ≥ 12 px on the phone.**
- With one layout at 82-88 % height, the page is 0.57-0.60 of its PC size.
- The mockup's text caps are 12-20 design px, so most labels land at 7-11 px:
  - stat labels 6-9 px
  - card names 7-9 px
  - chance pills 7 px
  - tab names 8-14 px
  - CLAIM! 12 px
  - the window title 33 px
- The approved size-B phone mock had the same sizes; this build matches it.
- Reaching 12 px needs bigger text boxes. That means a phone-specific arrangement, which the owner ruled out, or a bigger window, which isn't possible because it already uses 82-88 % of the height. **This is a decision for the owner or lead.**

**Text sizes on screen:** `TextBounds` reads in screen px. `evenChips` divides by `CanvasScale` to get the design-px cap.

## Backups

- `ServerStorage._Backup_GlacierS2.IndexBuild`: `StarterPlayer__StarterPlayerScripts__IndexClientLegacy`, `StarterGui__MainMenu__MenuController`, `ServerStorage__HatchRISTests__index_client`. All are disabled clones with tags stripped, saved before any edit.
- The older pre-Glacier IndexClientLegacy is still in `_Backup_GlacierS2.Before`.

## Left for the owner or lead

- **Save + Publish** (the owner).
- **Phone:**
  - a fresh emulator capture to confirm review 2 MUST 1 on the device (the lead's capture 18 is from before this fix);
  - the decision on the labels still under 9 px (see "Build review 2 round" and "Build review 1 round").
- **CLAIM ALL colour:** the owner's yes on the burnt orange (review 2 NICE 1; show capture 16 or 20).
- **Portraits:** new or re-uploaded portraits need a `PORTRAIT_CROP` entry. To measure one, draw it on magenta in Play and read the box from a capture.

## Build review 2 MUST, redone by the lead (2026-10-29 ~02:10)

The round-2 trim (rect clearance loop) passed its own mock, but on a **real Studio emulator** (iPhone 17 Pro, 749x381, top bar on) it shrank the labels: CLAIM! 7 px tall in a 7 px box, CLAIM ALL 5 px, "+5%" wrapped onto 2 lines in a 7 px wide box, "Income (best KG)" on 2 lines (capture `19c_emulator_iphone17pro_round2_trim_REGRESSION.jpg`).

- **Root cause:** UITextSizeConstraint caps act in screen px on this page. On a phone a design cap (16 / 20) never binds, so TextScaled fills the whole rect. The outlines don't scale either, so a phone label sat bigger in its button than on PC.
- **Fix:**
  - Back to the review-1 client (`_Backup_GlacierS2.IndexBuild3`). The round-2 version is kept in `_Backup_GlacierS2.IndexBuild4` and `src/IndexClientLegacy_round2_SUPERSEDED.lua`.
  - CLAIM!, CLAIM ALL, the count digit and the 4 reward chips are no longer floored.
  - On a phone, `applyKeep()` scales their caps and outlines by CanvasScale (the PC look, shrunk) and nudges the count badge 3 screen px right and up.
  - evenChips evens the 4 chips in screen px on a phone; PC stays exactly v8.
- **Tests** (`index_client` v8phone, new checks; RED first: CLAIM! -1.1 px, CLAIM ALL -0.3, badge -5.7, chips wrap):
  - Final: v8open 16/16, v8tabs 7/7, v8cards 17/17, v8inspect 5/5, v8claimui 6/6, v8phone 9/9 = 60/60.
  - Not re-run: v8claim and legacy (their code is untouched).
- **Real emulator after the fix** (iPhone 17 Pro, `21_emulator_iphone17pro_after_claim_fix.jpg`):
  - CLAIM! 36x11 text, 6.2 px clear each side.
  - CLAIM ALL 45x8, 7.3 px each side.
  - Chips "+5%" 16x8 and "x1" 8x8: all one size, one line.
  - The badge is clear of the letters.
- **Live client hash** 2909339269 (42972 chars), saved to Roblox. The other labels are as in the review-1 round.
