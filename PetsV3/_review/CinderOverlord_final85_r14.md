**Model: 8.4/10 - REVISE. Clips: 8.5/10 - APPROVED (lowest clip 8.5: idle 8.5, walk 8.5, roar 8.5, act_molt 8.5).**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 14 (fresh reviewer, 2026-10-28)

Round 14 is the owner-approved last small round: the five round-13 fixes (hood colour, nose, crown, molt hold, gate
file). The clips now pass. The model does not. The molt hold is fixed and the gate file is clean. The hood is now a
red fan separate from the dark frill and crown from the front and three-quarter views. From behind and above, and at
64 px, it still reads as a dark collar under a dark crown mass, not as a hood. That keeps the model at 8.4.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round-13 review `_review/CinderOverlord_final85_r13.md` (the 5 MUSTs).
- Builder notes: `CinderOverlord/MODEL_NOTES.md` (round 13, lines 7-69) and `CinderOverlord/CLIP_NOTES.md` (round 13, lines 12-27).
- Gate and proof files: `CinderOverlord/_scratch/gate_f85.json` (`gold_gate`, `area_gate`, `collision_proof_r13`,
  `stance_r13`, `icons_64_128`), `coll_probe_r13.txt`, `stance_r13.txt`, `headshare_r13.txt`, `face_id_r13.txt`,
  `pawpx_r13.txt`, `gold_r13.json`.
- Code read in `pets/CinderOverlord.py`: HEIGHT line 15; palette lines 19-29; HOOD constants lines 335-344; `cobra_hood()`
  rim `OBS_D` line 395 and back plate `PLUM_OBS` line 390 (both as the builder states); ribs `PALE_S` line 402; SKS nose
  stations line 509 (0.82 -> 0.112 / 0.066 / -0.040; 0.96 -> 0.046 / 0.028 / -0.062; tip 1.0 -> 0.026 / 0.018 / -0.068);
  jaw chin line 547; crown table lines 585-587 (centre `0.40`, middle `0.30`, outer `0.25`); `roar()` lines 797-812;
  `MOLT_ARCH, MOLT_HEAD = -9.0, 9.0` line 824; molt arch/head keys lines 835-836; idle roll line 761.
- Images opened (all of the brief's list; title bars 14:41-14:43, "final 8.5 round 13"): `renders/_molt_game.png`,
  `_scratch/nose_hide_r13.png`, `_scratch/nose_r13_before_after.png`, `gamelook_game.png`, `gamelook_tq.png`,
  `_icon_game_64_128.png`, `_icons2_strip_64.png` / `_128.png`, `_cv_idle_game.png`, `_cv_idle_front.png`,
  `_hood_back_2x_idle_f0_f20.png`, `../CinderOverlord_icon_alt.png`, `_icons_alt_strip_64.png` / `_128.png`,
  `_icons_strip_64.png` / `_128.png`, `close_front.png`, `_close_sheet.png`, `_model_sheet.png`, `_pose_tq_sheet.png`,
  `_molt_r13_front.png`, `_molt_r13_tq.png`, `_cv_roar_front.png`, `_cv_roar_side.png`, `_cv_walk_game.png`,
  `_cv_walk_side.png`. Also `../CinderOverlord_portrait_alt.png` (its path is `CinderOverlord/CinderOverlord_portrait_alt.png`).
- Style bar: the brief's summary, `FIERCE_GUIDE.md` (first part), vault `06 Modelling and Art/Creature Style.md` (secret /
  ultra-rare must outclass; 64 px read), `Model Review Checklist.md` (grep), `_review/GLACIER_CONCEPTS.md` OWNER DECISIONS,
  `_review/GLACIER_PLAN_REVIEW.md` section 2.10. `ANIM_REFS.md` not re-read this round (the round-13 reference stands).
- Limits: no pixel tool and no Blender run (reviewer rule). Area, gold, clearance and pose numbers are the builder's files;
  I checked them against the code and by eye, and they are internally consistent. The palette is not scored; the walk-tile
  tail crop is framing (waived); breath is a Studio check; the Cinder width rule is waived (serpent); HEIGHT 11.72 and
  the hood width |x| 0.64 are accepted; the two shoulder seats (<= 0.0277) are accepted (limb roots, not visible).

## 1. The owner's question, answered

**From the GAME camera (behind and above, phone size): closer, but not yet a hooded cobra.**
- `gamelook_game.png` and `_hood_back_2x_idle_f0_f20.png` (game row): the hood is now a red fan with a dark rim and pale
  ribs, separate from the dark frill spikes above and the dark crown. That part of the round-13 fix works.
- But from behind the hood reads as two red flaps on the neck, not a spread hood. The read is weaker than from the front.
- At 64 px (`_icon_game_64_128.png`, `_icons2_strip_64.png`, `_icons_alt_strip_64.png`) the Cinder is a red coil under a
  gold crown and a dark head mass. The hood is a dark collar at best. It does not read as a hood at 64 px.
- At 128 px (`_icons_alt_strip_128.png`, `_icons_strip_128.png`) the red fan under the head is visible.

**From the FRONT and 3/4 views: yes, a hooded, crowned cobra-dragon.**
- `close_front.png`, `_model_sheet.png` (panels 2 and 4) and `gamelook_tq.png`: the red hood fans flare out behind the jaw
  with the dark rim and pale ribs. The crown reads as five gold-tipped blades with a taller centre.

**Does the front read as a tapered dragon snout, not a pig nose? Yes.**
- `_close_sheet.png` panels 2 and 3 and `nose_r13_before_after.png`: the muzzle is a wedge that slopes down to a narrow
  tip with the nostrils on it. The old round oval end is gone.
- The top of the muzzle is still a small round dome from the front. That is a NICE item, not a block.

## 2. Clip table (per-clip floor: the clips score is the LOWEST clip)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | The cobra sway is upright and level. The hood moves with the neck (fixed-camera frames). The game head gap is 50.7-65.8 px (>= 50). Pitch-up 1.8 deg max. The sway is still small at phone size (roll 2.2 per bone, line 761; r11 NICE 3 not done). | `_cv_idle_game.png` (f0-f105), `_cv_idle_front.png`, `_hood_back_2x_idle_f0_f20.png`; `stance_r13.txt` (idle) |
| walk | 8.5 | The slither holds its line. Game head gap 61.8-63.0 px. Head pitch +/-0.6 deg, neck 1.1 deg max per bone. The tail tip crops in the game tile at f8-f40 (framing, waived). | `_cv_walk_side.png`, `_cv_walk_game.png`; `stance_r13.txt` (walk) |
| roar | 8.5 | The jaw opens with white fangs at f30-f44 (side view), and the head clears the jaw (Jaw\|Neck2 0.0769 at f30). The hood does NOT spread for the threat: the front wings are the same at f0, f30 and f44 (the hood is rigid on the neck). The game head gap dips to 47.5 px (no gate for roar; observed). | `_cv_roar_front.png`, `_cv_roar_side.png`; `coll_probe_r13.txt`; `stance_r13.txt` (roar) |
| act_molt | 8.5 | Fixed from 8.3. The game head gap is 52.5-62.2 px at every beat (r12: 34.8). The head stays level (head 9 deg, pitch-up 1.0 deg). The blade lift, fan and settle read in the game camera (lift f22, fan f34-f40, peak f56-f84, settle f100). Trade-off: the neck arch is halved (3 deg per bone), so the molt is a blade lift on a near-upright neck, not a rear-up. | `_molt_game.png` (NEW), `_molt_r13_front.png`, `_molt_r13_tq.png`; `stance_r13.txt` (act_molt) |

**Clip floor: min(8.5, 8.5, 8.5, 8.5) = 8.5. APPROVED for the clips.** The roar's 47.5 px dip and the rigid roar hood are
NICE items below, not blocks (as in round 12).

## 3. Round-13 items (PASS / PARTIAL / FAIL / OPEN)

| r13 item | result | evidence |
|---|---|---|
| 1. Hood colour: back plate `OBS_D` -> `PLUM_OBS`; ribs -> `PALE_S`; rim (`OBS_D`) and blue spot kept; geometry unchanged | **PARTIAL.** Built as stated (lines 390, 395, 402). From the front, 3/4 and the game camera the red fan separates from the dark frill. At 64 px the rim is still the same dark value as the frill and crown, so the hood merges into a dark collar. Pass for the owner's front / 3-4 read; not yet for the 64 px read. | `pets/CinderOverlord.py` 390-402; `gamelook_game.png`, `_hood_back_2x_idle_f0_f20.png`, `_icons_alt_strip_64.png` |
| 2. Nose: muzzle tip 0.026 x 0.018, 0.96 width 0.046, slope down (dz -0.040 / -0.062 / -0.068), cap ring x0.55, chin flatter (0.070 / 0.026, tip 0.024 / 0.012) | **PASS.** The side profile is a clean wedge; the front shows a narrow tip with the nostrils and no pig bulb. The hide test (`nose_hide_r13.png`) shows the two lumps removed. Visible half-height under the nostril line is 0.018 (<= 0.03). Fangs and roar mouth unchanged. NICE 3: the top of the muzzle is still a small dome from the front. | `_close_sheet.png` panels 2-3; `nose_r13_before_after.png`; `close_front.png` |
| 3. Crown **DEVIATION**: centre kept at 0.40; side blades 0.23 / 0.18 -> 0.30 / 0.25 | **ACCEPTED (better).** Kit portrait 64 px: gold 117 (r12 113), area 0.378 (r12 0.365), now >= Thunder Rex 0.372. Crown neighbours >= 0.0357 in all clips (r12 0.0307). The five-blade crown still reads in `close_front.png` and `_model_sheet.png`; no crown collisions. Open: `Crown_3|Head` clearance is not reported (see MUST 2). Alt portrait area 0.369 is still under Thunder Rex (see MUST 2). | `CinderOverlord/_scratch/gate_f85.json` (`gold_gate`, `area_gate`, `icons_64_128`, `collision_proof_r13.crown_neighbours_all_frames`); `pets/CinderOverlord.py` 585-587 |
| 4. Molt hold **DEVIATION**: head 20.5 -> 9, neck arch -22.5 -> -9 (3 deg per neck bone) | **ACCEPTED (better).** The game head gap is 52.5-62.2 px at every beat (r12 34.8), so the 50 px target holds. The head stays level. The trade is a halved arch: the molt is a blade lift on a near-upright neck, which is shallower than the S2 rear reference. The reared read now lives in idle and roar. The reviewer's own round-13 fallback was this route, so accepted. | `_molt_game.png`, `_molt_r13_front.png`; `stance_r13.txt` (act_molt screen gap [52.5, 62.2]); `pets/CinderOverlord.py` 824-836 |
| 5. Gate file: every old gold figure deleted (incl. "91"); `gold_gate` 117 is the only gold number; `area_gate` 0.378 added | **PASS.** `grep -w 91` finds nothing in `gate_f85.json`. The only gold field is `gold_gate` (117, floor 103). `area_gate` is present (0.378 >= 0.372). | `_scratch/gate_f85.json` |
| Gates (collision, ground, loops, stride, height, tris, pose, head share, game area, paws, head gaps) | **PASS** (all reproduce from the files). See section 7. | `gate_f85.json` (`step1`, `collision_proof_r13`, `stance_r13`, `game_icon_head_share`, `paws_past_body_outline_game_cam_BU`) |

## 4. Model score: 8.4 - REVISE

**Holds:**
- The molt hold is fixed (52.5 px at every beat) and the clips pass.
- The crown outclasses Thunder Rex on kit area (0.378 vs 0.372) and gold (117 vs 113 before, 93 Phoenix next).
- The nose is a tapered wedge from the side and a narrow tip from the front.
- The gate file has one gold number and no stale figure.
- Collision kit gate is true (85 pairs); ground -0.006; loops 0 / 0; stride 5.0089; tris 13,580; head share 0.320; game area 0.212.

**Blocks 8.5:**
1. **The 64 px hood read.** The hood rim is the same obsidian as the frill and the crown, so at 64 px and from behind the
   hood is a dark collar, not a red hood. (MUST 1.)
2. **Proof gap.** The round-13 review asked for `Crown_3|Head` clearance >= 0.02. It is not reported anywhere in the
   gate file or the notes. The alt portrait (0.369, under Thunder Rex) is not ruled out as a shipped icon. (MUST 2.)

## 5. MUST list (model, blocks 8.5)

**MUST 1 (model, the 64 px hood): separate the red hood from the dark frill by value at the rim.**
Evidence: `_icons_alt_strip_64.png` (tile 1), `gamelook_game.png`, `_icon_game_64_128.png`.
- Cause: the hood rim is `OBS_D` (line 395), the same obsidian as the frill and cheek spikes (lines 537-541) and the crown
  sockets. The rim merges with them at 64 px.
- Fix (primary): change the rim `B.seg` at line 395 from `OBS_D` to `PALE_S` (222, 194, 158). Keep its size. The fan gets a
  light edge that frames the red against the dark frill. Keep the ribs `PALE_S` (line 402) and the blue spot.
- Fallback, if the pale rim reads toy-like from the front: keep the rim `OBS_D` and lower the top edge of the Neck3
  hood outline by 0.03 BU (`HOOD_PANELS`, lines 341-342, the top point `(1.64, 0.15)` and `(1.60, 0.23)`). That opens a red
  band between the hood and the frill. Re-check `HOOD|SPIKES` (>= 0.02) and `HOOD|Head` (>= 0.02) after the change.
- Pass: in `gamelook_game.png` and the 64 px kit tile, the hood is a red fan with a light edge, visibly separate from the
  dark frill above. Front and 3/4 views stay clean (`close_front.png`).

**MUST 2 (proof): report the missing clearances and state the shipped icon.**
Evidence: `_scratch/gate_f85.json` (`collision_proof_r13`, `icons_64_128`), `pets/CinderOverlord.py` lines 585-587.
- Add `Crown_3|Head` (and `Crown_1..5|Head`) to `collision_proof_r13.min_surface_clearance_all_frames` with the frame and
  clip. Pass >= 0.02. Run `_scratch/coll_probe.py` for the pair; the kit gate is clean for the crown sockets, so this is a
  reporting fix unless the probe finds a real overlap.
- The gate file names the kit portrait as the gate icon (0.378). State in the file which portrait ships. If the alt
  portrait (molt f40, 0.369) ships anywhere, its 64 px area must reach 0.372 or it is dropped from the outclass claim.
- Pass: the gate file reports `Crown_3|Head` >= 0.02, and the shipped icon's area is >= 0.372.

## 6. NICE list (not blocking)

1. **Hood spread in the roar (r12 NICE 1, carried).** The hood is rigid on the neck, so the roar front shows the same wings
   at f0, f30 and f44 (`_cv_roar_front.png`). Give each side its own hinge (`Hood_L` / `Hood_R` off Neck3) and roll it
   outward 10-15 deg from f14 to f30, back to rest by f58. Re-run the hood clearance (>= 0.02). This is the cobra threat
   move and the largest single gain for the roar.
2. **Roar head gap 47.5 px (observed; not gated).** The molt now holds >= 50 px. Lift the roar's closest beat by 2-3 deg
   of head or neck gather (`roar()` lines 797-812) so the game gap reaches 50 px. Re-measure with `stance_probe.py`.
3. **Snout top from the front.** The muzzle top is still a small round dome. Lower the 0.82 station height from 0.066 to
   0.054 (line 509) so the front is a flatter wedge. Side profile unchanged; re-check the nose clearances.
4. **Hood side slab (r12 NICE 2, carried).** From the side (`_close_sheet.png` panel 2) the Neck2 panel is an edge-on dark
   plate at jaw height. Taper the outer edge in `HOOD_PANELS` (lines 339-341) so it reads as a fan from the side.
5. **Idle sway at phone size (r11 NICE 3, carried).** Roll 2.2 -> 3.0 deg per neck bone (line 761); head counter-roll
   -4.4 -> -6.0 (line 762). Keep the head level; re-measure the game gap (must stay >= 50 px).
6. **Claws at game size (r12 NICE 5, carried).** `PAW_CLAW` 0.110 -> 0.130 (line 213).

Waived or not scored (lead ruling): the walk-tile tail crop (framing), palette hygiene, breath (Studio check), the Cinder
width rule (serpent), HEIGHT 11.72 and hood width (accepted), the two shoulder seats (accepted).

## 7. Pass / fail checklist

| check | result |
|---|---|
| Model >= 8.5 | FAIL (8.4) |
| Clips, every clip >= 8.5 (lowest clip) | PASS (idle 8.5, walk 8.5, roar 8.5, act_molt 8.5) |
| Game silhouette reads a hooded cobra at 64 px (owner core test) | FAIL (hood is a dark collar at 64 px; separate from the frill from the game camera) |
| Hood red fan separate from the frill and crown (game camera) | PASS (`gamelook_game.png`, `_hood_back_2x` game row) |
| Front / 3/4 read: hooded, crowned cobra-dragon | PASS |
| Front face: tapered dragon snout, not a pig nose | PASS (top dome NICE 3) |
| Hood clean: no floating panel, gap or poke (all frames) | PASS (side slab NICE 4) |
| Hood clearance >= 0.02 to every part | PASS (min 0.0509, head) |
| Fierce eyes and brows; no glints; no smile | PASS (`_close_sheet.png`, `_cv_roar_front.png`) |
| Gold >= 103 at 64 px, one counter | PASS (117) |
| Gate file: no contradicting gold figure ("91") | PASS (grep finds nothing) |
| Outclass Thunder Rex on kit area (0.372) | PASS (0.378, kit portrait) |
| Alt portrait area >= 0.372 if it ships | FAIL/UNKNOWN (0.369; ship status not stated; MUST 2) |
| Outclass Phoenix / Ivonrath / Thunder Rex / Cosmic Leviathan on kit gold | PASS |
| Tris <= 15k | PASS (13,580) |
| Stride 5.0089; ground >= -0.02; loops 0 / 0; linear 0 | PASS (5.0089; -0.006; 0 / 0; 0) |
| Kit collision (joint-aware, 85 pairs) | PASS (true) |
| Strict run: only the shoulder seats, depth <= 0.035 | PASS (0.0264 rest / 0.0277 max) |
| Crown neighbours >= 0.02 in all clips | PASS (0.0357) |
| Crown_3\|Head >= 0.02 | NOT REPORTED (MUST 2) |
| Paws >= 0.10 BU past the neck outline (both sides) | PASS (0.388 / 0.164) |
| Paw-to-neck >= 0.02 | PASS (0.148) |
| Head + crown >= 0.30 of figure height | PASS (0.320) |
| Game area >= 0.18 | PASS (0.212) |
| Neck <= 7.5 deg per bone | PASS (max 4.0 roar; 3.0 molt; 2.45 idle roll) |
| Chest vs spine <= 5 deg | PASS (4.5) |
| Head + neck pitch-up <= 30 deg | PASS (max 4.0) |
| Game head gap >= 50 px: idle / walk / act_molt | PASS (50.7 / 61.8 / 52.5) |
| Game head gap >= 50 px: roar | Observed 47.5 px (no gate set; NICE 2) |
| No head shakes; acts in place; ends at rest | PASS |
| Shoulder seats not visible in any render | PASS (accepted) |
| Palette hygiene; breath; walk-tile crop; width rule | Not scored (lead ruling) |
| HEIGHT 11.72; hood width \|x\| 0.64 | Accepted (lead ruling) |
