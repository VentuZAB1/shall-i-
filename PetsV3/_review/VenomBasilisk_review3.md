# Venom Basilisk - art director review 3 (2026-10-14) - MODEL APPROVED; idle / walk / act_dash APPROVED; roar: one key change

**Model: APPROVE, 8/10 for a 5% rare** (v1 5/10, v2 7/10). Fixes 1-4 from review 2 all landed, and so did 5, 6
and 7. The mesh is locked: don't touch it unless the owner asks.

**Clips:**
- idle, walk and act_dash: approved.
- roar: approved with **one must-fix**. The frill flare, the pet's hero moment, is exactly edge-on from the game
  camera at the roar peak, and the raised head hides most of it from the front. The fix is a single counter-rotation
  of the Frill keys. I tested it in memory with your code (numbers and image below). Once it's in, Venom Basilisk is
  signed off.

What I looked at:
- `pets/VenomBasilisk.py`, diffed against `_tools/rex_versions/VenomBasilisk_v2r2.py`
- all the sheets you listed: model, flank, close, frill-back, icon strips, the three pose sheets, the pclose and
  pclose-roar sheets
- the single pose frames for walk, idle and dash f16
- my own renders, made outside the project:
  - I rebuilt the model, rig and all 4 clips in memory (no `write_clips`, no portrait; I checked that nothing in the
    project changed)
  - posed head and body views at 600 px of idle f0, roar f12/20/24/40 and dash f30/f60
  - the f60 frill flare from the front and from behind
  - a measured world lean of the frill per frame

---------------------------------------------------------------------------------------------------------------------
## 1. Review-2 fixes - sign-off

| fix | status | checked in |
|---|---|---|
| 1 Frill outline | **PASS** | Seven points, all with bone tips, from the front (model sheet) and from behind (`_frill_back_sheet`). At the f60 flash the outer groups spread +15° and there is **no hole** from the front or from behind. The visible boundary panels 30→58 and the hidden 15→30 under-flaps work as intended. |
| 2 Belly + stripes | **PASS** | The teeth tuck under the shell lip with no hide gap and stop above the pale under-shell. The underside is now one cream form per block, with scute gaps; the small steps between the chest, waist and hip shells read as belly plates. PALE+PALE_D is 5.8% (flat ID, side) against my 7% target. I accept that: the belly read is clearly there in `_flank_sheet` and the side view. The optional fallback (raise the under-shell top to `-0.45·h.z`) would add about 1%. |
| 3 Sail | **PASS** | Fanned 8→33°, deep-violet ribs, ivory points clear, a pointed violet edge. It reads as a spined sail, darker and lower than the frill. No grille. |
| 4 Tongue | **PASS** | Seg, forks and joint at z 0.703. It slides out at the lip line: idle f38 with the jaw at 3° (fork visible), and roar f24 with the jaw at 36° (a long forked tongue). |
| 5 Snout cleanup | PASS | Nostrils only. Cosmetic: the comment on L257 still says "rostral notch". |
| 6 Shell seams | PASS | The SEAM bars break up the slabs from the game camera. |
| 7 Venom glands on Head | PASS | In roar f24 the cheek mass stays with the skull while the jaw drops. |

**Value shares (official flat-ID measure):**
- side: HIDE 35 / DORSAL 32 / violet 17.4. In range.
- game: DORSAL 45 / HIDE 26 / violet 17.4. A dark back from above, as intended.
- I measured 69% of the violet on the frill from the game camera in v2, and the frill is unchanged since.
- Icon strips: at 64 and 128 px it is clearly the most striking pet in the Grass egg, and the lilac crown reads
  separately from the darker sail.

---------------------------------------------------------------------------------------------------------------------
## 2. Clips (30 fps)

Your audits are clean: linear 0, loops closed, foot drift and slide 0, `collision_free` true, ground_min ≥ -0.006.
All four clips cite their references (Sophocleous walk, Sea Beasts roar).

### idle (120 f) - APPROVED
- The look-around is Neck 8 + Neck2 7 + Head 10 = 25° each way. That reads from the game camera, as idle f38 shows.
- Two tongue flicks with the 3° jaw crack, a frill twitch, a tail S-curve, all four feet planted.
- Limits hold. No head shake: one slow look each way with long holds.

### walk (32 f) - APPROVED
- Diagonal pairs; the S-sway comes from Spine yaw ±8 with the Chest countering 4 (≤ 5) and the Neck countering 3,
  so the head stays nearly steady.
- The head dips after front contact; the tail lags 0.25; the sprawled feet arc out.
- The game-camera frames f0/8/16/24 show a readable lizard S.
- It runs 32 f where the reference note says ~45 f. A quick lizard trot is right for this animal, so keep it.

### act_dash (104 f) - APPROVED
- **It matches the beat table**: lock-on with the frill folded flat → rear to -36 → 5 hind steps (L/R/L/R/L) with
  the head world-locked by the roll counter → skid at -44 → slam at f55 → flash (frill -8 by f59, overshoot -11,
  outer groups +15, jaw 18, quiver) → diagonal-pair backpedal → settle with a tongue flick.
- **Silhouette.** From the side it reads as a real basilisk dash: upright trunk, tucked forearms, tail a straight
  counterweight. From the game camera the body becomes a tall dark shape with the tail whipping, and the frill is
  folded edge-on as a blade, which is what the design calls for.
- **Flash.** The flash is the best frill moment in the set: lean 9.6°, game-cam facing 0.61 (rest is 0.46).
- **Tail1 counter-pitch.** 40 in the sprint and 46 in the skid is the right call over my table's 30, since it
  keeps the tail off the floor.
- **Limits:**
  - Neck: -4/+6.
  - Chest: 2 ± 1.
  - Head: pitch-down only relative; the snout ends 14-16° above level in world.
  - No head shake; the counter-roll keeps the head still in world space.
- **Footprint:** 0.62 out and back, as specified. Events: launch f20, stomp f55, frill_flash f58, venom_drip f60.
- **Polish (optional):** add the same 3° Jaw crack to the act's two tongue flicks (Jaw 3 at f5-9 and f98-102,
  0 at f4/f10/f97/f103). Today the tongue slides out with the jaw shut, partly through the lip; it is invisible at
  game scale, but it would match the idle.

### roar (72 f) - APPROVED WITH ONE MUST-FIX: counter-rotate the frill at the peak

**Measured** (centre-spine lean in world, back = +; game-cam facing = how square the fan's back face is to the
follow camera, 1 = square, 0 = edge-on):

| frame | lean | game-cam facing |
|---|---|---|
| rest / idle f0 | 20.6° | 0.46 |
| roar f12 (gather) | 15.6° | 0.53 |
| **roar f20 / f24 / f40** | **47.6 / 49.6 / 50.3°** | **0.03 / 0.00 / -0.01** |
| dash f60 (flash) | 9.6° | 0.61 |

**Why it happens:** the roar raises the head ~35° in world (Spine 6 + Chest 3 + Neck/Neck2/Head 26). The frill rides
on the head, so the flare (-4/-6) is cancelled and the fan ends up ~50° back. From the follow camera it shrinks to a
thin violet slab (`_pose_game_sheet` roar f24). From the front the raised skull hides it (`_pclose_roar_sheet` front
f24). The roar is the frill's reveal, so this is the one place it must read.

**Fix (only the Frill "back" values; everything else stays):**
- K row f20: frill back **-4 → -30**.
- K rows f24 and f52: **-6 → -32**.
- Hold loop (L557): `frill(k, f, -32 + 1.5 * w, 15 + 2 * w)`.
- Keep f8/f12 at +10 (fold back) and f58 at 0. The fold-then-snap is now +10 → -30 over f12-20, a 40° snap,
  which reads as a real flare.

**Verified in memory with your code:**
- roar f24 lean 49.6° → **23.6°**, game-cam facing 0.00 → **0.42** (about the same as rest).
- From the front the fan now frames the raised head as a full crown.
- In a side close-up the frill clears the horns and the skull.
- See `VenomBasilisk_r3_roar_frill.png`: current on the left, fixed on the right, in game, front and tq.

`check_pairs` has no Frill-vs-Head pair because Frill is a child of Head, so look at the f20-52 frames by eye; my
f24 check was clean.

**Send:** roar f20/f24/f40 from the game camera and the front, plus the `collision_free` / ground_min line. If those
match the right-hand column of my comparison, consider Venom Basilisk **signed off** with no further round. I'll
confirm in a short 3b note.

---------------------------------------------------------------------------------------------------------------------
## 3. Summary for the coordinator
- **Model:** approved, 8/10. Fixes 1-7 are done; the mesh is locked.
- **Must-fix:** roar frill counter-rotation (the 4 values above).
- **Optional:**
  - a 3° jaw crack on the act's tongue flicks
  - the under-shell top at `-0.45·h.z` for +1% PALE
  - the stale comment on L257
- **Owner to-do after sign-off (as for all pets):**
  - Studio import as creator ZAB Studio
  - VFX Studio effects on the events (frill_flash, venom_drip on the Venom anchor, stomp, roar)
  - Save + Publish
