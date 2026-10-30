# inserts the ROUND 3 sections into my three MODEL_NOTES.md files + two CLIP_NOTES corrections (my own pets only)
import io
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"

R3 = {
"PermafrostTitan": """## ROUND 3 (2026-10-27, after `_review/PermafrostTitan_review2.md`, APPROVED WITH FIXES 7/10) - shipped with the clips
- **MUST 1** back echo ring: outer 0.27 BU diameter (BR_OUT 0.135, BR_IN 0.088, band 0.047, depth 0.06, proud 0.030), ice
  disc r 0.066; a ring only (no settings, spikes or crown). Game-camera gold at 64: **24 px** (kit counter; target >= 20).
- **MUST 2** upper shoulder caps 0.130 x 0.150 x 0.033 (rnd 0.30, three chunks), lower caps 0.076 x 0.145 x 0.034, pauldron
  bottom 0.80: game (back) **ICE_W 11.5 %** (target >= 11). No spikes on the hump.
- NICE 1 shin guard depth 0.028; NICE 2 chest bottom taper 0.66; NICE 4 brows 30 deg. NICE 3 (Studio colour) and NICE 5
  (pet facing) need Studio - not possible from here.
- Evidence: `renders/model_back.png`, `renders/under_lowback.png`, `renders/gamelook_game.png`, `renders/_icons2_strip_64.png` / `_128.png`,
  `_scratch/game_icon.json`, `_scratch/shares_strict.json`. Clips: see `CLIP_NOTES.md`.

""",
"CoralCrusher": """## ROUND 3 (2026-10-27, after `_review/CoralCrusher_review2.md`, APPROVED WITH FIXES 7/10) - shipped with the clips
- **M1** the cream claw undersides are dropped; palm, fingers and knuckles nostud. Pale share: **side 0.9 % / tq 0.4 % /
  game 0.8 %** - the >= 5 % side target is NOT met (the legs and margin spines cover the flank under the rim from the side
  camera; `_scratch/lipchk.png`). A flush ventral claw edge test gave 4.6 % side, ~83 % of it on the claws
  (`_scratch/shares_r3_with.json`) - against the <= 1/3 rule, so not shipped. Needs a ruling (see `CLIP_NOTES.md`).
- **M2** base pose at the walk's 45 deg spine yaw in every clip: crossfade ankle travel **0.077 BU** (was 0.79).
- **M3** `CoralCrusher_portrait_alt.png` = the game-camera icon of idle f0 (512 px, transparent).
- NICE N1 second plate row on the rear dome, N3 rear ledge 0.01 lower, N4 alternating margin spines, N5 walk claws 10 deg
  lower. Evidence: `renders/_close_sheet.png` (front, high, clawtq, clawside), `renders/_under_sheet.png`,
  `renders/_crossfade_sheet.png`, `_scratch/shares_strict.json`, `_scratch/xfade_r3.txt`.

""",
"CinderOverlord": """## ROUND 3 (2026-10-27, after `_review/CinderOverlord_review2.md`, REVISE 6/10) - every MUST + NICE 1/3 applied
- **MUST 1** obsidian cap arc 65-115 deg (was 55), rose slits 0.018 proud + pupils 0.023: the eyes read from the front.
- **MUST 2** V muzzle: the last skull stations (0.96: 0.070 x 0.048) and (1.0: 0.055 x 0.040).
- **MUST 3** dorsal saddle 9 deg (body) / 8 deg (tail), neck saddle dropped: **game PLUM_OBS 43.2 % / OBS_D 37.8 %**.
- **MUST 4** RAD[1..3] 0.275 / 0.250 / 0.225 (round 2: 0.250 / 0.230 / 0.205).
- **MUST 5** vent hot cores w x 0.50 in LAVA (255,128,24); the crown centre gem is LAVA; ROSE_H retired.
- NICE 1 outer-blade gold 0.020; NICE 3 the centre blade gold on its sides too (0.034) and 0.30 tall. Gold at 64:
  portrait 27 px, game 20. NICE 2 (Ivonrath hue) unchanged - S 0.44 kept; the 128 px strip is in the evidence.
- Evidence: `renders/model_front.png`, `renders/_icons_strip_64.png` / `_128.png`, `renders/gamelook_*.png`,
  `_scratch/shares_strict.json`, `_scratch/game_icon.json`. Clips: see `CLIP_NOTES.md`.

""",
}

for name, sec in R3.items():
    p = ROOT + "\\" + name + "\\MODEL_NOTES.md"
    t = io.open(p, encoding="utf-8").read()
    if "## ROUND 3" not in t:
        i = t.index("## ROUND 2")
        t = t[:i] + sec + t[i:]
        io.open(p, "w", encoding="utf-8", newline="\n").write(t)
        print("R3 ->", name)

# CLIP_NOTES corrections
p = ROOT + r"\CoralCrusher\CLIP_NOTES.md"
t = io.open(p, encoding="utf-8").read()
old = "allow a thin flush ventral claw edge back (it gave 3.5 % side, 74 %\n  of it on the claws)."
new = "allow a thin flush ventral claw edge back (the test gave 4.6 % side,\n  ~83 % of it on the claws: `_scratch/shares_r3_with.json`)."
assert old in t
t = t.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)

p = ROOT + r"\PermafrostTitan\CLIP_NOTES.md"
t = io.open(p, encoding="utf-8").read()
old = ("- Pose limits: chest vs spine <= 4 deg (kneel 4, roar 3.5); head + chest pitch-up max 15 deg (roar); no head shake;\n"
       "  no limb swing > 15 deg between frames.")
new = ("- Pose limits (from the key tables): chest vs spine <= 4 deg (kneel lean 4, roar 3.5); spine + chest + head pitch-up\n"
       "  max 15 deg (roar); no head shake; the fastest limb move is the right thigh into the kneel over 12 frames (f6-18).")
assert old in t
t = t.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
