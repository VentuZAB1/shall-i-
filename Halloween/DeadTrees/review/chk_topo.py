import bpy, bmesh, sys, numpy as np
from mathutils import Vector
fbx = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=fbx)
for o in sorted([o for o in bpy.context.scene.objects if o.type == "MESH"], key=lambda o: o.name):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bm.transform(o.matrix_world.copy() * 1.0)
    for v in bm.verts: v.co *= 100.0
    bnd = [e for e in bm.edges if e.is_boundary]
    nonman = [e for e in bm.edges if not e.is_manifold and not e.is_boundary]
    # winding consistency: manifold edges where both faces traverse the edge in the same direction
    bad = 0
    for e in bm.edges:
        if len(e.link_faces) == 2:
            f1, f2 = e.link_faces
            def dirn(f):
                vs = [v.index for v in f.verts]
                i = vs.index(e.verts[0].index); j = vs.index(e.verts[1].index)
                return 1 if (j - i) % len(vs) == 1 else -1
            if dirn(f1) == dirn(f2):
                bad += 1
    zs = np.array([((e.verts[0].co + e.verts[1].co) / 2)[:] for e in bnd]) if bnd else np.zeros((0, 3))
    print("TOPO", o.name, "faces", len(bm.faces), "boundary_edges", len(bnd), "nonmanifold", len(nonman), "inconsistent_winding_edges", bad)
    if len(zs) and o.name.endswith(("_Trunk", "_Limbs")):
        # cluster boundary edges by height band
        for lo in np.arange(-0.5, 16, 0.5):
            sel = zs[(zs[:, 2] >= lo) & (zs[:, 2] < lo + 0.5)]
            if len(sel):
                c = sel.mean(0)
                print("TOPO    z %.1f-%.1f: %d boundary edges, centre (%.2f, %.2f, %.2f)" % (lo, lo + 0.5, len(sel), c[0], c[1], c[2]))
    # volume sign check (closed meshes): outward normals => positive
    vol = 0.0
    for f in bm.faces:
        vs = [v.co for v in f.verts]
        for k in range(1, len(vs) - 1):
            vol += vs[0].dot(vs[k].cross(vs[k + 1])) / 6.0
    print("TOPO    signed volume", round(vol, 3))
    bm.free()
