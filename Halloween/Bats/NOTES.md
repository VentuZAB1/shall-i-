# Halloween BAT - notes (2026-10-12)

A flying bat for the flock (~10-14) that circles the giant jack-o'-lantern behind the hub's back wall. It's a fierce,
semi-realistic vampire / fruit-bat mix:
- dark brown-black combed fur with a rusty mantle;
- big pointed ears with inner ridges;
- deep-set slanted glossy eyes under a heavy brow;
- a fox-like muzzle with snarl wrinkles, an open mouth and 2+2 fangs;
- leathery plum-brown membrane wings (thin panels lighter, fine veins + elastin striations) on visible arm, forearm and
  finger bones, with hooked thumb claws;
- clawed hind legs trailing, and a narrow tail membrane.

**All coordinates below are in BLENDER space** (1 Blender metre = 1 stud, +Z up). The lead's note: Studio's importer
turns the model 180 degrees, so Blender +Y comes out as Roblox +Z and Blender +X as Roblox -X. See "Facing" below.

## Files
| What | Path |
|---|---|
| Build script | `Halloween\Bats\bat.py` (headless: `blender.exe -b --factory-startup --python bat.py -- build`, then `-- render export`) |
| Source scene | `Halloween\Bats\bat.blend`: game mesh `Bat` + `Armature` + actions `fly` / `glide`; the hi sculpt is in the hidden collection `Sculpt_hi` |
| FBX | `C:\cdimp\Halloween_Bat.fbx` (armature + skinned mesh, textures embedded, global scale 0.01 = 1 stud per metre) |
| Maps (1024) | `Halloween\Bats\maps\Bat_albedo.png` (colour x AO), `Bat_normal.png` (tangent, OpenGL +Y), `Bat_rough.png`; `Bat_ao.png` is only for reference (it's already multiplied into the albedo) |
| CreatureClips module | `Halloween\Bats\Bat.lua` -> ModuleScript **`ReplicatedStorage.CreatureClips.Bat`** (same petkit format as the PetsV2 modules; `Bat.json` is the same data) |
| Reviews | `review_bat_34.png`, `review_bat_top.png`, `review_bat_below.png`, `review_bat_face.png`, `review_flock_45studs.png`, `review_flock_below.png`, `review_flap_strip.png`; `renders\review_wing_close.png`, `renders\glide_strip.png`, `renders\flap_strip_front.png`, single frames `renders\strip_f*.png` |

## The object
| Name | Size (studs, X x Y x Z) | Tris | Texture | Pivot |
|---|---|---|---|---|
| `Bat` (one skinned MeshPart, material `Bat_PBR`) | 5.00 x 1.52 x 0.67 (wingspan 5.0 in the rest pose) | 5,740 | 1024 colour / normal / roughness | Origin (0, 0, 0) = body centre (chest/belly), also the `Root` bone |

- The hi sculpt was about 128k tris. The game mesh is its own coarse version of the same shapes.
- UV atlas:
  - v 0-0.5: the wing membrane. Left/right and top/bottom share one planar island, so the membrane detail is mirrored.
  - top-left square: body and head.
  - top-right square: ears, eyes, teeth, nose, mouth, arm/finger bones, legs, tail membrane.
- The maps were baked at 2048 and box-filtered down to 1024 (anti-aliased).
- The wing-bone faces were re-baked on their own, because their bake rays hit the membrane.
- Rest pose = wings spread flat (the glide pose without dihedral), legs trailing.

## Facing
- In Blender the bat **flies along +Y**: the nose is at +Y, up is +Z.
- So the bat's **anatomical LEFT is Blender -X** (bones `*_L`) and its **RIGHT is Blender +X** (`*_R`).
- After Studio's 180-degree import turn, the nose points along the imported model's **Roblox +Z**, the opposite of the
  pivot's LookVector. The bat's left wing ends up on Roblox +X.
- For the flock, aim the model the other way: `CFrame.lookAt(pos, pos - velocity)`, or append
  `* CFrame.Angles(0, math.pi, 0)` to the flight CFrame. Alternatively, rotate the PivotOffset 180 degrees on Y once.
- Do **not** rotate bones or the root part on their own.
- Check after import: `(Head.WorldPosition - Root.WorldPosition)` should point along the travel direction.
- The clips were sampled with petkit's mapping, Blender (x, y, z) -> Roblox root space (-x, z, y). That is the same
  180-degree convention the importer applies, so the clips match the imported bones whichever way you aim the model.

## Rig (11 bones, roll 0; head -> tail in Blender studs)
| Bone | Parent | Head | Tail | Skins |
|---|---|---|---|---|
| `Root` | - | (0, 0, 0) | (0, 0, 0.2) | nothing: zero influence, so **tick "Keep Zero Influence Bones"** |
| `Body` | Root | (0, -0.024, 0) | (0, 0.312, 0.048) | torso, membrane root along the flank |
| `Head` | Body | (0, 0.372, 0.06) | (0, 0.636, 0.06) | head, eyes, nose, mouth, fangs |
| `Ear_L` / `Ear_R` | Head | (-/+0.079, 0.462, 0.178) | (-/+0.185, 0.42, 0.442) | ears (base blends into Head) |
| `Wing_L` / `Wing_R` | Body | shoulder (-/+0.156, 0.192, 0.06) | wrist (-/+1.20, 0.30, 0.14) | humerus + forearm + inner membrane (arm bone) |
| `WingTip_L` / `WingTip_R` | Wing_* | wrist (-/+1.20, 0.30, 0.14) | (-/+1.647, 0.252, 0.126) | hand: thumb, fingers 2-5, finger membrane (hand bone) |
| `Leg_L` / `Leg_R` | Body | hip (-/+0.084, -0.324, -0.042) | ankle (-/+0.192, -0.54, -0.054) | legs, feet, claws; the membrane's ankle corner |

- Weights are positional and smooth: inverse-distance over arm / fingers / flank / leg for the membrane, arm and legs.
- That gives at most 4 influences per vertex and no unweighted vertices.
- The membrane is one connected sheet and follows arm + hand + body + leg without tearing.

## Clips (CreatureClips module `Bat`: fps 30, ref = Head, dist 0.37681)
| Clip | Frames | Length | Loop | What |
|---|---|---|---|---|
| `fly` | 12 | **0.40 s** | yes (seamless, audited 0 deg / 0 stud seam) | One wingbeat (keys below). The downstroke is fast (frames 0-5, 42%); the upstroke folds and recovers (5-12, 58%). The body rises on the downstroke (bob +-0.034 studs, pos channel on `Body`), the nose lifts about 2.5 deg on the power stroke (base 6 deg nose-up), the head counter-rotates and lags a frame, the ears flutter back, the legs pump. |
| `glide` | 72 | **2.40 s** | yes | Wings spread with about 7 deg dihedral. Small trims: L/R asymmetry, wingtip twist, +-4 deg body bank. The head looks around (+-12 deg yaw), the ears twitch, the legs drift. |

Key poses of `fly` (frame: arm raise / sweep forward / pronation, hand raise / hand sweep, in degrees):

| Frame | Arm | Hand | Pose |
|---|---|---|---|
| 0 | +58 / +2 / -4 | +22 / -14 | TOP |
| 2 | +14 / +12 / +12 | +4 / +6 | MAX SPAN, the power pose |
| 4 | -34 / +8 / +10 | -16 / +4 | late downstroke |
| 5 | -46 / +2 / +4 | -26 / -6 | BOTTOM, wings wrapped under |
| 7 | -26 / -12 / -14 | -40 / -44 | early upstroke: the wrist leads, the hand folds back and down |
| 9 | +16 / -12 / -14 | -24 / -46 | mid upstroke, still folded |
| 11 | +46 / -4 / -8 | +6 / -30 | unfolding |

For the flock, I suggest:
- Give each bat a random clip phase and play speed x0.9-1.15.
- Use mostly `fly`, with `glide` stretches of 1-3 s.
- Bank the whole model 15-25 deg into the turn.

`review_flap_strip.png` reads left to right, top row then bottom row: frames 0, 2, 4, 5 / 7, 8, 9, 11 (3/4 front view).

## Animation reference (owner rule: animationreference.org)
- **Clip:** "Batman: Background Animation & Creature Animation (#01 (BD) - Batman: The Animated Series)", from
  `/tags/flying` page 3. That's Sakugabooru post 69115: Man-Bat flying while dragging a victim.
- **Cost:** 1 clip open (counter 24 -> 23 of 25).
- **Format:** 24 fps, animated on twos. Frames were sampled from the overlay's `<video>` element.
- **Close shot f87-f109:** one beat is 10 drawings from top to top (f93 -> f103), or 0.42 s. That gave the 12-frame
  (0.40 s) cycle. Breakdown:
  - The downstroke is fast: f93 top -> f95 full span -> f97 below the body, about 40%.
  - At the bottom (f97-99) the wings wrap under.
  - The upstroke is slower, about 60%: at f101 the wrist leads, the hand is folded with the tips trailing down and back,
    then f103 is the top again.
  - The body rises on the downstroke; the head stays steady.
- **Far top-down shot f122-f140:** the max-span silhouette (f126-130: fingers fanned, deep scallops in the trailing
  edge) became frame 2 and the membrane outline. The wrap-under at f132 became frame 5. The folded upstroke at f134
  became frames 7-9.
- **Face f10:** heavy brow over the eye, a wrinkled muzzle, the upper lip raised over a long upper fang plus a lower
  fang. This informed the head sculpt.
- The footage was used only as reference for timing, poses and silhouette. Nothing was traced or copied.

## Attachment points (Blender object space, studs, rest pose; better to parent Attachments to the named bone)
| Point | Position | Bone |
|---|---|---|
| Eyes (for an optional faint red eye-glint particle) | (-/+0.065, 0.60, 0.105) | Head |
| Mouth centre | (0, 0.658, -0.019) | Head |
| Snout tip | (0, 0.775, 0.053) | Head |
| Wingtips (longest finger, for trail / dust motes) | (-/+2.50, 0.16, 0.10) | WingTip_* |
| Wrist / thumb claw | (-/+1.20, 0.30, 0.14) | Wing_* tail / WingTip_* head |
| Feet | (-/+0.197, -0.594, -0.052) | Leg_* |
| Body centre | (0, 0, 0) | Root / Body |

## Roblox setup for the lead
1. Import `C:\cdimp\Halloween_Bat.fbx` with **Keep Zero Influence Bones** ticked, so `Root` survives.
   - The importer builds the SurfaceAppearance from the embedded colour / normal / roughness. There's no metalness map.
   - Zero the importer's pivot rotation as usual, then aim the model as described under "Facing".
2. Settings:
   - No Neon, no emissive, no transparency.
   - DoubleSided is not needed: the membrane has real thickness (0.016 studs, closed rim).
   - Anchored; CanCollide / CanQuery / CanTouch off.
   - CastShadow optional (small and many; off is cheaper).
3. Scale: 1 stud = 1 metre, so the wingspan is 5.0 studs. `ScaleTo` is safe, because clip positions scale through the
   ref distance.
4. Clips: put `Bat.lua` in `ReplicatedStorage.CreatureClips.Bat` and drive it with CreatureAnimator (Bone.Transform),
   like the pets.
5. Glow: any eye glint is particles / lights only, set up in Studio.

## Known limitations
- The fur is baked (normal + colour). The silhouette is the smooth body shell, which is fine at 20+ studs.
- The membrane texture is shared L/R and top/bottom, so the vein pattern is mirrored.
- The underside reads mostly as a dark silhouette against the sky, which is intended.
- At extreme close-up (under about 3 studs):
  - faint stair-step streaks along the innermost finger bone;
  - slight faceting on the lo ears and eyes.
- The eyes are glossy black with a matte dark-red rim. There's no glow (owner rule).
- The legs are single bones (no foot bones). The feet are rigid with the shin.
