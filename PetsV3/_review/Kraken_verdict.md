REVISE - 5.5/10 vs the references (round 1).
The tentacle ring is good. But the mantle reads as a pink cube or bin in every view, the eyes read as letters, the pet is about 90 % one crimson, and tentacles sink into the ground in the clips.

MUST-FIX (most important first):
1. Mantle shape: top=(0.78, 0.78) makes the top narrower than the bottom (a bin), and flat walls with rnd 0.28 give a cube in the back and pose views.
   Give it an octopus bulb: bot=(0.82, 0.82), top=(0.92, 0.92), top_shift (0, 0.05) -> (0, 0.14), rnd 0.28 -> 0.42.
   Target: in the front view, widest at 70-80 % of the height under a domed top; in the side view, a curve rising behind the eyes that leans back at least 12 deg.
   Re-fit the face proxy to the new lean and taper, and keep the eye outlines at least 0.03 inside the flat area (scale 1.12 -> 1.0 if needed).
2. Fins: they read as devil horns or cat ears from the front and as sticks from the side.
   They are 0.08-thick bars whose broad face points UP (side=(-s*0.5, 1, 0)).
   Rebuild them as flat blades in the plane the side view sees (lesson 6):
   - side=(0, 0, 1), root (+-0.46, 0.10, 1.05) -> tip (+-0.58, 0.66, 1.30);
   - half width 0.18, thickness 0.10, top=(0.25, 1.0), so each sweeps back to a point;
   - dark rim on the trailing edge only.
   In the front view the fins must not rise above the mantle top.
3. Eyes: the horizontal bar pupil, with highlight 1 overlapping its top-left end, reads as letter shapes at 64-512 px, and the look is bored.
   Fix: pupil_size=(0.12, 0.09), hl_on_pupil=True, hl_size=(0.05, 0.0). That gives a chunky rectangular pupil with the glint on it.
4. Colour zones: about 90 % crimson. The UNDER skirt (z 0.30-0.44) is hidden, the tentacle strip shows only as an edge line, and the 6 dark spots read as windows.
   a) Add a flush UNDER lip band around the lower front and sides of the mantle (z 0.36-0.56, following the taper per lesson 2), carrying the beak. That is the muzzle zone, 15-20 %.
   b) Regroup the spots into 3 clusters (one 2x2 + two 1x1 touching at the corners) on the top-back and both upper flanks, where players see them.
   c) Mantle density 0.80 -> 0.62, so the flank plates stop forming a 3x3 keypad block.
5. Ground clipping: tentacle mid-segments go under the ground in idle_30, idle_70, act_crush_40, act_crush_74 and swim_24.
   You can see pink tip chips floating on the ground in _pose_tq_sheet. The idle swings b down to +15 deg and c to +24 deg while the Spine bobs -0.05.
   Keep every tentacle vertex at z >= 0.02 in every frame: e.g. idle b = 2 + 7*sin, c = 6 + 12*sin, Spine bob z = 0.03 + 0.03*wave.
   In crush, stop the SLAM at the ground. Add a per-frame min-z check for the T* meshes to the gate.

KEEP: the 8 tapered 4-segment tentacles with light undersides, sucker rows and curled tips (great 64 px read);
the bold amber eyes under the 15 deg dark brow; the hooked beak and the barnacle cluster.
