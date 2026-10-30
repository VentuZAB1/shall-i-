# Driver for PetsV3 (Steal-an-Egg style blocks), run inside the persistent Blender GUI through MCP:
#   import runpy; R = runpy.run_path(r"...\PetsV3\run3.py"); R["model"]("Raiju") / R["full"]("Raiju") / R["export"]()
# Reuses PetsV2's petkit (rig keys, audit, clip sampling, bake + FBX) and pets/_common (gaits, Flight...).
import sys, os, importlib, importlib.util, json
import bpy

V2 = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV2"
ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3"
for p in (V2, os.path.join(V2, "pets"), ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)
import petkit
importlib.reload(petkit)
petkit.ROOT = ROOT          # renders / exports of V3 pets go to PetsV3\<Name>
pk = petkit
import _common
importlib.reload(_common)
import blockkit
importlib.reload(blockkit)

STATE = {}


def spec(name):
    path = os.path.join(ROOT, "pets", name + ".py")
    sp = importlib.util.spec_from_file_location("pet3_" + name, path)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


def new_pet(m, name):
    from mathutils import Vector
    k = blockkit.BlockPet(name, getattr(m, "DISPLAY", name))
    k.head_xf = [(Vector(x[0]), x[1], set(x[2])) + tuple(x[3:]) for x in getattr(m, "HEAD_XF", [])]
    return k


def model(name, views=("tq", "side", "front", "back"), res=460):
    m = spec(name)
    k = new_pet(m, name)
    info = m.model(k) or {}
    pk.stage(k)
    files = pk.shots(k, "model", views, res)
    tris = sum(len(p.vertices) - 2 for o in k.coll.objects if o.type == "MESH" for p in o.data.polygons)
    STATE["k"], STATE["m"] = k, m
    return {"files": files, "tris": tris, "size": [round(v, 2) for v in (k.bounds()[1] - k.bounds()[0])], **info}


def full(name, pose_picks=None, save=True):
    m = spec(name)
    k = new_pet(m, name)
    m.model(k)
    m.rig(k)
    k.build_rig()
    stride = m.anim(k)
    rep = pk.audit(k)
    data = pk.sample(k)
    lua_bytes = pk.write_clips(k, data, stride)
    pk.stage(k)
    k.set_action("idle")
    bpy.context.scene.frame_set(0)
    STATE["k"], STATE["m"], STATE["stride"] = k, m, stride
    out = {"audit": rep, "stride": round(stride or 0, 4), "lua_bytes": lua_bytes,
           "clips": {c: v for c, v in k.clips.items()}, "events": k.events,
           "tris_body": sum(len(p.vertices) - 2 for p in k.main.data.polygons),
           "tris_glow": {h: sum(len(p.vertices) - 2 for p in g.data.polygons) for h, g in k.glowobjs.items()},
           "bones": [b.name for b in k.arm.data.bones]}
    if pose_picks:
        out["poses"] = pk.pose_renders(k, pose_picks)
    if save:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(k.dir, name + "_rigged.blend"))
    return out


def export():
    k = STATE["k"]
    TH = getattr(getattr(k, "blocks", None), "th", None) or 0.7
    st = getattr(k, "stud", None)
    info = pk.bake_and_export(k, ao_mix=(0.70, 0.30) if st else (0.60, 0.40), ao_dist=0.20 * TH, smooth_type="OFF",
                              stud=st)   # STYLE_BIBLE 2a; stud skin = fierce style 2026-10-09
    info["portrait"] = pk.portrait(k)
    mn, mx = k.bounds()
    bu_now = mx.z - mn.z
    height = getattr(STATE["m"], "HEIGHT", 7.0)          # pro pass: every pet rebuilt -> HEIGHT is the total height
    meta = {"name": k.name, "display": k.display, "motion": getattr(STATE["m"], "MOTION", "Walk"),
            "rig": getattr(STATE["m"], "RIG", "quad"), "height": height,
            "stride": STATE.get("stride") or 0, "walk_len": (k.clips.get("walk", (0, 0))[0] / pk.FPS),
            "glow": list(k.glowobjs.keys()), "lights": getattr(STATE["m"], "LIGHTS", {})}
    with open(os.path.join(k.dir, k.name + "_meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False)
    mn, mx = k.bounds()
    with open(os.path.join(k.dir, k.name + "_bu.json"), "w") as fh:     # Blender-unit size, for WalkSpeed in Studio
        json.dump({"height": mx.z - mn.z, "length": mx.y - mn.y, "width": mx.x - mn.x}, fh)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(k.dir, k.name + "_rigged.blend"))
    info["meta"] = meta
    return info


def gifs(actions=("idle", "walk", "fly")):
    k = STATE["k"]
    out = {}
    for a in actions:
        if a in k.clips:
            n, loop = k.clips[a]
            out[a] = pk.gif_frames(k, a, step=2 if n > 40 else 1, lift=0.6 if a == "fly" else 0.0)
    return out
