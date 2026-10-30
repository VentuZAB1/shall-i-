# Frostcrown Dragon - scores review 6 (2026-10-28) - FINAL GATE

**Model: 8.2/10 - FIX. Clips: 8.4/10 - FIX.**

Both are under the 8.5 bar. Round 6 is a real step up from round 5 (model 8.0, clips 8.0). The tq and game views now show segmented, curved horns, the gold hero reads at icon size, the takeoff hands off to fly with no step, and the act ends with a visible finish. What still holds it below 8.5: the front view of the horns still shows wide gold faces, the flank bands are too thin to read at 300 px, the stricter ice-white count sits at 8.9 %, and the clip evidence for the final build is partly stale. Five MUSTs below; most of the work is in `horn()` and `trim_band()`.

## What I looked at
Newest set only (by timestamp, `PetsV3\FrostcrownDragon\`):
- `renders\crown_front.png`, `_crown_sheet.png` (front / game / tq), `crown_game.png`, `crown_tq.png` (01:49).
- `renders\_model_sheet.png`, `model_tq.png`, `model_side.png`, `flat_game.png` (01:49-01:50).
- `FrostcrownDragon_icon_game.png`, `renders\_icons_strip_64.png` / `_128.png`, `_icons2_strip_64.png` / `_128.png` (01:49).
- `renders\pose_game_takeoff_12 / 14 / 19 / 27`, `pose_game_fly_00`, `pose_game_act_stillfreeze_44 / 60 / 64 / 110` (01:36).
- `renders\_pose_tq_roar_sheet.png`, `_pose_tq_land_sheet.png` (labelled; unchanged clips, 00:48).
- `renders\_pose_tq_act_stillfreeze_sheet.png`, `_pose_tq_takeoff_sheet.png` (labelled, 00:48: see the staleness note).
- `_scratch\side_game_look.png` (01:36), `_scratch\FrostcrownDragon_r6final.py.txt` (identical to `r6f`, 01:48), `full_step1.txt` (01:49), `clips_last.txt` (01:36), `rest_delta.txt` (00:04), `crown.log`, `gold.json`.
- Code: `pets\FrostcrownDragon.py` L20-30 (palette), L118, L126-134 (`trim_band`), L151-153 (fin facets), L162-190 (`horn`), L415 (tail bands). Sibling palettes: `pets\PermafrostTitan.py`, `CinderOverlord.py`, `ThunderRex.py`, `BlackDragon.py`.
- Notes: `MODEL_NOTES.md` (round 6), `CLIP_NOTES.md` (round 6), `ANIM_REFS.md`, `_review\GLACIER_REVIEWER_BRIEF.md`, `FrostcrownDragon_review5.md`, `FrostcrownDragon_plan.md`, `GLACIER_CONCEPTS.md`.

Evidence gaps (they affect the clip score):
- `_pose_tq_takeoff_sheet`, `_pose_tq_act_stillfreeze_sheet`, `_pose_tq_idle_sheet` are from 00:48. They predate C1, the takeoff downbeat, the act snaps and the 3 deg fin tick, so they do not show the final build.
- `renders\_pose_sheet.png` (01:36) has no frame labels. I could not identify its 12 frames, so I used the labelled `pose_game_*` frames instead.
- The `pose_game_*` frames (01:36) came from a build of 9,416 tris (`clips_last.txt`). The final build is 9,288 tris (01:49). The shapes look the same, but the frames are one build older than the final.
- `rest_delta.txt` is from 00:04. The round-6 rest claims (takeoff f28 = fly f0; act f110 after the act edit) are not in any file.
- Not judged: an underside view (none in the set), and the face at game distance (`_close_sheet.png` is from round 2).

Independent counts (my own, from the PNGs; read-only, no files written, pure-Python decode):
- Game icon 512 px, 8x8 box to 64 px, alpha > 128: gold tool rule 29, brief rule 30, strict 16. This reproduces the builder's BOX column exactly (29 / 30 / 16).
- 128 px strip, first Frostcrown cell (x 8-134, panel and gap colours excluded): pet share 42 %; ice-white L > 200 and s < .2 = 9.6 % of pet pixels; L > 215 and s < .15 (the portrait rule) = 8.9 %; mean L 108; dark (L < 70) = 22 %.
- 64 px strip, same method: ice-white 8.9 % (loose) / 7.8 % (portrait rule); mean L 109; dark 21 %; gold tool 74, brief 101, strict 43.
- Builder for comparison: ice-white 9.3 % (strip 128) and 9.1 % (portrait 128); luminance 105 / 104; dark 24 %.

## Round-5 items (PASS / PARTIAL / FAIL)

| # | Item | Result | Evidence |
|---|---|---|---|
| M1 | Horns read as horns, not slabs | **PARTIAL** | Good from tq and game views (`crown_tq.png`: segmented curved horns with orange ridge bands). Front view still shows two wide gold faces: each upper segment about 80 px wide at 600 px, and the horns reach x ~108 and ~490 against a skull x ~185-415 (span ~1.65x the skull). `crown_game.png`: the near horn is a large flat gold wedge (the slab look). The diagonal cross-section (L163-165, `HORN_SIDE` L162) is in place, and the -29 % width is in the notes. |
| M2 | In-game gold (brief rule) | **PASS** on the brief rule (30 BOX / 28 LANCZOS, gate 25). Strict rule 16 (BOX) / 18 (LANCZOS): lead ruling applies. | The crown reads as gold and as the hero at icon scale: in `_icons_strip_128.png` the crown is the first thing you see against Thunder Rex and Cosmic Leviathan; in the 512 game icon it is the only warm saturated element. |
| M3 | Ice-white >= 9 % on both counts | **PARTIAL** | My counts: 9.6 % (loose) and 8.9 % (portrait rule, 128 px). Builder 9.3 / 9.1. The portrait rule is 0.1 short on my count. ICE_W second facets are in place (L151-153). |
| M4 | Flank banding (outclass vs Rex) | **PARTIAL** (reads as FAIL at 300 px) | Bands exist (`trim_band` L126-134) but each bar is 0.018 wide, 0.005 thick, offset 0.003 from the hide, and the hide is studded. At 300 px they show only as faint specks on the chest and belly (`_scratch\side_game_look.png`). Flanks still read as plain studded blue in `model_tq.png`. |
| C1 | Takeoff-to-fly handoff | **PASS** | Builder table (min z): takeoff f27 0.0899, f28 0.0940 = fly f0 0.0940, gap 0.000. The final build's `full_step1.txt` agrees on the fly floor (0.089 at f26). Visually `pose_game_takeoff_27` and `pose_game_fly_00` are the same pose. |

Round-5 checklist, the rest:
1. Five crown points from the front: PASS (`crown_front.png`: five diadem points, centre tallest).
2. Horns as horns: PARTIAL (M1).
3. Back crown ring from the game camera: PASS (`crown_game.png`: back band and spikes read; back points are GOLD).
4. Dark top separate from flanks: PASS (DEEP_STEEL saddle unchanged).
5. Luminance <= 110: PASS, thin margin (108 mine / 105 builder).
6. Dark share >= 28 %: **FAIL on both counts now** (22 % mine, 24 % builder). Round 5's 29 % was on a count neither method reproduces now. Not raised to a MUST: the 28 % line is a review-5 checklist number, not a brief rule, and the body colour is the approved steel-blue. See the TO 9+ list and the note below.
7. Ice-white >= 9 % both counts: PARTIAL (M3).
8. Gold hero portrait 64 >= 25: PASS (strict 43 mine / 75 builder; brief 101).
9. Gold hero game 64 >= 25 (strict): lead ruling; brief rule PASS (30), strict FAIL (16), not counted against it.
10. Gold clearly ahead of Rex and Leviathan: PASS (strip view; builder 44 vs 4 / 11 on the portrait).
11. Outclass detail (banding / seams): PARTIAL (M4).
12. Tris <= 13k: PASS (9,288 final; 15k cap).
13. Step 1 collision-free, loops closed, linear 0: PASS (`full_step1.txt` 01:49: collision_free true; audit linear 0 on all clips; walk slide 0.0).
14. Ground >= -0.02: PASS (-0.010 walk; -0.005 takeoff / act / roar / land / idle).
15. Neck <= 8 deg: PASS (7.5 neck, 7.0 neck2, per `CLIP_NOTES`; builder figure, not re-run).
16. Chest vs spine <= 5: PASS (3.0; builder figure).
17. Head + neck pitch-up <= 30: PASS (15; builder figure).
18. Largest step < 60: PASS (25.9 deg; builder figure).
19. End frames at rest: PASS visually (roar f66 = roar f00 pose; act f110 = act f00 pose; land f27-28 at rest). Numbers are from the 00:04 run only (see evidence gaps).
20. Takeoff-to-fly handoff: PASS (C1).
21. Act peak reads: PASS (`pose_game_act_44`, `_58`: wings spread, fins up, head pressed; the labelled act sheet shows the same beat).
22. Act finish beat: PARTIAL. The two snaps are present (f60 / f64, up +4 / tip -6 per `CLIP_NOTES`). At 300 px they read as a small flutter (`pose_game_act_60 / 62 / 64`).
23. ANIM_REFS: site tags for each primary clip: PASS (site tags and frames cited; HTTYD not used, per the lead's ruling).
24. Events match the clip table: PASS (fractions reconcile: launch 0.393 x 28 = f11; touch 0.571 x 28 = f16; roar 0.364 x 66 = f24; click f16; frost f50; frostpuff f80).
25. Name, no glow, studs: PASS (`tglow` empty; studs on the hide).

Other round-6 claims:
- Horn lit edge (GOLD_HI, L188): present; visible in the tq view.
- ICE_W frost edge on the wing arm (L23 comment): not visible at 600 px in `model_side.png`; not counted.
- Second fin facet (L153): present.
- Idle fin tick 3 deg: from notes only; not visible in a current sheet.
- Takeoff downbeat 86 deg over 5 frames: from notes; `pose_game_takeoff_12 / 14` show the wings swept down and back, consistent with the note.

## New MUSTs (only what blocks 8.5)

**MUST 1 - Horns still read as gold slabs from the front (M1, carried over).**
- Where: `horn()` L168-190; `HORN_W, HORN_D = 0.45, 0.55` L163; `rnd=0.35` at L182 and L186.
- Fix, in this order, re-rendering after each:
  a. Round the upper sections: `rnd` 0.35 -> 0.60 at L182 and L186. This costs no gold.
  b. Taper the tip section (segment i = 2 in `horn()`): hw and hd x 0.6, so each horn ends in a point.
  c. Pull the outer horn edge in so the front-view span is <= 1.35 x the skull width (now ~1.65 x).
- Measure: `crown_front.png` at 600 px shows no flat gold face wider than ~50 px in either upper segment (now ~80 px). `crown_game.png` shows no single flat gold face on the near horn that covers more than about a third of its visible side.
- Gold guard: the brief-rule count is 30 (BOX) / 28 (LANCZOS) against a gate of 25, a margin of 3-5 px. Any horn slimming must keep both >= 25 on the 64 px game icon. Gold may not move onto the body (the crown-only rule). If (c) drops it below 25, keep (a) and (b) and skip (c).

**MUST 2 - Flank banding is too thin to read at 300 px (M4, carried over).**
- Where: `trim_band()` L126-134 (bar thickness 0.005 and normal offset 0.003 on L133; default width `w=0.018` on L126); tail call `w=0.016` at L415.
- Fix: width 0.018 -> 0.030 (L126); tail 0.016 -> 0.028 (L415); bar thickness 0.005 -> 0.012 (L133); normal offset 0.003 -> 0.008 (L133).
- Measure: `model_side.png` and `model_tq.png` at 600 px show a continuous pale line >= 3 px wide on each torso block (rib, waist, hips) and on the tail, clear of the stud pattern. Step 1 must stay collision_free (the bars now stand off the flank, so re-check `fold_pairs`).

**MUST 3 - Ice-white margin on the stricter count (M3, carried over).**
- Measure: 8.9 % on the portrait rule (L > 215, s < .15, 128 px cell, pet pixels). Target >= 9.2 % so both rules clear 9 % with margin.
- Fix: widen the second ICE_W facet on each front fin (L151-153: `c.lerp(tip, 0.55)` and the 0.30 scale) so its area grows about 5 %. Keep ICE_W. Luminance must stay <= 110 (108 on my count).

**MUST 4 - Clip evidence for the final build (blocks the clip PASS).**
- Re-render from the 01:49 build, with frame labels: `_pose_tq_takeoff_sheet.png` (f0-28, including the f8-15 downbeat), `_pose_tq_act_stillfreeze_sheet.png` (f44-110, including the f58-66 snaps), `_pose_tq_idle_sheet.png` (f32 and f92 tick). Label or replace `renders\_pose_sheet.png`.
- Re-run the rest delta (`_scratch\rest_delta.py`) on the 01:49 build: roar f66, act f110, land f28, and takeoff f28 vs fly f0. The current file is from 00:04.
- Re-run the min-z table (takeoff f26-28, fly f0-1) on the final build. The claw change (0.08 -> 0.09) sits on Foot_FL, the lowest bone in those frames.

**MUST 5 - The act finish is too small to read at gameplay distance (clip, carried from review 5 TO 9+).**
- Where: the f60 / f64 wing snaps (up +4, tip -6 per `CLIP_NOTES` round 6).
- Fix: raise the wing-arm snap from +4 to +6 (keep the tip at -6), so the Wing bones move at least 6 deg at f60 and f64. Keep the largest bone step under 25 deg.
- Measure: `pose_game_act_60 / 62 / 64` read as a visible wing flick against the f58 / f62 SPREAD holds at 300 px.

## TO 9+ (after the 8.5 items)
- **Model, body value:** deepen STEEL_BLUE (L20) from (62,104,176) to about (56,94,162), about -8 %. This moves the dark share toward 28 % (now 22-24 %) and widens the luminance margin (108 mine, 105 builder, cap 110). If the 28 % line is a gate, this becomes a MUST.
- **Model, near horn:** a second GOLD_HI ridge on the root segment (L188), so the big face in `crown_game.png` gets a value step.
- **Model, face:** at 3/4 close (`crown_tq.png`) the EYE_HOT slit (L118) reads only as a dark notch under the diadem's lower edge. Lift the diadem front edge or the brow so the slit shows at 600 px.
- **Clips, flight:** the fly stroke is 40 / -24 (64 deg); the takeoff downbeat is 86 deg. Deepen the fly bottom to about -32 so the mythic's flight matches its launch. Keep the loop closed and the feet >= 0.05.
- **Clips, act:** hold the SPREAD pose two frames before the f70 HALF so the two snaps land as holds, not a blur.

## Notes for the lead (not scored)
- **Shared gold:** Frostcrown's GOLD (255,196,50) is the same RGB as Permafrost Titan's hero bezel (`pets\PermafrostTitan.py` L25). Both are Glacier-egg pets, and the Glacier decisions list gold for both. This is owner-approved as the Glacier gold family, so I did not fault it, but the two heroes sit in the same egg. Confirm they still read apart on the egg ladder.
- **Gold crown motif:** Thunder Rex (crown band), Cinder Overlord (crown plates) and Black Dragon (antlers) also use the house gold. The plan records the crown as owner-approved; flagging it for distinctness only.
- **Dark share method:** my round-5 29 % did not reproduce. On this round's cell I get 22 %, and the builder gets 24 %. The lead should fix one method before the next gate.
- **Gold in Studio:** the lead's Studio check under game lighting still decides the strict gold gate. My view: the crown reads gold and as the hero from the game camera.

## Pass / fail summary
| Gate | Result |
|---|---|
| Five crown points from the front | PASS |
| Horns read as horns | FAIL (MUST 1) |
| Back crown ring | PASS |
| Luminance <= 110 | PASS (thin margin) |
| Dark share >= 28 % | FAIL on both counts (TO 9+; lead to rule) |
| Ice-white >= 9 % both counts | PARTIAL (MUST 3) |
| Gold, portrait 64 >= 25 | PASS |
| Gold, game 64 >= 25 (brief rule) | PASS (30 BOX / 28 LANCZOS) |
| Gold, game 64 strict | lead ruling |
| Outclass banding | FAIL (MUST 2) |
| Tris <= 13k | PASS (9,288) |
| Step 1 collision-free, loops, linear 0 | PASS |
| Ground >= -0.02 | PASS |
| Neck <= 8, chest vs spine <= 5, pitch <= 30, step < 60 | PASS |
| End frames at rest | PASS visually; numbers stale (MUST 4) |
| Takeoff-to-fly handoff | PASS (C1) |
| Act peak reads | PASS |
| Act finish beat | PARTIAL (MUST 5) |
| Clip evidence for the final build | FAIL (MUST 4) |
| Events match the clip table | PASS |
| Name, no glow, studs | PASS |

Verdict: **FIX. Model 8.2, clips 8.4.** Do MUST 1-3 for the model and MUST 4-5 for the clips. Re-send: `crown_front.png` at 600 px and `crown_game.png`; the 64 px game icon with BOX and LANCZOS gold counts; both ice-white counts; `model_side.png` and `model_tq.png` at 600 px; the labelled takeoff, act and idle sheets from the final build; and the rest-delta and min-z numbers from the same build.
