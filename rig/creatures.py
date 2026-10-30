# Rig type + options per Meshy creature (file name in ~/Downloads/Meshy without .glb).
RIG = {
    # Grass (Claude Design keepers, prepared by prep_cd.py into rig/src)
    "ForestStag": ("quad", {}),
    "MossbackTortoise": ("quad", {"tail": 0}),
    "VineSerpent": ("snake", {}),
    "Treant": ("biped", {"tail": 0}),  # needs ~/Downloads/Treant.glb -> prep_cd.py first
    # Water
    "krakens": ("kraken", {"bell": 0.5, "tents": 8}),
    "Sea Turtle Warrior": ("quad", {"tail": 0}),
    "Kappa": ("biped", {}),
    "Hippocampus": ("seahorse", {}),
    # Thunder
    "Spark Fox": ("biped", {}),  # stands upright on its hind legs
    "Raiju": ("quad", {}),
    "Storm Ram": ("quad", {}),
    "Thunder Bull": ("quad", {}),
    "Thunderbird": ("bird", {}),
    "Storm Wyvern": ("wingquad", {}),
    # Fire
    "Ember Hound": ("quad", {}),
    "Magma Salamander": ("quad", {}),
    "Cinder Scorpion": ("multileg", {"legs": 8}),
    "Molten Boar": ("quad", {}),
    "Flame Lynx": ("quad", {}),
    "Lava Golem": ("biped", {"tail": 0}),
    "Phoenix": ("bird", {}),
    "Inferno Drake": ("wingquad", {}),
    # Shadow
    "Nightwing Bat": ("bird", {}),
    "Gloom Spider": ("multileg", {"legs": 8, "tail": 0}),
    "Shade Panther": ("quad", {}),
    "Bone Raven": ("biped", {"arms": 0}),
    "Wraith Hound": ("quad", {}),
    "Nightmare Stallion": ("quad", {}),
    "Void Serpent": ("serpent", {}),
    "Shadow Mantis": ("multileg", {"legs": 6, "wings": 1, "tail": 0}),
    "Abyss Behemoth": ("biped", {"tail": 0}),
    "Void Dragon": ("bird", {}),  # stands on two legs, wings
    # Celestial
    "Star Moth": ("moth", {}),
    "Lunar Jackal": ("biped", {}),
    "Solar Lion": ("quad", {}),
    "Nebula Jelly": ("jelly", {"bell": 0.6, "tents": 8}),
    "Griffin": ("wingquad", {}),
    "Star Pegasus": ("wingquad", {}),
    "Celestial Tiger": ("quad", {}),
    "Seraph Owl": ("bird", {}),
    "Qilin": ("quad", {}),
    "Celestial Dragon": ("quad", {}),
}

# Hand-placed feet (x, y in the rigger's normalised space: height 2, +X = creature's left, +Y = back)
# for models whose pose fools the foot clustering (paws close together, tail tip on the ground).
FEET = {
    "Flame Lynx": [(-0.48, -0.78), (-0.15, -0.74), (0.32, 0.88), (0.08, 1.18)],
    "Shade Panther": [(-0.22, -0.86), (0.02, -0.86), (0.4, -0.05), (-0.3, 0.15)],
    "Shadow Mantis": [(0.36, -1.0), (-0.45, -1.0), (0.26, 0.72), (-0.32, 0.72)],
}
