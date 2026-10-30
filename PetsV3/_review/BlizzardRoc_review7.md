# Blizzard Roc - model + clip gate review 7 (2026-10-28, fresh reviewer)

**Model: 8.6/10 - PASS. Clips: 8.7/10 - PASS.**

- MUST 1 (documentation) LANDED. ANIM_REFS, the code header and the stale comments now match the clips.
- C1 (post-launch recovery at the fly tempo) LANDED. The numbers check out.
- M1 (tail blade), M3 (darker back) and N1 (frame labels) LANDED. M4 (eye) PARTIAL. M2 and N2 are lead rulings, not counted.
- No regression found. The 05:16 code edit is comments only (verified by diff).
- Clip average passes at 8.7, but the walk alone is 8.2. See section 3.

---------------------------------------------------------------------------------------------------------------------
## What I looked at

**Read (text):** `GLACIER_REVIEWER_BRIEF.md`; `BlizzardRoc_review6.md`; `BlizzardRoc/MODEL_NOTES.md` (round 7); `BlizzardRoc/CLIP_NOTES.md` (review 6 section); `BlizzardRoc/ANIM_REFS.md`; `pets/BlizzardRoc.py` (L1-7 header, L356-372 tail, L440-470 references, L700-810 fly / takeoff / land). Snapshot diffs in `_scratch`: r6final -> r7start -> r7a -> r7b -> r7final. Step-1 outputs `full_step1.txt`, `seam.txt`, `steps.txt`, `rest_delta.txt`.

**Currency check:** last geometry edit = `r7b` (05:13). Step-1 outputs 05:13. Renders 05:14-05:15. The last file (`r7final`, 05:16) differs from `r7b` only in two comment lines (L6 header, L465-466 reference note). So the renders match the current geometry.

**Images (newest set, `renders\`):**
- Takeoff sheets, all three cameras, all 12 tiles each (f0 10 13 15 17 19 21 23 25 29 33 36).
- Walk: `_pose_game_walk_sheet`, `_pose_tq_walk_sheet`.
- Fly: `_pose_tq/game/front_fly_sheet`. These hold fly f0 only, so no stroke frames were rendered.
- Land and idle game sheets (tail regression check).
- `_model_sheet`, `model_side`, `model_game`, `_head2x_sheet` (front + game), `_icons_strip_64` / `_128`.
- A 4x crop of the side-view tail.

**My own measurements:**
- Wing `up` angle per frame, using the `wing3.stroke` formula from `wing3.py` and the takeoff keys.
- Nearest-palette pixel shares on `flat_game.png` (29,751 model px), `flat_side.png`, `flat_tq.png`.

**Not re-run:** the headless step 1. I took its numbers from the 05:13 `_scratch` outputs, which match the current geometry. `_close_sheet.png` is stale (27 Oct, pre-eye change) and was superseded by `_head2x_sheet.png`.

---------------------------------------------------------------------------------------------------------------------
## 1. MUST 1 (documentation): LANDED

- `ANIM_REFS.md`: walk "36 f = 1.2 s" with the reason; takeoff beats (downstroke f13-21, rise f14-22, feet planted to f17, leave at f18, flight cycle f25-36); R1 and R4 rows "not used by any clip"; header "clip round 3 + round 4". No stale "airborne f16-19" or "30 f walk" line is left.
- `pets/BlizzardRoc.py` L458-465: names H1 #260630 (takeoff, land, roar, act_bow, walk, idle) and the R5 Bird Flight tutorial (fly). #260711 and #260644 are marked supporting only.
- N3 (stale comments) LANDED: L6 header now says "FOUR tail feathers in a fan"; L356-357 comment updated.
- Only stale phrases left are in the review 4 and 5 history sections of `CLIP_NOTES.md`. Not a blocker.

## 2. Clip 9+ items

- **C1 post-launch recovery: LANDED.** Computed with `wing3.stroke`:
  - f21 -36 -> f25 -19.5 (+16.5 in 4 frames, about 4.1 per frame, keyed).
  - f26-f29: +6.4 to +7.0 per frame.
  - f36: +36. Monotonic.
  - The fly's own stroke peaks at 8.6 per frame, mean 4.9. The recovery runs inside the fly's own speed.
  - Takeoff is 36 f and the launch event is 0.389 (`full_step1`).
  - Seam: takeoff f36 vs fly f0 is 0.00 deg / 0.000 BU (`seam.txt`).
  - Visually: front f25 wings still near horizontal, f29 a V. TQ f29-f36 the wings climb smoothly.
- **M1 tail: LANDED in the side view.** The outer pair now reads as a blade (4x crop: a grey wedge with stacked feathers, a violet band and dark tips). Round 6 was a thin rod. Game camera still shows one fan with violet tips (walk, land, idle game sheets). No visible intersection with the trailing legs in side or takeoff frames. Step 1: `collision_free` true, `collisions` {}.
- **M3 back: LANDED on the stated target, weak on intent.**
  - Game camera, nearest-palette shares: STORM 31.3 % (builder 31.7; target <= 40; was 47.5). MANTLE 14.6 %.
  - STORM + MANTLE together are 45.9 %. The two greys differ by only 18 levels, so the back still reads mid-grey.
  - CHAR fell to 17.7 % on the game camera.
- **M4 eye: PARTIAL.** Fresh 2x head renders exist (`head2x_front`, `head2x_game`). Front 2x: black socket, violet FROST_V slit, and a pale FROST_H bar inside the slit. The slit reads as a slit and the hot spot is no longer a round glint. At 2x the pale bar still reads as a lit dash. At phone scale it is sub-pixel. Not a regression.
- **N1 frame labels: LANDED.** Each tile carries "takeoff fN  t s" and a footer with the render time. Order matches CLIP_NOTES.
- **N2 covert stagger: NOT DONE** (lead ruling, not counted).
- **M2 wing twist: NOT DONE** (lead ruling, not counted).

## 3. Scores

**Clips (per clip, 7 clips, average as in review 6):**

| clip | score | basis |
|---|---|---|
| idle | 9.0 | Unchanged apart from the tail. Game idle sheet checked, no regression. N2 excluded. |
| walk | 8.2 | Unchanged apart from the tail. Lateral shift 0.01 BU still reads faint. |
| fly | 8.5 | Code unchanged. Only fly f0 is rendered, so the stroke is judged from the computed values. |
| takeoff | 8.7 | C1 fixed (recovery at fly speed, seam exact). Coil still shallow (lead ruling). Front wings near horizontal to f25. |
| land | 8.5 | Unchanged. Game land sheet checked, tail OK. |
| roar | 9.0 | Not re-opened this round. Tail the only change. |
| act_bow | 9.0 | Not re-opened this round. Tail the only change. |

**Clip average: 8.7 PASS.**

**Flag for the lead:** the walk alone is 8.2, below the owner's 8.5 floor. Round 6 scored the clip gate as an average, and I followed that. If the owner's floor applies per clip, the walk blocks and needs the work in section 6.

**Model: 8.6 PASS.** The silhouette reads as a raptor-like bird, with a fierce hook beak, violet crest and a slit eye. The studded skin is intact. The tail is a blade from the side and a fan from behind. The back is still a mid-grey (45.9 %). The bind-pose wings read as poles from the front and 3/4 views (M2, ruled not counted). The eye bar is a small pale dash. That is +0.1 over round 6 for the tail and the grey step-down.

## 4. Regression check: none found

- Geometry unchanged since `r7b` (05:13), diffed. Renders current.
- Tail tilt -40 affects every clip's tail. No visible intersection with the trailing legs. `collision_free` true.
- Ground minimums: walk -0.015, takeoff / land / roar / act_bow / idle -0.014, fly +0.377. All >= -0.02.
- Neck 7.5 (<= 8), chest vs spine 4.0 (<= 5), head + neck pitch 26 (<= 30, from CLIP_NOTES, not re-run). Largest bone step 36.5 (land f8, the snow-puff FX anchor) and takeoff 30.6 (Foot_L f19), both under the 60 limit.
- Tris 12,964 (<= 15k). No glow. Eye hot spot FROST_H 0.010 x 0.002.
- Two greys (STORM / MANTLE) with no visible seam in the game view. Harmless.

## 5. Pass / fail

| # | check | result |
|---|---|---|
| 1 | step 1: collision_free, ground >= -0.02, audit linear 0, loops closed | PASS (-0.014 / -0.015, fly +0.377) |
| 2 | neck <= 8, chest vs spine <= 5 | PASS (7.5 / 4.0) |
| 3 | head + neck pitch-up <= 30 | PASS (26, CLIP_NOTES, not re-run) |
| 4 | largest bone step <= 60 per frame | PASS (36.5 land FX, 30.6 takeoff) |
| 5 | events match frames | PASS (launch f14 = 0.389, touch f17, roar f20, snap f58) |
| 6 | rest frames 0 deg | PASS (roar f60, act_bow f110, land f32; takeoff f36 = fly f0) |
| 7 | takeoff to fly seam | PASS (0.00 deg / 0.000 BU) |
| 8 | launch reads as weight | PASS (8-frame downstroke, 0.65-stud rise) |
| 9 | post-launch recovery at fly tempo | PASS (16.5 deg in 4 frames, then 6-7 per frame, inside the fly's 8.6 peak) |
| 10 | refs cited and matching | PASS (MUST 1) |
| 11 | model evidence current | PASS (renders 05:14-05:15 > geometry 05:13; 05:16 is comments only) |
| 12 | no glow; tris <= 15k | PASS (12,964) |
| 13 | no head shakes, no airborne spin, acts in place, rest at end | PASS |
| 14 | idle, roar, act_bow, land read | PASS (N2 open, ruled) |
| 15 | walk reads | PASS (8.2, faint weight shift) |
| 16 | fly reads | PASS (computed stroke; no fly stroke frames rendered) |

## 6. What is still between this pet and 9+ (exact, measurable)

**Model**
- **M3b back:** add one CHAR band across the mantle (the brief's second option). On the Chest and Spine shingle rows (`pets/BlizzardRoc.py` ~L263-267), make the middle row CHAR. Target on the game camera: STORM + MANTLE <= 40 % (now 45.9), CHAR >= 20 % (now 17.7). Re-run `flat_game.png`.
- **M4b eye:** set the FROST_H hot bar (228,216,255) inside the slit (~L164) to FROST_V (176,140,255) or drop it. Target: no pale dash in the 2x front render.
- M2 (bind-pose wing twist) is the largest model gap, but it is a lead ruling and not counted.

**Clips**
- **Walk (8.2):** raise the stance lateral shift from 0.01 BU to 0.02 BU (`pets/BlizzardRoc.py` walk, ~L597-612). Re-run step 1: walk slide 0.0, ground >= -0.02, collision_free true.
- **Fly (8.5), roar (9.0), act_bow (9.0):** carried forward. The fly stroke has no frame sheet (only f0 exists). Render fly f0-30 every 5 frames to confirm the stroke. Not blocking.
- **Takeoff (8.7):** coil shallow (lead ruling, not counted).

---------------------------------------------------------------------------------------------------------------------
**Verdict.** Model 8.6, PASS. Clips 8.7, PASS (average). MUST 1 landed. C1 landed. No regression. Walk 8.2 is the flag for the lead (per-clip floor). The M3b and M4b edits and the 0.02 BU walk shift are the next 9+ steps.
