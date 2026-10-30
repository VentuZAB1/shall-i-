# Glacier Yeti - FINAL 8.5 GATE, ROUND 4 (2026-10-28, fresh reviewer) - PASS

**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

Summary: both round-3 faults now pass on the pixels. The fangs peak at lum 154-155 and the fist plates at 165-185. Nothing new blocks 8.5. The model sits on the floor, not above it. The shoulder caps clip to pure white (new finding below), and the profile cap and the 64 px accent are still open 9+ items. Any new problem in the Studio check would drop it under 8.5. The clips are carried from round 3 because their numbers are identical.

## What I looked at

- **Method:** PIL 12.3 and numpy 2.5 were available, so every value below is measured. Luma is Rec.601 (0.299 R + 0.587 G + 0.114 B). The ground is green-tinted, so fist and fang checks use a blue/neutral mask, and I report raw numbers as well. Scratch scripts sit in a temp folder outside the project. No Blender, no Studio, no edits.
- **Newest set** (pet file 05:19, renders 05:21-05:25, export 05:22, `verify.json` 05:23):
  - close-ups `pclose_front_idle_00`, `pclose_side_idle_00`, `pclose_side_roar_30`, `pclose_front_roar_30` (05:21), `_close_sheet` (05:24), `_final_mouth` (05:25);
  - model views `_model_sheet`, `model_front`, `model_tq`, `model_side`, `model_back`, `model_game`, `under` (05:21-05:24), and `flat_game` / `flat_side` / `flat_tq` (05:24);
  - icon strips `_icons_strip_64` / `_icons_strip_128` (05:24), `_crust_sheet` (05:25);
  - walk and skid frames `beat_f85r3_ws_tq_walk_000`, `beat_f85r3_ws_tq_act_skid_007` (05:21), the `beat_f85r3_ws_side_*` frames and the `_beats_f85r3_ws_tq` / `_side` sheets (05:22-05:25).
  - `_scratch/verify.json` and `_scratch/export_result_f85r3.txt`.
- All images opened. None failed to load.
- Read: the brief, round 3, `MODEL_NOTES.md` (final gate round 3), `GlacierYeti_plan.md`, the owner decisions in `GLACIER_CONCEPTS.md`, `FIERCE_GUIDE.md`, and the Obsidian Creature Style and Model Review Checklist notes.

## Round-3 items

| Item | Result | Evidence |
|---|---|---|
| **MN1 fangs: no white teeth** | **PASS** (on the fang pixels) | `pclose_front_idle_00`: the bone/grey-hued fang pixels peak at lum **154** (left, x 118-126, y 196-209, at (118,208)) and **155** (right, x 293-302, y 197-209, at (298,197)). None reach 170. The brief's literal left box (x 118-130, y 200-218) has a raw max of 185 and 15 px at 170 or more. All 15 are saturated blue fur (about (160,179,255)) at the fang's edge, none bone-hued, so that is fur, not fang. The brief's right box (x 280-292) misses the right fang entirely. `pclose_side_idle_00`, box x 160-192 / y 200-226: raw max **169**, 0 px at 170 or more; the profile fang's own peak is 119. Zoomed crops show flat grey-tan points with no highlight. The profile fang sits on the lip edge and does not poke past it. |
| **MN2 fist plates: no white strips** | **PASS** (on the fist plates) | The brief's literal boxes (model_front x 112-150 / 362-400, y 384-400) sit on the blue forearm and the ground corner. Raw max is 222 (left, ground pixel (196,238,205)) and 243 (right, (226,255,225)). On blue/neutral pixels only, the max is 200 (left) and 199 (right), both forearm edges against the ground. The fist plates are at model_front x 116-178 and x 422-484, y 428-466. Their max is **173** (left) and **185** (right), with interior max 165 and 185, and zero px at 200 or more. `model_tq`: the near-left plate interior (x 118-162, y 388-426) peaks at 185; the 219 pixel at (120,407) is the plate's antialiased edge against the ground. The near-right fist (x 340-420, y 470-530) peaks at 168. `beat_f85r3_ws_tq_walk_000` and `beat_f85r3_ws_tq_act_skid_007`: the fist plates peak at 163-185 on blue pixels, zero px at 200 or more. Crops show grey-blue plates, not white strips. |
| M2 roar mouth is a dark cavity | PASS | `pclose_front_roar_30` and `pclose_side_roar_30` show a dark maroon cavity. The closed idle hides it. |
| M4 crust reads as broken ice | PASS | `_crust_sheet`: pale cap, green seam, mid-ice lip, navy below. |
| M5 limbs not stacked boxes | PASS | `model_front` / `model_tq`: studded lofts with bellies, no box slabs. |
| M6 verification set | PASS | Every listed view is present and loads. The Studio 5-stud capture stays with the lead. |
| P1 crust split (front and back) | PASS | `crust_cfront` and `crust_cback`: two plates with a visible gap, the outer one raised and tilted. |
| P1b crust in profile | OPEN (9+) | `model_side` and the walk and skid side frames still show the cap as one flat card. |
| P2 accent at 64 px | PARTIAL (9+) | The first 64 px icon has **44** green-ish pixels (round 3 counted 38). The target is 100 or more. |
| P3 idle head drop | PASS (numbers) | `verify.json`: head local 6.35 at f76, neck 3.27 at f75. The motion check at 5 studs stays with the lead. |
| P4 look-turn doubling | Lead ruling | Not scored. |

## Other judging (player's eye)

- **64 px and 128 px:** the hunch, the pale shoulder crusts and the dark head read at both sizes. The species reads as a hunched beast, and it is clearly distinct from Ice Mammoth (cyan), LavaGolem (grey and gold), Treant (wood) and Raiju (dark, electric).
- **Face:** fierce. Heavy brow V, narrow slits with black sockets, dark flat nose, bone fangs, roar cavity. No glints, no smile.
- **Palette:** the body is POLAR_NAVY (96,106,186) with NAVY_D shading. The flat shares are as the notes state (game: POLAR_NAVY 38 %, PLATE_ICE 29 %). The body reads indigo-periwinkle in the preview. It is about 16 units off the approved Raiju calibration (80,102,182), so it is accepted under the x0.6 game rule.
- **Build:** studs are consistent; no floating, poking or underside parts seen in `under`, `model_back` or `model_game`.

## New finding (not a blocker): the shoulder caps clip to white

- Left cap top (model_front x 120-165, y 125-150): **91 %** of pixels have all three channels at 250 or more, mean (252,253,254). Right cap top (x 435-480): **76 %**, mean (249,253,254).
- The caps are the largest near-white area on the pet, and the tops show almost no form in the front and tq views.
- **Why this is not a MUST:** the brief judges in game colours (Roblox darkens about 0.6x, so the caps land near light grey-blue in game). The caps are the intended pale read, which passed at 128 px. Round 3 accepted the same crust geometry. It is the first 9+ item, not a blocker.
- Fix direction (9+): lower the cap top-face colour by about 10-15 % (PLATE_ICE (206,226,240) to about (180,200,214), top faces only), keeping the seam and the lip. Target: lit cap-top median 235 or less, and under 10 % of cap-top pixels with all channels at 250 or more. Check the 128 px pale read still holds.

## Clips (carried from round 3, 8.5 PASS)

- `verify.json` (05:23) and `export_result_f85r3.txt` (05:22): roar neck max **7.69** (limit 8), roar head joint **18.79**, head + neck pitch-up **24.08** (limit 30), chest vs spine max **4.61** (limit 5). Ground min z **0.002** in all four clips. `collisions` is empty and `collision_free` is true. Linear is 0, one-shots end at rest (0.056 and 0.234 deg), and tris_body is **7,728**.
- The walk f0 and skid f7 frames show no white fists, so the plate move did not disturb the clips.
- Not re-reviewed this round: the idle and roar pose sheets (not re-rendered). The Studio 5-stud capture and the live cross-fade stay with the lead.

## MUSTs (blocking 8.5)

None on the model. Both round-3 MUSTs pass on the pixels.

**Coordinate fix for the next gate (documentation, not a model fault):** the brief's boxes miss their targets. Use these instead:
- fangs: left x 118-126, y 196-209; right x 293-302, y 197-209 (`pclose_front_idle_00`);
- fist plates: `model_front` left x 116-178, right x 422-484, both y 428-466, measured on blue/neutral pixels so the ground is excluded.

## TO 9+ (polish, not blocking)

1. **Cap-top clip** (see above): lower the cap top faces about 10-15 % so the lit top keeps shading below 250.
2. **P1b profile cap:** chamfer the outer top edge about 0.02 units, or split the top into a stepped third plate, so the profile breaks up like broken ice.
3. **P2 accent at 64 px:** the first icon has 44 green-ish pixels (target 100 or more). Widen the crust front seam from 0.070 toward about 0.09, or give the rear hump blade an AURORA tip.
4. **Optional, preview only:** POLAR_NAVY (96,106,186) to about (88,98,176) would read a little more navy in the Blender preview. The x0.6 game rule already covers the in-game read, so this is taste, not a gate item.

## Checklist

| Check | Result |
|---|---|
| 64 px: hunched beast reads | PASS |
| 128 px: pale shoulders, dark head, accent rim | PASS |
| Face fierce (brow, slits, no glint, no smile) | PASS |
| Fangs: no white teeth in profile or front | PASS (fang pixels 154-155; profile 169 raw, 119 on fang) |
| Roar mouth is a dark cavity | PASS |
| Fists: no white strip | PASS (plates 173 / 185; literal box misplaced, see above) |
| Crust: second tone, broken ice front and back | PASS |
| Crust caps not clipped white | NOTE (91 % / 76 % clipped; 9+) |
| Limbs: not stacked boxes | PASS |
| Body colour: brightest channel 170 or more | PASS (186) |
| Floating, poking, or visible from below | PASS |
| Accent at 64 px | PARTIAL (44 px; 9+) |
| Clips: limits, ground, loops, rest, diagonal walk | PASS (numbers unchanged; clips carried) |
| Idle to walk cross-fade and 5-stud game camera | Lead, Studio (not scored) |

**Model 8.5 (PASS).** Both named faults pass on the pixels. The silhouette holds at 64 and 128 px, and the face is fierce. The score sits exactly on the floor. The clipped caps, the flat profile cap and the thin 64 px accent keep it from 9.

**Clips 8.5 (PASS).** Carried from round 3. The numbers are identical, and the walk and skid frames show nothing new.
