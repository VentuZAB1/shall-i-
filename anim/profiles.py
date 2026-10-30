"""Motion personality per creature. Lengths are multiples of the creature's leg length, times in seconds.
Each creature = a style preset + optional overrides. Used by author.py."""

STYLES = {
    # heavy four-legged beasts: slow, stomping, body rolls side to side, head swings low
    "heavy": dict(walkT=1.35, stride=0.55, lift=0.10, bob=0.04, sway=0.035, roll=0.06, nod=0.07, stab=0.2,
                  tail=0.12, idleT=6.0, roarT=2.8, acts=("stomp", "sniff")),
    # hoofed animals: head nods with every step
    "hoofed": dict(walkT=1.0, stride=0.75, lift=0.18, bob=0.03, sway=0.012, roll=0.03, nod=0.10, stab=0.0,
                   tail=0.15, idleT=5.0, roarT=2.4, acts=("shake", "sniff", "stomp")),
    # hunters: smooth, low, head locked on target
    "predator": dict(walkT=0.85, stride=0.85, lift=0.20, bob=0.02, sway=0.01, roll=0.025, nod=0.0, stab=0.85,
                     tail=0.22, idleT=4.0, roarT=2.2, acts=("stretch", "shake", "sniff")),
    # lizard: trot gait (diagonal pairs) + spine snakes sideways
    "reptile": dict(walkT=0.8, stride=0.7, lift=0.12, bob=0.01, sway=0.0, roll=0.02, nod=0.0, stab=0.7,
                    tail=0.30, spine=0.16, gait="trot", idleT=5.0, roarT=2.2, acts=("sniff", "shake")),
    "tortoise": dict(walkT=1.7, stride=0.45, lift=0.09, bob=0.02, sway=0.03, roll=0.05, nod=0.04, stab=0.3,
                     tail=0.05, idleT=7.0, roarT=2.8, acts=("sniff",)),
    # two legs
    "biped_heavy": dict(walkT=1.45, stride=0.5, lift=0.10, bob=0.04, sway=0.06, roll=0.07, nod=0.04, stab=0.3,
                        tail=0.10, arms=0.30, idleT=6.0, roarT=2.8, acts=("pound", "look")),
    "biped": dict(walkT=1.0, stride=0.7, lift=0.16, bob=0.03, sway=0.03, roll=0.04, nod=0.03, stab=0.5,
                  tail=0.18, arms=0.45, idleT=4.5, roarT=2.4, acts=("look", "crouch")),
    "biped_bird": dict(walkT=0.7, stride=0.6, lift=0.2, bob=0.03, sway=0.02, roll=0.03, nod=0.0, stab=0.0,
                       headbob=0.18, tail=0.08, arms=0.0, idleT=4.0, roarT=2.2, acts=("look", "shake")),
    # many legs
    "multileg": dict(walkT=0.55, stride=0.45, lift=0.28, bob=0.01, sway=0.0, roll=0.02, nod=0.0, stab=0.6,
                     tail=0.10, idleT=4.0, roarT=2.2, acts=("twitch",)),
    # flyers on the ground use a walking style above + wing settings here
    "bird": dict(walkT=0.7, stride=0.6, lift=0.2, bob=0.03, sway=0.02, roll=0.03, nod=0.0, stab=0.6,
                 tail=0.08, arms=0.0, flapT=0.75, flapA=1.0, idleT=4.0, roarT=2.2, acts=("wingstretch", "shake")),
    "dragon": dict(walkT=1.1, stride=0.7, lift=0.15, bob=0.03, sway=0.02, roll=0.04, nod=0.0, stab=0.7,
                   tail=0.18, flapT=1.05, flapA=0.9, idleT=5.0, roarT=2.6, acts=("wingstretch", "shake")),
    "moth": dict(flapT=0.32, flapA=0.9, idleT=4.0, roarT=2.0, acts=()),
    "skydragon": dict(walkT=1.1, stride=0.7, lift=0.15, bob=0.03, sway=0.02, roll=0.04, nod=0.0, stab=0.7,
                      tail=0.3, flapT=2.2, idleT=5.0, roarT=2.6, acts=("shake", "sniff")),
    # water / slither
    "swim": dict(swimT=1.8, idleT=5.0, roarT=2.4, acts=()),
    "snake": dict(slitherT=1.4, idleT=5.0, roarT=2.0, acts=()),
}

CREATURE = {
    "ForestStag": ("hoofed", {}),
    "MossbackTortoise": ("tortoise", {}),
    "VineSerpent": ("snake", {}),
    "Treant": ("biped_heavy", {}),
    "krakens": ("swim", {}),
    "Sea Turtle Warrior": ("tortoise", {"walkT": 1.4, "stride": 0.55}),
    "Kappa": ("biped", {"acts": ("crouch", "look")}),
    "Hippocampus": ("swim", {}),
    "Spark Fox": ("biped", {"walkT": 0.8, "stride": 0.65, "acts": ("look", "crouch")}),
    "Raiju": ("predator", {}),
    "Storm Ram": ("hoofed", {"acts": ("stomp", "shake")}),
    "Thunder Bull": ("heavy", {}),
    "Thunderbird": ("bird", {"flapT": 0.95}),
    "Storm Wyvern": ("dragon", {}),
    "Ember Hound": ("predator", {}),
    "Magma Salamander": ("reptile", {}),
    "Cinder Scorpion": ("multileg", {"tail": 0.05}),
    "Molten Boar": ("heavy", {"walkT": 1.0, "stride": 0.65, "acts": ("stomp", "sniff")}),
    "Flame Lynx": ("predator", {}),
    "Lava Golem": ("biped_heavy", {}),
    "Phoenix": ("bird", {"flapT": 0.85}),
    "Inferno Drake": ("dragon", {}),
    "Nightwing Bat": ("bird", {"flapT": 0.45, "flapA": 1.1}),
    "Gloom Spider": ("multileg", {}),
    "Shade Panther": ("predator", {}),
    "Bone Raven": ("biped_bird", {}),
    "Wraith Hound": ("predator", {"walkT": 0.8}),
    "Nightmare Stallion": ("hoofed", {"walkT": 0.95, "stride": 0.8}),
    "Void Serpent": ("snake", {}),
    "Shadow Mantis": ("multileg", {"walkT": 0.65}),
    "Abyss Behemoth": ("biped_heavy", {}),
    "Void Dragon": ("dragon", {"flapT": 1.2}),
    "Star Moth": ("moth", {}),
    "Lunar Jackal": ("biped", {"walkT": 0.85}),
    "Solar Lion": ("predator", {"walkT": 0.95, "stab": 0.5, "acts": ("stretch", "shake")}),
    "Nebula Jelly": ("swim", {"swimT": 2.2}),
    "Griffin": ("dragon", {"flapT": 0.9, "lean": 0.9}),
    "Star Pegasus": ("dragon", {"flapT": 1.0, "nod": 0.08, "stab": 0.0}),
    "Celestial Tiger": ("predator", {}),
    "Seraph Owl": ("bird", {"flapT": 0.9}),
    "Qilin": ("hoofed", {}),
    "Celestial Dragon": ("skydragon", {}),
}

# Blender file name -> Roblox model name
ROBLOX_NAME = {"krakens": "Kraken"}


def roblox_name(name):
    return ROBLOX_NAME.get(name, name.replace(" ", ""))


def profile_for(name):
    style, over = CREATURE[name]
    p = dict(STYLES[style])
    p.update(over)
    p["style"] = style
    return p
