REVISE 6.5/10 - it is a real horse now. The long narrow head, the arched two-part neck, the long legs on dark hooves and the magenta-tipped
flame crest all read at 64 px. But the side and back views (what players see most) show train-car torso blocks, a jaw that reads as a
bridle strap, and spiky pink "bracelets" at the fetlocks. (Phase 1 = model only; the clips were not judged. Colours were checked against the
Studio calibration: COAT (80,66,170) lands as deep indigo-violet, close to black, so do NOT darken it.)

Must fix:
1. Train-car torso (LESSONS 1 + plan B): the barrel (0.16,0.22,0.155) is within 5 % of the croup (0.168,0.21,0.175). So the side and back views show
   two equal boxes with a seam between them, and the croup ends in a square rear wall with the tail standing up above it. Turn the barrel into a waist: half
   (0.142,0.20,0.135), centre z 0.822 -> 0.84 (= 0.75 x the ribcage; the croup becomes a deliberate 18 % step). Croup rot (-8,0,0) -> (-15,0,0) and
   top=(0.80,0.86) -> (0.80,0.72): the top then slopes ~15 deg from the hip point (z ~1.04) down to the tail, with the buttock point behind it.
   Move the tail root onto the slope: TAILP[0] (0,0.56,0.95) -> (0,0.60,0.90), TAILP[1] (0,0.72,1.00) -> (0,0.76,0.92).
2. The jaw reads as a separate stick / bridle strap (close_side, model_side). It is a pale bar with a free back end under the jowl, a dark mouth line runs
   the whole face, and the fang tips poke out below the chin. Run the jaw back into the jowl (start hp((0,-0.18,-0.17)) -> hp((0,-0.08,-0.16)))
   and move the Jaw joint to hp((0,-0.08,-0.15)). Set hd 0.027 -> 0.035 and colour it COAT, with a UNDER chin block only on its front 0.12. Mouth line: half y 0.15 -> 0.07,
   centre y -0.33 -> -0.43 (a horse's mouth corner sits a third of the way back). Upper fangs: x +-0.066 -> +-0.076 so they sit outside the 0.07 jaw and
   show as bared fangs instead of being buried in it; length 0.075 -> 0.06.
3. The feathering reads as spiky pink crowns: 4 spikes per fetlock stick out sideways ~30 deg below horizontal. Friesian feathering is hair FALLING over
   the hoof. Use 3 flat blades per leg (flame() style, width ~0.06, 0.02 thick) rooted at the fetlock: dirs (s*0.35,-0.35,-1), (s*0.6,0.1,-1),
   (s*0.2,0.5,-1), length 0.11, MANE_D with ACCENT on the outer 35 %. The tips end beside the top of the hoof (z >= 0.06).
4. From the side, horn segment 2 runs flat backwards (h2 = h1 + (s*0.035,0.095,0.02)), so the horns and dark brows merge into one black visor across the
   poll. Raise it: h2 = h1 + (s*0.045,0.075,0.06), tip spike dir (s*0.15,1,0.55). The tips must stand above the poll line and stay >= 0.02 clear of the ears.
5. Side neck locks: the 3 locks per side are parallel flat flaps (LESSONS 5: "3 parallel blades = fingers"), and in model_back they stick out like shingles.
   Fan them 15-20 deg apart: the front lock steepest, the rear lock most swept back. Never sweep one further forward than today's ~34 deg, or the front lock hits the jowl. Lengths 0.22 / 0.30 / 0.26.

Keep:
- the long narrow, nose-down horse head: pale muzzle, flared nostril slits, narrow magenta eyes under dark brows
- the standing flame-blade crest with magenta tips (the strongest silhouette element; reads at 64 px) and the flame tail down to the hocks
- the long legs with thin dark cannons, knee/hock knobs and big black hooves
