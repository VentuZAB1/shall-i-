# Wraith Hound - clip notes (r9, 2026-10-28)

## Round 9 (per-clip evidence, the per-clip floor rule)
- Per-clip sheets from the final file, each with fixed cameras, the whole pet, game + tq rows and the time in the title:
  - `renders/_idle_sheet_r9.png` (f0-100, every 20 f);
  - `_walk_sheet_r9.png` (36 f loop, every 4 f);
  - `_roar_sheet_r9.png` (f0 / 12 / 20 / 30 / 44 / 54);
  - `_act_sheet_r9.png` (f0 / 16 / 28 / 44 / 54 / 70 / 84 / 100).
- Motion is unchanged since r8. Per clip:

  | clip | chest vs spine | neck | head pitch-up | limb local max | limb armature-space max |
  |---|---|---|---|---|---|
  | idle | 0.6 | 3.5 | 8.0 | 0.82 | 0.44 |
  | walk | 2.92 | 4.0 | 0 | 5.49 | 4.71 |
  | roar | 1.5 | 4.0 | 0 | 3.19 | 2.49 |
  | act | 1.5 | 5.0 | 3.5 | 5.54 | 2.98 |

- 0 quaternion flips. Ground 0.004. Loops closed, walk slide 0.0. collision_free.

---

# Wraith Hound - clip notes (9+ round, r8, 2026-10-28)

## Round 8 (`_review/WraithHound_final85_r4.md` clips NICE)
Per-frame LOCAL rotation steps of every limb bone (`_scratch/walkdump.py`, `clipmetrics.json` `local_max_by_limb_bone`).
- **Walk knee flicks (was Shin_FR 9.06 at f0->f1 lift-off, and Shin_FL 6.55 at the f29->f0 touchdown seam):**
  - The feet use my own `soft_target` / `soft_trot` (same trot pairs, same duty 0.5, the same stance sweep). The pet file only; `cm.quad_walk` is untouched.
  - **Swing path:** fore-aft is a smoothstep (0 speed at lift-off and touchdown). The lift is a smooth trapezoid: its vertical speed eases in and out over 8 % of the swing, so it is 0 at lift-off, apex and touchdown, with a lower peak than sin.
  - At 30 f this already removed the contact flicks: lift-off 9.1 -> 3.3 deg and touchdown seam 6.5 -> 0.7 deg. The fastest step was then the knee folding in early swing (8.3).
  - To get every limb step under 5.63:
    - lift 0.045 (was 0.060), about 0.32 studs of paw clearance;
    - a **36 f cycle** (1.2 s, was 30 f / 1.0 s): a calmer lean trot, stride 0.6 unchanged, meta `walk_len` 1.2.
    - (If the in-game animator speed-syncs the walk to the move speed, the cadence part does not slow the real knee; the softer path and the lower lift do.)
  - Result: walk limb local max **5.49** (Foot_FR f7), Shin max 5.34. Armature-space limb max 4.71 (was 5.63). Walk slide 0.0, loop closed, collision_free.
- **Act Shin_FL f6 (6.76):** the crouch drop is 24 f (was 18) and the rise 22 f (68 -> 90). Act limb local max **5.54** (Shin_FL f84). Events are unchanged (smoke_puff f16, cloak f28, drift f54). The act ends at rest (f100 vs f0 0.0).
- **Gates:**
  - collision_free true, ground 0.004 in every clip, linear 0;
  - loops closed, idle foot drift 0.0, walk slide 0.0;
  - 0 quaternion flips;
  - neck / chest / head-pitch limits unchanged: idle 3.5 / 0.6 / 8.0, walk 4.0 / 2.92 / 0, roar 4.0 / 1.5 / 0, act 5.0 / 1.5 / 3.5.
- Fresh pose sheet: `renders/_pose_tq_sheet_r8.png` (15 frames, rendered 05:24 from the current file).

---

# Wraith Hound - clip notes (8.5 gate round 2, 2026-10-28)

## Round 2 (the clips passed 8.5): TO 9+ item
- The cloak rows are staggered: lift 6 / 4 / 2 deg for Mane1 / 2 / 3; the 60 deg roll and the drift are unchanged.
  The fan no longer reads as a ring from behind (`renders/_fan_front_back_r2.png`, bottom right).
- **Step 1:** collision_free true, linear 0, loops closed, walk slide 0, ground 0.004.
- **Metrics:** neck max 5.0, chest vs spine 2.92 (walk), 0 quaternion flips, roar / act end vs f0 0.0.

---

# Wraith Hound - clip notes (final 8.5 gate fixes, 2026-10-28)

## Final 8.5 gate (`_review/WraithHound_final85.md`): what changed
- **C1:** the roar hold tremble has a 10-frame period (3 Hz, was a 4-frame 7.5 Hz flutter).
  - In the export the Jaw track over f26-44 is a smooth 22.6-24.5 deg wave, at most 0.6 deg per frame, with no
    4-frame pattern.
  - The jaw ramp f11-26 is unchanged (peak f26 = `snarl`).
- **C2:** the roar side wisps splay 12 deg (was 25), so there are no batwing horns from the front
  (`renders/_fan_front_back_f85.png`, middle top).
- **C3:** the cloak's centre lift is 6 deg (was 14); the 60 deg side roll, the 3 f row lag and the two drift cycles are
  unchanged. The fan now widens sideways instead of standing up (`_fan_front_back_f85.png`, right column).
- **Step 1:**
  - collision_free true, linear 0, loops closed, walk slide 0;
  - ground 0.004 in every clip;
  - tris 6,820.
- **Metrics:**
  - neck max 5.0;
  - chest vs spine 2.92 (walk);
  - head pitch-up 8.0 (the idle nose-lift);
  - limb max 5.6 (armature) / 9.1 (local);
  - 0 quaternion flips;
  - roar f59 and act f99 vs f0: 0.0.

---

# Earlier clip notes (review 4)
# Wraith Hound - clip notes (review 4: 8.5/10; the MUST and NICE items applied, 2026-10-27)

**References:** `ANIM_REFS.md`:
- **W0: animationreference.org `/tags/wolfs-rain` #30 (Sakugabooru #174333)**, for the walk timing and the snarl;
- W1: Sheep Dog coyote #143877;
- W2: The Pointer #258150;
- W3: MU display, ANIM_REFERENCES #6;
- W4: ANIM_REFERENCES #4 (site) and #8 (YouTube).

The site tags I tried are listed there.

## Model changes in this round (review 3 M2 and NICE 3 / 5)
- **M2, one plume:**
  - The Mane2 and Mane3 roots are 0.03 higher (z 0.935 / 0.905).
  - The side wisps rise more steeply (d1 z 0.18 → 0.42, L0 0.15 → 0.19 · sc), so their indigo tips sit next to the centre
    tips.
  - The back wisp and the outer-low wisps now end in SOOT, not INDIGO.
  - From the side, the indigo tips form one swept band and there is no third row of points (`renders/crop_mane_side.png`).
  - INDIGO is 3.5 % side / 6.1 % game (was 5.4 / 8.3).
- **NICE 3, front-view wings:** the side wisps' rest splay is narrower (d0 x 0.55 → 0.40). From the front they sit
  behind the head as a crown (`renders/crop_mane_front.png`, `_fan_front_back_r3.png`). The act roll is raised from 52 to
  60 deg so the cloak keeps its width.
- **NICE 5, under-view:** the chest plate half-depth is 0.030 → 0.046 (a rounder plate) and the belly tuck strip
  0.030 → 0.042 (`renders/low_below.png`).
- **Unchanged:** tris 6,820; bones, joints and timing.

## Full check, step 1 (`_scratch/fullcheck.json`)
- **collision_free:** True. The pairs include Mane1 / Mane1_L / Mane1_R against Head and the ears, and Tail1-3 against
  the hind legs.
- **linear:** 0 in every clip.
- **Loops:** idle and walk are closed.
- **Walk:** slide 0.0, foot_z_var 0.0.
- **ground_min_z:** 0.004 in every clip.
- **Stride:** 0.60.

## Clip evidence (`_scratch/clipmetrics.json`, every frame at step 1)
| Clip | Neck max | Chest vs spine | Head pitch-up, world | Limb swing max /f | Any bone max /f | Quat flips (keys / frames) | Last frame vs frame 0 |
|---|---|---|---|---|---|---|---|
| idle | 3.5 | 0.6 | 8.0 | 0.44 | 6.6 (Ear_L flick) | 0 / 0 | f120 0.0 |
| walk | 3.98 | **2.92** | 0.0 | **5.6** (Leg_BR) | 5.6 | 0 / 0 | loop |
| roar | 4.0 | 1.5 | 0.0 | 2.5 | 3.7 (Mane1_L, local) | 0 / 0 | f59 0.0, f60 0.0 (the MF track ends at f54, so the 4 f row lag settles by f58) |
| act_smokecloak | 5.0 | 1.5 | 3.5 | 3.6 | 6.6 (Mane2_R) | 0 / 0 | f99 0.0, f100 0.0 |

- **NICE 2, the walk knee snap:** the walk now carries the body 0.02 lower (Spine z -0.020 - 0.014 · bob), so the legs
  never reach full extension. It was 16-18 deg in one frame on Shin_FL f15-16 and Shin_FR f0-1. The worst steps now:
  - local (keyed / exported bone quaternions, `swing_local_max`): Leg 5.4 deg, **Shin 9.1 deg** (Shin_FR f1);
  - armature space (with the parents' motion, `swing_max_limb`): 5.6 deg (Leg_BR f21).

  Both metrics are defined in the JSON under `_definitions`.
- **"Head pitch-up, world"** (`head_pitch_up_world_max`): the largest rise, in degrees, of the Head bone's direction (its
  y axis in world space) above its rest elevation. The idle's 8.0 deg is the nose-lift beat (-8 deg); the other clips are
  3.5 deg or less.
- **The idle's frame 0 is now the exact rest.** The mane and tail waves are shifted to 0 at f0 (`wv()`). The tail had
  been 7 deg off, which made a pop when the roar or act started from the idle.

## Clips
| Clip | Frames | Loop | Events |
|---|---|---|---|
| idle | 120 | yes | none |
| walk | 30 | yes | none |
| roar | 60 | no | `fog` f14 (0.233), `snarl` f26 (0.433) |
| act_smokecloak | 100 | no | `smoke_puff` f16 (0.16), `cloak` f28 (0.28), `drift` f54 (0.54) |

## Beats (numbers checked against the data, NICE 1)
- **idle, "scent drift" (W2):**
  - The nose lowers 10 deg and sniffs twice, lifts to -8 deg, dips to +5 deg and settles.
  - The ears flick back 14 deg at f40 and forward 8 deg at f80.
  - The mane drifts with a 3 f lag per row and the tail sways down the chain.
- **walk, "lean trot-walk" (W0 + W1 + W4):**
  - Diagonal pairs, stride_half 0.15, lift 0.06, the head low and level.
  - The mane trails 4 f (+1 f per row) and the tail streams.
  - W0's walk cycle is ~27-30 f, so 30 f stands.
- **roar, "mane flare" (W0 + W1 + W3):**
  - f0-12: the rows lift 18 deg (**20 at peak with the 2 deg tremble**) and the side wisps splay 25 deg, 2 f lag per row.
    The ears go back 24 deg, 3 f late.
  - f14-26: the chest pushes forward 0.05H and the head pitches down 10 deg.
  - f11-26: the jaw opens 25 deg over **15 f**, matching W0's ~15 f (review 4 MUST; it was f14-26). `snarl` fires at
    f26 (the jaw peak, unchanged).
  - f26-44: hold with the tremble.
  - f44-60: the mane falls back and the jaw closes.
- **act_smokecloak, "the cloak spreads" (W3 + W4):**
  - f0-18: a flat crouch, the body down 0.20 (0.16H).
  - f18-32 (+3 f per row): the mane lifts 14 deg and the side wisps roll out **60 deg (63 at peak with the drift)**.
  - f40-68: the drift sways ±6 deg over two 14 f cycles.
  - f68-86: the mane folds back and the hound rises.
  - f86-100: the exact rest pose.
  - All four paws are planted in every frame, and the tail lifts 10 deg in the crouch.

## Deviations (accepted in review 3)
- The crouch is 0.16H, not "to 0.75H".
- The fan is wider and lower than the plan's 40 / 40.
- The roar lifts 18 and splays 25.

## Renders
- **`renders/_pose_tq_sheet.png`:** idle 0/30/62, walk 0/8/15/23, roar 12/26/59, act 16/30/47/78/99.
- **`renders/_pclose_tq_sheet.png` and `_pclose_side_sheet.png`:** idle 30/62, walk 8, roar 12/26/59, act 16/30/47/78/99.
- **`renders/_fan_front_back_r3.png`:** rest / roar f30 / act f47, from the front and back.
- **Model, after the M2 / NICE changes:**
  - `renders/crop_mane_side.png` and `crop_mane_front.png`;
  - `_icons_strip_128.png` and `_icons_strip_64.png`;
  - `low_below.png`, `game_view.png` and `_model_sheet.png`.
