# Blizzard Roc - clip gate review 4 (2026-10-27) - APPROVED WITH FIXES (clips)

**Score: 8/10 for a 7.4 % HIGH flyer** (ship target 8). The pose limits pass with margin, the acts are in place and end
at rest, the beats read, and there are no head shakes or spins. Two MUSTs are left, and both are small: (1) the
animation-reference source rule, and (2) the takeoff and landing read as light, not heavy. Fix them, re-run step 1 and
send the takeoff and landing sheets again. No other clip is held.

What I looked at:
- `BlizzardRoc/CLIP_NOTES.md`, `BlizzardRoc/ANIM_REFS.md`, `_scratch/full_step1.txt`
- code: `pets/BlizzardRoc.py` idle L551-576, walk L578-618, roar L620-641, act_bow L642-675, fly L689-712, takeoff L721-747, land L749-783
- all 21 pose sheets: `renders/_pose_tq_*`, `_pose_game_*`, `_pose_front_*` (seven clips each, frames labelled, 300 px a frame, the bow 600 px)
- the reused reference `_review/ANIM_REFERENCES_1014.md` #5 (checked for source)

---------------------------------------------------------------------------------------------------------------------
## 1. Step 1 (`full_step1.txt`, all frames)

| check | limit | value | result |
|---|---|---|---|
| collision_free | true | true | PASS |
| ground_min_z, ground clips | >= -0.02 | -0.014 (idle, takeoff, land, roar, act_bow); -0.015 (walk) | PASS (margin 0.005) |
| ground_min_z, fly | (airborne) | +0.377 | PASS |
| audit linear | 0 | 0 on every clip | PASS |
| loops closed | idle, walk, fly | loop_pos 0, loop_rot 0 | PASS |
| walk slide | 0 | 0.0, foot_z_var 0.0 | PASS |
| neck (Neck, Neck2) | <= 8 deg | 7.8 | PASS |
| chest vs spine | <= 5 deg | 3.0 | PASS |
| head + neck pitch-up (neck chain) | <= 30 deg | 26 | PASS |
| head pitch-down (neck chain, bow) | <= 30 deg | 25 | PASS (world space: see N3) |
| largest bone step | <= 60 deg per frame | 36.5 (land, snow-puff anchor); wings 32.6 (roar) | PASS |
| glow meshes | none | `tris_glow` {} | PASS |
| tris | <= 15k | 12,964 | PASS |
| event frames | match the table | the JSON event values are fractions of clip length: frostshed 0.2 x 120 = f24, launch 0.367 x 30 = f11, touch 0.531 x 32 = f17, roar 0.333 x 60 = f20, snap 0.527 x 110 = f58 | PASS |

I checked the event values against the frame table, and they agree. The step-1 `idle_foot_drift` 0.052 is the largest
foot move during the two talon re-grips, not a net drift. The clip gate accepts it, but see N5.

---------------------------------------------------------------------------------------------------------------------
## 2. The beats (judged in the pose sheets)

- **idle "frost shed" (120 f): PASS.** The wings lift half-open and the frost shiver is clear at f24 (front, tq, game).
  Head: two opposite 10-deg turns, each a quick move then a long hold (44-52 right, 90-98 left), then back to centre. It
  does not oscillate, so it is not a shake. The tail lowers at f68. No watch-scan.
- **walk (30 f): PASS.** Plain strut, wings folded, no hop. The body roll is small and the head is steady. From the front
  the feet alternate. The stride is subtle at 300 px, but it reads.
- **fly (30 f): PASS.** The wing stroke is clear. The front view shows no wing through the body, the body is nose-up, and
  the legs trail. It reads as a big bird.
- **takeoff (30 f): PARTIAL, reads light (MUST 2).** Stroke top at f10, launch at f11, the first downstroke at f13-16,
  and the feet are clear of the ground by f16 (front view). But the crouch is 0.06 BU (about 0.27 studs, 3 % H) and the
  whole run-up is half a second. It reads as a quick launch, not a heavy one.
- **land (32 f): PARTIAL (MUST 2 for the crouch; N1 for the edge-on wings).** Flare at f6, touch at f17 with the wings
  held at full span, crouch to f24, folded and standing at f31. The crouch at touch is only 0.05 BU (about 2.5 % H). From
  the front, at f6 and f24, the wings are edge-on and read as thin poles for about 0.2 s each.
- **roar "snap-open" (60 f): PASS.** The gather is at f14, the wings spread to a flat full span by f20 (front view), the
  crest is erect, and the beak opens after the spread (R2). The hold is clean, and the wings fold back by f45. The jaw
  buzz is the only small motion, and the head is still. Head is about 13 deg up in world space during the hold; the
  notes say level (N3).
- **act_bow "courtship bow" (110 f): PASS.** The chest lowers and the beak dips to near the ground (f22-38). The wings
  droop half-open and shudder. The wings snap up at f52 and close at f58. Two tail flicks at f68 and f76. Back to rest by
  f100. Root travel is zero net (the Spine z returns to 0, and the feet are planted). It reads as a bow, not a stoop.

---------------------------------------------------------------------------------------------------------------------
## 3. ANIM_REFS rule (owner rule: pull 1-3 clips from animationreference.org)

- **R5, the Bird Flight Tutorial (flapping):** PASS. It is ANIM_REFERENCES_1014 #5, which was pulled from animationreference.org.
- **R1-R4, The Boy and the Heron (Sakugabooru #260711, #260630, #260644):** PARTIAL. The notes say the bird and flying tag
  pages on animationreference.org "point to Sakugabooru", so the footage was not pulled from animationreference.org. The
  times and key poses are cited, which meets the citation half of the rule. The source half is not met. Owner decision
  needed: either the builder records the tag URL and the item it followed, or pulls one animationreference.org bird clip
  for the bow or the roar (about 25 free opens a day). I cannot settle this for the owner. It is a MUST (1) until one of
  the two is done.
- No HTTYD frames were read, as the notes say.

---------------------------------------------------------------------------------------------------------------------
## 4. Heavy read (the owner's question)

- **Wingbeat: reads heavy enough.** A 30-frame stroke (about 1 Hz) with a deep downstroke and the body rising on it
  reads as a big bird, not a small one. Keep it.
- **Takeoff: reads light.** See MUST 2.
- **Landing: reads moderate.** A bird that comes down with the wings held at full span and a shallow crouch looks
  controlled, not heavy.

---------------------------------------------------------------------------------------------------------------------
## 5. Carry-overs from review 3

- **Ground margin:** closed. The walk is now -0.015 (was -0.018), a margin of 0.005 to the -0.02 limit.
- **R3 white rump from behind:** closed. The game-camera sheets (idle, walk, roar, act_bow, takeoff, land) show grey and
  violet tail feathers. There is no white fan.

---------------------------------------------------------------------------------------------------------------------
## 6. MUST list

**MUST 1 - animation-reference source (ANIM_REFS rule).** Either (a) record in `ANIM_REFS.md` the animationreference.org tag
URL and the item that led to each Sakugabooru post for R1-R4, and get the owner's OK that Sakugabooru posts found that way
count; or (b) pull one animationreference.org bird clip for the bow or the roar, cite its frames, and keep the Heron
refs as supporting. No clip change is needed.

**MUST 2 - takeoff and landing read heavy (`pets/BlizzardRoc.py`).**
- Takeoff (L721-747): deepen the crouch. Keys at f6 z -0.06, f8 z -0.11, f10 z -0.13, and hold f10-12 (the wings stay at
  the stroke top). Move the `launch` event from f11 to f13 (`round(13/30, 3)`), so it still falls on the first big
  downstroke. Extend `plant_frames` to cover the deeper crouch.
- Landing (L749-783): the touch crouch goes from z -0.05 to z -0.09 at f17, and from -0.035 to -0.06 at f22. Hold f17-19.
  Keep `touch` at f17 on the contact frame.
- Then re-run step 1: `collision_free` true, `ground_min_z` >= -0.02 on takeoff and land, loops closed. Send the takeoff
  and landing sheets at 400 px a frame (tq, game and front).
- Target: the crouch reaches about 7-8 % of H (0.6-0.7 studs). It must not lift the feet off the planted spots.

---------------------------------------------------------------------------------------------------------------------
## 7. NICE list

- **N1 - edge-on wings from the front.** At land f06 and f24 the wings read as thin poles for about 0.2 s. Turn the
  feather plane 15-20 deg in the flare key (L736-740) and in the LIFT3/LIFT4 key, so the front view shows the feathers.
- **N2 - tail from behind.** In the game sheets the two outer tail feathers (yaw +-8, L364-366) read as long rods with
  violet tips. Spread them to +-12 deg, or shorten the two outer feathers from 0.74 to 0.66 BU.
- **N3 - record world-space head angles.** The bow head is about 38 deg down in world space (Spine 10 + Chest 3 + neck
  25), against 25 in the neck chain that the limit uses, so it passes. The roar head is about 13 deg up in the hold, and
  the notes and the docstring say "level". Correct the wording, or accept the call pose.
- **N4 - sheet size.** The 300 px frames are enough for this gate. Use 400 px for the takeoff and land fix pass.
- **N5 - idle foot drift.** Report the net drift at the loop end (it should be 0). The 0.052 is the peak during the re-grip.

---------------------------------------------------------------------------------------------------------------------
## 8. Pass / fail

| # | check | result |
|---|---|---|
| 1 | collision_free | PASS |
| 2 | ground_min_z >= -0.02 (ground clips) | PASS (-0.014 / -0.015) |
| 3 | audit linear 0 | PASS |
| 4 | loops closed (idle, walk, fly) | PASS |
| 5 | walk slide 0 | PASS |
| 6 | neck <= 8 | PASS (7.8) |
| 7 | chest vs spine <= 5 | PASS (3.0) |
| 8 | head + neck pitch-up <= 30 | PASS (26) |
| 9 | head pitch-down <= 30 (neck chain) | PASS (25) |
| 10 | largest bone step <= 60 | PASS (36.5) |
| 11 | no head shakes | PASS (idle turns are opposite and held; roar jaw buzz only) |
| 12 | no airborne spins | PASS |
| 13 | acts in place (zero net root travel) | PASS (act_bow) |
| 14 | acts end at rest | PASS (act_bow f100, roar f56, idle loops) |
| 15 | events match the frames | PASS |
| 16 | idle reads | PASS |
| 17 | walk reads, no hop | PASS |
| 18 | roar reads (snap, beak after the spread) | PASS |
| 19 | act_bow reads (bow, not stoop; snap) | PASS |
| 20 | fly reads (big bird) | PASS |
| 21 | takeoff reads heavy | **FAIL** (MUST 2) |
| 22 | landing reads heavy | PARTIAL (MUST 2) |
| 23 | ANIM_REFS source rule | **PARTIAL** (MUST 1) |
| 24 | no glow meshes | PASS |
| 25 | white fan from behind (R3 carry-over) | PASS |
| 26 | ground margin carry-over | PASS (0.005) |

Score 8/10. Apply MUST 1 and MUST 2, re-run step 1, and send the takeoff and landing sheets at 400 px. Then the clip gate
can close.
