# PetsV3 builder guide (2026-10-08, PRO pass)

The owner: the pets look LOW QUALITY; they must look professionally made, in the style of the Roblox game
"Steal an Egg" (references: `_refs/ref_01..25`, contact sheet `_refs/_contact.png`). Art rules: `STYLE_BIBLE.md`
(read it first, it has per-pet direction). Earlier reviewer verdicts: `REVIEW_NOTES.md`.

## Hard rules (owner)
- NO GLOW on meshes: never Neon/emissive parts. Fire, auras, sparks = Roblox particle VFX added later in Studio.
- Big heads, big readable eyes: both eyes and brows visible in a straight FRONT view; each eye >= ~20% of head
  width; brows contrast with the head colour.
- Every pet keeps ONE unique signature act + its own idle and roar (already authored; keep them working).
  No head shakes. Flyers flap wings AND pump legs; wings never pass through each other or the body.
- 0 collisions in every clip (`collision_free: true` from headless_full), clean audit (linear 0, loops closed,
  slide ~0).
- Never publish anything, never touch Roblox Studio, never touch other builders' pets.

## Files
- `pets/<Name>.py` = one pet: `model(k)`, `rig(k)`, `anim(k)` (returns walk stride), `check_pairs()`, optional
  `joints()` (hinge zones), constants `DISPLAY MOTION RIG HEIGHT HEAD_XF`. YOU EDIT ONLY YOUR OWN pets' files.
- `blockkit.py` = the shared kit (coordinator-owned; do NOT edit - ask for kit features in your report).
  It implements STYLE_BIBLE section 2 automatically: rounding by role (mass / limb / detail), smooth soft masses,
  brick-grid raised plates with fake light, plates only on outer side + front of limbs, none on bottoms.
  `B = bk.Blocks(k, seed=.., tier=1..6 | "S")` (tier = plate fill; TH auto = biggest torso block's height, or th=..)
  `B.add(center, half, color, bone, rot=(deg xyz) | R=Matrix, top=(sx, sy) taper, bot=.., top_shift=..,
  bevel=None(auto)|min bevel, studs=None(auto faces)|[] none|["+x",..], density=0.5 (x fill), role=None|"mass"|
  "limb"|"detail", rnd=None (rounding override, fraction of the smallest half-size), pvar=None|"diamond"|"flush")`.
  Bones named Leg*/Shin*/Foot*/Arm*/Tail*/Ear*/Wing*/Fin*/Tent*... are limbs automatically.
  `B.seg(p0, p1, hw, hd, ...)`, `B.bar(p0, p1, normal, width, thick, ...)`, `B.spike(base, dir, length, w, ...)`,
  `B.poly(pts, thick, ...)`, `B.on_face(blk, "-y", u, v, hu, hv, thick, color)` (plate on a block face, local units),
  `B.mirror(...)` (`{s}` in bone -> L/R).
  EYES: `B.face_eyes(head_block, "lovely"|"bold"|"fierce", iris_rgb, base=head_rgb, brow=rgb|None, lids=0..0.35,
  look=(x, y), z=None (x HH up the front face), x=None (x HW), scale=1.0, sclera=False)` builds BOTH eyes (+ brows
  for bold/fierce) on the head block's front (-y) face exactly per bible 2c (outline, iris, pupil, 2 highlights
  upper-left, dark-face light rim). The head block must face -y; keep the muzzle below the eye band.
  face_eyes extras (2026-10-08): pupil_size=(w,h) / hl_size=(big,small) / brow_spec=(w,h,deg) overrides,
  brow_angles=(left_deg, right_deg) per-side brow tilt, brow=rgb now also works for 'lovely' (soft default brow),
  and the 2nd highlight is skipped automatically when it would notch the pupil. Block(pmix=(1x1,1x2,2x1)) sets a
  per-block plate size mix (e.g. bark (0,1,0)).
  Block(prelief=1.5) = chunkier plates on that block, Block(p2x2=0.3) = share of 2x2 plates on its big faces.
  hl_on_pupil=True puts the glint ON the pupil (fierce eyes otherwise read like letters).
  Clips: one-shot clips no longer get CYCLES modifiers from bake_bezier_now (partially keyed channels used to
  repeat); only looping clips cycle.
  Old helper `B.eye(center, normal, hw, hh, iris, ...)` still exists for eyes on odd surfaces (side heads...).
- HEAD_XF is LEGACY for scaling: build heads at their final size (bible proportions). It may still be used as a pure
  TRANSLATION of the head group: `HEAD_XF = [(pivot, 1.0, bones, (dx, dy, dz))]` (moves blocks + joints), e.g. to lift
  a head off the chest so nods/howls stay collision-free (Raiju: (0, -0.12, 0.18)). Rule: the head must NOT overlap the
  chest at rest - a neck block on the Neck bone bridges them.
- Rig: `k.joint(name, pos, parent, tail=..)`, legs `k.add_leg2(leg, shin, foot, knee=pole)`,
  `k.solve_leg(leg, f, T, toe=None)` (T = ground point under the ankle). Anim: `k.new_action(name, n, loop)`,
  `k.key(bone, f, rot=(pitch, yaw, roll) deg, loc=..)` in armature axes relative to the parent; pitch + tips a
  -Y bone's nose DOWN; `cm.key_axis(k, bone, f, axis, deg, ...)`; `k.finish(loop=..)`. Pets face -Y, Z up.
  Head pivots belong at the THROAT (low/back of the head) or a nod swings the skull into the chest.

## Commands (background Blender, ~10 s each; runs in parallel with other builders)
```
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
cd "C:/Users/ventu/OneDrive/Desktop/SLINGSHOT Creatures/PetsV3"
"$BL" -b --factory-startup --python _tools/headless_model.py -- <Name> tq,front,side,back 520 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback"
python sheet3.py <Name> model_ 2          # -> <Name>/renders/_model_sheet.png (Read it to look)
"$BL" -b --factory-startup --python _tools/headless_full.py -- <Name> walk:8,roar:20,act_x:30 2 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback"
python sheet3.py <Name> pose_tq 3         # pose renders of the picks
"$BL" -b --factory-startup --python _tools/headless_full.py -- <Name> - 1 export 2>&1 | grep ...   # FINAL: step-1 check + export
```
Collision locator: `"$BL" -b --factory-startup --python _tools/collide_where.py -- <Name> <clip> <frame> "BoneA|BoneB"`
prints the REST-space centroids of the colliding triangles of each side (which block to move).
`headless_full` prints JSON with `audit`, `clips`, `collisions` {clip: {"A|B": [tri_pairs, worst_frame]}},
`collision_free`. Fix collisions by changing geometry first (thinner/shorter/moved parts, throat pivot,
joints() hinge zones only for genuine hidden knuckles), anim keys second. Re-run until `collision_free: true`
at step 1. If `check_pairs()` is missing, write one (legs vs legs, head/jaw vs chest/front legs, tail vs hind
legs, wings vs wings/body for flyers).

## Workflow per pet
1. Read STYLE_BIBLE.md (+ its paragraph for your pet), REVIEW_NOTES.md, `_review/<Name>_model.png`, the refs.
2. Rework `model(k)` for a PROFESSIONAL look: bigger head, B.eye eyes, shaped torso (several blocks: chest,
   belly, hips, back line), tapered limbs with big paws/hooves, layered detail (cheek tufts, armour plates,
   horn rings...), clean colour zones (2-3 tones per zone). Keep bone names and roughly the same joint layout so
   the authored animations still work; move joints in rig(k) if you move parts.
3. Render model views, look at them critically next to the refs, iterate until it is genuinely good.
4. Report the sheet path to the coordinator for the design review (the coordinator relays the verdict).
5. After approval: full pass, 0 collisions at step 1, look at pose renders (no part inside another, wings clear),
   then the export command. Report: files, tris, collision_free, anything odd.
Triangle budget: <= 15k tris per pet (tris in the JSON).

## Calibration
`pets/Raiju.py` is the first pet rebuilt to the bible (see `_review/Raiju_verdict.md` for the reviewer's verdict):
copy its patterns (one torso of 2 overlapping blocks, face_eyes, muzzle + nose sheen + grin, socks + paws with toe
grooves, chunky inlays, tier, role overrides, rig joints moved with the geometry, throat pivot, check_pairs /
joints()).
