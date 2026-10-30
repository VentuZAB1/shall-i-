# review 3 M1: the two animationreference.org site clips (tag page -> Sakugabooru frames, no opens) + the re-timed act
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher\ANIM_REFS.md"
t = io.open(P, encoding="utf-8").read()

old_log = "- **Sakugabooru:** no crab tag.\n"
new_log = """- **Round 4 (review 3 M1), the site clips:** I read the free tag pages `/tags/walk-cycle` (369 clips), `/tags/creature-animation`
  (2,414), `/tags/creature`, `/tags/animals` (540), `/tags/sea-beasts` (3), `/tags/body-mechanics` (76), `/tags/dragon` (217) and
  `/resources/locomotion-animation-reference`. I listed each clip's title, tags and Sakugabooru post from the page data, and
  stepped the frames on the Sakugabooru posts (the same mp4 the site player streams) as canvas contact sheets. **No site
  opens were spent** and nothing was downloaded. No crab or insect tag exists. The closest multi-leg gait on the site is the
  Ohmu in *Nausicaa* (S1). The limb raise-hold-return is James Baxter's dancing horse (S2). I looked at and rejected the
  Catbus (*Totoro*, #264357: a mammal gallop with stretch / gather, wrong for a crab), the *Kaiju No. 8* fist (#254909: the
  fist is already raised when the shot starts), and the *Pokemon* dance (#118237) and *Dungeon Meshi* (#250049): no single-limb hold.
  The `body-mechanics` clips are site-hosted only, so they would cost opens.
- **Sakugabooru:** no crab tag.
"""
assert old_log in t
t = t.replace(old_log, new_log, 1)

old_h = "## C1 - rock crab walk (4.6-7.0 s)"
SITE = """## S1 - SITE: the Ohmu run (*Nausicaa of the Valley of the Wind*), multi-leg gait
`/tags/creature-animation` -> Sakugabooru **#270689** (tags `takashi_nakamura`, `nausicaa_of_the_valley_of_the_wind`, `creatures`,
`running`; source "BD (Ohmu AD: Tadakatsu Yoshida)"). The shot used is the Ohmu legs close-up (front view, on sand), 82.9-85.2 s
= frames f1987-f2042 at 23.976 fps. The drawings change on twos.

| # | observation | frames |
|---|---|---|
| O1 | **Two alternating leg sets.** At every drawing roughly half of each side's legs are planted wide and the other half are arched high in swing. From one drawing to the next (f1991 -> f1993 -> f1995 ...) the planted and swinging legs swap, set by set. Neighbouring legs on one side are never in the same phase. | f1991-f2001 |
| O2 | **The shell stays level.** Its top edge holds the same height while the legs cycle. The motion is all in the legs (the same as C1 R1). | f1987-f2042 |
| O3 | The swing legs arch high because this is a run (a set swaps about every 4 frames, a cycle of about 8 = ~10 f at 30 fps). At a walk the same alternation runs slower and lower. | f1991-f1999 |

**Walk check (the review asked):** the site gait agrees with the Wikimedia read: alternating leg sets (= our tripods
L1/R5/L3 vs R4/L2/R6), a level shell (bob 0.010), and the legs doing the work. No contradiction, so **the walk is unchanged**.
The Ohmu's high leg arch is a run feature; our 30 f crab walk keeps the low lift 0.07 (C1 R1, R4).

## S2 - SITE: James Baxter's dancing horse (*Adventure Time* #243 "Horse and Ball"), one limb raise / hold / return
`/tags/creature-animation` -> Sakugabooru **#170480** (tags `james_baxter`, `adventure_time`, `animals`, `creatures`,
`dancing`, `performance`). The horse dances on its hind legs, 0.0-4.6 s (f0-f110), drawings on twos.

| # | observation | frames (24 fps) | at 30 fps |
|---|---|---|---|
| H1 | **Up:** after a buck (f28-30) it rears, and the right foreleg rises to point straight up. | f34 -> f42 (8 f) | ~10 f |
| H2 | **Hold:** the raised foreleg stays up while the hips sway. The OTHER foreleg swings out and back on the beat, so the hold never looks frozen. | f42 -> f90 (48 f, 2 s) | ~60 f |
| H3 | **Down:** the raised foreleg drops back to the chest quickly, faster than it rose. | f90 -> f92/94 (2-4 f) | ~3-5 f |

**Use:** each wave rises slower than it returns (H1 vs H3, the same as C2 F3). Each top is a real hold (H2). While the
crusher holds out after the waves, the small cutter claw taps (H2's other limb working during the hold).

"""
assert old_h in t
t = t.replace(old_h, SITE + "## C1 - rock crab walk (4.6-7.0 s) (Wikimedia study notes)", 1)
t = t.replace("## C2 - fiddler crab wave", "## C2 - fiddler crab wave (Wikimedia study notes)", 1)

old_act = t[t.index("- **act_semaphore (100 f): the fiddler wave (F1-F3).**"):]
new_act = """- **act_semaphore (120 f, round 4): the fiddler wave (F1-F3 + S2).** f0-18 stand tall: the body rises 0.10 BU with
  pitch -5 (review 3 N2), and the crusher unfolds up. Three SLOW display arcs follow. Each top holds 4 f: f26-30 / f48-52 /
  f70-74, with peaks and events `wave1` f28, `wave2` f50, `wave3` f72 (H2). Troughs are at f38 / f60. The up-sweep takes
  10 f and the return 8 f (H1 vs H3, F3). The top is the claw raised high (F1); the trough swings it down and forward in
  front (F2). Measured top <-> trough rotation in world space: merus 36.7 deg, carpus 42.1 deg, claw 36.7 deg. f74-80 the
  claw points out and holds while the cutter taps twice (`tap1` f84, `tap2` f90, S2's other limb). f90-104 the claw
  swings in first, then folds down. f104-120 exact rest. Legs planted every frame.
"""
t = t.replace(old_act, new_act)
t = t.replace("- **roar (60 f): clack threat (#6 + #5).** f0-14 the body rises 0.05 H and the claws lift forward 25 deg",
              "- **roar (60 f): clack threat (#6 + #5).** f0-14 the body rises 0.05 H and the claws lift forward 30 deg (review 3 N3)")
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
