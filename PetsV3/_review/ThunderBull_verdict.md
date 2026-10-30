REVISE - 7/10 vs the references (round 1).
It reads as a storm bull at 64 px and the front view is strong. Four things keep it below the Raiju bar: clipped eyes, a body that is all one slate, a crate head, and a weak side/back read.

MUST-FIX (most important first):
1. The eyes are clipped and read as windows.
   - The muzzle top (z 0.99) hides the bottom of both eye outlines (outline bottom z 0.95).
   - lids=0.30 cover the top of the iris, so the pupil fills about 70 % of the visible iris.
   - Only the right eye gets the 2nd glint.
   Fix: muzzle centre z 0.84 -> 0.81, half z 0.15 -> 0.13 (top 0.94); move the nostrils, ring, mouth and jaw down 0.03.
   Then call face_eyes(..., z=0.60, lids=0.22, pupil_size=(0.085, 0.09), hl_on_pupil=True, hl_size=(0.05, 0.0)) for one glint ON each pupil.
2. There is no belly zone where players look. The LIGHT belly slab (z 0.495) is on the underside and the brisket (y -0.703) is hidden behind the head.
   So the side and back views are about 85 % slate (bible 1.6 wants 15-25 % light).
   Add a flush LIGHT belly band on both flanks of the chest (z 0.52-0.70) and the hips (z 0.58-0.72), running between the legs.
   Follow the bot taper (lesson 2: x = h.x*(bot + (1-bot)*t) + 0.006) and give the top edge 2 steps.
   The side view must show a light underline from the front legs to the hind legs.
3. Crate head: the brief asks for ONE heavy 20 deg brow RIDGE across the forehead. Today it is 2 separate bars on a flat box face.
   Fix: brow_spec=(0.40, 0.09, 20), plus a DARK keystone block joining the inner brow ends (x 0, z about 1.20, half 0.07 x 0.045, as proud as the brows).
   Together they form one continuous V that shades the eyes.
4. The horns read as 2 upright antennae in the side and back views, because h2 -> h3 climbs almost straight up.
   Hook the tips forward like a charging bull: h2 = (+-0.82, -1.24, 1.56), h3 = (+-0.84, -1.46, 1.74). Keep the 2.2 HW span.
   Re-check Head vs Leg_F* in act_charge.
5. Socks: the LIGHT fetlock band (z 0.115-0.225) is 12 % of the leg; bible 1.9 asks for 22-28 %.
   Grow it to z 0.12-0.33 (centre 0.225, half z 0.105), still flush at 1.02 x shin.
6. Tail: the slate rope hangs flat against the slate back face of the hips (y 0.76-0.89), so from behind only the tuft shows.
   Swing it out: Tail1 end (0, 0.98, 0.84), Tail2 end (0, 1.04, 0.60), at least 0.08 clear of the hips.
   Root half width 0.08 -> 0.10, and make the rope DARK so it reads against the slate.

KEEP: the front-view horn span with the 2-tone cloud on the hump (great 64 px read); the light muzzle with dark nostrils and the gold nose ring;
the split dark hooves; the flush shoulder bolts.
