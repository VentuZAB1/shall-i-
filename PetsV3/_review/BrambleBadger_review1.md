# Bramble Badger - model gate review 1 (2026-10-27) - REVISE (model)

**Score: 6/10** for a 40 % starter. Ship target is 8/10.

The concept reads as a badger at 64 and 128 px, and it is distinct from every Grass pet. Three things drifted from the plan
and change what the pet looks like: the head is a black helmet, the palette is about 70 % dark in the side view, and the eyes
face sideways. All fixes are codeable on the current bones. No bone is renamed, so clip authoring can start in parallel, but
round 2 of the model gate must pass before export.

## What I looked at

- Plan: `_review/BrambleBadger_plan.md` (v2), section 2.7, and rulings 3.4 and 4 in `_review/GLACIER_PLAN_REVIEW.md`.
- Style: `Creature Style.md`, `Model Review Checklist.md`, `FIERCE_GUIDE.md`.
- Format and strictness: `_review/VenomBasilisk_review2.md`.
- Badger renders: `BrambleBadger/renders/_model_sheet.png`, `_close_sheet.png`, `close_front.png`,
  `_icons_strip_64.png`, `_icons_strip_128.png`.
- Comparisons: `ForestStag/renders/_model_sheet.png`, `VenomBasilisk/renders/_model_sheet.png`,
  `MossbackTortoise/renders/_model_sheet.png`, `_ALL_FIERCE_progress.png`.
- Source: `pets/BrambleBadger.py` (line numbers below). `blockkit.py`: `add()` takes half extents, `seg()` takes half width
  and half depth.

Units: HEIGHT = 0.61 model units = 6.5 studs (code line 12). 1 % of HEIGHT is about 0.006 units, or 0.065 studs.

Plan note: `BrambleBadger_plan.md` still says HEIGHT 7.0. The code and the brief say 6.5. Use 6.5 and update the plan.

## Value shares (side view, flat palette)

| Colour | Build | Plan | Status | In game (x0.6) |
|---|---|---|---|---|
| GREY (176,172,180) | 18.9 % | 40 % | FAIL | (106,103,108) |
| MANTLE (110,104,116) | 24.2 % | 10 % (min) | FAIL, over | (66,62,70) |
| BELLY_D (72,58,54) | 35.6 % | 17 % | FAIL | (43,35,32), near-black |
| FACE (240,236,226) | 5.0 % | 12 % | FAIL | (144,142,136), grey |
| AMBER (236,150,60) | 4.6 % | 6 % | FAIL, low | (142,90,36), brown-orange |
| THORN_D (120,70,36) | 0.7 % | 3 % | minor | (72,42,22) |
| BLACK (14,14,22) | 10.0 % | 6 % | FAIL, over | (8,8,13) |
| IVORY (238,234,220) | 0.8 % | under 1 % | PASS | |

Light (GREY + FACE + IVORY) is 24.7 %. Dark (MANTLE + BELLY_D + BLACK) is 69.8 %. The plan is about 53 % light. The inverted
colouring (pale back, dark belly) is accepted, but this balance is not the one the plan describes.

Target after the MUST fixes: GREY 35-40 %, MANTLE 11-14 %, BELLY_D 15-22 %, FACE 11-13 %, BLACK 6-8 %, AMBER 6-7 %,
THORN_D 2-3 %, IVORY under 1 %.

---

## MUST (round 2 blocks on these)

**M1. Head: the black stripes are slabs, so the head reads as a helmet.** (`pets/BrambleBadger.py` lines 65-67, 77)
- Built: each stripe is a seg with half width 0.058 to 0.085. The bands are 0.12 to 0.17 wide (20-28 % of HEIGHT each) and
  cover about 0.23 of the 0.30 skull width. The white centre is only 0.084 units (14 % of HEIGHT). The plan asked for thin flush
  inlays (0.012H) on a white face.
- Direction:
  - Line 65: stripe centre x 0.100 -> 0.090. Half width 0.058 -> 0.030 at the back and 0.085 -> 0.040 at the front. The band
    becomes 0.06-0.08 wide, with its outer edge at or inside x 0.13.
  - Line 67 (snout stripe): centre x 0.058 -> 0.050, half width 0.040 -> 0.022.
  - Result: the white centre is at least 0.12 units (20 % of HEIGHT) and still shows at 64 px.
- Face white: line 17 FACE (240,236,226) -> **(255,252,244)**. In game this lands at about (153,151,146). The current value
  lands at (144,142,136), which is grey.
- Cheek ruff, line 77: (0.04, 0.09, 0.05) at x 0.128 -> (0.05, 0.12, 0.06) at x 0.125. This brings the white share up toward 11 %.
- Check: BLACK at 8 % or less in the side view.

**M2. Palette: in-game colours and the accent.**
- Line 16 BELLY_D (72,58,54) -> **(104,88,80)**. In game (62,53,48) instead of near-black (43,35,32). House rule: near-black is
  only for claws, nose and sockets.
- Line 15 MANTLE (110,104,116) -> **(136,130,146)**. In game (82,78,88). This keeps a clear step down from GREY. Its share is
  fixed by M4.
- Line 18 AMBER (236,150,60) -> **(255,176,64)**. In game (153,106,38). AMBER_HOT (255,214,140) stays.
- Line 20 THORN_D (120,70,36) -> **(96,56,28)**. Thorn bases only.
- GREY (176,172,180) stays. Its share rises through M3 and M4.

**M3. Belly: box-shaped, and the grey/dark split sits too low.** (lines 47-54)
- Built: the dark lower blocks run from z 0.22 at the chest to z 0.24-0.25 at the waist and rump, so the belly line is almost
  flat. The grey/dark flank split is at z 0.36. Creature Style says no box bellies: the belly must rise from the chest to the
  hind legs.
- Direction (the z values are absolute, in model units):
  - Grey upper blocks drop their bottoms to z 0.30.
    - Line 47 (MANTLE chest): centre (0, -0.37, 0.42), half (0.245, 0.11, 0.12). M4 sets the y range.
    - Line 48 (GREY spine): z 0.43/0.432 -> 0.415/0.417, half depth 0.098 -> 0.115.
    - Line 49 (GREY rump): centre z 0.425 -> 0.415, half depth 0.098 -> 0.115.
  - Dark lower blocks have their tops at z 0.30 and keep the belly bottom rising.
    - Line 52 (chest): centre z 0.29 -> 0.26, half z 0.07 -> 0.04. Bottom stays at 0.22.
    - Line 53 (waist): centre z 0.30/0.315 -> 0.28/0.295, half depth 0.06 -> 0.02. Bottom becomes 0.26.
    - Line 54 (rump): centre z 0.30 -> 0.28, half z 0.055 -> 0.02. Bottom becomes 0.26.
  - Result: the skirt rises from 0.22 at the chest to 0.26 at the waist, a tuck of 0.04 (6.5 % of HEIGHT). The grey back runs
    down to z 0.30.
- Hip joints (lines 28-29) and the leg blocks stay as they are.

**M4. Mantle: a hard vertical block, not a shoulder cape.** (lines 47-48)
- Built: the MANTLE chest block spans y -0.48 to 0.06 (half y 0.27). The GREY spine seg starts at y -0.02, so the visible
  mantle runs from y -0.48 to -0.02. That is about half the torso and gives the 24 % share. The seam is a straight vertical cut.
- Direction:
  - Line 47: the mantle covers only y -0.48 to -0.26 (centre y -0.37, half y 0.11).
  - Line 48: the GREY spine starts at y -0.26 (was -0.02), so grey takes the shoulder.
  - Taper the mantle's back edge into the grey, with a top shift or a short sloped seg, so there is no step.
- Target: mantle 11-14 % of the side view. It must read as a shoulder cape, not a stuck-on block.

**M5. Eyes face sideways and sit on the outer wall.** (lines 70-74)
- Built: the amber slit sits at x +/-0.1285, on the outer side wall at the head's widest point. Its thin axis points sideways.
  From the front it is an edge sliver. In the game camera the grey brow hides most of it.
- Size is fine. The slit is 0.074 long and 0.023 tall (12 % and 4 % of HEIGHT), larger than the plan. Do not shrink it.
- Direction:
  - Line 70 slit: x +/-0.1285 -> +/-0.100 (the centre of the band after M1), y -0.735 -> -0.740, yaw s*10 -> s*35.
  - Line 72 hot centre: x 0.1315 -> 0.103, yaw s*35.
  - Line 74 brow: x 0.133 -> 0.105, y -0.728 -> -0.733, yaw s*10 -> s*35.
- The black band is the socket, so no extra block is needed. Creature Style wants a black socket with a slit and a hot centre
  under a brow; the band provides the socket once the slit sits on its centre.

**M6. Snout too long: anteater read.** (lines 60-61, 85-88, 144)
- Built: the snout seg runs from y -0.77 to -0.98, which is 0.21 units (34 % of HEIGHT). With the skull, the head is 0.44 units
  (72 % of HEIGHT). The plan gives 0.30H. A long narrow wedge with a black nose block reads as an anteater or aardvark.
- Direction:
  - Line 60: snout end y -0.98 -> -0.92 (snout 0.15 units, 25 % of HEIGHT).
  - Line 61 nose: y -0.995 -> -0.935.
  - Line 85 lower jaw: end y -0.94 -> -0.88.
  - Line 86 mouth: y -0.83 -> -0.80.
  - Line 88 fangs: y -0.925 -> -0.865.
  - Line 144 rig `Mouth` joint: y -0.97 -> -0.91.
- Result: head 0.38 units (62 % of HEIGHT). The plan's 0.30H (about 0.18 units) cannot hold a skull this size. The planner must
  either accept 0.38 or re-plan the number. I recommend accepting it.

**M7. Ear rims float above the head.** (line 82)
- Built: the FACE rim is placed at `ear.world((0, -0.010, 0.024))`, which is on the top of the ear. In `close_front.png` the two
  white tabs stand above the top corners of the stripes. They read as loose parts.
- Direction: set the rim's local z 0.024 -> 0.0 and local y -0.010 -> -0.022, so it sits flush on the ear's front face. Or delete
  the rims. Check in a 3/4 close-up.

---

## NICE (do these too)

**N1. Front claws too long.** Line 116: `0.072 if big` is 12 % of HEIGHT. The plan says 6 %. Change to 0.050 (8 %). At 128 px the
claws read as a rake.

**N2. Thorn crest slightly over the plan.** The five longest thorns (lines 33-34 and the middle entries, lengths 0.064-0.070)
are 10-11.5 % of HEIGHT. The plan says 8-10 %. Cut them to 0.058. The crest itself reads well and stays.

**N3. Whole upper body sits high and the head top is above the back.** The head top is at about z 0.58 and the back arch at
0.55. The plan wants a low, grumpy head. Lower the torso, neck, head, stripes, thorns, hips and tail by 0.03 (lines 28-33, 47-61,
65-88, 116-121). Re-scale to 6.5 studs afterwards. This also lowers the belly, so the visible legs get shorter. Apply it after M3,
and shift the M3 z values by -0.03.
- Ground-to-elbow is 0.20 units (33 % of HEIGHT). The plan says 22 %. The lowering brings it to about 0.17 (29 %).

**N4. Tail stub band.** In the back 3/4 view the black tail band (lines 120-121) looks like a block standing on the rump's top.
Seat the stub inside the rump, on its centre line, and keep the band shorter.

---

## Pass / fail checklist

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Reads as a badger at 64 px | PASS | Grey back, black head, white cheek, amber row. After M1 the white centre must still show at 64 px. |
| 2 | Reads at 128 px | PASS | |
| 3 | Distinct from every Grass pet (Stag, Mossback, Treant, Basilisk, Mantis) | PASS | Mossback also has a spiky back, but colour and silhouette separate them. The amber is the only warm accent in Grass. |
| 4 | Fierce, not cute | PARTIAL | Grey brow and black mask read grumpy. The eyes face sideways, so they fail in the game camera until M5. |
| 5 | Box belly, flat bottom | FAIL | M3 |
| 6 | Colours follow the plan (inversion accepted) | FAIL | The inversion is accepted. The balance is not. M1, M2, M3, M4. |
| 7 | Dark body, pale underside, one accent (value shares) | FAIL | Light 25 %, dark 70 %. |
| 8 | Amber accent strong enough | FAIL | 4.6 % in the side view, brown in game. M2. |
| 9 | Proportions: legs | FAIL | Ground-to-elbow 33 % against 22 %. N3. |
| 10 | Proportions: head | FAIL | 0.44 units (72 %) against 0.30H. M6. |
| 11 | Proportions: length | PASS | 1.58 units. Long and low is badger-plausible. |
| 12 | Floating or poking parts | FAIL (minor) | Ear rims, M7. Tail stub, N4. |
| 13 | Eyes: slit under brow, socket | FAIL | Facing sideways. No change needed to size. M5. |
| 14 | Studs | PASS | Body, legs and skirt studded. Stripes, eyes, thorns, claws and nose smooth, as intended. |
| 15 | Game colours | FAIL | BELLY_D near-black, FACE grey, AMBER brown. M2. |
| 16 | Tris | PASS | 4,912 against the 15k cap. |
| 17 | Collision and ground | NOT CHECKED | Clip stage. |

## Round 2 send list

- Model sheet (front, side, back, three-quarter).
- Close-ups: face close-up, front close-up, and a game-camera frame (about 5 studs, FOV 70, three-quarter from the front and above).
- Icon strips at 64 and 128 px, next to ForestStag, MossbackTortoise, VenomBasilisk, Treant and ThornbladeMantis.
- Value shares, side view and game view.
- Back three-quarter view for the tail and the mantle seam.
