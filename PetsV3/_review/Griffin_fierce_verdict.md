REVISE 7/10 - at 64 px it reads instantly as a griffin: eagle front, lion rear, huge 3-row wings, yellow shanks. The proportions are real and
the lion's belly line rises. But the face is a gold mask. Golden brows, a golden crown and a tall yellow cere surround yellow eyes, so there is no dark
brow shadow and the head reads toy-like instead of fierce. (Phase 1 = model only. The wings were judged spread; the folded rest pose comes from the clips. Colours are fine per the
Studio calibration.)

Must fix:
1. Fierce eagle face (close_front, close_tq): the eyes vanish yellow-on-gold.
   - Brow ridges: NAPE -> a new BROW (84,56,40) (lands as near-black brown in game). Half (0.075,0.045,0.028) -> (0.085,0.045,0.03), x 0.088 -> 0.080,
     so the inner ends meet in a V over the beak root (the Raiju keystone).
   - Cere: half z 0.06 -> 0.036, centre z +0.005 -> -0.015. It becomes a band at the beak root and the brown forehead shows between the eyes.
     Today the yellow block rises to brow level, which reads as a mask.
   - Nostrils (0.004,0.016,0.009) -> (0.004,0.010,0.007), at z -0.005. In close_tq the current slash reads as a second eye.
   - Keep the golden crown and ear tufts: the dark brow then sits between two gold zones and the yellow slits pop.
2. The wings will lose their studs: feather() hard-codes role="detail", so with the new StudMask every wing feather renders smooth, and the wings are the
   largest surfaces on the pet. Use role="limb" in feather() (bevel 0.008 unchanged), as the arm and knuckle already do.
3. Golden nape board in model_back (the view players see most): the NAPE seg (0,-0.44,1.00) -> (0,-0.66,1.30), 0.13 x 0.07, is a smooth bright
   plank running from the shoulders to the crown. Start it at (0,-0.58,1.19). Replace the lower part with 2 staggered rows (3 + 2) of overlapping NAPE
   shingle feathers (the chest-ruff recipe, ~0.06 x 0.02 x 0.09, tips pointing down the neck toward the withers, lower edges proud), so the gold reads as
   a feathered hackle cape.

Keep:
- the hooked beak (yellow bill, dark hooked tip, red gape line) and the swept golden ear tufts + neck-ruff spikes
- the eagle forelegs (brown trousers + fringe, scaly yellow shanks, 4 black talons) set against the lion hind legs and tufted tail
- the 3-row feather wings with clear value steps from coverts to secondaries to primaries
