#!/usr/bin/env python3
"""
Genera el perfil de GitHub completo (estética Precision Dark): README.md y
los 12 SVG de /assets (6 de escritorio + 6 variantes «-mobile»).

Uso:
    python scripts/generate_assets.py

Solo usa la biblioteca estándar. Para actualizar el perfil, edita ÚNICAMENTE
la sección «CONTENIDO» y vuelve a ejecutar el script. No edites README.md ni
los SVG a mano: se sobrescriben. Los archivos cuyo contenido no cambia no se
reescriben, así que Git solo mostrará lo que realmente se modificó.
"""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# ════════════════════════════════════════════════════════════════════
#  CONTENIDO — edita aquí
# ════════════════════════════════════════════════════════════════════

NAME = "Karen Lorena"
DEGREE = "Ingeniería de Sistemas"
ROLE = f"Estudiante de {DEGREE}"
FOCUS = ["soporte técnico", "desarrollo de software", "redes e infraestructura"]
USER = "KarenLGT"
BRANCH = "main"

# Etiquetas de la barra de estado de la cabecera (escritorio).
HEADER_TAGS = ["python", "django", "fastapi", "sql"]

# Formación: nombre completo (README) y forma corta (terminal, donde el espacio es limitado).
EDUCATION = [
    ("Técnica en Sistemas", "Técnica en Sistemas"),
    ("Tecnóloga en Análisis y Desarrollo de Sistemas de Información (ADSI)", "Tecnóloga en ADSI"),
    (f"{DEGREE} (en curso)", f"{DEGREE} (en curso)"),
]

# Datos que muestra la terminal (cat profile.json y ls projects/).
EXPERIENCE = ["soporte técnico", "mantenimiento de computadores", "consultas SQL"]
PROJECT_DIRS = ["asistencia-qr", "manson", "redes-infraestructura"]

# Sección «Sobre mí» del README (admite Markdown).
ABOUT = [
    f"Soy **técnica en Sistemas** y **tecnóloga en Análisis y Desarrollo de Sistemas de "
    f"Información (ADSI)**, y actualmente estudio **{DEGREE}**.",
    "Mi experiencia laboral se centra en el soporte técnico: mantenimiento de computadores, "
    "instalación y configuración de software, consultas SQL y resolución de incidencias "
    "relacionadas con sistemas de información.",
    "Me interesan especialmente el desarrollo de software, las redes y la infraestructura "
    "tecnológica, áreas en las que trabajo a través de proyectos académicos y personales.",
]

CONTACT = (f"Puedes seguir mi trabajo y contactarme a través de GitHub: "
           f"**[@{USER}](https://github.com/{USER})**.")

# Orden pensado para que los paneles de cada fila tengan alturas parecidas.
STACK = [
    ("Desarrollo de software", ["Python", "Django", "FastAPI", "JavaScript", "HTML", "CSS"]),
    ("Redes e infraestructura", ["Cisco Packet Tracer", "Redes informáticas",
                                 "Configuración de redes"]),
    ("Bases de datos", ["SQL", "SQLite"]),
    ("Herramientas de desarrollo", ["Git", "GitHub", "Visual Studio Code"]),
]

PROJECTS = [
    {
        "file": "project-qr.svg",
        "title": "Asistencia con QR dinámicos",
        "status": "en desarrollo",
        "desc": "Sistema web para registrar la asistencia académica mediante códigos QR dinámicos.",
        "tech": ["Python", "Django", "SQLite"],
        "glyph": "qr",
    },
    {
        "file": "project-manson.svg",
        "title": "Manson · asistente virtual personal",
        "status": "en desarrollo",
        "desc": "Asistente virtual personal desarrollado con Python y FastAPI, con integración "
                "de modelos de lenguaje a través de Ollama.",
        "tech": ["Python", "FastAPI", "SQLite", "Ollama"],
        "glyph": "wave",
    },
    {
        "file": "project-networks.svg",
        "title": "Redes e infraestructura",
        "status": "académico",
        "desc": "Proyectos académicos relacionados con el diseño, configuración y administración "
                "de redes informáticas mediante herramientas de simulación.",
        "tech": ["Cisco Packet Tracer"],
        "glyph": "net",
    },
]

# ════════════════════════════════════════════════════════════════════
#  SISTEMA VISUAL
# ════════════════════════════════════════════════════════════════════

BG = "#0D0D0D"        # negro profundo
PANEL = "#171717"     # gris grafito
RED = "#DC2626"       # rojo principal (solo acentos)
RED_DARK = "#991B1B"  # rojo oscuro (brillos y halos)
MUTED = "#A3A3A3"     # gris secundario
TEXT = "#F5F5F5"      # blanco suave
LINE = "#262626"      # bordes
DIM = "#5C5C5C"       # metadatos
NODE = "#3A3A3A"      # elementos decorativos

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', 'Cascadia Code', Consolas, 'Liberation Mono', Menlo, monospace"

W = 840          # ancho de los recursos de escritorio
WM = 400         # ancho de las variantes móviles (se muestran al ~81 % en un teléfono de 390 px)
CHAR = 0.6       # ancho aproximado de un carácter monoespaciado (en em)

BASE_CSS = (
    ".s{font-family:" + SANS + "}"
    ".m{font-family:" + MONO + "}"
)
NO_MOTION = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def svg(w, h, body, title, css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">'
        f'<title id="t">{escape(title)}</title>'
        f'<style>{BASE_CSS}{css}</style>{body}</svg>\n'
    )


def text(x, y, content, cls="s", size=14, fill=TEXT, extra=""):
    return (f'<text x="{x:g}" y="{y:g}" class="{cls}" font-size="{size}" '
            f'fill="{fill}"{extra}>{content}</text>')


def chip_width(label, size=15):
    return round(len(label) * size * CHAR + 22)


def chip(x, y, label, size=15):
    w, h = chip_width(label, size), 30
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{BG}" stroke="{LINE}"/>'
        + text(x + w / 2, y + h / 2 + size * 0.35, escape(label), "m", size, TEXT,
               ' text-anchor="middle"')
    ), w


def chip_flow(x, y, max_w, labels, gap=8, row_h=38):
    """Coloca chips en filas; devuelve (svg, número de filas)."""
    out, cx, cy, rows = [], x, y, 1
    for label in labels:
        w = chip_width(label)
        if cx > x and cx + w > x + max_w:
            cx, cy, rows = x, cy + row_h, rows + 1
        part, w = chip(cx, cy, label)
        out.append(part)
        cx += w + gap
    return "".join(out), rows


def brackets(x, y, w, h, l=10, color=DIM):
    """Esquinas tipo corchete alrededor de un área."""
    d = (f"M{x},{y + l}V{y}H{x + l} M{x + w - l},{y}H{x + w}V{y + l} "
         f"M{x + w},{y + h - l}V{y + h}H{x + w - l} M{x + l},{y + h}H{x}V{y + h - l}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5"/>'


def wrap(s, max_chars):
    lines, cur = [], ""
    for word in s.split():
        if cur and len(cur) + 1 + len(word) > max_chars:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    return lines + [cur] if cur else lines


DOT_GRID = (
    '<pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse">'
    f'<circle cx="1" cy="1" r="1" fill="{TEXT}" fill-opacity=".07"/></pattern>'
)

# ════════════════════════════════════════════════════════════════════
#  TEXTOS ALTERNATIVOS — compartidos por el <title> de cada SVG y el alt del README
# ════════════════════════════════════════════════════════════════════

def header_summary():
    return f"{NAME} — {ROLE}. " + ", ".join(FOCUS).capitalize() + "."


def stack_summary():
    return "Tecnologías: " + "; ".join(f"{t}: {', '.join(i)}" for t, i in STACK) + "."


def project_summary(n, p):
    return (f"Proyecto {n:02d}: {p['title']} ({p['status']}). {p['desc']} "
            f"Tecnologías: {', '.join(p['tech'])}.")

# ════════════════════════════════════════════════════════════════════
#  CABECERA
# ════════════════════════════════════════════════════════════════════

def header():
    h = 280
    sep = f'<tspan fill="{RED}">  /  </tspan>'
    focus = sep.join(f'<tspan fill="{MUTED}">{escape(f)}</tspan>' for f in FOCUS)

    nodes = [(628, 96), (706, 70), (782, 104), (660, 168), (742, 150), (800, 196)]
    edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4), (2, 4), (4, 5)]
    net = "".join(
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" '
        f'stroke="{NODE}" stroke-width="1"/>' for a, b in edges)
    for i, (x, y) in enumerate(nodes):
        if i == 4:
            net += (f'<circle class="pulse" cx="{x}" cy="{y}" r="10" fill="none" stroke="{RED}"/>'
                    f'<circle cx="{x}" cy="{y}" r="5" fill="{RED}"/>')
        else:
            net += f'<circle cx="{x}" cy="{y}" r="4" fill="{PANEL}" stroke="{DIM}"/>'

    body = (
        '<defs>' + DOT_GRID +
        f'<radialGradient id="glow" cx="85%" cy="35%" r="55%">'
        f'<stop offset="0" stop-color="{RED_DARK}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{RED_DARK}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="c"><rect width="{W}" height="{h}" rx="14"/></clipPath></defs>'
        '<g clip-path="url(#c)">'
        f'<rect width="{W}" height="{h}" fill="{BG}"/>'
        f'<rect width="{W}" height="{h}" fill="url(#g)"/>'
        f'<rect width="{W}" height="{h}" fill="url(#glow)"/>'
        # barra superior
        + text(32, 28, f'<tspan fill="{RED}">~/</tspan>{USER} <tspan fill="{NODE}">·</tspan> README.md',
               "m", 12, DIM)
        + text(W - 32, 28, "perfil profesional", "m", 12, DIM, ' text-anchor="end"')
        + f'<line x1="0" y1="44" x2="{W}" y2="44" stroke="{LINE}"/>'
        # identidad
        + f'<rect x="32" y="86" width="3" height="90" fill="{RED}"/>'
        + text(56, 140, escape(NAME), "s", 54, TEXT, ' font-weight="600" letter-spacing="-1"')
        + text(58, 172, escape(ROLE), "s", 20, MUTED)
        + text(32, 222, focus, "m", 14, MUTED)
        + f'<g class="deco">{net}</g>'
        # barra de estado
        + f'<rect y="{h - 36}" width="{W}" height="36" fill="{PANEL}"/>'
        + f'<line x1="0" y1="{h - 36}" x2="{W}" y2="{h - 36}" stroke="{LINE}"/>'
        + f'<circle cx="38" cy="{h - 18}" r="3.5" fill="{RED}"/>'
        + text(50, h - 14, "main", "m", 12, MUTED)
        + text(110, h - 14, " · ".join(HEADER_TAGS), "m", 12, DIM)
        + text(W - 32, h - 14, f"github.com/{USER}", "m", 12, DIM, ' text-anchor="end"')
        + '</g>'
        + f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>'
    )
    css = (
        ".pulse{transform-box:fill-box;transform-origin:center;"
        "animation:p 3.2s ease-out infinite}"
        "@keyframes p{0%{transform:scale(.6);opacity:.7}100%{transform:scale(1.9);opacity:0}}"
        + NO_MOTION
    )
    return svg(W, h, body, header_summary(), css)

# ════════════════════════════════════════════════════════════════════
#  TERMINAL
# ════════════════════════════════════════════════════════════════════

def terminal_lines(compact):
    """Líneas de la terminal como (tipo, contenido); «cmd» se escribe con efecto de tecleo."""
    def k(s): return f'<tspan fill="{MUTED}">"{escape(s)}"</tspan>'
    def v(s): return f'<tspan fill="{TEXT}">"{escape(s)}"</tspan>'
    def p(s): return f'<tspan fill="{DIM}">{escape(s)}</tspan>'
    def d(s): return (f'<tspan fill="{TEXT}" font-weight="600">{escape(s)}</tspan>'
                      f'<tspan fill="{RED}">/</tspan>')

    def block(key, items, last=False):
        """Lista JSON con un elemento por línea."""
        rows = [("out", "  " + k(key) + p(": ["))]
        rows += [("out", "    " + v(it) + (p(",") if i < len(items) - 1 else ""))
                 for i, it in enumerate(items)]
        return rows + [("out", "  " + p("]" if last else "],"))]

    def inline(key, items, last=False):
        """Lista JSON en una sola línea (solo escritorio)."""
        return [("out", "  " + k(key) + p(": [") + p(", ").join(v(i) for i in items)
                 + p("]" if last else "],"))]

    name = f'<tspan fill="{TEXT}">{escape(NAME)}</tspan>'
    role = f'<tspan fill="{MUTED}">{escape(ROLE[0].lower() + ROLE[1:])}</tspan>'
    education = [short for _, short in EDUCATION]

    if compact:
        # Un dato por línea para que el texto conserve un tamaño legible en móvil.
        whoami = [("out", name), ("out", role)]
        experience = block("experiencia", EXPERIENCE, last=True)
        dirs = [("out", d(x)) for x in PROJECT_DIRS]
    else:
        whoami = [("out", name + f'<tspan fill="{DIM}"> · </tspan>' + role)]
        experience = inline("experiencia", EXPERIENCE, last=True)
        dirs = [("out", "    ".join(d(x) for x in PROJECT_DIRS))]

    return ([("cmd", "whoami")] + whoami + [("gap", ""),
             ("cmd", "cat profile.json"), ("out", p("{"))]
            + block("formacion", education) + experience
            + [("out", p("}")), ("gap", ""), ("cmd", "ls projects/")]
            + dirs + [("end", "")])

def terminal(compact=False):
    w = WM if compact else W
    fs, lh, x0, top, pad, bottom = (15, 25, 20, 40, 34, 24) if compact else (15, 26, 28, 40, 36, 28)
    cw = fs * CHAR
    speed = 0.07                          # segundos por carácter tecleado
    step = 0.06 if compact else 0.1       # pausa entre líneas de salida
    lines = terminal_lines(compact)
    h = top + pad + (len(lines) - 1) * lh + bottom
    prompt_w = 2 * cw  # "❯ "

    css = [
        "text{white-space:pre}",
        ".l{animation:in .25s ease both}",
        "@keyframes in{from{opacity:0}to{opacity:1}}",
        ".cur{opacity:0}",
        "@keyframes on{0%,99%{opacity:1}100%{opacity:0}}",
        ".blink{animation:in .2s ease both,b 1.1s steps(1) infinite}",
        "@keyframes b{50%{opacity:0}}",
    ]
    body, t, n = [], 0.3, 0
    for i, (kind, content) in enumerate(lines):
        y = top + pad + i * lh
        if kind == "gap":
            t += 0.3
            continue
        if kind == "cmd":
            n += 1
            tw = len(content) * cw
            dur = len(content) * speed
            css.append(f"@keyframes t{n}{{from{{transform:translateX(-{tw:.1f}px)}}"
                       f"to{{transform:translateX(0)}}}}")
            css.append(f".t{n}{{animation:t{n} {dur:.2f}s steps({len(content)}) {t + .15:.2f}s both}}")
            css.append(f".c{n}{{animation:on {dur + .3:.2f}s linear {t + .15:.2f}s both}}")
            ex = x0 + prompt_w + tw
            body.append(
                f'<g class="l" style="animation-delay:{t:.2f}s">'
                + text(x0, y, f'<tspan fill="{RED}">❯</tspan> {escape(content)}', "m", fs, TEXT)
                + f'<g class="t{n}"><rect x="{ex:.1f}" y="{y - fs}" width="{tw + 14:.1f}" '
                  f'height="{lh}" fill="{BG}"/>'
                + f'<rect class="cur c{n}" x="{ex + 1:.1f}" y="{y - fs + 2}" width="{cw:.1f}" '
                  f'height="{fs + 3}" fill="{RED}"/></g></g>')
            t += 0.15 + dur + 0.3
        elif kind == "out":
            body.append(f'<g class="l" style="animation-delay:{t:.2f}s">'
                        + text(x0, y, content, "m", fs, MUTED) + '</g>')
            t += step
        elif kind == "end":
            t += 0.3
            body.append(
                f'<g class="l" style="animation-delay:{t:.2f}s">'
                + text(x0, y, f'<tspan fill="{RED}">❯</tspan>', "m", fs, TEXT) + '</g>'
                + f'<rect class="blink" style="animation-delay:{t:.2f}s,{t:.2f}s" '
                  f'x="{x0 + prompt_w + 1:.1f}" y="{y - fs + 2}" width="{cw:.1f}" '
                  f'height="{fs + 3}" fill="{RED}"/>')

    chrome = (
        f'<defs><clipPath id="c"><rect width="{w}" height="{h}" rx="12"/></clipPath></defs>'
        '<g clip-path="url(#c)">'
        f'<rect width="{w}" height="{h}" fill="{BG}"/>'
        f'<rect width="{w}" height="{top}" fill="{PANEL}"/>'
        f'<line x1="0" y1="{top}" x2="{w}" y2="{top}" stroke="{LINE}"/>'
        f'<circle cx="24" cy="20" r="5.5" fill="{RED}"/>'
        f'<circle cx="43" cy="20" r="5.5" fill="{NODE}"/>'
        f'<circle cx="62" cy="20" r="5.5" fill="{NODE}"/>'
        + (text(w - 20, 25, "karen@lorena: ~", "m", 14, DIM, ' text-anchor="end"') if compact else
           text(w / 2, 24, "karen@lorena: ~", "m", 12, DIM, ' text-anchor="middle"')
           + text(w - 24, 24, "bash", "m", 12, NODE, ' text-anchor="end"'))
        + "".join(body)
        + '</g>'
        + f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="none" stroke="{LINE}"/>'
    )
    return svg(w, h, chrome, terminal_summary(), "".join(css) + NO_MOTION)


def terminal_summary():
    return (f"Terminal: whoami muestra {NAME}, {ROLE[0].lower() + ROLE[1:]}; "
            f"cat profile.json resume la formación ({'; '.join(f for f, _ in EDUCATION)}) "
            f"y la experiencia en {', '.join(EXPERIENCE)}; "
            f"ls projects/ lista {', '.join(PROJECT_DIRS)}.")

# ════════════════════════════════════════════════════════════════════
#  TECNOLOGÍAS
# ════════════════════════════════════════════════════════════════════

def stack():
    gap, pw, inner = 16, (W - 16) // 2, 24
    head = 68
    layouts = []
    for i, (title, items) in enumerate(STACK):
        chips, rows = chip_flow(0, 0, pw - 2 * inner, items)
        layouts.append((i, title, items, rows))
    # altura por fila de paneles = la del panel más alto
    row_heights = []
    for r in range(0, len(layouts), 2):
        rows = max(l[3] for l in layouts[r:r + 2])
        row_heights.append(head + rows * 38 + 18)
    h = sum(row_heights) + gap * (len(row_heights) - 1)

    body, y = [], 0
    for r, rh in enumerate(row_heights):
        for c in range(2):
            idx = r * 2 + c
            if idx >= len(layouts):
                break
            i, title, items, _ = layouts[idx]
            x = c * (pw + gap)
            chips, _ = chip_flow(x + inner, y + head, pw - 2 * inner, items)
            body.append(
                f'<rect x="{x + .5}" y="{y + .5}" width="{pw - 1}" height="{rh - 1}" rx="10" '
                f'fill="{PANEL}" stroke="{LINE}"/>'
                + text(x + inner, y + 36, f"{i + 1:02d}", "m", 12, RED)
                + text(x + inner + 30, y + 36, escape(title), "s", 18, TEXT, ' font-weight="600"')
                + f'<line x1="{x + inner}" y1="{y + 52}" x2="{x + pw - inner}" y2="{y + 52}" '
                  f'stroke="{LINE}"/>'
                + chips)
        y += rh + gap
    return svg(W, h, "".join(body), stack_summary())

# ════════════════════════════════════════════════════════════════════
#  TARJETAS DE PROYECTO
# ════════════════════════════════════════════════════════════════════

def glyph(kind, x, y):
    """Ilustración abstracta de 112×112 px en la esquina de la tarjeta."""
    if kind == "qr":
        # Patrón decorativo inspirado en un QR (no es un código válido).
        cells = ["1110101", "1010011", "1110110", "0001010", "1011101", "0110011", "1010111"]
        red = {(3, 3), (5, 1)}
        s, g, out = 13, 3, []
        for r, row in enumerate(cells):
            for c, bit in enumerate(row):
                if bit == "1":
                    color = RED if (r, c) in red else NODE
                    out.append(f'<rect x="{x + c * (s + g)}" y="{y + r * (s + g)}" '
                               f'width="{s}" height="{s}" rx="2" fill="{color}"/>')
        return "".join(out)
    if kind == "wave":
        hs = [18, 34, 58, 82, 104, 74, 46, 88, 60, 30, 16]
        bw, g, out = 6, 4.6, []
        for i, bh in enumerate(hs):
            color = RED if i == 4 else NODE
            out.append(f'<rect x="{x + i * (bw + g):.1f}" y="{y + 56 - bh / 2}" width="{bw}" '
                       f'height="{bh}" rx="3" fill="{color}"/>')
        return "".join(out)
    # net: router central y cuatro equipos
    cx, cy = x + 56, y + 56
    pts = [(x + 6, y + 10), (x + 106, y + 10), (x + 6, y + 102), (x + 106, y + 102)]
    out = [f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="{NODE}"/>' for px, py in pts]
    out.append(f'<line x1="{pts[0][0]}" y1="{pts[0][1]}" x2="{pts[1][0]}" y2="{pts[1][1]}" '
               f'stroke="{NODE}" stroke-dasharray="3 4"/>')
    out += [f'<rect x="{px - 8}" y="{py - 8}" width="16" height="16" rx="3" fill="{PANEL}" '
            f'stroke="{DIM}"/>' for px, py in pts]
    out.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="{RED}" stroke-opacity=".4"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{RED}"/>')
    return "".join(out)


def project_card(n, p):
    h, pad = 224, 28
    status_w = round(len(p["status"]) * 12 * CHAR + 34)
    sx = W - pad - status_w
    desc = "".join(
        text(pad, 120 + i * 24, escape(line), "s", 16, MUTED)
        for i, line in enumerate(wrap(p["desc"], 84)))
    chips, _ = chip_flow(pad, h - pad - 30, 600, p["tech"])
    body = (
        f'<defs>{DOT_GRID}<clipPath id="c"><rect width="{W}" height="{h}" rx="12"/></clipPath></defs>'
        '<g clip-path="url(#c)">'
        f'<rect width="{W}" height="{h}" fill="{PANEL}"/>'
        f'<rect x="{W - 200}" width="200" height="{h}" fill="url(#g)"/>'
        f'<rect width="3" height="{h}" fill="{RED}"/>'
        '</g>'
        f'<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="12" fill="none" stroke="{LINE}"/>'
        + text(pad, 40, f'proyecto <tspan fill="{NODE}">/</tspan> <tspan fill="{RED}">{n:02d}</tspan>',
               "m", 12, DIM)
        + f'<rect x="{sx}" y="23" width="{status_w}" height="24" rx="12" fill="{BG}" stroke="{LINE}"/>'
        + f'<circle cx="{sx + 14}" cy="35" r="3.5" fill="{RED}"/>'
        + text(sx + 24, 39, escape(p["status"]), "m", 12, MUTED)
        + text(pad, 86, escape(p["title"]), "s", 26, TEXT, ' font-weight="600"')
        + desc
        + chips
        + '<g class="deco">' + brackets(W - 160, 72, 128, 128)
        + glyph(p["glyph"], W - 152, 80) + '</g>'
    )
    return svg(W, h, body, project_summary(n, p))

# ════════════════════════════════════════════════════════════════════
#  VARIANTES MÓVILES (WM = 400 px)
#  Se sirven con <picture> en pantallas de hasta 600 px. Los tamaños de
#  letra están pensados para verse a ~81 %: 15 px → ~12 px en pantalla.
# ════════════════════════════════════════════════════════════════════

def header_mobile():
    w, h = WM, 304
    nodes = [(292, 190), (334, 176), (380, 196), (306, 240), (350, 228), (384, 254)]
    edges = [(0, 1), (1, 2), (0, 3), (3, 4), (1, 4), (2, 4), (4, 5)]
    net = "".join(
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" '
        f'stroke="{NODE}"/>' for a, b in edges)
    for i, (x, y) in enumerate(nodes):
        net += (f'<circle class="pulse" cx="{x}" cy="{y}" r="8" fill="none" stroke="{RED}"/>'
                f'<circle cx="{x}" cy="{y}" r="4" fill="{RED}"/>' if i == 4 else
                f'<circle cx="{x}" cy="{y}" r="3" fill="{PANEL}" stroke="{DIM}"/>')
    focus = "".join(
        text(20, 198 + i * 24, f'<tspan fill="{RED}">/</tspan> {escape(f)}', "m", 15, MUTED)
        for i, f in enumerate(FOCUS))
    body = (
        '<defs>' + DOT_GRID +
        f'<radialGradient id="glow" cx="85%" cy="30%" r="70%">'
        f'<stop offset="0" stop-color="{RED_DARK}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{RED_DARK}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="c"><rect width="{w}" height="{h}" rx="12"/></clipPath></defs>'
        '<g clip-path="url(#c)">'
        f'<rect width="{w}" height="{h}" fill="{BG}"/>'
        f'<rect width="{w}" height="{h}" fill="url(#g)"/>'
        f'<rect width="{w}" height="{h}" fill="url(#glow)"/>'
        + text(20, 28, f'<tspan fill="{RED}">~/</tspan>{USER} <tspan fill="{NODE}">·</tspan> README.md',
               "m", 14, DIM)
        + f'<line x1="0" y1="44" x2="{w}" y2="44" stroke="{LINE}"/>'
        + f'<rect x="20" y="74" width="3" height="84" fill="{RED}"/>'
        + text(38, 118, escape(NAME), "s", 42, TEXT, ' font-weight="600" letter-spacing="-1"')
        + text(39, 148, escape(ROLE), "s", 17, MUTED)
        + focus + f'<g class="deco">{net}</g>'
        + f'<rect y="{h - 38}" width="{w}" height="38" fill="{PANEL}"/>'
        + f'<line x1="0" y1="{h - 38}" x2="{w}" y2="{h - 38}" stroke="{LINE}"/>'
        + f'<circle cx="26" cy="{h - 19}" r="3.5" fill="{RED}"/>'
        + text(38, h - 14, "main", "m", 14, MUTED)
        + text(w - 20, h - 14, f"github.com/{USER}", "m", 14, DIM, ' text-anchor="end"')
        + '</g>'
        + f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="none" stroke="{LINE}"/>'
    )
    css = (".pulse{transform-box:fill-box;transform-origin:center;animation:p 3.2s ease-out infinite}"
           "@keyframes p{0%{transform:scale(.6);opacity:.7}100%{transform:scale(1.9);opacity:0}}"
           + NO_MOTION)
    return svg(w, h, body, header_summary(), css)


def stack_mobile():
    """Tecnologías en una sola columna."""
    w, inner, head, gap = WM, 18, 64, 12
    body, y = [], 0
    for i, (title, items) in enumerate(STACK):
        _, rows = chip_flow(0, 0, w - 2 * inner, items)
        ph = head + rows * 38 + 12
        chips, _ = chip_flow(inner, y + head, w - 2 * inner, items)
        body.append(
            f'<rect x=".5" y="{y + .5}" width="{w - 1}" height="{ph - 1}" rx="10" '
            f'fill="{PANEL}" stroke="{LINE}"/>'
            + text(inner, y + 34, f"{i + 1:02d}", "m", 14, RED)
            + text(inner + 30, y + 34, escape(title), "s", 18, TEXT, ' font-weight="600"')
            + f'<line x1="{inner}" y1="{y + 50}" x2="{w - inner}" y2="{y + 50}" stroke="{LINE}"/>'
            + chips)
        y += ph + gap
    return svg(w, y - gap, "".join(body), stack_summary())


def project_card_mobile(n, p):
    """Tarjeta vertical sin ilustración: más espacio para el contenido."""
    w, pad = WM, 20
    title_lines, desc_lines = wrap(p["title"], 29), wrap(p["desc"], 41)
    ty0 = 84
    dy0 = ty0 + (len(title_lines) - 1) * 28 + 34
    cy = dy0 + (len(desc_lines) - 1) * 24 + 22
    _, rows = chip_flow(0, 0, w - 2 * pad, p["tech"])
    h = cy + rows * 38 - 8 + pad
    chips, _ = chip_flow(pad, cy, w - 2 * pad, p["tech"])
    sw = round(len(p["status"]) * 14 * CHAR + 38)
    sx = w - pad - sw
    body = (
        f'<defs>{DOT_GRID}<clipPath id="c"><rect width="{w}" height="{h}" rx="12"/></clipPath></defs>'
        '<g clip-path="url(#c)">'
        f'<rect width="{w}" height="{h}" fill="{PANEL}"/>'
        f'<rect x="{w - 140}" width="140" height="{h}" fill="url(#g)"/>'
        f'<rect width="3" height="{h}" fill="{RED}"/>'
        '</g>'
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="12" fill="none" stroke="{LINE}"/>'
        + text(pad, 39, f'proyecto <tspan fill="{NODE}">/</tspan> <tspan fill="{RED}">{n:02d}</tspan>',
               "m", 14, DIM)
        + f'<rect x="{sx}" y="20" width="{sw}" height="27" rx="13.5" fill="{BG}" stroke="{LINE}"/>'
        + f'<circle cx="{sx + 15}" cy="33.5" r="3.5" fill="{RED}"/>'
        + text(sx + 26, 38.5, escape(p["status"]), "m", 14, MUTED)
        + "".join(text(pad, ty0 + i * 28, escape(l), "s", 22, TEXT, ' font-weight="600"')
                  for i, l in enumerate(title_lines))
        + "".join(text(pad, dy0 + i * 24, escape(l), "s", 17, MUTED)
                  for i, l in enumerate(desc_lines))
        + chips
    )
    return svg(w, h, body, project_summary(n, p))

# ════════════════════════════════════════════════════════════════════

def mobile_name(filename):
    return filename.replace(".svg", "-mobile.svg")

# ════════════════════════════════════════════════════════════════════
#  README
# ════════════════════════════════════════════════════════════════════

MOBILE_QUERY = "(max-width: 600px)"


def asset_url(rel):
    # URL absolutas: GitHub muestra el README en github.com/<usuario>, donde las rutas
    # relativas de <source srcset> no están garantizadas. raw.githubusercontent.com
    # sirve los SVG como image/svg+xml y permite sus estilos internos.
    return f"https://raw.githubusercontent.com/{USER}/{USER}/{BRANCH}/assets/{rel}"


def picture(rel, alt):
    """Imagen de escritorio con variante móvil; <img> es el respaldo."""
    return ('<p align="center">\n'
            '  <picture>\n'
            f'    <source media="{MOBILE_QUERY}" srcset="{asset_url(mobile_name(rel))}">\n'
            f'    <img src="{asset_url(rel)}" width="100%" alt={quoteattr(alt)}>\n'
            '  </picture>\n'
            '</p>')


def heading(n, title):
    return f"### `{n:02d}` &nbsp;{title}"


def readme():
    table = "\n".join(f"| {cat} | {' · '.join(items)} |" for cat, items in STACK)
    parts = [
        "<!--\n"
        "  ARCHIVO GENERADO — no lo edites a mano.\n"
        "  Edita la sección «CONTENIDO» de scripts/generate_assets.py y ejecuta:\n"
        "      python scripts/generate_assets.py\n"
        "-->",
        picture("banners/header.svg", header_summary()),
        picture("animations/terminal.svg", terminal_summary()),
        heading(1, "Sobre mí"),
        *ABOUT,
        heading(2, "Tecnologías"),
        picture("banners/stack.svg", stack_summary()),
        "<details>\n<summary>Ver como texto</summary>\n\n"
        f"| Categoría | Herramientas |\n|---|---|\n{table}\n\n</details>",
        heading(3, "Proyectos destacados"),
        *(picture(f"cards/{p['file']}", project_summary(n, p))
          for n, p in enumerate(PROJECTS, 1)),
        heading(4, "Contacto"),
        CONTACT,
    ]
    return "\n\n".join(parts) + "\n"

# ════════════════════════════════════════════════════════════════════

def write_if_changed(path, content):
    """Escribe solo si el contenido cambió; así Git no registra cambios vacíos."""
    data = content.encode("utf-8")
    if path.exists() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True


def main():
    files = {
        ROOT / "README.md": readme(),
        ASSETS / "banners" / "header.svg": header(),
        ASSETS / "banners" / "header-mobile.svg": header_mobile(),
        ASSETS / "banners" / "stack.svg": stack(),
        ASSETS / "banners" / "stack-mobile.svg": stack_mobile(),
        ASSETS / "animations" / "terminal.svg": terminal(),
        ASSETS / "animations" / "terminal-mobile.svg": terminal(compact=True),
    }
    for n, p in enumerate(PROJECTS, 1):
        files[ASSETS / "cards" / p["file"]] = project_card(n, p)
        files[ASSETS / "cards" / mobile_name(p["file"])] = project_card_mobile(n, p)
    changed = 0
    for path, content in files.items():
        updated = write_if_changed(path, content)
        changed += updated
        print(f"{path.relative_to(ROOT).as_posix():42} {len(content.encode()) / 1024:5.1f} KB  "
              f"{'actualizado' if updated else 'sin cambios'}")
    print(f"\n{changed} de {len(files)} archivos actualizados.")


if __name__ == "__main__":
    main()
