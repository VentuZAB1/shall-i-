# Cinder ANIM_REFS round 4 (review 3 MUST 1): the site clip for the S-wave travel + the idle head hold; tags tried
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord\ANIM_REFS.md"
t = io.open(P, encoding="utf-8").read()

old = "- **Sakugabooru:** tag search `snake*` returns no tags.\n"
new = """- **Round 4 (review 3 MUST 1), the site clip:** I read the free tag pages `/tags/creature-animation` (2,414 clips),
  `/tags/animals` (540), `/tags/creature`, `/tags/dragon` (217), `/tags/sea-beasts` (3), `/tags/walk-cycle` (369) and
  `/tags/body-mechanics` (76) from their page data (title, tags, Sakugabooru post). I searched them for snake, serpent, eel,
  worm, naga, orochi, Shenron, Haku and eastern dragon. The only serpentine body on the site is **Haku, the white dragon in
  *Spirited Away***: `/tags/creature-animation` -> Sakugabooru **#225387**. `Kanada Dragon` is an effects style, not a dragon.
  The `/tags/dragon` clips are Dragon Ball / Kanada beams, and the `body-mechanics` clips are site-hosted only (they cost
  opens). I stepped the frames on the Sakugabooru post (the same mp4 the site player streams) as canvas contact sheets.
  **No site opens were spent**, nothing was downloaded. The Wikimedia snake clips (S1, S2) stay as study notes.
- **Sakugabooru:** tag search `snake*` returns no tags.
"""
assert old in t
t = t.replace(old, new, 1)

SITE = """## D - SITE: Haku the river dragon (*Spirited Away*), Sakugabooru #225387
Tags `spirited_away`, `takeshi_inamura`, `yoshihiro_osugi`, `creatures`, `flying`, `cgi`, `3d_background`; 47 s,
23.997 fps. Haku is a long-bodied eastern dragon, the closest thing on the site to a serpent body.

| # | observation | frames (24 fps) |
|---|---|---|
| D1 | **The bend travels head -> tail.** Low over the ground, the head and neck stay on a straight, level line. A big arch forms just behind the forelegs and runs back along the body, leaving the front straight again. The bend takes ~16-20 frames (~0.7-0.8 s) to pass along the visible body. | f146-f186 (arch forms f154, peaks mid-body f162, gone to the rear by f178) |
| D2 | **Gliding side view:** smaller humps keep running from the neck to the tail while the head holds its line. The amplitude is smallest at the neck and largest mid-body to the rear. | f636-f680 (sampled every 4 f) |
| D3 | **The head holds still while the body moves.** In the riding close-up the head stays level, the gaze locked forward, and the motion is in the body and mane behind it. No head bob or shake. | f696-f760 |

**Use:** D1 + D2 back the slither: the wave runs head -> tail with a lag per bone, the amplitude grows to mid-body (U2),
and the reared neck counter-yaws so the head stays on its line. This also backs the lead's ruling on the head -> tail
direction. D3 backs the idle: the breaths and sway live in the neck and body while the head counter-pitches and
counter-yaws to stay level (C1). The slow, minimal-motion idle also matches the site's *Kaiju No. 8* K8c (#254909,
cited in the Titan's ANIM_REFS): weight reads through stillness.

"""
t = t.replace("## S1 - lateral undulation (sand)", SITE + "## S1 - lateral undulation (sand) (Wikimedia study notes)", 1)
t = t.replace("## S2 - reared cobra", "## S2 - reared cobra (Wikimedia study notes)", 1)
t = t.replace("- **slither = the \"walk\" clip (48 f loop, U1-U4).**", "- **slither = the \"walk\" clip (48 f loop, D1-D2 + U1-U4).**")
t = t.replace("- **idle (120 f loop): ember breathing (C1, C2).**", "- **idle (120 f loop): ember breathing (D3 + C1, C2).**")
t = t.replace("`breath1` f30 / `breath2` f90 for the vent smoke;", "`smoke1` f30 / `smoke2` f90 for the vent smoke;")
old_m = t[t.index("- **act_molt (110 f): the crown sheds (#9 + U1).**"):]
new_m = """- **act_molt (110 f): the crown sheds (#9 + U1).** f0-18 the neck arches 22.5 deg pitch-up in total (7.5 per bone,
  round 4), head level. f18-42 the blades lift one by one 35 deg (3-frame lag, round 4), `lift1` f22. f40-62 the centre
  blade lifts furthest and holds while the outer blades drop back, `lift2` f48, `shed` f56. f62-86 a ripple runs tail -> head
  along the body (plan; 6 deg per body / tail bone, the Spine 4.5). f84-110 the blades reseat in reverse order, slower than
  they rose (#9): the centre blade takes 11 f (f84-95). Exact rest.
"""
t = t.replace(old_m, new_m)
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
