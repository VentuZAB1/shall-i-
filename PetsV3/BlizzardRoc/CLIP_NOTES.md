# Blizzard Roc - clip notes (clip round 6 after review 8, builder D, 2026-10-28; PASSED review 9, ship file = the 08:19 export)

Code: `pets/BlizzardRoc.py` (from "fold <-> open waypoints" down). References: `BlizzardRoc/ANIM_REFS.md` (site tags ->
Sakugabooru: #260630 heron takeoff / landing / threat display / droop / wading walk via `/tags/flying`, #236985 via
`/tags/flying`, the `/tags/bird-flight` tutorial; #260711 / #260644 supporting only, not on the site).

## Review 8 fixes (clip round 6) - the walk
- **W3, reference first:** the H1 heron (#260630, 17.85-20.85 s, stepped at 1/24 s) shows NO hold-then-thrust. The
  head advances smoothly and then glides to a stop, at one height. Timestamps and pixel track: `ANIM_REFS.md`, walk
  row.
  - So the review-7 (round 5) thrust bob is **dropped**, and W2 (bob +-5 -> +-7.5) is not applied; it would be the same uncited
    thrust.
  - If you still want a head bob for readability, it is a one-line restore. It would then be a stylisation, not a
    reference beat.
- **W1:** body roll +-3 -> **+-5** and lateral shift 0.02 -> **0.05 BU**, in phase over the stance leg. Docstring
  fixed (it said +-4). At 5 the sway reads as a heavy stalk, not a waddle (the yaw stays +-2 and there is no hop), so
  I did not need 4.5.
- **Crest range** (`_scratch/crest_range.py`: the FROST_V crest-plume pixels in the top 45 % of each 300 px tile,
  centroid per frame, f0-36 every 3):

  | view | x range | y range | target |
  |---|---|---|---|
  | front | **29.3 px** | 5.0 px | x >= 24 (was ~16) |
  | game | 23.2 px | 6.7 px | |

  y stays at 5 px because the thrust is gone (W2 not applied).
- **Limits:** walk Neck 1.1, Chest 0.0, largest step 6.2. Walk slide 0.0, foot_z_var 0.0, ground -0.015, loop
  closed (f36 = f0). Collision-free in every clip. Rest delta 0.00 (idle, land, roar, act_bow). Seam takeoff f36 =
  fly f0, 0.00.
- Sheets: `renders/_pose_<front|game|tq>_walk_sheet.png` (f0-36 every 3, labelled with times).
- **Export:** `C:\cdimp\BlizzardRoc.fbx` re-exported from this build.


## Review 7 fixes (clip round 5)
- **Walk (MUST, was 8.2), a heron stalk.** This is the CURRENT walk (round 6, review 8, replaced the round-5 head
  bob; `pets/BlizzardRoc.py` `walk()`, 36 f = 1.2 s, no hop):
  - the body **rolls +-5** over the stance leg and **shifts 0.05 BU** sideways over it, in phase (round 5 had +-3 /
    0.02); yaw +-2 and a 0.02 contact dip;
  - **head: no hold-then-thrust.** Stepping the H1 heron (#260630 wading walk, 17.85-20.85 s, at 1/24 s) shows the
    head advancing smoothly at one height and gliding to a stop, with no thrust (`ANIM_REFS.md`, walk row). So the
    round-5 thrust bob is gone and review 8 W2 (bob +-7.5) was not applied. The neck chain (Neck 0.2, Neck2 0.2,
    Head 0.35) cancels ~75 % of the body's pitch / roll / yaw, so the head glides level (gyro head);
  - wings folded, with a 0-15 % blend toward LIFT1 on each contact; the tail rides with the hips;
  - Neck local max 1.1 (limit 8), Chest 0.0, largest walk step 6.2 deg;
  - walk slide **0.0**, foot_z_var 0.0, ground -0.015, loop closed (walk f36 vs f0 0.00), collision-free;
  - crest range (front) x 29.3 px / y 5.0 px;
  - sheets: `renders/_pose_<game|tq|front>_walk_sheet.png`, every 3 frames, f0-36.
- **Fly evidence:** `renders/_pose_tq_fly_sheet.png` and `_pose_game_fly_sheet.png`, f0 / 5 / 10 / 15 / 20 / 25 / 30.
- **Step 1, all clips:** collision_free, linear 0, loops closed, ground -0.014 / walk -0.015 / fly +0.377.
  - Largest step per clip: idle 9.0, walk 6.3, fly 8.7, takeoff 30.6, land 36.5 (FX bone), roar 32.6, act_bow 26.6.
  - Neck max 7.5, chest vs spine 4.0. Rest delta 0.00 (idle, land, roar, act_bow). Seam takeoff f36 = fly f0, 0.00.
  - Events: launch 0.389, touch 0.531, roar 0.333, snap 0.527, frostshed 0.2. Tris 12,940.
- **Export:** `C:\cdimp\BlizzardRoc.fbx` re-exported from this build (meta: walk_len 1.2, stride 0.5).

## Review 6 fixes (clip round 4)
- **MUST 1, documentation:**
  - `ANIM_REFS.md`:
    - header now reads clip round 3 (review 5) + round 4 (review 6);
    - walk = 36 f / 1.2 s, deliberately slower than the ~1.0 s reference, with the 0.01 BU lateral shift;
    - takeoff beats: downstroke f13-21, rise f14-22, feet planted to f17 / leave at f18, flight cycle f25-36;
    - R1 / R4 marked "not used by any clip".
  - `pets/BlizzardRoc.py`:
    - the reference header names H1 #260630 (takeoff, land, roar, act_bow, walk, idle) and the R5 Bird Flight
      tutorial (fly); #260711 / #260644 are supporting only;
    - the stale "FOUR plain feathers (no fan)" comments (file header and tail) are fixed.
- **TO 9+ C1, recovery at the fly tempo:** the takeoff is **36 f**. f25-36 key the flight cycle with
  `ph = 1 + (f - 36) / 30`, so f25 is phase 0.633, just past the stroke bottom. The wing climbs about 4-5 deg a
  frame (was 56.5 deg in f21-25), and f36 = fly f0.
  - `launch` = 14 / 36 = **0.389**.
  - Seam (takeoff f36 vs fly f0, every bone): **0.00 deg / 0.000 BU**.
- **N1:** every sheet now has frame + time labels and a render-time footer (`_scratch/clip_sheet.py`):
  `renders/_pose_<tq|game|front>_<takeoff|fly|idle|walk|land|roar|act_bow>_sheet.png`. The takeoff sheets show f0 /
  10 / 13 / 15 / 17 / 19 / 21 / 23 / 25 / 29 / 33 / 36.
- **N2, idle covert stagger: not done.** The covert rows have no bones of their own; they ride Wing / WingTip. A
  per-row stagger would need new bones.
- **Step 1:**
  - collision_free, linear 0, loops closed, walk slide 0;
  - ground -0.014 / -0.015, fly +0.377;
  - largest step 36.5 (land FX bone), takeoff 30.6 (Foot_L f19, the leg release);
  - Neck 7.5, chest vs spine 4.0;
  - rest delta 0.00 for roar, act_bow, land and idle; tris 12,964.

## Review 5 fixes (clip round 3)
- **MUST 1, takeoff seam:** f25-30 now run the flight cycle at the FLY tempo, 1/30 per frame:
  `fly_pose(k, f, 1 + (f - 30) / 30)` + `fly_legs` on every frame, from phase 5/6 at f25 to **1.0 at f30 = fly f0**.
  Check (`FrostcrownDragon/_scratch/rest_delta.py -- BlizzardRoc fly`, the takeoff's last frame against fly f0, every
  bone): **0.00 deg, 0.000 BU** (limit 3 deg / 0.02 BU). The 30.6 deg wing jump and the 0.26-stud drop are gone.
- **MUST 2, launch stretched:**
  - `launch` stays at f14 (the push). The coil still holds f10-14.
  - The first downstroke runs over **8 frames**: wing 36 (f13) -> -8 (f17) -> -36 (f21).
  - The body rises over **8 frames**: z -0.075 (f14) -> -0.01 (f18) -> +0.07 (f22), i.e. 0.145 BU = 0.65 studs in
    0.27 s. Pitch 17 -> 20 -> 24.
  - The feet are planted f0-17 (the knee splay eases out f15-18) and the legs leave at f18. The FK leg tuck is at f20
    and f23. `lift_air_frames` runs f18-30.
  - `renders/_pose_front_takeoff_sheet.png`, `_pose_tq_takeoff_sheet.png` and `_pose_game_takeoff_sheet.png` show
    f10 / 13 / 15 / 17 / 19 / 21 / 23 / 25 / 28 / 30 plus fly f0 (f30 and fly f0 are the same pose).
- **TO 9+, edge-on wings f16-19:** the launch wing keys turn the feather plane 16 deg further (twist 8 -> 24 at f17,
  6 -> 22 at f21). The front sheet shows the feather surface at f17-19, not planks.
- **TO 9+, walk weight:** the cycle is 30 -> **36 f (1.2 s)**, with a 0.01 BU lateral shift over the stance leg (in
  phase with the roll). Walk slide 0.0, foot_z_var 0.0, ground -0.015. The H1 heron walk is ~1.0 s; the slower beat
  follows the reviewer.
- **TO 9+, knee bend in the coil: NOT done.**
  - I tried coil -0.10, -0.09 and -0.08 with the upper trouser block moved back 0.02 and slimmed (top 1.23 -> 1.14).
  - All three cut: Shin vs Spine at f9-10, 82 / 6 / 2 hits. `collide_where`: the trouser cuff (z 0.34-0.51) meets the
    flank skirt spikes on the Spine (z 0.53-0.66, x 0.17-0.26), not the belly.
  - A deeper coil needs the flank skirt shortened (a model change on the approved model). I reverted the trouser and
    kept the coil at -0.075.
- **MUST 3, refs:** #174482 (*Maid Dragon S*) and #256671 (*The Cat Returns*) are Frostcrown references. They do not
  drive any Roc clip, and `ANIM_REFS.md` does not cite them (checked). The Roc walk is H1's wading walk (#260630,
  17.85-20.85 s). They were wrongly listed for the Roc in my earlier report.

## Review 4 fixes (clip round 2)
- **MUST 2, heavy takeoff and landing.**
  - The knees could not go deeper: a hip drop past ~0.08 puts the belly into the feathered trousers (Shin vs Spine).
    This holds even with the knees turned out (I added a knee splay; it helps, but the trousers sit under the belly).
  - So the weight comes from a COIL instead: the hips drop 0.075-0.08, the body pitches forward 17 (chest +4, inside
    the Chest vs Spine limit of 5) and holds.
  - Measured against the rest pose (`_scratch/crouch_depth.py`, H 2.03): hips -3.7 / -3.9 % H, chest -6.2 / -6.3 %, body
    top **-11.9 / -12.0 %**, head -13.4 / -13.7 % (takeoff / land).
  - Takeoff: coil f0-10, **hold f10-13** with the wings at the top, **`launch` moved f11 -> f14** (the push and the
    first downstroke), airborne f16-19, flight cycle f25.
  - Land: touch f17, the same coil f19 and **hold f19-22**, then rise and fold f24-32. Feet planted throughout.
  - Sheets are 400 px a frame in tq, game and front.
- **N1:** the land flare (f6) and the fold key (f24) turn the feathers to the front (twist -28 / -40). From the front
  they no longer read as poles.
- **N2:** the outer tail feathers are fanned to +-12 and shortened 0.74 -> 0.70.
- **N3:** the roar notes now say "head raised ~13 deg in world (the call pose)".
- **N5:** idle foot drift: the NET drift at the loop end is 0 (loop_pos 0). The 0.052 is the peak lift during a re-grip.
- **Rest frames:** roar f60, act_bow f110 and land f32 are 0.00 deg from the ground rest pose (`rest_delta.py`).
  Takeoff ends in the flight cycle (fly phase 0.2).

## Step 1 (`_tools/headless_full.py -- BlizzardRoc - 1`, all frames; round 3)
- collision_free **true**; audit linear 0 on every clip; loops closed (idle / walk / fly loop_pos 0, loop_rot 0);
  walk slide 0.0, foot_z_var 0.0; tris 12,964; tris_glow none.
- ground_min_z: idle -0.014, walk -0.015, takeoff -0.014, land -0.014, roar -0.014, act_bow -0.014, fly +0.377
  (review 2 M5: the talon hooks are modelled 0.031 under z 0, so every planted foot sits FOOT_LIFT 0.017 up).
- Largest per-frame bone step (`_scratch/step_check.py`): 36.5 deg (land f8, the snow-puff anchor); takeoff 30.3
  (Foot_L f19, the leg release); wings max 32.6 (roar snap). Neck / Neck2 local max 7.5, Chest vs Spine max 4.0,
  head + neck pitch-up max 26.
- Rest delta (last frame vs the ground rest pose): roar, act_bow, land and idle 0.00; takeoff f30 = fly f0 (0.00).
- idle_foot_drift 0.052 = the two talon re-grips (each foot lifts 0.06 and sets back on its spot).

## Clips (30 fps)
| clip | frames | loop | events | what it does |
|---|---|---|---|---|
| idle | 120 | yes | `frostshed` f24 | FROST SHED: breath swell; quick 8 f head turns + long holds (yaw +-10 total, R4); f10-40 the wings lift half-open (FOLD -> LIFT1 -> BREATH), shiver the primary tips 4x (frost falls, FX on FX_FrostTrail_L/R), fold back; f60-84 the tail lowers 6 and back; talon re-grip L f88-94, R f104-110 |
| walk | 36 | yes | - | HERON STALK (1.2 s), no hop: roll +-5 / yaw +-2 and a 0.05 lateral shift over the stance leg, the head gliding level (no bob), 0.02 contact dip, gyro head, wings folded (0-15 % toward LIFT1 on contacts), passing foot swings 0.06 wide of the keel; stride 0.5 |
| fly | 30 | yes | - | R1 + R5: stroke top 36 (high V) / bottom -38, the arm leads the tips, outer wing folds on the upstroke, body rises on the downstroke (+-0.06), body pitch 28, head near level (a 6 deg look-down), legs trail beside the tail with a small pump |
| takeoff | 36 | no | `launch` f14 | H1 97-99 s: a COIL (hips -0.075, body pitched 17, chest 4) while the wings open FOLD -> LIFT1-4 -> stroke top (f10), HOLD f10-14, the push (f14), the first deep downstroke over 8 f (f13-21) while the body rises over 8 f (f14-22), the feet leave at f18, legs tuck, then f25-36 the flight cycle at the fly tempo, ending exactly on fly f0 |
| land | 32 | no | `touch` f17 | H1 12.6-17 s: flare upright (feathers to the front), wings brake forward, tail lifted, legs reach; TOUCH f17 into the coil (hips -0.08, pitch 16, chest 4) holding the FULL SPAN, HOLD f19-22, folds LIFT4 -> FOLD |
| roar | 60 | no | `roar` f20 | SNAP-OPEN (R2): f0-14 gather (neck in, head up 12, crest back), f14-20 the wings SNAP to FULL SPAN through LIFT1-4 (1-2 f per step), surfaces to the front; the beak opens AFTER the spread (f20-24, jaw lags), crest flares erect, f22-38 hold with a jaw buzz, head still; f38-54 fold back, crest settles |
| act_bow | 110 | no | `snap` f58 | COURTSHIP BOW (R3), zero net root travel: f0-22 chest lowers, head + neck bend forward (pitch down 25 = Neck 7.5 / Neck2 7.5 / Head 10), tail lifts; f22-44 two vertical bobs (Spine z -0.02 -> -0.06 -> -0.02, feet planted) with the wings DROOPED half-open low at the sides and a tip shudder on each bob; f44-58 rise, crest flares, wings lift (LIFT2 -> LIFT3) and SNAP closed (event f58); f64-80 two 6 deg tail flicks; f80-110 rest |

## Decisions / deviations
- Wing waypoints: the Thunderbird's tested LIFT1-4 + BREATH work unchanged on this wing (`_tools/path_test.py`: every
  fold <-> open path 0 hits). New: SPAN (25, 0, -45, 0) = the full span with the surfaces to the camera (the roar; not
  the Thunderbird / Griffin raised V), DROOP (65, 26, -75, 10) = half-open, hanging low (the bow).
- roar event at f20 (plan f18): the reference shows the beak opening only after the spread completes; the event marks
  the call.
- Fly body pitch 28 (Thunderbird 40) so the neck chain can level the head inside the pose limits (head + neck
  pitch-up <= 30, each neck bone <= 8).
- Knee capsule in `joints()` widened to the Thunderbird's (K - 0.10 d .. K + 0.20 d, r 0.13): the drumstick top is
  buried in the belly feathers when the body lowers. Crouches kept shallow (takeoff -0.06, land -0.05, bow -0.06).
- R3 (white rump) check, review 3: game-camera renders of every clip beat from behind and above
  (`renders/_pose_game_*_sheet.png`) show no white fan; the four tail feathers stay grey / violet / CHAR.

## Renders
`renders/_pose_tq_idle_sheet.png`, `_pose_tq_walk_sheet.png`, `_pose_tq_fly_sheet.png`, `_pose_tq_takeoff_sheet.png`,
`_pose_tq_land_sheet.png`, `_pose_tq_roar_sheet.png`, `_pose_tq_act_bow_sheet.png` (frames labelled);
`_pose_front_<clip>_sheet.png` and `_pose_game_<clip>_sheet.png` for every clip (re-rendered after FOOT_LIFT 0.017).
