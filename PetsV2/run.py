# Driver for PetsV2 (run inside the persistent Blender GUI through MCP):
#   import runpy; R = runpy.run_path(r"...\PetsV2\run.py"); R["model"]("Ivonrath") / R["full"]("Ivonrath") / R["export"]()
import sys, os, importlib, importlib.util, json, traceback
import bpy

ROOT = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV2"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import petkit
importlib.reload(petkit)
pk = petkit
PETS = os.path.join(ROOT, "pets")
if PETS not in sys.path:
    sys.path.insert(0, PETS)
import _common
importlib.reload(_common)

STATE = {}


def spec(name):
    path = os.path.join(ROOT, "pets", name + ".py")
    sp = importlib.util.spec_from_file_location("pet_" + name, path)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod


def model(name, views=("tq", "side", "front", "back"), res=420):
    m = spec(name)
    k = pk.Pet(name, getattr(m, "DISPLAY", name))
    m.model(k)
    pk.stage(k)
    files = pk.shots(k, "model", views, res)
    tris = sum(len(p.vertices) - 2 for o in k.coll.objects if o.type == "MESH" for p in o.data.polygons)
    STATE["k"], STATE["m"] = k, m
    return {"files": files, "tris": tris, "size": [round(v, 2) for v in (k.bounds()[1] - k.bounds()[0])]}


def full(name, pose_picks=None, save=True):
    m = spec(name)
    k = pk.Pet(name, getattr(m, "DISPLAY", name))
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
    info = pk.bake_and_export(k)
    info["portrait"] = pk.portrait(k)
    meta = {"name": k.name, "display": k.display, "motion": getattr(STATE["m"], "MOTION", "Walk"),
            "rig": getattr(STATE["m"], "RIG", "quad"), "height": getattr(STATE["m"], "HEIGHT", 7.0),
            "stride": STATE.get("stride") or 0, "walk_len": (k.clips.get("walk", (0, 0))[0] / pk.FPS),
            "glow": list(k.glowobjs.keys()), "lights": getattr(STATE["m"], "LIGHTS", {})}
    with open(os.path.join(k.dir, k.name + "_meta.json"), "w") as fh:
        json.dump(meta, fh)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(k.dir, k.name + "_rigged.blend"))
    info["meta"] = meta
    return info


def gifs(actions=("idle", "walk", "fly")):
    k = STATE["k"]
    out = {}
    for a in actions:
        if a in k.clips:
            n, loop = k.clips[a]
            lift = 0.6 if a in ("fly",) else 0.0
            out[a] = pk.gif_frames(k, a, step=2 if n > 40 else 1, lift=lift)
    return out
