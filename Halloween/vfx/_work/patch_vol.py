p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\Halloween\vfx.py"
s = open(p, encoding="utf-8").read()

old_how = s[s.index("# How: every texture"):s.index("# Flipbooks: one 2x2-unit tile")]
new_how = '''# How (two kinds, both Cycles CPU + OSL shaders in Halloween\\vfx\\osl\\*.osl with common.h prepended, orthographic camera):
#  "flat"   (flames, glow, ember): an emission shader on one plane that covers the whole atlas, no denoise, many AA
#           samples. Two passes: mode 0 = the straight colour (defined everywhere, so filtered edges never go dark),
#           mode 1 = the alpha. Colour values are authored in sRGB 0-1 and stored as-is.
#  "volume" (smoke, mist): an OSL density field inside a 2x2x2 cube (Principled Volume), lit by a sun + sky ambient
#           (real self-shadowing), film transparent, one render per frame. The premultiplied linear result is
#           un-premultiplied (colour dilated into the transparent pixels), sRGB-encoded and packed.
# All passes go through 32-bit EXR and are packed into one RGBA PNG.
'''
s = s.replace(old_how, new_how)

s = s.replace('''    "smoke": dict(osl="smoke.osl", out="SmokeWisp_4x4.png", cols=4, px=256, samples=48),''',
'''    "smoke": dict(osl="smoke_vol.osl", out="SmokeWisp_4x4.png", cols=4, px=256, samples=256, kind="volume",
                  sun=(3.0, (-40, -30, 0)), sky=((0.55, 0.60, 0.70), 0.5), step_rate=1.0),''')
s = s.replace('''    "mist": dict(osl="mist.osl", out="Mist.png", cols=1, px=512, samples=48),''',
'''    "mist": dict(osl="mist.osl", out="Mist.png", cols=1, px=512, samples=48),
    "mistvol": dict(osl="mist_vol.osl", out="Mist.png", cols=1, px=512, samples=128, kind="volume",
                    sun=(2.5, (-55, -20, 0)), sky=((0.75, 0.78, 0.88), 0.9), step_rate=1.0),''')

vol_code = '''

# ------------------------------------------------------------------ volume kind (smoke, mist)
def setup_volume(px, samples, sun, sky, step_rate):
    import math
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.shading_system = True
    sc.cycles.samples = samples
    sc.cycles.use_denoising = False
    sc.cycles.use_adaptive_sampling = False
    sc.cycles.max_bounces = 1
    sc.cycles.volume_bounces = 1
    sc.cycles.volume_step_rate = step_rate
    sc.cycles.filter_width = 1.2
    sc.render.resolution_x = sc.render.resolution_y = px
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.view_settings.view_transform = "Standard"
    w = bpy.data.worlds.new("W")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = (*sky[0], 1.0)
    bg.inputs["Strength"].default_value = sky[1]
    ld = bpy.data.lights.new("Sun", "SUN")
    ld.energy = sun[0]
    ld.angle = math.radians(8)
    lo = bpy.data.objects.new("Sun", ld)
    sc.collection.objects.link(lo)
    lo.rotation_euler = tuple(math.radians(a) for a in sun[1])
    me = bpy.data.meshes.new("Domain")
    v = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    f = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me.from_pydata(v, [], f)
    me.update()
    dom = bpy.data.objects.new("Domain", me)
    sc.collection.objects.link(dom)
    cd = bpy.data.cameras.new("Cam")
    cd.type = "ORTHO"
    cd.ortho_scale = 2.0
    cam = bpy.data.objects.new("Cam", cd)
    cam.location = (0, 0, 10)
    sc.collection.objects.link(cam)
    sc.camera = cam
    ims = sc.render.image_settings
    ims.file_format = "OPEN_EXR"
    ims.color_depth = "32"
    ims.color_mode = "RGBA"
    return sc, dom


def volume_material(dom, fname, frames):
    mat = bpy.data.materials.new("VOL_" + fname)
    mat.use_nodes = True
    nt = mat.node_tree
    out = None
    for n in list(nt.nodes):
        if n.type == "OUTPUT_MATERIAL":
            out = n
        else:
            nt.nodes.remove(n)
    sn = nt.nodes.new("ShaderNodeScript")
    sn.mode = "INTERNAL"
    sn.script = osl_text(fname)
    if "Density" not in sn.outputs:
        raise RuntimeError("OSL compile failed for " + fname + " (see the log above)")
    if "frames" in sn.inputs:
        sn.inputs["frames"].default_value = frames
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    nt.links.new(sn.outputs["Density"], pv.inputs["Density"])
    nt.links.new(sn.outputs["Albedo"], pv.inputs["Color"])
    nt.links.new(pv.outputs[0], out.inputs["Volume"])
    dom.data.materials.append(mat)
    return sn


def box_blur(a, r, axis):
    pad = [(r + 1, r) if i == axis else (0, 0) for i in range(a.ndim)]
    c = np.cumsum(np.pad(a, pad, mode="edge"), axis=axis)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2 * r + 1, 2 * r + 1 + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return (hi - lo) / (2 * r + 1)


def blur(a, r):
    for _ in range(3):
        a = box_blur(box_blur(a, r, 0), r, 1)
    return a


def srgb_encode(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def unpremultiply(pm):
    """premultiplied linear RGBA (one frame) -> straight sRGB RGBA; colour dilated into (near-)transparent pixels."""
    a = pm[..., 3]
    rgb = pm[..., :3] / np.maximum(a, 1e-6)[..., None]
    br = blur(pm[..., :3], 6)
    ba = blur(a, 6)
    dil = br / np.maximum(ba, 1e-6)[..., None]
    mean = pm[..., :3].sum((0, 1)) / a.sum() if a.sum() > 0 else np.zeros(3, np.float32)
    dil = np.where((ba > 1e-4)[..., None], dil, mean)
    w = np.clip((a - 0.01) / 0.05, 0.0, 1.0)[..., None]
    out = np.empty_like(pm)
    out[..., :3] = srgb_encode(rgb * w + dil * (1 - w))
    out[..., 3] = np.clip(a, 0.0, 1.0)
    return out


def build_volume(key, sp):
    t0 = time.time()
    cols, px = sp["cols"], sp["px"]
    n = cols * cols
    sc, dom = setup_volume(px, sp["samples"], sp["sun"], sp["sky"], sp["step_rate"])
    sn = volume_material(dom, sp["osl"], n)
    stem = os.path.splitext(sp["out"])[0]
    atlas = np.zeros((cols * px, cols * px, 4), np.float32)          # top row first
    for i in range(n):
        if "frame" in sn.inputs:
            sn.inputs["frame"].default_value = i
        path = os.path.join(WORK, f"{stem}_f{i:02d}.exr")
        sc.render.filepath = path
        bpy.ops.render.render(write_still=True)
        img = bpy.data.images.load(path)
        a = np.empty(px * px * 4, np.float32)
        img.pixels.foreach_get(a)
        bpy.data.images.remove(img)
        fr = unpremultiply(a.reshape(px, px, 4))[::-1]
        r, c = divmod(i, cols)
        atlas[r * px:(r + 1) * px, c * px:(c + 1) * px] = fr
    atlas[..., 3][atlas[..., 3] < 0.5 / 255.0] = 0.0
    out = os.path.join(VFX_DIR, sp["out"])
    save_rgba(atlas[::-1], out)
    st = stats(atlas, cols, px)
    st["seconds"] = round(time.time() - t0, 1)
    st["file"] = out
    return st
'''
anchor = '''

def build(key):
    sp = SPECS[key]
    t0 = time.time()'''
assert anchor in s
s = s.replace(anchor, vol_code + '''

def build(key):
    sp = SPECS[key]
    if sp.get("kind") == "volume":
        return build_volume(key, sp)
    t0 = time.time()''')
old_keys = '''    keys = list(SPECS) if "all" in argv else [k for k in argv if k in SPECS]'''
assert old_keys in s
s = s.replace(old_keys, '''    keys = ["candle", "tongue", "smoke", "glow", "ember", "mistvol"] if "all" in argv else \\
        [k for k in argv if k in SPECS]''')
open(p, "w", encoding="utf-8").write(s)
print("patched")
