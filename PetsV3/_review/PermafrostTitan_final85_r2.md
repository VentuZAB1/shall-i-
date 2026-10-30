# Permafrost Titan - FINAL 8.5 GATE, ROUND 2 (model + clips, as re-exported 2026-10-28) - FIX

**Model: 7.5/10. Clips: 7/10. Verdict: FIX (both below 8.5).**
Owner bar: 8.5 is the minimum, higher is better. Nothing under 8.5 ships.

Round 2 landed the big items. The chest ring is bigger and reads at 64 px. The roar now reads as a bellow: the arms go out, the head lifts, and the open jaw shows a dark gap at f27. The mouth and the belly band are fixed, the knuckles read as fingers, and the blunt pauldron ice reads as crust.

Two things still hold it back. The legs still read as stacked blocks from the side and the front, and the kneel has no clear read from the 3/4 or the game camera. The idle is better but still small at 2x.

## What I looked at (round 2)

- Notes: `PermafrostTitan/MODEL_NOTES.md` and `CLIP_NOTES.md` (FINAL 8.5 sections). Source: `pets/PermafrostTitan.py` (edited 01:09; line numbers below are approximate after the edits).
- Model renders: `_model_sheet.png`, `_icons_strip_64.png` / `_128.png`, `_icons2_strip_64.png` / `_128.png`, `gamelook_game.png`, `model_back.png`.
- Clip renders: `_kneel_views.png`, `_beats2x_kneel.png`, `_beats2x_roar.png`, `_beats2x_idle.png`, `_roar_jaw_close.png`, `hx_tq_act_kneelrise_40.png`, `hx_game_act_kneelrise_40.png`.
- Not re-run: Blender and the headless gate (the brief forbids it). Clip numbers come from the notes. Studio colour is not checked (the lead's ruling: judged in Studio).

## Model score: 7.5/10 (was 7)

**Fixed since round 1**
- **Hero:** chest ring R_OUT 0.272 (portrait gold 51 px at 64). It reads as the clear hero at 64 and 128 px, and the back ring still reads from behind (27 px).
- **Head:** the skull is bigger and the slits are 15 % wider. The fierce brow reads at 128 px.
- **Fists:** the knuckle shards are shorter. The fists read as curled fingers, not teeth.
- **Pauldrons:** blunt flat-topped ICE_W chunks. Good: pale mass without spikes.
- **Belly band:** smooth ICE_W under the ribcage. Readable, a little like a white belt (see NICE).
- **Colour:** MAUVE (164,116,200) and PLUM (98,66,130) as specified. The lead rules that Studio decides, so colour is no longer a MUST here.

**Still costs points**
- **The legs are still stacked blocks.** In `_model_sheet.png` (side and tq) and `_kneel_views.png`, each leg still has a thigh plate, a knee cap and a shin guard, plus an ankle band, all as separate dark steps. The thigh top sits under the hip block, so the leg starts from a box. This is the robot read that held the Yeti at 5/10.
- **The hip block hides the thigh tops** from the front view (the builder says so). The legs look like they hang from a block, not from the hip.
- **Side silhouette:** the chest and pelvis are still two stacked blocks with a dark joint band between them (`model_side`).

## Clip score: 7/10 (was 6.5)

- **Roar: 8/10 (was 5-6).** `_beats2x_roar.png`: f22 to f50 the left arm swings out toward the camera and the right arm is clear of the torso. The head lifts and the chest pushes forward. `_roar_jaw_close.png` shows a dark slate mouth gap at f27, from the front and 3/4. This reads as a bellow now. Keep.
- **Idle: 7/10 (was 5).** `_beats2x_idle.png` f0 / f30 / f60 / f90: the fists and the torso change visibly at 2x. At 5 studs the change is still small, so it needs a bit more (MUST 2).
- **Kneel: 6.5/10.** From the side it reads. The 3/4 front-left view (`hx_tq_act_kneelrise_40.png`) reads as a lunge: the kneeling knee is hidden behind the standing shin and the right sole is not visible. The game camera (`hx_game_act_kneelrise_40.png`) shows the bent right leg and the lying foot, but not clearly a knee on the snow. The game camera is the view players see most, so this matters most.
- **Walk: 7/10.** Heavy, planted, unchanged. Fine.
- **Gate numbers (from the notes, not re-measured):** collisions 0, ground >= -0.02 (-0.009 at the kneel), loops closed, slide 0, chest vs spine 3 deg, head up 22 deg world (limit 30), no head shake. Pass.

## MUST (to 8.5 on both)

**Model**
1. **Legs, one tapered tube (thigh ~L264-266, knee cap ~L270, shin guard ~L272, shin ~L271).**
   - Thigh taper goes to 0.66 at the knee (the notes say 0.72 now).
   - The thigh plum plate (L266) goes from half-depth 0.046 to 0.02, so it is a flush plate and not a step.
   - Knee cap (L270): half-depth 0.04 to 0.02, so it reads as a bulge on the tube.
   - Drop the separate ankle band (A + 0.015 on the shin, L272) to one flat band at the ankle, or remove it.
   - Test: `model_side.png` and `_kneel_views.png` front show no step on the thigh or shin, from the side and the front.
2. **Legs start from the hip, not under the block.** The hip block (Spine, L105) goes from width 0.30 to 0.27 at its base, and the thigh top (L264) moves out 0.02 in x. Test: `_model_sheet.png` front shows the thigh tops clear of the hip block.
3. **Chest and pelvis as one shape (L108 to L110).** Round the belt joint (L107) from rnd 0.4 to 0.5 and the chest bottom from 0.66 to 0.62 taper, so the side silhouette has no step between the chest and the pelvis.

**Clips**
4. **Kneel readable from the game camera and the 3/4 (act_kneelrise, Foot_R and Knee_R).**
   - First, a posed close-up at f40 from the game camera, aimed at `Knee_R`, and one from the 3/4. If the right knee cap is clearly on the snow in both, no change.
   - If not (the expected result from the current renders), mirror the kneel to the **left knee** (the camera side), with the same timing, the Spine roll, the foot turn and the elbows, and move the `Knee_R` and `Foot_R` anchors to the kneeling side. Keep the ground rule (>= -0.02) and the chest vs spine <= 5 deg.
   - Test: `hx_game` and `hx_tq` at f40 show the kneeling knee on the snow and the sole visible.
5. **Idle needs more life at 5 studs.** `idle()`: the hip yaw `4 * sn` goes to **6**, and add a chest counter-yaw of 2 deg (the Chest yaw goes from -0.4 x yaw to -0.8 x yaw), keeping the head level. The fist flex stays at 8 deg.
   - Test: `_beats2x_idle.png` f0 vs f30 shows a clear shift of the torso and the fists. Feet stay planted; re-run step 1.

## NICE

1. The ICE_W belly band (L110 to L112) reads as a white belt. Narrow it from half-width 0.20 to 0.16 and height 0.016 to 0.012, so it reads as pale underside.
2. The 64 px portrait: the Titan is still a purple figure with a yellow ring. The lineup is fine, but the purple reads softer than the Yeti's blue. Studio decides.
3. The 24-beat pose sheet is too small to judge the kneel. Send the kneel close-ups at 2x, as the builder did for the roar.

## Pass / fail checklist (round 2)

| Check | Result |
|---|---|
| Model 8.5 or higher | FAIL (7.5) |
| Clips 8.5 or higher | FAIL (7) |
| Hero reads at 64 px (portrait gold 51) | PASS |
| Hero reads at 128 px and from behind (back 27) | PASS |
| Three bands plus gold | PASS |
| Fierce face (slits, no glint, no smile, bigger brow) | PASS |
| Blunt ice, no spikes, no crown, no cyan, no glow | PASS |
| Knuckles read as fingers | PASS |
| Pauldrons read as crust, not shelves | PASS |
| Belly band reads as underside | PARTIAL (belt read; NICE 1) |
| Legs read as tapered limbs (no stacked blocks) | FAIL (MUST 1, 2) |
| Hip block and thigh tops | FAIL (MUST 2) |
| Chest and pelvis as one shape from the side | PARTIAL (MUST 3) |
| Mouth reads open at the roar peak | PASS (f27 dark gap) |
| Roar reads as a bellow | PASS (8/10) |
| Idle reads alive at 5 studs | PARTIAL (MUST 5) |
| Kneel reads from the side | PASS |
| Kneel reads from the 3/4 and the game camera | FAIL (MUST 4) |
| Collisions, ground, loops, slide, chest vs spine, head limits | PASS (notes; re-run after MUST 2, 4, 5) |
| Tris at or under 15k (7,672) | PASS |
