#!/usr/bin/env python3
"""Generate the profile illustrations into ../

Run:  python3 assets/_src/build_assets.py

GitHub READMEs allow no CSS or JS, so every visual is a standalone static SVG
loaded through <img>. Animations are CSS inside the SVG, they honour
prefers-reduced-motion, and the fonts are generic system stacks (no external
assets). Most files are written as <name>-light.svg and <name>-dark.svg; the
buttons look the same in both themes and are written once.

The mascot comes from the banner artwork: mascot-light.json and
mascot-dark.json hold the real vector shapes extracted from the banners.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent

THEMES = {
    "light": dict(
        name="light", ink="#0f0f0f", muted="#6b6880", purple="#8b5cf6", lime="#c6f400",
        card="#faf8ff", border="#e3dcf7", on_lime="#0f0f0f",
    ),
    "dark": dict(
        name="dark", ink="#f2f0fa", muted="#9b98b3", purple="#a78bfa", lime="#d2ff3a",
        card="#161b22", border="#30363d", on_lime="#0f0f0f",
    ),
}

MONO = 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace'


def svg(w, h, body, extra_css="", title=""):
    """Wrap a body in an <svg> with the shared style block."""
    css = f"""
    text {{ font-family: {MONO}; }}
    @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 0%,49% {{ opacity: 1; }} 50%,100% {{ opacity: 0; }} }}
    @keyframes twinkle {{ 0%,100% {{ opacity: .2; }} 50% {{ opacity: 1; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: .35; }} }}
    @keyframes bob {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-5px); }} }}
    @keyframes nudge {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(6px); }} }}
    @keyframes sweep {{ from {{ transform: translateX(-200px); }} to {{ transform: translateX({w}px); }} }}
    {extra_css}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
    """
    t_tag = f"<title>{title}</title>" if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img">{t_tag}<style>{css}</style>{body}</svg>'
    )


def colors(t):
    """Text colour classes for one theme."""
    return (f".ink{{fill:{t['ink']}}}.muted{{fill:{t['muted']}}}"
            f".purple{{fill:{t['purple']}}}.b{{font-weight:700}}")


def write(name, w, h, make, title="", single=False):
    modes = {"light": THEMES["light"]} if single else THEMES
    for mode, t in modes.items():
        body, css = make(t)
        out = svg(w, h, body, colors(t) + css, title)
        fname = f"{name}.svg" if single else f"{name}-{mode}.svg"
        (OUT / fname).write_text(out)


def mascot(t, x, y, height, bob=True):
    """The character from the banner, drawn from its real vector shapes."""
    m = json.loads((HERE / f"mascot-{t['name']}.json").read_text())
    s = height / m["h"]
    anim = "animation: bob 3.2s ease-in-out infinite;" if bob else ""
    return (f'<defs>{m["defs"]}</defs><style>{m["css"]}</style>'
            f'<g transform="translate({x} {y}) scale({s:.4f})"><g style="{anim}">{m["body"]}</g></g>')


def star(t, x, y, size=18, delay=0.0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" class="muted" '
            f'style="animation: twinkle 3s ease-in-out {delay}s infinite;">*</text>')


# ---------------------------------------------------------------- hero card
def hero(t):
    lines = [
        [("struct", "k"), (" Ali ", "i"), ("{", "p")],
        [("  string ", "k"), ("role   ", "i"), ("{ ", "p"), ('"aspiring AI systems architect"', "s"), (" };", "p")],
        [("  string ", "k"), ("based  ", "i"), ("{ ", "p"), ('"Morocco"', "s"), (" };", "p")],
        [("  string ", "k"), ("focus  ", "i"), ("{ ", "p"), ('"agents · governance · AI"', "s"), (" };", "p")],
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
    out += [star(t, 640, 100, 18, 0.2), star(t, 752, 84, 14, 1.1), star(t, 600, 214, 14, 0.7),
            star(t, 560, 84, 12, 1.6), star(t, 770, 150, 16, 0.5), star(t, 520, 244, 12, 2.0)]
    return "".join(out), ""


# ------------------------------------------------------------ section label
def label(num, text):
    def make(t):
        gx = 74 + 22 * (len(text) + 3)
        body = f"""
        <rect x="2" y="12" width="54" height="40" rx="10" fill="{t['lime']}"/>
        <text x="29" y="40" font-size="22" text-anchor="middle" font-weight="700" fill="{t['on_lime']}">{num}</text>
        <text x="74" y="42" font-size="30" class="ink b">/ {text}</text>
        <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{t['purple']}"/><stop offset="1" stop-color="{t['purple']}" stop-opacity="0"/></linearGradient></defs>
        <rect x="{gx}" y="31" width="{800 - gx}" height="3" rx="1.5" fill="url(#g)"/>
        {star(t, 760, 26, 18, 0.4)}
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
            + mascot(t, 40, 30, 120)
            + f'<text x="190" y="82" font-size="24" class="ink b">end of file.</text>'
              f'<text x="190" y="116" font-size="20" class="muted">bye, anomaly.</text>'
              f'<rect x="362" y="100" width="11" height="22" fill="{t["lime"]}" style="animation: blink 1.1s step-end infinite;"/>'
            + star(t, 690, 60, 20, 0.3) + star(t, 740, 100, 14, 1.3) + star(t, 620, 120, 16, 0.8)
            + star(t, 540, 50, 14, 1.8) + star(t, 770, 40, 12, 0.9))
    return body, ""


def main():
    for f in OUT.glob("*.svg"):
        if not f.name.startswith("banner-"):
            f.unlink()
    write("hero", 800, 280, hero, title="about.cpp")
    write("label-connect", 800, 64, label("@", "connect"), title="connect")
    write("label-info", 800, 64, label("+", "more info"), title="more info")
    write("btn-github", 380, 72, button("github.com/boussecsou"), title="GitHub", single=True)
    write("footer", 800, 170, footer, title="end of file")
    print("done:", len(list(OUT.glob("*.svg"))), "files")


if __name__ == "__main__":
    main()
