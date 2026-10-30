# Wraith Hound - sign-off check, review 4 (2026-10-27) - ONE MUST LEFT

**Score: 8.5/10.** The round-3 fixes landed. One small timing MUST remains, then sign-off.

## Round-3 items

| item | result |
|---|---|
| M1 refs: site clip W0 (`/tags/wolfs-rain`, #30) and the tags tried | **accepted.** The site clip was opened (counter 5 to 4), the tags are listed, and the frames were read off the same Sakugabooru #174333 file the player streams. Acceptable. Note for next time: keep the Browser pane visible so the site player can step frames itself. |
| M2 one swept plume | **accepted.** In `crop_mane_side.png` the crest now reads as one swept soot mass with a blue point line along the top. Back and outer-low tips are soot (`tipcol=SOOT`, L81 and L87). Centre and side tips stay indigo. |
| M2 indigo share (3.5 % side, 6.1 % game) | **enough.** The game-camera share meets the plan's 6 %. The accent still reads on the crest tips at 128 px (`_icons_strip_128.png`) and in the eye slits. The side-view share is lower, but the player never sees that view. |
| NICE 3 narrower rest wings | **done** (d0 x 0.55 to 0.40, L84). From the front the rest pose is a crown, not wings (`crop_mane_front.png`). |
| NICE 3 fan width | **done.** Act roll 52 to 60 deg; the data peaks at 62.9 with the drift (documented in ANIM_REFS). `_fan_front_back_r3.png` shows the fan holding its width. |
| NICE 2 walk knee | **done, smooth.** The Leg bones peak at 5.4 deg per frame and the shins at 9.1 (f0 to 1), but the shins now ease out (9.1, 7.9, 6.9). The "5.6" in the notes is the Leg figure only; correct it. |
| NICE 5 thicker chest plate and belly strip | **done** (plate half-depth 0.030 to 0.046, L134; strip 0.030 to 0.042, L132). In `low_below.png` the plate is rounder but still a pale block from below. Acceptable. |
| NICE idle frame 0 | **done.** Only the rig's rest offsets remain (Jaw 1.5 deg, legs about 0.5 deg), the same as every clip's rest. |
| NICE notes corrected | **mostly.** The walk chest (2.92) is now stated honestly. The roar and act figures match the new JSON. |
| `fullcheck.json` (17:41) | collision_free true, collisions empty, glow empty, tris 6,820, ground minimum 0.004. Re-run after the mane change, so it is current. |

## Remaining MUST

**MUST 1 - the roar jaw must open over 15 f, as the reference says (`pets/WraithHound.py` roar clip, or wherever the jaw key lives).** W0 gives "the mouth opens over ~15 f", and the coordinator's spec repeats it. The export opens the jaw from f14 (-1.5 deg) to its peak at f26 (-25 deg), which is 12 f. ANIM_REFS says "12 f here" and keeps it. That is a choice that contradicts the cited reference.
- Fix: start the jaw track at f11, so it opens over f11 to f26. Keep the peak at f26 so the `snarl` event does not move.
- Re-export, then re-check `jaw pitch` by frame and `ground_min_z`. Nothing else changes.
- If you would rather keep 12 f, write the reason into ANIM_REFS against W0 and tell the owner.

## NICE (optional, not blocking)
1. Zero the roar's last Mane3_R residual (0.49 deg at f59) so the roar ends exactly on frame 0.
2. Correct the walk knee figure in CLIP_NOTES: Leg 5.4, Shin 9.1 (smooth).
3. Define "head pitch-up, world" in CLIP_NOTES. The act shows 3.5 there and 7.0 for neck plus head; both are well inside 30.
