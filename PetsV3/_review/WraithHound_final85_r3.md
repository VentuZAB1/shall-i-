# Wraith Hound - FINAL 8.5 GATE, round 3 (model, export 01:42) - 2026-10-28

**Model 8.5/10. PASS (at the bar, thin margin). Clips 8.5/10 (passed in round 2, unchanged; the stagger was re-checked in the new metrics). Overall PASS.**

Round 2 scored the model 8.0. Every round-2 MUST and TO 9+ item is applied, and the code matches the claims. The player's view now shows the design: the lavender ghost body, one long indigo leader on the middle row, a rounder saddle, a rounded throat, and sockets that frame the eye. What still keeps the margin thin is at icon size only: the blue accent and the eye slits are faint at 64 and 128 px. Nothing on this list is a MUST. The TO 9+ items below are the next steps.

## What I looked at
- Notes and data: `WraithHound/MODEL_NOTES.md` (round 6), `_scratch/gate6.log`, `_scratch/fullcheck.json` (01:41), `_scratch/clipmetrics.json` (01:41), `pets/WraithHound.py` (01:39).
- Renders (01:40-01:41): `_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `_close_sheet.png`, `crop_mane_side.png`, `_fan_front_back_r2.png`.
- Not re-rendered this round: `model_front.png` (older), `crop_mane_front.png` (01:40, used only for the throat check via the model sheet).
- No Blender, no Studio. I did not zoom the strips (no PIL in this shell), so the icon-size read is from the full strips at their native size.

## Round-2 items, checked
| item | result |
|---|---|
| M1 indigo tips fatter (tip-width factor 0.85) | **done** (L77 `tw = 0.85 if tipcol == INDIGO`). The blue leader is clear in `game_view.png` and `crop_mane_side.png`. At 64 and 128 px it is faint (see below). Game INDIGO 5.3 %. |
| M2 socket 0.028 tall | **done** (L167). In `_close_sheet.png` the black socket frames the blue slit under the brow. |
| TO 9+ saddle rounder (rnd_t 0.45) | **done** (L134-136). The saddle top reads as fur in `game_view.png`, not as a flat board. |
| TO 9+ Mane1 / Mane3 side tips SOOT, one line on Mane2 | **done** (L86, L92). The only blue on the crest is the Mane2 centre leader and its side tips. |
| TO 9+ throat rounded (rnd 0.45) | **done** (L145-146). The throat reads as a rounded pale patch, not a bib. |
| Cloak stagger 6 / 4 / 2 deg | **done** (L437). `_fan_front_back_r2.png` bottom-middle: the fan reads as a swept crest from behind, not a ring. `act_smokecloak` metrics unchanged: neck 5.0, chest 1.5, pitch 3.5. |
| Gates | **pass.** fullcheck: collision_free true, collisions {}, ground min 0.004 in every clip, tris 6,820. |

## Measured
**Shares (`_scratch/gate6.log`):**

| view | ASH_LAV | MIST | SOOT | WISP_ROOT | INDIGO |
|---|---|---|---|---|---|
| side | 47.2 | 6.8 | 24.1 | 13.7 | 3.1 |
| game | **41.1** | 5.1 | 28.4 | 15.5 | **5.3** |

The dark family (SOOT + WISP_ROOT) is 43.9 % in game. The lavender body is still the largest single colour, which is the ghost read. The player-camera view has no more than 5.3 % indigo, but the leader is large and reads.

**Clip limits (01:41 metrics):** neck max 3.5 / 3.98 / 4.0 / 5.0 (idle / walk / roar / act; limit 8). Chest vs spine 0.6 / 2.92 / 1.5 / 1.5 (limit 5). Head + neck pitch-up 8.0 / 0 / 0 / 3.5 (limit 30). Last frame = first frame in the non-looping clips. **All pass.**

---------------------------------------------------------------------------------------------------------------------
## MODEL: 8.5/10 (PASS)

**What works now:**
- **Ghost read:** the body is a pale lilac hound with a dark topline. In `game_view.png` the lavender flanks and tail dominate, and the dark part is the rounded saddle and the crest.
- **Plume:** one long indigo leader on the middle row (`crop_mane_side.png`), with soot tips on the front and back rows. The crest reads as one swept mane, not three stacked fins.
- **Face in close-up:** heavy soot brows, black sockets framing the blue slit, black nose, ivory fangs. No glint, no smile. Fierce.
- **Build:** 6,820 tris, studs on every surface, no glow, no collisions, no floating or poking parts.
- **Tier fit:** height 9.0 ties the Stallion. The silhouette is distinct from every Void-egg sibling.

**Why it is 8.5 and not higher (icon size only; none is a MUST):**
1. **The accent is faint at 64 and 128 px.** In `_icons_strip_64.png` and `_icons_strip_128.png` the blue points barely show. The leader reads in the game view and in the close-up, but not in the inventory icon.
2. **The eyes do not read at 64 px.** In the strips the face reads as a dark brow and a black nose. The blue slit disappears into the socket at that size.
3. **The palette is the palest of the Void-egg pets.** At icon size the Wraith is a white-lilac ghost with grey crest. It is distinctive and not cute, but it is less punchy than the Panther, Stallion and Dragon beside it.

---------------------------------------------------------------------------------------------------------------------
## CLIPS: 8.5/10 (PASS, unchanged from round 2)
The clip gate passed in round 2. The only change since is the cloak stagger (6 / 4 / 2 deg), and the act metrics confirm it did not move any limit. The fan now streams back rather than ringing, from both the side and the rear.

---------------------------------------------------------------------------------------------------------------------
## TO 9+ (higher is better; none blocks the ship)
1. **Icon-size eye (model).** In `pets/WraithHound.py` the indigo slit (L168, `(0.042, 0.006, 0.018)`) sits inside the socket (L167, `(0.052, 0.008, 0.028)`). Make the slit a brighter, hotter colour, `INDIGO_L` for the slit and a deeper `INDIGO` for the rim, or raise the slit height to 0.022. Check the 64 px strip for an eye that reads as a point of light under the brow.
2. **Icon-size accent (model).** The Mane2 leader is the only strong blue at icon size. Option A: fatten the Mane2 side tips further (the width factor 0.85 on the side wisps only), so the leader reads as three blue points at 64 px. Option B: accept the current read, since the game view shows it clearly. Pick one and check the strip.
3. **Palette test (optional).** Try ASH_LAV at 5 % lower value, `(158, 148, 198)` in place of `(170, 160, 206)` (L17), and compare the 64 px strip. The goal is to keep the body's dusky tone at icon size without losing the game-view ghost. Only ship it if the game view still reads lavender (ASH_LAV stays at 40 % or more).

---------------------------------------------------------------------------------------------------------------------
## Pass / fail checklist (round 3)

**Model**

| check | result |
|---|---|
| 64 px: species reads (canid, wedge head, ears, tail) | PASS |
| 64 px: ghost reads (pale body, dark crest) | PASS |
| 128 px: one plume, not stacked spines | PASS (one leader; the front and back rows are soot tips) |
| Fierce face in close-up | PASS |
| Face reads at 64 px | PARTIAL (TO 9+ #1) |
| Accent reads at 64 px | PARTIAL (TO 9+ #2) |
| Studs, smooth details, no glow | PASS |
| Tris <= 15k (6,820) | PASS |
| Dark body + pale underside + one accent (in game) | PASS (ASH_LAV 41.1 is the largest colour) |
| Accent distinct from Raiju and the Void violets | PASS |
| No box belly, no bib, no plastic slabs | PASS (the rounded throat reads as fur) |
| Floating or poking parts | PASS |
| Height ties the Stallion (9.0) | PASS |

**Clips**

| check | result |
|---|---|
| Neck, chest, head pitch, no shakes, no spins | PASS (all limits) |
| Acts in place, ending at rest | PASS |
| Ground, collision_free, linear 0, loops closed | PASS |
| Roar jaw wave, roar flare 12 deg | PASS |
| Cloak reads as a swept fan, not a ring | PASS (side and rear) |
| Anim-reference rule | PASS (accepted in review 4) |

---------------------------------------------------------------------------------------------------------------------
**Verdict:** PASS at 8.5. Nothing is left as a MUST. The TO 9+ items are the icon-size eye, the icon-size accent and an optional palette test. Round 4 is only needed if the builder changes the body palette or the eye geometry, since those are the only changes that could move the score.
