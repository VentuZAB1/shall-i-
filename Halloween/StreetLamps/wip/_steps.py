
# ===================================================================== build / bake / web / export / verify
POST_GROUPS = ("column", "feet", "crook", "volute", "bat")
BAKE = {
    "Post": dict(tex="tex_big", ao=(0.55, 0.35), metal=True,
                 groups=[(g, cg) for g, cg in zip(POST_GROUPS, ((0.05, 0.10), (0.04, 0.08), (0.03, 0.07),
                                                                  (0.03, 0.06), (0.05, 0.10)))]),
    "Cage": dict(tex="tex_small", ao=(0.5, 0.2), metal=True,
                 groups=[(g, cg) for g, cg in zip(CAGE_GROUPS, ((0.03, 0.06), (0.03, 0.07), (0.015, 0.04),
                                                                  (0.015, 0.04), (0.03, 0.07)))]),
}


def pumpkin_seams_world():
    loc = pick_seams(PUMP["N"], PUMP["phase"], [48, 32], [25.0, 155.0, 270.0])
    return [round((a + 180.0) % 360.0, 4) for a in loc]


def world_verts(ob):
    me = ob.data
    co = np.empty(len(me.vertices) * 3, np.float32)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    M = np.array(ob.matrix_world)
    return co @ M[:3, :3].T + M[:3, 3]


def bvh_faces(ob, keep_mat=None, drop_mat=None):
    me = ob.data
    V = [ob.matrix_world @ v.co for v in me.vertices]
    F = [tuple(p.vertices) for p in me.polygons
         if (keep_mat is None or p.material_index in keep_mat) and (drop_mat is None or p.material_index not in drop_mat)]
    return BVHTree.FromPolygons(V, F, all_triangles=False)


def nearest(bvh, P):
    best, where = 1e9, None
    for p in P:
        h = bvh.find_nearest(Vector(tuple(float(x) for x in p)))
        if h[0] is not None and h[3] < best:
            best, where = h[3], [round(float(x), 3) for x in p]
    return round(best, 4), where


def rot_about_axis(P, k):
    a = math.radians(90.0 * k)
    c, s_ = math.cos(a), math.sin(a)
    Q = np.asarray(P, float).copy()
    x, y = Q[:, 0] - 0.0, Q[:, 1] - HANG_Y
    Q[:, 0], Q[:, 1] = c * x - s_ * y, HANG_Y + s_ * x + c * y
    return Q


def step_build():
    R = RES()
    fresh(samples=R["samples"])
    A = assemble(True)
    rep = A["rep"]
    pk, H, zc = A["pk"], A["H"], A["zc"]
    ironhi = mat_iron_hi("IronHi")
    # ---- Post
    post = A["post_acc"].build("Post", mats=[bpy.data.materials.new("PostG_" + g) for g in POST_GROUPS])
    triangulate(post)
    pack_uv(post)
    for g in POST_GROUPS:
        A["hi_accs"][g].build("Hi_Post_" + g, mats=[ironhi])
    # ---- Cage
    cage = A["cage_acc"].build("Cage", mats=[bpy.data.materials.new("CageG_" + g) for g in CAGE_GROUPS])
    triangulate(cage)
    pack_uv(cage)
    for g in CAGE_GROUPS:
        A["hi_accs"]["cage"][g].build("Hi_Cage_" + g, mats=[ironhi])
    # ---- Pumpkin lo: shell + stem + candle + wick + puddle -> one object
    lo = join([pk["lo"], pk["stem_lo"], pk["candle_lo"], pk["wick_lo"], pk["puddle_lo"]], "Pumpkin")
    triangulate(lo)
    strip_colors(lo)
    for at in list(lo.data.attributes):
        if at.name == "Depth":
            lo.data.attributes.remove(at)
    seams = pumpkin_seams_world()
    nseam = uv_layout(lo, seams, {"Skin", "Inner"}, {"Inner": 0.55, "WaxMat": 0.6, "WickMat": 0.6},
                      centre_xy=(0.0, HANG_Y))
    rep["pumpkin_uv"] = dict(seams=seams, seam_edges=nseam)
    for k_, nm in (("hi", "Hi_Pumpkin"), ("stem_hi", "Hi_Stem"), ("candle_hi", "Hi_Candle"), ("wick_hi", "Hi_Wick"),
                   ("puddle_hi", "Hi_Puddle")):
        pk[k_].name = nm
    pk["cut"].name = "Cutter"
    pk["cut"].hide_render = True
    pk["cut"].hide_viewport = True
    if pk["repair"][1] != 0:
        raise RuntimeError("repair_attrs left %d vertices" % pk["repair"][1])
    # ---- triangle budgets
    tris = {"Post": len(post.data.polygons), "Cage": len(cage.data.polygons), "Pumpkin": len(lo.data.polygons)}
    rep["tris"] = tris
    log("tris", tris)
    for k_, v in tris.items():
        if v > BUDGET[k_]:
            raise RuntimeError("%s has %d tris > %d" % (k_, v, BUDGET[k_]))
    # ---- texel density
    rep["texel_px_per_stud"] = {o.name: round(texel_density(o, s_)[0], 1)
                                for o, s_ in ((post, R["tex_big"]), (cage, R["tex_small"]), (lo, R["tex_big"]))}
    log("texel", rep["texel_px_per_stud"])
    # ---- clearances
    chk = {}
    zb = rep["pumpkin"]["bottom"]
    skin = world_verts(bpy.data.objects["Hi_Pumpkin"])
    skin = skin[skin[:, 2] > zb + 0.10][::3]
    stem = world_verts(bpy.data.objects["Hi_Stem"])[::2]
    cb = bvh_faces(cage, drop_mat={CAGE_GROUPS.index("seat")})
    for k_ in range(4):
        chk["pumpkin_skin_vs_cage_rot%d" % (90 * k_)] = nearest(cb, rot_about_axis(skin, k_))
        chk["stem_vs_cage_rot%d" % (90 * k_)] = nearest(cb, rot_about_axis(stem, k_))
    pb = bvh_faces(post)
    cv_ = world_verts(cage)
    vm = np.zeros(len(cv_), np.int64)
    for poly in cage.data.polygons:
        vm[list(poly.vertices)] = poly.material_index
    away = cv_[(vm != CAGE_GROUPS.index("ring_l2")) & (vm != CAGE_GROUPS.index("link1"))][::2]
    chk["cage_vs_post"] = nearest(pb, away)
    chk["link1_vs_post"] = nearest(pb, cv_[vm == CAGE_GROUPS.index("link1")])
    O, ra = bat_frame(A["cv"])
    pv = world_verts(post)
    pm = np.zeros(len(pv), np.int64)
    for poly in post.data.polygons:
        pm[list(poly.vertices)] = poly.material_index
    wings = pv[(pm == POST_GROUPS.index("bat")) & (np.abs(pv[:, 1] - O[1]) > 0.16)]
    crb = bvh_faces(post, keep_mat={POST_GROUPS.index("crook")})
    chk["bat_wings_vs_crook"] = nearest(crb, wings)
    rep["clearance"] = chk
    log("clearance", chk)
    bad = [k_ for k_, v in chk.items() if (k_.startswith(("pumpkin", "stem")) and v[0] < 0.30) or
           (k_ == "cage_vs_post" and v[0] < 0.40) or (k_ == "link1_vs_post" and v[0] < 0.004) or
           (k_ == "bat_wings_vs_crook" and v[0] < 0.035)]
    if bad:
        log("CLEARANCE FAIL", bad)
        rep["clearance_fail"] = bad
    # ---- attachment points (Blender object space = world; every object keeps the FBX origin)
    itop, ibot = pk["itop"], pk["ibot"]
    wt = pk["wick_top"]
    att = {
        "wick_tip": [round(v, 3) for v in pk["wick_tip"]],
        "wick_top": [round(v, 3) for v in wt],
        "flame_centre": [round(wt.x, 3), round(wt.y, 3), round(wt.z + 0.05, 3)],
        "cavity_centre": [0.0, HANG_Y, round(zc + 0.5 * (itop + ibot), 3)],
        "cavity_floor": [0.0, HANG_Y, round(zc + ibot, 3)],
        "suggested_pointlight": [round(wt.x, 3), round(wt.y, 3), round(wt.z + 0.06, 3)],
        "ground_light": [0.0, HANG_Y, round(A["cage_info"]["col"][0] - 0.03, 3)],
        "chain_top": [0.0, HANG_Y, round(H["chain_top"], 3)],
        "pumpkin_pivot": [0.0, HANG_Y, round(zc, 3)],
        "bat_perch": [round(float(x), 3) for x in O],
    }
    rep["attach"] = att
    log("attach", att)
    for o in (post, cage, lo):
        o.hide_render = False
    with open(os.path.join(OUT, "build.json"), "w") as fh:
        json.dump(rep, fh, indent=1, default=float)
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    return rep


def _hide_for_bake():
    for o in bpy.context.scene.objects:
        if o.type != "MESH":
            continue
        o.hide_render = not o.name.startswith("Hi_")
    bpy.data.objects["Hi_Pumpkin"].hide_render = True       # its split copies take its place


def step_bake(part):
    R = RES()
    bpy.ops.wm.open_mainfile(filepath=SRC)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = R["samples"]
    lo = bpy.data.objects[part]
    groups, made = [], []
    hp = bpy.data.objects["Hi_Pumpkin"]
    hk = {"Skin": "HiSplit_Skin", "Flesh": "HiSplit_Wall", "Inner": "HiSplit_Inner"}
    hs_ = {v: split_copy(hp, v, (lambda n_: lambda f, nm: nm[f.material_index] == n_)(k)) for k, v in hk.items()}
    his_split = list(hs_.values())
    _hide_for_bake()
    for o in his_split:
        o.hide_render = False
    if part == "Pumpkin":
        defs = [("LoSkin", ("Skin", "StemMat"), [hs_["HiSplit_Skin"], bpy.data.objects["Hi_Stem"]], 0.04, 0.09),
                ("LoWall", ("Flesh",), [hs_["HiSplit_Wall"]], 0.03, 0.07),
                ("LoInner", ("Inner",), [hs_["HiSplit_Inner"]], 0.04, 0.09),
                ("LoWax", ("WaxMat",), [bpy.data.objects["Hi_Candle"], bpy.data.objects["Hi_Puddle"]], 0.035, 0.08),
                ("LoWick", ("WickMat",), [bpy.data.objects["Hi_Wick"]], 0.012, 0.03)]
        for nm, mats, his, cage_, maxray in defs:
            o = split_copy(lo, nm, (lambda ms: lambda f, names: names[f.material_index] in ms)(mats))
            made.append(o)
            groups.append((o, his, cage_, maxray))
        size, ao, metal = R["tex_big"], (0.5, 0.25), False
    else:
        cfg = BAKE[part]
        prefix = "Hi_Post_" if part == "Post" else "Hi_Cage_"
        for gi, (g, (cage_, maxray)) in enumerate(cfg["groups"]):
            o = split_copy(lo, "Lo_" + g, (lambda i: lambda f, names: f.material_index == i)(gi))
            made.append(o)
            groups.append((o, [bpy.data.objects[prefix + g]], cage_, maxray))
        size, ao, metal = R[cfg["tex"]], cfg["ao"], cfg["metal"]
    lo.hide_render = True
    imgs = bake_groups(groups, size, part, ao[0], ao[1], metal=metal)
    for o in made + his_split:
        bpy.data.objects.remove(o)
    lo.hide_render = False
    pbr_material(lo, part + "_PBR", imgs)
    info = dict(part=part, size=size, stats=imgs["stats"],
                albedo_mean_srgb=albedo_mean(os.path.join(MAPS, part + "_albedo.png")))
    log("bake", info)
    with open(os.path.join(OUT, "bake_%s.json" % part.lower()), "w") as fh:
        json.dump(info, fh, indent=1)
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            o.hide_render = o.name.startswith("Hi_") or o.name == "Cutter"
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    return info


def albedo_mean(path):
    img = bpy.data.images.load(path, check_existing=False)
    a = np.empty(img.size[0] * img.size[1] * 4, np.float32)
    img.pixels.foreach_get(a)
    a = a.reshape(-1, 4)[:, :3]
    nz = a[a.sum(1) > 0.003]
    out = [round(float(x) * 255, 1) for x in nz.mean(0)]
    bpy.data.images.remove(img)
    return out


def step_web():
    R = RES()
    bpy.ops.wm.open_mainfile(filepath=SRC)
    for nm in ("Web", "WebSilk"):
        if nm in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[nm])
    cv = crook_design()
    vc = volute_curve(cv)
    H = head_stack(cv)
    web, silk, info = build_web(cv, vc, H)
    ci, ri = strand_maps(R["tex_small"])
    web.data.materials.append(mat_tex("Web_Mat", ci, ri, rough=0.6))
    simg = silk_texture(R["tex_small"], os.path.join(MAPS, "WebSilk_albedo.png"))
    silk.data.materials.append(mat_tex("WebSilk_Mat", simg, None, alpha=True, rough=0.8))
    for o in (web, silk):
        o.visible_shadow = False
    wv = world_verts(web)
    info["tris"] = {"Web": _tris_of_objs([web]), "WebSilk": _tris_of_objs([silk])}
    info["strand_bbox"] = dict(y=[round(float(wv[:, 1].min()), 3), round(float(wv[:, 1].max()), 3)],
                               z=[round(float(wv[:, 2].min()), 3), round(float(wv[:, 2].max()), 3)])
    info["strand_span"] = dict(y=round(float(wv[:, 1].max() - wv[:, 1].min()), 3),
                               z=round(float(wv[:, 2].max() - wv[:, 2].min()), 3))
    cage = bpy.data.objects["Cage"]
    cb = bvh_faces(cage)
    info["web_vs_cage"] = nearest(cb, wv[::2])
    info["silk_vs_cage"] = nearest(cb, world_verts(silk))
    pb = bvh_faces(bpy.data.objects["Pumpkin"])
    info["web_vs_pumpkin"] = nearest(pb, wv[::2])
    log("web", info)
    for nm, lim in (("Web", BUDGET["Web"]), ("WebSilk", BUDGET["WebSilk"])):
        if info["tris"][nm] > lim:
            raise RuntimeError("%s over budget" % nm)
    with open(os.path.join(OUT, "web.json"), "w") as fh:
        json.dump(info, fh, indent=1, default=float)
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    return info


FINAL_NAMES = ("Post", "Cage", "Pumpkin", "Web", "WebSilk")


def step_export():
    bpy.ops.wm.open_mainfile(filepath=SRC)
    objs = [bpy.data.objects[n] for n in FINAL_NAMES]
    for o in objs:
        o.hide_render = False
        o.hide_viewport = False
        o.hide_set(False)
    with open(os.path.join(OUT, "build.json")) as fh:
        rep = json.load(fh)
    with open(os.path.join(OUT, "web.json")) as fh:
        web = json.load(fh)
    tris = {o.name: _tris_of_objs([o]) for o in objs}
    total = sum(tris.values())
    if total > TOTAL_CAP or any(v > 8000 for v in tris.values()):
        raise RuntimeError("budget: %s total %d" % (tris, total))
    allv = np.vstack([world_verts(o) for o in objs])
    pv = world_verts(objs[0])
    base = pv[pv[:, 2] < 1.0]
    sizes = {}
    for o in objs:
        w = world_verts(o)
        mn, mx = w.min(0), w.max(0)
        sizes[o.name] = dict(size=[round(float(x), 3) for x in mx - mn], min=[round(float(x), 3) for x in mn],
                             max=[round(float(x), 3) for x in mx], centre=[round(float(x), 3) for x in (mn + mx) / 2])
    chk = dict(min_z=round(float(allv[:, 2].min()), 4), height=round(float(allv[:, 2].max()), 3),
               footprint=[round(float(base[:, 0].max() - base[:, 0].min()), 3),
                          round(float(base[:, 1].max() - base[:, 1].min()), 3)],
               reach_iron=round(float(-pv[:, 1].min()), 3),
               lowest_head=round(float(world_verts(objs[1])[:, 2].min()), 3))
    if chk["min_z"] < -0.05:
        raise RuntimeError("geometry below the ground: %s" % chk["min_z"])
    if max(chk["footprint"]) > 2.6:
        raise RuntimeError("footprint %s" % chk["footprint"])
    res = export_fbx(objs, FBX)
    out = dict(fbx=FBX, kb=res["kb"], tris=tris, total=total, sizes=sizes, checks=chk, attach=rep["attach"],
               clearance=rep["clearance"], web=web)
    log("export", json.dumps(out, default=float)[:2000])
    with open(os.path.join(OUT, "export.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    bpy.ops.wm.save_as_mainfile(filepath=SRC)
    for o in list(bpy.data.objects):
        if o.name not in FINAL_NAMES:
            bpy.data.objects.remove(o)
    bpy.ops.wm.save_as_mainfile(filepath=FINAL)
    return out


def import_lamp(path=FBX):
    """Import the FBX and bake its 0.01 object scale into the meshes (studs, identity transforms)."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=path)
    objs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    for o in objs:
        M = o.matrix_world.copy()
        o.data.transform(Matrix.Scale(100.0, 4) @ M)
        o.matrix_world = Matrix.Identity(4)
    for o in [o for o in bpy.data.objects if o not in before and o.type != "MESH"]:
        bpy.data.objects.remove(o)
    return {o.name.split(".")[0]: o for o in objs}


def step_verify():
    fresh(4)
    objs = import_lamp()
    rep = {}
    for nm, o in objs.items():
        me = o.data
        imgs = []
        for m in me.materials:
            if m and m.use_nodes:
                for n in m.node_tree.nodes:
                    if n.type == "TEX_IMAGE" and n.image:
                        im = n.image
                        a = np.empty(im.size[0] * im.size[1] * 4, np.float32)
                        im.pixels.foreach_get(a)
                        al = a.reshape(-1, 4)[:, 3]
                        sock = [l.to_socket.name for l in m.node_tree.links if l.from_node == n]
                        imgs.append(dict(name=im.name, size=list(im.size), packed=im.packed_file is not None,
                                         linked_to=sock, alpha=[round(float(al.min()), 3), round(float(al.max()), 3),
                                                                round(float(al.mean()), 3)]))
        w = world_verts(o)
        rep[nm] = dict(tris=_tris_of_objs([o]), images=imgs, min=[round(float(x), 3) for x in w.min(0)],
                       max=[round(float(x), 3) for x in w.max(0)], object_scale_on_import=0.01)
    pk = objs.get("Pumpkin")
    if pk:
        lab = components(pk)
        me = pk.data
        ev = np.empty(len(me.edges) * 2, np.int64)
        me.edges.foreach_get("vertices", ev)
        ev = ev.reshape(-1, 2)
        comps = {}
        for c in np.unique(lab):
            vs = lab == c
            ne = int(vs[ev[:, 0]].sum())
            nf = sum(1 for p in me.polygons if vs[p.vertices[0]])
            comps[int(c)] = (int(vs.sum()), ne, nf)
        big = max(comps.values(), key=lambda t: t[0])
        chi = big[0] - big[1] + big[2]
        rep["pumpkin_shell"] = dict(components=len(comps), euler=chi, holes=(4 - chi) / 2)
    rep["total_tris"] = sum(v["tris"] for k, v in rep.items() if isinstance(v, dict) and "tris" in v)
    log("verify", json.dumps(rep)[:3000])
    with open(os.path.join(OUT, "verify.json"), "w") as fh:
        json.dump(rep, fh, indent=1)
    return rep


# ===================================================================== lighting: night calibration + review
NIGHT_TARGET = {"green": (93, 159, 88), "cream": (184, 177, 185)}
CALIB = os.path.join(OUT, "calib.json")
IN_LIGHT_COL = lin((255, 150, 60))
SPOT_COL = lin((255, 176, 104))


def night_world(sc, L, moon_strength, moon_col, sky_cam=True):
    """World: L lights the scene; camera rays see a dark-blue starry sky. A cool moon sun gives the shadows."""
    w = sc.world
    w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg_l = nt.nodes.new("ShaderNodeBackground")
    bg_l.inputs["Color"].default_value = (*L, 1)
    bg_l.inputs["Strength"].default_value = 1.0
    if sky_cam:
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = 0.0
        ramp.color_ramp.elements[0].color = (*lin((58, 72, 138)), 1)
        ramp.color_ramp.elements[1].position = 0.55
        ramp.color_ramp.elements[1].color = (*lin((16, 22, 62)), 1)
        nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
        vor = nt.nodes.new("ShaderNodeTexVoronoi")
        vor.inputs["Scale"].default_value = 260.0
        nt.links.new(tc.outputs["Generated"], vor.inputs["Vector"])
        st = nt.nodes.new("ShaderNodeMapRange")
        st.inputs["From Min"].default_value = 0.06
        st.inputs["From Max"].default_value = 0.0
        st.inputs["To Max"].default_value = 0.9
        nt.links.new(vor.outputs["Distance"], st.inputs["Value"])
        add = nt.nodes.new("ShaderNodeMix")
        add.data_type = "RGBA"
        add.blend_type = "ADD"
        add.inputs["Factor"].default_value = 1.0
        nt.links.new(ramp.outputs["Color"], add.inputs["A"])
        nt.links.new(st.outputs["Result"], add.inputs["B"])
        bg_s = nt.nodes.new("ShaderNodeBackground")
        nt.links.new(add.outputs["Result"], bg_s.inputs["Color"])
        lp = nt.nodes.new("ShaderNodeLightPath")
        mx = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs["Fac"])
        nt.links.new(bg_l.outputs["Background"], mx.inputs[1])
        nt.links.new(bg_s.outputs["Background"], mx.inputs[2])
        nt.links.new(mx.outputs["Shader"], out.inputs["Surface"])
    else:
        nt.links.new(bg_l.outputs["Background"], out.inputs["Surface"])
    for o in [o for o in sc.objects if o.type == "LIGHT" and o.name.startswith("Sun")]:
        bpy.data.objects.remove(o)
    ld = bpy.data.lights.new("SunMoon", "SUN")
    ld.energy, ld.color = moon_strength, moon_col
    ld.angle = math.radians(1.5)
    mo = link(bpy.data.objects.new("SunMoon", ld))
    mo.rotation_euler = (math.radians(40), 0, math.radians(-35))
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.view_settings.exposure = 0.0
    return mo


def _read_png(path):
    img = bpy.data.images.load(path, check_existing=False)
    a = np.empty(img.size[0] * img.size[1] * 4, np.float32)
    img.pixels.foreach_get(a)
    a = a.reshape(img.size[1], img.size[0], 4)
    bpy.data.images.remove(img)
    return a


def _tolin(v):
    v = np.asarray(v, float) / 255.0
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def step_calib():
    """Fit the night world + moon so a plain green plane and a cream patch render as the in-game Moonlit night
    (green ~ (93,159,88), cream ~ (184,177,185) sRGB)."""
    sc = fresh(8)
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.dither_intensity = 0.0
    sc.render.resolution_x, sc.render.resolution_y = 64, 32
    gm = mat_flat("G", lin(GREEN), rough=0.9)
    cm = mat_flat("C", lin(CREAM), rough=0.9)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(-0.5, 0, 0))
    bpy.context.active_object.data.materials.append(gm)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0.5, 0, 0))
    bpy.context.active_object.data.materials.append(cm)
    cd = bpy.data.cameras.new("Cam")
    cd.type = "ORTHO"
    cd.ortho_scale = 2.0
    cam = link(bpy.data.objects.new("Cam", cd))
    cam.location = (0, 0, 5)
    sc.camera = cam
    E = np.array([0.60, 0.60, 0.70])
    moon_col = np.array([0.80, 0.86, 1.0])
    moon_frac = 0.38
    cosz = math.cos(math.radians(40))
    hist = []

    def setup(E):
        L = E * (1 - moon_frac)
        S = float((E * moon_frac)[2] * math.pi / (moon_col[2] * cosz))
        mcol = (E * moon_frac) * math.pi / (S * cosz)
        return L, S, mcol
    for it in range(5):
        L, S, mcol = setup(E)
        night_world(sc, tuple(L), S, tuple(np.clip(mcol, 0, 10)), sky_cam=False)
        path = os.path.join(WIP, "calib_%d.png" % it)
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        a = _read_png(path)
        gpx = a[8:24, 6:26, :3].reshape(-1, 3).mean(0)
        cpx = a[8:24, 38:58, :3].reshape(-1, 3).mean(0)
        meas = {"green": [round(float(x) * 255, 1) for x in gpx], "cream": [round(float(x) * 255, 1) for x in cpx]}
        hist.append(dict(E=[round(float(x), 4) for x in E], measured=meas))
        log("calib", it, hist[-1])
        rg = _tolin(NIGHT_TARGET["green"]) / np.maximum(_tolin(meas["green"]), 1e-4)
        rc = _tolin(NIGHT_TARGET["cream"]) / np.maximum(_tolin(meas["cream"]), 1e-4)
        E = E * np.sqrt(rg * rc)
    L, S, mcol = setup(E)
    final = dict(E=[float(x) for x in E], moon_frac=moon_frac, moon_col=[float(x) for x in moon_col], history=hist,
                 target=NIGHT_TARGET, albedo_green=GREEN, albedo_cream=CREAM, world_L=[float(x) for x in L],
                 moon_strength=S, moon_rgb=[float(x) for x in mcol])
    with open(CALIB, "w") as fh:
        json.dump(final, fh, indent=1)
    return final


def apply_night(sc, darker=1.0):
    with open(CALIB) as fh:
        cal = json.load(fh)
    L = np.array(cal["world_L"]) * darker
    night_world(sc, tuple(L), cal["moon_strength"] * darker, tuple(cal["moon_rgb"]))
    sc.render.engine = "BLENDER_EEVEE"


def lamp_lights(att, energy_in, energy_spot, offset=(0, 0, 0), rot_k=0):
    off = Vector(offset)
    pl = Vector(att["suggested_pointlight"])
    ft = Vector(att["flame_centre"])
    if rot_k:
        pl = Vector(rot_about_axis(np.array([tuple(pl)]), rot_k)[0])
        ft = Vector(rot_about_axis(np.array([tuple(ft)]), rot_k)[0])
    out = [point("InLight", pl + off, energy_in, col=IN_LIGHT_COL, radius=0.06, shadow=True),
           spot("GroundSpot", Vector(att["ground_light"]) + off, energy_spot, 110.0, SPOT_COL, blend=0.75),
           flame("Flame", ft + off + Vector((0, 0, 0.02)), 0.05, 0.13, 30.0)]
    return out


def rotate_pumpkin(ob, k):
    a = math.radians(90.0 * k)
    M = Matrix.Translation((0, HANG_Y, 0)) @ Matrix.Rotation(a, 4, "Z") @ Matrix.Translation((0, -HANG_Y, 0))
    ob.matrix_world = M @ ob.matrix_world


def review_scene(night, energy_in, energy_spot, darker=1.0):
    sc = fresh(16)
    review_setup(res=(1600, 1200))
    sc.eevee.taa_render_samples = 64
    objs = import_lamp()
    for o in objs.values():
        for m in o.data.materials:
            if m:
                m.use_backface_culling = True
    for m in objs["WebSilk"].data.materials:
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    for nm in ("Web", "WebSilk"):
        objs[nm].visible_shadow = False
    ground(sc)
    if night:
        apply_night(sc, darker)
    with open(os.path.join(OUT, "build.json")) as fh:
        att = json.load(fh)["attach"]
    lamp_lights(att, energy_in, energy_spot)
    return sc, objs, att


def _turn_lamp_lights(sc, k):
    for o in [o for o in sc.objects if o.name.startswith(("InLight", "Flame"))]:
        o.location = Vector(rot_about_axis(np.array([tuple(o.location)]), k)[0])


def shots_lamp(sc, objs, night):
    tgt = Vector((0, -1.8, 9.0))
    head = Vector((0, HANG_Y, 13.6))
    out = []
    tag = "night" if night else "day"
    out.append(shoot_fov(os.path.join(OUT, "review_%s_25.png" % tag), _cam(tgt, (-0.57, -0.82), 25), tgt))
    out.append(shoot_fov(os.path.join(OUT if not night else WIP, "review_%s_25_side.png" % tag), _cam(tgt, (1, 0), 25),
                         tgt))
    if not night:
        out.append(shoot_fov(os.path.join(OUT, "review_day_50.png"), _cam(tgt, (-0.57, -0.82), 50), tgt))
        out.append(shoot_fov(os.path.join(WIP, "rv_day_40_front.png"), _cam(tgt, (0, -1), 40), tgt))
        out.append(shoot_fov(os.path.join(WIP, "rv_day_40_side.png"), _cam(tgt, (1, 0), 40), tgt))
        out.append(shoot_fov(os.path.join(WIP, "rv_day_25_back.png"), _cam(tgt, (0.3, 1), 25), tgt))
        out.append(shoot_fov(os.path.join(OUT, "review_close_head.png"), head + Vector((-3.4, -5.6, -1.8)), head, lens=50))
        out.append(shoot_fov(os.path.join(WIP, "rv_head_below12.png"), Vector((1.5, HANG_Y - 11.0, 5.0)), head))
        out.append(shoot_fov(os.path.join(WIP, "rv_base_5.png"), Vector((-2.6, -4.2, 3.2)), Vector((0, 0, 1.1)), lens=40))
        crook = Vector((0, -1.9, 16.4))
        out.append(shoot_fov(os.path.join(WIP, "rv_crook_8.png"), crook + Vector((8.0, -0.5, -1.5)), crook, lens=45))
        out.append(shoot_fov(os.path.join(WIP, "rv_twist_4.png"), Vector((2.4, -3.0, 7.0)), Vector((0, 0, 7.2)), lens=45))
    else:
        out.append(shoot_fov(os.path.join(OUT, "review_night_close.png"), head + Vector((-3.4, -5.6, -1.8)), head,
                             lens=50))
    rotate_pumpkin(objs["Pumpkin"], 1)
    _turn_lamp_lights(sc, 1)
    out.append(shoot_fov(os.path.join(OUT, "review_%s_25_side_face.png" % tag), _cam(tgt, (1, 0), 25), tgt))
    out.append(shoot_fov(os.path.join(WIP, "rv_%s_head_side_face.png" % tag), head + Vector((7.0, -1.0, -1.6)), head,
                         lens=50))
    rotate_pumpkin(objs["Pumpkin"], -1)
    _turn_lamp_lights(sc, -1)
    return out


def path_of_lamps(sc, objs, att, energy_in, energy_spot, tag):
    """3 lamps 16 studs apart along the path, faces turned along the path toward the camera (+X)."""
    rotate_pumpkin(objs["Pumpkin"], 1)
    for o in [o for o in sc.objects if o.name.startswith(("InLight", "Flame", "GroundSpot"))]:
        bpy.data.objects.remove(o)
    for dx in (-16.0, 0.0, 16.0):
        if dx != 0.0:
            for nm, o in objs.items():
                c = o.copy()
                link(c)
                c.matrix_world = Matrix.Translation((dx, 0, 0)) @ o.matrix_world
        lamp_lights(att, energy_in, energy_spot, offset=(dx, 0, 0), rot_k=1)
    cam = Vector((44.0, -5.25, 5.0))
    tgt = Vector((0.0, -3.0, 9.0))
    return shoot_fov(os.path.join(OUT, "review_%s_path_3lamps.png" % tag), cam, tgt)


LIGHT_E = dict(inside=40.0, spot=700.0)


def step_review(which="all"):
    outs = []
    E_IN, E_SPOT = LIGHT_E["inside"], LIGHT_E["spot"]
    if which in ("all", "day"):
        sc, objs, att = review_scene(False, E_IN, E_SPOT)
        outs += shots_lamp(sc, objs, False)
        outs.append(path_of_lamps(sc, objs, att, E_IN, E_SPOT, "day"))
    if which in ("all", "night"):
        sc, objs, att = review_scene(True, E_IN, E_SPOT)
        outs += shots_lamp(sc, objs, True)
        outs.append(path_of_lamps(sc, objs, att, E_IN, E_SPOT, "night"))
        sc, objs, att = review_scene(True, E_IN, E_SPOT, darker=0.35)
        tgt = Vector((0, -1.8, 9.0))
        outs.append(shoot_fov(os.path.join(WIP, "rv_night_dark_variant_25.png"), _cam(tgt, (-0.57, -0.82), 25), tgt))
    log("review", outs)
    return outs


