# Cinder MODEL_NOTES: the lead's hue ruling (ember) replaces the MUST 5 colour paragraph of ROUND 4
import io
P = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord\MODEL_NOTES.md"
t = io.open(P, encoding="utf-8").read()
a = t.index("- **MUST 5, outclass:**")
b = t.index("- **MUST 4, one set of numbers:**")
NEW = """- **MUST 5 + lead hue ruling (2026-10-27): EMBER.** The wine body (160, 87, 102) read as a pink worm, so the hue moved to
  fire. Comparison: `_scratch/hue_cmp.png`. It shows rows r4-now / A / B / A2 / B2 at 128 and 64 px next to Ivonrath,
  InfernoPhoenix and ThunderRex. The brief's "Fire-egg Rex" is ThunderRex, the only Rex built.
  - A = ember body (166, 66, 50); B = oxblood (160, 50, 56). Both have the warm ash belly (222, 194, 158).
  - With the old ROSE accent (255, 96, 150), **A and B still showed pink at 64 px**: the vent slits, eye slits and crown
    inner edges. So I added A2 / B2 with the accent turned to a hot ember (255, 84, 48).
  - **Pick: A2.**
    - It reads FIRE at 64 px: an ember / cinder body with hot orange-red slits around the lava cores.
    - It has no pink left anywhere.
    - It is clearly apart from Ivonrath's crimson: A2 leans orange, while B / B2 sit right on Ivonrath's red.
  - **Applied:** PLUM_OBS **(166, 66, 50)**, PALE_S **(222, 194, 158)**, ROSE (the accent) **(255, 84, 48)**.
  - **Kept:** OBS_D (62, 50, 64) saddle and rings, LAVA cores, GOLD / GOLD_D crown.
  - The rig has one body tone (PLUM_OBS), so there was no separate shadow tone to shift.
"""
t = t[:a] + NEW + t[b:]
a = t.index("- **MUST 4, one set of numbers:**")
b = t.index("- Model unchanged otherwise:")
NEW4 = """- **MUST 4, one set of numbers:** `_scratch/gate_r4.json` is the ONLY gate-number file. It was re-written after the ember run.
  The 18:13 files were renamed `_scratch/STALE_1813_*`; gate_clip_out.txt was an even older round-2 run (tris 11,124, gold
  25 / 19). From gate_r4.json:
  - **Gold at 64 px** (kit counter `_tools/game_icon.py`): **portrait 35, game 20.**
    - The portrait rose from 27 because the crown's inner edges are now ember, not rose. The counter's hue window
      (29-58 deg) catches the gold / ember edge blend: 32 of the 35 pixels are in the crown rows, 3 on the body.
  - **Shares**, flat_game.png, every figure pixel to the nearest palette colour: **body PLUM_OBS 42.4 %, obsidian OBS_D
    34.1 %** (targets >= 40 / <= 40); ember accent 6.8, lava 2.8.
  - Side: body 48.9, obsidian 22.5, warm pale **10.3**. Tq: body 41.4, obsidian 25.8, pale **11.6** (the pale band keeps its
    share).
- **Step 1 after the hue change** (`_scratch/clipgate_r4.txt`): collision_free true, ground_min_z -0.006, linear 0, loops 0 / 0.
"""
t = t[:a] + NEW4 + t[b:]
io.open(P, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
