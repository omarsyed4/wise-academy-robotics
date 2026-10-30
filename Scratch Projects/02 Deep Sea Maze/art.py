"""Week 2 art and sounds: an underwater cave maze, an anglerfish, a jellyfish and a pearl."""

import random as rnd

from scratchkit import svg, tone, wav

ROCK = "#178f8a"  # the walls are this one flat color, so "touching color" works on every part of them
WATER = "#0a1c40"
GLOW = "#d7ff3a"

# The maze is a 7 x 5 grid of 64-unit cells. Tunnels are 50 wide, leaving 14 of rock between them.
CELL, LEFT, TOP, COLS, ROWS = 64, 16, 32, 7, 5
TUNNEL = 50

# Pairs of cells (column, row) joined by a tunnel. Everything else is rock.
# The way home: down, right, down, right across the jellyfish's tunnel, then up and snake down the right side.
PASSAGES = [
    # left third, with two dead ends and a long loop along the bottom
    ((0, 0), (0, 1)), ((0, 1), (1, 1)), ((0, 1), (0, 2)), ((0, 2), (0, 3)), ((0, 3), (0, 4)),
    ((0, 4), (1, 4)), ((1, 4), (2, 4)), ((2, 4), (2, 3)), ((2, 3), (1, 3)),
    ((1, 1), (1, 0)), ((1, 0), (2, 0)), ((2, 0), (2, 1)), ((1, 1), (1, 2)), ((1, 2), (2, 2)),
    # the middle column: the jellyfish's tunnel, crossed once at row 2
    ((2, 2), (3, 2)), ((3, 0), (3, 1)), ((3, 1), (3, 2)), ((3, 2), (3, 3)), ((3, 3), (3, 4)),
    ((3, 2), (4, 2)),
    # right third: the snake to the pearl, and a dead end that ends right beside it
    ((4, 2), (4, 1)), ((4, 1), (4, 0)), ((4, 0), (5, 0)), ((5, 0), (6, 0)), ((6, 0), (6, 1)),
    ((6, 1), (5, 1)), ((5, 1), (5, 2)), ((5, 2), (6, 2)), ((6, 2), (6, 3)), ((6, 3), (6, 4)),
    ((4, 2), (4, 3)), ((4, 3), (4, 4)), ((4, 4), (5, 4)), ((5, 4), (5, 3)),
]


def cell_center(c, r):
    """Where a cell's middle is on the backdrop, in pixels from the top left."""
    return LEFT + CELL * c + CELL // 2, TOP + CELL * r + CELL // 2


def stage_xy(c, r):
    """The same spot in Scratch's x and y."""
    px, py = cell_center(c, r)
    return px - 240, 180 - py


# ---------------------------------------------------------------- art

def cave_backdrop():
    tunnels = "".join(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
        for a, b in PASSAGES
        for (x1, y1), (x2, y2) in [(cell_center(*a), cell_center(*b))]
    )

    # Specks of glowing plankton, kept well inside the tunnels so no wall pixel changes color.
    rng = rnd.Random(7)
    plankton = ""
    for c in range(COLS):
        for r in range(ROWS):
            cx, cy = cell_center(c, r)
            for _ in range(2):
                x, y = cx + rng.uniform(-15, 15), cy + rng.uniform(-15, 15)
                plankton += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rng.uniform(0.8, 1.6):.1f}" '
                             f'fill="#8ff3ff" opacity="{rng.uniform(0.25, 0.55):.2f}"/>')

    bubbles = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#8ff3ff" stroke-opacity="0.5"/>'
        for x, y, r in [(216, 10, 2.5), (226, 20, 1.6), (262, 14, 2), (300, 9, 1.4), (318, 21, 2.2)]
    )

    body = (
        f'<rect width="480" height="360" fill="{ROCK}"/>'
        '<rect width="480" height="30" fill="#050d22"/>'
        + bubbles
        + '<text x="470" y="21" text-anchor="end" font-family="Sans Serif" font-weight="bold" '
        'font-size="15" fill="#7fe9e0">DEEP SEA MAZE</text>'
        f'<g stroke="{WATER}" stroke-width="{TUNNEL}" stroke-linecap="round" fill="none">{tunnels}</g>'
        + plankton
    )
    return svg(480, 360, body)


def anglerfish():
    """A small orange anglerfish facing right, about 31 x 21 so it fits the tunnels with room to spare."""
    body = (
        '<g transform="translate(0 1)">'
        '<path d="M7 13 L1 6 Q3.5 13 1 20 Z" fill="#e5673a"/>'
        '<ellipse cx="16" cy="13" rx="10" ry="8" fill="#ff9a62"/>'
        '<path d="M9 16 Q16 22 24 16 Q16 19 9 16 Z" fill="#ffd2b0"/>'
        '<path d="M13 13 Q10 19 15.5 17.5 Z" fill="#e5673a"/>'
        '<circle cx="20" cy="10" r="3" fill="#ffffff"/><circle cx="21" cy="10" r="1.6" fill="#1b1030"/>'
        '<path d="M21.5 15.5 Q24.5 17 26 13.5" stroke="#7a2a12" stroke-width="1.2" fill="none" stroke-linecap="round"/>'
        '<path d="M22.6 15.9 L23.2 17 L23.9 15.9 M24.4 15.4 L25.1 16.4 L25.6 15" stroke="#ffffff" stroke-width="0.8" fill="none"/>'
        '<path d="M18 5.5 Q22 -0.5 28 3" stroke="#ffb38a" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
        f'<circle cx="28.5" cy="4" r="3" fill="{GLOW}"/><circle cx="27.8" cy="3.2" r="1" fill="#ffffff"/>'
        '</g>'
    )
    return svg(34, 24, body)


def jellyfish():
    tentacles = "".join(
        f'<path d="M{x} 24 Q{x - 3} 29 {x} 33 Q{x + 3} 37 {x} 42"/>' for x in (10, 16, 24, 30)
    )
    body = (
        f'<g stroke="#ff9ae3" stroke-width="2" fill="none" stroke-linecap="round">{tentacles}</g>'
        '<path d="M5 22 C5 2 35 2 35 22 Q31 25.5 27.5 22 Q24 25.5 20 22 Q16 25.5 12.5 22 Q9 25.5 5 22 Z" '
        'fill="#ff7ad9"/>'
        '<path d="M10 18 C10 11 18 8.5 24 9.5" stroke="#ffd1f2" stroke-width="2.5" fill="none" '
        'stroke-linecap="round" opacity="0.85"/>'
        '<circle cx="16" cy="16.5" r="1.4" fill="#3b0f35"/><circle cx="24" cy="16.5" r="1.4" fill="#3b0f35"/>'
        '<path d="M18 19 Q20 20.5 22 19" stroke="#3b0f35" stroke-width="1" fill="none" stroke-linecap="round"/>'
    )
    return svg(40, 46, body)


def pearl(shining):
    defs = (
        '<radialGradient id="pearl" cx="0.4" cy="0.35" r="0.7"><stop offset="0" stop-color="#ffffff"/>'
        '<stop offset="0.6" stop-color="#f4e8ff"/><stop offset="1" stop-color="#cdb8ea"/></radialGradient>'
        '<radialGradient id="halo"><stop offset="0" stop-color="#ffe9fb" stop-opacity="0.55"/>'
        '<stop offset="1" stop-color="#ffe9fb" stop-opacity="0"/></radialGradient>'
    )
    ridges_top = "".join(f'<path d="M23 21 L{x} {y}"/>' for x, y in [(11, 15), (16, 9), (23, 7), (30, 9), (35, 15)])
    ridges_bottom = "".join(f'<path d="M23 36 L{x} 23"/>' for x in (10, 16, 23, 30, 36))
    body = (
        (f'<circle cx="23" cy="19" r="17" fill="url(#halo)"/>' if shining else "")
        + '<path d="M7 21 Q23 1 39 21 Z" fill="#f3a6cf"/>'
        f'<g stroke="#d77fb0" stroke-width="1" fill="none">{ridges_top}</g>'
        '<circle cx="23" cy="19" r="7" fill="url(#pearl)"/>'
        '<circle cx="20.6" cy="16.6" r="2" fill="#ffffff"/>'
        '<path d="M5 22 L41 22 Q40 36 23 37 Q6 36 5 22 Z" fill="#e98bbd"/>'
        f'<g stroke="#c86aa0" stroke-width="1" fill="none">{ridges_bottom}</g>'
        + ('<path d="M33 6 L34 9.5 L37.5 10.5 L34 11.5 L33 15 L32 11.5 L28.5 10.5 L32 9.5 Z" fill="#ffffff"/>'
           if shining else "")
    )
    return svg(46, 40, body, defs)


# ---------------------------------------------------------------- sound

def bonk():
    return wav(tone(180, 0.16, vol=0.7, decay=16, slide_to=90))


def zap():
    return wav(tone(900, 0.09, vol=0.3, decay=4, shape="square", slide_to=500)
               + tone(700, 0.22, vol=0.3, decay=6, shape="square", slide_to=180))


def win():
    notes = [(587.3, 0.1), (784.0, 0.1), (987.8, 0.1), (1174.7, 0.1), (1568.0, 0.45)]
    out = []
    for f, d in notes:
        out += tone(f, d, decay=3 if d > 0.2 else 7)
    return wav(out)
