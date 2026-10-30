"""Create a separate OBS profile + scene collection "SLINGSHOT Trailer" (the user's own setup is not touched).
Window capture of the Roblox Studio main window (WGC, no cursor) + Application Audio Capture of Studio only."""
import ctypes, ctypes.wintypes as wt, json, os, uuid

APPDATA = os.environ["APPDATA"]
OBS = os.path.join(APPDATA, "obs-studio")
FOOTAGE = r"C:\Users\ventu\Videos\SLINGSHOT_trailer_footage"

# --- find the Studio main window title (exact unicode) ---
user32 = ctypes.windll.user32
titles = []
@ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
def cb(h, _):
    if not user32.IsWindowVisible(h):
        return True
    n = user32.GetWindowTextLengthW(h)
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(h, buf, n + 1)
    if buf.value.endswith("Roblox Studio"):
        cls = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(h, cls, 256)
        titles.append((buf.value, cls.value))
    return True
user32.EnumWindows(cb, 0)
print("studio windows:", titles)
title, cls = titles[0]

def esc(s):  # OBS window string escapes ':' as '#3A'
    return s.replace("#", "#22").replace(":", "#3A")
win = f"{esc(title)}:{esc(cls)}:RobloxStudioBeta.exe"

# --- profile ---
pdir = os.path.join(OBS, "basic", "profiles", "SLINGSHOT_Trailer")
os.makedirs(pdir, exist_ok=True)
fp = FOOTAGE.replace("\\", "\\\\")
ini = f"""[General]
Name=SLINGSHOT Trailer

[Output]
Mode=Simple
FilenameFormatting=take_%CCYY-%MM-%DD_%hh-%mm-%ss

[SimpleOutput]
FilePath={fp}
RecFormat2=mkv
RecQuality=HQ
RecEncoder=amd
RecAudioEncoder=aac
ABitrate=320
RecTracks=1
RecRB=false

[Video]
BaseCX=1920
BaseCY=1080
OutputCX=1920
OutputCY=1080
FPSType=0
FPSCommon=60
ScaleType=bicubic
ColorFormat=NV12
ColorSpace=709
ColorRange=Partial

[Audio]
SampleRate=48000
ChannelSetup=Stereo
"""
with open(os.path.join(pdir, "basic.ini"), "w", encoding="utf-8-sig") as f:
    f.write(ini)

# --- scene collection ---
def src(id_, name, settings):
    return {"prev_ver": 536936449, "name": name, "uuid": str(uuid.uuid4()), "id": id_, "versioned_id": id_,
            "settings": settings, "mixers": 255, "sync": 0, "flags": 0, "volume": 1.0, "balance": 0.5,
            "enabled": True, "muted": False, "push-to-mute": False, "push-to-mute-delay": 0,
            "push-to-talk": False, "push-to-talk-delay": 0, "hotkeys": {}, "deinterlace_mode": 0,
            "deinterlace_field_order": 0, "monitoring_type": 0, "private_settings": {}}
video = src("window_capture", "Studio Window", {"window": win, "method": 2, "priority": 0, "cursor": False,
                                                 "client_area": True, "force_sdr": False})
audio = src("wasapi_process_output_capture", "Studio Audio", {"window": win, "priority": 2})
def item(s, i):
    return {"name": s["name"], "source_uuid": s["uuid"], "visible": True, "locked": False, "rot": 0.0,
            "scale_ref": {"x": 1920.0, "y": 1080.0}, "align": 5, "bounds_type": 0, "bounds_align": 0,
            "bounds_crop": False, "crop_left": 0, "crop_top": 0, "crop_right": 0, "crop_bottom": 0,
            "id": i, "group_item_backup": False, "pos": {"x": 0.0, "y": 0.0}, "pos_rel": {"x": -1.7777777, "y": -1.0},
            "scale": {"x": 1.0, "y": 1.0}, "scale_rel": {"x": 1.0, "y": 1.0}, "bounds": {"x": 0.0, "y": 0.0},
            "bounds_rel": {"x": 0.0, "y": 0.0}, "scale_filter": "disable", "blend_method": "default",
            "blend_type": "normal", "show_transition": {"duration": 0}, "hide_transition": {"duration": 0},
            "private_settings": {}}
scene = src("scene", "Trailer", {"id_counter": 2, "custom_size": False, "items": [item(video, 1), item(audio, 2)]})
coll = {"name": "SLINGSHOT Trailer", "sources": [video, audio, scene], "groups": [],
        "scene_order": [{"name": "Trailer"}], "current_scene": "Trailer", "current_program_scene": "Trailer",
        "current_transition": "Fade", "transition_duration": 300, "transitions": [], "quick_transitions": [],
        "saved_projectors": [], "preview_locked": False, "scaling_enabled": False, "scaling_level": 0,
        "scaling_off_x": 0.0, "scaling_off_y": 0.0, "modules": {}, "resolution": {"x": 1920, "y": 1080}, "version": 2}
with open(os.path.join(OBS, "basic", "scenes", "SLINGSHOT_Trailer.json"), "w", encoding="utf-8") as f:
    json.dump(coll, f, indent=2, ensure_ascii=False)
print("window string:", win)
print("ok")
