# Ice Mammoth - model gate review 2 (2026-10-27) - APPROVED WITH FIXES (model)

**Score: 8/10 for a MEDIUM 26 %.** Round 1 was 6/10. Every round-1 MUST now passes on measured numbers, and the trunk, the
underside, the dome and the accent all read. No blocking MUST remains. The mesh and rig are cleared for clip authoring on the
current bone names. Two small NICE items and one in-game check go with the clip round (below).

## Round-1 MUST status
| # | item | round-1 | round-2 (my count) | verdict |
|---|---|---|---|---|
| M1 | MINT accent | 0.12 % side, 0.03 % game, invisible at 64 px | 1.9-2.0 % side (builder 2.3), 0.8 % game (builder 1.0); about 30 mint-hued px in the 64 px icon (0.8 %), 1.0 % at 128 px | **PASS** (target 1.5 % side, 0.8 % game) |
| M2 | Body colours | CHAR 162 brightest, grey-slate in game; WOOL near-black | CHAR (96,168,184) brightest 184, S 0.48; WOOL (80,110,124) brightest 124; game est. CHAR (58,101,110), WOOL (48,66,74) | **PASS** on the rule (see check 1) |
| M3 | Pale underside | 0.7 % side, 0.09 % game | 3.0-3.3 % side (builder 3.3), 0.6-0.9 % game (builder 0.9); band runs to the rump | **PASS** (side and under view; the game camera sees little of it, see note) |
| M4 | Dome silhouette | spiky head cap and spine ridge | rounded clumps (top 0.6-0.7); wool dome is the top; WOOL 43-44.5 % game | **PASS** |
| M5 | Round-2 deliverables | missing | under.png, trunk_icon_64_x4.png, flat_side/tq/game, 64/128 strips, combined strip (VoltRhino/_scratch/_all_strips_r2.png) | **PASS** |

Flat-render shares I counted (object pixels, background excluded): side CHAR 58.8 / WOOL 23.9 / BELLY 3.0 / TUSK 2.9 / DARK 2.9 /
MINT 1.9; game CHAR 46.6 / WOOL 43.0 / MINT 0.8 / BELLY 0.6. The builder's numbers reproduce within about 1.5 points.

## Round-1 NICE status
1. Tusk socket rings in WOOL_D: **done**, they read as sockets now, and less as bracelets.
2. Tusk ice (226,240,246): **done**.
3. Skull rnd 0.55: **done**, the front reads rounder.
4. Trunk tip lowered (0.30 build, 0.21 world): **done**. In the side view the tip hangs about one stud above the ground and below
   the knee line. Trunk reads in the 64 px icon.
5. Wool skirt fringe: **done** (rows 2-3 shortened). The side view now reads as blocks.
6. Dorsal seams: **done**, two teal seams read as plate lines.
7. Brows 0.01 into the skull: **done**.
8. Accordion step 0.94: **done**, the trunk is less caterpillar-like in close-up.

## Checks the coordinator asked for
1. **Body colour in game read.** The rule holds on paper: brightest 184, S 0.48, and the wool is not near-black in game
   (48,66,74). But the lit Blender preview is bright aqua: the icon body averages about (112,180,206), V 0.81, and the side
   render about (131,190,214), V 0.84. Hue 190 reads as pool cyan, not glacier teal. In the combined strip it is the
   brightest saturated body among the blue, violet and dark pets. I could not run the game, so this is an estimate. **Check
   it in a Studio capture at the 5-stud camera before sign-off.** If it reads aqua or toy-like, use NICE 3.
2. **Mint is readable at 64 px.** About 30 px of the 64 px icon is mint-hued (hue 140-178, against the body's 183-205), so it
   separates by hue even though it is close in value. It is clearly visible at 128 px and in the game render (the left tusk tip
   reads green-mint). The 40 % cap is larger than the plan's accent (4 % share), but at 64 px the cap plus the 3 cracks is the only
   accent on the pet that reads. Accepted deviation (see NICE 1 for the edge).
3. **Underside.** under.png shows a pale band between the legs and under the barrel, plus dark toenails and pads. The pads sit
   flat on the ground line. Nothing is floating from below.
4. **Dome.** The wool clumps replace the spikes. At 64 px the top is a dome with bumps, not a crest.
5. **Tris 13,676.** It is under the 15k cap and about 0.7k above the 13k step-1 target. The extra is the tusk tubes and 54 locks.
   Accepted.

## MUST (blocking)
None. The mesh, the rig and the bone names are cleared for clip authoring.

**Before sign-off (a check, not a mesh change, owner or coordinator):**
- C1. Studio capture of the body at the 5-stud game camera. Confirm the body reads dark rich teal, not aqua. Apply NICE 3 if
  it does not.

## NICE (do them; small)
1. **Mint cap edge:** the white-to-mint change on each tusk is a hard ring (the cap starts at t 0.60, `pets/IceMammoth.py` L196-197).
   Add one intermediate ring at t 0.52 with a radius 0.002 larger than the tube, or a short taper over 0.04 units, so the cap reads
   as ice, not a dipped sleeve. Keep the 40 % length.
2. **Head clumps:** at close range the head-top clumps read as popcorn or cloud. Use two larger clumps (about 0.10 wide) instead of
   the current four to five small ones, or flatten the top with `rnd` 0.6 on the wool dome. Keep the top a dome.
3. **Body hue (only if C1 says aqua):** CHAR_TEAL (96,168,184) to **(92,160,184)**. Brightest still 184, hue 196 (was 190), S 0.50.
   That moves it off the Tide teals (Sea Turtle Warrior, Kappa) and toward glacier teal.
4. **Eye socket:** the DARK socket is (0.082, 0.012, 0.030) at L171 around a (0.074, 0.008, 0.018) slit, so the frame is about
   0.006 proud. At close range it looks slightly like goggles. Tighten the socket to (0.078, 0.012, 0.024) to keep the black socket
   the guide asks for and lose the square frame. Not a fierce-face fault as built.

## Deviations from the plan: accept or reject
- **MINT caps 40 % of each tusk (plan: cracks only): ACCEPT.** It is the only 64 px accent that reads, and it is well placed.
- **Tusk cracks: 3 per tusk at 0.035 x 0.012 (plan: 2 per tusk).** ACCEPT.
- **Tris 13,676 (plan 8-11k, cap 15k):** ACCEPT, under the cap.
- **WOOL 43-44.5 % in game (plan 18 % side):** ACCEPT as the dark mane. The game camera is looking at the back.
- **Belly 3 % side (plan 10 %):** ACCEPT. The pale band reads from the side and under. A bigger belly would bring the skirt back.
- **Toenails are blocks, not spike claws:** ACCEPT. Keep it that way for the elephant foot.

## Pass / fail checklist
| check | result | note |
|---|---|---|
| Tris <= 15k | PASS | 13,676 (builder; not re-counted) |
| HEIGHT 9.0 | PASS | builder's 1.76 units = 9.0 studs; not re-measured |
| Studded body, head, legs, trunk; details smooth | PASS | close sheet |
| No glow, no Neon | PASS | renders |
| Eyes: narrow slits in a black socket, no glint, not googly | PASS | NICE 4 |
| Brow V reads fierce | PASS | |
| Trunk reads at 128 px and 64 px | PASS | tip lowered |
| Tusks read at 64 px | PASS | |
| MINT accent readable at 64 px | PASS | about 30 px, hue-separated; NICE 1 |
| MINT accent in game colours | PASS | 0.8 % game |
| Body brightest channel >= 170 | PASS | 184 |
| Body not muddy in game (estimate) | PASS, check C1 | game est. (58,101,110) |
| Near-black only for details | PASS | WOOL game est. (48,66,74) |
| Pale underside visible (side, under) | PASS | 3.3 % side |
| Dome silhouette, no spiky crest | PASS | NICE 2 |
| Floating / poking / intersecting parts (renders) | PASS | |
| Parts visible from below | PASS | under.png |
| Trunk tip above ground | PASS by side view | clip gate `ground_min_z` confirms |
| Builder shares match the render | PASS | within about 1.5 points |
| Clip gate | NOT RUN | next round |

## Not done in this review
- No Blender run and no game run. In-game colours are the 0.6x estimate, so check C1.
- Clip gate not run. The clip round needs pose sheets, `collision_free`, `ground_min_z`, and the act beats.
