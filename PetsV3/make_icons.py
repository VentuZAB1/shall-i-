# SLINGSHOT UI icons: original designs in a chunky "sticker" style
# (flat fill, one darker bottom shade band, small white shine, thick dark outline, soft drop shadow).
# Writes icons/<name>.svg; render with render_icons.sh (headless Chrome, transparent background).
import os, math

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)
INK = "#27233a"
THIN = 6  # inner part outlines; the thick outer outline comes from the filter


class Icon:
    def __init__(self):
        self.body, self.defs, self.n = [], [], 0

    def part(self, shape, fill, shade=None, shade_y=None, transform=None, stroke=True):
        """shape = an SVG element string without fill/stroke, e.g. '<rect x=.. />'"""
        self.n += 1
        cid = f"c{self.n}"
        g = []
        g.append(shape.replace("/>", f' fill="{fill}"/>'))
        if shade:
            self.defs.append(f'<clipPath id="{cid}">{shape}</clipPath>')
            g.append(f'<g clip-path="url(#{cid})"><rect x="-50" y="{shade_y}" width="400" height="400" fill="{shade}"/></g>')
        if stroke:
            g.append(shape.replace("/>", f' fill="none" stroke="{INK}" stroke-width="{THIN}" stroke-linejoin="round"/>'))
        inner = "".join(g)
        self.body.append(f'<g transform="{transform}">{inner}</g>' if transform else inner)

    def raw(self, s):
        self.body.append(s)

    def shine(self, x, y, w, h, rot=0):
        r = min(w, h) / 2
        self.body.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" opacity="0.85" transform="rotate({rot} {x + w / 2} {y + h / 2})"/>')

    def svg(self):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-16 -16 288 288" width="512" height="512">
<defs>
<filter id="outline" x="-20%" y="-20%" width="140%" height="140%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d"/>
  <feFlood flood-color="{INK}"/><feComposite in2="d" operator="in" result="o"/>
  <feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
  <feMorphology in="SourceAlpha" operator="dilate" radius="9" result="d"/>
  <feFlood flood-color="#000" flood-opacity="0.22"/><feComposite in2="d" operator="in"/>
</filter>
{"".join(self.defs)}
<g id="art">{"".join(self.body)}</g>
</defs>
<use xlink:href="#art" filter="url(#shadow)" transform="translate(0 12)"/>
<use xlink:href="#art" filter="url(#outline)"/>
</svg>'''


def rect(x, y, w, h, rx):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'


def path(d):
    return f'<path d="{d}"/>'


def circle(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'


icons = {}

# ---- cash: two bills + gold band
i = Icon()
i.part(rect(52, 50, 170, 104, 14), "#3fb54f", "#2c8f3b", 128, transform="rotate(-9 137 102)")
i.part(rect(34, 96, 180, 112, 14), "#5fd064", "#3aa648", 172)
i.part(circle(84, 152, 24), "#8fe28f", "#6fcf72", 160)
i.raw(f'<text x="84" y="166" font-family="Arial Black,Arial" font-weight="900" font-size="38" fill="{INK}" text-anchor="middle">$</text>')
i.part(rect(130, 90, 34, 124, 6), "#ffcc3d", "#f0a020", 172)
i.shine(48, 108, 54, 11)
icons["cash"] = i

# ---- shoe (speed): blue sneaker, toe right
i = Icon()
i.part(path("M44 160 L52 86 Q54 70 72 72 L102 76 Q116 78 120 94 L126 112 Q172 114 206 134 Q226 146 224 164 Z"), "#43aef7", "#2780d0", 140)
i.part(rect(34, 154, 198, 40, 18), "#ffffff", "#d3d9e6", 178)
i.part(path("M44 124 Q84 118 118 140 L110 150 Q80 132 46 138 Z"), "#ffffff", None)
for (x1, y1, x2, y2) in ((126, 118, 138, 100), (146, 122, 158, 104), (166, 128, 176, 112)):
    i.raw(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{INK}" stroke-width="18" stroke-linecap="round"/>')
    i.raw(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="#fff" stroke-width="7" stroke-linecap="round"/>')
i.shine(62, 84, 11, 34, rot=6)
icons["shoe"] = i

# ---- shop: orange shopping bag
i = Icon()
i.raw(f'<path d="M92 100 V76 Q92 38 128 38 Q164 38 164 76 V100" fill="none" stroke="{INK}" stroke-width="26" stroke-linecap="round"/>')
i.raw('<path d="M92 100 V76 Q92 38 128 38 Q164 38 164 76 V100" fill="none" stroke="#ffd75e" stroke-width="11" stroke-linecap="round"/>')
i.part(path("M50 90 H206 L218 206 Q220 224 202 224 H54 Q36 224 38 206 Z"), "#ff7b47", "#e0531f", 184)
i.part(rect(50, 90, 156, 24, 4), "#ff9d70", None)
i.part(circle(92, 132, 8), INK, None, stroke=False)
i.part(circle(164, 132, 8), INK, None, stroke=False)
i.shine(56, 124, 12, 58, rot=-4)
icons["shop"] = i

# ---- gift: red box + gold ribbon
i = Icon()
i.part(path("M128 90 C96 30 34 40 52 80 C62 100 104 98 128 90 Z"), "#ffcc3d", "#f0a020", 82)
i.part(path("M128 90 C160 30 222 40 204 80 C194 100 152 98 128 90 Z"), "#ffcc3d", "#f0a020", 82)
i.part(rect(50, 126, 156, 98, 10), "#ff4d5e", "#d92c40", 192)
i.part(rect(36, 88, 184, 44, 10), "#ff5f6e", "#d92c40", 118)
i.part(rect(112, 88, 32, 136, 4), "#ffcc3d", "#f0a020", 192)
i.part(circle(128, 88, 18), "#ffd75e", None)
i.shine(48, 98, 50, 10)
icons["gift"] = i

# ---- rebirth: one looping arrow around a gold star
i = Icon()
i.part(circle(128, 132, 70), "#f4ecff", "#e2d2ff", 160)
ring = "M180.7 69.2 A82 82 0 1 1 87 61"
head = "M116.4 44 L73 36.8 L101 85.2 Z"
i.raw(f'<path d="{ring}" fill="none" stroke="{INK}" stroke-width="{26 + 2 * THIN}" stroke-linecap="round"/>')
i.raw(f'<path d="{head}" fill="{INK}" stroke="{INK}" stroke-width="{2 * THIN + 8}" stroke-linejoin="round"/>')
i.raw(f'<path d="{ring}" fill="none" stroke="#ff6fb5" stroke-width="26" stroke-linecap="round"/>')
i.raw('<path d="M199 173 A82 82 0 0 1 57 173" fill="none" stroke="#e2458f" stroke-width="26"/>')  # bottom shade
i.raw(f'<path d="{head}" fill="#ff6fb5" stroke="#ff6fb5" stroke-width="8" stroke-linejoin="round"/>')
star = []
for k in range(10):
    a = -math.pi / 2 + k * math.pi / 5
    rr = 46 if k % 2 == 0 else 21
    star.append(f"{128 + rr * math.cos(a):.1f} {138 + rr * math.sin(a):.1f}")
i.part(path("M" + " L".join(star) + " Z"), "#ffcc3d", "#f0a020", 148)
i.raw('<path d="M45.3 162.1 A88 88 0 0 1 51.8 88" fill="none" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity="0.85"/>')
i.shine(114, 112, 8, 20, rot=20)
icons["rebirth"] = i

# ---- index: blue book with bookmark
i = Icon()
i.part(path("M148 200 V256 L162 243 L176 256 V200 Z"), "#ff4d5e", "#d92c40", 244)
i.part(rect(62, 46, 150, 180, 12), "#ffffff", "#d3d9e6", 206)
i.part(rect(44, 34, 152, 180, 14), "#3f8cff", "#2a64d6", 182)
i.part(rect(44, 34, 28, 180, 12), "#2a64d6", None)
i.part(rect(96, 72, 76, 36, 8), "#ffffff", None)
i.shine(84, 124, 10, 56)
icons["index"] = i

# ---- settings: grey gear
i = Icon()
pts = []
teeth, R, r0 = 8, 104, 80
for k in range(teeth * 6):
    a = (k / (teeth * 6)) * 2 * math.pi - math.pi / 2
    rad = R if k % 6 in (1, 2, 3) else r0
    pts.append(f"{128 + rad * math.cos(a):.1f} {128 + rad * math.sin(a):.1f}")
gear = "M" + " L".join(pts) + " Z"
i.part(path(gear), "#b3bccd", "#838fa8", 158)
i.part(circle(128, 128, 32), "#5d6682", "#454d66", 136)
i.raw('<path d="M72 112 A60 60 0 0 1 112 72" fill="none" stroke="#fff" stroke-width="10" stroke-linecap="round" opacity="0.85"/>')
icons["settings"] = i

for name, icon in icons.items():
    with open(os.path.join(OUT, name + ".svg"), "w") as f:
        f.write(icon.svg())
print("wrote", list(icons))
