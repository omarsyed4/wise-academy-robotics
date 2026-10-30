"""Week 1 art and sounds, shared by the simple build and the full version."""

from scratchkit import svg, tone, wav

GLOW = "#d7ff3a"


# ---------------------------------------------------------------- art

def pine(x, base, h, w, fill):
    """Three stacked triangles, trunk hidden by the ground."""
    tiers = []
    for i, (top, spread) in enumerate([(0.0, 0.55), (0.28, 0.8), (0.52, 1.0)]):
        y_top = base - h + top * h
        y_bot = y_top + h * (0.48 if i < 2 else 0.5)
        half = w / 2 * spread
        tiers.append(f"M{x} {y_top:.1f} L{x + half:.1f} {y_bot:.1f} L{x - half:.1f} {y_bot:.1f} Z")
    return f'<path d="{" ".join(tiers)}" fill="{fill}"/>'


def mushroom(x, y, s, hue):
    return (
        f'<circle cx="{x}" cy="{y - 4 * s}" r="{16 * s}" fill="url(#shroomGlow{hue})"/>'
        f'<rect x="{x - 1.6 * s}" y="{y - 6 * s}" width="{3.2 * s}" height="{6 * s}" rx="1" fill="#cfe9e4"/>'
        f'<path d="M{x - 6 * s} {y - 5.5 * s} Q{x} {y - 14 * s} {x + 6 * s} {y - 5.5 * s} Z" fill="{hue}"/>'
    )


def forest_backdrop():
    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#070b1d"/><stop offset="0.6" stop-color="#14224a"/>'
        '<stop offset="1" stop-color="#22386b"/></linearGradient>'
        '<radialGradient id="moonGlow"><stop offset="0" stop-color="#fff7d6" stop-opacity="0.45"/>'
        '<stop offset="1" stop-color="#fff7d6" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#0f2a24"/><stop offset="1" stop-color="#06120f"/></linearGradient>'
    )
    for hue in ("#5ef2d6", "#a98bff"):
        defs += (
            f'<radialGradient id="shroomGlow{hue}"><stop offset="0" stop-color="{hue}" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="{hue}" stop-opacity="0"/></radialGradient>'
        )

    stars = [
        (28, 22, 1.2), (74, 58, 0.8), (118, 18, 1.0), (160, 74, 0.7), (205, 30, 1.3),
        (250, 62, 0.8), (288, 16, 1.0), (330, 48, 0.7), (352, 104, 0.9), (446, 128, 0.8),
        (60, 112, 0.9), (190, 122, 0.7), (270, 110, 1.0), (128, 150, 0.6), (300, 150, 0.7),
        (468, 30, 1.0), (14, 160, 0.7), (226, 168, 0.6), (98, 88, 0.6), (372, 22, 0.8),
    ]
    star_svg = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity="{0.35 + r * 0.4:.2f}"/>'
        for x, y, r in stars
    )

    back_trees = "".join(pine(x, 300, h, w, "#16294a") for x, h, w in [
        (30, 190, 70), (88, 150, 58), (140, 120, 50), (330, 125, 52), (384, 160, 60), (444, 200, 74),
    ])
    front_trees = "".join(pine(x, 312, h, w, "#0a1426") for x, h, w in [
        (-4, 250, 96), (58, 205, 80), (420, 215, 82), (486, 260, 100),
    ])

    body = (
        '<rect width="480" height="360" fill="url(#sky)"/>'
        + star_svg
        + '<circle cx="404" cy="62" r="54" fill="url(#moonGlow)"/>'
        '<circle cx="404" cy="62" r="21" fill="#fbf3cf"/>'
        '<circle cx="397" cy="56" r="4" fill="#ebe0b0"/><circle cx="410" cy="69" r="3" fill="#ebe0b0"/>'
        '<path d="M0 262 Q70 228 150 250 T300 244 T480 238 L480 360 L0 360 Z" fill="#101e3a"/>'
        + back_trees
        + '<path d="M0 300 Q120 290 240 298 T480 296 L480 360 L0 360 Z" fill="url(#ground)"/>'
        + front_trees
        + mushroom(120, 318, 1.0, "#5ef2d6")
        + mushroom(134, 322, 0.7, "#5ef2d6")
        + mushroom(352, 316, 0.9, "#a98bff")
        + mushroom(28, 330, 0.8, "#a98bff")
        + mushroom(458, 334, 0.8, "#5ef2d6")
        + '<path d="M0 352 Q240 340 480 352 L480 360 L0 360 Z" fill="#040b09"/>'
    )
    return svg(480, 360, body, defs)


def jar(glowing):
    defs = (
        '<linearGradient id="lid" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#c9ced8"/><stop offset="1" stop-color="#7d8594"/></linearGradient>'
    )
    inside = ""
    if glowing:
        defs += (
            f'<radialGradient id="fill" cx="0.5" cy="0.6" r="0.6"><stop offset="0" stop-color="{GLOW}" stop-opacity="0.95"/>'
            f'<stop offset="1" stop-color="{GLOW}" stop-opacity="0.15"/></radialGradient>'
        )
        inside = (
            '<rect x="10" y="20" width="44" height="56" rx="12" fill="url(#fill)"/>'
            '<circle cx="24" cy="46" r="2.5" fill="#ffffff"/><circle cx="40" cy="58" r="2" fill="#ffffff"/>'
            '<circle cx="34" cy="36" r="1.8" fill="#ffffff"/>'
        )
    body = (
        '<rect x="8" y="18" width="48" height="60" rx="13" fill="#cfe8ff" fill-opacity="0.22" '
        'stroke="#e6f4ff" stroke-opacity="0.85" stroke-width="2.5"/>'
        + inside
        + '<path d="M16 28 Q14 46 16 66" stroke="#ffffff" stroke-opacity="0.7" stroke-width="3" '
        'stroke-linecap="round" fill="none"/>'
        '<rect x="12" y="13" width="40" height="8" rx="2" fill="#aeb6c3"/>'
        '<rect x="10" y="3" width="44" height="12" rx="3" fill="url(#lid)" stroke="#5d6573" stroke-width="1.5"/>'
        '<path d="M17 5 V13 M25 5 V13 M33 5 V13 M41 5 V13 M49 5 V13" stroke="#5d6573" '
        'stroke-opacity="0.6" stroke-width="1.2"/>'
    )
    return svg(64, 80, body, defs)


def firefly(bright):
    halo = 19 if bright else 12
    core_opacity = 1 if bright else 0.7
    defs = (
        f'<radialGradient id="halo"><stop offset="0" stop-color="{GLOW}" stop-opacity="{0.8 if bright else 0.55}"/>'
        f'<stop offset="0.45" stop-color="{GLOW}" stop-opacity="{0.35 if bright else 0.2}"/>'
        f'<stop offset="1" stop-color="{GLOW}" stop-opacity="0"/></radialGradient>'
    )
    body = (
        f'<circle cx="20" cy="24" r="{halo}" fill="url(#halo)"/>'
        '<ellipse cx="13.5" cy="16" rx="6" ry="9" fill="#e9f3ff" fill-opacity="0.55" '
        'stroke="#ffffff" stroke-opacity="0.6" transform="rotate(-25 13.5 16)"/>'
        '<ellipse cx="26.5" cy="16" rx="6" ry="9" fill="#e9f3ff" fill-opacity="0.55" '
        'stroke="#ffffff" stroke-opacity="0.6" transform="rotate(25 26.5 16)"/>'
        '<ellipse cx="20" cy="15" rx="4" ry="5" fill="#3a2c22"/>'
        '<circle cx="20" cy="8.5" r="3.4" fill="#2a1f18"/>'
        '<path d="M18.5 6 Q16 2 13.5 1.5 M21.5 6 Q24 2 26.5 1.5" stroke="#2a1f18" stroke-width="1" fill="none"/>'
        f'<ellipse cx="20" cy="25" rx="4.6" ry="7" fill="{GLOW}" opacity="{core_opacity}"/>'
        '<ellipse cx="18.8" cy="23" rx="1.5" ry="3" fill="#ffffff" opacity="0.8"/>'
    )
    return svg(40, 44, body, defs)


def bat(wings_up):
    if wings_up:
        wings = (
            "M36 22 C30 10 18 2 4 6 C10 10 10 16 8 20 C14 16 20 20 22 26 Z "
            "M36 22 C42 10 54 2 68 6 C62 10 62 16 64 20 C58 16 52 20 50 26 Z"
        )
    else:
        wings = (
            "M36 18 C28 22 16 22 4 30 C12 30 12 36 10 40 C16 34 22 34 24 38 C26 30 30 26 36 24 Z "
            "M36 18 C44 22 56 22 68 30 C60 30 60 36 62 40 C56 34 50 34 48 38 C46 30 42 26 36 24 Z"
        )
    body = (
        f'<path d="{wings}" fill="#3d2f5c" stroke="#a594dc" stroke-width="1.5" stroke-linejoin="round"/>'
        '<ellipse cx="36" cy="23" rx="7" ry="9" fill="#3d2f5c" stroke="#a594dc" stroke-width="1.5"/>'
        '<path d="M31 16 L30 9 L34 14 Z M41 16 L42 9 L38 14 Z" fill="#3d2f5c" stroke="#a594dc" stroke-width="1.2"/>'
        '<circle cx="33.5" cy="20" r="1.8" fill="#ffd84d"/><circle cx="38.5" cy="20" r="1.8" fill="#ffd84d"/>'
        '<path d="M34 26 L35 28 L36 26 L37 28 L38 26" stroke="#ffffff" stroke-width="0.9" fill="none"/>'
    )
    return svg(72, 44, body)


def banner():
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GLOW}" opacity="{o}"/>'
        for x, y, r, o in [(30, 30, 3, 0.9), (290, 34, 2.5, 0.8), (46, 124, 2, 0.7),
                           (276, 120, 3, 0.9), (262, 22, 1.6, 0.6), (58, 18, 1.6, 0.6)]
    )
    body = (
        '<rect x="4" y="4" width="312" height="142" rx="22" fill="#0b1630" fill-opacity="0.94" '
        f'stroke="{GLOW}" stroke-width="4"/>'
        + dots
        + f'<text x="160" y="80" text-anchor="middle" font-family="Sans Serif" font-weight="bold" '
        f'font-size="46" fill="{GLOW}">TIME\'S UP!</text>'
        '<text x="160" y="114" text-anchor="middle" font-family="Sans Serif" font-size="18" '
        'fill="#ffffff" fill-opacity="0.85">How many did you catch?</text>'
    )
    return svg(320, 150, body)


# ---------------------------------------------------------------- sound

def chime():
    return wav(tone(1318.5, 0.11, decay=10) + tone(1975.5, 0.26, decay=9))


def screech():
    return wav(tone(520, 0.28, vol=0.35, decay=4, shape="square", slide_to=140))


def fanfare():
    notes = [(523.3, 0.13), (659.3, 0.13), (784.0, 0.13), (1046.5, 0.5)]
    out = []
    for f, d in notes:
        out += tone(f, d, decay=3 if d > 0.2 else 5)
    return wav(out)
