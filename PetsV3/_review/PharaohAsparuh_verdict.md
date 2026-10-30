REVISE - 6/10 vs the references (round 1). From the front it is the charmer of the set (a ref_05 cat face plus the
pharaoh costume). From the side and back it is a white tower on a grey box under a stack of pancakes, and the V2
half-lidded look is gone.

MUST FIX (most important first):
1. The rear half looks like grey concrete. Body (line 77), haunches (102), Shin_B (104) and tail (128, 131) are SHADE
   (222, 206, 188), only 15 % saturated, which renders as grey stone and splits the cat at the chest's back face into a
   white front and a grey back. Make all of them FUR: one cream Persian, as in V2 (SHADE unused or underside only).
2. The back view is 3 stacked boxes: head back, a 0.32-tall flat chest wall (z 0.52-0.84), then the body.
   (a) FUR shoulder-slope block on Spine: centre (0, 0.16, 0.62), half (0.40, 0.30, 0.10), rot (-26, 0, 0), ends
       buried in chest and body, so the top runs from the chest top (z 0.84) to the body top near y 0.45.
   (b) The nemes must wrap the back of the head: LAPIS back panel (0, -0.08, 1.32), half (0.50, 0.04, 0.22), with
       2 flush GOLD stripes 0.086 tall, meeting the side flaps; the queue (line 197) sits on top of it.
3. The eyes are not half-lidded. The lid (lids=0.30, line 153) is FUR on a FUR face, so it is invisible, and highlight 1
   peeks out under it as a white notch at the top-left of each eye (512 px crop). Use lids=0.36, look=(0, -0.4),
   hl_on_pupil=True, and add a KOHL lash bar along each lid's lower edge (1.08 x outline W, 0.035 HW tall, 0.004
   prouder than the lid, outer end joining the kohl wing). This restores the V2 regal half-lidded look.
4. The nemes reads as pancakes from the side and a flat gold tray from above: 5 dome steps, 5 flap bars and 7 lappet
   bars (lines 179-196) are each bevelled and offset, so every stripe is a groove. Rebuild as striped cloth: each side
   flap = 1 LAPIS block, half (0.05, 0.30, 0.22), with 2 flush GOLD stripes; each lappet = 1 LAPIS block, half
   (0.09, 0.05, 0.31), with 3 flush GOLD stripes (front + outer faces); dome = gold brow band + lapis + a lapis cap with
   4 front-to-back GOLD stripes 0.086 wide, replacing the flat 0.60 x 0.52 gold top (> 3 x 3 cells, §1 item 7).
5. The haunches (line 102) bulge 0.09 past the body as square boxes (side/back). Centre x +-0.34 -> +-0.31, half
   (0.15, 0.24, 0.23) -> (0.13, 0.26, 0.21), rnd 0.45, so the outer face lines up with the chest (0.46) as a round hip.

KEEP:
- The front face: big copper eyes with kohl wings, the pink nose with sheen, the "w" mouth and the blush.
- The usekh collar (gold / turquoise / gold with drop gems) and the gold uraeus with its red gem.
- The sphinx pose with the huge head (about 45 % of H) and the stretched paws with gold anklets.
