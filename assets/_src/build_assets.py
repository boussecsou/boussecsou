#!/usr/bin/env python3
"""Generate the profile illustrations (light + dark) into ../.

Run:  python3 assets/_src/build_assets.py

GitHub READMEs allow no CSS or JS, so every visual is a standalone static SVG
loaded through <img>. Animations are CSS/SMIL inside the SVG, they honour
prefers-reduced-motion, and the fonts are generic system stacks (no external
assets). Each file is written as <name>-light.svg and <name>-dark.svg.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent

THEMES = {
    "light": dict(
        ink="#0f0f0f", muted="#6b6880", purple="#8b5cf6", purple_soft="#e4dbff",
        lime="#c6f400", card="#faf8ff", border="#e3dcf7", on_lime="#0f0f0f",
        head="#161616", head_hi="#9a9a9a", body="#222222", legs="#3d3d3d", eyes="#ffffff",
    ),
    "dark": dict(
        ink="#f2f0fa", muted="#9b98b3", purple="#a78bfa", purple_soft="#3a2c63",
        lime="#d2ff3a", card="#161b22", border="#30363d", on_lime="#0f0f0f",
        head="#5d5d68", head_hi="#d0d0d8", body="#f2f2f2", legs="#b9b9c4", eyes="#3030ff",
    ),
}

MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'


def svg(w, h, body, t, extra_css="", title=""):
    """Wrap a body in an <svg> with the shared style block."""
    css = f"""
    text {{ font-family: {MONO}; }}
    .ink {{ fill: {t['ink']}; }} .muted {{ fill: {t['muted']}; }}
    .purple {{ fill: {t['purple']}; }} .b {{ font-weight: 700; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
    @keyframes twinkle {{ 0%,100% {{ opacity: .25; }} 50% {{ opacity: 1; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    @keyframes bob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
    @keyframes eyes {{ 0%,92%,100% {{ transform: scaleY(1); }} 95% {{ transform: scaleY(.1); }} }}
    @keyframes nudge {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(6px); }} }}
    @keyframes sweep {{ from {{ transform: translateX(-200px); }} to {{ transform: translateX(%(sweep)s); }} }}
    {extra_css}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
    """
    t_tag = f"<title>{title}</title>" if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img">{t_tag}<style>{css}</style>{body}</svg>'
    )


def write(name, w, h, make, **kw):
    for mode, t in THEMES.items():
        body, css = make(t)
        out = svg(w, h, body, t, css, kw.get("title", ""))
        out = out.replace("%(sweep)s", f"{w}px")
        (OUT / f"{name}-{mode}.svg").write_text(out)


def mascot(t, x, y, s=1.0, bob=True):
    """The small pixel character, built from rectangles."""
    anim = "animation: bob 3.2s ease-in-out infinite;" if bob else ""
    return f"""
    <g transform="translate({x} {y}) scale({s})"><g style="{anim}">
      <rect x="0" y="0" width="76" height="44" rx="5" fill="{t['head']}"/>
      <rect x="0" y="0" width="76" height="8" rx="3" fill="{t['head_hi']}" opacity=".55"/>
      <g style="transform-box: fill-box; transform-origin: center; animation: eyes 4.5s infinite;">
        <rect x="16" y="20" width="11" height="11" fill="{t['eyes']}"/>
        <rect x="49" y="20" width="11" height="11" fill="{t['eyes']}"/>
      </g>
      <rect x="18" y="44" width="40" height="40" rx="6" fill="{t['body']}"/>
      <rect x="14" y="84" width="22" height="34" rx="4" fill="{t['legs']}"/>
      <rect x="40" y="84" width="22" height="34" rx="4" fill="{t['legs']}"/>
    </g></g>"""


def star(t, x, y, size=18, delay=0.0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" class="muted" '
            f'style="animation: twinkle 3s ease-in-out {delay}s infinite;">*</text>')


# ---------------------------------------------------------------- hero card
def hero(t):
    lines = [
        [("struct", "k"), (" Ali ", "i"), ("{", "p")],
        [("  string ", "k"), ("role   ", "i"), ("{ ", "p"), ('"aspiring AI systems architect"', "s"), (" };", "p")],
        [("  string ", "k"), ("based  ", "i"), ("{ ", "p"), ('"Kenitra, Morocco"', "s"), (" };", "p")],
        [("  string ", "k"), ("focus  ", "i"), ("{ ", "p"), ('"agents · security · cloud"', "s"), (" };", "p")],
        [("  bool   ", "k"), ("learning ", "i"), ("{ ", "p"), ("true", "t"), (" };", "p")],
        [("};", "p")],
    ]
    fs, cw = 20, 12.0          # font size, monospace char width
    x0, y0, lh = 78, 92, 34
    out = [f'<rect x="1" y="1" width="798" height="278" rx="16" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="2"/>',
           f'<circle cx="34" cy="30" r="7" fill="{t["purple"]}"/><circle cx="58" cy="30" r="7" fill="{t["lime"]}"/>'
           f'<circle cx="82" cy="30" r="7" fill="{t["border"]}"/>',
           f'<text x="118" y="36" font-size="16" class="muted">about.cpp</text>',
           f'<line x1="1" y1="56" x2="799" y2="56" stroke="{t["border"]}" stroke-width="2"/>']
    for n, parts in enumerate(lines):
        y = y0 + n * lh
        delay = 0.25 + n * 0.28
        spans, cx = [], x0
        pills = ""
        for txt, kind in parts:
            cls = {"k": "purple b", "i": "ink", "p": "muted", "s": "ink b", "t": "ink b"}[kind]
            if kind == "t":
                pills = (f'<rect x="{cx - 4}" y="{y - 21}" width="{len(txt) * cw + 8}" height="28" rx="6" '
                         f'fill="{t["lime"]}"/>')
            spans.append(f'<tspan class="{cls}">{txt}</tspan>')
            cx += len(txt) * cw
        out.append(
            f'<g style="animation: rise .5s ease {delay}s both;">'
            f'<text x="30" y="{y}" font-size="{fs - 2}" class="muted" opacity=".6">{n + 1}</text>{pills}'
            f'<text x="{x0}" y="{y}" font-size="{fs}" xml:space="preserve" style="white-space: pre;">{"".join(spans)}</text></g>')
    ly = y0 + 5 * lh
    out.append(f'<rect x="{x0 + 3 * cw}" y="{ly - 20}" width="11" height="26" fill="{t["lime"]}" '
               f'style="animation: blink 1.1s step-end 2.2s infinite;"/>')
    out.append(mascot(t, 690, 150, 0.9))
    out += [star(t, 640, 100, 18, 0.2), star(t, 752, 84, 14, 1.1), star(t, 600, 214, 14, 0.7)]
    return "".join(out), ""


# ------------------------------------------------------------ section label
def label(num, text):
    def make(t):
        body = f"""
        <rect x="2" y="12" width="54" height="40" rx="10" fill="{t['lime']}"/>
        <text x="29" y="40" font-size="22" text-anchor="middle" font-weight="700" fill="{t['on_lime']}">{num}</text>
        <text x="74" y="42" font-size="30" class="ink b">/ {text}</text>
        <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{t['purple']}"/><stop offset="1" stop-color="{t['purple']}" stop-opacity="0"/></linearGradient></defs>
        <rect x="{74 + 22 * (len(text) + 3)}" y="31" width="{800 - 74 - 22 * (len(text) + 3)}" height="3" rx="1.5" fill="url(#g)"/>
        """
        return body, ""
    return make


def divider(t):
    body = f"""
    <defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{t['purple']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t['purple']}"/><stop offset="1" stop-color="{t['purple']}" stop-opacity="0"/></linearGradient>
      <clipPath id="c"><rect x="0" y="0" width="800" height="24"/></clipPath></defs>
    <rect x="0" y="10" width="800" height="3" rx="1.5" fill="url(#d)" opacity=".55"/>
    <g clip-path="url(#c)"><rect x="0" y="9" width="150" height="5" rx="2.5" fill="{t['lime']}" style="animation: sweep 5s ease-in-out infinite alternate;"/></g>
    """
    return body, ""


# ------------------------------------------------------------ project cards
def card(title, desc, tags, status="in progress", private=True):
    def make(t):
        rows = "".join(
            f'<text x="40" y="{100 + i * 32}" font-size="22" class="muted">{d}</text>' for i, d in enumerate(desc))
        py = 100 + len(desc) * 32 + 16
        pill1 = (f'<rect x="40" y="{py}" width="190" height="40" rx="20" fill="{t["lime"]}"/>'
                 f'<circle cx="64" cy="{py + 20}" r="6" fill="{t["on_lime"]}" style="animation: pulse 1.8s ease-in-out infinite;"/>'
                 f'<text x="80" y="{py + 27}" font-size="20" font-weight="700" fill="{t["on_lime"]}">{status}</text>')
        pill2 = ""
        if private:
            pill2 = (f'<rect x="246" y="{py}" width="190" height="40" rx="20" fill="none" stroke="{t["purple"]}" stroke-width="2"/>'
                     f'<text x="341" y="{py + 27}" font-size="20" text-anchor="middle" class="purple">private repo</text>')
        h = py + 40 + 70
        body = (f'<rect x="1" y="1" width="798" height="{h - 2}" rx="16" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="2"/>'
                f'<rect x="1" y="1" width="10" height="{h - 2}" rx="5" fill="{t["purple"]}"/>'
                f'<text x="40" y="58" font-size="34" class="ink b">{title}</text>{rows}{pill1}{pill2}'
                f'<text x="760" y="58" font-size="30" text-anchor="end" class="muted" style="animation: twinkle 3s ease-in-out infinite;">*</text>'
                f'<text x="40" y="{h - 24}" font-size="19" class="purple">{tags}</text>')
        return body, ""
    return make


def card_height(desc):
    return 100 + len(desc) * 32 + 16 + 40 + 70


# -------------------------------------------------------------- skill tiles
def icon_agents(t):
    return (f'<g stroke="{t["purple"]}" stroke-width="4" stroke-linecap="round" fill="none">'
            f'<line x1="60" y1="34" x2="28" y2="88"/><line x1="60" y1="34" x2="92" y2="88"/><line x1="28" y1="88" x2="92" y2="88"/></g>'
            f'<circle cx="60" cy="34" r="13" fill="{t["lime"]}" stroke="{t["ink"]}" stroke-width="4"/>'
            f'<circle cx="28" cy="88" r="11" fill="{t["card"]}" stroke="{t["ink"]}" stroke-width="4"/>'
            f'<circle cx="92" cy="88" r="11" fill="{t["card"]}" stroke="{t["ink"]}" stroke-width="4"/>')


def icon_backend(t):
    return (f'<text x="60" y="76" font-size="46" font-weight="700" text-anchor="middle" fill="{t["ink"]}">{{ }}</text>'
            f'<rect x="26" y="90" width="68" height="6" rx="3" fill="{t["lime"]}"/>')


def icon_security(t):
    return (f'<path d="M60 14 L96 28 V58 C96 84 80 100 60 108 C40 100 24 84 24 58 V28 Z" fill="none" '
            f'stroke="{t["ink"]}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M42 60 L56 74 L80 46" fill="none" stroke="{t["purple"]}" stroke-width="7" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def icon_cpp(t):
    return (f'<text x="60" y="76" font-size="50" font-weight="700" text-anchor="middle" fill="{t["ink"]}">C<tspan fill="{t["purple"]}">++</tspan></text>'
            f'<rect x="26" y="90" width="68" height="6" rx="3" fill="{t["lime"]}"/>')


def icon_cloud(t):
    return (f'<path d="M34 92 C16 92 14 64 34 62 C36 40 70 34 80 56 C102 54 108 92 86 92 Z" fill="none" '
            f'stroke="{t["ink"]}" stroke-width="4" stroke-linejoin="round"/>'
            f'<circle cx="60" cy="76" r="7" fill="{t["lime"]}" stroke="{t["ink"]}" stroke-width="3"/>')


def icon_eval(t):
    rows = "".join(
        f'<rect x="22" y="{y}" width="20" height="20" rx="4" fill="{f}" stroke="{t["ink"]}" stroke-width="3.5"/>'
        f'<line x1="54" y1="{y + 10}" x2="98" y2="{y + 10}" stroke="{t["muted"]}" stroke-width="5" stroke-linecap="round"/>'
        for y, f in ((24, t["lime"]), (52, t["lime"]), (80, t["card"])))
    return rows


def tile(title, sub, icon, hands_on):
    def make(t):
        dot = (f'<circle cx="244" cy="30" r="9" fill="{t["lime"]}" stroke="{t["ink"]}" stroke-width="2" style="animation: pulse 2.4s ease-in-out infinite;"/>'
               if hands_on else
               f'<circle cx="244" cy="30" r="8" fill="none" stroke="{t["purple"]}" stroke-width="3"/>')
        body = (f'<rect x="1" y="1" width="270" height="318" rx="20" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="2"/>{dot}'
                f'<g transform="translate(76 34)">{icon(t)}</g>'
                f'<text x="136" y="212" font-size="28" text-anchor="middle" class="ink b">{title}</text>'
                + "".join(f'<text x="136" y="{248 + i * 30}" font-size="21" text-anchor="middle" class="muted">{s}</text>'
                          for i, s in enumerate(sub)))
        return body, ""
    return make


# --------------------------------------------------------------- principles
def principles(t):
    items = ["Explicit approval for sensitive actions", "Least-privilege permissions", "Clear system boundaries",
             "Testing and evaluation", "Reliability and maintainability", "AI behavior that stays controllable"]
    out = [f'<rect x="1" y="1" width="798" height="{40 + 62 * len(items) + 54}" rx="16" fill="{t["card"]}" stroke="{t["border"]}" stroke-width="2"/>']
    for i, text in enumerate(items):
        y = 62 + i * 62
        out.append(
            f'<g style="animation: rise .5s ease {0.15 + i * 0.12}s both;">'
            f'<circle cx="58" cy="{y}" r="19" fill="{t["lime"]}"/>'
            f'<path d="M49 {y} L56 {y + 8} L68 {y - 8}" fill="none" stroke="{t["on_lime"]}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<text x="96" y="{y + 9}" font-size="26" class="ink b">{text}</text></g>')
    out.append(f'<text x="40" y="{40 + 62 * len(items) + 30}" font-size="19" class="muted">priorities I work toward, not guarantees.</text>')
    return "".join(out), ""


# ------------------------------------------------------------------ buttons
def button(text, w=380):
    def make(t):
        body = (f'<rect x="2" y="2" width="{w - 4}" height="68" rx="34" fill="{t["lime"]}"/>'
                f'<text x="{(w - 56) / 2 + 10}" y="45" font-size="23" font-weight="700" text-anchor="middle" fill="{t["on_lime"]}">{text}</text>'
                f'<text x="{w - 44}" y="46" font-size="28" font-weight="700" fill="{t["on_lime"]}" style="animation: nudge 1.6s ease-in-out infinite;">→</text>')
        return body, ""
    return make


# ------------------------------------------------------------------- footer
def footer(t):
    body = (f'<line x1="0" y1="12" x2="800" y2="12" stroke="{t["border"]}" stroke-width="2"/>'
            + mascot(t, 40, 28, 0.9)
            + f'<text x="150" y="80" font-size="24" class="ink b">end of file.</text>'
              f'<text x="150" y="114" font-size="20" class="muted">bye, anomaly.</text>'
              f'<rect x="322" y="98" width="11" height="22" fill="{t["lime"]}" style="animation: blink 1.1s step-end infinite;"/>'
            + star(t, 690, 60, 20, 0.3) + star(t, 740, 100, 14, 1.3) + star(t, 620, 120, 16, 0.8))
    return body, ""


def main():
    write("hero", 800, 280, hero, title="Ali Boussecsou — about.cpp")
    for num, text in (("01", "about"), ("02", "building"), ("03", "toolbox"), ("04", "principles"), ("05", "connect")):
        write(f"label-{text}", 800, 64, label(num, text), title=text)
    write("divider", 800, 24, divider)
    sa2 = ["A voice-first AI assistant on Azure.", "Exploring controlled tool use, OAuth,", "explicit approval and secure backends."]
    cpp = ["A command line that turns typed commands", "into events: validation, bus, handlers."]
    write("card-sa2", 800, card_height(sa2), card("Savant Azurian 2", sa2, "LangGraph · Notion MCP · Azure"), title="Savant Azurian 2")
    write("card-cpp", 800, card_height(cpp), card("C++ Event System", cpp, "C++ · CMake · std::expected"), title="C++ Event System")
    for name, title, sub, icon, hands in (
        ("agents", "Agents", ["LangGraph", "tool use · MCP"], icon_agents, True),
        ("backend", "Backend", ["BFF pattern", "APIs · OAuth"], icon_backend, True),
        ("cpp", "Modern C++", ["CMake · Git", "std::expected"], icon_cpp, True),
        ("security", "Security", ["approval · access", "threat modeling"], icon_security, False),
        ("cloud", "Cloud", ["Azure", "Key Vault · ACA"], icon_cloud, False),
        ("eval", "Evaluation", ["testing agent", "behavior"], icon_eval, False),
    ):
        write(f"tile-{name}", 272, 320, tile(title, sub, icon, hands), title=title)
    write("principles", 800, 40 + 62 * 6 + 56, principles, title="Engineering principles")
    write("btn-more", 380, 72, button("more about me"), title="More about me")
    write("btn-github", 380, 72, button("github.com/boussecsou"), title="GitHub")
    write("footer", 800, 170, footer, title="end of file")
    print("done:", len(list(OUT.glob("*-light.svg"))), "pairs")


if __name__ == "__main__":
    main()
