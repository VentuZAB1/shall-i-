p = "pets/EclipseSeraph.py"
s = open(p, encoding="utf-8").read()
a0 = s.index("def feather(B, root, tip")
a1 = s.index("def eye(B, c, s, yaw=20")
new = '''def feather(B, root, tip, nrm, width, thick, color, bone, taper=0.24, tipc=None, tipf=0.30, studs=False, bev=0.004):
    """flat tapered feather in the wing plane; tipc = a coloured pointed tip over the last tipf of the length.
    bev <= 0.004 = an unbevelled 12-tri blade (dense six-wing budget), > 0.004 = a bevelled one"""
    root, tip = Vector(root), Vector(tip)
    R = frame(tip - root, nrm)
    L = (tip - root).length
    kw = dict(role="limb", bevel=max(bev, 0.007)) if studs else dict(role="limb", bevel=bev, nostud=True, studs=[])
    if not tipc:
        return B.add((root + tip) / 2, (thick / 2, width / 2, L / 2), color, bone, R=R, top=(1.0, taper), **kw)
    m = root.lerp(tip, 1 - tipf)
    w1 = 1.0 - (1.0 - taper) * (1 - tipf)
    B.add((root + m) / 2, (thick / 2, width / 2, (m - root).length / 2 + 0.004), color, bone, R=R, top=(1.0, w1), **kw)
    d = (tip - root).normalized()
    B.add((m + tip) / 2 - d * 0.004, (thick / 2 + 0.0015, width * w1 / 2, (tip - m).length / 2 + 0.004), tipc, bone,
          R=R, top=(1.0, taper / w1), role="limb", bevel=bev, nostud=True, studs=[])
    return tip


WSPEC = {   # pair: (size, coverts, secondaries, primaries, flight-feather width, bevel)
    "A": (1.0, 6, 8, 7, 0.30, 0.006),
    "B": (0.82, 5, 6, 6, 0.27, 0.004),
    "C": (0.62, 4, 4, 4, 0.21, 0.004)}


def angel_wing(B, P, s, side, rows3):
    """dense feather wing: MOON_IVORY arm bar (studded) + wrist + hand bar; a covert row (MOON_IVORY studded on the
    upper pair, WING_IN on the others); secondaries hanging back to the hinge line (IVORY_D on the upper pair, WING_IN
    on the others); primaries fanned densely from the wrist on the hand bone; every flight feather tipped OBSID"""
    wg, h2, tp = WINGS[P]
    S0, W, H, bb, T = X(wg.S, s), X(wg.W, s), X(h2, s), X(wg.BB, s), X(tp, s)
    wb, tb = "Wing_%s_%s" % (P, side), "WingTip_%s_%s" % (P, side)
    nrm = (T - W).cross(H - W).normalized()
    if nrm.z < 0:
        nrm = -nrm
    pl = lambda p: Vector(p) - nrm * (Vector(p) - W).dot(nrm)
    S, H, bb = pl(S0), pl(H), pl(bb)
    sz, n_cov, n_sec, n_pri, fw, bev = WSPEC[P]
    aw = 0.062 * sz + 0.01
    B.seg(S0, W, aw, aw * 1.4, MOON_IVORY, wb, side=nrm, ext=0.05, role="limb", top=(0.82, 0.8))
    B.add(W, (aw * 0.9, aw * 1.1, aw * 1.1), MOON_IVORY, wb, R=frame(W - S, nrm), role="limb")
    B.seg(W + nrm * 0.03, W.lerp(T, 0.25) + nrm * 0.03, aw * 0.5, aw * 0.75, MOON_IVORY, tb, side=nrm, role="limb",
          top=(0.7, 0.7))
    for i in range(n_sec):                                   # secondaries: arm -> hinge line, OBSID tips
        t = (i + 0.5) / n_sec
        a = S.lerp(W, 0.04 + 0.92 * t)
        end = bb.lerp(H, t)
        end = end + (end - a).normalized() * (0.06 + 0.03 * ((i % 2) * 2 - 1)) * sz
        feather(B, a - nrm * 0.016, end - nrm * 0.016, nrm, fw, 0.03, IVORY_D if rows3 else WING_IN, wb,
                taper=0.35, tipc=OBSID, tipf=0.24, bev=bev)
    for i in range(n_cov):                                   # coverts
        t = (i + 0.5) / n_cov
        a = S.lerp(W, 0.03 + 0.94 * t)
        end = a.lerp(bb.lerp(H, t), 0.52)
        feather(B, a + nrm * 0.018, end + nrm * 0.018, nrm, fw * 0.80, 0.032, MOON_IVORY if rows3 else WING_IN, wb,
                taper=0.5, studs=rows3, bev=bev)
    for i in range(n_pri):                                   # primaries (hand): WING_IN, OBSID tips
        t = i / (n_pri - 1)
        dv = (H - W).normalized().lerp((T - W).normalized(), 0.12 + 0.88 * t).normalized()
        ln = (T - W).length * (0.66 + 0.36 * t) * (1.0 + 0.03 * ((i % 2) * 2 - 1))
        o = nrm * (0.03 + 0.004 * (n_pri - 1 - i))
        tipp = feather(B, W + dv * 0.04 + o, W + dv * ln + o, nrm, fw * 0.90, 0.03, WING_IN, tb, taper=0.22,
                       tipc=OBSID, tipf=0.30, bev=bev)
        if i == n_pri // 2:
            ANCH["FX_FeatherSparkle_%s_%s" % (P, side)] = tuple(tipp)
    if rows3:
        for i in range(3):                                   # hand coverts
            t = (i + 0.5) / 3
            dv = (H - W).normalized().lerp((T - W).normalized(), 0.40 + 0.60 * t).normalized()
            feather(B, W + dv * 0.03 + nrm * 0.065, W + dv * 0.36 + nrm * 0.065, nrm, 0.20, 0.03, MOON_IVORY, tb,
                    taper=0.5, bev=bev)


'''
s = s[:a0] + new + s[a1:]
# halo a little higher + slimmer, fewer segments
s = s.replace("HALO_C = HC + Vector((0, 0.07, 0.60))             # halo disc centre (0.20 H above the head)",
              "HALO_C = HC + Vector((0, 0.07, 0.64))             # halo disc centre (0.20 H above the head)")
s = s.replace("def ring_pts(R, n=40):", "def ring_pts(R, n=32):")
s = s.replace("    rim_o, rim_i = HALO_R, HALO_R - 0.045\n    n = 40\n", "    rim_o, rim_i = HALO_R, HALO_R - 0.045\n    n = 32\n")
s += '''

# ------------------------------------------------------------------ wings + the MODEL-GATE placeholder idle
def wings(k, f, P, up, fwd=0.0, twist=0.0, tip=0.0, side=None):
    WINGS[P][0].key(k, f, up, fwd, twist, tip, side)


DISPLAY_POSE = {"A": (42.0, -4.0, 0.0, 0.0), "B": (4.0, -14.0, 0.0, 0.0), "C": (-12.0, -10.0, 0.0, -8.0)}


def anim(k):
    """MODEL-GATE placeholder: idle = the six-wing display pose held (upper pair raised in a V, middle pair spread back,
    lower pair tucked at the flank) - the ground pose players see; the real clips come after the model gate"""
    n = 40
    k.new_action("idle", n, True)
    for f in (0, n):
        k.key("Spine", f, rot=(0, 0, 0), loc=(0, 0, 0))
        for P, w in DISPLAY_POSE.items():
            wings(k, f, P, *w)
    k.finish()
    return 0.5
'''
open(p, "w", encoding="utf-8").write(s)
print("ok")
