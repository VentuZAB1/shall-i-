import os
D = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(D, "..", "bushes.py")
s = open(p, encoding="utf-8").read()
new = open(os.path.join(D, "thorn_v2.py"), encoding="utf-8").read()
a = s.index("# ================================================================== BUSH_THORN")
b = s.index("# ================================================================== BUSH_AUTUMN")
new += '''def bez(p0, p1, p2, p3, t):
    a = 1 - t
    return p0 * (a * a * a) + p1 * (3 * a * a * t) + p2 * (3 * a * t * t) + p3 * (t * t * t)


'''
s = s[:a] + new + s[b:]


def rep(x, y, n=1):
    global s
    c = s.count(x)
    assert c == n, (c, x[:80])
    s = s.replace(x, y)


rep("    for c, r, sq in clump_balls(B, seed):",
    "    for c, r, sq in (lobe_balls(B, seed) if \"lobe_list\" in B else clump_balls(B, seed)):")
rep("    base, dust = srgb((218, 220, 228)), srgb((180, 174, 166))",
    "    base, dust = srgb((208, 210, 218)), srgb((176, 170, 162))")
rep('''    dust = np.clip((mnoise(size, 6.0, 77, 3) - 0.5) * 2.0, 0, 1) * 0.35''',
    '''    dust = np.clip((mnoise(size // 4, 1.5, 77, 3) - 0.5) * 2.0, 0, 1) * 0.35
    dust = np.repeat(np.repeat(dust, 4, 0), 4, 1)''')
# eye-height check renders (mirror the reviewer's player cameras), into wip/
a = s.index("def load_objs(")
eye = '''def cam_eye(target, dist, yaw_deg=0.0, eye=5.0, fov=70.0, lens=None):
    sc = bpy.context.scene
    cd = bpy.data.cameras.new("Cam")
    cam = link(bpy.data.objects.new("Cam", cd))
    yaw = math.radians(yaw_deg)
    t = Vector(target)
    cam.location = Vector((t.x + math.sin(yaw) * dist, t.y - math.cos(yaw) * dist, eye))
    cam.rotation_euler = (t - cam.location).to_track_quat("-Z", "Y").to_euler()
    if lens:
        cd.lens = lens
    else:
        cd.sensor_fit = "VERTICAL"
        cd.angle_y = math.radians(fov)
    cd.clip_end = 5000
    sc.camera = cam
    return cam


def snap(path, cam, res=(1400, 1000)):
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(cam)
    return path


def eyecheck(key):
    """Player-eye views like the reviewer: eye 5 studs up, 40 studs away through a 150 mm lens (front + back), a
    25-stud 70-degree frame, low close-up, and flat black silhouettes (webs hidden) from 0 / 90 / 200 degrees."""
    bpy.ops.wm.open_mainfile(filepath=blend_path(key))
    sc = review_scene()
    ground_set()
    for m in bpy.data.materials:
        m.use_backface_culling = True
        try:
            m.surface_render_method = "DITHERED"
        except Exception:
            pass
    h = 2.6 if key != "bramble" else 1.6
    pre = os.path.join(WIP, "eye_%s" % key)
    out = []
    for yaw, tag in ((0, "front"), (150, "back"), (240, "left")):
        out.append(snap(pre + "_40_%s.png" % tag, cam_eye((1.2, 0, h), 40, yaw, lens=150)))
    out.append(snap(pre + "_25_frame.png", cam_eye((0, 0, 2.5), 25), res=(1920, 1080)))
    out.append(snap(pre + "_close_low.png", cam_eye((0, 0, h * 0.55), 11, 10, eye=h * 0.55 + 0.7, lens=50)))
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type, sh.single_color = "FLAT", "SINGLE", (0, 0, 0)
    sh.show_backface_culling = True
    sc.world.color = (1, 1, 1)
    for o in bpy.data.objects:
        if o.name.startswith(("Ground", "Bed", "Web")):
            o.hide_render = True
    for yaw in (0, 90, 200):
        d3 = Vector((math.sin(math.radians(yaw)), -math.cos(math.radians(yaw)), 0.18)).normalized()
        cd = bpy.data.cameras.new("Cam")
        cam = link(bpy.data.objects.new("Cam", cd))
        cam.location = Vector((0, 0, h)) + d3 * (12 if key != "bramble" else 8.5)
        cam.rotation_euler = (Vector((0, 0, h)) - cam.location).to_track_quat("-Z", "Y").to_euler()
        cd.lens = 50
        sc.camera = cam
        out.append(snap(pre + "_sil_%d.png" % yaw, cam, res=(1000, 800)))
    return out


'''
s = s[:a] + eye + s[a:]
rep('''        elif st == "render":''', '''        elif st == "eye":
            i += 1
            rep["eye"] = eyecheck(argv[i])
        elif st == "render":''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
