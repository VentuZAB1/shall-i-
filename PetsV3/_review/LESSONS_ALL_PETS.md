LESSONS FOR ALL PETS (from Raiju rounds 1-3; builders, apply these before your first render):
1. Body: never 2 touching blocks within +-10 % of each other's size. If the rig needs chest + hips, make the chest >= 15-20 % bigger in W and H (a deliberate step) with >= 40 % overlap.
   Move the hind legs in so their outer face is flush with the narrower hips. No haunch bulges.
2. Inlays (bolts, stripes, patches) on TAPERED blocks: compute the surface at each height, e.g. x = h.x*(bot + (1-bot)*t) (+0.006), and tilt the bar normal to match.
   on_face() assumes an untapered block, and that is why the round-1 bolt and bib floated. Keep every inlay inside the flat area (inside the bevel, about 0.22*h_min).
3. Plates: density=0.62 on every mass and leg block (fill about 0.80) brought Raiju close to the refs. Plates take the zone's own tone only (coloured plates = the "messy" CD look).
   Plates are rejected within about one cell of any inlay AND where a limb top pokes out of a tapered flank. Put emblems on faces >= 5x4 cells, or expect that face to go bare.
   Count the plates per big face after the build (target >= 4) instead of trusting the density number.
4. Heads: build them at their final size. HEAD_XF is for pure translation only (scale 1.0), and it moves ONLY the listed bones.
   Move the neck block and any Neck-bone tufts or manes yourself (do not add "Neck" to HEAD_XF: its joint moves too).
   Neck block >= 0.9 HW wide, top meeting the head's back face at mid-height, bottom buried in the chest. Check the back view: a dark slot = a gap.
5. Fur, ruffs, manes: no raised rectangular patches on a face (= palm). White face zones are flush inlays (<= 0.01 proud).
   Tufts grow from the BACK or edge of a part and extend the silhouette (ref_08). Fan them >= 45 deg apart, vary lengths +-20 %, thickness >= 0.6x width. 3 parallel blades = fingers.
   Head-mounted tufts swing with the head: test the idle yaw (Raiju needed its lowest blade at dz >= -0.22 to clear the chest at 26 deg).
   Dorsal crests: wide tufts laid back 60-75 deg, on a continuous surface. In a gap they read as saw teeth.
6. Signature shapes (bolt, flame, leaf, fin tails): FLAT broad prisms in the plane the side view sees (width >= 0.25 TW, thickness about 0.12 TW), always ending in a point.
   Check the front view so a raised tip does not read as a horn between the ears.
7. Eyes (face_eyes): pupil height <= 70 % of iris height, never equal (that gives a split-window look). Fierce: pupil_size=(0.09,0.095), hl_size=(0.07,0.0), look=(0,0.6).
   Lovely/bold: 2 highlights only if the pupil is big enough to hold them. Inspect a 512 px face crop: no notch cut into a pupil, no "letters".
8. Feet: socks are a flush colour band (sock half = leg half x leg bot taper x 1.02); paw 1.12x leg. Toes = 3 light claw nubs; dark grooves on a dark paw are invisible.
9. Gate every pet in 4 views + a 512 px face crop + 64 px. Most Raiju defects showed only from the BACK (seam, trench, floating bolt) or close up (eye glyphs), not in the hero tq view.
   Pets follow the player, so the back and side are what players see most.
10. Kit changes (e.g. the 2026-10-08 quaternion sign fix) affect every pet: re-bake and re-run collision_free on all clips after a kit update before you export.
