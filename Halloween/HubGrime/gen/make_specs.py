# HubGrime - single source of truth for the decal set (pure Python: importable from Blender and system Python).
# name: pixel size, carrier size in studs (w, h), surface, contact edge + hidden band (studs from that carrier edge),
# edges that carry content (Roblox wraps U/V: every other edge has a >= 4 px transparent margin)
SPECS = {
    "G_Crack_A": dict(px=(1024, 512), studs=(14, 7), surface="floor"),
    "G_Crack_B": dict(px=(768, 768), studs=(10, 10), surface="floor"),
    "G_Crack_C": dict(px=(960, 640), studs=(12, 8), surface="floor"),
    "G_Moss_A": dict(px=(576, 576), studs=(8, 8), surface="floor"),
    "G_Moss_B": dict(px=(720, 432), studs=(10, 6), surface="floor"),
    "G_Stain_A": dict(px=(512, 512), studs=(10, 10), surface="floor"),
    "G_Stain_B": dict(px=(576, 384), studs=(12, 8), surface="floor"),
    "G_Slime_A": dict(px=(512, 512), studs=(6, 6), surface="floor"),   # round 4: 5 -> 6 studs (same art, 1.2x)
    "W_Crack_A": dict(px=(384, 768), studs=(5, 10), surface="wall"),
    "W_Crack_B": dict(px=(608, 760), studs=(8, 10), surface="wall"),
    "W_Crack_C": dict(px=(448, 924), studs=(6, 12.375), surface="wall", contact=("bottom", 0.375)),
    "W_MossBase_A": dict(px=(1024, 272), studs=(24, 6.375), surface="wall", contact=("bottom", 0.375),
                         keep=("l", "r")),
    "W_MossBase_B": dict(px=(1024, 272), studs=(24, 6.375), surface="wall", contact=("bottom", 0.375),
                         keep=("l", "r")),
    "W_MossBase_EndL": dict(px=(256, 272), studs=(6, 6.375), surface="wall", contact=("bottom", 0.375),
                            keep=("r",)),
    "W_MossBase_EndR": dict(px=(256, 272), studs=(6, 6.375), surface="wall", contact=("bottom", 0.375),
                            keep=("l",)),
    "W_Drip_A": dict(px=(320, 908), studs=(4, 11.35), surface="wall", contact=("top", 0.35)),
    "W_Drip_B": dict(px=(320, 668), studs=(4, 8.35), surface="wall", contact=("top", 0.35)),
}
SPEC_STUDS = {k: v["studs"] for k, v in SPECS.items()}
