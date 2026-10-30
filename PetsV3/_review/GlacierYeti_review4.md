# Glacier Yeti - clip gate review 4 (2026-10-27) - APPROVED WITH FIXES (clips)

**Score: 8/10.** Ship at 8/10 or better, once the one verification item below is done.

Every review-3 MUST is now resolved. One of them was my error: the walk gait was already correct, and I withdraw my MUST 1. The one open item is verification only. The beat and model renders are older than the last pet, JSON and Lua write, so they do not yet show the final files. No motion change is needed.

## Correction: review-3 MUST 1 (walk gait) withdrawn

I read the offsets in `legs` as the order in which the feet step. They are phase leads. In `pets/GlacierYeti.py` (`PetsV2/petkit.py` L590-600), `gait_target` uses `t = (f/n + offset) % 1`, and a foot touches down where `t = 0`. So a limb with offset `o` touches down at `f = (1 - o) * n`, not at `o * n`.

Checked two ways:
- **From the offsets and `gait_target`:** Leg_L f0, Arm_R f12, Leg_R f24, Arm_L f36 (matches `_scratch/footfalls.txt`).
- **From the baked clip data (`GlacierYeti.json`, walk, pitch of each limb):**
  - Arm_R peaks at f12, the forward-most point, and then sweeps back to its minimum at f42. Stance is 30 f (duty 0.62 of 48).
  - Arm_L peaks at f36 and has its minimum at f18.
  - Leg_L has its minimum at f30 (lift-off) and peaks at f43, so it touches down at f0.
  - Leg_R peaks at f18 (end of its swing) and stands on the ground f24-f54.
  - Each limb's stance is 30 f and each swing is 18 f.

So the order is LH f0, RF f12, RH f24, LF f36. That is the diagonal sequence of Muybridge plate 747, and the walk stays as built. The stills (`_beats_rw_side.png`, `_beats_rw_tq.png`) show one fist planted per 12 f in that order. The L/R labels are not readable in the stills, so the left and right identities come from the JSON, not from the images.

## Review-3 MUST list: status

| # | Item | Result |
|---|---|---|
| 1 | Walk gait | WITHDRAWN (my error). Diagonal LH, RF, RH, LF is correct. |
| 2 | Front crust icicle | PASS. `model_side.png` shows the front icicle gone, with one small spike at the back-lower edge, pointing out and back. Code: one rim icicle, `(s*1.0, 0.30, -0.15)`, L202. |
| 3 | Shelf 2 back | PASS. In `model_side.png` the pale slab sits at about x 295-380, behind the chest line. Code: `Ua` y +0.14, L213. It still reads as a pale slab on the mid-flank, not as a chest pocket. |
| 4 | Neck limit (lead ruling: Option B) | PASS under the head + neck ≤ 30 rule. Head joint maxima from the JSON: idle 6.68, walk 6.03, roar 22.55 (f22), act 16.0. Armature pitch-up: roar 20.1, act 4.1. |
| 5 | ANIM_REFS / central refs | PASS on the citations. Walk cites 1014 #4 (Dragon Walk Cycle), with Muybridge kept as the frame study. Roar and skid cite Kaiju No. 8 #257646 and W0 #174333, plus the earlier refs. The stepped frames are not in the files (see NICE 1). |
| 6 | Plate vs Jaw pairs | PASS. `check_pairs` L267 includes `("Plate_L", "Jaw"), ("Plate_R", "Jaw")`. `full_step1.txt`: collision_free true, collisions {}. |

## Numbers I checked in the JSON (all match the notes)

- **Roar jaw:** opens from about f12 to peak -26 at f28, holds to about f44, then closes. This matches the W0 timing in ANIM_REFS.
- **Skid jaw:** rest is -1 to -6, with a gasp to -17/-18 at f58-60. Only the brake gasp opens wide.
- **Idle:** plates lift about 5.5 deg (builder says 6 deg, twice). Chest breath about 2.8 deg. Head drops to -6.4 at f55-75.
- **Idle and walk jaw:** -1 to 0 (breath only).
- **Skid drop:** spine reaches -12.5 deg by f7, and the shoulder reaches 34 deg by f8. This matches the keys at f7 in the final pets file (L429-434) and the "lands by f7" claim.
- **One-shot ends:** residuals 0.06 deg (roar) and 0.23 deg (skid) from the bind pose.
- **Chest vs spine:** max 4.39 deg (skid). Largest one-frame swing 9.4 deg (Arm_R, act f78).
- **Walk:** end-vs-start 0.00 (loop closed). Slide 0.
- **Events:** clip-length fractions, for example stomp 0.5 x 48 = f24 (Leg_R touch-down), roar 0.4 x 61 = f24. These match CLIP_NOTES.

## Items still open

### MUST (verification only, no motion change)

1. **Re-render the sheets from the final files.** `renders/model_side.png`, `_model_sheet.png`, `_beats_rw_side/tq.png` and `_beats_act_side/tq.png` are stamped 17:55. `pets/GlacierYeti.py`, `GlacierYeti.json` and `GlacierYeti.lua` were written at 21:57, and `ANIM_REFS.md` / `CLIP_NOTES.md` at 21:58. The skid drop timing and the Plate-Jaw change are in the 21:57 files, so the 17:55 beat sheets predate them. Send the sheets stamped after 21:57, or confirm that nothing visible changed. The clip gate passes on the JSON numbers, but the stills should show the files we ship.

### NICE

1. **Save the frame-step evidence.** The Kaiju No. 8 #257646 and W0 #174333 contact sheets are not in `_scratch` or the renders. Saving them lets the next reviewer check the stepped timings without the site. Put them in `GlacierYeti/_scratch/refs/`.
2. **Stomp anchor.** `FX_SnowPuff` is on `Chest`, but the stomp is the Leg_R touch-down (f24). Anchor the puff to `Foot_R`, so it appears at the foot that lands.
3. **Neck overlap.** `collisions_raw_no_hinges` shows the Head and Chest overlapping for 49-76 frames per clip. That is the neck-sleeve hinge (r 0.18), exempted by design, and I accept it. Check one close side view at the roar peak (f22, head pitched up 20 deg) for a visible gap or clip at the neck.
4. **Idle to walk cross-fade.** The 0.2 s cross-fade in `CreatureAnimator` is accepted from the notes. I could not check it from these files; please confirm in the runtime test.

## Checklist (clip gate, round 4)

| Check | Result |
|---|---|
| Collision-free (with the neck-sleeve hinge), ground ≥ -0.02, linear 0, loops closed, walk slide 0 | PASS |
| Chest vs spine ≤ 5 | PASS (max 4.39) |
| Head + neck pitch-up ≤ 30 (lead ruling: no Neck bone, Option B) | PASS (max 22.55) |
| No head shakes | PASS |
| No airborne spins | PASS (no flight) |
| Acts in place (root net 0) | PASS |
| Acts end at rest | PASS (residuals ≤ 0.23 deg) |
| Walk is the diagonal gait (LH, RF, RH, LF) | PASS (see correction above) |
| Readable beats: skid (drop, sled, slide, dig, rise), roar (lift, jaw open) | PASS |
| Crust and icicles clean in profile | PASS |
| Plate vs Jaw collision checked | PASS |
| ANIM_REFS rule: 1-3 animationreference.org clips, cited | PASS on the citations (NICE 1 for the evidence) |
| Renders match the final files | OPEN (MUST 1) |
