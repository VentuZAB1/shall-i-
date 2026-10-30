# Permafrost Titan - FINAL 8.5 GATE (model + clips, as exported) (2026-10-28) - FIX

**Model: 7/10. Clips: 6.5/10. Verdict: FIX (both below 8.5).**
Owner bar (2026-10-28): nothing under 8.5 ships. Owner clarification: 8.5 is the minimum, higher is better. The TO 9+ list is below the MUST list.

The pet is solid and the hero works: the chest ring reads at 128 px and from behind, there are no spikes, no crown, no cyan and no glow, and the palette is three bands plus gold. It does not yet outclass the Yeti (14 %) or the Roc (7.4 %) as a SECRET. The limbs are still a stack of boxes (the same robot read that got the Yeti 5/10 earlier), the in-game body is dusky, and the clips are the weak half. The idle is almost static, the roar barely reads, and one bug stops the jaw from opening visibly.

## What I looked at

- Review files: `PermafrostTitan_plan.md` (v2), `PermafrostTitan_review1.md` to `review4.md`, `GLACIER_CONCEPTS.md` (owner decisions), `GLACIER_REVIEWER_BRIEF.md`.
- Notes: `PermafrostTitan/MODEL_NOTES.md` (rounds 1 to 5), `CLIP_NOTES.md` (rounds 4 and 5), `ANIM_REFS.md` (sections A to C).
- Source: `pets/PermafrostTitan.py` (palette L19 to L28, chest ring L162, jaw and mouth L218 to L220, arms and fists L222 to L242, legs L260 to L276, `idle()` L383, `roar()` L436, `act_kneelrise()` L458 to L490). Source lines are cited from grep, not re-read in full.
- Renders: `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64/128.png`, `_icons2_strip_64/128.png`, `gamelook_game.png`, `gamelook_tq.png`, `flat_game.png`, `model_back.png`, `_kneel_views.png`, `_beats2x_kneel.png`, `_beats2x_roar.png`, `_pose_tq_sheet.png`.
- Comparisons: `GlacierYeti/renders/_model_sheet.png` and `_icons_strip_128.png`, `BlizzardRoc/renders/_model_sheet.png` and `_icons2_strip_128.png`, `Raiju/renders/_model_sheet.png`, `_review/GlacierYeti_review4.md` (8/10 clips), `BlizzardRoc_review4.md` (8/10 clips), `_ALL_FIERCE_progress.png`.
- Not re-run: Blender and the headless gate (the brief forbids it). Clip numbers come from the notes and the earlier reviews' recomputation. I did not re-read `PermafrostTitan.json` this round. Studio colour is not checked (no Studio access from here).

## Model score: 7/10

**Works**
- The chest bezel is a clear hero at 128 px (yellow ring around the white core). From behind the back echo ring gives 24 gold px at 64 px (no other pet in the lineup has any gold on its back).
- Three bands plus gold: MAUVE body, PLUM plates, ICE_W caps and core, GOLD hero. Pale caps read as crust, not shelves.
- No spikes, no crown, no cyan, no glow, no Neon. Studs on the body, smooth details. Tris 7,552 (builder count), under the 15k cap.
- Face: slits under a slate brow, black pupils, no glint, no smile. Reads fierce at 128 px.
- Clean from below (`_under_sheet.png`): no floating or poking parts.

**Costs points**
- **The limbs are still stacked boxes.** In `_model_sheet.png` (side and tq) and `_kneel_views.png`, the thighs, shins, forearms and upper arms are straight prisms with separate plum plates. Stacked segments read as a robot, the same read that got the Yeti 5/10.
- **The in-game body is dusky.** `gamelook_game.png` shows a dark muted purple, about (72,64,104) in the dominant bucket. Rounds 2 and 3 asked for the lift to be checked in game. That is still open, so the body reads as a purple toy at 64 px.
- **The head is small and sunk.** At 64 px the head is a nub between the caps; the face carries only through the brow.
- **The gold is modest at 64 px.** Portrait gold is 31 to 37 px, a small yellow ring. It is a clear hero at 128 px, but at the phone size it reads as a dot.
- **The fist knuckle shards look like teeth** from the front (`_model_sheet.png`, `_kneel_views.png` front). Not a blocker, but it hurts the animal read.
- **Lineup:** the Titan is a box-golem like LavaGolem (same family of stubby legs and box fists). The gold ring keeps them apart, but the build is not yet its own.

## Clip score: 6.5/10

**Passes (gate):** collisions 0, ground_min_z at or above -0.02, loops closed, walk slide 0, chest vs spine within 5 deg, head up within 30 and down within 20, no head shake, acts end at rest (notes). The kneel reads from the side and the rise is clean (`_beats2x_kneel.png`).

**Reads weakly (what the player sees)**
- **Idle is almost static.** `idle()` (L383 to L400): the chest pitch is 1 deg, the spine rise is 0.005 BU (about 0.03 studs), the arms settle 2 deg, the hip yaw is 3 deg. In `_pose_tq_sheet.png` the f0, f30 and f60 frames look the same. A secret's most-watched clip needs visible life.
- **The roar barely reads.** `roar()` (L436 to L444): the arms go out 8 to 9 deg, the head lifts 10 deg, the spine leans 1 deg. In `_beats2x_roar.png` the f0 and f50 frames look almost the same, and the mouth stays a thin line through f27.
- **Bug: the jaw cannot show.** The jaw block is on bone `Jaw` (L219), but the mouth slit is on bone `Head` (L220). The jaw opens 16 deg at f27 (L441), yet the slit stays put, so the open jaw shows no dark gap. That is why the roar mouth stays a line.
- **The kneel is readable from the side, weak from 3/4.** In `_kneel_views.png` tq f40 the kneeling knee is hidden behind the standing thigh, and the right foot's sole does not show.

## Verdict and MUST list (to reach 8.5 on both)

**MUST 1 (model, colour, L19 and L22).** Lift the body so the in-game colour carries.
- MAUVE (146,101,178) becomes **(164,116,200)**. Hue stays about 274 (same family), saturation stays about 0.42, brightest channel 200.
- PLUM (86,56,112) becomes **(98,66,130)**, so the three bands stay apart.
- Test: in the `gamelook_game` camera, the dominant body bucket is at least **(100,80,130)**. It is about (72,64,104) now.

**MUST 2 (model, limbs, L230, L264, L271).** Stop the stacked-box read on the limbs.
- Thigh (L264), pillar shin (L271) and forearm (L230): each gets a taper toward the joint below it, the same way the torso already tapers (`bot` scale about 0.80 to 0.84). Round the deltoid (L226) from rnd 0.45 to 0.55.
- Test: `model_side.png` and `_kneel_views.png` show no straight prism on any leg or arm segment.

**MUST 3 (model and roar, L219, L220, roar K table L437 to L444): fix the jaw.**
- Move the MOUTH slit (L220) to bone `Jaw`, so it moves with the jaw. Its centre stays on the jaw hinge line.
- Add a JOINT_D dark cavity block (about 0.084 x 0.02 x 0.03 BU) on `Head` behind the jaw, so an open jaw shows black.
- Test: a close-up of the roar at f27 (jaw 16 deg) shows a clear dark mouth gap, not a line.

**MUST 4 (clip, roar, L437 to L444): make the bellow readable.**
- Arms out: the arm column goes from 8 to 9 deg to **22 deg** at f22 to f50 (f34 at 24, f58 at 10; f10 stays at -2 as the anticipation).
- Head lift: the head column (`hd`) goes from -10 to **-15** (up limit 30, so this has margin).
- Lean: Spine pitch from -1 to **-4**, Chest pitch from -3 to **-7**. Chest vs spine stays at 3 deg (limit 5).
- Per-frame swing stays under about 3 deg (limit 60).
- Test: `_beats2x_roar.png` at f0, f22, f34, f50 shows arms clearly out and a visible forward push.

**MUST 5 (clip, idle, L383 to L400): give the idle visible life.**
- Breath: Chest pitch `-1.0 * br` becomes **`-2.0 * br`**. Spine sink `-0.005 * br` (the body drops at the breath peak) becomes **`-0.015 * br`** (about 0.07 studs).
- Hip yaw: `3 * sn(...)` becomes **`4 * sn(...)`**.
- Fists: add a slow flex of **+/- 8 deg** on the `Hand_L` and `Hand_R` bones, 60-frame period. Keep the feet planted and the head level (no head tilt).
- Re-run step 1 (ground_min_z and collisions) after the change.
- Test: idle f0 and f60 differ clearly in `_pose_tq_sheet.png` at 2x.

**MUST 6 (clip, kneel, `act_kneelrise` L458 to L490): make the kneel read from 3/4.**
- The right foot (Foot_R) turns **10 deg outward** during f18 to f50, so the sole shows in the 3/4 view. Keep the knee at or above -0.02 on the snow (the notes give -0.009 now).
- The elbow bend in the hold (f30 to f50) goes from 4 to **8 deg**, so the fists sit on the thighs.
- Test: `cv_tq_act_kneelrise_40.png` and `kv_tq_act_kneelrise_40.png` show the right knee on the snow and the sole visible.

## TO 9+ (the outclass push for a SECRET, highest impact first)

1. **Bigger chest hero.** `R_OUT` (L162) goes from 0.240 to **0.265** (outer diameter about 0.53 BU). Keep the ring alone, clear of the pauldrons. Target: at least 45 portrait gold px at 64 px (now 37). This is the single biggest rarity cue at phone size.
2. **Bigger head.** The skull (L203) goes from (0.145, 0.150, 0.128) to **(0.160, 0.160, 0.135)**, raised 0.02 BU so it clears the shoulder line. Slits (`ice_eye`, L77) +15 % wide. The face then carries at 64 px.
3. **Blunt ice at the pauldron tips.** The upper caps (L246) grow a flat-topped ICE_W chunk about 0.18 BU tall. Blunt, no points (keeps the no-spike rule), but it widens the 64 px silhouette and adds pale mass. This is the crystal-vs-studded contrast a secret should have.
4. **Shorter fist shards.** The knuckle shards (L238, L241 to L242) go from 0.058 to about **0.035**, so they stop reading as teeth in the front view.
5. **Pale underside (FIERCE rule).** An ICE_W belly band (about 0.20 x 0.03 BU) under the ribcage (L110 to L112), smooth. The rule asks for a pale underside, and the Titan does not have one (review 1, PARTIAL).
6. **VFX, not mesh.** Core bellow snow burst on `icedust` (f24) and a kneel dust puff on `icecrack` (f18), through the Blender flipbook pipeline (never a glow mesh).

## Pass / fail checklist (final gate)

| Check | Result |
|---|---|
| Model 8.5 or higher | FAIL (7/10) |
| Clips 8.5 or higher | FAIL (6.5/10) |
| Hero reads at 128 px (front, back) | PASS |
| Hero reads at 64 px (phone size) | PARTIAL (small dot; TO 9+ 1) |
| Three bands plus gold | PASS |
| Fierce face (slits, no glint, no smile) | PASS |
| Real anatomy, no stacked-box limbs | FAIL (MUST 2) |
| In-game colour carries | FAIL (MUST 1) |
| Not a toy / not childish | PARTIAL (purple body, boxy limbs) |
| Distinct from Rex, Leviathan, Yeti, Roc | PASS (no spikes, no crown, no cyan, no feathers) |
| Distinct from LavaGolem build | PARTIAL (same box-golem family; TO 9+ 2 and 3) |
| No spikes, crown, cyan, glow, Neon | PASS |
| Tris at or under 15k | PASS (7,552, builder count) |
| collision_free, ground >= -0.02, loops, slide 0 | PASS (notes; re-run after MUST 5 and 6) |
| Idle reads as alive | FAIL (MUST 5) |
| Roar reads as a bellow (arms, head, jaw) | FAIL (MUST 3, 4) |
| Kneel reads from side, front and 3/4 | PARTIAL (3/4 FAIL; MUST 6) |
| Walk reads heavy, in place | PASS |
| Acts in place, end at rest | PASS (notes) |
| Animation refs cited (owner rule) | PASS (ANIM_REFS section A to C) |
