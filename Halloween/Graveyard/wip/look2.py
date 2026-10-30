import sys, os
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\Graveyard")
sys.argv = [sys.argv[0]]
import graveyard as G
from mathutils import Vector
G.ground_scene()
ob = G.import_asset("Grave_C", "fbx")
G.shoot(os.path.join(G.WIP, "look_C_edge.png"), Vector((1.45, -0.3, 1.6)), (1.0, -0.8, 0.2), 2.6, lens=50)
G.shoot(os.path.join(G.WIP, "look_C_r34_12.png"), Vector((0.3, 0.0, 2.0)), (1.0, -0.75, 0.3), 12.0, lens=50)
G.shoot(os.path.join(G.WIP, "look_C_front25.png"), Vector((0.0, 0.0, 1.8)), (0.25, -1.0, 0.3), 25.0, lens=50)
