REVISE - 7/10 vs the Raiju and the refs (fierce phase 1: MODEL only, the old clips are ignored).
A real tank: the keeled 3-row dome, the saw rim and the hooked snapper beak read at 64 px from every side. Two things keep it
under 8. The shell is solid, so the head and forelegs have nowhere to go in act_hide. The head is also a box in profile.

MUST-FIX
1. Build the shell MOUTH that act_hide needs (FIERCE_PLAN: hollow front 0.35 S; owner: it sleeps and hides in its shell). The
   only gap today is a 0.16-tall slot (plastron top z 0.42 to MID bottom 0.58), and the neck already sits inside the solid
   rim/MID. Cut a cavity x +-0.30, y -0.80 -> -0.24, z 0.42 -> 0.88: rim slab y -0.46..0.80 -> -0.24..0.80, with the 2 corner
   blocks extended back to y -0.24; split MID into a back block (y -0.24..0.776), 2 side walls (|x| 0.30..0.62) and a roof
   over the opening; SEAM back wall at y -0.24. Drop the centre "-y" MID tile and keep the 2 side tiles as the opening's
   cheeks. Move the hood up to the top edge (centre ~(0, -0.75, 0.86), same size, ~0.12 overhang). Result: a dark arch
   ~0.60 W x 0.46 H around the neck in the front and tq views. The head (0.45 W x 0.43 H) slides fully in, and the two scaled
   forelegs (0.28 W each) can plug it. The legs need no change, because the dark rim underside already swallows them.
2. Head profile (your note, confirmed in close_side: a box with a box glued on, and the cream jaw reads as a loose plank).
   Skull seg top=(0.50, 0.62) -> (0.50, 0.42) so the forehead slopes into the beak. Cheeks (0.065, 0.12, 0.08) ->
   (0.05, 0.09, 0.06), rot (-15, 0, +-12), top=(0.6, 0.6), rnd 0.45, x 0.16 -> 0.15, so they read as jowls. Jaw seg
   top=(0.42, 0.62) -> (0.42, 0.40), SKIN on top, and PLAS only as a 0.02 underside strip.
3. Brow (0.092, 0.045, 0.033) -> (0.11, 0.05, 0.042), 0.015 further forward. In the side view it should be a ledge over the
   lime slit; today it is a small cap behind it.
4. The "Mossback" name: the back view shows only 3 lime specks. Scale the 5 tufts x1.3 and add 2 in the back half
   ((MID, "+x", 0.55, 0.97) and (MID, "-x", 0.55, 0.97)), so the 64 px back view carries 4-5 lime chunks >= 0.13 wide.
5. Keel ridges: SHELL_L (146, 130, 80) -> (176, 158, 100), so the pyramid rows still separate from the (120, 106, 64)
   scutes in game. This lifts the ridges and darkens nothing; tones only 1.2x apart merge after the Roblox shift.
6. Tail from behind reads as a grey ladder (pale rod + dark rungs): tail SKIN -> SKIN_D, its 5 spikes BEAK -> SHELL_L.

KEEP
- The keeled triple-row dome, the serrated back rim and the dark seam belt: the "tank" silhouette is the hero.
- The hooked dark beak, lime slit eyes and chin barbels: a real alligator-snapper face, not a cartoon turtle.
- The scaled column forelegs with 5 black claws. They become the shield in act_hide.
