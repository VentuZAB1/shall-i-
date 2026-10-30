def stormbreath(k):
    """SIGNATURE (Thunder Rex only, review 3) - STORM BREATH, the kaiju charge: plants low and glares, the tail drags
    then goes stiff; the body sinks and PUMPS three times while the crystal ridge lights up tail -> crown (VFX events
    charge1-3 on Bolt+Ridge3 / Ridge2+Core / Ridge1+Crown); rears and inhales, then fires a lightning beam from the mouth
    (Breath anchor) with a recoil absorbed by the planted legs, sweeping the head slowly across the beam; snaps the jaw
    shut (smoke puff), snorts and exhales; settles. Planted the whole time, no head shake (owner rule)."""
    n = 100
    k.new_action("act_stormbreath", n, False)
    EACH = (0.2, 0.45, 0.75, 1.0)
    K = [  # f, spine z, spine y, spine pitch, chest, neck pitch, neck yaw, head pitch, head yaw, jaw, tail, curl, spread
        (0, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0),
        (8, -0.06, 0.0, 6, 3, 6, 0, 8, 0, 3, -4, 20, 0),
        (14, -0.06, 0.0, 6, 3, 6, 0, 8, 0, 3, -4, 20, 0),
        (20, -0.085, 0.0, 6, -2, 6, 0, 10, 0, 4, 0, 22, 0),
        (25, -0.06, 0.0, 6, 3, 6, 0, 10, 0, 3, 2, 22, 0),
        (30, -0.085, 0.0, 6, -2, 6, 0, 12, 0, 4, 4, 24, 0),
        (35, -0.06, 0.0, 6, 3, 6, 0, 12, 0, 3, 6, 24, 0),
        (40, -0.085, 0.0, 6, -2, 6, 0, 14, 0, 4, 8, 26, 0),
        (44, -0.06, 0.0, 4, 2, 4, 0, 10, 0, 6, 8, 26, 0),
        (48, -0.02, 0.0, -6, -4, -8, 0, -14, 0, 26, 6, 30, 12),
        (52, -0.02, 0.0, -6, -4, -8, 0, -14, 0, 26, 6, 30, 12),
        (54, -0.05, 0.04, 4, 2, 4, -5, 6, -12, 40, 4, 34, 16),
        (80, -0.04, 0.01, 4, 2, 4, 5, 6, 12, 40, 4, 34, 16),
        (83, -0.03, 0.0, 2, 1, 2, 2, 2, 5, 3, 3, 20, 6),
        (86, -0.03, 0.0, 0, 0, 0, 0, -4, 0, 3, 2, 10, 0),
        (90, -0.01, 0.0, 0, 0, 0, 0, 0, 0, 3, 1, 4, 0),
        (100, 0.0, 0.0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0)]
    for f, z, y, p, ch, nk, ny, hd, hy, jw, tp, cu, sp in K:
        k.key("Spine", f, rot=(p, 0, 0), loc=(0, y, z))
        k.key("Chest", f, rot=(ch, 0, 0))
        k.key("Neck", f, rot=(nk, ny, 0))
        k.key("Head", f, rot=(hd, hy, 0))
        k.key("Jaw", f, rot=(jw, 0, 0))
        tail(k, f, tp, 0, each=EACH)
        arms(k, f, up=0, spread=sp, curl=cu)
    for f in range(57, 80, 3):                       # beam: jaw buzz + tail-tip shiver, head sweeping slowly
        w = 1 if (f // 3) % 2 else -1
        t = (f - 54) / 26.0
        k.key("Jaw", f, rot=(40 + 2 * w, 0, 0))
        k.key("Head", f, rot=(6, -12 + 24 * t, 0))
        k.key("Neck", f, rot=(4, -5 + 10 * t, 0))
        k.key("Tail4", f, rot=(4, 5 * w, 0))
    plant_frames(k, range(0, n + 1))
    k.finish(loop=False)
    k.events["act_stormbreath"] = {"charge1": round(20 / n, 3), "charge2": round(30 / n, 3), "charge3": round(40 / n, 3),
                                   "breath": round(54 / n, 3), "breath_end": round(80 / n, 3), "smoke": round(83 / n, 3)}


