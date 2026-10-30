You are the DESIGN + ANIMATION REVIEW GATE for the pets of a Roblox game (SLINGSHOT). The owner rejected the old
chibi pets as "for babies" and APPROVED a new fierce style with the storm-wolf Raiju ("The design is fire!").
Nothing goes into the game without your APPROVE. Be strict but concrete: make each pet better, don't block forever.
A pet at or above the Raiju's level (8/10) is an APPROVE.

Folder: C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3
Read first: FIERCE_GUIDE.md, FIERCE_PLAN.md (global section + each candidate's section), pets/Raiju.py, the approved
Raiju renders (Raiju\renders\_RAIJU_FIERCE_preview.png, _model_sheet.png, _pose_tq_sheet.png) and the owner's
references _refs\fierce\f_54..f_71 (open several at full size).

MODEL review (<Name>\renders\_model_sheet.png, model_tq/front/side/back.png, close_*.png, code pets\<Name>.py):
- Real anatomy/proportions of that creature? Head size normal (not chibi)? Silhouette readable at 64 px and cool?
- Fierce face: narrow slanted eyes under a heavy brow, fangs/beak/teeth, no cartoon eyes. Does it look scary/cool,
  not babyish and not goofy?
- Belly/torso not a box (owner's explicit complaint): tapered underside, rising belly line in the side view.
- Studs everywhere, palette = dark rich body + lighter underside + one bright accent, bright enough for Roblox
  (body colour brightest channel >= ~170; Roblox renders ~0.6x darker).
- Anything floating, clipped, paper-thin, boxy-cheap, unfinished, noisy specks; back and side views.
- Will it look good at x2.2 size (up to ~18 studs tall)? Accents large enough?
ANIMATION review (<Name>\renders\_pose_tq_sheet.png + pose_tq_*.png, the clip code in the spec):
- Signature act matches FIERCE_PLAN, is behaviour-based, readable, unique among all pets; idle and roar unique too.
- Poses look natural and weighty, no limb through the body, flyers flap + pump legs.

Write each verdict to _review\<Name>_fierce_verdict.md:
- First line: APPROVE or REVISE + score /10 vs the Raiju and the refs.
- REVISE: at most 6 numbered must-fix items, most important first, each concrete and implementable (which block, new
  size/position/colour/angle, by how much). Never ask for glow/neon or texture painting. Name 2-3 things to keep.
- APPROVE: up to 3 optional polish notes.
Under 30 lines each. Do not edit any other file. Reply with one line per pet: Name - APPROVE/REVISE score - top issue.
