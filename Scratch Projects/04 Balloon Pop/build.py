#!/usr/bin/env python3
"""Week 4: Balloon Pop, a much simpler week after Math Cat.

Click the balloon and it pops: a Pop sound, a point, a new colour, a little smaller,
and it jumps somewhere new. That's the whole game. One sprite from Scratch's library
(Balloon1, which comes with three colours and the Pop sound), one variable, and two short
scripts, seven blocks in all. The only new block is Events' "when this sprite clicked".
Everything else (start sound, go to random position, a Score variable, next costume,
change size) the class has used or can find in a colour they know.

Four missions, each adding one or two blocks to the same script:

    1 Pop      when this sprite clicked: start sound Pop, go to random position
    2 Score    change Score by 1 when clicked; set Score to 0 when the flag is clicked
    3 Colour   next costume when clicked
    4 Smaller  change size by -5 when clicked; set size to 100 % when the flag is clicked

    python3 build.py

writes  Balloon Pop - Solution.sb3   the finished game, and a copy at docs/scratch/balloon-pop/balloon-pop.sb3
                                     for the teacher (File, then Load from your computer)

There's no Starter: students build it in a blank project from Create, picking the balloon
with Choose a Sprite.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from scratchkit import *  # noqa: E402,F403  the block helpers read like the Scratch palette

SHRINK = -5   # ten pops leave the balloon at half size; the green flag puts it back to 100 %

# Balloon1 and the Blue Sky backdrop, as Scratch's library has them (sprites.json and
# backdrops.json in scratch-gui). Balloon1's three costumes are its three colours.
BALLOON_COSTUMES = [("balloon1-a", "d7974f9e15000c16222f94ee32d8227a.svg", 32, 94),
                    ("balloon1-b", "a2516ac2b8d7a348194908e630387ea9.svg", 31, 94),
                    ("balloon1-c", "63e5aea255610f9fdf0735e1e9a55a5c.svg", 31, 94)]
BALLOON_SOUNDS = [("Pop", "83a9787d4cb6f3b7632b4ddfebf74367.wav", 44100, 1032)]
BACKDROP = ("Blue Sky", "e7c147730f19d284bcd7b3f00af19bb6.svg")


def build():
    a = Assets()
    score = Var("Score")

    stage = new_stage([a.library_costume(BACKDROP[0], BACKDROP[1], 240, 180)])
    balloon = new_sprite("Balloon1", [a.library_costume(*c) for c in BALLOON_COSTUMES],
                         [a.library_sound(*s) for s in BALLOON_SOUNDS], 1, 0, 0)
    stage["variables"] = {score.id: [score.name, 0]}
    stage["comments"]["note"] = note("SOLUTION. Everything is on the balloon (Balloon1).", 20, 20)
    balloon["comments"]["note"] = note("SOLUTION. Two scripts. Missions 1 to 4 build the click script; "
                                       "Missions 2 and 4 also add one block each to the green flag script.", 20, 20)

    emit(balloon["blocks"], [
        when_flag(),
        set_var(score, 0),            # Mission 2 · Score
        set_size(100),                # Mission 4 · Smaller
    ], x=20, y=160)

    emit(balloon["blocks"], [
        when_clicked(),               # Mission 1 · Pop
        play("Pop"),
        go_to_random(),
        change_var(score, 1),         # Mission 2 · Score
        next_costume(),               # Mission 3 · Colour
        change_size(SHRINK),          # Mission 4 · Smaller
    ], x=20, y=340)

    return package([stage, balloon], a, monitors=[monitor(score, 5, 5)])


if __name__ == "__main__":
    out = HERE / "Balloon Pop - Solution.sb3"
    out.write_bytes(build())
    print(f"wrote {out.name}  ({out.stat().st_size // 1024} KB)")
    site = WEBSITE / "balloon-pop"
    site.mkdir(parents=True, exist_ok=True)
    (site / "balloon-pop.sb3").write_bytes(out.read_bytes())
    print("copied it to docs/scratch/balloon-pop/balloon-pop.sb3")
