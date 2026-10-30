import sys, os
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\Graveyard")
sys.argv = [sys.argv[0]]
import graveyard as G
from mathutils import Vector
G.ground_scene()
ob = G.import_asset("Grave_C", "blend")
G.shoot(os.path.join(G.WIP, "look_C_right.png"), Vector((1.0, 0.3, 2.9)), (1.0, -0.6, 0.35), 4.0, lens=50)
hi = None
import bpy
with bpy.data.libraries.load(os.path.join(G.OUT, "Grave_C.blend")) as (s, d):
    d.objects = ["Grave_C_hi"]
h = d.objects[0]; G.link(h); h.hide_render = False; h.location.x = 6
ob.hide_render = True
G.shoot(os.path.join(G.WIP, "look_C_right_hi.png"), Vector((7.0, 0.3, 2.9)), (1.0, -0.6, 0.35), 4.0, lens=50)
