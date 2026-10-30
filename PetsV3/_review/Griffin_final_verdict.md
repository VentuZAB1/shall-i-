APPROVE 8/10 - at the Raiju bar. It is a dark golden-eagle griffin: a hooked yellow beak with a dark tip, a dark brow V over yellow slits,
gold ear tufts and crown, scaly yellow shanks with black talons and lion hindquarters. The huge 3-row wings are the signature from any
distance. (Final gate, phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Gold face mask: FIXED. The BROW (84,56,40) ridges meet in a V over the beak root. The cere is a low band (half z 0.036 at -0.015) and the
   nostrils are small. The yellow eyes now pop between the dark brow and the gold crown, and the face reads fierce instead of toy-like.
2. Smooth wings: FIXED. feather() and the arm/hand blocks are role="limb", so the wings carry studs.
3. Golden nape board: FIXED. The plank now starts at (0,-0.58,1.19), and below it a 3 + 2 + 1 staggered NAPE shingle cape points down to the withers.
   model_back reads as a feathered hackle.

Builder deviation accepted: the rest wings are a raised heraldic V (FOLD 40,-4,0,100, primaries swept back) instead of a flank fold.
It looks like a segreant griffin, keeps the biggest shape in the silhouette while it follows the player, and avoids the fold collisions.

Animation (tq key beats):
- idle RAPTOR WATCH: snappy head-locked turns (6 f turn, ~20 f holds), cocks its head 36-38 deg to look up with one eye, a beak clack at 84-92,
  then re-tucks the wings (wrists +6) and flicks the tail tuft. A real raptor read, and unique.
- roar SKY SCREECH: chest up, the wings unfold into a tall V with the primaries spread, and the beak gapes forward. Clear.
- act_mantle: locks on (12), the right talon strikes 0.26 ahead (18), the wings spread wide and low with the head low between them (32-44),
  two tearing pulls with heaving wings, then the head snaps up with the beak open (72-78), folds and steps back. Behaviour-based and unique.
- fly / takeoff / land: flap-flap-glide with the talons tucked and the lion legs trailing. Launch and flare beats are present.

Optional polish (not blocking):
1. The mantle spreads the wings to the sides and back (TENT fwd 24) rather than "arched forward like a tent over the prey". Raise fwd
   24 -> 38 so the tips come down in front of the talon, if the wing/head pairs stay collision-free.
2. The rest pose is already a V, so the roar's V is only 4 deg taller (40 -> 44). Raise the roar up to ~56 so the screech clearly towers over the idle.
