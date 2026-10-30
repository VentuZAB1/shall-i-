import io
T = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CoralCrusher"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


TXT = """## WALK ROUND (2026-10-28, after `_review/PERCLIP_AUDIT_crusher_mammoth.md`: walk 8.4 under the per-clip floor) - EXPORTED 06:20
Backups:
- the 05:24 export: `_scratch/CoralCrusher_exported_eyes_r4.py`
- this export: `_scratch/CoralCrusher_exported_walk_r6.py`

Walk block only.
- **Changes:**
  - Leg lift **0.07 -> 0.10 BU**.
  - Carapace bob **0.010 -> 0.016 BU** (as asked).
  - Spine walk roll **1.2 -> 2.4 deg**, same phase and 2 cycles, so the timing is unchanged.
  - Why the roll: with the asked bob alone the carapace moved only 2.4 px on screen (see below). The game camera
    foreshortens vertical motion: bob 0.020 added only +0.3 px, so I kept 0.016 and let the roll rock the shell.
  - Unchanged: claw sway 6 deg, duty 0.55, n 30, stride 0.309, the crab-footage timing (the sand1 / sand2 events).
- **Phone-size motion** (`_scratch/walk_px.py`, game camera 390 px, fixed camera, f0-15 = contact to contact):

  | point | before (05:24) | lift + bob only | **final (+ roll 2.4)** |
  |---|---|---|---|
  | carapace top centre | 1.9 | 2.4 | **3.5** |
  | carapace rim +x | - | 4.6 | **8.1** |
  | carapace rim -x | - | 2.4 | **5.2** |
  | leg tips | 12.1-20.0 | 12.1-21.8 | **12.1-21.7** |
  - Over the full cycle (f0-30) the leg tips move 16.4-22.4 px.
  - Pass >= 4 px: the leg tips and both carapace rims (the body silhouette) pass. The top-centre point of the shell
    reads 3.5 px. It sits on the roll axis, so only the bob moves it.
  - Data: `_scratch/walkpx_before.txt`, `walkpx_after.txt` (lift + bob), `walkpx_roll24.txt`, `walkpx_final.txt`,
    `walkpx_final_fullcycle.txt`.
- **Renders** (title bar 06:22): `renders/_walk_strip_game.png` and `renders/_walk_strip_tq.png`, f0-27 every 3 f at 390 px.
- **Portrait:** idle f0 is pixel-identical to 05:24. I compared the kit portrait before and after (diff bbox None), so
  `CoralCrusher_portrait_alt.png` (05:44) stays.
- **Step 1** (`_scratch/export_walk_r6.txt`):
  - collision_free **true**; ground -0.013; linear 0; loops 0 / 0.
  - Walk slide **0.0016** (<= 0.002); foot z var 0.0008; idle foot drift 0; stride 0.3091.
  - Tris 12,452. FBX `C:\\cdimp\\CoralCrusher.fbx` 06:20.

"""
ins(T + r"\CLIP_NOTES.md", "## EYE ROUND", TXT)
print("ok")
