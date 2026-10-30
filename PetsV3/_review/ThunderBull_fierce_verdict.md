REVISE 6.5/10 - the tq hero view already reads as a real storm bison at 64 px (hump, low horned head, chunky blue Lichtenberg branches, slit eyes under
heavy brows) and is close to Raiju level. The side and back views are what players see most, though. There the head hangs straight down (grazing),
dark shards dangle under the head, and the front view is a cartoon cow muzzle.
(Phase 1 = model only. The clips were not judged.)

Must fix:
1. Grazing head (your flag, confirmed). HEAD_P -22 puts the head's long axis ~68 deg below horizontal, so in model_side the face is a vertical
   box, the eye is a speck on its front edge and the muzzle points at the ground. The plan line (forehead 0.62 SH, nose 0.35 SH, head 0.42 SH) is ~45 deg.
   Set HEAD_P -22 -> -42 and HEAD_O (0,-0.86,0.62) -> (0,-0.92,0.63). The -0.06 y keeps the woolly crown's back corner (now y ~-0.60) clear of the cape
   front at y -0.59; Head-Chest is a check pair, so verify it at rest. Expected: jaw bottom ~0.40 (0.37 SH), muzzle front ~y -1.21, and the eye plus the
   whole muzzle profile visible in close_side. The horns are world offsets from hp() and keep their shape.
2. Cow face from the front: the flat pale square with two big black slots (0.038 x 0.06 each) is the MoltenBoar pig-nose trap. Replace the 2 nostril
   blocks with one NOSE pad: hadd (0,-0.166,-0.125), half (0.085,0.008,0.042), bot=(0.8,1), flush. Add 2 small BLACK slits on its outer ends,
   half (0.012,0.004,0.02) at x +-0.055, rolled +-25 deg with the outer end up. Taper the muzzle's lower end bot=(0.84,0.82) -> (0.74,0.80) so it is not a square.
3. Loose shards in model_side. The beard is a 0.14-wide plank hanging 0.17 below the jaw. The 3 brisket spikes per side float in front of the forelegs
   (the y -0.52 root sits just outside the cape front). Beard: drop (0,0.03,-0.17) -> (0,0.04,-0.09), half width 0.07 -> 0.09, top=(0.5,0.6), rooted on
   the throat so it continues the neck line; delete the 2 side locks. Fringe: 2 per side at y -0.42/-0.30, x +-0.07 -> +-0.10, z 0.50 -> 0.47 (on the
   cape bottom), length 0.08, width 0.065, laid back (dy -> 0.8). It should read as the cape's shaggy hem.
4. Box-on-box back. In model_side the hump is a separate cap with a step down to the mane. In model_back the dark mane slab (top 0.48 wide)
   stands proud of the lighter waist like a seat or plank. Hump: half y 0.22 -> 0.28, centre y -0.31 -> -0.26 (peak stays over the shoulders, longer rear
   slope). Mane: top=(0.48,0.92) -> (0.80,0.92), centre z 0.865 -> 0.85, and end it at mid-ribcage as the plan says (half y 0.27 -> 0.20, centre y 0.09 -> 0.02)
   so it blends into one falling top line.
5. Pencil horns: studs=[] does not stop stud_skin (only role "detail" or nostud=True does), so the ivory horns are studded and read as Lego pencils
   with a black lead. Add nostud=True to the 2 horn segs and both horn spikes so they are smooth ivory.

Keep:
- the tq silhouette: hump peak over the shoulders, the rump stepping down to ~0.79 of it, lean hindquarters, short legs on split hooves with dew claws
- the Lichtenberg scars: trunk ~0.05 + 3 branches on the hump, cape and waist. Chunky, pointed, and the accent stays well under 10 %
- the face recipe: slanted blue slits in black sockets under the heavy CAPE_D brows, plus the sawtooth cape edge on the flank
