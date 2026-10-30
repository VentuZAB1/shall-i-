# Frostfang Lynx - clip gate review 3 (2026-10-27) - APPROVED WITH FIXES

**Score: 7/10 for the clip gate** (the model was 8/10 at round 2). Pose limits pass, the four clips read, and the loops close. Two MUSTs remain: the claw flex collapses into one cyan plank, and the chest bib fix is not yet visible in any render. Both are small and codeable, and neither changes a bone name, a joint or the rest pose. Send one claw close-up and one front + below crop, then ship.

## What I looked at
- `FrostfangLynx/ANIM_REFS.md`, `CLIP_NOTES.md`, `MODEL_NOTES.md` (round 2).
- `_scratch/fullcheck.json` and `_scratch/gate.log`.
- `FrostfangLynx.json` (the exported clip tracks). I decoded every rotation track (quaternion per frame) and measured the angles myself. Details in section 2.
- `pets/FrostfangLynx.py` (timestamp 15:18) and its chest and throat lines (127-137), and the `rig()` / `check_pairs()` section.
- Renders: `_pose_tq_sheet.png`, `_pclose_tq_sheet.png`, `_pclose_side_sheet.png`, `pclose_side_act_clawflex_50.png`, `pclose_tq_roar_30.png`, `pose_tq_act_clawflex_50.png`, `pose_tq_walk_06.png`, `crop_front_throat.png`, `low_below.png`, `_scratch/clawtmp/claw_paw2.png`.
- My zooms (outside the project, in `C:\Users\ventu\AppData\Local\Temp\lynx_rev\`): the throat from the side idle frame, the throat from the tq roar frame, the claw-flex paws from the tq act frame.

---------------------------------------------------------------------------------------------------------------------
## 1. The chest-bib fix (round-2 MUST): NOT CONFIRMED

- `crop_front_throat.png` and `low_below.png` are both dated 14:49. `pets/FrostfangLynx.py` was changed at 15:18. The two crops therefore predate the source change. **They still show the old flat studded bib**: a light-blue rectangle hanging from the chin to the belly, about 0.27 units tall. They cannot confirm anything.
- The source at 15:18 does remove the old `B.add((0, -0.418, 0.600), ...)` bib. It is replaced by a sloped SNOW throat seg on the Neck (line 137: `B.seg((0,-0.385,0.560),(0,-0.56,0.785), 0.070, 0.056, SNOW, "Neck", ..., rnd=0.45)`).
- **That replacement still reads as a flat plank.** In my zoom of `pclose_side_idle_26.png` it is a pale, straight-edged, studded band running from under the jaw down to the front leg. In `pclose_tq_roar_30.png` it is a pale flat panel under the jaw. It is narrower than the old bib (half-width 0.070 against the old 0.086 / 0.028 depth), but it is the same plate in the same place.

**MUST M1:** make the throat fur, not a plate. Either:
- half-width 0.070 -> 0.045, half-depth 0.056 -> 0.035, `rnd` 0.45 -> 0.7; or
- split it into 2-3 tapered SNOW tufts (like the chest spikes on line 132-133) and delete the seg.

Then send `crop_front_throat.png` and `low_below.png` rendered from the current source (after 15:18). The renders must be newer than the source file.

**NICE 3 (one saddle band): ACCEPTED, not done.** The three torso inlays follow the torso blocks, so their tops step with the blocks. They read as segment seams at game distance (`game_view.png`, `pclose_side_act_clawflex_50.png`). They are flush with the body (`crop_rump_side.png`). Merge them later only if the owner sees plate joints.

---------------------------------------------------------------------------------------------------------------------
## 2. Numbers (my decode of `FrostfangLynx.json`, plus the builder's `fullcheck.json`)

**Builder audit (`_scratch/fullcheck.json`):** collision_free true; collisions none; linear 0 in all four clips; idle loop 0.0; walk loop 0.0, slide 0.0, foot_z_var 0.0; idle foot drift 0.0; ground_min_z -0.000 in all four clips; stride 0.355; tris 6,356; 34 bones. **Confirmed.**

**My decode of the rotation tracks (quaternion to Euler, degrees):**

| clip | Neck (total) | Head yaw | Neck+head pitch (min / max) | Chest vs Spine | Biggest per-frame step | Limit | Result |
|---|---|---|---|---|---|---|---|
| idle | 5.6 (yaw) | 8.4 (neck + head = 14.0) | -0.3 / +0.2 | 0.5 | Tail3 5.6 | neck <= 8, pitch <= 30 | **PASS** |
| walk | 2.0 | 2.8 | -0.5 / +0.5 | 2.4 | Shin 12.4 | chest vs spine <= 5 | **PASS** |
| roar | 4.0 (pitch) | 7.6 (pitch) | -8.4 / +5.0 | 1.0 | Shin 6.1 | pitch <= 30 | **PASS** |
| act_clawflex | 7.0 (X 5.0, Y 4.9) | 9.7 | -3.5 / +6.4 | 2.0 | Claw_FR 8.4 | neck <= 8, chest <= 5 | **PASS** |

Notes:
- The act neck total is 7.0. CLIP_NOTES says 6.5. It is still inside the 8 limit, so this is only a correction to the note.
- Claws: Claw_FL/FR open 39 deg max (notes say 35 + 4 knead). Per-frame step 8.4 deg (limit 60). **PASS.**
- Jaw: 25.2 deg open in roar (notes say 24). PASS.
- Ruff bones: roar Z 20.7 deg. Act Z 4.0. PASS.
- No head shakes: the idle turns are two slow 18-frame swings, +14 then -8, each held. Not a shake.
- No airborne frames: ground_min_z -0.000 everywhere.

**Loop seams (last stored frame to first):**
- idle: 0.9 deg max (Shin). Closed.
- walk: 10.9 deg on Foot_FR. That is a normal frame step (the biggest per-frame step is 11.7), so it reads as continuous, not a pop. Closed.

---------------------------------------------------------------------------------------------------------------------
## 3. MUST list

### M2 - The claw flex collapses into one cyan plank (act_clawflex f50 and f62)
`_scratch/clawtmp/claw_paw2.png` and my zoom of `pose_tq_act_clawflex_50.png` show the flexing paw's four claws as one flat cyan slab lying along the front of the paw. The four separate spikes at rest become a single blade when the paw opens. It reads as a ski or a plank, not as four claws. The act is named for the claws, so this is the signature of the clip.

**Root cause:** one `Claw_FL` / `Claw_FR` bone carries all four claws (MODEL_NOTES, "one Claw bone per forepaw"). All four are parallel at rest (direction 0, -1, -0.55) and rotate together, so the four stay parallel and merge into one plank from the side.

**Fix (pick one):**
1. Split the claws into four child bones of the Claw bone (or of the Foot), each with its own open angle and a yaw splay of about -14, -5, +5, +14 deg in the flex pose. This is the clean fix. Keep the 39 deg open on the centre two and 30 deg on the outers, so the fan spreads.
2. Or keep one bone and add a per-claw yaw in the mesh so the rest claws already fan slightly (about 6 deg between neighbours). Then the flex opens them into a fan.

- **Pass:** `claw_paw2.png` at f50 and f62 shows four separate cyan claws, not one slab. Also check the rest pose: the four claws must still look like four claws.

### M1 - The chest throat still reads as a plate (see section 1)

---------------------------------------------------------------------------------------------------------------------
## 4. NICE list
1. **Walk loop seam:** 10.9 deg on Foot_FR at the wrap. It is a normal step, so no action is needed. If the walk ever looks like it hitches at the wrap, copy the frame-0 pose into frame 24.
2. **Reference rule:** ANIM_REFS used Sakugabooru because animationreference.org had no cat, crouch or claw tags. The brief names Sakugabooru as the fallback. Accepted. Log the tag misses so the next pet tries the same tags first.
3. **Neck note:** correct CLIP_NOTES from 6.5 to 7.0 deg for the act neck total, or leave it. Inside the 8 limit either way.
4. **Claw timing:** claw1 f48 and claw2 f60 match the plan. Keep them.
5. **Toe roll:** 12 deg toe roll with the heel down. Accepted (see deviations). It reads as a raised paw in the tq frames.

---------------------------------------------------------------------------------------------------------------------
## 5. Deviations, one by one

| deviation | verdict | reason |
|---|---|---|
| New Ruff_L/R bones for the roar flare | **ACCEPT** | The flare needs its own hinge. Ruff bones move only the cheek ruff. Roar Z 20.7 deg, collision_free true, `check_pairs` updated. The roar frame (`pclose_tq_roar_30.png`) shows the flare reads as fins. |
| Right paw lag 12 f (not 8) | **ACCEPT** | The sparks land on the plan frames (f48 and f60). The 8 f lag would put claw2 at f56. |
| 12 deg toe roll, heel down | **ACCEPT** | Claw rotation alone did not read. The roll reads as a lifted paw in the tq frames. The ankle rise is at most 0.008, so the heel stays planted. |
| Head turns 14 deg to the pet's left (+X), not toward the follow camera | **ACCEPT** | The follow camera is behind the player, so the pet's left is the side that shows in the game three-quarter view. The head yaw total (neck + head) is 14.0 deg in idle. In act the head's total rotation is 9.7 deg, mostly the look-down. Reasonable. |

---------------------------------------------------------------------------------------------------------------------
## 6. Clip reads (from the player's eye)

- **idle (120 f loop, look-around):** reads as a watchful look. Two slow turns, +14 then -8, each held. Ears follow late. Pass.
- **walk (24 f loop, lateral sequence):** reads as a steady cat walk. Head is steady. Stride 0.355. Pass. Slide 0.
- **roar (60 f, ruff flare f13, hiss f30):** reads as a threat. The cheek ruff flares into cyan fins, the jaw opens on the frost fangs, the neck pushes forward 8 deg. The best clip so far. Pass.
- **act_clawflex (96 f, in place):** the crouch and the stare read. The toe roll reads as a raised paw. **The claw spread does not read** (M2). Fix M2 and this passes.

## 7. Pass/fail checklist (clip gate)

| # | item | result |
|---|---|---|
| 1 | collision_free true | **PASS** |
| 2 | linear 0 in every clip | **PASS** |
| 3 | loops closed (idle, walk) | **PASS** |
| 4 | walk slide 0, foot_z_var 0 | **PASS** |
| 5 | ground_min_z >= -0.02 | **PASS** (-0.000) |
| 6 | neck <= 8 deg | **PASS** (max 7.0 in act) |
| 7 | chest vs spine <= 5 deg | **PASS** (max 2.4 walk, 2.0 act) |
| 8 | head + neck pitch-up <= 30 deg | **PASS** (-8.4 / +6.4) |
| 9 | no head shakes | **PASS** |
| 10 | no airborne spins or frames | **PASS** |
| 11 | per-frame limb step <= ~60 deg | **PASS** (max 12.4) |
| 12 | acts in place, end at rest | **PASS** (act ends at rest by f88, paws planted) |
| 13 | readable beats (idle, walk, roar, act) | **PASS** for idle, walk, roar. **FAIL** for act claws (M2) |
| 14 | ANIM_REFS rule (refs cited, timings used) | **PASS** (Sakugabooru fallback, named) |
| 15 | chest bib / throat reads as fur from front and below | **FAIL** (M1, not yet confirmed by a current render) |
| 16 | saddle: one band (NICE) | **NOT DONE, accepted** |

Score tally: 12 PASS, 2 FAIL (items 13 and 15, from M2 and M1), 1 accepted NICE (item 16), 1 PASS with note (item 14).

## 8. Re-send checklist
- `FrostfangLynx/renders/pclose_tq_act_clawflex_50.png` and `pose_tq_act_clawflex_50.png` after the claw split (M2), plus `_scratch/clawtmp/claw_paw2.png` at f50 and f62.
- `crop_front_throat.png` and `low_below.png` rendered from the current source, after the throat change (M1). The render must be newer than `pets/FrostfangLynx.py` (currently 15:18).
- `FrostfangLynx.json` and `.lua` after the rig change, plus `fullcheck.json` (collision_free must stay true).

Verdict: **APPROVED WITH FIXES, 7/10.** Two MUSTs (M1 throat, M2 claws). Once both are re-rendered and checked, the Lynx is ready to ship.
