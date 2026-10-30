# Bramble Badger - FINAL 8.5 GATE, ROUND 5 (2026-10-28) - Model PASS, Clips FIX

**Model: 8.6/10 - PASS. Clips: 8.4/10 - FIX.**

Overall: FIX, on one blocking item. The breath fix is real in substance, the act, roar and walk renders are now current, and every numeric gate passes. The clip cannot clear 8.5 until the neck clause of round-4 M2 has visual evidence (MUST 1). Everything else is polish.

## What I looked at

- Brief: `_review/GLACIER_REVIEWER_BRIEF.md`. Round 4: `_review/BrambleBadger_final85_r4.md`.
- Builder notes: `BrambleBadger/CLIP_NOTES.md` (round 4 section), `MODEL_NOTES.md` (round 6), `ANIM_REFS.md`.
- Numbers: `BrambleBadger/_scratch/measure_breath_b0.json` and `measure_breath_b1.json` (04:24), `measure_clear_b1.0.json` (04:39), `cm_r4.log` and `clipmetrics.json` (04:32), `fc_r4.txt` and `fullcheck.json` (04:32), `export.log` (04:42), `gate_r4.txt`.
- Code: `PetsV3/pets/BrambleBadger.py` (mtime 04:32:25; md5 matches `_scratch/BrambleBadger_f85r4.py`, the 04:42 copy). Lines checked: 40-42 (test switches), 139-140 (mantle and tilt), 175 (cheek ruff), 331-345 (idle keys), 416-430 (act kick table), roar thorns and drop, walk body.
- Images opened: `renders/_breath_side_r4.png`, `_pose_side_r4.png`, `_pose_tq_r4.png`, `_ear_twitch_r4.png`, `_model_sheet.png`, `_icons_strip_64.png`, `_icons_strip_128.png`, `game_view.png`, `_close_sheet.png`, `pclose_game_idle_36.png`. No image failed to load.
- My own crops (outside the project): `C:\Users\ventu\AppData\Local\Temp\bb_r5\act68_head_mantle_3x.png`, `act44_head_mantle_3x.png`, `tq_act68_3x.png`.
- Timestamps: the pet file was last written at 04:32:25. Every act, roar and walk render (04:32:33-45), `_pose_side_r4` and `_pose_tq_r4` (04:32:45), and the idle renders from 04:36-04:39 are later than that, so they are current.
- I did not run Blender. Numbers come from the saved logs, checked against the code formulas.

## Breath arithmetic (breath on vs off, same frame)

From `measure_breath_b0` and `b1`:
- Breath-only shift at every breath peak and trough (f10, 30, 50, 70, 90, 110): the mantle edge point, the shoulder-top centre and the Spine hull top each move exactly ±0.0140 (0.028 peak to peak, about 0.29 studs).
- Mantle-minus-hull, breath on vs off: identical at all 8 sampled frames (f50 0.0044 vs 0.0044; f70 0.0140 vs 0.0140; f110 0.0272 vs 0.0272). Breath-only slip is 0.0000.
- Snout, breath-only: largest change 0.0017 at f30 (limit 0.003).
- Lowest Head or Jaw Z over f0-120: 0.0226 at f28.

## Round-4 items

| Item | Verdict | Evidence |
|---|---|---|
| M1: breath lifts the chest (code) | PASS | Lines 336-341: Spine `loc z = -0.010*d + 0.014*b`, Chest `rot = 1.0*d` (no breath pitch), Head `15.5*d - 10*lf + 2.0*b`. Matches the notes. |
| M1: breath visible at the mantle and shoulder | PASS (in substance) | Breath-only edge and centre shift is 0.028 peak to peak (brief asked for at least 0.024). Shoulder-top centre f50 to f70 drops 0.0251 (pass). |
| M1: literal f50 vs f70 pair | NOT MET as written, not a breath problem | Edge point drops 0.0116 (asked for at least 0.024). Mantle-minus-hull changes 0.0096 (asked for at most 0.002). Both come from the sniff roll (`3.5*yw/8`, yaw -6 at f50 to +4.2 at f70) tilting off-centre points. Breath on vs off shows zero slip at every frame. I accept the breath-only test as the real measure. Future rounds should report breath-only numbers (TO 6). |
| M1: snout, low Z, chest vs spine, pitch-up, collision, ground, loop | PASS | Snout 0.0017 (limit 0.003); low Z 0.0226 (at least 0.000); chest vs spine 1.0 (limit 5); head pitch-up 2.0 (limit 30); `collision_free` true with `{}`; `ground_min_z` -0.002 in all four clips; idle f120 vs f0 0.0. |
| M1: evidence | PASS | `_breath_side_r4.png`: f50 and f70 side panels at matching framing, with the ground line, rump, shoulder and nose visible. The two tick lines show the back top lower on f70 at shoulder, mid-back and rump; the drop looks even along the back. The notes call it 2x; the panels are 1100 px, which is legible. |
| M2: fresh act, roar, walk renders | PASS | act f5/20/44/68, roar f12/30/59, walk f0/8 in `_pose_side_r4` and `_pose_tq_r4`, plus the `pclose_*` sheets. All are newer than the last pet write (04:32:25). |
| M2: head and jaw clearance to the chest blocks | PASS | Act f5-68 minimum 0.0116 (f68); roar f0-45 0.0277; walk 0.0231. The builder measured the union of mantle, grey shoulder and chest plate, which is stricter than mantle alone. My 3x crops of act f44 and f68 show the head clear of the mantle front. At f68 the ear and cheek ruff sit on the mantle front corner with a visible seam and no poke-through. |
| M2: neck clause | FAIL (no evidence) | `neck_vs_chest_min` is -0.0418 at act f64 and -0.0332 at rest. The brief asked for at least 0.01 with no visible contact. The builder accepts the intersection on purpose (neck tucked under the cape). No render at f64, and no underside or low view, shows it hidden. The f68 side crop shows no mantle-coloured neck block poking out, which is encouraging, but it is a different frame and says nothing about the underside. See MUST 1. |
| N1: nose lift 10 deg | PASS | Line 341 `-10.0*lf`. ANIM_REFS and notes agree. |
| N2: ear twitch you can see | PARTIAL | 6-frame triangles (33/36/39, 49/52/55, 65/68/71) and 8 deg forward plus 20 deg outward are in the code. The builder's own on/off test gives 345 changed px at 1x and 1957 at 2x. In `_ear_twitch_r4.png` the 1x panels show the ear as a small dark shape behind the first thorns, so the beat does not read at phone size. At 2x it does. See TO 2. |
| N3: sniff roll 3.5 | PASS | Line 338. The effect is small (about 0.1 studs of sideways shoulder motion). |
| N4: ANIM_REFS matches the build | PARTIAL | The builder's notes say it matches. Three numbers do not: roar root drop "-0.05H" (code `drop = 0.10 * H_U`), roar thorns "flatten back 15 deg" (code `-22.0 * tab(TH, f)`), and act kick "shoves back 0.06" (code KICK 0.070). Idle, walk and act thorn figures match. See TO 1. |
| N5: mantle rear rolls into the back | PASS | `rnd 0.50` (capped to 0.45 by blockkit, as the notes say) and `MANTLE_TILT -10`. `game_view.png` shows the rear top edge softened into the back. |
| N6: flat mantle top | Not done (optional) | Still flat. See TO 8. |
| Clip limits: loops, ground, collision, no head shake | PASS | Neck max 7.87 (limit 8); chest vs spine max 2.92 (walk); head yaw max 2.99 deg/f (act); head pitch-up max 6.25 (act, the pop-up look); 0 quaternion flips. |
| Walk, roar, act on the current model | PARTIAL | Renders are current. Walk has only f0 and f8 on this build, so the gait is judged on 2 of 30 frames. Roar f30 shows a dark mouth interior under the jaw, which is the intended growl. See TO 4. |
| Breath at the player's eye | Not provided | No game-camera breath evidence. See TO 3. |

## Model: 8.6/10 - PASS

- Checklist: the badger reads at 64 px and 128 px (`_icons_strip_64.png`, first slot): white face with black bands, grey body, amber crest. The face has slit eyes with an amber accent and no glint (`_close_sheet.png`). Tris 6,544 (cap 15k). Game-view shares: GREY 47.6, MANTLE 10.4, BELLY_D 14.4, AMBER 17.1 (+0.4 hot). Nothing floats in `_model_sheet.png`.
- This round's changes (mantle tilt and rounding, cheek ruff shortened by 0.018, tris down) do not move the silhouette visibly. The score holds at 8.6.
- Weak points that do not block: the side silhouette still reads as a long loaf (length about 2.5 times height, straight flat skirt) and the tail stub is small. See TO 8.

## Clips: 8.4/10 - FIX

- Gains since round 4: the breath now works on the spine, with breath-only shifts of ±0.014 and no mantle slip. Act, roar and walk renders are current. The nose lift (10 deg), sniff roll (3.5 deg) and twitch are in the build. The numeric gates all pass.
- Why 8.4: one round-4 M2 requirement (the neck) is not evidenced. The ear beat is weak at phone size, and the ANIM_REFS claim is three numbers short. Those are fixable in a single pass.

## New MUSTs (blocking 8.5)

**MUST 1. Neck clearance evidence (round-4 M2, neck clause).**
- Current state: the neck block sits -0.042 into the chest blocks at act f64 (-0.033 at rest), by design.
- Fix, evidence first: with the current `pets/BrambleBadger.py`, render act f64, act f68 and rest from (a) the low side camera at z about 0.15 (the `low_below.png` setup) and (b) a low front-left 3/4 that shows the underside of the mantle and the nape. Save 2x crops of the mantle front edge, the nape and the mantle underside. Pass = no MANTLE-coloured Neck geometry visible below the mantle's lower edge, in front of the mantle's front face, or through its top.
- If anything shows: shorten the Neck segment `B.seg((0, -0.42, 0.42), (0, -0.58, 0.41), ...)` so its front end stops inside the mantle footprint (no further forward than the mantle front face at y -0.474 before tilt). Re-run the head and neck clearance over act f5-68 and paste the new numbers into `CLIP_NOTES.md`.
- If nothing shows: keep the tuck, record it as a deliberate deviation in `CLIP_NOTES.md` with the render paths, and the lead can rule on it.

## TO 9+ (after MUST 1)

1. **ANIM_REFS, three stale numbers (N4 claimed done).** In the roar entry change "root goes down -0.05H" to -0.10H (code `0.10 * H_U`) and "thorns flatten back 15 deg" to 22 deg. In the act entry change "shoves back 0.06" to 0.07 (KICK table, line 430).
2. **Ear twitch readable at phone size.** On the game camera it is 345 px at 1x and the ear hides behind the first thorns. Raise the twitch splay from 20 to about 30 deg, or move the ears 0.02 units outward so they clear the crest. Target: at least 1000 px changed at 1x (twitch on vs off, `BADGER_TWITCH` switch).
3. **Breath and sniff at the player's eye.** The current game crops (`pclose_game_idle_33/36/40/70`) cut the head and crest off the top of the frame, so the head-down sniff and the sweeps cannot be judged from them. Re-frame the game camera to include the head, then give a 2x crop of f50 vs f70 (breath on) with the back-top line.
4. **Walk on the current build.** Add walk f15 and f23 (pose_tq and side) so the diagonal pairs and the head dips can be judged across the loop, not from 2 of 30 frames.
5. **Sheet framing.** In `_pose_tq_r4.png` the snout is cut at the left edge in act f5, f20, f44, roar f12/f30/f59 and walk f0. Re-frame so the head is complete.
6. **Report breath-only numbers.** Future rounds should report breath on vs off at the same frame, not f50 vs f70 pairs, because the sniff roll confounds the pair. Also re-run `measure_breath_b0/b1` on the 04:32:25 file. The saved breath JSON is from 04:24, before the last pet write. The values match the code formulas, so they are very likely current.
7. **Breath visibility (optional).** At ±0.014 units the breath is subtle at phone size. If the owner wants it readable, scale the Spine lift to ±0.020 and the head counter-pitch to `+2.9*b` (same ratio, keeps the nose still). Keep the mantle-minus-hull breath-only slip at 0.0000.
8. **Model polish (optional).** Soften the loaf silhouette with a 0.02-unit waist tuck in the flank hull, and add the 0.01-unit crown on the mantle top (N6).

## Pass / fail checklist (round 5)

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Badger reads at 64 px and 128 px | PASS | Icon strips, first slot |
| 2 | Fierce face, no glint | PASS | `_close_sheet.png` |
| 3 | Model tris under cap | PASS | 6,544 |
| 4 | Breath lifts the back as one (breath-only) | PASS | ±0.014 on mantle, shoulder, hull; slip 0.0000 |
| 5 | Snout held (breath-only) | PASS | 0.0017 (limit 0.003) |
| 6 | Literal f50-f70 breath pair | FAIL as written | Sniff roll confounds it; breath-only is the real test (TO 6) |
| 7 | Head and jaw clearance to chest blocks | PASS | act min 0.0116; roar 0.0277; walk 0.0231 |
| 8 | Neck clearance / no visible contact | FAIL (no evidence) | MUST 1 |
| 9 | Act, roar, walk renders current | PASS | After last pet write |
| 10 | Nose lift 10, sniff roll 3.5 in build | PASS | Lines 338, 341 |
| 11 | Ear twitch visible at phone size | PARTIAL | TO 2 |
| 12 | ANIM_REFS matches build | PARTIAL | TO 1 (three numbers) |
| 13 | Walk, roar, act judged across the loop | PARTIAL | TO 4 |
| 14 | Loops, ground, collision, pose limits | PASS | Numbers in the table above |
| 15 | No head shake, no airborne spin | PASS | Head yaw 2.99 deg/f max |
