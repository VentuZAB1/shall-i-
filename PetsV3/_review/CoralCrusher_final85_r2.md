# Coral Crusher - FINAL GATE round 2 (8.5 bar), 2026-10-28

**Model: 8.5/10 - PASS. Clips: 8.0/10 - FIX.** The clips need one more pass before they go into the game (owner bar 8.5).
Round 1 of this gate was model 7.5 / clips 7.5. The model fixes landed clearly. The clip fixes landed, but they are small
enough that I can't confirm them from stills, and one of them (CM3, walk timing) rests on a lead ruling rather than the
owner's written sign-off.

## What I looked at
- `renders/_model_sheet.png` (tq, front, side, back), `_close_sheet.png`, `close_crushertq.png`, `close_crusherin.png`
  (pincer gape and molars), `gamelook_game.png`, `flat_game.png`, `flat_side.png`, `model_tq.png`
- Icon strips: `renders/_icons_strip_128.png`, `_icons3_strip_128.png` (crab beside Kappa, Turtle, Kraken, Hammerjaw, Orca)
- `CoralCrusher_portrait_alt.png` (Index portrait, game-camera render of idle f0)
- `renders/_wave_strip.png` (tq and game, f18-82)
- `renders/_pose_tq_sheet.png` (idle f0-110, walk f0-23, roar, act f18-110)
- `renders/_act_eyes_roll.png` (act face, f0 / f30 / f41 / f53, tq and front)
- Notes: `CoralCrusher/MODEL_NOTES.md` (FINAL 8.5 section), `CLIP_NOTES.md` (FINAL 8.5 section), `ANIM_REFS.md`
  (lead ruling for CM3), `_scratch/shares_all_f85.json`, `_scratch/shares_strict_f85.json`
- Not re-run: the headless gate. I used the numbers the notes report (collision_free true, ground_min_z -0.013,
  loops 0/0, idle foot drift 0, walk slide 0.002). Not opened: the Sakugabooru posts.

---

## 1. MODEL: 8.5/10 - PASS

**Round 1 MUSTs, checked**
- **MM1, colour: PASS.** The copper is now a saturated rust copper (BRONZE 214,110,70; BRONZE_D 150,74,50; SHELL_D 80,46,34).
  The model sheet reads orange-copper, and `gamelook_game` reads rust red-brown, not tan. Against the icon strip it sits
  clearly apart from the teal Kappa and Turtle, the red Kraken and the navy Hammerjaw. It is now the pet's own colour,
  with the rose accent on top.
- **MM2, pale underside: ACCEPTED BY LEAD RULING, not counted** (per the coordinator's message). The numbers are as
  reported: side 1.6 %, game 2.2 %, back 5.6 %. The cream rim is visible at the rear and in the portrait. The builder's
  own notes say the owner's written no-pale sign-off is still needed (MODEL_NOTES, MM2). That is a different sign-off
  from the lead ruling. See the flags below.
- **TO 9+ 1, legs 20 % thicker: PASS.** The merus reads chunkier in `_model_sheet` (bottom-left). The six legs no longer
  read as stilts in the tq view.
- **TO 9+ 2, pincer gape and molars: PASS.** `close_crushertq` and `close_crusherin` show a clear gape between the fixed
  finger and the dactyl, with four molars on the inner edges. The claw now reads as a pincer, not a mitt.
- **TO 9+ 3, two taller rose clusters on the dome: PASS, with a NICE.** The clusters read in the tq view and the model
  sheet. At close range they look like straight pink tubes (`close_crushertq` top left). See N1.
- **TO 9+ 4, walk claw sway: not verifiable from stills.** See CM-R2-3.

**Other checks**
- Icon strip at 64 and 128 px: the crab reads as a crab with claws up, next to the other Water pets. PASS.
- Index portrait (`CoralCrusher_portrait_alt.png`): reads well, and it is the game-camera render. PASS.
- Tris 12,644 (cap 15k). PASS.
- Value shares (all figure pixels): BRONZE 47-52 %, SHELL_D 16-20 %, rose 9-14 %, pale 0.8-2.2 % (back 5.6 %).
  The shares match the notes. The pale share is the accepted deviation.

**Model NICE (does not block)**
- **N1:** the dome rose clusters are straight cylinders. Taper them (a wider ROSE_D base, a pointed ROSE tip), so they
  match the spikes elsewhere on the pet.

---

## 2. CLIPS: 8.0/10 - FIX

**Round 1 MUSTs, checked**
- **CM1, idle breathes: PARTIAL.** The breath is real. `_pose_tq_sheet` idle f30, f45 and f62 show the crusher at
  different heights, and the tap at f70 still reads. But the amplitude is ±3 deg on a claw held at 20 deg. At game
  distance that is close to invisible, so the idle still looks like a held guard pose. The body bob is 0.008 BU, which is
  also too small to read. See CM-R2-1.
- **CM2, secondary motion on the act: PARTIAL.** The eyestalks track the crusher. The probe table in CLIP_NOTES shows the
  left eye's angle to the tip changes by about 13.5 deg between the tops and the troughs. The right eye changes by only
  about 5 deg (15.8 -> 20.7), so the two eyes do not read as one tracking pair. The shell roll is ±2 deg, which I cannot
  see in `_wave_strip`. The eye glance-away fix is in: `_act_eyes_roll` f0-f53 shows no right-eye glance off the claw.
  See CM-R2-2.
- **CM3, walk timing: CLOSED BY LEAD RULING, not by the owner.** ANIM_REFS now records that the Wikimedia crab footage
  (C1) sets the walk timing and that the site Ohmu clip (S1) backs only the leg alternation. That is written down, but
  the owner's animation-references rule asks for site clips, and a lead ruling does not change an owner rule. See the
  flags below.

**Other checks**
- Gate numbers (as reported, not re-run): collision_free true; ground_min_z -0.013; linear 0; idle and walk loops 0/0;
  idle foot drift 0; walk slide 0.002. Events unchanged (act wave1 30, wave2 53, wave3 76, tap1 90, tap2 96).
- Act rest: exact at f110-120 (`_pose_tq_sheet` act f110). PASS.
- No head shakes, no airborne moves. The eye swing is one smooth arc per beat, not a left-right shake. PASS.
- The walk, roar and idle poses are unchanged in silhouette. PASS.

**Clip MUSTs (to reach 8.5)**
- **CM-R2-1 - idle breath too small to read.** In `idle(k)` (L457), raise the crusher guard breath from ±3 deg to **±5 deg**
  (the lift runs 15-25 deg, the same 35 f period, troughs f45 and f80, peak f62). Keep the f70 tap. Check by eye on the
  pose sheet at f45 / f62 / f80: the claw height should differ by a step you can see at 64 px.
- **CM-R2-2 - act secondary motion needs to read.** In `act_semaphore` (L538-580):
  - raise the shell roll on each peak from ±2 deg to **±3 deg**;
  - bring the right eye's track up so its angle to the tip swings at least **10 deg** between the tops and troughs,
    matching the left (currently about 5 deg);
  - keep the rest exact at f110-120, and re-check collision_free and foot drift 0.
- **CM-R2-3 - show the walk sway, then tune it.** The 4 deg crusher sway is not visible in a 30 f still strip. Render an
  animated preview (the walk f0-29 every 2 f at the game camera, as a strip or a GIF) and confirm the sway reads. If it
  does not, raise it to 6 deg and re-run the gate.
- **CM-R2-4 - the walk timing needs the owner's sign-off, or a site clip.** This is a process item, not a clip change.
  Either the owner writes that the Wikimedia crab footage sets the walk timing (the owner's rule allows that only in
  writing), or the builder adds one animationreference.org walk clip that supports the 30 f cycle. Until then, the
  walk's timing citation stays open.

---

## 3. Flags for the lead and the owner
1. **MM2 pale underside.** The lead ruled it accepted. The builder's own notes say it still needs the owner's written
   no-pale sign-off. Please get that sign-off before the pet goes into the game. This does not change the score, per the
   ruling.
2. **Export status.** CLIP_NOTES says the pet was exported (`C:\cdimp\CoralCrusher.fbx`, 01:48) at the round-1 clip state.
   The owner bar is 8.5 for anything that goes into the game. Clips are 8.0, so the export should be re-done after
   CM-R2-1 to CM-R2-3, and re-gated, before it is used.
3. **CM-R2-4 (walk timing).** Closed by a lead ruling, not by the owner's rule. Needs the owner's sign-off or a site clip.

---

## 4. Pass / fail checklist (round 2)

| # | check | result |
|---|---|---|
| 1 | MM1 rust copper, reads apart from the lineup in game | PASS |
| 2 | MM2 pale underside >= 4 % | ACCEPTED by lead ruling (1.6 % side / 2.2 % game), not counted |
| 3 | TO 9+ 1 legs 20 % thicker | PASS |
| 4 | TO 9+ 2 pincer gape ~0.06 H, molars | PASS |
| 5 | TO 9+ 3 two rose clusters on the dome | PASS (N1: taper them) |
| 6 | TO 9+ 4 walk claw sway visible | NOT VERIFIABLE from stills (CM-R2-3) |
| 7 | Icon strip 64 / 128 px, portrait | PASS |
| 8 | Tris <= 15k (12,644) | PASS |
| 9 | Gate numbers (as reported, not re-run) | PASS |
| 10 | CM1 idle breath readable at game distance | PARTIAL (CM-R2-1) |
| 11 | CM2 act secondary motion readable (both eyes, shell roll) | PARTIAL (CM-R2-2) |
| 12 | Act rest exact, no head shakes, no airborne moves | PASS |
| 13 | CM3 walk timing backed by a site clip or the owner's written ruling | OPEN (CM-R2-4) |

**Model 8.5/10 - PASS. Clips 8.0/10 - FIX.** Send the next round with: the idle pose sheet at f45 / f62 / f80, the act
wave strip with the new roll and eye values, the walk sway strip (f0-29 every 2 f, game camera), and the owner's
written walk-timing sign-off or the site clip.
