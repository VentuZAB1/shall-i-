import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()

# 1) style constants
old = 'FACES = {"+x": (0, 1),'
new = '''# PRO pass (2026-10-08, user: "should not look this LOW QUALITY"): rounded faceted base forms + Steal-an-Egg plates
STYLE = {
    "round": 0.24,       # base-form edge rounding, fraction of the block's smallest half-size (blk.rnd overrides)
    "round_seg": 2,      # bevel segments on rounded edges (faceted-round, like the references)
    "plate_cov": 0.46,   # share of face cells that start a plate
    "plate_h": 1.0,      # plate relief multiplier on Blocks.stud_h
    "plate_gap": 0.17,   # groove around each plate, fraction of a cell
    "plate_jit": 0.06,   # per-plate brightness jitter (+-)
}
FACES = {"+x": (0, 1),'''
assert old in t; t = t.replace(old, new, 1)

# 2) Block gets rnd
old = '''                 bevel=0.03, studs=None, density=0.5, glow=None, name="", R=None):'''
new = '''                 bevel=0.03, studs=None, density=0.5, glow=None, name="", R=None, rnd=None):'''
assert old in t; t = t.replace(old, new, 1)
old = '''        self.name = name

    # local corner'''
new = '''        self.name = name
        self.rnd = rnd              # edge rounding override (fraction of the smallest half-size); None = STYLE

    # local corner'''
assert old in t; t = t.replace(old, new, 1)

# 3) rounded bevel
old = '''    mn = min(blk.h.x * min(blk.top[0], blk.bot[0]), blk.h.y * min(blk.top[1], blk.bot[1]), blk.h.z)
    off = min(blk.bevel, mn * 0.45)
    if off > 0.004:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=off, offset_type="OFFSET", segments=1, profile=0.5,
                        affect="EDGES", clamp_overlap=True)'''
new = '''    mn = min(blk.h.x * min(blk.top[0], blk.bot[0]), blk.h.y * min(blk.top[1], blk.bot[1]), blk.h.z)
    rr = STYLE["round"] if getattr(blk, "rnd", None) is None else blk.rnd
    off = min(max(blk.bevel, mn * rr), mn * 0.45)
    seg = STYLE["round_seg"] if off > 0.025 else 1
    if off > 0.004:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=off, offset_type="OFFSET", segments=seg, profile=0.5,
                        affect="EDGES", clamp_overlap=True)'''
assert old in t; t = t.replace(old, new, 1)

# 4) plate geometry: two-step chamfered top
old = '''def _stud(bm, L, ctr, u, v, n, a, b, hgt, color):
    """raised square tile: straight sides then a chamfered top (a, b = half extents along u, v)"""
    c = min(a, b) * 0.32
    rings = []
    for (da, db, dz) in ((a, b, -0.006), (a, b, hgt * 0.5), (a - c, b - c, hgt)):'''
new = '''def _stud(bm, L, ctr, u, v, n, a, b, hgt, color):
    """raised plate: straight sides, then a two-step chamfered top (a, b = half extents along u, v)"""
    c = min(a, b) * 0.34
    rings = []
    for (da, db, dz) in ((a, b, -0.006), (a, b, hgt * 0.45), (a - c * 0.45, b - c * 0.45, hgt * 0.85),
                         (a - c, b - c, hgt)):'''
assert old in t; t = t.replace(old, new, 1)
old = '''    for i in range(2):
        for j in range(4):
            bm.faces.new((rings[i][j], rings[i][(j + 1) % 4], rings[i + 1][(j + 1) % 4], rings[i + 1][j]))
    bm.faces.new(rings[2])'''
new = '''    for i in range(3):
        for j in range(4):
            bm.faces.new((rings[i][j], rings[i][(j + 1) % 4], rings[i + 1][(j + 1) % 4], rings[i + 1][j]))
    bm.faces.new(rings[3])'''
assert old in t; t = t.replace(old, new, 1)

# 5) plate layout + eye builder
a = t.index("    def _studs_for(self, blk, bm, L):")
b = t.index("    def _apply_head_xf(self):")
new_fn = open(sys.argv[2], encoding="utf-8").read()
t = t[:a] + new_fn + "\n" + t[b:]
open(p, "w", encoding="utf-8").write(t)
print("ok")
