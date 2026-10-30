REVISE - 7/10 vs the references (round 1). A strong, readable red dragon from the front, but the face is grumpy rather
than "lovely-fierce, chibi but proud", the hero crown does not read, and from behind it is a stack of red boxes.

MUST FIX (most important first):
1. Face appeal (line 113). The 0.05-wide slit with the highlight beside it reads as a "□|" glyph in the 512 px crop, and
   the flat yellow square iris matches the belly bands and the crown. Use pupil_size (0.08, 0.13) (62 % of the iris
   height), hl_on_pupil=True, hl_size (0.05, 0.035); add a darker lower-iris band IRIS_D (232, 118, 20) over the lower
   40 % of each iris (Cvetibara lines 172-175); brow_spec (0.26, 0.05, 10) -> (0.22, 0.04, 8). Proud and cheeky, not angry.
2. The crown is buried: the band (line 130) spans z 1.735-1.815 on a head top at 1.78, so only 3 tiny spikes show (a
   yellow tuft from the front, nothing from behind). Band centre (0, -0.80, 1.83), half (0.27, 0.12, 0.05), standing
   0.10 proud between the horn roots; 5 points on its top edge (h 0.10 / 0.15 / 0.20 / 0.15 / 0.10, w 0.045); gem on
   the band's FRONT face at (0, -0.926, 1.83), half (0.05, 0.006, 0.04).
3. The gold tips of the back spikes are invisible: at 80 % of the length the dark blade (top=(0.45, 0.10)) is already as
   big as the gold block (lines 142-145) and hides it. Per §2a: end the dark blade at 70 % of L, then a GOLD spike for the
   last 30 % that continues the blade's taper. From behind, the crest should read red -> gold.
4. The back of the head shows a second face: 2 plates side by side above the dark tip of the Neck spike (back view).
   Drop "+y" from the head studs (line 99); add a crest blade on the head's back face at (0, -0.50, 1.58), sz 0.7, bone
   "Head", laid back like the others, so the crest runs from the crown to the tail.
5. From the back 3/4 view the tail end reads as an elephant trunk with a square flag (the last segment climbs 0.26).
   TAILP[3] -> (0, 1.74, 0.70) (move the Flame joint with it); spade 0.19 -> 0.24 half length with a GOLD tip block on
   its last 30 %, matching the spikes. Re-run collision_free for the tail against the legs and wings.

KEEP:
- The big head on the chunky stepped chest with the 4 light belly bands, the cream jaw and the smirk with 1 fang.
- The 2-tone scalloped membrane wings with the ivory wrist claws.
- The big ivory 3-segment swept horns, which give a great silhouette at 64 px.
