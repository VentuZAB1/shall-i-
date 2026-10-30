# Frostfang Lynx - model gate review 2 (2026-10-27) - APPROVED WITH FIXES

**Score: 8/10 for a 50 % STARTER** (up from 7/10). Ship bar is about 8/10, so one small MUST remains (the throat bib, section 2). Once that is fixed and checked with one front crop and one below crop, the Lynx ships. No further full model round is needed.

Round 2 landed every review-1 item and most of the NICE list. The Lynx now reads as a frosted lynx with a bobtail, a clean saddle, a fierce face and a real Glacier accent. The one thing I would not accept as it is, is the flat chest bib.

## What I looked at
- `FrostfangLynx/renders/_model_sheet.png` (5 panels: back 3/4, front, side, tq, front-3/4)
- `FrostfangLynx/renders/_close_sheet.png` (front, side, tq close-ups of the head)
- `FrostfangLynx/renders/game_view.png`
- `FrostfangLynx/renders/_icons_strip_64.png` and `_icons_strip_128.png` (the Lynx is first, then Badger, Panther, Raiju from the earlier sets)
- `FrostfangLynx/renders/_shares.json` and `MODEL_NOTES.md` (round 2 section)
- New crops: `crop_rump_side.png`, `crop_eyes_front.png`, `low_below.png`, plus `model_side.png`
- My own check on the flat renders (`flat_side.png`, `flat_game.png`, `flat_tq.png`), and a zoom of the chest bib from `low_below.png` (in `C:\Users\ventu\AppData\Local\Temp\lynx_rev\`, outside the project)

## Measurements (my own count on the flat renders, nearest-colour match, same method as review 1)

| view | ICE, mine | ICE, builder | ICE_CLAW | other notes |
|---|---|---|---|---|
| side | 2.3 % | 2.6 % | 0.6 % | WARM 48.6, BACK 26.8, SNOW 13.0, BLACK 3.7 |
| game | 2.0 % | 2.2 % | 0.3 % | WARM 46.8, BACK 32.3, SNOW 9.9 |
| tq | 4.0 % | 4.5 % | 1.5 % | |

My count and the builder's differ by about 0.3 points, which is anti-alias classification. Both are at or just above the gate (side 2.5, game 2.0). Rosettes are 20.8 % of the side view, as the builder reports. Accepted.

Badger's amber is 2.8-4.9 % side and 8.5-12 % game. The Lynx is now about a quarter of that, not a tenth. It is a starter accent, and it reads at 64 px.

---------------------------------------------------------------------------------------------------------------------
## 1. Review-1 items, one by one

| # | review-1 item | result |
|---|---|---|
| M1 | Saddle floats 0.03 above the rump and rib | **PASS.** `crop_rump_side.png` shows the hips and rib saddle flush on the body. No green gap. |
| M2 | Tail reads as a cat/leopard tail | **PASS.** 0.19 bobtail with a black tip. The side view reads as a short stub. |
| M3 | ICE accent at least 2.5 % side / 2 % game | **PASS (at gate).** Claws ICE, outer 45 % of each ruff spike ICE, ICE_CLAW fangs at 0.066, iris 0.034. At 128 px the frost reads as frost, not horns. |
| M4 | Cat pupil not visible from the front | **PASS.** `crop_eyes_front.png` shows a black vertical bar in each cyan slit. See NICE 1 on its position. |
| M5 | Ears read as horns at 128 px | **PASS.** Bases wider (0.088), pencils shortened to 0.045 / 0.040. The 128 px strip reads as lynx ears with frosted tufts. |
| NICE 1 | Front sock too long (white stockings) | **PASS.** The front lower legs are beige, with white only on the paws. |
| NICE 2 | Shin spots (leopard count) | **PASS.** Fewer spots on the lower legs. |
| NICE 3 | Belly line rising to the hind legs | **PARTIAL.** The rise is subtle. See NICE 4. |
| NICE 4 | Shorter ruff | **PASS.** The mid and top spikes are shorter. The fan reads as fur, not fins. |

Every review-1 MUST is resolved. Every NICE item is at least partly resolved.

---------------------------------------------------------------------------------------------------------------------
## 2. MUST list (one item)

### M1 - The throat / chest bib is a flat studded slab (`pets/FrostfangLynx.py` line 130-131)
The SNOW block `B.add((0, -0.418, 0.600), (0.086, 0.028, 0.135), SNOW, "Chest", bot=(0.30, 0.8), top=(1.0, 1), rot=(-14, 0, 0), rnd=0.35)` hangs from the chin to the chest as one flat rectangle with a hard edge. From below (`low_below.png`) it reads as a white plastic plate with studs, about 0.27 units tall. From the front (`model_sheet`, front panel) it is a light-blue rectangle on the chest. That is the "plastic toy slab" and "box" read the owner has rejected, and it is the one new goat cue (a bib hanging from the chin).

- **Fix:** round it into a throat, not a plate. Keep the width but drop the depth and the height so it is a tapered throat:
  - `rnd` 0.35 -> 0.55, `bot=(0.30, 0.8)` -> `bot=(0.5, 0.7)`;
  - half-depth 0.028 -> 0.020;
  - half-height 0.135 -> 0.110;
  - or, if simpler, delete the block and keep the two chest spikes on line 132-133 plus the SNOW underside strip (line 129). That already gives a white throat.
- **Pass:** from `low_below.png` and the front panel, the throat reads as soft fur, not a flat plate. The stud pattern shows as fur, not a grid.
- **Check:** one front render and one low render, nothing else.

---------------------------------------------------------------------------------------------------------------------
## 3. NICE list (optional, not gates)
1. **Pupil position.** In `crop_eyes_front.png` the black bar sits toward the nose side of each slit (about the inner half). The pupil is set at x +/-0.049 and the iris centre is +/-0.051, so it should be centred. Check on the iris centre. A centred pupil is the cleaner fierce read. If the bar is the socket's inner edge, leave it.
2. **ICE margin.** The accent is at the gate, not above it. If the owner wants more margin, the top edge of each ear front (SNOW, line 181-182) can take ICE, about +0.2 %. Optional.
3. **Saddle seams.** In `game_view.png` the three saddle inlays read as separate dark tiles with a body-coloured seam between them. The flush fix works. If it still reads like tiles, merge them into one band over chest, waist and hips (one tube). Optional.
4. **Belly rise.** The underline from the chest to the hind legs is nearly straight, with a subtle tuck. The +0.015 rise is in the builder's notes. It is fine, but a further +0.01 at the waist would make it a clearer tuck.
5. **Top ruff blade.** From the front the outermost cyan blades form a fan that is bold but not busy. Keep it, or trim the top blade's ICE tip if the close-up looks like wings later.

---------------------------------------------------------------------------------------------------------------------
## 4. Pass/fail checklist (model gate, round 2)

| # | item | result |
|---|---|---|
| 1 | 64 px: species reads at once (cat, frosted tufts, spots) | **PASS.** Reads as a lynx, with cyan frost on the tips and ruff |
| 2 | 128 px: no goat or horn read from ears or beard | **PASS.** Ears are wider and the tufts short. The bib is the one remaining goat cue (M1) |
| 3 | Game camera: body reads sand-silver, rosettes and SNOW underside visible | **PASS.** WARM 47 %, BACK 34 %, SNOW 10 % |
| 4 | Face: fierce slit eyes under heavy brows, no googly, no glint, no smile | **PASS.** Pupil visible (NICE 1 for centring) |
| 5 | Head: lynx wedge, not dog or goat | **PASS** |
| 6 | Accent: ICE at least 2.5 % side / 2 % game | **PASS (at gate).** 2.3-2.6 side, 2.0-2.2 game |
| 7 | Palette follows the plan | **PASS** |
| 8 | Rosettes at least 20 % of the side view | **PASS.** 20.8 % (builder) |
| 9 | Floating, poking or intersecting parts | **PASS** for saddles and tail. **FAIL** for the bib, which is a flat slab, not a floating part (M1) |
| 10 | Parts visible from below | **FAIL.** The bib reads as a plate from below (M1). Paws and claws pass |
| 11 | Tri count at most 15k | **PASS.** 6,400 |
| 12 | Distinct from Shade Panther | **PASS.** Panther is violet with crystals and a bulky head. Lynx is sand-silver with cyan frost |
| 13 | Details smooth (eyes, claws, fangs, tufts) | **PASS.** The ICE claws and fangs are smooth |
| 14 | Tail reads as a lynx bobtail | **PASS.** Short stub with black tip |
| 15 | Fierce, not cute | **PASS.** Socks reduced, brows and slits fierce, frost reads as hunting, not toy |

Score tally: 13 PASS, item 9 mixed (saddle and tail pass, the bib fails), item 10 FAIL. Both fails come from M1, which is the single MUST. The NICE items are not counted.

## 5. Re-send checklist
- `pets/FrostfangLynx.py` diff for lines 130-131 (and 129 if the strip is changed)
- `FrostfangLynx/renders/crop_front_throat.png` (a front crop at the chest, near the bib) and `low_below.png` after the change
- `_model_sheet.png` and `_icons_strip_64.png` only if the silhouette or the head changes
- No clip-gate material is needed for this round.

Verdict: **APPROVED WITH FIXES, 8/10.** One MUST (the chest bib), then ship.
