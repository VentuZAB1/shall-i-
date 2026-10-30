REVISE 6.5/10 - the leopard anatomy is right: long low body, deep chest with a strong tuck (best belly line of the batch), small head,
big clawed paws, long fangs. But the front read is soft (the crystals look like big pink ears, the whisker pads are puffy cartoon cheeks), and the body is one
tone with no shadow structure.
(Phase 1 = model only. The old clips were not judged. The close-ups (08:55) are older than the last spec edit (08:56), so re-render them.)

Colour, checked against the Studio calibration: FUR (92,80,148) lands as deep indigo-violet in game, so it is NOT lavender and the body should
not be darkened. The "lilac" read in the previews comes from the pale zones and pink-white crystal tips plus a body with only one tone (items 1-3).

Must fix:
1. Crystals read as big pink ears/horns from the front: in model_front the shoulder clusters rise right behind the ears, and the light
   tips (VIOLET_L on 38 % of each shard) read pink-white. Move the clusters back and out: base (+-0.10,-0.38,0.83) -> (+-0.12,-0.31,0.81),
   direction (s*0.35,0.40,1) -> (s*0.6,0.55,0.75), so from the front they flank the neck below the ear line. Shift the accent off pink
   toward the plan violet: VIOLET (196,96,255) -> (170,80,255), VIOLET_L (236,198,255) -> (206,160,255), light-tip share 0.38 -> 0.25.
2. Soft face: the two pale whisker pads (rnd 0.45) under the nose make a cartoon cat mouth. Make them FUR, flatter
   (h.z 0.024 -> 0.016, rnd 0.2) and 0.005 further back; the long upper fangs keep showing below them. Ear inner PALE -> FUR.
3. One-tone body, so no "shadow": make FUR_D a real dark top zone. Use a topline saddle (see 4), dark ear backs (already), dark paws (already), and FUR_D
   on the last TWO tail segments. Keep PALE only on the throat/chest/belly strip.
4. Coin slot on the back: the dark back stripe (0,0.06,0.776) is buried under the rib and hips and only shows in the waist dip, where it
   reads as a dark slot/hatch in the tq and back views. Replace it with a saddle lying ON the top surfaces (+0.012): B.seg withers
   (0,-0.36,0.817) -> waist (0,0.10,0.787) -> rump (0,0.40,0.80), half-width 0.065.
5. Rosettes read as scattered specks / paw prints (8 small rings per side, r 0.030-0.040, bars 0.026). Use 5 bigger rings per side
   instead (rib 2, waist 1, hips 2): r 0.050-0.056, bar width 0.034, n=5 with gaps, GHOST (58,48,102) -> (48,40,86) so they survive at 30 studs.
6. Thick leopard tail (plan): the tail is as thin as a shin and reads like a rope. Change Tail1/Tail2 half-widths 0.052/0.046 -> 0.064/0.056 and Tail3
   0.042 -> 0.050.

Keep:
- the long low body with the deep chest, strong tuck and prominent shoulder blades (real leopard, not chibi)
- the heavy dark brows over the narrow slit eyes with vertical pupils, plus the long upper fangs
- the big dark paws with 4 black claws, and the crystal-tipped tail curl
