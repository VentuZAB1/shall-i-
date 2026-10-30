APPROVE 8.5/10 - above the Raiju for silhouette. The crested skull, splayed horns, membrane wings with red-sprite zigzags, jagged dorsal
ridge and blade tail read instantly. The triple wing clap is the most spectacular signature of this batch and is easy to read. (Final gate,
phase 2: model + all clips.)

Earlier must-fixes (fierce_verdict), all addressed:
1. Slim torso vs wings: FIXED. There are flight-muscle masses at the wing roots and the chest is 0.25, so the wing arms now grow out of
   shoulders.
2. Box chest: FIXED. The keel narrows to a point (top 0.40) and the bands go 0.115/0.085/0.06: a V from the front.
3. Rivet spines: FIXED. The spines are 0.17-0.21 long x 0.075, and the tail spines 0.15/0.12/0.09, making one jagged ridge from crest to blade in model_back.
4. Candle crown: FIXED. The horns splay out (0.65,0.75,0.25) at 0.19 long, and the crest stays the single centre blade.
5. Floating zigzags: FIXED (lift 0.019).

Animation (my own renders of the exported blend from front/back/side/tq). ground_min >= 0.000 except -0.012 in act_thunderclap f54 (the
talon tips on tiptoe), -0.005 in idle and -0.002 in walk, which is negligible.
- idle GARGOYLE PERCH: crouched with the wings folded high like a cloak. Tail whip-crack at f40, 2 jaw clacks at 70-78, a head turn at 98-104.
- roar HOOD SHRIEK: the wings arch up and forward into a canopy over the low head, the jaw opens 36 with a chatter, and the tail lashes. It is
  a different shape from Griffin's tent and Cvetibara's wrap.
- act_thunderclap: crouches with the tail braced (f10) and sweeps the wings up (f20). CLAP 1 at f24 with a head thrust and jaw snap, open
  (f32), CLAP 2 (f38), open (f46). CLAP 3 at f52-56 up on its toes with the tail lifted. Wings held high with the jaw wide (f62-70), then it
  folds (f80-90). From the front the wings meet as two vertical blades above the back with a hairline gap and never cross. With the
  shoulders moved out, the raised wing arms clear the neck and the horns.
- fly: deep downstrokes with the legs pulled back and the tail as a rudder; takeoff and land are fine.

Optional polish (not blocking):
1. The third clap is meant to be the biggest. Make the on-toe rise 0.05 -> 0.08 and Spine pitch 10 -> 14 at f52-56 so it outranks claps 1-2.
2. Place the coordinator's spark VFX at f24/38/52 where the wing tips meet above the back, not on the body.
