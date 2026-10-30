# Blizzard Roc - model gate review 2 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 8/10 for a 7.4 % HIGH flyer** (the ship target). Review 1 was 7/10. The round-1 MUSTs and NICEs landed, and
the value targets are met. One visible face fault is left (the eyes still read as glasses from the front), plus three
deliverable gaps. All of them are small. Apply M1 and the deliverables, then send the head close and the strip. No new
full model gate is needed. Clips can start once M1 is in.

What I looked at (`pets/BlizzardRoc.py` round 2, `BlizzardRoc/MODEL_NOTES.md` ROUND 2):
- `renders/_model_sheet.png` (bind, 600 px, 5 views), `model_under.png` (under view, ground hidden)
- `renders/_close_sheet.png`, `head_front.png` (full size), `crest_back.png`, `head_game.png`
- `renders/_idle_sheet.png` (ground fold), `idle_game.png` (game camera)
- `renders/_icons2_strip_64.png` and `_128.png`
- `flat_side.png`, `flat_tq.png`, `flat_game.png` (my own pixel count, section 1)
- the code at L47, L94, L131-134, L155-167, L251, L282-284, L291-300, L357-369, L447

---------------------------------------------------------------------------------------------------------------------
## 1. Numbers (my count against the builder's)

| flat ID | colour | builder side / tq / game | mine side / tq / game | round-2 target | result |
|---|---|---|---|---|---|
| | SNOW | 19.0 / 32.7 / **15.9** | 19.4 / 33.7 / **16.2** | game >= 15 | PASS |
| | STORM_GREY | 38.3 / 27.5 / 47.4 | 39.1 / 28.3 / 48.3 | (plan 25) | see N1 |
| | CHAR | **25.7** / 19.7 / **19.2** | **26.3** / 20.3 / **19.5** | side <= 28, game <= 22 | PASS |
| | PALE_G | 1.9 / 4.5 / 2.0 | 2.0 / 4.7 / 2.1 | (plan 6) | see N3 |
| | FROST_V | 8.5 / 6.3 / 9.5 | 8.7 / 6.5 / 9.7 | <= 12 | PASS |

My figures are within about 1 point of the builder's on every value. The builder's shares are reliable.

Span and fold, as the builder reports them: span 3.999 BU = 2.00 H, FOLD (86, 10, -80, 10), 45 / 81 collision-free.
I cannot confirm 2.00 H from the perspective renders, so I accept it on the printed number (M4). ground_min_z -0.031
in the bind pose is the talon hooks (M5).

Size: 12,964 tris (cap 15k): PASS.

---------------------------------------------------------------------------------------------------------------------
## 2. Deviations R1-R4

**R1 - grey primary roots, outer 60 % dark (L94 PBARS, `[(CHAR,.11),(FROST_V,.17),(CHAR,.32)]`): ACCEPT.**
The wings now have depth. The root is grey, the band is charcoal, the violet bar and the charcoal point stay at the tips.
The flank no longer reads as one charcoal slab in the side view. The side-view grey rises to 39 % (see N1).

**R2 - white nape collar down the back of the neck (L282-284, SNOW rows at t 0.85 and 0.50): ACCEPT.**
From the game camera (`head_game.png`, `idle_game.png`) it reads as a white head and neck over the grey mantle, and it
joins the white crest. This is the "snowy" read that review 1 said was lost from behind. It is not a fan, so it does
not bring back the Thunderbird.

**R3 - white rump, upper tail coverts and tail base (L251, L358-361): ACCEPT, with a check.**
It is small. The four tail feathers stay grey with a violet bar and a charcoal tip (L369), and there is no white fan.
The rump is mostly hidden by the fold, so it adds little from the game camera. If the clip gate reads any white fan
from behind, revert L358-361 first (the tail-base seg and the three coverts).

**R4 - inner 3 of 7 coverts SNOW, secondary charcoal edge 0.30 to 0.18 (L131-134, L128): ACCEPT.**
The snowy shoulder is visible in the front view and in the fold. The dark outer wing stays, and the secondaries keep a
charcoal edge.

---------------------------------------------------------------------------------------------------------------------
## 3. The face: the glasses read is real (M1, the one model MUST)

The builder's note is right. At full size (`head_front.png`) each eye is a black socket with a violet window in it,
plus a dark brow above. It reads as goggles.

The cause is in `eye()`:
- The black socket (L160-161) is `(0.050*sc, 0.008, 0.017*sc)`, so it is about 0.042 BU tall. The violet slit (L162-163)
  is `0.0085*sc`, so it is about 0.021 BU tall. The black frame is about twice the height of the slit. It shows above and
  at the outer end, so the slit sits in a frame.
- The pale FROST_H hot spot (L164-165) is `0.0045*sc` tall, a pale window in the middle of the slit. That is what makes the
  lens read as a window.

**M1 (MUST): make the eye a slit, not a lens.** In `eye()`:
1. The socket L160-161 becomes `(0.046*sc, 0.008, 0.011*sc)`, centred at `z +0.004*sc` (was 0.0). It is now a black lid
   over the slit, not a frame. The socket's outer end is trimmed by 0.004 BU.
2. The slit L162-163 stays at `0.045*sc x 0.0085*sc`.
3. The FROST_H hot spot L164-165 shrinks to `0.014*sc x 0.003*sc`.
4. The brow (L299-300) stays. Its top lid is now the only black above the eye.

Test: `head_front.png` should show a violet slit under a black lid, with no dark frame on the outer side. The FIERCE
rule (black socket, bright slit, small hot centre) is kept. The hot centre just gets smaller.

---------------------------------------------------------------------------------------------------------------------
## 4. MUST and NICE

**MUST**
- **M1 - eye as a slit, not a lens** (section 3). Send `head_front.png` after the change.
- **M2 - deliverable: the strip is incomplete.** `_icons2_strip_64/128.png` holds only four icons: two Roc angles,
  Thunderbird and Griffin. The second Roc icon duplicates the first in pose and costs a slot. The comparison set the
  lead asked for is missing. Send one strip at 64 px and at 128 px, with the pet first, then Lynx, Ice Mammoth, Glacier
  Yeti, Thunderbird, Griffin, Inferno Phoenix and Frostcrown Dragon. Drop the duplicate angle. Review 1 asked for the
  same set, and this was not done.
- **M3 - deliverable: `renders/model_tq.png` is 200 x 200 px** (the same fault that VenomBasilisk had). The headless
  close-up overwrites it. Re-render at 600 px and check the file size.
- **M4 - record the span (not a model change).** Span 2.00 H is the builder's number. A perspective front render cannot
  confirm it (I get about 1.8 to 1.9 H, which is inconclusive). Paste the printed `span` value from `model()` (L378) and
  the step-1 log into MODEL_NOTES. An orthographic front render would settle it if the clip gate doubts it.
- **M5 - ground pose, before the clip gate (not a model blocker).** ground_min_z is -0.031 in the bind pose, from the
  talon hooks. The bind pose is not used in game, so I accept the deferral. The root lift must land in the rig or the
  clip set, and the fold idle must report ground_min_z >= -0.02 before the clip gate passes. The clips' ground_min_z
  numbers are the test.

**NICE**
- **N1 - side-view grey 39 % (plan 25).** R1 moved the grey up. If it bothers the clip gate, the root can shorten from
  0.40 to 0.34 of the length: `PBARS` L94, CHAR band `.32` to `.38`. Otherwise keep it.
- **N2 - keep the FROST_V covert bar on the inner SNOW covert (L134)** as built. It is the only violet on the white
  shoulder, and it stays.
- **N3 - PALE_G 2 % in the side view.** The fold covers the belly, so the under view shows the white belly (`model_under.png`).
  That is fine. Check the pale underside in the clip render, not here.
- **N4 - the breast chevron (L261-262, violet middle bar) reads well** in the front view. Keep it.

---------------------------------------------------------------------------------------------------------------------
## 5. Presence (the lead's question from review 1)

- **Silhouette:** the span now reads at the icon angle (the 2.00 H wing and the three violet crest points). The crest
  reads from behind (`crest_back.png`) and from the side.
- **Colour:** the Roc is still the palest pet in its egg. Yeti (navy) and Mammoth (teal) are saturated and bulky.
  The Roc does not need to win on colour. It wins on span, crest and the charcoal wing tips.
- **Game camera:** the white head and nape now show from behind. The grey mantle is the largest zone, as in review 1,
  but it has shingle studs, and it no longer reads as a plain slab.
- **Floor caution (from review 1, still open):** the Glacier floor is probably ice or snow-pale. Check the Roc on the
  Studio Glacier floor at the clip gate.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail

| # | check | result |
|---|---|---|
| 1 | Tris <= 15k | PASS (12,964) |
| 2 | Height 9.0 to the crest | PASS |
| 3 | Span 2.0-2.4 H | PASS on the builder's number (M4 records it) |
| 4 | 64 px species read | PASS |
| 5 | Game camera: white and presence | PASS (R2 nape collar, crest) |
| 6 | Face reads (narrow slit, no glasses) | **FAIL** (M1) |
| 7 | CHAR within round-2 target | PASS (side 26.3, game 19.5) |
| 8 | SNOW game >= 15 | PASS (16.2) |
| 9 | FROST_V <= 12 | PASS (8.7 side, 9.7 game) |
| 10 | PALE_G underside (plan 6) | PARTIAL (2.0 side, fold covers it; check in clips) |
| 11 | Not a recolour of Thunderbird | PASS (no fan, no gold, no teal) |
| 12 | Fierce, not cute | PASS |
| 13 | Brightest body channel >= 170 | PASS |
| 14 | Stud skin, no box belly, no glow | PASS |
| 15 | Floating or poking parts, bind and fold | PASS (talon sink is M5, deferred) |
| 16 | Parts visible from below | PASS (`model_under.png`) |
| 17 | Tail reads as a fan of four, not rods | PASS (wider feathers, violet bars) |
| 18 | Deviations R1-R4 judged | PASS (all four accepted; R3 to check) |
| 19 | Deliverables complete | **FAIL** (M2 strip, M3 200 px tq) |

Score 8/10. Apply M1, send the head close and the strip (M2, M3), and record the span (M4). Then the clips can start,
with M5 as the ground gate.
