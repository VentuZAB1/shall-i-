# Review round 1, part C: layouts, rolls, budgets, AO, eye-height review renders
src = open("tptree.py", encoding="utf-8").read()


def rep(a, b, cnt=1):
    global src
    assert src.count(a) == cnt, (a[:80], src.count(a))
    src = src.replace(a, b)


def replace_block(start_marker, end_marker, new_text):
    global src
    s = src.index(start_marker)
    e = src.index(end_marker, s)
    src = src[:s] + new_text + src[e:]


rep('''    roll_tris = 2 * 24 * 2 + 4 * 24 * 2 + 2 * 24 * 2       # wrap + 4 annuli + inner tube, per roll
    roll_tris = len(rolls) * roll_tris''', '''    roll_tris = len(rolls) * (48 + 4 * 48 + 48)       # wrap + 4 annuli + inner tube (24-gon)''')

# twig 2 a bit longer (the roll hangs on it, clear of the canopy)
rep('''        out = mid.normalized() * 6.2''', '''        out = mid.normalized() * (6.55 if k == 3 else 6.2)''')

TREE = r'''def roll_arc(c, axis, e, phi0, phi1, gap0=0.0, gap1=0.02, step=0.1):
    """Points of a loose outer layer around a roll (in the plane across the axis: e = 0 deg, 'up' = 90 deg)."""
    a = Vector(axis).normalized()
    e = Vector(e)
    e = (e - a * e.dot(a)).normalized()
    up = a.cross(e).normalized()
    if up.z < 0:
        up = -up
    r0 = ROLL["Ro"] + 0.035
    n = max(3, int(abs(math.radians(phi1 - phi0)) * r0 / step) + 1)
    out = []
    for i in range(n):
        t = i / (n - 1)
        ph = math.radians(phi0 + (phi1 - phi0) * t)
        rr = r0 + gap0 + (gap1 - gap0) * t
        dirr = e * math.cos(ph) + up * math.sin(ph)
        out.append((Vector(c) + dirr * rr, dirr))
    return out


def roll_collider(col, rolls):
    dummy = {"outer": (0, 0, 8, 8), "endA": (0, 0, 8, 8), "endB": (0, 0, 8, 8), "inner": (0, 0, 8, 8), "size": 1024}
    for c, axis in rolls:
        V, F, _ = roll_low(c, axis, dummy)
        col.add(bvh_np(V, F), 0.05, "roll")


def tree_specs(twig_arc, fallen_arc, fallen_end):
    D = lambda az, el: ("dir", az, el)
    arcn = lambda arc: [("pt", tuple(p), tuple(n)) for p, n in arc]
    return [
        # two streamers thrown over the crown, tails on the diagonals
        dict(name="OverA", nodes=[D(42, -2), D(42, 45), D(62, 82), D(225, 45), D(225, -4)],
             spans=["drape"] * 4, pins=[False, True, True, True, False], tail0=4.6, tail1=4.8, twist=0.15),
        dict(name="OverB", nodes=[D(135, -3), D(135, 45), D(152, 80), D(313, 45), D(313, -5)],
             spans=["drape"] * 4, pins=[False, True, True, True, False], tail0=4.4, tail1=4.2, twist=0.17),
        # festoons sagging along the outer rim on all four sides, long tails on the back and sides
        dict(name="FestFront", nodes=[D(246, -13), D(292, -12)], spans=["sag:1.18"], pins=[True, True],
             tail0=0.9, tail1=2.6, twist=0.12),
        dict(name="FestRight", nodes=[D(336, -14), D(18, -12)], spans=["sag:1.17"], pins=[True, True],
             tail0=3.8, tail1=1.1, twist=0.12),
        dict(name="FestBack", nodes=[D(68, -12), D(112, -14)], spans=["sag:1.2"], pins=[True, True],
             tail0=1.3, tail1=4.3, twist=0.12),
        dict(name="FestLeft", nodes=[D(160, -13), D(204, -12)], spans=["sag:1.16"], pins=[True, True],
             tail0=4.1, tail1=1.0, twist=0.12),
        # strips thrown over the twigs that poke out of the canopy (back, front-left)
        dict(name="TwigBack", nodes=[("twig", 0, 0.9)], spans=[], pins=[True], tail0=0.6, tail1=3.6, twist=0.2),
        dict(name="TwigLeft", nodes=[("twig", 1, 0.9)], spans=[], pins=[True], tail0=3.0, tail1=0.6, twist=0.18),
        # the roll hanging on the front-right twig, unrolling into a long tail
        dict(name="TwigRoll", nodes=arcn(twig_arc), spans=["sag:1.0"] * (len(twig_arc) - 1),
             pins=[True] * len(twig_arc), tail1=4.0, dir1=(0, 0, -1), roll_start=True, tear=(False, True),
             twist=0.16),
        # the fallen, half-unrolled roll on the soil
        dict(name="FallenRoll", nodes=arcn(fallen_arc) + [("pt", tuple(fallen_end), (0, 0, 1))],
             spans=["sag:1.0"] * (len(fallen_arc) - 1) + ["sag:1.05"], pins=[True] * len(fallen_arc) + [False],
             roll_start=True, tear=(False, True), twist=0.0, sway=0.0),
    ]


'''
replace_block("def tree_specs(", "def canopy_parts(", TREE)

# ---------------------------------------------------------------- build_tree body
s = src.index("def build_tree():")
e = src.index("def bbox_of(", s)
src = src[:s] + r'''def build_tree():
    setup_scene()
    q = CFG["quick"]
    rep = {}
    clumps, blobs = tree_clumps(21)
    base, canopy = canopy_parts("Canopy", blobs, 0.09 if q else 0.06, 8, 0.12, 0.7, 5, 16600, 0.07,
                                lobes=dict(spacing=1.1, rad=(0.6, 0.85), amp=(0.2, 0.3)))
    area = mesh_area(base)
    nleaf = int(area * (6 if q else 25))
    log("canopy base", len(base.data.polygons), "area", round(area, 1), "leaves", nleaf)
    leaves, _p, _n = scatter_leaves("LeavesHi", base, nleaf,
                                    dict(L=(0.42, 0.62), wk=(0.48, 0.6), tilt=(0.16, 0.48), sink=0.03,
                                         fold=(0.15, 0.35), curl=(-0.05, 0.12), centre=TREE_CENTRE),
                                    tree_leaf_colours(clumps), 77)
    leaves.data.materials.append(mat_vc("LeafHi"))
    nv = len(base.data.vertices)
    set_colors(base.data, "Col", np.tile(L((84, 32, 20)), (nv, 1)))
    set_colors(base.data, "Rough", np.full((nv, 3), 0.95))
    base.data.materials.append(mat_vc("CanopyGapHi"))
    base.name = "CanopyHi"
    log("leaves", tri_count(leaves))
    br, limbs, twigs, lead = tree_skeleton(clumps, 3)
    trunk_hi, trunk, sk = build_trunk(br, base, 0.045 if q else 0.032, 5200, 9)
    log("trunk hi", tri_count(trunk_hi), "lo", tri_count(trunk), "canopy lo", tri_count(canopy))
    col = Colliders(0.035)
    cbv = bvh_ob(canopy)
    col.add(cbv, 0.085, "canopy")
    col.add(bvh_ob(trunk), 0.07, "trunk")
    ctx = dict(col=col, centre=TREE_CENTRE, limbs=limbs, twigs=twigs)
    # roll 1: hanging on the front-right twig (the twig runs through its core), end face + hole outward
    tw = twigs[2]
    tip = Vector(tw["P"][-1].tolist())
    dtw = Vector((tw["P"][-1] - tw["P"][-5]).tolist()).normalized()
    upw = (Vector((0, 0, 1)) - dtw * dtw.z).normalized()
    c1 = tip - dtw * (ROLL["hl"] + 0.14) - upw * (ROLL["Ri"] - float(tw["R"][-1]) - 0.01)
    ax1 = dtw
    e1 = Vector((-ax1.y, ax1.x, 0)).normalized()
    if e1.y > 0:
        e1 = -e1
    twig_arc = roll_arc(c1, ax1, e1, 100.0, 0.0, 0.0, 0.03)
    loc, nr, idx, dist = cbv.find_nearest(c1, 9.0)
    rep["roll_twig"] = dict(centre=[round(v, 3) for v in c1], axis=[round(v, 3) for v in ax1],
                            canopy_clear=round(dist - ROLL["Ro"], 3), inside=bool((c1 - loc).dot(nr) < 0))
    # roll 2: fallen on the soil at the front-left, half unrolled toward the trunk
    ang = math.radians(236)
    rdir = Vector((math.cos(ang), math.sin(ang), 0))
    tb = bvh_ob(trunk)
    rad = 2.4
    ax2 = Vector((math.cos(math.radians(300)), math.sin(math.radians(300)), 0.0))
    while rad < 5.0:
        c2 = rdir * rad + Vector((0, 0, ROLL["Ro"] + 0.065))
        loc, nr, idx, dist = tb.find_nearest(c2, 9.0)
        if dist > ROLL["Ro"] + 0.25 and (c2 - loc).dot(nr) > 0:
            break
        rad += 0.05
    e2 = Vector((-ax2.y, ax2.x, 0)).normalized()
    if e2.dot(-rdir) < 0:
        e2 = -e2
    fallen_arc = roll_arc(c2, ax2, -e2, 120.0, -95.0, 0.03, 0.0)      # over the top + far side, out from under it
    fallen_end = c2 + e2 * 1.9 + Vector((0, 0, -c2.z + 0.04))
    rep["roll_fallen"] = dict(centre=[round(v, 3) for v in c2], axis=[round(v, 3) for v in ax2], radius=round(rad, 2))
    rolls = [(c1, ax1), (c2, ax2)]
    roll_collider(col, rolls)
    specs = tree_specs(twig_arc, fallen_arc, fallen_end)
    budget = 29950 - tri_count(trunk) - tri_count(canopy)
    tp_los, tp_his, done, trep = build_tp(specs, rolls, ctx, 1024, 4242, budget)
    rep["tp"] = trep
    log("TP", trep)
    # two canopy MeshParts (x >= 0 / x < 0), one 1024 map each -> ~2x the leaf texel density
    Vw, _Tw, Nw = obj_arrays(canopy)
    halves = split_faces(canopy, {"CanopyA": lambda f: f.calc_center_median().x >= 0.0, "CanopyB": lambda f: True})
    canA, canB = halves["CanopyA"], halves["CanopyB"]
    from mathutils.kdtree import KDTree
    kd = KDTree(len(Vw))
    for i, v in enumerate(Vw):
        kd.insert(Vector(v.tolist()), i)
    kd.balance()
    for o in (canA, canB):
        rep.setdefault("slivers_removed", {})[o.name] = drop_slivers(o)
        o.data.shade_smooth()
        Vh, _t, _n = obj_arrays(o)
        o.data.normals_split_custom_set_from_vertices([tuple(Nw[kd.find(Vector(v.tolist()))[1]]) for v in Vh])
        smart_uv(o)
    smart_uv(trunk)
    rep["tris"] = {o.name: tri_count(o) for o in (trunk, canA, canB)}
    rep["tris"]["TP"] = trep["tris"]
    rep["tris"]["total"] = sum(rep["tris"].values())
    rep["hi_tris"] = {o.name: tri_count(o) for o in (trunk_hi, base, leaves)}
    rep["hi_tris"]["TPHi"] = trep["hi_tris"]
    rep["bbox"] = bbox_of([trunk, canA, canB] + tp_los)
    save_json(rep, os.path.join(WIP, "tree_build.json"))
    for o in [trunk_hi, base, leaves] + tp_his:
        o.hide_render = True
    bpy.ops.wm.save_as_mainfile(filepath=TREE_BLEND_WIP)
    return rep


''' + src[e:]

# ---------------------------------------------------------------- bush
s = src.index("def bush_specs(")
e = src.index("# ================================================================== bakes", s)
src = src[:s] + r'''def bush_specs(roll_arc_, ground_pt):
    D = lambda az, el: ("dir", az, el)
    arcn = [("pt", tuple(p), tuple(n)) for p, n in roll_arc_]
    na = len(arcn)
    return [
        # from the roll: out from under it, along the soil, up the front and diagonally over the crown
        dict(name="BRoll", nodes=arcn + [("pt", tuple(ground_pt), (0, 0, 1)), D(270, 22), D(296, 64), D(104, 36)],
             spans=["sag:1.0"] * (na - 1) + ["sag:1.02", "sag:1.02", "drape", "drape"],
             pins=[True] * na + [False, False, True, False], tail1=0.95, roll_start=True, tear=(False, True),
             twist=0.16),
        # over one shoulder (not across the crown), both tails ending in the air
        dict(name="BShoulder", nodes=[D(196, 8), D(226, 42), D(330, 40), D(354, 6)], spans=["drape"] * 3,
             pins=[False, True, True, False], tail0=0.95, tail1=1.05, twist=0.16),
        # a loose loop sagging off the back-left side
        dict(name="BLoop", nodes=[D(112, 12), D(166, 4)], spans=["sag:1.3"], pins=[True, True],
             tail0=0.0, tail1=0.55, twist=0.12),
    ]


def build_bush():
    setup_scene()
    q = CFG["quick"]
    rep = {}
    clumps, blobs = bush_clumps(31)
    base, canopy = canopy_parts("Canopy", blobs, 0.06 if q else 0.04, 8, 0.06, 1.3, 8, 7300, 0.05, zfloor=-0.05,
                                lobes=dict(spacing=0.72, rad=(0.36, 0.52), amp=(0.15, 0.24)), drop_bottom=0.12)
    area = mesh_area(base)
    nleaf = int(area * (10 if q else 42))
    log("bush base", len(base.data.polygons), "area", round(area, 1), "leaves", nleaf)
    leaves, _p, _n = scatter_leaves("LeavesHi", base, nleaf,
                                    dict(L=(0.3, 0.42), wk=(0.5, 0.62), tilt=(0.16, 0.48), sink=0.02,
                                         fold=(0.15, 0.35), curl=(-0.04, 0.1), centre=BUSH_CENTRE),
                                    bush_leaf_colours(clumps, (0, 0, 1.6), 3.0, 4.8), 91, skip_bottom=0.12)
    leaves.data.materials.append(mat_vc("LeafHi"))
    nv = len(base.data.vertices)
    set_colors(base.data, "Col", np.tile(L((46, 50, 24)), (nv, 1)))
    set_colors(base.data, "Rough", np.full((nv, 3), 0.95))
    base.data.materials.append(mat_vc("CanopyGapHi"))
    base.name = "CanopyHi"
    col = Colliders(0.035)
    cb = bvh_ob(canopy)
    col.add(cb, 0.075, "canopy")
    # the roll on the soil at the front, clear of the foliage, the paper coming out from under it toward the bush
    ang = math.radians(-82)
    rdir = Vector((math.cos(ang), math.sin(ang), 0))
    rad = 1.6
    while rad < 4.0:
        c = rdir * rad + Vector((0, 0, ROLL["Ro"] + 0.065))
        loc, nr, idx, dist = cb.find_nearest(c, 5.0)
        if (c - loc).dot(nr) > 0 and dist > ROLL["Ro"] + 0.06:
            break
        rad += 0.02
    axis = Vector((-rdir.y, rdir.x, 0)).normalized()
    axis = (Matrix.Rotation(math.radians(-16), 3, "Z") @ axis).normalized()
    axis = Vector((axis.x, axis.y, 0.06)).normalized()          # tipped a little
    e = Vector((-rdir.x, -rdir.y, 0))                            # toward the bush
    e = (e - axis * e.dot(axis)).normalized()
    arc = roll_arc(c, axis, -e, 120.0, -95.0, 0.03, 0.0)         # loose layer over the top + far side, out from under it
    ground_pt = c + e * (ROLL["Ro"] + 0.55) + Vector((0, 0, -c.z + 0.04))
    rep["roll"] = dict(centre=[round(v, 3) for v in c], axis=[round(v, 3) for v in axis], radius_from_axis=round(rad, 3))
    roll_collider(col, [(c, axis)])
    ctx = dict(col=col, centre=BUSH_CENTRE, limbs=[], twigs=[])
    budget = 9950 - tri_count(canopy)
    tp_los, tp_his, done, trep = build_tp(bush_specs(arc, ground_pt), [(c, axis)], ctx, 512, 5151, budget)
    rep["tp"] = trep
    log("TP", trep)
    smart_uv(canopy)
    rep["tris"] = {"Canopy": tri_count(canopy), "TP": trep["tris"]}
    rep["tris"]["total"] = sum(rep["tris"].values())
    rep["hi_tris"] = {o.name: tri_count(o) for o in (base, leaves)}
    rep["hi_tris"]["TPHi"] = trep["hi_tris"]
    rep["bbox"] = bbox_of([canopy] + tp_los)
    save_json(rep, os.path.join(WIP, "bush_build.json"))
    for o in [base, leaves] + tp_his:
        o.hide_render = True
    bpy.ops.wm.save_as_mainfile(filepath=BUSH_BLEND_WIP)
    return rep


''' + src[e:]

# ---------------------------------------------------------------- AO: less crush in the leaf gaps
rep('''    ("CanopyA", ["CanopyHi", "LeavesHi"], ["Trunk", "CanopyB"], 1024, "TPTree_CanopyA", 0.3, 0.62, 0.7, 0.9),
    ("CanopyB", ["CanopyHi", "LeavesHi"], ["Trunk", "CanopyA"], 1024, "TPTree_CanopyB", 0.3, 0.62, 0.7, 0.9),''',
    '''    ("CanopyA", ["CanopyHi", "LeavesHi"], ["Trunk", "CanopyB"], 1024, "TPTree_CanopyA", 0.36, 0.7, 0.45, 0.8),
    ("CanopyB", ["CanopyHi", "LeavesHi"], ["Trunk", "CanopyA"], 1024, "TPTree_CanopyB", 0.36, 0.7, 0.45, 0.8),''')
rep('''    ("Canopy", ["CanopyHi", "LeavesHi"], [], 1024, "TPBush_Canopy", 0.2, 0.5, 0.7, 0.7),''',
    '''    ("Canopy", ["CanopyHi", "LeavesHi"], [], 1024, "TPBush_Canopy", 0.3, 0.6, 0.45, 0.6),''')

# ---------------------------------------------------------------- eye-height review cameras (5 studs, 70 deg vertical)
s = src.index("def render_asset(")
e = src.index("def export_asset(", s)
src = src[:s] + r'''def shoot_eye(path, cam_pos, target, fov_v=70.0):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("Cam")
    cd.sensor_fit = "VERTICAL"
    cd.sensor_height = 24.0
    cd.lens = 12.0 / math.tan(math.radians(fov_v) / 2)
    cd.clip_start = 0.05
    cd.clip_end = 3000
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = Vector(cam_pos)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    return path


def render_asset(which, hi=False):
    final = TREE_BLEND if which == "tree" else BUSH_BLEND
    if hi:
        final = TREE_BLEND_WIP if which == "tree" else BUSH_BLEND_WIP
    bpy.ops.wm.open_mainfile(filepath=final)
    sc = review_setup(res=(1600, 900))
    sc.eevee.taa_render_samples = 48
    for o in bpy.data.objects:
        if o.type == "MESH":
            ishi = o.name.endswith("Hi") or o.name.startswith("TPHi_")
            o.hide_render = (not ishi) if hi else ishi
        if o.type == "MESH":
            for m in o.data.materials:
                if m:
                    m.use_backface_culling = True
    review_ground(8.6 if which == "tree" else 4.2)
    tag = "hi_" if hi else ""
    J = json.load(open(os.path.join(WIP, "%s_build.json" % which)))
    out = []
    E = 5.0
    if which == "tree":
        for side, dv in (("front", (0, -1)), ("back", (0, 1)), ("side", (1, 0)), ("left", (-1, 0))):
            for dist, tz in ((25, 7.0), (45, 6.5)):
                out.append(shoot_eye(os.path.join(OUT, "review_%stree_%s_%d.png" % (tag, side, dist)),
                                     (dv[0] * dist, dv[1] * dist, E), (0, 0, tz)))
        r1 = J["roll_twig"]["centre"]
        r2 = J["roll_fallen"]["centre"]
        out.append(shoot_eye(os.path.join(OUT, "review_%stree_close_twigroll.png" % tag), (r1[0] + 1.0, r1[1] - 8.0, E),
                             (r1[0], r1[1], r1[2] - 0.8), 34))
        out.append(shoot_eye(os.path.join(OUT, "review_%stree_close_fallenroll.png" % tag), (r2[0] - 1.5, r2[1] - 5.5, 3.2),
                             (r2[0] + 0.6, r2[1] + 0.4, 0.3), 34))
        out.append(shoot_eye(os.path.join(OUT, "review_%stree_under_lookup.png" % tag), (2.0, -8.5, E), (0, 0, 10.5)))
        out.append(shoot_eye(os.path.join(OUT, "review_%stree_close_canopy.png" % tag), (3.0, -14.0, E), (0.5, -4.5, 10.5),
                             34))
    else:
        for side, dv in (("front", (0, -1)), ("back", (0, 1)), ("side", (1, 0)), ("left", (-1, 0))):
            out.append(shoot_eye(os.path.join(OUT, "review_%sbush_%s_25.png" % (tag, side)),
                                 (dv[0] * 25, dv[1] * 25, E), (0, 0, 2.6)))
        out.append(shoot_eye(os.path.join(OUT, "review_%sbush_front_45.png" % tag), (0, -45, E), (0, 0, 2.6)))
        r = J["roll"]["centre"]
        out.append(shoot_eye(os.path.join(OUT, "review_%sbush_close.png" % tag), (2.5, -8.0, E), (0, 0, 2.2), 50))
        out.append(shoot_eye(os.path.join(OUT, "review_%sbush_close_roll.png" % tag), (r[0] + 1.6, r[1] - 4.5, 2.6),
                             (r[0] - 0.1, r[1] + 0.6, 0.6), 30))
        out.append(shoot_eye(os.path.join(OUT, "review_%sbush_close_back.png" % tag), (-2.0, 8.0, E), (0, 0, 2.4), 50))
    return out


''' + src[e:]
open("tptree.py", "w", encoding="utf-8").write(src)
print("part C ok")
