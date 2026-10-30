# Wraith Hound - model gate review 2 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 7.5/10 for a 10 % medium-high** (review 1 was 6/10). Ship bar is 8/10.

The ghost works now. The torso is lavender with a dark top band, the tail is pale with a dark tip, the palette passes both share gates, and the indigo has moved off the Raiju body blue. Two MUSTs remain. Both are small and both are in code. Neither changes a bone name or a joint, so clips can start once they are in:
- **MUST 1:** the mane still reads as three rows of separate fins, not one streaming plume (the signature).
- **MUST 2:** the height is 8.5, still below NightmareStallion's 9.0. The plan's rarity ladder needs the Wraith at least level with it, and the code comment says the opposite.

Send one re-render of `model_side` and the 128 px strip after the fixes. No full round is needed.

## What I looked at
- Round-2 notes: `WraithHound/MODEL_NOTES.md` (round 2 section) and `renders/_shares.json`.
- Code: `pets/WraithHound.py`, checked line by line against the round-2 claims (HEIGHT L14, INDIGO L19-20, torso `upper()` L127-129, chest plate L133, muzzle and fangs L140-148, eyes L157-161, front sock L194, tail L209).
- Renders: `_model_sheet.png`, `_close_sheet.png`, `low_below.png`, `model_side.png`, `model_tq.png`, `game_view.png`, `flat_side.png`, `_icons_strip_64.png`, `_icons_strip_128.png`.
- My own read-only checks (no Blender, no Studio):
  - a palette-ID pixel count on `flat_side.png` (flat render, no lighting);
  - a crop-and-enlarge of the two white slabs in `low_below.png`;
  - hue angles from the RGB values in each pet file.
- Comparisons: the 128 px strip (Raiju, ShadePanther, BlackDragon, NightmareStallion, Pharaoh, AbyssWeaver). The model sheets of Raiju and Cerberus from round 1 still stand.

## Measured (my count, against the builder's `_shares.json`)

| region / share | my count (flat side) | builder (side) | gate |
|---|---|---|---|
| SOOT, whole silhouette | 37.1 % | 35.5 % | <= 38 % - PASS |
| ASH_LAV + MIST, whole silhouette | 58.6 % | 54.9 % | >= 48 % - PASS |
| torso band (x150-240, y172-208) | ASH 77 % / SOOT 23 % | - | (round 1: SOOT 84 %) |
| lower torso (y196-215) | ASH 99.5 % | - | pale flank |
| legs | ASH 78 % / MIST 20 % | - | (round 1: ASH 75 %) |
| tail (x290-400) | ASH 44 % / SOOT 56 % | - | (round 1: SOOT 85 %) |

My count reproduces the builder's shares within about 3 points, so I accept the builder's numbers.

**Hue (H, degrees), round 2:**

| colour | H | distance from new INDIGO (H 236) |
|---|---|---|
| WH INDIGO (112,120,240) | 236 | - |
| Raiju FUR (80,102,182) | 227 | 9 (lighter accent: V 240 vs Raiju V 182) |
| BlackDragon INK (78,68,158) | 247 | 10 |
| BlackDragon MANE (146,84,236) | 265 | 28 |
| ShadePanther VIOLET (170,80,255) | 271 | 35 |

**Heights (studs):** Wraith 8.5. For comparison: ShadePanther 7.0, Raiju 8.0, Cerberus 8.5, BlackDragon 9.0, NightmareStallion 9.0.

---------------------------------------------------------------------------------------------------------------------
## 1. Review-1 items, status

| # | item | status |
|---|---|---|
| M0 | saddle waiver (18 % to 10-14 %) | **accepted**: builder reports 11.7 % side. I could not re-measure it, since no `WH_SADDLEDBG` render is in the folder (see NICE 3) |
| M1 | torso soot cut | **closed**: the chest band is 77 % lavender; the lower torso is 99.5 % lavender; the dark saddle is the top band only |
| M2 | tail: lavender root, soot tip | **closed**: Tail1-2 lavender, Tail3 and the tuft soot (see note) |
| M3 | mane leans back | **partial** - see MUST 1 |
| M4 | indigo off Raiju | **closed**: H 236 (from 231); the accent is lighter (V 240) than Raiju's body (V 182); 35 and 28 degrees from the violets |
| NICE 1 | shorter front socks | **closed**: the sock covers 18 % of the shin; the paws still read as white feet |
| NICE 2 | narrower chest plate | **partial**: narrowed to 0.090, but from below it is still a flat white slab - see NICE 1 |
| NICE 3 | lavender upper muzzle, MIST jowls and jaw | **closed**: the close-ups show a lavender muzzle, white jowls and a dark nose |
| NICE 4 | fangs 0.075, bigger eyes | **closed** for fangs (they read in the close-up). Eyes are bigger but still about 1-2 px at icon size - see NICE 2 |
| NICE 5 | rising belly line | **accepted by eye**: the chest-to-hip underline rises slightly into the mist tuck; not measured |
| NICE 6 | HEIGHT 8.5 | **partial** - see MUST 2 |
| NICE 7 | under-view | **closed**: `low_below.png` supplied; it shows the two slabs in NICE 1 |

*Note on M2:* the plan (section 5) says the tail is lavender with a soot tuft at the tip. The build is lavender for the first half and soot for the second half (Tail3 plus the tuft). That is a deliberate read and it works on the silhouette. Accepted.

---------------------------------------------------------------------------------------------------------------------
## 2. What works now
- **Ghost read:** the body is pale lilac-ash, the saddle is a dark band on top, the legs and head are pale, and the tail's dark end matches. In `game_view.png` and `model_tq.png` it reads as a pale hound with a dark topline, not a dark wolf.
- **Face:** lavender muzzle, closed mouth, 0.075 ivory fangs, heavy soot brows, slit eyes. No googly eyes, no smile, no glint.
- **Feet:** the front socks are short and the black claws read on every paw.
- **Accent:** the indigo tips are now a lighter blue-violet, clearly not Raiju's royal blue and not the Void violets.
- **Build:** 6,820 tris, no glow, studs on the whole surface, details smooth.

---------------------------------------------------------------------------------------------------------------------
## 3. MUST (fix before the clip gate)

**MUST 1 - the mane must read as one plume, not three fins (pets/WraithHound.py, `mane_row`).** In `model_side.png` and the 128 px strip each row is a separate blade with its own blue point, so the crest reads as stacked dorsal fins. That is the Raiju back-spine read the review asked to remove. The rows still sit too far apart for the tails to merge.
- L79, centre wisp: tail length `0.25 * sc` becomes `0.36 * sc`, so the tip reaches over the next row's root.
- L80, back wisp: tail length `0.19 * sc` becomes `0.28 * sc`.
- L84, side wisps: tail length `0.20 * sc` becomes `0.28 * sc`.
- Leave the root directions and the outer-low wisps (L86) alone.
- Target: the three tips overlap into one swept crest, and the indigo points form one line along the back, not three spikes. Check `model_side` and the 128 px strip next to Raiju.

**MUST 2 - height is still below the Stallion (pets/WraithHound.py L14).** `HEIGHT = 8.5` is below NightmareStallion's 9.0. The plan (`WraithHound_plan.md` section 2) says the Wraith must look bigger and stranger than the Stallion (25 %), which is a rarer-tier signal. Also, the comment on L14 ("bigger than the Stallion's 9.0 read") is wrong; 8.5 is smaller.
- Set `HEIGHT = 9.0`. That ties the Stallion and stays under BlackDragon's 9.0 rarer tier, which the ladder allows.
- Correct the comment on L14.
- Re-run the export and check that `ground_min_z` is still at or above -0.02 at rest.

---------------------------------------------------------------------------------------------------------------------
## 4. NICE (do these too)

1. **Under-view slabs.** From below, the chest plate (L133, `rnd 0.35`) and the belly tuck strip (L132, MIST seg) read as flat white boxes pasted on the body, not fur. Raise the chest plate's `rnd` to 0.5 and the tuck seg's `rnd` to about 0.45, so their edges round off. Do not change their size.
2. **Eyes at icon size.** The slit (L161, 0.038 x 0.012) is about 1-2 px at 64 and 128 px, so the face reads only in close-up. Option: a brighter rim (INDIGO_L (176,184,255) to about (200,206,255)) or a slit 0.042 wide. Keep the slit tilt and the socket.
3. **Verify the 11.7 % saddle.** Send the `WH_SADDLEDBG` render or its share number with the next packet. My count of the top band could not isolate it from the mane root.
4. **Jowls (optional).** From the front, the white jowls are large enough to read as mutton-chop cheeks. If the face reads husky, trim them about 20 %: the jowl block at L145 (`MIST`, `Head`, half-size 0.034 x 0.068 x 0.022).

---------------------------------------------------------------------------------------------------------------------
## 5. Pass / fail checklist (round 2)

| check | result |
|---|---|
| 64 px: species reads (canid, wedge head, ears, spines) | PASS |
| 64 px: ghost reads (pale body, dark topline) | PASS (improved from round 1) |
| 128 px: mane reads as one plume, not fins | **FAIL** (MUST 1) |
| Fierce face: slit eyes under brow, closed mouth, fangs, no googly eyes, no smile | PASS (eyes need NICE 2 at icon size) |
| Studs on the whole surface, details smooth, no glow | PASS |
| Tris <= 15k (6,820) | PASS |
| Dark body + pale underside + one accent (ghost exception) | PASS (pale flank 99.5 %, dark top band only) |
| Saddle 10-14 % (waiver) | PASS on the builder's 11.7 %, not re-measured (NICE 3) |
| SOOT <= 38 % side | PASS (37.1 mine, 35.5 builder) |
| ASH_LAV + MIST >= 48 % side | PASS (58.6 mine, 54.9 builder) |
| Accent distinct from Void violets | PASS (28-35 degrees) |
| Accent distinct from Raiju | PASS (9 degrees of hue, lighter value; see NICE 2 for the icon-size read) |
| Tail per plan (pale root, soot tip) | PASS (Tail3 soot is accepted; see note in section 1) |
| No box belly, no plastic-toy slabs (side and front) | PASS in side and front |
| Plastic-toy slabs from below (chest plate, tuck strip) | **PARTIAL** (NICE 1) |
| Tier fit on the egg ladder (height vs Stallion) | **FAIL** (MUST 2) |
| Floating or poking parts (4 views + under-view) | PASS (the slabs in NICE 1 are attached, not floating) |
| Rarity fit (10 %, no hero piece) | PASS once MUST 1 and MUST 2 land |

**Round-3 packet (short):** `model_side`, `_icons_strip_128` (Wraith first, next to Raiju, ShadePanther and BlackDragon), `low_below`, and the saddle number (NICE 3). The clip gate follows once MUST 1 and MUST 2 are in.
