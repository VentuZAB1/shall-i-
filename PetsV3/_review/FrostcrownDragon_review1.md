# Frostcrown Dragon - model gate review 1 (2026-10-27) - REVISE

**Score: 6/10 for a 0.1 % mythic (ship at 8+).** The build is clean: real anatomy, a fierce face, studs on the hide with
smooth details, a gold crown that reads, tris well inside the gate. It does NOT outclass the 1 % secrets yet. It is the
palest of the three, its signature fins are too small to read at 64 px, and from the front the crown reads as a pair of
yellow ears. Every fix below is numeric, inside `pets/FrostcrownDragon.py`, and needs no bone rename. Tris headroom is
about +2k.

## What I looked at
- Brief, `Creature Style.md`, `Model Review Checklist.md`, `Creature Animation.md`, `FIERCE_GUIDE.md` (Obsidian and PetsV3).
- `_review/FrostcrownDragon_plan.md` (v2), `GLACIER_CONCEPTS.md` (OWNER DECISIONS), section 2.6 of `GLACIER_PLAN_REVIEW.md`.
- `FrostcrownDragon/MODEL_NOTES.md` and `pets/FrostcrownDragon.py` (read in full).
- Renders: `_model_sheet`, `_close_sheet`, `_idle_sheet`, `flat_game`, `_icons_strip_64`, `_icons2_strip_128`.
- Comparisons: ThunderRex and CosmicLeviathan `_model_sheet` + `_icons_strip_128`; CelestialDragon `_model_sheet`;
  Raiju `_model_sheet` (calibration); `_ALL_FIERCE_progress.png`.
- My own numbers: pixel shares measured on the icon strips (table below). The crops I made are in `%TEMP%`, outside the
  project. I did not run Blender, so the tri count (8,140) and the gold count (60 px on the portrait) are builder-reported.

## Icon numbers (128 px cell, pet pixels only, same threshold on each strip)
| Icon | Mean luminance | Dark share (lum < 70) | Ice-white share | Gold share |
|---|---|---|---|---|
| Frostcrown portrait | **130** | **24 %** | 6.0 % | 1.5 % |
| Thunder Rex | 95 | 45 % | 6.5 % | 0.5 % |
| Cosmic Leviathan | 94 | 37 % | 2.3 % | 1.1 % |

- Gold at 64 px: my strict count on the 64 strip, cell 1, is **24 gold px**. The builder's 60 is on the portrait and depends
  on the threshold. The gate is 25, so the margin is gone.
- Ice-white at 64 px: 106 px of 5,320 (2 %). Most of it is the fins and the tail tip, and they are too small to read.

Read: the Frostcrown is about 35 % brighter than both secrets and has about half of Rex's dark mass. Its ice is no bigger
than Rex's crystal row, and its fins are much smaller. The gold is the highest of the three, so the crown is a real asset.

## Deviation rulings
- **D1 colour (88,136,210): ACCEPT the direction, PUSH further (MUST 4).** The plan palette was pastel, so the builder is
  right to move it. In the icon the body still reads cornflower sky-blue at the same brightness as the sky, and it is the
  lightest of the three rare pets. The plan palette does not come back.
- **D2 DARK 14-19 %: ACCEPT.** The dark fingers and trim frame the pale parts. Dark share in the icon is 24 %.
- **D3 five fins, not seven: REVISE to seven, and bigger (MUST 1).** The count was cut for tris. The tris have room.
- **D4 wing root back, tallest fin forward: ACCEPT.** Three fins now show from the side. They are still too small (MUST 1).
- **D5 ICE_W claws on DARK bases: ACCEPT.**
- **D6 placeholder idle (ground fold): ACCEPT for this gate.** Clips are the next gate.

## Lead's question: what to add to clearly outclass Rex and Leviathan (64 px and close-up)
| Feature | Now | Target | Where (`pets/FrostcrownDragon.py`) |
|---|---|---|---|
| Dorsal crystal fins | 5 fins, 0.31-0.48 BU tall | 7 fins, 0.40-0.60 BU tall, chords +20 % | L41, L283-287, L295 |
| Ice-white share, portrait | 6.0 % | >= 9 % | fins + frost core + tail tip |
| Gold at 64 px (strict count) | 24 px | >= 40 px | L267-281 |
| Gold share, portrait | 1.5 % | >= 2.5 % | same |
| Crown read from the front | two yellow ears / V of horns | 5-point band, tall centre point | L272-281 |
| Chest / core feature | none; ICE_BELLY plate + DARK bars read as a grille | ICE_W faceted frost core, 0.20 BU wide | L203-214 |
| Tail feature | 0.32 BU tip, invisible in the icon | 0.44 BU tip + 0.26 BU side blades | L357-364 |
| Body value (mean lum, pet px) | 130 | <= 115 | L20, L23, L24 |
| Dark share, portrait | 24 % | >= 30 % | same |
| Tris | 8,140 | about 10k (gate 13k, cap 15k) | |

Tris estimate: two extra fins about +0.8k, frost core +0.3k, tail blades +0.2k, extra crown points +0.1k, fewer belly
rungs -0.1k. That is about +1.3k to +2k, so the total is about 10k.

## MUST (in priority order)

### MUST 1 - Dorsal crystal row: seven fins, bigger (the signature must be readable at 64 px)
- `fin_spec` (L283-287), heights / chords (BU):
  - Fin_1 (Neck2): 0.31 / 0.21 -> **0.40 / 0.26**
  - Fin_2 (Neck): 0.41 / 0.26 -> **0.50 / 0.31**
  - Fin_3 (withers, the tallest): 0.48 / 0.32 -> **0.60 / 0.38**
  - Fin_4 (Spine): 0.42 / 0.29 -> **0.52 / 0.35**
  - Fin_5 (Spine): 0.32 / 0.24 -> **0.42 / 0.29**
- Add **Fin_6** on the Tail1 base (0, 0.66, 0.94), h 0.30, chord 0.20. Add **Fin_7** on the Tail2 base (0, 1.12, 0.80), h 0.24,
  chord 0.17. Both ICE_W, the same frost_fin pattern.
- `frost_fin(... 0.075 ...)` at L295: thickness 0.075 -> **0.085**, so the blades do not vanish in game.
- `FIN_BONES` (L41): `range(1, 5)` -> `range(1, 8)`.
- **BUILD GOTCHA:** the rig loop (`for i, (nm, parent) in enumerate(zip(FIN_BONES, ("Neck2", "Neck", "Chest", "Spine", "Spine")))`)
  is zipped against a 5-tuple. With seven fins it silently drops Fin_6 and Fin_7 from the rig. Extend the tuple to
  `("Neck2", "Neck", "Chest", "Spine", "Spine", "Tail1", "Tail2")` and add `FX_FinSpark_6/7` anchors.
- After the change, check Fin_3 against both Wing roots (the wing root moved back in D4) and Fin_6/7 against the tail. The
  `check_pairs()` list already covers these pairs.

### MUST 2 - Frost core on the chest, and remove the grille
- Replace the ICE_BELLY keel plate (`seat_plate(... ICE_BELLY, "Chest" ...)`, about L209-210) with an **ICE_W faceted diamond**
  ("frost core"): 0.20 BU wide, 0.26 BU tall, seated proud by 0.012 on the chest. Give it an ICE_BELLY inner facet (use the
  frost_fin facet pattern). Keep `ANCH["Core"]` (L214) at its centre.
- Delete the four DARK keel scute gaps (L211-213). They read as a grille.
- Belly rungs (L205-208): cut the four DARK bars to two (at t 0.40 and 0.80), or none.
- Why: from the front (`_model_sheet`, top-middle) the chest is a white radiator grille, and from the side it is a ladder.
  The body needs ONE crystal focal point, the way Rex has a chest emblem. That is the "crystal vs studded hide" contrast the
  rare-tier rule asks for.

### MUST 3 - The gold crown: bigger, and a crown from the front
- Horn base width `horn(B, P, 0.066, ...)` (L269): **0.066 -> 0.080**.
- Horn tip `P[3]` (L267-268): `(s*0.285, 0.64, 0.38)` -> **`(s*0.31, 0.74, 0.40)`**.
- Diadem band (L272): `(0.13, 0.022, 0.032)` -> **`(0.15, 0.030, 0.040)`**. Diadem sides (L274-276) radius 0.016 / 0.032 ->
  **0.022 / 0.040**. Diadem back (L277-278) height 0.03 -> **0.04**.
- Points (L279-281): three -> **five**, at x = -0.10, -0.05, 0.00, +0.05, +0.10 with heights 0.06, 0.09, **0.13**, 0.09, 0.06.
- Why: from the front (`_model_sheet`, top-middle; `_close_sheet` left) the swept horns are a yellow V of ears. That is
  close to BlackDragon's antler V. A five-point band with a tall centre point is the crown read.
- Targets: >= 40 gold px at 64 px (strict count), >= 2.5 % gold in the 128 portrait.

### MUST 4 - Value: a darker steel, a darker top band, pale membranes
- L20 `STEEL_BLUE` **(88,136,210) -> (70,118,190)**. Hue stays 216. Brightest channel 190 keeps the >= 170 rule. In game this is
  about (42,71,114).
- L24 `DEEP_STEEL` **(58,86,156) -> (38,64,130)**. The 3-band blocking needs this. Right now the dark top band is not visible
  in the icon.
- L23 `MEMBRANE` **(150,178,228) -> (116,146,206)**. The folded wings wash out the white fins at the moment.
- Targets: mean luminance of pet px in the 128 portrait <= 115 (now 130). Dark share >= 30 % (now 24 %).
- Do not go darker than this (Rex is 95). The steel read and the premium look need the mid-tone.

### MUST 5 - Tail: a visible crystal finish
- L360 tip spike `0.32 x 0.065` -> **`0.44 x 0.085`** (ICE_W, keep the ICE_BELLY spike at L364).
- L362 side spikes `0.19 x 0.042` -> **`0.26 x 0.05`**.
- Why: the tail tip is a notch at the back of the portrait and is invisible at 64 px. It is the second frost feature and it
  balances the fins at the back of the silhouette.

## NICE
- **N1** Head skull, L232: `(0.155, 0.16, 0.125)` -> `(0.17, 0.175, 0.135)`. The head reads small under the crown from the game
  camera. Keep the slit eyes and the brows as they are; the face passes.
- **N2** Foreleg upper arm radius (the `B.seg(H + ..., K, 0.105, 0.13 ...)` line): 0.105 -> 0.12. The thin legs read weak at 64 px.
- **N3** The three DARK ridge spikes (L312-315). Keep them dark; the value change in MUST 4 makes them read.
- **N4** The face (slit eyes in black sockets, brow spines, ICE teeth): keep. It is the fierce read the style asks for.

## Pass / fail checklist
| # | Item | Result | Note |
|---|---|---|---|
| 1 | Species reads at 64 px | PASS | Winged 4-legged dragon with a gold head read |
| 2 | Fins read in silhouette | FAIL | Too small (MUST 1); 3 of 5 visible from the side but barely |
| 3 | Fierce face (no round eyes, no glint, no smile) | PASS | Slits, heavy brows, fangs |
| 4 | No box belly / no toy slabs | PARTIAL | Chest reads as a grille (MUST 2); back shells read as plates |
| 5 | Studs on hide, smooth details | PASS | Studs on body / neck / legs; fins, horns, claws, membranes smooth |
| 6 | Palette follows plan (D1) | PARTIAL | D1 direction accepted; value still too light (MUST 4) |
| 7 | Accent strong in game colours | FAIL | Ice is 6 % but in small shapes |
| 8 | Gold hero >= 25 px at 64 px | MARGINAL | 24 px strict count (MUST 3 for margin) |
| 9 | Crown reads as a crown from the front | FAIL | Yellow V of ears (MUST 3) |
| 10 | Rare tier outclasses Rex and Leviathan | FAIL | Luminance 130 vs 94-95; dorsal spectacle lower |
| 11 | Distinct from siblings | PARTIAL | Gold horn V is close to BlackDragon's antlers; gold crown + spine row is Rex's recipe. Fins are white, not Rex's cyan, which is right |
| 12 | Tris within gate | PASS | 8,140 builder-reported; step-1 gate 13k, cap 15k |
| 13 | No glow / no Neon | PASS | |
| 14 | Name is two words | PASS | Frostcrown Dragon |
| 15 | No floating / intersecting parts | NOT CHECKED | Clip gate `collision_free` next; Fin_3 vs Wing root and Fin_6/7 vs tail after MUST 1 |
| 16 | Gate renders complete | PARTIAL | No 600 px game-camera or rear 3/4 view, no same-camera comparison sheet |

## Next round: send with the revision
- `_model_sheet` (600 px), `_close_sheet` (front and side crowns), `flat_game` plus the value shares.
- `_icons_strip_64` and `_icons_strip_128` with the same camera next to ThunderRex, CosmicLeviathan, CelestialDragon,
  BlackDragon and Ivonrath. Show the Frostcrown portrait and the game-camera icon.
- The step-1 tri count and `collision_free` output from the run.
- The placeholder idle sheet. The clip review follows separately.

Verdict: **REVISE, 6/10.** Do MUST 1-5 and send the next round. Once the fins, the frost core and the crown read at 64 px,
and the value is at or below 115, this is the mythic.
