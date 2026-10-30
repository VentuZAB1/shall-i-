REVISE 5.5/10 - the 64 px read is clear (a trident taller than the pet, coral band tails, a shell), and the trident, plastron and coral accents are good.
It is still the most toy-like pet of the batch: a flat cube head with a coral lid, a small "nose" beak that covers the inner third of each eye, a
waffle-grid backpack from behind (the view players see most), robot knee sockets, and one flat mint on every limb.
(Phase 1 = model only. The clips were not judged. The mint lands as darker teal in game, so don't darken it. On your rest-pose flag: the guard-stance idle will
bend it. The toy look comes from items 1-6, not from the pose.)

Must fix:
1. Waffle backpack (model_back): the 3x3 SHELL_L squares, each with a KEEL pyramid, read as a grid or radiator, not the plan's 5 keels. Delete the 9 squares and
   9 peaks. Run 5 continuous KEEL ridges top -> bottom: 3 on the dome's back face at u = 0, +-0.13 (local v -0.24 -> +0.26) and 1 per side along the sloped
   flank (replacing the 3+3 flank spikes). Each is 0.05 wide and 0.035 proud (the centre one 0.05), ending in a point at the serrated rim. Optional: flush SHELL_L
   scute inlays (<= 0.01 proud) between them.
2. Cube head with a coral lid: the skull is only 0.30 tall (plan 0.18 H = 0.39) and the band is a solid slab flush with its top, so tq/front show a box with
   a coral lid and teal squares on it. Skull half z 0.15 -> 0.18, centre z 1.62 -> 1.65 (bottom unchanged), top=(0.84,0.86) -> (0.70,0.72), rnd 0.45.
   Move eyes and brows up 0.03 and the band to sit just above the brows (~z 1.75). Re-fit the band's half size to the skull there (~0.16 x 0.17, +0.012), and move
   the SCALE scutes to the new SKIN crown so a domed head shows above a headband.
3. Small nose beak: from the front the tan beak is a narrow trapezoid under the eyes, a snout rather than the plan's massive hooked loggerhead beak. Its top
   also buries the inner third of both slits (close_front). Using the room from item 2: root half width 0.155 -> 0.18, hook spike 0.10 -> 0.15 long, 0.048 -> 0.068
   wide, aimed (0,-0.1,-1) so it hangs over the jaw tip, jaw half width 0.13 -> 0.155. Keep the beak's top under the sockets so the full coral slits show.
4. Robot knee sockets: the KEEL spike points straight forward, so model_front/tq show a black square in the middle of a blue square. Re-aim it up the guard as
   a keel: root kg + (0,-0.035,-0.06), dir (0,-0.35,1), length 0.07 -> 0.12, width 0.04 -> 0.03. Or delete it.
5. Shell hangs off the back (model_side): the KEEL rim flange is a flat 0.94 x 0.92 plank between body and dome, and the dome ends 0.28 behind the back.
   Dome centre y 0.29 -> 0.25, local half z 0.23 -> 0.21. Flange y 0.21 -> 0.19 and half (0.47,_,0.46) -> (0.44,_,0.44), so only its serrated lower rim shows.
6. Toy finish: the plan's darker scale pattern exists only on the crown. Add flush SCALE scale inlays (<= 0.01 proud, polygons 0.07-0.10 wide, 3-4 per part)
   on the outer forearm blades, shins, thighs and neck sides. Add nostud=True to every Trident block; a studded shaft reads as a plastic toy.

Keep:
- the trident: 1.15 H, barbed prongs, pearl, 2 coral wraps. It's the strongest far-read shape
- the cream plastron of stacked tapered plates on the V-taper chest, plus the spiked shell pauldrons
- the coral accent budget: war-band + 2 ragged tails, shaft wraps, slit eyes under heavy brows
