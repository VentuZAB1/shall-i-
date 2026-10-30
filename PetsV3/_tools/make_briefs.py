base = open("_tools/builder_prompt.md", encoding="utf-8").read()
groups = {
    "A": ("MossbackTortoise (tier 1), ForestStag (tier 1), Treant (tier 1), Kappa (tier 2)", ""),
    "B": ("SeaTurtleWarrior (tier 2), Kraken (tier 2, floater/swimmer: MOTION Swim, its swim clip is the locomotion), "
          "ThunderBull (tier 3), StormWyvern (tier 3, flyer)",
          "StormWyvern is a flyer: keep its fly/takeoff/land clips and the wing3.py rules (wings never pass through each "
          "other or the body); give the membrane wings the bible 2d construction."),
    "C": ("MoltenBoar (tier 4), LavaGolem (tier 4), Cerberus (tier 4, 3 heads), ShadePanther (tier 5)",
          "Cerberus's three heads: use face_eyes on each head block if it faces roughly -y, else B.eye(...) with the "
          "head's front normal."),
    "D": ("NightmareStallion (tier 5), BlackDragon (tier 5, eastern serpent flyer), SolarLion (tier 6), "
          "Griffin (tier 6, flyer)",
          "Griffin was never exported and its last full run was not re-checked: its wing fold uses "
          "FOLD = (-25, -16, -5, 100), walk du 14, preen du 50; it must end collision_free with the (Wing, WingTip) "
          "pairs included. BlackDragon flies (serpent): keep its fly clips."),
}
for g, (pets, extra) in groups.items():
    s = base.replace("{PETS}", pets).replace("{EXTRA}", extra)
    open(f"_tools/builder_{g}.md", "w", encoding="utf-8").write(s)

extraE = r"""These 4 pets have NO PetsV3 spec yet: create pets\<Name>.py from scratch in the V3 block style. Their
approved PetsV2 versions (smooth chibi style, metaball bodies) are in
C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV2\pets\<Name>.py: READ them for DISPLAY / MOTION / RIG /
HEIGHT, the rig (bone names + joint layout) and the animations (idle, walk, roar, the unique signature act, and for
flyers fly / takeoff with event "launch" / land with event "touch"). Port the rig + animations into the new spec
(BlockPet supports k.joint / k.key / the cm helpers / k.add_leg2 / k.solve_leg; drop V2-only body/metaball code,
model() is blocks now), keeping each pet's personality and its signature act. Flyers: copy the wing approach of
pets\StormWyvern.py / pets\Griffin.py with wing3.py (wings never through each other or the body; legs pump while
flying). The owner LOVED the V2 Cvetibara design (caramel capybara, halo, flower, white-to-gold wings): keep its
concept, rebuilt in blocks with the softest settings (bible SECRET row). Ivonrath = red fire dragon (fire breath is a
particle VFX later, never a glowing mesh). PharaohAsparuh = Persian-cat pharaoh in a sphinx pose. Look at the V2
renders in PetsV2\<Name>\renders\ if they exist. Add a 1-line ledger entry per pet to your report (signature act)."""
s = base.replace("{PETS}", 'Cvetibara (SECRET, tier "S"), Ivonrath (SECRET "S", flyer), PharaohAsparuh (SECRET "S"), '
                 'CelestialDragon (tier 6, flyer)').replace("{EXTRA}", extraE)
open("_tools/builder_E.md", "w", encoding="utf-8").write(s)
print("written")
