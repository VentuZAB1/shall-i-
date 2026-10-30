# HubGrime - procedural 1-stud "SurfaceType.Studs" tile (flat surface + normal/AO, like Roblox draws it).
# Outputs (HubGrime\mock\): stud_normal.png (tangent space, OpenGL, Blender UV up = -row), stud_ao.png (multiplier,
# non-colour), stud_lit.png (pre-lit shading factor for the 2D swatch sheets).
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from grime_lib import HERE, smoothstep, blur  # noqa: E402

N = 128  # px per stud
OUT = os.path.join(HERE, "mock")


def tile():
    c = (np.arange(N) + 0.5) / N - 0.5
    X, Y = np.meshgrid(c, c)  # studs, Y down, cell centre at 0
    # round 4: the live game draws ROUNDED-SQUARE studs (screenshots in ingame_round3\), not round ones.
    # r = distance-like field of a rounded square (half size B, corner radius RC); r = R on its outline
    B, RC = 0.245, 0.085
    qx, qy = np.abs(X) - (B - RC), np.abs(Y) - (B - RC)
    sdf = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - RC
    R, Hs, fil = 0.29, 0.06, 0.05
    r = sdf + R
    # stud: flat top + rounded edge (fillet) + steep side
    top = np.where(r < R - fil, Hs, Hs - (fil - np.sqrt(np.clip(fil * fil - (r - (R - fil)) ** 2, 0, None))))
    stud = np.where(r < R, top, 0.0)
    # faint cell groove at the cell border (the classic stud texture shows soft cell lines)
    edge = np.minimum(0.5 - np.abs(X), 0.5 - np.abs(Y))
    groove = -0.012 * (1 - smoothstep(0.0, 0.035, edge))
    h = stud + groove
    h = blur(h.astype(np.float32), 1.2, wrap_x=True)
    # wrap in y too (tile): blur did zero-pad in y; re-tile by averaging with a rolled copy at the borders
    hp = np.pad(stud + groove, ((8, 8), (8, 8)), mode="wrap").astype(np.float32)
    hp = blur(hp, 2.2)
    h = hp[8:-8, 8:-8]
    gy, gx = np.gradient(h, 1.0 / N)  # per stud
    # tangent space: u = +x (cols), v = UP = -rows
    dhdu = gx
    dhdv = -gy
    nx, ny, nz = -dhdu, -dhdv, np.ones_like(h)
    inv = 1 / np.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny, nz = nx * inv, ny * inv, nz * inv
    nrm = np.dstack([(nx * 0.5 + 0.5), (ny * 0.5 + 0.5), (nz * 0.5 + 0.5)])
    # AO: dark ring at the stud foot, slightly darker groove
    foot = np.exp(-((r - R - 0.02) / 0.035) ** 2) * (r > R - 0.01)
    ao = 1 - 0.16 * foot - 0.5 * np.clip(-groove / 0.012, 0, 1) * 0.12
    ao = ao * (0.93 + 0.07 * smoothstep(R + 0.01, R - 0.02, r))     # the stud tops read a touch lighter in game
    ao = np.clip(ao, 0, 1)
    # pre-lit factor for 2D sheets: light from the upper left, mostly overhead
    L = np.array([-0.35, 0.45, 0.82])  # (u, v-up, z)
    L /= np.linalg.norm(L)
    lam = nx * L[0] + ny * L[1] + nz * L[2]
    lit = np.clip((0.55 + 0.55 * lam) * ao / (0.55 + 0.55 * L[2]), 0, 1.3)
    return nrm, ao, lit


def main():
    os.makedirs(OUT, exist_ok=True)
    nrm, ao, lit = tile()
    Image.fromarray(np.round(nrm * 255).astype(np.uint8), "RGB").save(os.path.join(OUT, "stud_normal.png"))
    Image.fromarray(np.round(ao * 255).astype(np.uint8), "L").save(os.path.join(OUT, "stud_ao.png"))
    np.save(os.path.join(OUT, "stud_lit.npy"), lit.astype(np.float32))
    Image.fromarray(np.round(np.clip(lit / 1.3, 0, 1) * 255).astype(np.uint8), "L").save(os.path.join(OUT, "stud_lit.png"))
    print("studs ok", nrm.shape, float(ao.min()), float(lit.min()), float(lit.max()))


if __name__ == "__main__":
    main()
