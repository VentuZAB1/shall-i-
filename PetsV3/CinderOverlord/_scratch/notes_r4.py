# Cinder CLIP_NOTES + MODEL_NOTES round 4 (review 3)
import io
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"

P = ROOT + r"\CLIP_NOTES.md"
t = io.open(P, encoding="utf-8").read()
R4 = """## ROUND 4 (2026-10-27, after `_review/CinderOverlord_review3.md`, REVISE 7/10)
- **MUST 1, site refs for idle + walk:** `ANIM_REFS.md` section D: Haku in *Spirited Away* (site `/tags/creature-animation`
  -> Sakugabooru #225387). D1 / D2 = the bend runs head -> tail with the head on a level line (f146-186, f636-680); D3 = the
  head holds level while the body moves (f696-760). The tags tried are listed. No opens spent.
- **MUST 2, chest:** the molt ripple on the **Spine (the chest base) is now 4.5 deg** (Body / Tail bones keep 6).
  Measured per bone (`_scratch/ang_probe.py`): Spine max **4.5** (<= 5), each Neck bone max **7.5** (<= 8, NICE 6 margin).
- **MUST 3, centre blade reseat:** Crown_3 rises at a peak of **5.18 deg/f** and now reseats at **4.62 deg/f** (f84-95,
  was f84-92 at 6.3). The outer blades rise at 5.81 and fall at 4.15.
- **NICE 3:** the blades lift one by one with a **3-frame** lag (was 2), so the sequence reads at game distance.
- **NICE 6:** the molt neck arch is 22.5 deg in total (7.5 per bone), and the head counter-pitch is 20.5.
- **Gate (step 1, `_scratch/clipgate_r4.txt`):** collision_free **true**, ground_min_z -0.006 in every clip, linear 0,
  idle + walk loops 0 / 0. Events unchanged (molt `lift1` f22, `lift2` f48, `shed` f56).
- **Renders:** molt beats f0-110 from three fixed cameras: `renders/_molt_r4_front.png`, `_molt_r4_side.png`,
  `_molt_r4_tq.png`.

"""
i = t.index("## Numbers (step 1)")
t = t[:i] + R4 + t[i:]
t = t.replace("- Pose limits: each neck bone <= 8 deg (molt arch 24 deg over three bones);",
              "- Pose limits (round 4): each neck bone <= 7.5 deg (molt arch 22.5 deg over three bones); the Spine (chest base) <= 4.5;")
t = t.replace("f0-18 the neck arches 24 deg, head level; f18-36 the blades lift one by one (2-frame lag) 35 deg",
              "f0-18 the neck arches 22.5 deg, head level; f18-42 the blades lift one by one (3-frame lag, round 4) 35 deg")
t = t.replace("f84-104 the blades reseat in reverse order, slower than they rose;",
              "f84-104 the blades reseat in reverse order, slower than they rose (the centre blade over f84-95);")
io.open(P, "w", encoding="utf-8", newline="\n").write(t)

P = ROOT + r"\MODEL_NOTES.md"
t = io.open(P, encoding="utf-8").read()
M4 = """## ROUND 4 (2026-10-27, after `_review/CinderOverlord_review3.md`, REVISE 7/10)
- **MUST 5, outclass:** the body PLUM_OBS is lifted at the same wine hue, (144, 80, 96) -> **(160, 87, 102)** (H 347,
  S 0.46). I tried (166, 90, 106) first. At 64 / 128 px both read as the same dusty wine-rose, a little pink-leaning next to
  the red Ivonrath (`_scratch/body_cmp.png`: 166 | 160 | Ivonrath at 128 px). So I stopped at 160 as the brief said. The
  pink tint comes from the hue (H 347 leans toward magenta), not the value. If it still reads pink, the fix is the hue
  (toward H ~355, e.g. (160, 86, 94)), which I did not change without a ruling. In `_icons_strip_128.png` it now reads as
  bright as Rex / Leviathan, no longer the darkest serpent. The obsidian saddle (OBS_D 62,50,64) and the lava cores are
  unchanged.
- **MUST 4, one set of numbers:** `_scratch/gate_r4.json` is the ONLY gate-number file (written after this run). The
  18:13 files were renamed `_scratch/STALE_1813_*` (gate_clip_out.txt was an even older round-2 run: tris 11,124, gold 25 /
  19). From gate_r4.json:
  - gold at 64 px (kit counter `_tools/game_icon.py`): **portrait 27, game 20**.
  - shares, flat_game.png, every figure pixel to the nearest palette colour: **body PLUM_OBS 42.8 %, obsidian OBS_D 35.7 %**
    (targets >= 40 / <= 40).
  - side 49.1 / 23.6, tq 41.4 / 26.9.
- Model unchanged otherwise: tris 10,852, H 2.232. Renders: `renders/_model_sheet.png`, `_icons_strip_64.png` /
  `_128.png`, `_icons2_strip_*`, `gamelook_*.png`.

"""
i = t.index("## ROUND 3")
t = t[:i] + M4 + t[i:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
