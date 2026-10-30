**Model: 8.5/10 - PASS. Clips: 8.5/10 - PASS.**

# Wraith Hound - FINAL 8.5 GATE, round 6 (socket fix check + per-clip scores) - 2026-10-28

Fresh reviewer. Read: `_review/GLACIER_REVIEWER_BRIEF.md`, `_review/WraithHound_final85_r5.md`, `WraithHound/MODEL_NOTES.md` (Round 9), `WraithHound/CLIP_NOTES.md` (Round 9).

Looked at (all opened and loaded): `renders/_idle_sheet_r9.png`, `_walk_sheet_r9.png`, `_roar_sheet_r9.png`, `_act_sheet_r9.png`, `close_front.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `_model_sheet.png`.

Also checked: `pets/WraithHound.py` lines 168-177 (socket, slit, pupil, brow), `_scratch/fc_r9.txt`, `_scratch/export.log` (HEADLESS_RESULT), `ANIM_REFS.md`. I measured the icon eye pixels myself with a numpy PNG reader, in memory only; no files were written except this review.

Caveats: the sheets are shown at reduced size and I could not zoom into single frames, so the motion scores rest on the sheets plus the measured metrics (same limit as round 5). Colours were not scored (owner's lavender decision).

## Socket fix: PASS

| check | result | evidence |
|---|---|---|
| Socket widened | PASS. Line 169 is now `(0.054, 0.008, 0.030)` (r8 was 0.050). | `pets/WraithHound.py` L169 |
| Black frame back in close-up | PASS. Dark frame visible round both blue slits at the outer edges. | `renders/close_front.png` |
| 64 px eye count (floor 6) | PASS, exactly 6. Box x16-30, y24-36 of the first icon, mask b-r>70 and b>120. Pixels at (16,28), (21,29), (21,30), (22,29), (22,30), (23,29). | `renders/_icons_strip_64.png` |
| 128 px eye count (floor 16) | PASS. My box x32-60, y48-72 gives 19. Builder says 21 (box choice differs). Both above 16. | `renders/_icons_strip_128.png` |
| No collisions, tris | PASS. `collision_free` true, collisions `{}`, tris 6,820, no glow meshes (`tris_glow` `{}`). | `_scratch/fc_r9.txt`, `export.log` |

## Per-clip scores (the lowest sets the clips score)

| clip | score | why | evidence file |
|---|---|---|---|
| idle (120 f loop) | 8.6 | Calm hold with a readable nose-lift beat (8.0 deg, visible in the game row at f60). Quiet limbs (local max 0.82), neck 3.5, chest vs spine 0.6, no pops. The sniff and ear-flick beats are small at sheet scale. | `renders/_idle_sheet_r9.png`; CLIP_NOTES r9 table |
| walk (36 f, 1.2 s) | 8.5 | Diagonal trot, feet planted, head low and level, slide 0. Lowest score because the paw lift is 0.045 (about 0.32 studs, roughly 3.6 % of the 9-stud height), the smallest clearance of the four clips, and it reads close to a shuffle at 5 studs. Knee steps are 5.49 against the 5.63 target. Cadence is not marked (lead ruling). | `renders/_walk_sheet_r9.png` |
| roar (60 f) | 8.6 | Jaw opens and closes clearly in the TQ row (f20-f44); the mane rows lift and splay. From the game camera only the mane flare reads, the snarl does not. Ends at rest (f59 vs f0 = 0.0). | `renders/_roar_sheet_r9.png` |
| act_smokecloak (100 f) | 8.6 | Crouch at f16, cloak fan f44-f70 reads as a wide cape from both views, rises f84, ends at rest (f100 vs f0 = 0.0). Events in place. The 6.4 deg/frame cloak-fan mane (non-limb) is not a rule breach. | `renders/_act_sheet_r9.png` |

**Clips: 8.5 PASS** (walk is the lowest).

Clip gate metrics (CLIP_NOTES r9 and `fc_r9.txt`), all within the brief's limits:
- Neck max: idle 3.5, walk 4.0, roar 4.0, act 5.0 (limit 8).
- Chest vs spine: 0.6, 2.92, 1.5, 1.5 (limit 5).
- Head pitch-up: 8.0, 0, 0, 3.5 (limit 30).
- Loops closed (idle, walk); ground min 0.004 in all clips; linear 0; 0 quaternion flips; no airborne spins; `collision_free` true.
- ANIM_REFS rule: met. `ANIM_REFS.md` cites W0 for the walk and snarl, and records the 36 f choice against W0's 27-30 f with a 30 f fallback.

## Model: 8.5 PASS

Holds at the floor. The socket regression is fixed and the icons read as a fierce, studded hound with a blue plume and a blue eye at 64 px. It is not higher because two round-4 9+ items are still open (accent split, close-up slit ratio, both below).

## New MUSTs

None. Nothing blocks 8.5 on the model or on any clip.

## TO 9+ (not blocking)

1. **Accent at 64 px.** The plume still shows two blue elements (centre tip and a side streak). Split the Mane2 side tips (`pets/WraithHound.py` around L93-94, the `wisp(...)` call with `tipcol=INDIGO`): `d0 x` 0.40 to 0.46 on the `_L` and `_R` side wisps only. Accept only if `close_front.png` shows no front wings and the 64 px plume shows three separate blue elements. Eye stays at 6 or more.
2. **Close-up eye slit.** The slit is 0.046 x 0.025 (L173), a 1.84:1 ratio. At close range it reads as a blue panel inside a frame, not a narrow slit. Owner's call, since a narrower slit (about 2.5:1) costs the 64 px eye count.
3. **Pupil code (L175-176).** The notes say it never renders. Delete the block or make it visible. No score effect.
4. **Walk paw lift.** Lift 0.045 gives about 0.32 studs of clearance. Test 0.050-0.055 with the walk knee-step check: keep it only if the walk limb local max stays at or below 5.63. Otherwise keep 0.045.
5. **Owner decision, not scored:** the darker lavender (round 5 watch item).

## Pass / fail checklist (round 6)

| check | result |
|---|---|
| Socket frame restored (R1) | PASS |
| 64 px eye >= 6 | PASS (6) |
| 128 px eye >= 16 | PASS (19 mine, 21 builder) |
| Collision, poke, intersect | PASS (none) |
| Tris <= 15k (6,820), no glow | PASS |
| Clip pose limits (neck, chest vs spine, pitch-up) | PASS |
| Loops, ground, flips, linear, ends at rest | PASS |
| ANIM_REFS rule | PASS |
| Accent: three separate plume elements at 64 px | NOT DONE (TO 9+ #1) |
| Close-up slit narrow | NOT DONE (TO 9+ #2, owner call) |
