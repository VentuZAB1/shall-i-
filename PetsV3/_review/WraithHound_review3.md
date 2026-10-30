# Wraith Hound - clip gate review 3 (2026-10-27) - APPROVED WITH FIXES (clips)

**Score: 7.5/10** (round 2 was 7.5/10). Ship bar is 8/10.

The clips pass every pose limit with margin. Idle, walk, roar and the cloak all close their loops, stay in place, end on the rest pose, and keep the feet on the ground. The beats read: the drift, the trot, the snarl with the fangs out, the crouch and the fan. The model is close too.

Two MUSTs remain, both small:
- **MUST 1 (clips, doc and process):** the animation-reference rule was not followed for two of the four refs. The owner rule says animationreference.org, and the builder had 6 opens left.
- **MUST 2 (model, carry-over):** round-2 MUST 1 is only partly met. The mane's three rows still read as three separate fins. This is geometry only: no bone, joint or clip timing changes.

HEIGHT 9.0 (round-2 MUST 2) is closed, and the saddle waiver is accepted.

## What I looked at
- Notes and refs: `WraithHound/CLIP_NOTES.md`, `WraithHound/ANIM_REFS.md`, `WraithHound/MODEL_NOTES.md`, the rule `feedback-animation-references` and the vault guide `Animation References.md`, and the earlier refs `_review/ANIM_REFERENCES_1014.md`.
- Data: `_scratch/fullcheck.json` and `WraithHound/WraithHound.json` (clip export: quaternions as XYZW, rest-relative; positions in Roblox axes, X lateral, Y up, Z forward). I computed the angles per frame, the frame-to-frame steps, the loop wrap and the event times myself. I used Python on the JSON only. No Blender, no Studio.
- Mane and HEIGHT: `renders/crop_mane_side.png`, `crop_mane_front.png`, `_icons_strip_128.png`, `low_below.png`, `saddle_debug_side.png`, `saddle_debug_game.png`.
- Pose sheets: `renders/_pose_tq_sheet.png` (15 tiles), `_pclose_tq_sheet.png`, `_pclose_side_sheet.png`, `_fan47.png`, and the single frames `pclose_front_act_smokecloak_47.png`, `pclose_side_act_smokecloak_30.png`, `pclose_front_roar_30.png`.

## Numbers (from the JSON, not the notes)

| clip | neck max | chest max | neck+head pitch | head yaw / roll | Spine Y (up) | Spine Z (fwd) | loop |
|---|---|---|---|---|---|---|---|
| idle (120 f) | up 2.8 / down 3.5 | 0.6 | up 8.0 / down 10.0 | 0 / 0 | +-0.003 | 0 | wrap 0.85 deg, typical step p99 0.89 - closed |
| walk (30 f) | 4.0 | 2.9 | down 3.3 to 4.6 | yaw 1.5 / 0 | -0.014 | 0 | wrap inside the walk's step range - closed |
| roar (60 f) | 4.0 (down) | 1.5 | down 10.6 | 0 / 0 | -0.020 | -0.064 | rest in and out |
| act (100 f) | 5.0 | 1.5 | up 7.0 | 0 / 0 | **-0.200** | +0.015 | rest in and out |

**Limits (brief)**

| limit | data | result |
|---|---|---|
| neck <= 8 deg | 5.0 (act) | PASS |
| chest vs spine <= 5 deg | 2.9 (walk) | PASS (the notes say 1.5, which is wrong; see NICE 1) |
| head + neck pitch-up <= 30 deg | 8.0 (idle), 7.0 (act) | PASS |
| no head shakes | head yaw 0 in idle, roar and act; 1.5 in walk | PASS |
| no airborne spins | no Spine or Root rotation track; chest yaw 2.5 in walk | PASS |
| in place | Spine X = 0 in every clip; Z at most 0.064 (roar lean) | PASS |
| ends at rest | last frame equals first frame in all four clips | PASS |
| collision_free / linear 0 / slide 0 | true / 0 / 0 (fullcheck) | PASS |
| ground_min_z >= -0.02 | 0.004 in all clips (fullcheck) | PASS |

Two of my findings were not what I first thought. The first pass read the wrong axis and seemed to show no crouch drop. The export is Roblox-axes, so the drop lives on Y and is 0.200 units, as the notes say. The roar's forward push of 0.064 and its 0.020 drop also match the notes.

**Event times** (fraction of clip length x length): roar `fog` 0.233 = f14, `snarl` 0.433 = f26; act `smoke_puff` f16, `cloak` f28, `drift` f54. All match CLIP_NOTES. FX anchors (`FX_Fog`, `FX_SmokePuff_F*`, `FX_SmokeWisp_1-3`, `FX_IndigoWisp_L/R`, `FX_SmokeTrail`) are all in the bone list.

## Beats
- **idle "scent drift":** the nose lowers 10 deg (neck and head together) and lifts 8 deg; the ears flick back 14 deg and forward 8 deg. Reads as sniffing, with no head shake.
- **walk "lean trot":** diagonal pairs, stride 0.6, the head low and level. The loop is continuous. The knees snap quickly (NICE 2).
- **roar "mane flare":** the rows lift 20 deg, the side wisps splay 25 deg (roll), the ears go back 25 deg, the head drops 10.6 deg, and the jaw opens 26 deg. In the front tile the fangs read and the snarl reads. The side wisps fan out at head height, like winged spikes (NICE 3).
- **act "cloak spreads":** the body drops 0.200 units (0.16H) and the tail lifts 10 deg. The forelegs swing forward 41 deg to keep the paws planted. The fan at f47 opens the rows (lift 14 deg, side roll 55 deg). It reads as a dramatic spiky fan from the front, the back and the three-quarter view in `_fan47.png`. It reads more as a crest than as smoke, but the beat is clear. The feet stay planted in every frame.

## Model check (round 2 carry-over)
- **HEIGHT 9.0:** closed. The ground minimum is 0.004 in every clip.
- **Saddle waiver:** accepted. In `saddle_debug_side.png` the magenta covers 8.5 % of the non-black pixels. Against the flat silhouette, which is 28k pixels, it is 13 %. The builder's 11.7 % sits in that range. I'd like the denominator written into MODEL_NOTES.
- **Mane plume:** partly met. In `crop_mane_side.png` the blades are longer and sweep back at about 30 deg, which is a real improvement. But the top, middle and bottom rows still have separate blue tips. At 128 px it reads as a dark spiked crest. The round-2 target was one overlapping line.
- **Under-view slabs** (chest plate and belly tuck, round-2 NICE 1): still flat and pasted-on in `low_below.png`.
- **Icon strip 128:** the Wraith (first) reads as a pale lilac hound with a dark crest. It is clearly not Raiju's royal-blue body.

---------------------------------------------------------------------------------------------------------------------
## 1. MUST

**MUST 1 - the animation-reference rule (clips, before export).** The owner rule (`feedback-animation-references`, `Animation References.md`) says: before ANY animation, pull 1-3 clips from **animationreference.org**, note the frames and cite them in the plan. ANIM_REFS cites two refs straight from Sakugabooru: W1 (Sheep Dog, #143877) and W2 (The Pointer, #258150). The vault guide allows the Sakugabooru copy only "when the 25/day are used up". The note says 6 opens were left. Its claim that "its tags have no canid" is not fully checked: `/tags/animals` (532 clips) and `/tags/walk-cycle` (367) were not tried. The "quadruped" tag is a 404, as noted.
- Fix: open one or two canid or quadruped clips on animationreference.org (try `/tags/animals` and `/tags/walk-cycle`, then the site's own player). Take the frames for the walk and the snarl, cite the site tag and clip in ANIM_REFS, and re-check the timings against them. Keep W3 and W4, which come from animationreference.org (ANIM_REFERENCES_1014 #6 and #4).
- If the site has nothing usable, list the tags tried in ANIM_REFS and ask the owner for an exception before the clips ship. Do not just cite Sakugabooru.
- Doc note: W4 #8 is a YouTube source in the earlier file, not the site. Say so.

**MUST 2 - the mane rows must merge into one plume (model, before export).** Round-2 MUST 1 is only partly met (see above). The blades are longer, but the three rows still read as three blade sets.
- In `pets/WraithHound.py`, `mane_row` (L77-89): the rows' blue tips must lie on one swept line. Practical direction: raise the Mane2 and Mane3 roots about 0.03 (their Z in MANE, L33-35) so each row's tail covers the next row's root, and keep the back-wisp tail at about 0.34 x sc.
- Check: `crop_mane_side.png` and the 128 px strip. The blue points should form one swept line, with no third row of separate points.
- This does not change any bone, joint or clip timing. The mane bone names stay. Re-run the headless export so the `collision_free` pairs (Mane1 against the Head and ears) still pass.

---------------------------------------------------------------------------------------------------------------------
## 2. NICE

1. **Notes accuracy (CLIP_NOTES, ANIM_REFS).** The data disagrees with the notes in four places. Correct them before the owner reads them:
   - chest vs spine: the notes say <= 1.5; the walk reaches 2.9 (the brief's limit is 5, so it passes);
   - roar mane lift: the notes say 18 deg; the data peaks at 20;
   - act side-wisp roll: the notes say 52 deg; the data peaks at 55;
   - ANIM_REFS maps the `snarl` event to f20; CLIP_NOTES and the data say f26.
2. **Walk knee snaps.** The front knees move about 16-18 deg in a single frame: Shin_FL f15 to f16 (-17.9 to -1.6), and Shin_FR f0 to f1 (-19.6 to -1.5). Spread each over two frames (for example f15 -> -9 -> -1.6) so the trot does not look like a click.
3. **Front-view wings.** From the front, the side wisps flare out at brow height in the rest pose (`crop_mane_front.png`) and again at roar and f47 (`pclose_front_act_smokecloak_47.png`). They read as spiky wings or horns beside the head. Option: reduce the rest lateral in `mane_row` L84 from `s_ * 0.55` to about `s_ * 0.40`, and keep the fan width in the clip's roll.
4. **Crouch forepaws.** The upper forelegs swing 41 deg forward (plan: 30 deg bend). The forepaws reach out in front of the chest. It reads as a stalk, not a lunge, so it passes. If the owner calls it a lunge in game, cut the swing to about 30 deg and let the drop carry the crouch.
5. **Under-view slabs** (round-2 NICE 1, still open): round the chest plate (`rnd` 0.35 to 0.5 at L134) and the belly tuck (L132).

---------------------------------------------------------------------------------------------------------------------
## 3. Pass / fail checklist (clip gate)

| check | result |
|---|---|
| Neck <= 8 deg | PASS (5.0) |
| Chest vs spine <= 5 deg | PASS (2.9) |
| Head + neck pitch-up <= 30 deg | PASS (8.0 idle, 7.0 act) |
| No head shakes | PASS (head yaw 0; walk 1.5) |
| No airborne spins | PASS (no Spine or Root rotation; chest yaw 2.5 in walk) |
| Acts in place, ending at rest | PASS (X = 0; last frame = first frame) |
| Readable beats | PASS (drift, trot, snarl with fangs, crouch and fan) |
| Feet planted in act | PASS (ground min 0.004 at all clip frames) |
| collision_free / linear 0 / slide 0 | PASS (fullcheck) |
| Loops closed | PASS (idle wrap 0.85 deg; walk wrap within its step range) |
| Event timing matches notes | PASS (roar f14/f26; act f16/f28/f54) |
| ANIM_REFS rule (animationreference.org) | **FAIL** (MUST 1) |
| Mane reads as one plume | **FAIL** (MUST 2) |
| HEIGHT 9.0, ground clear | PASS (round-2 MUST 2 closed) |
| Saddle waiver 10-14 % | PASS (11.7 builder; 8.5-13 % my count, denominator note) |
| Tris <= 15k, no glow | PASS (6,820; no glow meshes) |

**Round-4 packet (short):** the updated ANIM_REFS with the site's clip(s) (MUST 1), `crop_mane_side` plus the 128 px strip (MUST 2), the corrected CLIP_NOTES, and a re-run of `fullcheck.json` after the mane change.
