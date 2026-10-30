REVISE 7/10 - in the tq and front views it's the strongest silhouette in the batch (wedge head + upturned tusks + magma-tipped crest + rock-socket eyes, at or near Raiju level). From the side and back, though, the belly reads as a big orange box, and those are the views players see most.
(Phase 1 = model only. The clips in the file are the old ones and were not judged.)

Must fix:
1. Accent over budget: orange is ~18 % of the side view and ~12 % of the back view (Raiju 4-5 %, limit 10 %). The cause is the
   waist block (0,0.12,0.70): it's MAGMA with no shell over it, so its whole flank is orange, and the three shells stop high (za -0.20/-0.18/-0.11).
   Add a 4th rock shell over the waist block (full y range, down to ~0.04 above its bottom, rnd 0.42, same rock teeth) and
   lower the other shells' za by ~0.06. Orange should then show only as (a) 0.05-0.06 gaps between neighbouring shells and (b) a belly
   strip 0.04-0.06 tall under the shell edges. Target 6-9 % orange in the side view.
2. Box belly (the owner's complaint): in the side view the underline is flat from behind the front leg to the hind leg (~0.45 BL; the rule
   is <= 0.25 BL). Raise the flank: waist h.z 0.19 -> 0.15 and centre z 0.70 -> 0.74 (bottom 0.51 -> 0.59); hips h.z 0.185 -> 0.16
   and centre z 0.665 -> 0.70 (bottom 0.48 -> 0.54); tuck seg end (0,0.30,0.565) -> (0,0.28,0.62). The line must rise ~15 deg
   from the brisket to the stifle.
3. Not a wedge from behind: the back view reads as three equal rounded boxes ("train cars"), and the rump shell looks biggest. Narrow the
   hips x 0.21 -> 0.18 (~28 % under the ribcage), move the hind legs in from x 0.135 to 0.115 so the thighs stay flush (LESSONS 1),
   and sit the rump shell top ~0.03 lower than the rib shell so the top line steps down from the withers.
4. The eye is hidden in the side view: the tusk's tip spike ends at (+-0.205, -0.99, 0.80), right over the eye (y -0.99, z 0.775).
   Shorten it 0.11 -> 0.07 and aim it (s*0.05, 0.45, 0.9) so the tip stops ~0.05 in front of the eye. Check that close_side
   shows the whole orange slit.
5. Reads as a cartoon pig snout: the two square black nostrils (0.034 x 0.052 each) take up most of the disc. Make them 0.020 x 0.030,
   rotated +-20 deg with the outer end up, set 0.004 into the disc. Keep the SNOUT colour (per the Studio calibration it renders as a deep rose-brown in game).

Keep:
- the wedge head + ivory tusks + narrow orange eyes under the light ROCK_T brows (fierce, not goofy)
- the two-tone crest laid back along the Mane (the best crest so far) and the zig-zag cracks on the shoulder/ham armour
- the slim dark lower legs on black cloven hooves with dewclaws (real boar legs)
