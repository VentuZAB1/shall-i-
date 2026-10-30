import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\CLIP_NOTES.md"
t = io.open(P, encoding="utf-8").read()
R5 = """## ROUND 5 (2026-10-27, after `_review/CoralCrusher_review4.md`, APPROVED 8/10): NICE pass, then EXPORT
- The wave tops are now **held 8 f** (f26-34 / f49-57 / f72-80). Events sit on the hold centres: `wave1` f30, `wave2` f53,
  `wave3` f72 + 4 = **f76**.
- The down-stroke is now **5 f** (trough f39 / f62; S2 H3's drop is 3-5 f) and the up-sweep 10 f.
- The act stays **120 f**. The time came out of the rest tail:
  - point out f80-86;
  - cutter taps **f90 / f96** (`tap1`, `tap2`);
  - swing in f96-103, fold down f103-110;
  - exact rest f110-120.
- The act is keyed every frame so the odd-frame troughs land exactly (Lua 58.7 KB).
- Step 1 (`_scratch/clipgate_r5.txt`): collision_free **true**, ground_min_z -0.013, linear 0, loops 0 / 0, slide 0.002.
- `renders/_wave_strip.png` re-rendered: tq + game, every 2 f, f18-82, holds / troughs labelled. I checked it: the three
  holds are still poses, and each drop to the in-front trough is visible.

"""
i = t.index("## ROUND 4")
t = t[:i] + R5 + t[i:]
# walk row: the Ohmu note
old = "| walk | 30 | yes | `sand1` 13.8, `sand2` 28.8 (tripod touch-downs) | diagonal scuttle at yaw 45 (C1 R2),"
assert old in t
t = t.replace(old, "| walk | 30 | yes | `sand1` 13.8, `sand2` 28.8 (tripod touch-downs) | diagonal scuttle at yaw 45 (C1 R2; the site Ohmu clip S1 is a RUN: it supports the leg alternation, not the walk timing),")
a = t.index("| act_semaphore | 120 | no |")
b = t.index("\n", a) + 1
t = t[:a] + ("| act_semaphore | 120 | no | `wave1` 30, `wave2` 53, `wave3` 76, `tap1` 90, `tap2` 96 | THE FIDDLER WAVE (round 5): "
             "stand tall f0-18 (rise 0.10 BU, pitch -5); three slow arcs with 8-f held tops (f26-34, f49-57, f72-80), troughs "
             "f39 / f62, 10 f up / 5 f down; f80-86 the claw points out and holds while the cutter taps twice (f90, f96); "
             "f96-110 swing in, then fold down; exact rest f110-120. Legs planted every frame. |\n") + t[b:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
