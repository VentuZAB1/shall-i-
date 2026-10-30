import io
T = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


TXT = """## EYE ROUND (2026-10-28, after `_review/CoralCrusher_final85_r4.md`: still PASS 8.5 / 8.5; eye follow not shown at phone size) - EXPORTED 05:24
Backups:
- the 04:43 (9+) export: `_scratch/CoralCrusher_exported_9plus.py`
- this export: `_scratch/CoralCrusher_exported_eyes_r4.py`

The patch is `_scratch/fix_eyes_r4.py`.

- **Geometry (model only, no clip keys changed):**
  - `ES, EB = 1.25, 1.20`: the eyestalk vector is x1.25, (0.02, -0.055, 0.07) -> (0.025, -0.069, 0.0875).
  - The bulb, its offset, the eye (socket / rose slit / black slit pupil, sc 1.1 -> 1.32) and the slate lid are x1.2.
  - The stalk thickness and the joint anchor are unchanged.
  - The look stays fierce: dark copper bulb, black socket, narrow rose slit, black slit pupil, angry slate lid at 18 deg.
    The eyes stand a little taller over the front rim; I don't think they read as cartoony.
  - `renders/_eyes_r4_face.png` shows before / after, front + high 3/4; `renders/_model_sheet.png` (05:25).
- **Phone-size eye travel** (`_scratch/eye_px.py`, game camera at 1x = **390 px**, fixed camera aimed at rest):
  - Projected per eye:
    - tip = the eye vertex farthest from the joint.
    - cen = the slit-eye cluster.
    - own = the eye's motion on screen minus where the same point would sit if rigid with the Spine (the body roll / bob
      taken out).
  - Results, top f30 -> trough f41 (before -> after, px):

    | measure | eye | before | after |
    |---|---|---|---|
    | own motion, cen | L | 4.3 | **5.5** |
    | own motion, cen | R | 5.8 | **7.2** |
    | own motion, tip | L | 5.5 | **6.6** |
    | own motion, tip | R | 6.2 | **7.4** |
    | total travel, tip | L | 10.8 | **12.4** |
    | total travel, tip | R | 6.4 | **7.2** |
  - At the second trough (f66) the after values are own cen 6.2 (L) / 6.7 (R) and total tip 11.0 / 6.3.
  - The tops (f30 / f53 / f76) are identical frames.
  - Pass >= 4 px: met for both eyes at both troughs. Before the change it was already 4.3-6.2 own; the review's 1-3 px
    was an estimate.
  - Raw data: `_scratch/eyepx_before.txt` / `eyepx_after.txt`.
- **Claw over the right eye:**
  - Ray cast from the game camera to every vertex of each eye's front cluster: **vis 1.0** at f30 / 36 / 41 / 44 / 53 / 60
    / 62 / 66 / 76 for both eyes, so no other bone's faces are in front.
  - Seen in `renders/_eyes_r4_game1x.png`: f30 / 41 / 53 / 62 / 66, the full 390 px frame plus the eye box x4
    (nearest-neighbour). At the troughs the crusher's lower edge passes just above the right stalk and does not cover it.
  - `renders/_eyes_r4_game_cmp.png` compares the eye box before vs after at f30 / f41 / f66.
- **Step 1** (`_scratch/export_eyes_r4.txt`):
  - collision_free **true** (claw vs Eye_L / Eye_R are in check_pairs); ground -0.013 everywhere.
  - Linear 0; loops 0 / 0; walk slide 0.002; tris **12,452** (unchanged); stride 0.3091.
  - FBX `C:\\cdimp\\CoralCrusher.fbx` 05:24.

"""

ins(T + r"\MODEL_NOTES.md", "## FINAL 8.5 (2026-10-28", TXT)
ins(T + r"\CLIP_NOTES.md", "## 9+ ROUND", TXT)
print("ok")
