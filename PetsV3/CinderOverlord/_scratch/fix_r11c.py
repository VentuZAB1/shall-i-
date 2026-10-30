# Cinder r11 (c): the IDLE redo for the raised cobra stance - the neck no longer leans back on the breath (that drops
# the head toward the game camera); it stands upright and sways side to side (cobra sway, roll), the head held level.
import io
p = r"C:\Users\ventu\OneDrive\Desktop\SLINGSHOT Creatures\PetsV3\pets\CinderOverlord.py"
s = io.open(p, encoding="utf-8").read()
a = s[s.index("def idle(k):"):s.index("def walk(k):")]
b = '''def idle(k):
    """COBRA SWAY (r11, raised cobra stance; refs S2 C1/C2): the reared neck stands upright and sways slowly side to side
    (a lateral roll, 2.2 deg per neck bone, one sway per loop) with the head held level and turning a little into the
    sway; two slow breaths stay small (neck 1 deg per bone, crown and jaw lift) so the head and crown keep their full
    height from the game camera (the r10 idle leaned the neck back 13.5 deg on each breath, which dropped the head
    toward the camera); the vents smoke on each breath; one quick tail flick at f80."""
    n = 120
    k.new_action("idle", n, True)
    flick = [(0, 0), (74, 0), (78, 8), (81, -3), (86, 0), (120, 0)]
    for f in range(0, n + 1, 2):
        br = 0.5 - 0.5 * math.cos(4 * math.pi * f / n)                  # 0 -> 1 -> 0 twice
        sw = sn(f, n)                                                   # one side-to-side sway per loop
        sw_l = sn(f, n, -0.04)                                          # the head follows the neck ~5 f later
        for b in NECK3:
            k.key(b, f, rot=(-1.0 * br, 0.4 * sw, 2.2 * sw))            # pitch (rise), yaw, ROLL (lateral sway)
        k.key("Head", f, rot=(0.8 * br, 3.0 * sw_l, -4.4 * sw_l))      # level: counter-roll most of the 6.6 deg
        k.key("Jaw", f, rot=(2.25 * br, 0, 0))
        rest_chain(k, f, skip=("Tail3", "Tail4"))
        k.key("Tail3", f, rot=(0, 0.4 * curve(flick, f), 0))
        k.key("Tail4", f, rot=(0, curve(flick, f), 0))
        crown(k, f, [(2.25 * br, 0)] * 5)
        arms(k, f, paddle_l=3 * br, paddle_r=3 * br)
    k.finish()
    k.events["idle"] = {"smoke1": round(30 / n, 3), "flick": round(80 / n, 3), "smoke2": round(90 / n, 3)}


'''
s = s.replace(a, b)
io.open(p, "w", encoding="utf-8").write(s)
print("idle replaced")
