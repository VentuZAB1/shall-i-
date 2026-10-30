# quick probe: does a Cycles selected-to-active NORMAL bake pick up a shader Bump driven by a UV map on the hi mesh?
import sys
sys.path.insert(0, r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween")
from hkit import *  # noqa
import numpy as np

sc = fresh(4)
# hi: a 1x1 grid at z=0 with UV "LeafUV" (u -1..1, v 0..1)
bm = bmesh.new()
n = 20
vs = [[bm.verts.new((i / n - 0.5, j / n - 0.5, 0.0)) for i in range(n + 1)] for j in range(n + 1)]
for j in range(n):
    for i in range(n):
        bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
hi = obj_from_bm(bm, "hi")
uv = hi.data.uv_layers.new(name="LeafUV")
for lp in hi.data.loops:
    co = hi.data.vertices[lp.vertex_index].co
    uv.data[lp.index].uv = (co.x * 2.0, co.y + 0.5)
m = bpy.data.materials.new("veins")
m.use_nodes = True
nt = m.node_tree
b = nt.nodes["Principled BSDF"]
uvn = nt.nodes.new("ShaderNodeUVMap")
uvn.uv_map = "LeafUV"
sep = nt.nodes.new("ShaderNodeSeparateXYZ")
nt.links.new(uvn.outputs["UV"], sep.inputs["Vector"])
mth = nt.nodes.new("ShaderNodeMath")
mth.operation = "SINE"
mul = nt.nodes.new("ShaderNodeMath")
mul.operation = "MULTIPLY"
mul.inputs[1].default_value = 30.0
nt.links.new(sep.outputs["Y"], mul.inputs[0])
nt.links.new(mul.outputs[0], mth.inputs[0])
bp = nt.nodes.new("ShaderNodeBump")
bp.inputs["Strength"].default_value = 1.0
bp.inputs["Distance"].default_value = 0.02
nt.links.new(mth.outputs[0], bp.inputs["Height"])
nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
hi.data.materials.append(m)
# lo: a quad slightly below
bm = bmesh.new()
q = [bm.verts.new(p) for p in ((-0.5, -0.5, -0.01), (0.5, -0.5, -0.01), (0.5, 0.5, -0.01), (-0.5, 0.5, -0.01))]
bm.faces.new(q)
lo = obj_from_bm(bm, "lo")
lo.data.uv_layers.new(name="UVMap")
for lp in lo.data.loops:
    co = lo.data.vertices[lp.vertex_index].co
    lo.data.uv_layers["UVMap"].data[lp.index].uv = (co.x + 0.5, co.y + 0.5)
imgs = bake_set(lo, [hi], 128, "probe", cage=0.05, maxray=0.1,
                outdir=r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\SpookyBushes\wip")
a = np.array(imgs["normal"].pixels[:]).reshape(128, 128, 4)
print("PROBE normal R std", float(a[..., 0].std()), "G std", float(a[..., 1].std()), "B mean", float(a[..., 2].mean()),
      "miss", imgs["miss_fraction"])
