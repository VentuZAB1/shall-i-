"""Temporarily enlarge the Roblox Studio main window (owner-approved 2026-10-15) and restore it.
usage: studio_window.py info | size W H [X Y] | restore"""
import ctypes, ctypes.wintypes as wt, json, os, sys
user32 = ctypes.windll.user32
SAVE = os.path.join(os.path.dirname(__file__), "studio_placement.json")

class WINDOWPLACEMENT(ctypes.Structure):
    _fields_ = [("length", wt.UINT), ("flags", wt.UINT), ("showCmd", wt.UINT), ("ptMinPosition", wt.POINT),
                ("ptMaxPosition", wt.POINT), ("rcNormalPosition", wt.RECT)]

def studio():
    found = []
    @ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
    def cb(h, _):
        if user32.IsWindowVisible(h):
            n = user32.GetWindowTextLengthW(h); b = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(h, b, n + 1)
            if b.value.endswith("- Roblox Studio"):
                found.append(h)
        return True
    user32.EnumWindows(cb, 0)
    return found[0]

def rects(h):
    r = wt.RECT(); user32.GetWindowRect(h, ctypes.byref(r))
    c = wt.RECT(); user32.GetClientRect(h, ctypes.byref(c))
    return (r.left, r.top, r.right - r.left, r.bottom - r.top), (c.right, c.bottom)

h = studio()
cmd = sys.argv[1]
if cmd == "info":
    print("window", *rects(h), "zoomed", bool(user32.IsZoomed(h)))
elif cmd == "size":
    if not os.path.exists(SAVE):
        wp = WINDOWPLACEMENT(); wp.length = ctypes.sizeof(wp); user32.GetWindowPlacement(h, ctypes.byref(wp))
        r = wp.rcNormalPosition
        json.dump({"showCmd": wp.showCmd, "flags": wp.flags, "normal": [r.left, r.top, r.right, r.bottom],
                   "max": [wp.ptMaxPosition.x, wp.ptMaxPosition.y], "min": [wp.ptMinPosition.x, wp.ptMinPosition.y]},
                  open(SAVE, "w"))
        print("saved placement", open(SAVE).read())
    w, hh = int(sys.argv[2]), int(sys.argv[3])
    x = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    y = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    if user32.IsZoomed(h):
        user32.ShowWindow(h, 9)  # SW_RESTORE
    user32.SetWindowPos(h, 0, x, y, w, hh, 0x0004 | 0x0010)  # NOZORDER | NOACTIVATE
    print("now", *rects(h))
elif cmd == "restore":
    d = json.load(open(SAVE))
    wp = WINDOWPLACEMENT(); wp.length = ctypes.sizeof(wp)
    wp.flags = d["flags"]; wp.showCmd = d["showCmd"]
    wp.ptMinPosition = wt.POINT(*d["min"]); wp.ptMaxPosition = wt.POINT(*d["max"])
    wp.rcNormalPosition = wt.RECT(*d["normal"])
    user32.SetWindowPlacement(h, ctypes.byref(wp))
    if d["showCmd"] == 3:
        user32.ShowWindow(h, 3)  # SW_MAXIMIZE
    print("restored", *rects(h), "zoomed", bool(user32.IsZoomed(h)))
    os.remove(SAVE)
elif cmd == "remax":
    user32.ShowWindow(h, 9)
    import time; time.sleep(0.5)
    user32.ShowWindow(h, 3); time.sleep(0.8)
    print("remax", *rects(h), "zoomed", bool(user32.IsZoomed(h)))
