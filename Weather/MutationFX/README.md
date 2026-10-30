# Mutation effects v2 (UFO / Meteor on pets and eggs), 2026-10-12

The owner, on the first version: "UFO / Meteor VFX on pets, are ugly.. Low quality.. Can we fix that?"

**Why v1 looked bad:** every particle came from ONE attachment at the model's centre, including a big glow billboard
scaled with the pet. That made a green fog blob that lit up the walls, and the Meteor version was a few flames from a
single point.

**Owner's pick (2026-10-12):** "remove the little green particle that's like a dot looking ... also the ring around it ... the electric energy is cool. Don't touch meteor." So the UFO lost both dot effects (Motes, Coat) and both rings (Reticle, Scan). The full v2 UFO is in `ServerStorage._Backup_MutationFX.UFOAura_v2_full`; a WeatherTests check keeps the dots and rings out.

**v2:** `ReplicatedStorage.MutationFX` dresses the body. The templates in `ReplicatedStorage.WeatherFX` are folders
with up to three Attachments of ParticleEmitters, authored for a 6-stud model:

| Section | Where it goes | UFO | Meteor |
|---|---|---|---|
| Body | 8 points spread over the pet's Bones (farthest-point pick), or an ellipsoid around a rigless egg | Zaps (quick green electric crackles), Glints (thin 4-point sparkles) | Embers (short orange streaks, velocity-aligned) |
| Top | 5 points on the upper body | - | Flames (flame licks), Smoke (dark wisps) |
| Ground | 1 point at the feet; sized by the footprint | - | Heat (orange glow on the ground) |

- **On a rig,** each point is a small child Bone of the picked bone, turned upright in the model's frame. A bone's own
  axes point along the limb, so "Top" emitted sideways. The animator only drives the bones its clips name.
- **Pets out of range:** PetAnimator switches the effects off past ANIMATE_RANGE (`MutationFX.setEnabled`), like the
  creature effects.
- **Textures** are all from the VFX Studio library:
  - UFO: Spec soft dot 6673021984, Star thin glint 114082716877453, Lightning spider 332491482, Circle reticle
    12402871480, Circle soft ring 7136539160.
  - Meteor: Spec spark streak 80742887810818, Fire flame 11037279462, Smoke #4 4510290214.
- **Gotchas:**
  - Black-background textures (the flame) need LightEmission 1, or a dark square shows.
  - In velocity-aligned mode the streak texture needs Rotation 90.
  - Additive colours wash out to white on the bright floors, so the ground rings use LightEmission 0.25-0.35.
- **v1** (templates + module) is backed up in `ServerStorage._Backup_MutationFX`.
- **Studio preview stage:** `require(ServerStorage._MutPreviewKit:Clone())(petName, "UFO" | "Meteor" | "UFO,Meteor")`
  puts a pet on a platform at y = 600 and frames it. Delete `workspace._MutStage` afterwards.
- `sheets/`: contact sheets of VFX Studio library textures (public Roblox thumbnails), used to choose by eye.
  `make_sheets.py` + `lib_ids.json` rebuild them.
