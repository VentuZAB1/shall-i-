# Eclipse Seraph - model gate review 2 (2026-10-27) - REVISE (one short round)

**Score: 7/10 for a 0.1 % MYTHIC** (up from 5/10; ship at 8+).

Round 2 fixed most of review 1. The halo now reads as an eclipse from the front, the gold is about twice as big, red appears on the face, the body is a rich lilac instead of white or grey, and the mane reads as a mane. Four things stop it shipping: the pale is still above target, the chroma is still below the 1 % Leviathan, the dark mane mass is still under 22 %, and the game-camera view has no red at all. All four are small code changes. No concept change, no rebuild.

Keep: six wings (11,228 tris, builder's count), HEIGHT 11.5 (halo rim top), halo tilt 40, the 0.045 gold lip, the raised lower-pair root with display "up" 10, the red slit eyes, the lilac face and underside.

---

## What I looked at
- The brief and the round 1 review (`EclipseSeraph_review1.md`).
- `EclipseSeraph/MODEL_NOTES.md` ROUND 2 section (builder's numbers and deviations).
- `pets/EclipseSeraph.py` (round 2 constants and line references below).
- Renders: `_icons_strip_64.png` (7 cells, same pets as round 1), `_icons2_strip_64.png` and `_128.png` (4 cells: portrait, game-camera icon, Cosmic Leviathan, Frostcrown Dragon), `_model_sheet`, `_close_sheet` (face, halo, rim, corona), `_idle_sheet` (display pose), `halo_game.png`, `_scratch/var_apri_icon.png` (the upper-primaries variant the builder tested).
- Geometry: the halo edge-on ratio for each tilt against the game camera (about 38 deg above and behind), computed from the disc normal.

Method: object-pixel counts on the renders, same classifier for round 1 and round 2 (about +/-3 points). I did not run Blender, so clearances and tris are the builder's numbers. The builder's own counts (raw render, no outline) differ from mine, and I give both where they matter.

## Measured: round 1 against round 2 (portrait icon, same method)

| 64 px item | round 1 | round 2 | target | status |
|---|---|---|---|---|
| near-white (lum > 200) | 42 % | **32 %** | <= 25 | FAIL (builder: 36.1 % raw, 26.6 % strip) |
| mean saturation | 0.18 | **0.27** | >= 0.33 | FAIL (Leviathan 0.35, Frostcrown 0.44, Solar Lion 0.42) |
| dark (lum < 90) | 15 % | **20 %** | >= 22 | FAIL, near (Solar Lion 22 %) |
| gold px, portrait | 42 | **82** | >= 20 | PASS (Leviathan 20, Frostcrown 92) |
| red px, portrait | 0 | **12** | >= 10 | PASS |
| gold px, game-camera icon | 8 | **13** | >= 20 | BORDERLINE (builder counts 22; my crop is stricter) |
| red px, game-camera icon | 0 | **0** | >= 10 | FAIL |

Gold is now larger than the Leviathan's and close to the Frostcrown's. Chroma is still the plainest of the mythic-class set. The Seraph is still paler than the Solar Lion (32 % against 9 %), and its saturation is still below the Solar Lion's (0.27 against 0.42).

Flat IDs (builder's table, display pose, game camera): BODY_MID 29.0 %, WING_LILAC 25.5 %, OBSID 22.1 %, WING_IN 7.9 %, MOON_IVORY 5.4 %, GOLD 3.7 %. The true colours are now mostly lilac, not white. The icon's key light lifts lilac over luminance 200 more than the flat render does, which is why the icon pale share is high while the flat share is low. The Index and portrait are what the owner sees, so the pale target belongs on the icon measure.

## Rulings

**(a) Red from the game camera: YES, the back needs a small red element. Not on the halo.**
- The halo cannot carry it. The disc is edge-on to a camera 38 deg above and behind at tilt 38 to 40 (edge-on ratio 0.035 at tilt 40, 0.31 at tilt 20, 0.21 at tilt 50). Tilt 60 shows the face (0.37) but its lower front rim drops onto the forehead (about HC.z + 0.14 against the crown at HC.z + 0.136) and the top rises about 0.08 BU, so it cannot be done without a head clash and a height change. Keep tilt 40.
- The portrait red (12 px, the ring on the disc face and the eyes) stays for the portrait, the Index and the hatch view. That part is enough.
- The game camera looks at the back. The back needs a BLOOD element in the tail brush: `B.add(tip + ..., (0.10, 0.11, 0.095), OBSID, "Tail4", ...)` (line 329), and the brush spikes (tuft loop, line 332), both to BLOOD. The tail is the rear-most silhouette point and does not touch the mane's dark read.
- Fallback if the tail fails the test: BLOOD tips on the six crest tufts (`# crest`, line 294), not gold.

**(b) Upper primaries lilac: YES, do it.**
- The white upper V is the strongest pegasus cue in the portrait and the idle sheet. Making it lilac takes the icon near-white from about 36 % to about 31 % raw, and the builder's strip measure to about 22 %, which is under the 25 % target. The variant also reads as one lilac hero wing, not a white flag.
- Keep one pale highlight on the three hand coverts (line 171, now WING_LILAC, change to WING_IN). That is the single light note the wing needs.
- Risk: the lilac body and lilac wing merge in silhouette. The OBSID tips (0.12 / 0.15) separate them, and the builder should check the wing-body edge at 128 px.

**R1 deviation (body, wing and mane colours): ACCEPT, with two conditions.**
- BODY_MID (184,128,214), WING_LILAC (190,150,226) and OBSID (46,46,70) are better than round 1. The body is a rich lilac now, not grey, and the mane counts as dark mass. They follow the FIERCE "dark rich body" rule better than the concept's near-white.
- Condition 1 (planner): the concept lists one body colour (#E8D0F0). The planner must approve the split: rich lilac on the body, ivory kept on the face and underside.
- Condition 2 (distinctness): BODY_MID hue 279 is 8 deg from Shade Panther's VIOLET accent (hue 271, the one accent of the Void egg). The body is fine, but no violet may appear on the Seraph anywhere. Its accents stay BLOOD and GOLD.

**Accepted with no change:** halo tilt 40, the 0.045 gold lip (game-camera gold up), the lower-pair root raised to 1.05 with display "up" 10 (18 cut the middle pair), display span 1.41 H (NICE 2), the halo clearances (0.056 to the head, 0.105 to the mane; the close sheet is consistent with them, Blender check stands with the builder).

## MUST (round 3; model only)

**MUST 1 - Upper primaries lilac (ruling b).** Line 163: `WING_IN if rows3 else WING_LILAC` becomes `WING_LILAC` for all pairs. Keep WING_IN on the hand coverts (line 171 for the upper pair only). Target: near-white on the 64 px portrait icon at most 25 % (mine now 32 %, builder's strip 26.6 %).

**MUST 2 - Back red (ruling a).** Tail brush to BLOOD: line 329 (`OBSID, "Tail4"` becomes `BLOOD`), and the brush spikes on line 332 (`tuft(... OBSID, "Tail4")` becomes `BLOOD`). Target: at least 10 red px in the game-camera icon (now 0). Keep the front corona and eyes as they are. Fallback: BLOOD tips on the crest tufts (line 294).

**MUST 3 - Dark mane mass to 22 %.** The outer mane ring tuple (line 283, the third entry: `(0.29, 0.34, 0.10, 24, 0.19, "Mane", 1.1)`) goes to about `(0.31, 0.36, 0.10, 26, 0.19, "Mane", 1.1)`: +7 % radius, +6 % length, two more tufts. Target: dark (lum < 90) at least 22 % on the 64 px portrait (now 20 %). Clearance from the halo must stay at least 0.05 BU (now 0.105, so there is room).

**MUST 4 - Chroma, same value.** Line 21: `BODY_MID = (184, 128, 214)` becomes `(190, 120, 226)`. Same luminance (about 153 against 154), saturation 0.40 to 0.47, hue 280. Target: mean saturation at least 0.33 on the 64 px portrait (now 0.27; Leviathan 0.35). This is the only lever that gets the Seraph past the 1 % Leviathan on colour richness.

Re-run the same 7-cell 64 px strip and the 4-cell icons2 strip after MUSTs 1 to 4, on the same classifier as round 1 and 2, and report both the raw and the strip counts.

## NICE
1. If MUST 1 pulls the silhouette lighter than the mane, add a thin OBSID trailing hem to the lilac upper primaries (`tipf=0.15` to 0.18 on line 164). Only if the wing edge is lost at 128 px.
2. The game-camera gold is about 13 px by my crop and 22 by the builder's counter. Confirm the counter used in the next notes. If MUST 1 to 4 shrink the halo's share, move the rim lip from 0.045 to 0.05 before adding any gold elsewhere. No gold elsewhere.
3. The lower-pair display: at "up" 10 the tips are visible past the flank in the front 3/4 (idle sheet). Good. No change.

## Outclass check (the mythic must beat the 1 % and match the other 0.1 %)
- Against Cosmic Leviathan (1 %): gold PASS (82 against 20 px); chroma FAIL (0.27 against 0.35, and the Leviathan's purple and blue give it more colour variety); dark mass FAIL (20 % against 35 %, but the Leviathan's dark is body, not hero).
- Against Frostcrown Dragon (0.1 %): gold roughly level (82 px at 7.9 % against 92 px at 5.7 %, so the Seraph's share is larger, the Frostcrown's count is larger); chroma FAIL (0.27 against 0.44). The two mythics read as different families (lilac-violet and steel blue), which is good.
- Against Solar Lion (common, 54.9 %): still paler (32 % against 9 % near-white) and less saturated (0.27 against 0.42). The lead's "plainer than the common Solar Lion" is still true on chroma. MUST 4 is the answer.

## Pass / fail checklist (round 2)

| item | result |
|---|---|
| 64 px species reads as a lion-angel (not a pegasus) | PARTIAL (lion read now carried by the dark mane and red face; white upper V still the pegasus cue until MUST 1) |
| 128 px: halo, mane, face | PASS |
| Fierce, not cute | PASS |
| Face red eyes at 64 px | PASS (portrait red 12 px) |
| No box belly, rising belly line | PASS |
| Studs on hide; smooth gold, red, feather tips; no Neon, no glow | PASS |
| Palette follows the plan | PARTIAL (body split is a planner-approved deviation; ivory down from the plan's 40 %) |
| Dark body + pale underside + one bright accent | PARTIAL (body now a dark rich lilac; the accent is only visible from the front) |
| 3-band colour blocking | PARTIAL (dark / lilac / gold clear; pale only on the upper primaries until MUST 1) |
| Accent strong in game colours | FAIL until MUST 2 (no red from the game camera) |
| Gold hero at 64 px (portrait, game) | PASS portrait (82); BORDERLINE game (13 by my crop, 22 by the builder) |
| Six wings: tris <= 15k, countable, not a blob | PASS |
| Floating, poking or intersecting parts | PASS (builder's cut-through 0; halo clearances consistent with the close sheet; Blender check stands) |
| Distinct from Shade Panther (violet) | PASS with condition (no violet on the Seraph) |
| Distinct from Solar Lion (radial mane, sun colours) | PASS (mane is dark and swept; no gold on the mane) |
| Beats Cosmic Leviathan (1 %) | FAIL on chroma (gold passes) |
| Equals Frostcrown Dragon (0.1 %) | PARTIAL (gold level; chroma below) |
| Name is two words | PASS |

## Next round: send with
- `_icons_strip_64.png` (7 cells) and `_icons2_strip_64.png` / `_128.png` (4 cells), with the raw and strip counts.
- `_close_sheet.png` (face, halo, rim) and `_idle_sheet.png`.
- A game-camera render from behind and above (the view that must show the red tail brush).
- `flat_game.png` with the value shares.
- The builder's tri count and clearance numbers.

**Bottom line:** REVISE at 7/10. Rulings: (a) yes, a small red element on the back in the tail brush, not on the halo; (b) yes, upper primaries lilac with a three-feather white highlight. The colour and mane fixes (MUST 3 and 4) are what decide whether it beats the Leviathan on colour. Ship at 8 or above only after a clean round 3.
