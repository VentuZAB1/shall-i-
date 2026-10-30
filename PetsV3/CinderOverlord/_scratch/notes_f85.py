import io, json
D = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\CinderOverlord"
g = json.load(open(D + r"\_scratch\gate_f85.json"))
sh = g["shares_pct"]


def ins(path, marker, text):
    s = io.open(path, encoding="utf-8").read()
    i = s.index(marker)
    io.open(path, "w", encoding="utf-8").write(s[:i] + text + s[i:])


def rep(path, a, b):
    s = io.open(path, encoding="utf-8").read()
    assert s.count(a) == 1, (path, s.count(a), a[:70])
    io.open(path, "w", encoding="utf-8").write(s.replace(a, b))


def row(v):
    x = sh[v]
    return "| %s | %.1f | %.1f | %.1f | %.1f | %.1f |" % (v, x["PLUM_OBS"], x["OBS_D"], x["PALE_S"], x["CROWN_IN"],
                                                         x["GOLD"] + x["GOLD_D"])


MODEL = """## FINAL 8.5 (2026-10-28, after `_review/CinderOverlord_final85.md`, FIX model 7) - EXPORTED
The single gate file is `_scratch/gate_f85.json`. `gate_r6.json` and `gold_windows_r6.txt` are renamed `STALE_f85_*`.
Backup of the r6 export: `_scratch/CinderOverlord_exported_r6.py`. Colours are unchanged (rulings A/B, body not lifted).
- **M1, mass, not a worm:**
  - `RAD` = 0.297 / 0.308 / 0.280 / 0.252 / 0.200 (+12 %%); `FRAD` +5 %% (0.282 ... 0.189). The chest base sits on the
    thicker body (FRONT[0] z 0.254 -> 0.285).
  - The Body3, Tail1 and Tail3 rings are dropped, so every second ring is gone from Body2 to Tail4. The Spine, Body1
    and neck rings stay.
  - The rest are narrowed: body bands 0.62-0.80 (was 0.55-0.84), tail bands 0.66-0.76 (was 0.62-0.79).
  - The vents, dorsal spikes and scutes follow the radii. The vents move 4 deg up the flank (28 / 152, was 24 / 156),
    so the wider scutes (T1) do not cover their lower ends.
- **M2, head:**
  - The jaw-muscle bulges are cut to 60 %% (0.035 x 0.069 x 0.053) and tucked under a new flat, tapered OBS_D cheek
    plate on each side. The plate is laid on the skull surface via `surf_hit`, from the jaw hinge to under the eye,
    and tapers to 55 %% at the front.
  - **Head studs:** the stud skin is one object-space box projection with one global pitch (`bk.stud_skin`, pitch
    0.0482). The head studs therefore already have the same size as Body1's. The "bubble" look came from the tile
    stretching over the round jaw bulges; those are now covered by the flat plate (`renders/_close_sheet.png`, side).
- **M3, eyes:** socket 0.125 x 0.010 x 0.036, slit 0.110 x 0.010 x 0.020 (+30 %%, deep blue). The pupil grows with the
  slit (0.0065 x 0.020, 0.003 proud). No glint, no round eye; the slits stay angled and set under the brow.
  - In the 64 px portrait icon the near eye reads as a clear blue slit. The far eye is behind the skull in this
    front-left 3/4 camera, so only one slit can show (`_scratch/icons_64x4.png`, 4x nearest-neighbour).
- **M4, clean crown:**
  - The mount ends are 0.22 (was 0.30) and dropped 0.02 behind the blades; the two side blocks are removed.
  - The "dark arms over the brows" in the r6 `close_front` were mostly the BROWS: their outer ends rose to the crown
    line from the front. The brows are now shorter and less rolled (half-length 0.090, was 0.108; roll 16, was 22),
    and kept toward the nose so the forward point is unchanged.
  - From the front no dark arm reaches the crown now (`renders/close_front.png`).
- **M5, gold - ONE method (kit counter, `_tools/game_icon.py`, H 29-58, s > 0.5, v > 0.45):**
  - **portrait %d, game %d** at 64 px (r6: 26 / 20).
  - Added: a rounded gold tip nib on the centre blade (top 29 %% of the blade, above the blue V) and a smaller one on
    blades 2 / 4 (top 22 %%). The centre frames are deeper (half-depth t/2 + 0.022, was + 0.009); blades 2 / 4 are
    t/2 + 0.017. The frame widths are unchanged (wider frames touched in the molt).
  - Finding: in the kit portrait the lit flat gold faces clip to lemon (255,255,99) = H 60, outside the window (59
    such pixels at 64 px). A flat cap therefore added no counted pixels; the counted gold comes from the less-lit side
    faces, hence the deeper frames.
- **T1:** the pale scutes on Body1-4 wrap 8 deg further up each flank (180-360, was 188-352). Pale share: side 12.5 %%,
  tq 12.9 %%. From the top-down game camera it is still only 2.7 %%, because the body lies on its belly.
- **T2:** Tail1-3 radii 0.168 / 0.135 / 0.103 (+25 %%); Tail4 0.072 (was 0.060) to keep the taper smooth; tip 0.042.
- **T4:** blades 1 / 5 keep 0.020 frames, no nib and normal depth. The centre carries the most gold, then 2 / 4.
- **Shares (all figure pixels, flat renders, %%):**

  | view | body | obsidian | pale | blue accent | gold |
  |---|---|---|---|---|---|
%s
%s
%s
%s

  Body >= 40 and obsidian <= 40 in every view.
- **Tris 10,588.** Height 2.254 BU (10.5 studs).
- **Renders (2026-10-28):** `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64/128.png`,
  `_icons2_strip_64/128.png`, `gamelook_game.png` / `gamelook_tq.png`, `flat_*.png`.

""" % (g["gold_px_64"]["portrait"], g["gold_px_64"]["game"], row("game"), row("side"), row("tq"), row("back"))

fan = g["molt_front_fan"]["spread_1_5_deg"]
CLIP = """## FINAL 8.5 (2026-10-28, after `_review/CinderOverlord_final85.md`, FIX clips 7.5) - EXPORTED
- **C1, the molt reads from the front:**
  - The four outer blades lift **45 deg** (was 35). The centre lifts 35, then 40, as before.
  - The lifts start at **f12** (was f18), with a 3-frame lag and the same 10-frame rise. Blade 1 is fully up at
    `lift1` f22.
  - The middle blades' fan goes from 10 to 14 deg (outer 18), scaled by the lift.
  - Front-view fan spread, Crown_1 to Crown_5 (`_scratch/fan_probe.py`): **f0 %.1f, f22 %.1f, f34 %.1f, f40 %.1f
    deg**. That is +18.9 / +37.0 / +37.0 vs f0. Each fanned blade moves 16-18.5 deg in the front view at f34-40.
  - Evidence: `renders/_molt_r4_front.png` (f0 ... f110), `_scratch/molt_fan_zoom.png` (crown crop f0 / 22 / 34 / 40)
    and `renders/_cv_molt_front.png`.
  - Reseats are stretched: the centre goes 40 -> 6 over **f84-100** (was f84-95) and to 0 at f106; the outer blades
    reach 2 at f100 / 98 / 94 / 92 and 0 at f108.
  - Speeds (`_scratch/ang_probe.py`, deg/f) - every fall stays under its rise:

    | blade | rise | fall |
    |---|---|---|
    | outer (1 / 5) | 7.47 | 5.80 |
    | middle (2 / 4) | 7.10 | 5.56 |
    | centre | 5.18 | 3.17 |
  - The blades are collision-free at 45 deg.
- **T3, idle:** the neck breath is 3 deg per bone (was 2; total 9) and the head counter-pitch is 6. The head stays
  near level.
- **C2, renders re-made from the current model and palette** (stale ones moved to `_scratch/stale_r6_renders/`):
  - `_pose_tq_sheet.png`: 26 beats - idle 0/30/60/90, walk 0/12/24/36, roar 0/14/22/30/44/66, and molt 0 ... 110.
  - `_cv_walk_side.png`, `_cv_walk_game.png` (walk f0-40 from the fixed side and game cameras).
  - `_cv_roar_front.png`, `_cv_roar_side.png`.
  - `_molt_r4_front.png` / `_side.png` / `_tq.png` (14 frames each), `_cv_molt_front.png` (f0 / 22 / 34 / 40).
- **C3 (walk speed in Studio) and C4 (owner disclosure): skipped per the coordinator.** The walk stride stays 5.19 BU
  per 48 f.
- **Step 1** (`_scratch/clipgate_f85.txt`, export run `_scratch/export_f85.txt`):
  - collision_free **true**; ground_min_z -0.006 in every clip; linear 0; idle and walk loops 0 / 0.
  - Tris 10,588. Events are unchanged (molt `lift1` 22, `lift2` 48, `shed` 56).
- **Export:** `C:\\cdimp\\CinderOverlord.fbx` (2026-10-28 01:31, 1,287,228 B). The portrait raw is re-made.

""" % (fan["0"], fan["22"], fan["34"], fan["40"])

ins(D + r"\MODEL_NOTES.md", "## ROUND 6 (2026-10-27, lead rulings", MODEL)
ins(D + r"\CLIP_NOTES.md", "## ROUND 6 (2026-10-27): FINAL, EXPORTED", CLIP)
rep(D + r"\CLIP_NOTES.md", "| EMBER BREATHING: two slow breaths - the neck rises 6 deg and sinks back",
    "| EMBER BREATHING: two slow breaths - the neck rises 9 deg (3 per bone, final 8.5) and sinks back")
rep(D + r"\CLIP_NOTES.md", "f18-42 the blades lift one by one (3-frame lag, round 4) 35 deg and fan open like a crest (front read)",
    "f12-34 the blades lift one by one (3-frame lag) - the four outer blades 45 deg, the centre 35 (final 8.5) - and fan open like a crest (front read)")
rep(D + r"\CLIP_NOTES.md", "f84-104 the blades reseat in reverse order, slower than they rose (the centre blade over f84-95)",
    "f84-108 the blades reseat in reverse order, slower than they rose (the centre blade over f84-100)")
rep(D + r"\ANIM_REFS.md", "Slow breathing: the neck rises 6 deg and sinks back (each neck bone\n  <= 2 deg)",
    "Slow breathing: the neck rises 9 deg and sinks back (each neck bone\n  3 deg, final 8.5)")
rep(D + r"\ANIM_REFS.md", "f18-42 the blades lift one by one 35 deg (3-frame lag, round 4), `lift1` f22.",
    "f12-34 the blades lift one by one (3-frame lag): the four outer blades 45 deg, the centre 35 (final 8.5); blade 1 is\n  fully up at `lift1` f22.")
rep(D + r"\ANIM_REFS.md", "the centre blade takes 11 f (f84-95). Exact rest.",
    "the centre blade takes 16 f (f84-100), the outer blades end at f108 (final 8.5). Exact rest.")
print("notes ok")
