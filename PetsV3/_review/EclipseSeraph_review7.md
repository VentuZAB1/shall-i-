# Eclipse Seraph - model + clip gate review 7 (2026-10-28) - final gate

**Model: 8.0/10 - FIX. Clips: 8.5/10 - PASS.**

Round 6 was model 8 / clips 8.5. Since round 6 the Index card now shows six wings, the punch is clearly ahead of the Solar Lion, and the muzzle no longer reads as a white cat muzzle. One round-6 acceptance is still missed: the far lower wing tips protrude about 0.09-0.11 H outside the mane, not the 0.15 H asked for. The lion read at card size is also still moderate. That keeps the model under the 8.5 bar. The clips hold at 8.5.

---

## What I looked at (newest set, renders 04:57-05:07 on 2026-10-28)

- `EclipseSeraph_icon.png` (512 Index card), with 3x crops of both flanks and a 4x face crop. Scratch crops are in `C:\Users\ventu\AppData\Local\Temp\r7scratch`. Nothing was written to the pet or review folders.
- `renders\_icons_strip_64.png` (496 px) and `_icons_strip_128.png` (944 px). Both hold **7 cells**: Seraph, Solar Lion, Frostcrown, Griffin, Celestial Dragon, Cvetibara, Cosmic Leviathan. The round-6 "6 cells" gap is closed.
- `renders\_icons2_strip_64.png` and `_128.png` (3 cells).
- `renders\idle_front.png`, `idle_game.png`, `idle_tq.png`, `_model_sheet.png`.
- Clip sheets, **front and game views for all seven clips** (idle, walk, fly, takeoff, land, roar, act_wingcascade). The 7 `pose_tq_*` sheets were not opened.
- My own punch count on the 64 px strip (tile pixels excluded, outline counted in and out):

| 64 px strip cell | mean S (outline in) | share S > 0.35 (in) | mean S (outline out) | share (out) |
|---|---|---|---|---|
| **Seraph** | **0.412** | **66.6 %** | **0.434** | **78.8 %** |
| Solar Lion | 0.397 | 58.3 % | 0.400 | 62.5 % |
| Frostcrown | 0.385 | 59.0 % | 0.405 | 68.2 % |
| Celestial Dragon | 0.378 | 56.0 % | 0.416 | 72.2 % |

  The builder's own count is Seraph 0.410 / 65.9 % and Solar Lion 0.391 / 56.5 %. Mine agrees within about 0.02.

- Documents: `GLACIER_REVIEWER_BRIEF.md`, `EclipseSeraph_review6.md`, `EclipseSeraph_plan.md`, `GLACIER_CONCEPTS.md` (owner decisions), `MODEL_NOTES.md` (round 7), `CLIP_NOTES.md`.
- **Not re-run:** the headless gates, the tris count (builder 11,336), and the raw-render dark share. I took the builder's figures for those and checked them only where they show on screen.

---

## Round-6 items

### MUST 1 - six wings on the Index card and at rest: **PARTIAL**

- **Count on the 512 card: PASS.** I count six wing shapes:
  - far side: the upper fan (six or seven blades above the halo), a middle group (three blades left of the halo), and a lower group (three dark tip clusters at cheek height, left of the muzzle);
  - near side: the upper blade, the horizontal middle fan, and the lower wing reaching past the foreleg.
- **Acceptance (b), far lower tip depth: FAIL.** The far lower tips extend only about 35 px beyond the mane outline on the card. By my read H is about 315 px there, so that is about 0.11 H (the builder's own figure is 0.09 H). The round-6 target was 0.15 H, about 47 px at this scale. The far lower wing is three tips, not a full wing shape, so it is the weakest of the six.
- **Acceptance (c), cut-through and walk at 0 hits: not re-run.** The builder reports 0 hits and collision_free true.
- **Acceptance (d), icon re-rendered: PASS.** `EclipseSeraph_icon.png` is dated 05:07.
- **Front view: PASS.** `idle_front.png` and the front idle, fly, takeoff and cascade sheets all show three tiers per side. From the front the six-point star reads clearly.
- **Rest pose majestic, not awkward: PASS with a note.** In the front and game views the spread reads as a deliberate display. In the three-quarter rest view (`idle_tq.png`) the far lower tips cross beside the muzzle. That is crowded at the face, though not awkward in motion. Any fix must push the reach outward or back, not forward.

### MUST 2 - punch vs the Solar Lion at 64 px: **PASS (clear margin)**

- Mean saturation now leads on both counts (+0.015 with outline, +0.034 without). The saturated share leads by about 8 points with outline and 16 without.
- The Seraph also leads the Frostcrown and the Celestial Dragon on my outline-out count. The round-6 "mean level" concern is closed.
- Guards: near-white 18.8 % (builder, raw render) passes the 30 % guard. Dark is 22.7 % (builder, raw), which passes the 22 % guard with a thin margin. I did not re-measure the raw dark share.

### Face: muzzle no longer cat-like: **PARTIAL-PASS**

- The muzzle is now a lilac-grey stud pad with only the chin white. The white muzzle that read as a cat is gone (`_icons_strip_128.png`, `icon_face_4x`).
- The lion read at 64 and 128 px is still moderate. At strip size the Seraph reads as a pale-faced winged creature inside a dark mane. The Solar Lion reads as a lion at the same size.

### Halo at the launch (MUST 3 of round 5): **PARTIAL (unchanged)**

- f13 and f17 are clear: the gold rim and the red corona both read.
- f10: the left upper blade touches the lower-left rim. Light.
- f24: the left blades cover part of the halo. This is the approved fly stroke top, per the lead ruling.

### Other round-6 items

| item | result |
|---|---|
| Gold, halo on the card and strip | PASS (rim and corona read at 64 and 128 px) |
| 7-cell strip restored (TO 9+ 2) | PASS |
| Punch margin 0.41 on the strip count (TO 9+ 3) | PASS (0.412 in, 0.410 builder) |
| Front fly lower beat (TO 9+ 4) | PARTIAL-PASS (lower pair visible at flank level, softer than the upper pair) |
| Roar tilt 18 (round-5 TO 9+ 5, not re-checked in round 6) | PASS on sight (see clips) |
| Tris <= 15k | builder 11,336 (not re-counted) |

---

## Clips: **8.5 PASS**

- **Six wings in motion, game view: PASS.** The cascade (f58 / f70) shows three tiers per side.
- **Six wings, front view: PASS.** Front cascade hold f58-70 shows the lower pair as a level tier.
- **Halo at launch: PARTIAL (unchanged).** As above.
- **Front fly lower beat: PARTIAL-PASS (unchanged).**
- **Roar, tilt 18: PASS on sight.** The roar sheets at f30 and f50 show the halo lifted and tilted, with a visible gap above the mane. The builder's 0.055 BU clearance is not re-measured.
- **Idle, walk, land (not re-rendered in round 6): PASS on sight.** The rest pose holds through the idle and walk. Land settles into the display fan by f28. No visible clipping in the game or front views.
- **Collisions, ground, pose limits: builder logs only, not re-run.** Logged: collision_free true, ground_min_z -0.013 (worst), neck 6.0, chest vs spine 2.5, head plus neck 15, largest step 21.6 deg.

The clip score rests on the builder's logs and my read of the front and game sheets. I did not open the `pose_tq_*` sheets.

---

## New MUST (model only; this is the one item that blocks 8.5)

**MUST 1 - far lower wing tip depth on the Index card (round-6 MUST 1, acceptance (b), not yet met).**

- **Where:** the far lower pair (viewer's left on the 512 card), `Wing_C_L` / `WingTip_C_L`, in `DISPLAY_POSE` (currently C = -12 / +70 / 0 / -45).
- **Measure:** the far lower tips protrude about 0.09-0.11 H (about 0.20-0.25 BU of the 2.234 BU model) outside the mane outline. The target is 0.15 H (about 0.335 BU). The gap is about +0.11 BU (+0.05 H) of extra tip reach.
- **Fix:** add that reach by one of these, whichever keeps the tips clear of the cheek in `idle_tq`:
  - lengthen the far C feathers by about 0.11 BU at the tip; or
  - move the far C root outward by about 0.11 BU.
  Push the reach outward and back, not forward (forward reach is what crowds the muzzle).
- **Acceptance:**
  - on the re-rendered 512 card at the same camera, the far lower tips sit at least 0.15 H (about 47 px at 512) outside the mane outline;
  - the DISPLAY_POSE cut-through ray test is 0 hits;
  - step 1 holds: collision_free true, linear 0, loops closed, ground >= -0.015, neck <= 7.5, chest vs spine <= 4;
  - all 7 clips at 0 collisions;
  - `EclipseSeraph_icon.png` and the 64 / 128 px strips are re-rendered and sent with the next round.

With this item met and nothing else changed, I expect the model to clear 8.5.

---

## TO 9+ (after the 8.5 bar; not required)

1. **Lion read at card and 128 px.** The face is still small against the mane. Give the lilac muzzle and the OBSID cheek ruff a little more share of the head, so the face reads as a lion at 128 px without bringing back a white muzzle.
2. **Palette vs the owner decision.** `GLACIER_CONCEPTS.md` binds the body to `#E8D0F0` (lilac-ivory). The model now uses MOON_IVORY (210,150,246) and BODY_MID (184,86,228), a saturated violet. The punch gain is real, and the owner left details to the builder, so this is not a blocker. The lead should confirm the violet with the owner, or move back toward the owner's hex in a step that keeps the punch margin.
3. **Front fly lower beat.** Give the lower pair's downstroke about 4 deg more amplitude, so it reads as strongly as the upper pair.
4. **Halo at f10.** Trim the far upper blade's root by about 2 deg for f8-12 so its edge clears the rim's lower-left. Leave f24 alone (approved fly stroke top).
5. **Evidence.** Open the seven `pose_tq_*` sheets before the next gate. They are current (04:59) but were not opened for this review.

---

## Pass / fail checklist (round 7)

**Model**

| item | result |
|---|---|
| Six wings countable on the card (MUST 1 count) | PASS (six, the far lower is three tips) |
| Far lower tip depth >= 0.15 H (MUST 1 acceptance b) | FAIL (about 0.09-0.11 H) |
| Six wings, front view | PASS |
| Rest pose not awkward | PASS with a note (far tips crowd the muzzle in tq) |
| Punch: mean S and share vs Solar Lion (MUST 2) | PASS (clear margin on both counts) |
| Near-white <= 30 % (guard) | PASS (18.8 %, builder raw) |
| Dark >= 22 % (guard) | PASS, thin (22.7 %, builder raw) |
| Muzzle no longer cat-like | PASS (white muzzle gone) |
| Lion read at 64 / 128 px | PARTIAL (improved, still moderate) |
| 7-cell strip restored | PASS |
| Halo, gold rim and corona | PASS |
| Tris <= 15k | builder 11,336 (not re-counted) |

**Clips**

| item | result |
|---|---|
| Halo unoccluded at the launch (f12-20) | PASS (f13, f17); f10 light; f24 lead ruling |
| Six wings in motion, game view | PASS |
| Six wings, front view and cascade hold | PASS |
| Front fly lower beat | PARTIAL-PASS |
| Roar tilt 18 | PASS on sight |
| Idle, walk, land re-render | PASS on sight |
| Pose limits, collisions, ground | PASS per builder logs (not re-run) |

---

**Verdict:** the model is held at 8.0 by one item: the far lower wing shows as three tips, about 0.09-0.11 H outside the mane, against the 0.15 H the round-6 acceptance asked for. The count and the punch are fixed, and the face is better. The clips are at 8.5 and pass.
