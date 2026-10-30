# Blizzard Roc - model gate review 3 (2026-10-27) - APPROVED (model gate passed)

**Score: 8.5/10 for a 7.4 % HIGH flyer** (ship target 8). All five round-2 MUSTs have landed as specified. No model MUST
is left. Two items carry to the clip gate (section 3), and there is one NICE. This is a verdict on the model only; the
clips are judged separately.

What I checked, as evidence against each MUST:
- `pets/BlizzardRoc.py` (eye at L155-167; span at L47; `model()` return at L378; ground planting at L462, L506-515, L611)
- `BlizzardRoc/MODEL_NOTES.md` (REVIEW 2 FIXES section)
- `renders/head_front.png` (700 px, full size), `renders/_eye_sheet.png` (eye front and tq close), `renders/_model_sheet.png`
- `renders/_icons_strip_64.png` and `_128.png`
- `renders/model_tq.png`, `model_front.png`, `model_under.png`, `model_side.png`, `model_game.png`, `model_back.png` (all 600 px)
- `flat_side.png`, `flat_tq.png`, `flat_game.png` (my own pixel count, section 2)
- not judged here: the `_pose_*` sheets (clips, clip gate)

---------------------------------------------------------------------------------------------------------------------
## 1. M1-M5 evidence

| # | round-2 MUST | evidence | result |
|---|---|---|---|
| M1 | Eye reads as a slit under a lid, not a lens | Code L160 is `(0.046*sc, 0.008, 0.011*sc)` at `z +0.004*sc`; slit L162 kept at `0.045*sc x 0.0085*sc`; hot spot L164 is `0.014*sc x 0.003*sc`. In `head_front.png` the black frame under the violet is gone: each eye is a violet slit with a black lid above it, and the head no longer reads as goggles. | **LANDED** (NICE 1 for the glint) |
| M2 | One strip, no duplicate angle, the full comparison set | `_icons_strip_64.png` and `_128.png`: Roc, Frostfang Lynx, Ice Mammoth, Glacier Yeti, Thunderbird, Griffin, Inferno Phoenix, Frostcrown Dragon. Eight icons, one Roc, no duplicate. | **LANDED** |
| M3 | `model_tq.png` at 600 px | `model_tq.png` is 600 x 600 (the same for every model view, and `_model_sheet.png` is 1800 x 1200). | **LANDED** |
| M4 | Span printed and recorded | MODEL_NOTES quotes `model()` output: `"span": 3.999`, `"H": 1.996`, so 3.999 / 1.996 = **2.00 H** in the bind pose. The code at L378 returns `span` as `2*max(|mn.x|, mx.x)`, which matches. | **LANDED** (recorded) |
| M5 | Ground minimums at or above -0.02 in the clips | MODEL_NOTES reports step-1 `ground_min_z`: idle -0.017, walk -0.018, takeoff / land / roar / act_bow -0.017, `collision_free` true. The code plants feet at FOOT_LIFT 0.014 (L31, L512, L611). | **REPORTED, carry to clip gate** (section 3) |

M4 is the one I could not check from the pictures, because perspective renders cannot confirm 2.00 H. The printed value
is consistent with the code, and I accept it.

---------------------------------------------------------------------------------------------------------------------
## 2. Shares and look (my pixel count, round 3 flat IDs)

| flat ID | colour | builder (notes) | mine | target | result |
|---|---|---|---|---|---|
| side | SNOW | 18.9 | 19.3 | - | |
| side | STORM_GREY | 38.4 | 39.3 | (plan 25) | see N2 |
| side | CHAR | 25.8 | 26.3 | <= 28 | PASS |
| side | FROST_V | 8.5 | 8.7 | <= 12 | PASS |
| game | SNOW | 16.1 | 16.4 | >= 15 | PASS |
| game | CHAR | 19.2 | 19.6 | <= 22 | PASS |
| game | FROST_V | 9.5 | 9.7 | <= 12 | PASS |

My counts agree with the builder's to within about 1 point. Nothing regressed in the rest of the model sheet: the wings,
the breast chevron, the white nape collar and the crest all read as in review 2.

---------------------------------------------------------------------------------------------------------------------
## 3. Carry-over to the clip gate (not model MUSTs)

- **Ground margin (M5):** -0.017 to -0.018 is inside the -0.02 limit, but the walk margin is only 0.002. The clip gate
  must re-measure `ground_min_z` for every clip from the headless output, not from this summary. A walk at -0.021 would fail.
- **R3 white rump (review 2 deviation):** check from behind in the walk and takeoff frames that the white tail base does
  not read as a white fan. If it does, revert L358-361 (the Tail1 seg and its three coverts).

---------------------------------------------------------------------------------------------------------------------
## 4. NICE

1. **The white FROST_H bar in each eye** (L164-165) is now the brightest mark on the face at close range, and it reads a
   little like a window glint. The FIERCE guide asks for a hot centre, so keep it. If the owner calls it a glint, shrink
   it to `0.010*sc x 0.002*sc`, or move it to the inner corner.
2. **The outer end of the eye socket** still shows a small dark corner in `head_front.png`. This is cosmetic. Leave it.

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail

| # | check | result |
|---|---|---|
| 1 | Tris <= 15k | PASS (12,964) |
| 2 | Height 9.0 to the crest | PASS (H 1.996 BU) |
| 3 | Span 2.0-2.4 H | PASS (2.00 H, recorded) |
| 4 | 64 px species read | PASS (`_icons_strip_64.png`) |
| 5 | Game camera: white and presence | PASS |
| 6 | Face reads (narrow slit, no glasses) | PASS (M1; NICE 1 for the glint) |
| 7 | CHAR within target | PASS (side 26.3, game 19.6) |
| 8 | SNOW game >= 15 | PASS (16.4) |
| 9 | FROST_V <= 12 | PASS |
| 10 | Not a recolour of Thunderbird | PASS |
| 11 | Fierce, not cute | PASS |
| 12 | Brightest body channel >= 170 | PASS |
| 13 | Stud skin, no box belly, no glow | PASS |
| 14 | Floating or poking parts (bind, fold) | PASS |
| 15 | Parts visible from below | PASS (`model_under.png`) |
| 16 | Deviations R1-R4 | PASS (accepted in review 2; R3 carried to the clip gate) |
| 17 | Deliverables (strip, 600 px tq, span line) | PASS (M2, M3, M4) |
| 18 | Ground minimums (M5) | REPORTED (carried to the clip gate) |

Verdict: **APPROVED.** The model gate is passed. The clips are next, judged at the clip gate with the two carry-over
items in section 3. No model MUST is open.
