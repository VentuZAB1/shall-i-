# Glacier update: PET BUILDER BRIEF (binding for every builder agent), 2026-10-27

You are an Opus builder. You build your assigned pets in Blender with the PetsV3 kit, headless, until each one passes an independent Haiku reviewer. The lead (Claude, the coordinator) relays the reviewer verdicts to you with SendMessage. The owner judges the final look.

## The owner's words
- "let's make our new pets & new area and the new eggs"
- "you can run haiku reviewers and opus 5.5 builders"
- Names are two words.
- About the concept details: "do it as you wish".
- Taste and polish bar:
  - The polish bar is the front-page Roblox pet games (Steal a Brainrot, Steal an Egg, Pet Simulator 99).
  - Past rejections: "too childish, for babies", "grey plastic toy", "looks AI generated", "low poly".
  - The owner LOVED the FIERCE storm-wolf Raiju: "The design is fire!".

## Read first (in this order)
- **Vault rules:**
  - `V:\Obsidian\Roblox\00 START HERE.md`
  - `V:\Obsidian\Roblox\01 Rules\*.md`
  - `V:\Obsidian\Roblox\06 Modelling and Art\Creature Style.md`, `Pet Build Pipeline.md`, `Model Review Checklist.md`, `Creature Animation.md`, `Animation References.md`, `Blender Modelling Lessons.md`
- **Kit guides** (in `PetsV3`): `FIERCE_GUIDE.md` (the look + commands + workflow) and `BUILDER_GUIDE.md` (the kit API: B.add / B.seg / B.spike / B.bar / B.poly / B.on_face / Tube...).
- **Your pets' approved plans:** `_review/<Name>_plan.md` (v2) and `_review/GLACIER_PLAN_REVIEW.md` (your pet's section + the rulings).
- **The owner decisions:** `_review/GLACIER_CONCEPTS.md`, section "OWNER DECISIONS (2026-10-27, binding)".
  - Permafrost Titan = option A, the GOLD CHEST BEZEL.
  - Eclipse Seraph has 6 wings; it falls back to 4 only if the step-1 gate fails.
- **The closest existing pet file named in your plan** (e.g. `pets/ShadePanther.py` for cats, `pets/Raiju.py` = the calibration quad, `pets/AbyssWeaver.py` for multi-leg, `pets/InfernoPhoenix.py` / `pets/Thunderbird.py` for wing-bipeds, `pets/BlackDragon.py` for serpents, `pets/CelestialDragon.py` / `pets/Griffin.py` for wing-quads, `pets/ThunderRex.py` / `pets/LavaGolem.py` for bipeds).
  - Copy patterns from it (helpers like side_pt / rosette / hp() head scaling, walk/plant/solve_leg usage).
- **Memory notes with hard-won lessons:** `C:\Users\ventu\.claude\projects\C--Users-ventu\memory\roblox-new-pets-1014.md` (collision fixes, eye rules, pose limits, tools such as pose_try / fold_search / mantis_fk / headless_clips / headless_pack).

## Hard rules
- **Files you may touch:** only `pets/<YourPet>.py` and the `<YourPet>/` folder for your own pets (scratch scripts go in `<YourPet>/_scratch/`).
  - NEVER edit blockkit.py, petkit.py, run3.py, curveloft.py, other pets, or `_tools/*`. If you need a kit feature, write a helper inside your own pet file or ask the lead in your report.
  - Never touch Roblox Studio. Never publish anything.
- **The look:**
  - real anatomy; tapered bevelled blocks under a full stud skin (`bk.stud_skin(k, PITCH)` LAST in model(), PITCH ~0.08 x torso height);
  - no box bellies (the belly line rises from chest to hind legs);
  - fierce narrow slit eyes under heavy brows: NEVER round/googly eyes, no glints on pupils, no smiles;
  - dark rich body + pale underside + ONE bright accent (unless your plan has an accepted exception);
  - Roblox darkens colours ~0.6x, so body colours need a brightest channel >= ~170;
  - NO glow / Neon (auras = particles, done later by the lead);
  - readable at 64 px;
  - <= 15k tris (most pets 4-12k).
- **Rare tiers** (secret / ultra-rare / mythic) must OUTCLASS everything below them:
  - a gold hero piece readable at 64 px, strong 3-band colour blocking, one big signature feature, crystal/gold vs studded hide contrast;
  - never copy a sibling's accent or act.
- **Animation:**
  - Own idle, walk (or fly/swim + takeoff/land for flyers), roar, and ONE signature act per pet (from the plan).
  - Acts play in place and end exactly in the rest pose. No props the pet doesn't own.
  - No head shakes. No airborne spins/flips.
  - Pose limits: neck <= 8 deg, chest vs spine <= 5 deg, head+neck pitch-up <= 30 deg.
  - Never swing a limb > ~60 deg between two adjacent frames (add an in-between key).
  - 0 collisions at step 1 (`collision_free: true`), `ground_min_z >= -0.02`, audit linear 0, loops closed, walk slide ~0.
  - Head pivot at the THROAT.
  - Events (for VFX) named after the effect; repeated events numbered (lick1, lick2). Never name an event `end`.
- **Animation references (OWNER RULE):** before keying ANY clip, look at 1-3 real reference clips and write the key poses/timings you take from them into `<YourPet>/ANIM_REFS.md`.
  - First choice: animationreference.org. It has free tag pages, 25 clip opens a day; Sakugabooru is its source.
  - Use whatever web tools you have (WebFetch / WebSearch / a browser).
  - Also reuse `_review/ANIM_REFERENCES_1014.md` where it fits.
  - If you truly cannot open any video, cite the closest frame-by-frame sources you can read (Sakugabooru post pages, Muybridge plates, Richard Williams' walk notes) and say so in your report.

## Commands (background Blender, parallel-safe, ~10-20 s each; cwd = PetsV3)
```
BL="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"
"$BL" -b --factory-startup --python _tools/headless_model.py -- <Name> tq,front,side,back 600 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback"
python sheet3.py <Name> model_ 2                     # -> <Name>/renders/_model_sheet.png (Read it and LOOK, critically)
"$BL" -b --factory-startup --python _tools/headless_closeup.py -- <Name> x,y,z dist 700   # face close-ups
python sheet3.py <Name> close_ 3
"$BL" -b --factory-startup --python _tools/headless_pack.py -- <Name>                      # portrait + flat palette renders
python _tools/pack_post.py <Name> <Cmp1,Cmp2,...>    # 64/128 px icon strips next to comparison pets + value shares JSON
"$BL" -b --factory-startup --python _tools/headless_full.py -- <Name> idle:40,roar:30,act_x:30 2 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback"
python sheet3.py <Name> pose_tq 3
"$BL" -b --factory-startup --python _tools/headless_full.py -- <Name> - 1 export 2>&1 | grep -E "HEADLESS_RESULT|Error|Traceback"   # FINAL: step-1 check + export to C:\cdimp
```
- Bash heredocs with Python often break on quotes. Write patch scripts to a file (in your `_scratch`) and run them.
- headless_pack uses the model-only path while your pet file has no `anim()`.
- headless_closeup re-renders model_tq at 200 px, so render the model views LAST before a gate.

## Gates (STOP at each one and report; the lead runs a fresh Haiku reviewer and relays the verdict)
1. **MODEL GATE (all your pets together).** Build each model and critique it honestly yourself first (64 px read, side-view belly line, face close-up, value shares vs the plan, distinctness from the comparison pets). Iterate until it's genuinely good. Then produce for each pet:
   - `_model_sheet.png`, `_close_sheet.png`, `_icons_strip_64.png` / `_128.png` (comparison pets = its egg siblings), the value shares;
   - the tris and HEIGHT;
   - a short `<Name>/MODEL_NOTES.md` (what you built, deviations from the plan + why).
   Then END your turn with the report.
2. After the verdicts arrive: apply EVERY MUST and NICE fix, then author the clips (with ANIM_REFS.md first).
3. **CLIP GATE.** Pose sheets of the key beats of EVERY clip (`pose_tq`), the headless_full JSON (collision_free, ground_min_z, audit), the clip list with lengths and events, `<Name>/CLIP_NOTES.md`. END your turn with the report.
4. After the clip verdicts: fix, re-gate if the reviewer asks, then EXPORT (`headless_full ... - 1 export`) to `C:\cdimp\<Name>.fbx` (+ clip Lua + meta + portrait).
5. **FINAL report:** files, tris, collision_free, clips with lengths + events, VFX anchor bones, the signature act in one line, and anything odd.

Keep reports short and plain: paths + numbers + decisions.
