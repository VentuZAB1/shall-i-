import io, re
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
T = D + r"\PermafrostTitan"


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


def rep(path, a, b, cnt=1):
    s = io.open(path, encoding="utf-8").read()
    assert s.count(a) == cnt, (path, s.count(a), a[:70])
    io.open(path, "w", encoding="utf-8").write(s.replace(a, b))


MODEL = """## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/PermafrostTitan_final85_r2.md`, FIX model 7.5) - re-exported
Backup of the round-1 export: `_scratch/PermafrostTitan_exported_f85.py`.
- **MUST 1, one tapered tube per leg:**
  - Thigh 0.182 x 0.194, tapering to **0.66** at the knee.
  - The shin starts at the thigh's knee width (+0.006, a slight calf) and tapers to 0.84 at the ankle, so there is no
    step at the knee.
  - The plum thigh plate is now **0.020** thick (was 0.046). It rides 0.012 inside the thigh surface (0.008 proud) and
    stays on the flat part of the side.
  - The knee cap is 0.020 deep and sits on the shin front, so it is a bulge, not a block.
  - The knee joint is inside the tube.
  - The shin guard is 0.018 thick and rides the tapering shin front (0.008 proud).
  - **One** thin ankle band (+0.008 over the shin end); the foot's ankle joint sits inside it.
- **MUST 2, hips:**
  - The hip block is 0.27 wide (was 0.30), with a 0.78 base taper.
  - The thigh tops sit 0.02 further out.
  - The plum hip plates are thinner (0.034, was 0.058) and sit on the hip (x 0.238), not over the thigh tops.
  - `_model_sheet.png` front: the thighs now start as wide tops right under the hip block and taper down.
- **MUST 3, chest to pelvis:** the belt joint rnd 0.5 (was 0.4, width 0.262); the chest bottom taper 0.62 (was 0.66);
  the chest/waist gap rnd 0.5, width 0.26.
- **NICE 1:** the belly band is 0.16 x 0.012 x 0.030 (was 0.20 x 0.016 x 0.036).
- **Numbers:**
  - Tris **7,664**.
  - Gold at 64 px (kit counter): **portrait 52, game 27**.
  - Shares, all figure pixels:

    | view | MAUVE | PLUM | ICE_W |
    |---|---|---|---|
    | side | 60.6 | 12.0 | 14.6 |
    | tq | 58.3 | 13.9 | 12.1 |
    | game | 56.7 | 16.6 | 15.2 |
    | back | 60.3 | 16.9 | 11.4 |
- **Renders (all re-made):** `_model_sheet.png`, `_close_sheet.png`, `_under_sheet.png`, the icon strips,
  `gamelook_*.png`, `flat_*.png`.

"""

CLIP = """## FINAL 8.5 ROUND 2 (2026-10-28, after `_review/PermafrostTitan_final85_r2.md`, FIX clips 7) - re-exported
- **MUST 4, the kneel is MIRRORED - it now kneels on the LEFT knee (the camera side):**
  - Same timing. The RIGHT foot steps forward 0.30 and 0.04 out.
  - The LEFT foot tucks and turns 10 deg out in the hold.
  - The Spine rolls +7 toward the left; the Chest and Head counter-roll -3.5. The f6 weight shift goes onto the left foot.
  - **The VFX anchor is renamed `Knee_L`** (`icecrack` f18), on `Shin_L` at the knee front. `Knee_R` no longer exists.
  - The slimmer knee cap and shin lifted the knee 0.03-0.04 off the snow, so the pelvis drop is **0.312** (was 0.272).
    Ground probe (`_scratch/ground_probe.py`): the LEFT knee (Shin_L) is the lowest part from f18 to f52, at -0.003 to
    -0.009 in the hold and **-0.018** at the f20 settle (limit -0.02).
  - **Asymmetric hold:** with the 0.31 drop the hanging fists reached the snow and the left fist covered the kneeling
    knee from the front and the 3/4. The RIGHT fist now rests forward on the raised right knee (fwd 20, bend 32). The
    LEFT elbow bends 48 so its fist sits on the thigh above the knee (out 12, fwd 8).
  - Evidence:
    - `renders/_kneel_close_f40.png`: the tq and game cameras at f40, plus close-ups aimed at `Knee_L` - the left knee
      cap is flat on the snow (3/4) and the left shin lies on the snow with the sole up (game).
    - `_kneel_views.png`: front / tq / back / game at f18 / 40 / 58.
    - `_beats2x_kneel.png`.
- **MUST 5, idle:** hip yaw **+/-6 deg** (was 4).
  - The Chest counter-yaws **-0.75 x yaw** (4.5 deg) and the Head -0.25 x yaw, so the head stays facing forward.
  - The review's -0.8 would make chest vs spine 5.2 deg at f30, where the 2 deg breath pitch stacks on it; -0.75 keeps
    it at **4.92**.
  - The fist flex stays at 8 deg. `renders/_beats2x_idle.png`.
- **Chest vs spine (measured, `CinderOverlord/_scratch/ang_probe.py` on the Chest bone):** idle 4.92, roar 3.0,
  act 4.68 (limit 5). Head max: roar 15, act 13.5.
- **Step 1** (`_scratch/export_r2.txt`):
  - collision_free **true**. ground_min_z 0.000 for idle / walk / roar; -0.018 for the act at f20 (the knee settle).
  - Linear 0. Idle and walk loops 0 / 0. Walk slide 0.0. Idle foot drift 0.
  - Tris 7,664. Events are unchanged.
- **Renders:** `_pose_tq_sheet.png` (24 beats), `_beats2x_idle/roar/kneel.png`, `_kneel_views.png` and
  `_kneel_close_f40.png`.
- **Export:** `C:\\cdimp\\PermafrostTitan.fbx` (2026-10-28 03:29).

"""

ins(T + r"\MODEL_NOTES.md", "## FINAL 8.5 (2026-10-28", MODEL)
ins(T + r"\CLIP_NOTES.md", "## FINAL 8.5 (2026-10-28", CLIP)
# current descriptions: the kneel is on the LEFT knee now
c = io.open(T + r"\CLIP_NOTES.md", encoding="utf-8").read()
c = c.replace("`Knee_R` (FX_IceCrack on `icecrack`)", "`Knee_L` (FX_IceCrack on `icecrack`; was `Knee_R` before final 8.5 round 2)")
c = c.replace("The giant drops to one knee on the snow, bows with its ice core pulsing, then leans forward and rises.",
              "The giant drops to its left knee on the snow, bows with its ice core pulsing, then leans forward and rises.")
io.open(T + r"\CLIP_NOTES.md", "w", encoding="utf-8").write(c)
a = io.open(T + r"\ANIM_REFS.md", encoding="utf-8").read()
a = a.replace("- **act_kneelrise (100 f): K1-K4 + K8a + #9.**",
              "- **act_kneelrise (100 f): K1-K4 + K8a + #9.** (Final 8.5 round 2: MIRRORED - the left knee goes down and the\n"
              "  right foot steps forward; read left / right swapped below.)")
io.open(T + r"\ANIM_REFS.md", "w", encoding="utf-8").write(a)
# the act docstring in the pet file
p = D + r"\pets\PermafrostTitan.py"
rep(p, '''    """KNEEL AND RISE (plan; Plate 356 K1-K4 + #9): the left foot steps forward, the body drops straight down and the
    right knee lands (ice crack), the right toes tuck, the head bows 12 deg, the fists come to rest over the thighs;''',
    '''    """KNEEL AND RISE (plan; Plate 356 K1-K4 + #9; final 8.5 r2 MIRRORED): the right foot steps forward, the body drops
    straight down and the LEFT knee lands (ice crack, `Knee_L`), the left toes tuck and turn out, the head bows 12 deg,
    the right fist rests on the raised right knee and the left fist on the left thigh;''')
print("titan notes ok")
