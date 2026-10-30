# FIERCE builder guide (2026-10-09) - replaces BUILDER_GUIDE.md / STYLE_BIBLE.md chibi rules

The owner rejected the chibi pets ("too CHILDISH... for babies") and APPROVED the new storm-wolf Raiju:
"The design is fire!". Calibration pet = `pets/Raiju.py` (read it fully, copy its patterns) and its renders
`Raiju/renders/_RAIJU_FIERCE_preview.png`, `_model_sheet.png`, `_pose_tq_sheet.png`. Owner references:
`_refs/fierce/f_54..f_71` (Steal-a-Brainrot-style pets: Spideron, Lunar/Ice dragons, Cerberus T-rex, Bronto, Orca,
King Mammoth, Royal Sphinx, Mantis). Per-pet direction (research, design, idle, roar, SIGNATURE act):
`FIERCE_PLAN.md` - follow it; if something in it is not feasible, pick the closest feasible variant and say so.

## The look (hard rules)
- REAL animal / creature anatomy and proportions: normal-size heads (no big chibi heads), long jointed legs, snouts,
  necks, tucked waists, real silhouettes. Built from tapered, beveled blocks (blockkit) - Roblox-like, not photoreal.
- The whole surface is covered in small Roblox studs: `B = bk.Blocks(k, seed=.., tier=.., plates=False)` and, as the
  LAST line of model() after `B.build()`: `bk.stud_skin(k, PITCH)` with PITCH ~= 0.08 x torso height (Raiju: TH 0.52,
  PITCH 0.042). No raised plates (plates=False).
  StudMask (kit, 2026-10-09 08:40): blocks with role "detail" (eyes, teeth, claws, spikes, thin inlays) stay SMOOTH
  automatically; pass `nostud=True` to B.add/B.seg/... to keep any other block smooth (e.g. gold trim, horns).
- No box bellies (owner: "make the stomach look less like a BOX"): taper every torso underside (bot=(0.66, 0.56) on
  a ribcage block), a sloped "tuck" segment from chest to waist (B.seg), narrower waist, rounder masses (rnd=0.30
  on torso blocks), pale underside strips that follow the slope. Look at the side view: the belly line must rise
  from the chest to the hind legs, never a straight flat bottom.
- Fierce faces: narrow slanted eye slits (black socket + bright iris + small hot centre, tilted ~18 deg, inner end
  low) under a heavy brow block that overhangs slightly; fangs/teeth (B.spike), dark nose, cheek ruffs or scales.
  NEVER big round cartoon eyes, highlights-on-pupils, blush, smiles. (`B.face_eyes` is the old chibi helper - don't
  use it.)
- Claws on every paw (4 black B.spike claws), horns/spikes/hackles where the creature has them.
- Colour: dark rich body + lighter underside + ONE bright accent (markings as flat B.bar stripes / flush inlays).
  ROBLOX DARKENS COLOURS: in-game the pet looks ~0.6x as bright as the Blender preview and shadow sides go near
  black. So pick body colours BRIGHTER than the look you want: main body colour value >= ~170 in its brightest
  channel or luminance >= ~95 (Raiju FUR = (80, 102, 182) reads dark storm navy in game). Near-black only for
  claws, nose, eye sockets, small details.
- NO glow, no Neon (fire / sparks / auras = Studio particle VFX, done by the coordinator).
- Sizes: in game a pet scales from x0.8 (1 KG) to x2.2 (10M KG), max ~18 studs tall next to a 5-stud player. It
  must look great small AND huge: strong silhouette, accents big enough to read at 64 px, no noisy specks
  (no detail < ~0.02 Blender units), studs everywhere for close-ups.
- Triangle budget <= 15k (Raiju ~4.1k). One Body mesh (blockkit merges parts at export).

## Animation (owner, VERY IMPORTANT)
- Every pet has its OWN idle, walk/fly/swim, roar and ONE SIGNATURE act (`act_<word>`) from FIERCE_PLAN.md,
  behaviour-based (owner examples: deer scratches its tummy with its head; Mossback sleeps and hides inside its
  shell). No two pets share a motif. No head shakes. Acts play in place and end exactly in the rest pose.
- Flyers: flap wings AND pump legs, wings never pass through each other or the body; keep the existing
  fly / takeoff (event "launch") / land (event "touch") clip set of your spec (see the old spec + `../PetsV2/pets/
  _common.py` Flight, `wing3.py`).
- Quadrupeds: 2-bone legs + Foot like Raiju (`k.add_leg2(leg, shin, foot, knee=pole)`, front pole (0,1,0), back
  pole (0,-1,0)); walk = `cm.quad_walk`; idles/acts keep paws planted with `cm.plant(k, n)` or `k.solve_leg`.
- 0 collisions at step 1 (`collision_free: true`), `ground_min_z` >= -0.02 in every clip, audit linear 0, loops
  closed, walk slide ~0. Head pivots at the THROAT (low/back of the head).
- Keep clip names: idle, walk (or fly/swim + takeoff/land for flyers as in the old spec), roar, act_<word>.

## Files and rules
- You edit ONLY your own `pets/<Name>.py` and `<Name>/` folder. Do NOT edit blockkit.py, run3.py, petkit.py,
  other pets, Studio, or anything else - ask the coordinator for kit features in your report.
- Back up the chibi spec first: `cp pets/<Name>.py _tools/chibi_specs/<Name>.py` (mkdir -p).
- Kit API: see BUILDER_GUIDE.md "Files" (B.add / B.seg / B.spike / B.bar / B.on_face / B.mirror / B.poly,
  role/rnd/top/bot tapers) + the new `plates=False` and `bk.stud_skin(k, PITCH)`.

## Commands (background Blender, ~5-15 s each, parallel-safe)
```
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
cd "C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
"$BL" -b --factory-startup --python _tools/headless_model.py -- <Name> tq,front,side,back 600 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback"
python sheet3.py <Name> model_ 2                       # -> <Name>/renders/_model_sheet.png (Read it and LOOK)
"$BL" -b --factory-startup --python _tools/headless_closeup.py -- <Name> x,y,z dist 700   # close_tq/side/front.png aimed at a point (face!)
python sheet3.py <Name> close_ 3
"$BL" -b --factory-startup --python _tools/headless_full.py -- <Name> idle:40,roar:30,act_x:30 2 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback"
python sheet3.py <Name> pose_tq 3                      # delete stale pose_tq_* files of old clips first
"$BL" -b --factory-startup --python _tools/headless_full.py -- <Name> - 1 export 2>&1 | grep ...   # FINAL (step 1 + export to C:\cdimp)
```
Collision locator: `_tools/collide_where.py -- <Name> <clip> <frame> "BoneA|BoneB"`.

## Workflow per pet
1. Read FIERCE_PLAN.md (global + your pet), pets/Raiju.py, your old spec (bone names, clips, rig type), the refs.
2. Rebuild model(k) + rig(k) in the fierce style. Render sheet + face close-ups; critique them honestly against the
   Raiju and the refs (silhouette at 64 px, side view belly line, face, back view) and iterate until it's genuinely
   good. Then report the sheet paths to the coordinator for the reviewer gate (wait for the verdict, fix).
3. Author the clips from FIERCE_PLAN.md (unique idle / roar / signature + locomotion). Pose renders of the key
   beats of EVERY clip, look at them, fix. 0 collisions at step 1, then export.
4. Report: files, tris, collision_free, clip list with lengths, the signature in one line, anything odd.
