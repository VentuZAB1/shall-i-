REVISE - 6/10 vs the Raiju and the refs (fierce phase 1: MODEL only, the old clips are ignored).
Right: frog legs, long arms, gills, aqua slits under a V brow, the side-view shell; teal is fine (deep teal in game).
Not yet: from behind the shell is a lumpy square backpack; from the front a box torso, horn-like hair and a trunk beak.

MUST-FIX
1. Carapace from behind (your note, confirmed: the 2 R45 copies make a lumpy octagon, which reads as a backpack or pineapple).
   Delete both R45 blocks. Change the carapace (0.285, 0.09, 0.28) -> (0.25, 0.10, 0.31) with bot=(0.60, 0.9), top=(0.90, 0.8),
   rnd 0.45, and the inner dome (0.22, 0.075, 0.215) -> (0.19, 0.07, 0.25) with the same bot. It becomes an oval shield, wide
   at the shoulders and narrow at the belt. Tile real scutes on its +y face like the Tortoise does (bent to the taper,
   LESSONS item 2): 3 vertebral scutes (0.07 x 0.085 half, 0.02 thick, SHELL_L ~(128, 152, 98)) at local z -0.17 / 0 / +0.17,
   3 costal per side at x +-0.13, 0.02 RIDGE gaps; keel spikes on the vertebral row only; 8 flat marginal tiles instead of
   the 3 rim blobs per side.
2. The torso front is a rectangle (the owner's box complaint). Chest bot=(0.74, 0.84) -> (0.62, 0.84); plastron
   bot=(0.75, 1) -> (0.45, 1) so it narrows to the belt like a shield; plastron bars (bottom -> top) 0.12/0.15/0.155 ->
   0.08/0.11/0.14 to fit the new taper. Shoulder balls (0.08, 0.08, 0.075) -> (0.07, 0.07, 0.065), 0.02 lower.
3. Hair: from the front, the 5 / 175 deg locks stick out level like 2 horns (LESSONS item 6). Change their direction z
   -0.45 -> -1.1 and L 0.17 -> 0.13, and the 40 / 140 deg locks z -0.45 -> -0.8, so they hang over the ears as shaggy hair.
   Keep the 72-108 deg back fan (it reads great from behind).
4. Beak from the front: a long trunk that fills the face up to the brows. Upper beak start z hb+0.13 -> hb+0.095 and
   half-height 0.06 -> 0.05, leaving a teal strip under the eyes. Half-width 0.085 -> 0.105 with top=(0.40, 0.6), and the
   hook end z hb-0.005 -> hb+0.03. From the front it becomes a wide V wedge, and it stays hooked in profile.
5. The dish reads as frosting or a snow ring (a studded, bumpy rim). Set nostud=True on the plates and the 8 rim blocks, and
   raise the rim 0.022 -> 0.03 so the aqua water sits sunken in a smooth plate. Keep the light colour (a great 64 px read).
6. Head side: delete the dark square "ear hole" stickers (or shrink them to 0.02 x 0.02). Jowls (0.05, 0.10, 0.06) ->
   (0.04, 0.08, 0.05), top=(0.6, 0.6), rnd 0.45.

KEEP
- The crouched frog legs with webbed, clawed 3-toe feet; the knee-length arms with webbed claw hands.
- The aqua slit eyes under the V brow, the aqua gill stripes, the navy rope mawashi, the side-view shell with keel spikes.
