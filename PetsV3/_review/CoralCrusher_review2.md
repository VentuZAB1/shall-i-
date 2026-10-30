# Coral Crusher - model gate review 2 (2026-10-27) - APPROVED WITH FIXES

**Score: 7/10 for a 15 % Medium (ship bar 8).** Round 1 was 6/10. Almost every round-1 MUST landed, and the crab now reads
as a crab from the front, the side and the game camera: low shell, shorter legs, raised shell plates, big rose spikes, small
fierce mandibles. The fixes below are colour and stud changes plus one clip decision, not a rebuild. Clips can start once
**M1 and M2 are decided** and M3 is set. Round 3 is a render check only (claw closeups, shares, the crossfade decision).

**The coordinator's question: do the broad cream claw undersides read as plastic inserts?** Yes. They read as white
mittens or marshmallow stuck to the palms (close_sheet claw panels, model_front, the wave frames in `_walkgate_sheet`). They
are also studded like the body. This is the "plastic toy" look the owner rejected before, so M1 is a MUST.

## What I looked at
- `CoralCrusher/MODEL_NOTES.md` ROUND 2 section (the lead rulings: yaw 45, HEIGHT 6.1, the portrait alternatives)
- `renders/`: `_model_sheet.png` (tq, front, side, back, 600 px each), `_close_sheet.png` (claw tq and side, face front and high),
  `_icons3_strip_64/128.png` (kit portrait, ALT portrait, game-camera icon, Kappa, Turtle, Kraken, Hammerjaw, Orca),
  `_crossfade_sheet.png` (9 frames, idle to walk, 0.3 s), `_walkgate_sheet.png`, `model_front.png`, `gamelook_game.png`,
  `flat_side/tq/game.png`
- Round-1 review (`CoralCrusher_review1.md`) to check each item
- Plan §5 ("stud skin on the carapace and the arm blocks; not on the spikes, eyes, claws, teeth, legs") and Creature Style
  ("details... claws... stay smooth")

## Value shares (re-measured from the flat renders, background and anti-alias pixels excluded)

| colour | side (mine / builder) | tq (mine / builder) | game (mine) | target |
|---|---|---|---|---|
| dark slate SHELL_D | 19.1 / 18.2 | 18.3 / 17.8 | 14.6 | <= 20 side |
| BELLY_PALE | **5.6 / 5.4** | **11.4 / 10.3** | 1.0 | >= 5 side, >= 4 tq |
| ROSE + ROSE_D | 11.3 / 12.3 | 12.4 / 13.4 | 12.0 | >= 10 |
| BRONZE_D (new) | 15.6 | 8.6 | 11.7 | - |

The numbers reproduce within about one point. The pale **target is met but in the wrong place**. In the side view, about
**77 % of the pale pixels are on the claws** (the cream palm underside); the shell lip and sternum give only about 1.3 % of the
side view, because the legs hide the lower flank. In the tq view the split is about half and half. The target is met by
the claws, which is the wrong surface (M1).

Size: 12,156 tris (cap 15k). HEIGHT 6.1 studs (lead ruling: same in-game body size as round 1). Accepted.

## 1. Round-1 items, checked

| r1 | item | result |
|---|---|---|
| M1 walk turn | yaw 45 (lead ruling) | **PARTIAL.** The turn is smaller, but the crossfade is a skate (M2). |
| M2 legs | knees z 0.30, leg chain 0.38H, merus BRONZE_D | **PASS.** Low shell, legs read as crab legs, not stilts. |
| M3 mandibles | small slate plates, ivory hook tips | **PASS.** Fierce, not buck teeth. The mouth reads as a dark slot with fangs. |
| M4a armour | raised slate plates, stepped rear ledge | **PARTIAL.** The shell has structure now. The Turtle still reads more armoured (N1). |
| M4b pale underside | cream lip past the rim + cream underside | **PARTIAL.** The lip reads as a pale edge (side, close_front). Most of the pale is on the claws (M1). |
| M5 portrait | game-camera / ALT icon | **PASS if used.** The game-camera icon (item 3) reads as a crab with claws up at 64 and 128 px. The kit portrait (item 1) still reads as a flat lying slug. Do not ship the kit portrait (M3). |
| M6 rose | bigger spikes | **PASS.** The rose is the one bright accent, clearly readable in gamelook_game and at 64 px. The margin is now a busy pink row, acceptable (N4). |
| M7 halo | normals + stud colours | **PASS.** The bronze stalks and knuckle are darker and smooth; the halo is gone in close_high. |
| N1 brows | one V plate | **PASS.** The face now reads grumpy and fierce. |
| N2 keels | strips dropped | **PASS**, but the cream claw undersides came back in a bigger form (M1). |
| N3 rest claws | down 15 deg | **PASS.** The act's lift from the new rest is clear in the walkgate wave frames. |
| N4 copper | (200,136,88) | **PASS.** The game colour is a warmer copper now, not chocolate. |
| N5 rose lightness | (255,135,165) | **PASS.** The rose reads pink in gamelook, not mauve. |

## 2. New findings

### F1. The cream claw undersides are plastic inserts, and they are studded
- They are a flat, sharp-edged cream plane on the lower third of each palm, and they carry the same white stud dots as the
  body (close_sheet top panels, model_front).
- They break two rules: "claws stay smooth" (Creature Style, and the plan §5 "not on the claws") and the
  "no plastic toy" read. They are also the reason the side-view pale target is met.
- In the walk wave frames the raised claw reads as a white glove.

### F2. The crossfade skates the feet (`_crossfade_sheet.png`)
- The builder's simulation gives about 0.79 BU of ankle travel during the 0.3 s blend (about 0.73 of it is the 45-degree
  turn itself). At this model's scale that is about **4.6 studs in game in 0.3 s**. Every idle-to-walk start will show the
  outer feet skating.
- The feet stay on the ground (ankles at 0.066-0.068 BU, never sink), so this is a skid, not a sink. It is still visible at
  play distance.
- The lead ruled out a runtime hook. So the fix must be in the clips: see M2.

### F3. Pacing of the arm wave is fine
- The wave lifts the claw about 45 degrees from the new rest and the feet stay planted (walkgate f26/f40). No issues.

## 3. Deviations (round 2)
1. **HEIGHT 6.1 (lead ruling):** ACCEPT. Same in-game body size.
2. **Walk yaw 45 (lead ruling):** ACCEPT as the walk pose. The turn is a smaller snap than 90, but it skates the feet (F2).
   Condition: M2.
3. **Cream claw undersides (builder's additions):** **REJECT as built** (M1). Keep the lip and underside cream; drop the claw
   cream to a narrow edge.

---------------------------------------------------------------------------------------------------------------------
## 4. MUST (in priority order)

### M1 - Claws: smooth, and no plastic cream (the coordinator's question)
- **Drop the cream claw undersides to a narrow flush ventral edge**: at most the lowest 15 % of the palm height, full palm
  length, a thin band, not a third of the palm. Or drop them entirely; the fixed finger tip can stay IVORY.
- **Make the palm and the cream smooth** (`nostud=True`): palm tube and the cream strip. Claws stay studded only on the
  merus (the plan allows the arm blocks). Check the carpus knuckle too.
- **Move the pale share to the underside, where a real crab has it:** widen the cream lip (the pale lip L157 in round 1)
  so it drops about 0.02 BU lower and reads from the side, and keep the sternum visible from a low front camera.
- **Target:** BELLY_PALE at **>= 5 % in the side view with at most a third of it on the claws**. Side claw pale is now about
  77 %.
- Re-check with close_clawtq, close_clawside, model_front and one side view at 600.

### M2 - Walk blend: decide the foot skate before idle authoring
Two options. The builder must pick one and show it:
- **A (recommended, no runtime hook):** set the idle, roar and act base pose to **the walk's spine yaw (45)**, so the idle
  to walk blend turns nothing and only the leg phase blends. The crab then rests angled 45 degrees, which crabs do. Re-run
  the crossfade simulation and show the ankle travel, target **<= 0.2 BU**.
- **B:** keep the idle at yaw 0 and accept the skate. Then the lead must sign it off in writing, with a Studio play test at
  play distance (the simulation is not a Studio run). Target still: ankle travel <= 0.8 BU, and no claw cross-over.

Either way, re-run the walk gate on the final rest pose. The tripods (L1/R5/L3 vs R4/L2/R6) and the planted-feet numbers
(collision_free, ground_min_z >= -0.02, slide 0) stay the same.

### M3 - Index portrait: ship the game-camera icon
- **Do not ship the kit portrait** (`_icons3` item 1). It reads as a flat slug at 64 and 128 px.
- Ship **the game-camera icon** (item 3). It reads as a crab with claws up, and it is the best of the three at 64 px next
  to Kappa, Turtle, Kraken, Hammerjaw and Orca. The ALT portrait (item 2) is the fallback.
- The lead / Studio import decides which file is uploaded. Confirm in writing which file the Index shows.

---------------------------------------------------------------------------------------------------------------------
## 5. NICE

- **N1 Armour vs Turtle:** the shell reads as a bronze dome with dark seams. Add one more plate row: a second raised ridge
  across the dome (0.02 BU proud) or a slate plate on each side of the H groove. Then check the lineup: the crab should read
  more armoured than SeaTurtleWarrior (25 %).
- **N2 Stud skin on the arm:** the merus stays studded (allowed), but make the carpus knuckle smooth so the cream and the
  studs do not meet at the joint (see F1).
- **N3 Rear ledge:** from the side the stepped ledge reads as a dark band. Lower its top by about 0.01 so the shell reads as
  one dome, not a dome with a shelf.
- **N4 Rose margin:** the margin is now a continuous pink row, which busies the side silhouette. Alternate the sizes
  (large, small) so the rim reads as spines, not a fringe.
- **N5 Walk claw:** in walkgate panels the crusher claw stays raised through the walk. Lower the walk pose claw about 10
  degrees so the walk reads as a scuttle, not a boxer's guard.

---------------------------------------------------------------------------------------------------------------------
## 6. Pass / fail checklist

| # | check | result |
|---|---|---|
| 1 | Silhouette at 64 px (game-camera icon) | **PASS** (kit portrait FAIL: M3) |
| 2 | Crab, not a spider or bug | **PASS** (legs fixed) |
| 3 | Fierce face (brows, slits, mandibles) | **PASS** |
| 4 | No box belly; underside reads pale | PARTIAL (lip reads; claws carry the share: M1) |
| 5 | Dark body + pale underside + ONE accent | PARTIAL (pale on the wrong surface: M1) |
| 6 | Rose accent reads at 64 px and in game | **PASS** |
| 7 | Armour reads more than the Turtle | PARTIAL (N1) |
| 8 | Hard rules: studs on body, claws smooth, no Neon, <= 15k tris | **FAIL** on claws (M1); tris 12,156 PASS |
| 9 | Floating, intersecting, see-through, inside-out | PASS (normals check; the halo is gone) |
| 10 | Palette shares reproduce | **PASS** (within about one point) |
| 11 | Walk: planted, tripods, no snap, no skate | PARTIAL (tripods PASS; skate: M2) |
| 12 | Deviations accepted only where better | HEIGHT 6.1 ACCEPT; yaw 45 ACCEPT with M2; cream claws REJECT (M1) |

Round-3 check: claw closeups (tq and side), the shares, the crossfade decision (M2), and the chosen portrait file (M3). No full model round is needed.

**APPROVED WITH FIXES, 7/10.** Ship bar 8: M1, M2 and M3 must land before the clip gate.
