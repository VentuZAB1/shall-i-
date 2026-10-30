# CLIP_NOTES round 4 (review 3: M1 site refs, M2 wave re-timed, N2, N3)
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\CLIP_NOTES.md"
t = io.open(P, encoding="utf-8").read()

R4 = """## ROUND 4 (2026-10-27, after `_review/CoralCrusher_review3.md`, APPROVED WITH FIXES 8/10)
- **M1, site refs:** `ANIM_REFS.md` S1 = the *Nausicaa* Ohmu run (site `/tags/creature-animation` -> Sakugabooru #270689,
  f1987-f2042: alternating leg sets, level shell). It agrees with the Wikimedia read, so **the walk is unchanged**.
  S2 = James Baxter's dancing horse (site `/tags/creature-animation` -> Sakugabooru #170480: raise f34-42, hold f42-90 while
  the other foreleg works, quick drop f90-92). No site opens spent. The tags tried and the rejected clips are in the log.
- **M2, the wave re-timed (act length 120):** three slow display arcs. The tops hold 4 f (f26-30 / f48-52 / f70-74);
  `wave1` f28, `wave2` f50 and `wave3` f72 sit on the held peaks. Troughs at f38 / f60; the up-sweep takes 10 f, the
  return 8 f. Top = the claw raised high; trough = swung down and forward in front. Rotation between top and trough
  (world, `_scratch/swing_probe.py`): **merus 36.7 deg, carpus 42.1 deg, claw 36.7 deg** (all >= 30). After the waves
  (f74-80) the claw points out and holds while the cutter taps (`tap1` f84, `tap2` f90). f90-104 it swings in first, then
  folds down. f104-120 exact rest.
  - A first try waved only the carpus (8 <-> 44 deg). Its "peak" folded the claw BACK over the shell, lower, not up
    (`_scratch/tip_probe.py`). The final keys move the merus, spread, carpus and palm together.
  - Two collision-free limits shaped the trough. With the merus below ~16 deg and the claw spread out, the carpus cut into
    the front rim (`collide_where`: 74-112 tri pairs at f38-41). So the trough keeps the merus at 16 and brings the claw IN
    (spread 6); the palm drop (-40) carries the "down".
- **N2:** the act stands taller: body rise 0.05 -> **0.10 BU**, pitch -3 -> **-5**. All six feet stay planted (foot drift
  0.0 every frame, `_scratch/plant_probe.py`).
- **N3:** the roar claws lift to **30 deg** (from 25); the clacks stay cocked open 30 deg.
- **N1 (optional belly dome):** not done. It is a model change for a view the game camera never shows; it can go into a
  later model pass if wanted.
- **Gate (step 1, `_scratch/clipgate_r4.txt`):** collision_free **true**, ground_min_z -0.013 (rest), linear 0, idle loop
  0 / 0, walk loop 0 / 0, slide 0.002, foot_z_var 0.001.
- **Renders:** `renders/_wave_strip.png` (tq + game, every 2 f, f18-78, tops / troughs labelled);
  `renders/_pose_tq_sheet.png` rebuilt with the new roar + act beats (the round-3 act renders moved to `_scratch/old_r3_poses/`).

"""
i = t.index("## Numbers (step 1)")
t = t[:i] + R4 + t[i:]

old_row = t[t.index("| act_semaphore | 100 | no |"):]
old_row = old_row[:old_row.index("\n") + 1]
new_row = ("| act_semaphore | 120 | no | `wave1` 28, `wave2` 50, `wave3` 72, `tap1` 84, `tap2` 90 | THE FIDDLER WAVE (round 4): "
           "stand tall f0-18 (rise 0.10 BU, pitch -5); three slow arcs with 4-f held tops (f26-30, f48-52, f70-74), troughs "
           "f38 / f60, 10 f up / 8 f down; f74-80 the claw points out and holds while the cutter taps twice (f84, f90); "
           "f90-104 swing in, then fold down; exact rest f104-120. Legs planted every frame. |\n")
t = t.replace(old_row, new_row)
t = t.replace("| roar | 60 | no | `clack1` 22, `clack2` 30, `clack3` 38, `bubble` 24 | CLACK THREAT: a short crouch f0-4, the body rises 0.05 H and both claws lift forward 25 deg",
              "| roar | 60 | no | `clack1` 22, `clack2` 30, `clack3` 38, `bubble` 24 | CLACK THREAT: a short crouch f0-4, the body rises 0.05 H and both claws lift forward 30 deg (round 4)")
t = t.replace("The fiddler wave: the crab stands tall and waves its giant crusher claw three times like a semaphore, then answers\nwith two taps of the small claw.",
              "The fiddler wave: the crab stands tall and waves its giant crusher claw in three slow arcs, holding each top, then\nanswers with two taps of the small claw.")
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
