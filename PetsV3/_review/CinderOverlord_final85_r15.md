**Model: 8.5/10 - APPROVED. Clips: 8.5/10 - APPROVED (lowest clip 8.5: idle 8.5, walk 8.5, roar 8.5, act_molt 8.5).**

# Cinder Overlord - FINAL 8.5 GATE, ROUND 15 (fresh reviewer, 2026-10-28)

Round 15 is the round-14 blocker fix (the obsidian hood rim is now pale) plus the two round-14 proof items. The
hood now reads as a light-edged red fan from the game camera, the front and the icon. The round-14 blocker is gone.
What is left is NICE-level polish that has been carried for several rounds. The model clears the 8.5 floor.

## 0. What I looked at, and the limits

- Brief `_review/GLACIER_REVIEWER_BRIEF.md`; round-14 review `_review/CinderOverlord_final85_r14.md` (MUST 1 and MUST 2).
- Builder notes: `CinderOverlord/MODEL_NOTES.md` (round 14, lines 7-41).
- Gate and proof files: `CinderOverlord/_scratch/gate_f85.json` (`shipping_portrait`, `gold_gate`, `area_gate`,
  `collision_proof_r14`, `stance_r14`); `coll_probe_r14.txt`, `stance_r14.txt`, `headshare_r14.txt`, `face_id_r14.txt`,
  `gold_r14.json`. `grep -w 91` on `gate_f85.json` returns nothing.
- Code read in `pets/CinderOverlord.py`: HOOD constants lines 335-345; `cobra_hood()` hood back `PLUM_OBS`, rim
  `B.seg(... PALE_S ...)` (r14 line marked) and ribs `PALE_S` (lines ~386-405); nose station table line 509 (`SKS`);
  crown table lines 583-588 (centre 0.40, sides 0.30 / 0.25); `roar()` lines 795-813 (no hood keys, so the hood does
  not spread); `act_molt` lines 822-837 (`MOLT_ARCH, MOLT_HEAD = -9.0, 9.0`).
- `CinderOverlord/ANIM_REFS.md` read for the clip rule (refs cited for idle, walk, roar and act_molt).
- Images opened (all of the brief's list): `renders/gamelook_game.png`, `gamelook_tq.png`, `_icon_game_64_128.png`,
  `_icons2_strip_64.png`, `_icons2_strip_128.png`, `_cv_idle_game.png`, `_cv_idle_front.png`,
  `_hood_back_2x_idle_f0_f20.png`, `_molt_game.png`; shipping `../CinderOverlord_portrait_raw.png` and
  `../CinderOverlord_icon.png`; reference `../CinderOverlord_portrait_alt.png`; `_icons_strip_64.png`,
  `_icons_strip_128.png`, `_icons_alt_strip_64.png`, `_icons_alt_strip_128.png`; `close_front.png`, `_close_sheet.png`,
  `_model_sheet.png`, `_pose_tq_sheet.png`, `_molt_r14_front.png`, `_molt_r14_tq.png`, `_cv_roar_front.png`,
  `_cv_roar_side.png`, `_cv_walk_game.png`, `_cv_walk_side.png`.
- Limits: no pixel tool is available (PIL is not installed, and I did not write any image file). The 64 px hood read
  is by eye at native size and cannot be zoomed, so I rely on the builder's 64 px proof for the value step. I did not
  re-run the probes; the numbers are the builder's files, checked against each other and the code.
- Waived or not scored (lead ruling): the walk-tile tail crop (framing), palette hygiene, breath (Studio check), the
  Cinder width rule (serpent). Accepted: HEIGHT 11.72, hood width |x| 0.64, the round-13 crown and molt deviations, the
  two shoulder seats (<= 0.028), and the crown blade hinges inside the mount.

## 1. The owner's question, answered

**From the GAME camera (behind and above, phone size): yes, a hooded, crowned cobra-dragon.**
- `gamelook_game.png`: the crown reads as five gold blades on a dark studded mount. The frill is dark and spiky. The
  hood shows as two light-edged red flaps at neck height, separate from the dark frill above. The round-14 blocker is
  fixed here.
- `_hood_back_2x_idle_f0_f20.png` (game row): the cream rim and the pale ribs frame a red fan, and the dark frill sits
  above and to the sides. From behind the hood still reads as two flaps, not a full spread. That is the rigid roar
  hood (NICE 1), not a model fault.
- "Reared": the idle neck is raised with the head level (`gamelook_tq.png`, `_model_sheet.png` panel 4). It is not a
  full rear. The molt rear was halved in round 13 and accepted.

**At 64 px:** the crown and head read. The hood is a light band under the dark head (the builder's read, which I
confirmed by eye at native size on `_icons_strip_64.png` and `_icon_game_64_128.png`). The value step is there, but
it is small. This is the only point I could not verify beyond the builder's proof.

**From the FRONT and 3/4 views:** yes. `close_front.png` and `_close_sheet.png` panels 1 and 3 show the pale-piped red
hood flaring out behind the jaw, the dark frill, and five gold-tipped blades with a taller centre. The snout is a
tapered wedge with a narrow tip and nostrils. The eyes are narrow slits under heavy brows, with no glints and no smile.

**Worthy MYTHIC next to the other secrets?** Yes on the numbers the lead ruled on (kit 64 px, `gate_f85.json`):
- Gold 117 (floor 103). Next highest: InfernoPhoenix 93. Ivonrath 25, Cosmic Leviathan 20, Thunder Rex 13.
- Area 0.378 (shipping kit icon). Thunder Rex 0.372, Ivonrath 0.295, InfernoPhoenix 0.267, Cosmic Leviathan 0.208.
  The margin over Thunder Rex is thin (+0.006), so it is a NICE item to protect.
- Distinct: red, cream and dark with a gold crown. Phoenix is orange flame, Ivonrath is a purple-red bat, Thunder Rex
  is blue-black, Cosmic Leviathan is purple and blue. No sibling accent is copied.

## 2. Clip table (per-clip floor: the clips score is the LOWEST clip)

| clip | score | why | evidence |
|---|---|---|---|
| idle | 8.5 | The cobra sway is upright and level, with the head held on its line (head pitch-up 1.8 deg max, head 5.4 deg). The game head gap is 50.7-65.8 px (>= 50). The sway is small at phone size (NICE 5). The hood moves with the neck. | `_cv_idle_game.png` (f0-f105), `_cv_idle_front.png`; `stance_r14.txt` (idle) |
| walk | 8.5 | The slither wave runs head to tail, with the S-bend moving through the body. The game head gap is 61.8-63.0 px. Head pitch +/-0.6 deg; neck 1.12 deg max per bone. The tail tip crops in the game tile at f8-f40 (framing, waived). | `_cv_walk_game.png`, `_cv_walk_side.png`; `stance_r14.txt` (walk) |
| roar | 8.5 | The jaw opens with white fangs at f30-f44 (side view), the head stays level, and the neck gathers 12 deg total (4 per bone, max). The hood does NOT spread: no hood keys in `roar()` (lines 795-813), so the wings are the same at f0, f30 and f44. The game head gap dips to 47.5 px (not gated; observed). The roar is at the floor, held there by NICE 1 and NICE 2. | `_cv_roar_front.png`, `_cv_roar_side.png`; `coll_probe_r14.txt` (Jaw\|Neck2 0.0769); `stance_r14.txt` (roar) |
| act_molt | 8.5 | The blade lift, fan and settle read in the game camera: lift f22, fan f34-f40, centre peak f56-f84, reseat f100. The game head gap is 52.5-62.2 px at every beat. The head stays level (head 9 deg, pitch-up 1.0 deg). Trade-off, accepted in round 13: the neck arch is halved (-9 total, 3 per bone), so the molt is a blade lift on a near-upright neck, not a rear-up. | `_molt_game.png`, `_molt_r14_front.png`, `_molt_r14_tq.png`; `stance_r14.txt` (act_molt) |

**Clip floor: min(8.5, 8.5, 8.5, 8.5) = 8.5. APPROVED for the clips.**

## 3. Round-14 items (PASS / PARTIAL / FAIL)

| r14 item | result | evidence |
|---|---|---|
| MUST 1. Hood rim `OBS_D` -> `PALE_S` (222, 194, 158); size unchanged | **PASS.** Built as stated (the `B.seg` rim with `PALE_S`, r14 comment; size 0.018 and offset `HOOD_T/2 + 0.008` unchanged). The hood clearance is unchanged (HOOD\|Head min 0.0509 idle f96). From the game camera the red fan has a light edge and is separate from the dark frill; from the front the pale rim reads as a piped edge, not a toy outline. The fallback (lower the hood top 0.03) was not needed. 64 px: PASS on the builder's proof and by eye (a light band under the dark head), not zoomable here. | `pets/CinderOverlord.py` ~386-405; `gamelook_game.png`; `_hood_back_2x_idle_f0_f20.png` (game row); `close_front.png`; `CinderOverlord_icon.png` |
| MUST 2a. Report `Crown_3\|Head` (and `Crown_1..5\|Head`) with frame and clip; pass >= 0.02 | **PASS.** Reported in `gate_f85.json` `collision_proof_r14.crown_vs_head_all_frames`: Crown_1 0.1813 (act_molt f110); Crown_2 0.1661 (act_molt f26); **Crown_3 0.0527 (roar f44)**; Crown_4 0.1661 (act_molt f32); Crown_5 0.1813 (act_molt f110). All >= 0.02. This matches `coll_probe_r14.txt` (BLADE_1..5\|Head). The blade measure excludes vertices within 0.07 of the hinge, which sit in the mount by design; accepted as a hinge, and the sockets are not visible in `close_front.png`. | `gate_f85.json`; `coll_probe_r14.txt`; `_close_sheet.png` |
| MUST 2b. State the shipping portrait; the shipped icon's area >= 0.372 | **PASS.** `shipping_portrait`: `CinderOverlord_portrait_raw.png` -> icon `CinderOverlord_icon.png`; gold 117 (floor 103), area 0.378 vs Thunder Rex 0.372. The alt (`CinderOverlord_portrait_alt.png`, area 0.369) is labelled "not shipped" in the gate file and in `_icons_alt_strip_*` (`Cinder alt (notshipped)`). It is not in the outclass claim. | `gate_f85.json` (`shipping_portrait`, `gold_gate`, `area_gate`); `_icons_alt_strip_64.png`, `_icons_alt_strip_128.png` |
| 5 (r14). Gate file clean: no stale "91"; one gold counter | **PASS.** `grep -w 91 gate_f85.json` is empty. `gold_gate` = 117 is the only gold number. | `gate_f85.json` |
| Carried NICE (r13 NICE 1, 2, 3, 4): roar hood spread, roar gap 47.5 px, snout top dome, hood side slab | **Open, not blocking.** See NICE 1-4. | see section 6 |

## 4. Model score: 8.5 - APPROVED

**Holds:**
- The round-14 blocker is fixed: the hood is a light-edged red fan, separate from the dark frill and crown from the game
  camera, the front, the 3/4 and the icon. The hood clearances are unchanged (min 0.0509).
- Crown: five blades; neighbours >= 0.0357; all crown-to-head clearances reported and >= 0.02; kit gold 117 and area 0.378,
  outclassing Phoenix (93 gold) and Thunder Rex (0.372 area).
- Front face: tapered snout, nostrils, fierce brows and slits, no glints, no smile.
- Gates reproduce from the files: kit collision true (85 pairs); strict run only the two shoulder seats (0.0277 max, not
  visible); ground -0.006; loops 0 / 0; stride 5.0089; HEIGHT 11.72 (accepted); tris 13,580 (<= 15k); head + crown share
  0.320 of the whole figure (`headshare_r14.txt`: head 140.3 px of figure 438.5 px); game area 0.212; paws 0.388 / 0.164
  past the body outline.

**Does not block 8.5 (carried NICE, see section 6):** the roar hood does not spread; the roar game gap is 47.5 px; a
small dark plate of the hood edge-on at jaw height (`_close_sheet.png` panel 2); a round dome on the top of the snout
from the front. Also the 64 px hood is a light band, not a wide fan. The score is at the floor, so the NICE items are
the next gain, not a gate.

## 5. MUST list (model and clips)

**None.** The round-14 blocker is resolved, the round-14 proof items are reported, and every gate passes. Model 8.5, clips 8.5.

## 6. NICE list (not blocking)

1. **Roar hood spread (r12 NICE 1, r13 NICE 1, carried).** The hood is rigid on the neck; `roar()` (lines 795-813) has no
   hood keys. Give each side its own hinge (`Hood_L` / `Hood_R` off Neck3, built in `cobra_hood()` ~lines 386-405) and roll
   it outward 10-15 deg from f14 to f30, back to rest by f58. Re-run HOOD\|Head (>= 0.02). This is the cobra threat move
   and the largest single gain for the roar.
2. **Roar game head gap 47.5 px (observed; not gated).** The roar head key `head = [(0,0),(14,10),(26,8),(44,8),(58,1),(66,0)]`
   (~line 800) holds at 8 deg through f26-f44. Raise the 26-44 hold to 10-11 deg, or deepen the f14 gather to -14 deg
   (`gather`, line ~799), so the closest beat reaches 50 px. Re-measure with `stance_probe.py`, or set a roar gate at 50.
3. **Hood side slab (r12 NICE 2, r13 NICE 4, carried).** From the side (`_close_sheet.png` panel 2) the Neck2 hood panel
   is an edge-on dark plate at jaw height. Taper its outer edge in `HOOD_PANELS` (lines 339-341) so it reads as a fan
   from the side. Re-check HOOD\|Head and HOOD\|Jaw.
4. **Snout top from the front (r13 NICE 3, carried).** The muzzle top is still a small round dome. Lower the 0.82 station
   height in `SKS` (line 509) from 0.066 to 0.054. Side profile unchanged; re-check the nose clearances.
5. **Idle sway at phone size (r11 NICE 3, carried).** Roll 2.2 -> 3.0 deg per neck bone (~line 761) and head counter-roll
   -4.4 -> -6.0 (~line 762). Keep the head level; the game gap must stay >= 50 px.
6. **Claws at game size (r12 NICE 5, carried).** `PAW_CLAW` 0.110 -> 0.130 (~line 213).
7. **Stale comment and reference (new).** The `act_molt()` docstring still says "the neck arches 22.5 deg", and
   `CinderOverlord/ANIM_REFS.md` (act_molt line) still says "22.5 deg ... 7.5 per bone". The code is now -9 total, 3 per
   bone (lines 822-837). Update both so the next reviewer does not read the old intent.
8. **Thin area margin (new).** Kit area 0.378 vs Thunder Rex 0.372 (+0.006); at 128 px it is 0.377 vs 0.374. Re-measure
   the shipping icon after any crown, hood or silhouette change, and do not trade crown area away.

Waived or not scored (lead ruling): the walk-tile tail crop, palette hygiene, breath (Studio check), the Cinder width rule
(serpent), HEIGHT 11.72 and hood width (accepted), the two shoulder seats (accepted), the crown blade hinges (accepted).

## 7. Pass / fail checklist

| check | result |
|---|---|
| Model >= 8.5 | PASS (8.5) |
| Clips, every clip >= 8.5 (lowest clip) | PASS (idle 8.5, walk 8.5, roar 8.5, act_molt 8.5) |
| Game silhouette reads a hooded, crowned cobra at phone size (owner core test) | PASS (`gamelook_game.png`, `_hood_back_2x` game row) |
| Hood red fan separate from the dark frill and crown (game camera) | PASS |
| Hood reads at 64 px (light band under the dark head) | PASS on proof and by eye at native size; not zoomable here |
| Front / 3/4 read: hooded, crowned cobra-dragon | PASS |
| Front face: tapered dragon snout, not a pig nose | PASS (top dome NICE 4) |
| Fierce eyes and brows; no glints; no smile | PASS (`_close_sheet.png`, `_cv_roar_front.png`) |
| Hood clean: no floating panel, gap or poke (all frames) | PASS (side slab NICE 3) |
| Hood clearance >= 0.02 to every part | PASS (min 0.0509, head) |
| Gold >= 103 at 64 px, one counter | PASS (117) |
| Gate file: no contradicting gold figure ("91") | PASS (grep empty) |
| Outclass Thunder Rex on kit area (>= 0.372) | PASS (0.378; thin, NICE 8) |
| Outclass Phoenix / Ivonrath / Thunder Rex / Cosmic Leviathan on kit gold | PASS |
| Shipping portrait and icon stated; alt labelled "not shipped" | PASS |
| Tris <= 15k | PASS (13,580) |
| Stride 5.0089; ground >= -0.02; loops 0 / 0; linear 0 | PASS (5.0089; -0.006; 0 / 0) |
| Kit collision (joint-aware, 85 pairs) | PASS (true) |
| Strict run: only the two shoulder seats, depth <= 0.028 | PASS (0.0264 rest / 0.0277 max) |
| Crown neighbours >= 0.02 in all clips | PASS (0.0357) |
| Crown blade to head >= 0.02 in all clips (Crown_1..5) | PASS (min 0.0527, Crown_3 roar f44) |
| Paws >= 0.10 BU past the neck outline (both sides) | PASS (0.388 / 0.164) |
| Paw-to-neck >= 0.02 | PASS (0.148) |
| Head + crown >= 0.30 of figure height | PASS (0.320) |
| Game area >= 0.18 | PASS (0.212) |
| Neck <= 7.5 deg per bone | PASS (max 4.0 roar, 3.0 molt, 2.45 idle) |
| Chest vs spine <= 5 deg | PASS (4.5, act_molt) |
| Head + neck pitch-up <= 30 deg | PASS (max neck sum 12 + head 4 at roar) |
| Game head gap >= 50 px: idle / walk / act_molt | PASS (50.7 / 61.8 / 52.5) |
| Game head gap >= 50 px: roar | Observed 47.5 px (no gate set; NICE 2) |
| No head shakes; acts in place; ends at rest | PASS |
| ANIM_REFS cited for every clip | PASS (idle D3+C1; walk D1-D2+U1-U4; roar #3+#6; act_molt #9+U1); stale molt line (NICE 7) |
| Shoulder seats not visible in any render | PASS (accepted) |
| Palette hygiene; breath; walk-tile crop; width rule | Not scored (lead ruling) |
| HEIGHT 11.72; hood width \|x\| 0.64 | Accepted (lead ruling) |
