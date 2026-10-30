# Blizzard Roc - clip gate review 5 (2026-10-28) - MODEL 8.5 APPROVED / CLIPS 8.4 APPROVED WITH FIXES (below the 8.5 bar)

**Scores (new bar: 8.5 minimum, higher is better)**
- **Model: 8.5 / 10. APPROVED.** The only code change is the tail fan (N2). Its model renders predate the last edit (see MUST 4).
- **Clips: 8.4 / 10. APPROVED WITH FIXES.** Below the bar. The takeoff is the weak beat: it snaps into the fly loop and
  the launch reads light. The other six clips are at 8.5 or better. MUST 1-3 should take the clips to about 8.6.

**Does the coil read as heavy?** The landing: yes. It holds the full span, the body sinks, it rises slowly and folds
back, and the touch reads as a thud. The takeoff: not yet. The coil reads as a crouch and lean, but the launch is a
pop (0.6 studs in 0.1 s) with a 3-frame wing whip, and the takeoff hands off to the fly loop with a visible snap.
MUST 1 and MUST 2 fix the takeoff.

What I looked at:
- `BlizzardRoc/CLIP_NOTES.md`, `BlizzardRoc/ANIM_REFS.md`, `BlizzardRoc/_scratch/full_step1.txt`, `rest_delta.txt`, `crouch.txt`
- code diff against the review-4 snapshot (`_scratch/BlizzardRoc_r4final.py.txt`): the tail fan, the knee splay in `plant_frames`, the takeoff, land and roar changes
- all 400 px takeoff and land sheets (tq, game, front), and the roar, act_bow, idle, walk and fly sheets (unchanged keys, rest-checked)
- the model renders and the walk game sheet for the tail
- `wing3.stroke` (evaluated outside Blender, to measure the seam)

---------------------------------------------------------------------------------------------------------------------
## 1. Step 1 (`full_step1.txt`)

| check | limit | value | result |
|---|---|---|---|
| collision_free | true | true | PASS |
| ground_min_z, ground clips | >= -0.02 | -0.014 (idle, takeoff, land, roar, act_bow), -0.015 (walk) | PASS (margin 0.005) |
| ground_min_z, fly | (airborne) | +0.377 | PASS |
| audit linear | 0 | 0 on every clip | PASS |
| loops closed | idle, walk, fly | loop_pos 0 | PASS |
| walk slide | 0 | 0.0 | PASS |
| neck | <= 8 deg | 7.8 | PASS |
| chest vs spine | <= 5 deg | 4.0 (the coil) | PASS |
| head + neck pitch-up | <= 30 deg | 26 | PASS |
| largest bone step | <= 60 deg per frame | 36.5 (land), wings 32.6 (roar) | PASS |
| events | match the frames | launch 0.467 x 30 = f14; touch 0.531 x 32 = f17; roar f20; snap f58; frostshed f24 | PASS |
| rest frames | 0 deg from rest | roar f60, act_bow f110, land f32 (rest_delta) | PASS |
| glow, tris | none, <= 15k | `tris_glow` {}, 12,964 | PASS |

---------------------------------------------------------------------------------------------------------------------
## 2. Clip scores (out of 10)

| clip | score | why |
|---|---|---|
| idle (frost shed) | 9.0 | Reads: the wings lift half-open at f24, the head turns are opposite and held (not a shake), the net foot drift is 0 (N5 done). |
| walk | 8.0 | Plain strut, no hop, the head is steady, the wings are folded. Small at phone size, and a 1.0 s cycle reads a little mechanical (TO 9). |
| fly | 8.5 | A clear big-bird stroke, no wing through the body, legs trail. Its loop is fine. The seam fault is at the takeoff end. |
| takeoff | **7.0** | The seam snaps into the fly loop (MUST 1). The launch is a pop (MUST 2). The coil reads as a lean, and the legs don't flex visibly. |
| land | 8.5 | The flare turns the feathers to the front (N1 done). The touch thud, the hold at full span, the slow rise and the fold read as a controlled heavy landing. The rest frame is exact. |
| roar | 9.0 | The snap-open reads (f14-20). The beak opens after the spread. The head is still, the crest is erect, the wings fold clean. |
| act_bow | 9.0 | Reads as a bow, not a stoop. Zero net root travel. The snap at f58 and the tail flicks read. Rest is exact. |
| **average** | **8.4** | Below the 8.5 bar. |

---------------------------------------------------------------------------------------------------------------------
## 3. The takeoff seam (new finding, the biggest fault)

`pets/BlizzardRoc.py` L754-755: the takeoff's flight keys end at `fly_pose(k, n, 0.2)`. The takeoff's last frame is
flight phase **0.2**. The fly clip's frame 0 is phase **0.0** (`fly()` uses `fly_pose(k, f, f/n)`). The game plays
takeoff, then fly, so the two poses meet at the seam. Evaluated from `wing3.stroke` and the fly keys:

| bone / body | takeoff f30 (phase 0.2) | fly f0 (phase 0.0) | jump in one frame |
|---|---|---|---|
| wing up | 5.4 deg | 36.0 deg | **30.6 deg** |
| spine pitch | 26.2 deg | 29.8 deg | 3.5 deg |
| body z | 0.100 BU (0.45 studs) | 0.043 BU (0.19 studs) | **-0.26 studs** |

A 30-degree wing snap and a 0.26-stud drop in one frame is a visible pop. The fly-to-land seam is clean (land f0 is
fly phase 0), so this is the takeoff only.

Also, the takeoff's flight phase runs 5 frames per 0.2 of a cycle (25 frames a cycle), but the fly loop is 30 frames a
cycle. The tempo changes at the seam too.

---------------------------------------------------------------------------------------------------------------------
## 4. The launch (the heavy read)

Takeoff keys (L743-747): the coil goes to z -0.075 at f13, then z +0.06 at f16 and +0.14 at f19. The body rises 0.135 BU
(0.61 studs) in 3 frames (0.1 s). The wings drop from +36 to -14 in 3 frames (f13-16). A heavy bird does not pop: it
pushes, and the wings take longer to bring down.

---------------------------------------------------------------------------------------------------------------------
## 5. Checks that passed

- Land: the touch (f17) sinks the body, a 2-frame drop from f15 to f17. The hold (f19-22) keeps the span. The fold
  (f24-32) is slow, and the rest is exact.
- Front and game takeoff: the coil reads as the body dropping about 12 % of height with the wings raised, then the
  launch. The feet are planted until the lift.
- N1 (land f6 and f24, the feathers face the front): done. The front land sheet shows feathers, not poles.
- N2 (the tail fan to ±12): applied in code. The model renders (00:26) predate it. The walk game sheet still shows the two
  outer feathers as rods from behind (TO 9).
- The knee splay (the clip-only pole change in `splay_at` and `plant_frames`, L505-531): feet stay on their spots, and step 1 is clean.
- Refs (ANIM_REFS.md): H1 (#260630, Akihiko Yamashita, `/tags/flying` item), E1 (#236985, Earthsea), and R5 (the bird-flight
  tutorial, from animationreference.org) each record a tag, a site item and the frames cited. The earlier MUST 1 is
  satisfied for these. I have not re-verified the md5 mapping (the reviewer does not open sites).

---------------------------------------------------------------------------------------------------------------------
## 6. MUST list (to reach 8.5+ on the clips)

**MUST 1 - the takeoff seam (`takeoff()`, L754-760).** Make the takeoff's last flight frame the fly loop's frame 0 (phase
1.0 = 0.0), and run the flight phase at the fly tempo (1/30 a frame). Change:
- `fly_pose(k, 25, 0.0)` to `fly_pose(k, 25, 5/6)`, and `fly_pose(k, n, 0.2)` to `fly_pose(k, n, 1.0)`;
- `fly_legs(k, 25, 0.0)` to `fly_legs(k, 25, 5/6)`, and `fly_legs(k, n, 0.2)` to `fly_legs(k, n, 1.0)`.

Verify with the step-1 check: the seam (takeoff f30 against fly f0) must differ by no more than 3 deg per bone, and the
body z by no more than 0.02 BU.

**MUST 2 - stretch the launch (`takeoff()`, L743-747, and `plant_frames` L754).** Keep `launch` at f14 (the push).
- The first downstroke: (13, 36 hold), (17, -8), (21, -36). It takes about 8 frames, not 3.
- The body rise: (14, z -0.075), (18, z -0.01), (22, z +0.07). The pitch can stay at 17-26.
- Move the plant range to f0-17 and `lift_air_frames` to f17+.
- Target: the body rises 0.6 studs over about 0.3 s, and the first downstroke takes 8 frames. Re-run step 1 (collision
  free, ground_min_z >= -0.02 on takeoff).

**MUST 3 - references must match the clips (documentation).** The coordinator's report lists two refs that are NOT in
`ANIM_REFS.md` or `CLIP_NOTES.md` (as of 00:50): #174482 (*Maid Dragon S*, level flight) and #256671 (*The Cat Returns*,
walk via `/tags/walk-cycle`). Either record them (tag, site item, Sakugabooru post, the frames and what they drive, as the
other refs are), or remove them from the report. The walk in the clips uses the heron (#260630, wading walk), so the
Cat Returns walk should not be cited unless it drives a clip.

**MUST 4 - the model evidence is stale (deliverable).** The model renders are dated 00:26, and the code's last edit is
00:49 (the tail fan ±12). Re-render `model_game`, `model_side` and `_model_sheet` after the tail change, and confirm the
outer feathers fan on the game camera. The model's score (8.5) holds only if the new fan reads as a fan, not rods.

---------------------------------------------------------------------------------------------------------------------
## 7. TO 9+ list (after the MUSTs; higher is better)

1. **Visible knee bend in the coil.** The hips drop only 3.7 % because the trousers hit the belly. The fix is in the
   mesh, not the keys: shorten the upper SNOW trouser block or move it back about 0.02 BU, so the hips can drop 6-7 %.
   Then re-key the coil to about -0.10 (about 5 %). Keep the feet planted (no ground slide).
2. **Walk weight.** A 1.0 s cycle reads a little mechanical. Slow it to about 1.2 s and add a 0.01 BU lateral roll on the
   stance, so the bird reads heavier. Re-check the walk slide (0) and the ground margin.
3. **Edge-on wings in the takeoff front view (f16-19).** The wings read as planks for about 0.2 s. Turn the feather plane
   15-20 deg in the LIFT keys at f16-19, as with N1.
4. **Tail from behind (game walk).** The two outer feathers still read as rods with violet tips. Spread them to ±14, or
   taper the outer two more (the fan and length at L364-365, the taper at L368).
5. **Eye hot spot (model, NICE 1 from review 3).** The white FROST_H bar still reads like a glint at close range. Shrink it
   to 0.010 x 0.002, or move it to the inner corner.
6. **Idle front (f24).** The half-open wing reads as flat grey plates. Give the coverts a slight stagger.
7. **Runtime note (not a clip fix).** Fly to land starts at fly phase 0, so the runtime should trigger land at phase 0
   (or crossfade). Any clip-to-clip switch at an arbitrary phase has the same snap.

---------------------------------------------------------------------------------------------------------------------
## 8. Pass / fail

| # | check | result |
|---|---|---|
| 1 | collision_free | PASS |
| 2 | ground margin (>= -0.02) | PASS (-0.014 / -0.015) |
| 3 | audit linear 0; loops closed; walk slide 0 | PASS |
| 4 | neck <= 8 | PASS (7.8) |
| 5 | chest vs spine <= 5 | PASS (4.0) |
| 6 | head + neck pitch-up <= 30 | PASS (26) |
| 7 | largest bone step <= 60 | PASS (36.5) |
| 8 | no head shakes | PASS |
| 9 | no airborne spin | PASS |
| 10 | acts in place (zero net root) | PASS (act_bow) |
| 11 | acts end at rest | PASS (roar, act_bow, land) |
| 12 | events match the frames | PASS |
| 13 | takeoff to fly seam | **FAIL** (MUST 1) |
| 14 | launch reads as weight | **FAIL** (MUST 2) |
| 15 | landing reads as weight | PASS |
| 16 | idle, roar, act_bow read | PASS |
| 17 | walk reads | PASS (TO 9 on weight) |
| 18 | fly reads | PASS |
| 19 | refs cited and matching the clips | **PARTIAL** (MUST 3) |
| 20 | model evidence current | **PARTIAL** (MUST 4) |
| 21 | no glow; no white fan from behind | PASS |

**Verdict.** Model 8.5, APPROVED. Clips 8.4, APPROVED WITH FIXES (below the 8.5 bar). After MUST 1-4, the clips should
reach about 8.6 (my estimate: takeoff to 8.5, the others unchanged). Then the TO 9+ list is what raises it further.
