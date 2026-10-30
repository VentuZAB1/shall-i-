# Frostfang Lynx - model gate review 1 (2026-10-27) - APPROVED WITH FIXES

**Score: 7/10 for a 50 % STARTER** (the Glacier egg's commonest pet). Ship bar is about 8/10. With the MUST list applied, expect about 8.

The build is a real cat. It has a feline wedge head with heavy fierce brows, slit eyes, a rosette coat, long legs with snowshoe paws, and it is clearly not Shade Panther. The problems are one bug and four look issues, all codeable without touching the rig or the pose. **No new full model round is needed.** Send one updated `_model_sheet`, `_close_sheet`, the two icon strips and `_shares.json`, and I will check the fixes.

## What I looked at
- `pets/FrostfangLynx.py` (v2, lines 1-260 read in full, with the `rig()` / `check_pairs()` section).
- `FrostfangLynx/MODEL_NOTES.md`, `renders/_shares.json`, `_review/FrostfangLynx_plan.md` (v2), `_review/GLACIER_PLAN_REVIEW.md` section 2.1, `_review/GLACIER_CONCEPTS.md`, `FIERCE_GUIDE.md`, the Obsidian `Creature Style.md` and `Model Review Checklist.md`.
- Renders: `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `flat_side.png`, `flat_game.png`, `flat_tq.png`, `model_side.png`, `model_front.png`, `model_back.png`, `model_tq.png`, `close_tq.png`, `close_front.png`, `close_side.png`, `FrostfangLynx_icon.png`.
- Comparisons: `ShadePanther/renders/_model_sheet.png` and `_close_sheet.png`, `BrambleBadger/renders/_model_sheet.png`, `Raiju/renders/_model_sheet.png`, `IceMammoth`, `GlacierYeti`, `BlizzardRoc`, `FrostcrownDragon` `_model_sheet.png`, `_ALL_FIERCE_progress.png`.
- My own zooms (outside the project, in `C:\Users\ventu\AppData\Local\Temp\lynx_rev\`): the front-eye crop, the rump saddle crop (flat and model), the flat side silhouette at 3x, the game flat view at 3x.

## Measurements (my own pixel count on the flat renders, non-background pixels)
Non-background pixels of the flat renders include anti-aliased edges. The builder's shares are within about 0.2 points of mine.

| view | ICE (Lynx) | AMBER (Badger, starter sibling) | Glacier siblings |
|---|---|---|---|
| side | 0.5-0.6 % | 2.8-4.9 % | MINT (Mammoth) 0.1 %, AURORA (Yeti) 0.8 %, GOLD (Frostcrown hero) 1.3-1.7 % |
| game | **0.85-0.95 %** | **8.5-12 %** | |
| tq | 1.2-1.4 % | | |

ICE_CLAW (214,244,255) is 0.9 % side / 1.9 % tq, but it reads as white, not cyan.

Shares: side WARM 48 %, BACK 27 % (rosettes + saddle), SNOW 13.5 %, BLACK 4 %. Game: WARM 46 %, BACK 32 %, SNOW 11 %.

---------------------------------------------------------------------------------------------------------------------
## 1. The two questions from the brief

### Q1 - Is the ice accent too weak at 0.7 %?
**Yes, for a GLACIER pet.** At 64 px the Lynx reads as a tan spotted cat with two cyan ear tips. The ICE is mostly invisible, and the egg's ice identity is missing from the commonest pet. In the game colours the Lynx's ICE is 0.9 % of the pet. The Badger's amber in the same game colours is 8.5-12 %, about ten times as much. The plan target was 5 %. The builder's reason (horn-sized tufts read as a goat) is valid for the ear tufts, but the accent does not have to come from the ears.

**Raise it to about 3 % side / 2.5-3 % game, without horns, from four places:**
1. **Claws: ICE_CLAW (214,244,255) becomes ICE (150,236,255)** on all 8 claws (`pets/FrostfangLynx.py` line 215, `ICE_CLAW` -> `ICE`). Smooth, role detail. This adds about +0.9 % side and +1.9 % tq, and it makes the "icy claws" of `act_clawflex` read in the ICE sparks. No goat risk.
2. **Ruff tips: the outer 40 % of each cheek ruff spike goes ICE** (lines 170-174, 4 spikes per side). Split each SNOW spike into a SNOW base (60 %) and an ICE tip (40 %, the same direction, width about 0.8x, smooth). This adds about +1.5-2 % side. It reads as frost on the fur, and it is sideways, not a chin beard, so it does not add a goat read.
3. **Fangs: the name is "Frostfang", so the fangs should be the frost.** Line 151: the TEETH spikes (0.050 long, 0.011 half-width) become ICE_CLAW, 0.066 long, 0.014 half-width. Smooth, role detail. This is a close-up accent (the owner will see it from the side and in the tq), and it puts the name on the model.
4. **Eyes: enlarge the ICE iris a little** (line 160: half-size (0.030, 0.006, 0.0098) -> (0.034, 0.006, 0.0120)). Keep the BLACK vertical pupil on top (line 162-163), see MUST 4. About +0.1-0.2 %.

Expected total: about 3-3.5 % side, about 2.5-3 % game. That is enough for a starter, and it is not a horn. Do **not** add ICE to the ear tufts' length or add a chin tuft: those are the goat read.

### Q2 - Does it read as a lynx (not a dog or goat), and is it fierce not cute? Distinct from Shade Panther?
- **Lynx: 6/10 as drafted, reaching 8 with MUST 2.** The face, the ears, the long legs and the ruff say cat and fit a lynx. The spotted coat in the side view looks more like a **leopard or jaguar**, because the tail is long (0.33 units, about 0.37 of the body) and the spots are heavy. A lynx is recognised by its **bobtail**. Shorten the tail (MUST 2) and the lynx read follows.
- **Dog: no.** The head is a wedge with a flat forehead and a short muzzle. From the front it has no dog-like long snout.
- **Goat: low risk at 64 px, moderate at 128 px.** The 128 px icon shows the tall ears with two thin cyan spikes as "horns" (`_icons_strip_128.png`, the Lynx is first). The chest bib (line 130-131) and the cheek ruff are the other goat cues. Keep the ruff flaring sideways (it does), keep the chest bib under the chest, and do not hang anything below the jaw.
- **Fierce vs cute: fierce 7/10.** The brows are heavy, the eyes are slits, the nose is black, and the body is not chibi (head about 0.25 vs body 0.30 wide). It loses fierceness in two places: the big **white snow socks** on the front legs (line 205, the SNOW sock rises 0.07 above the paw, so the forelegs look like white stockings), and the tail. Shorten the front sock to 0.035 (NICE 1).
- **Distinct from Shade Panther: yes, 8/10.** The Panther is indigo-violet with violet crystals and a bulky head. The Lynx is sand-silver with dark spots, cyan and white, and a lean body. Both use heavy BACK_SHADE brows, which is a shared family look but not a copy. The accent families are not the same (Panther violet, Lynx ICE cyan).
- **Distinct from the Badger (also a starter):** warm beige vs a cool lilac-grey, and different silhouettes. Accepted.

---------------------------------------------------------------------------------------------------------------------
## 2. MUST list (before the clip gate)

### M1 - BUG: the rump and rib saddle tubes float 0.03 above the body (`saddle()` line 105, `DZ` loop lines 252-257)
The body is lowered by `DZ = -0.030` in the DZ loop. That loop shifts `blk.pts` and `blk.c`, but **not `blk.rings`**. The saddle is a `Tube` (blockkit `class Tube`, lines 134-156), and its mesh is built from `t.rings` (`_tube_bm`, line 163). So the saddle keeps its un-lowered height. In `model_side.png` the hips saddle is clearly a grey slab hovering above the rump with green visible under it (about 0.02-0.03 units), and the rib saddle sits high too. That is a floating part, which the checklist fails.
- **Fix (pick one):**
  - in `saddle()` add `+ Vector((0, 0, DZ))` to each ring point on line 105, or
  - in the DZ loop, call `blk.map(lambda q: q + dz)` for `Tube` items (`Tube.map` updates `rings`, `pts` and `c`).
- After the fix, check that the saddle still sits flush on the top of each block with no green gap in the side view.

### M2 - Make it a LYNX: a bobtail (line 34, `TAILP`; tail widths lines 250-251)
The tail is 0.33 units long (0.37 of the body): a cat tail, which leads to the leopard read. A lynx has a short bobtail with a black tip.
- New `TAILP`: `[(0, 0.43, 0.725), (0, 0.50, 0.70), (0, 0.55, 0.66), (0, 0.59, 0.63)]`, which is about 0.19 long (about 0.2 of the body).
- Keep the black tip band on the last segment (`i == 2`, line 251).
- Also keep `FX_SnowFlick` on `TAILP[3]` (line 286), which moves with it.
- Pass: the side silhouette reads as a short stub, not a leopard tail.

### M3 - Raise the ICE accent to about 3 % side (see Q1, the four places)
- Claws: `ICE_CLAW` -> `ICE` on line 215.
- Ruff tips: outer 40 % of each of the 8 ruff spikes (lines 170-174) -> ICE, smooth.
- Fangs: line 151 `TEETH` -> `ICE_CLAW`, length 0.050 -> 0.066, half-width 0.011 -> 0.014.
- Eyes: line 160 ICE slit half-height 0.0098 -> 0.0120, half-width 0.030 -> 0.034.
- Re-measure with `flat_side` and `flat_game`. Target: ICE at least 2.5 % side and 2 % game. Anything below that fails.

### M4 - The eye: the cat pupil is not visible at the front close-up (lines 156-165)
In the zoomed front close-up (`close_front.png`) the eye reads as a cyan window in a black frame. I could not make out the vertical black pupil (line 162-163, half-size 0.0072 x 0.0120, at y -0.714, in front of the ICE slit at y -0.706). The brow block on line 164-165 sits right over the inner top of the slit and may hide the top half of the pupil.
- Check the pupil in the front close-up. If hidden, move the pupil forward (y -0.714 -> -0.722) and raise the brow 0.004 (line 164, z 0.958 -> 0.962), or shorten the brow's inner droop (rot -26 -> -20).
- Pass: a black vertical slit is visible in the middle of the cyan from the front, and the brow still reads as fierce.

### M5 - The ear: stop the tuft reading as a horn (lines 176-188)
The ears are tall spikes (base 0.08 wide, tip 0.26 of base), and the two ICE pencils (lines 186-188, 0.070 and 0.058 long, half-width 0.0115) rise above them like antennae or horns. At 128 px that is the goat/horn read.
- Shorten the pencils to 0.045 and 0.040 (keep the same width), so the total ear height drops by about 0.03. Or make the ear base 0.10 wide (line 179, half-width 0.040 -> 0.048) so the ear reads as a lynx triangle.
- Pass: at 128 px the ears read as lynx ears with frosted tips, not as horns.

---------------------------------------------------------------------------------------------------------------------
## 3. NICE list (do these too)
1. **Front sock** (line 205): the SNOW sock on the front lower leg rises 0.07 above the paw, which makes "white stockings". Drop it to 0.035 (keep the paw snow). Reduces the cute read.
2. **Saddle read:** from the back view and `game_view.png`, the three saddle tiles look like flat grey plates with gaps (and read pale in the model back view). Once M1 is fixed the gaps close. If it still reads like tiles, make it one continuous band over the top of the chest, waist and hips (one saddle tube, not three).
3. **Leopard risk:** the legs carry 3 extra spots each (lines 237-247). Remove the lowest spot on each shin (line 242 and 247, `blob(... lo ...)`) to lower the leopard count. The rosette share stays above 20 % because the flank spots carry it.
4. **Belly tuck:** the underline from chest to hind legs is nearly straight with a small tuck near the hips. Not a box, but raise the waist underline by about 0.015 units, so the belly line rises toward the hind legs.
5. **Ruff fan:** the four cheek spikes per side fan out like blades in the front close-up (`close_front.png`). Shorten the outermost spike (line 174, 0.088 -> 0.072) so the fan reads as fur, not fins.
6. **Icon:** `FrostfangLynx_icon.png` reads well. After M3 the ice ruff and claws should show in the icon. Recheck it.

---------------------------------------------------------------------------------------------------------------------
## 4. Pass/fail checklist (model gate)

| # | item | result |
|---|---|---|
| 1 | 64 px silhouette: species reads at once | **PASS (partial).** Cat with ear tufts and a spotted coat. Reads leopard-ish until M2 |
| 2 | 128 px: no goat/horn read | **FAIL.** Ears + pencils read as horns. M5 |
| 3 | Game camera: body reads sand-silver, rosettes and SNOW underside visible | **PASS.** Game WARM 46 %, BACK 32 %, SNOW 11 % |
| 4 | Face: fierce slit eyes under a heavy brow, no googly eyes, no glint, no smile | **PARTIAL.** Brows and slits are fierce. Pupil not clearly visible (M4) |
| 5 | Head: lynx wedge, not dog or goat | **PASS** (dog: no). Goat: low risk at 64 px, moderate at 128 px |
| 6 | Accent: ICE at least 2.5 % side / 2 % game (starter: close to Badger's read) | **FAIL.** 0.5-0.6 % side / 0.9 % game. M3 |
| 7 | Palette follows the plan (WARM 190,172,150 / BACK 126,116,110 / SNOW 240,244,250 / ICE 150,236,255) | **PASS.** Matches plan v2 |
| 8 | Rosettes >= 20 % of the side view | **PASS.** 20.3 % (builder) |
| 9 | Floating, poking or intersecting parts | **FAIL.** Saddle floats 0.03 above the rump and rib (M1) |
| 10 | Parts visible from below | **PASS.** Claws and snowshoe paws are fine from the low camera |
| 11 | Tri count <= 15k | **PASS.** 6,416 |
| 12 | Distinct from Shade Panther (no copied accent or act) | **PASS.** 8/10 |
| 13 | Stud skin: details (eyes, claws, tufts, fangs, saddle) smooth where planned | **PASS.** Eyes, claws, pencils and brows are smooth. Keep the new ICE claws, ruff tips and fangs smooth too (`role="detail"` or `nostud=True`) |
| 14 | Tail reads as a lynx bobtail | **FAIL.** 0.33 long, reads as cat/leopard. M2 |
| 15 | Fierce, not cute (no socks, no fluff-blobs) | **PARTIAL.** Front socks read cute (NICE 1) |

Score tally: 8 PASS, 3 PARTIAL (items 1, 4, 15), 4 FAIL (items 2, 6, 9, 14). Every FAIL and PARTIAL maps to a MUST or NICE item. Verdict: **APPROVED WITH FIXES, 7/10.**

## 5. Re-send checklist (one round, no full review again)
- `pets/FrostfangLynx.py` diff (M1-M5 and NICE 1)
- `FrostfangLynx/renders/_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `flat_side.png`, `flat_game.png`, `_shares.json`
- A `model_side.png` crop at the rump (to show M1 is gone) and a `close_front.png` crop at the eyes (to show the pupil, M4)
- Clip gate: the `pose_tq` sheets for `idle`, `walk`, `roar`, `act_clawflex` are not needed for this model review. Send them with the clip gate as usual.
