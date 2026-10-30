#!/usr/bin/env python3
"""Week 1: Firefly Catcher.

Two sprites, four missions, no timer. The jar's right-arrow script comes already
built so students have a pattern to copy. The longer version is in Full version/.

    python3 build.py

writes  Firefly Catcher - Starter.sb3   art, sound, instructions, one example script
        Firefly Catcher - Solution.sb3  the finished game plus the three bonus ideas
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from scratchkit import *  # noqa: E402,F403  the block helpers read like the Scratch palette
from art import chime, firefly, forest_backdrop, jar  # noqa: E402


# ---------------------------------------------------------------- missions

OVERVIEW = """
FIREFLY CATCHER

Catch the falling fireflies in your jar!

Click a sprite under the stage to see its missions:
1. Jar: move left and right
2. Firefly: fall from the sky
3. Firefly: start over at the bottom
4. Firefly: score a point when you catch it

Click the green flag after each mission to test it.
"""

JAR_TASK = """
MISSION 1: MOVE THE JAR

The right arrow already works. Press it and watch the jar move.

Now make the LEFT arrow work:
1. Right-click the script below and choose Duplicate.
2. Change "right arrow" to "left arrow".
3. Change 20 to -20.
"""

FIREFLY_TASK = """
MISSION 2: FALL
when green flag clicked
   go to x: (pick random -200 to 200) y: 150
   forever
      change y by -4

Test it. The firefly falls, then gets stuck at the bottom.


MISSION 3: START OVER
Inside the forever, add:
   if <touching edge?> then
      go to x: (pick random -200 to 200) y: 150


MISSION 4: SCORE
1. Go to Variables and click Make a Variable. Name it Score.
2. Right under the green flag block, add: set Score to 0
3. Inside the forever, add:
   if <touching Jar?> then
      change Score by 1
      start sound Chime
      go to x: (pick random -200 to 200) y: 150


DONE? TRY THESE
- Make the firefly fall faster.
- Make it flicker: add a second green flag script that does next costume, then waits 0.3 seconds, forever.
- When Score = 10, say "You win!" and stop all.
"""

SOLUTION_NOTES = {
    "Jar": "SOLUTION. Mission 1. The right-arrow script comes with the Starter.",
    "Firefly": "SOLUTION. Missions 2, 3 and 4 in the big script. The flicker script and the You win! check are the bonus ideas.",
}


def build(with_code):
    a = Assets()
    score = Var("Score")

    stage = new_stage([a.costume("night forest", forest_backdrop(), 240, 180)])
    fly = new_sprite("Firefly", [a.costume("bright", firefly(True), 20, 22), a.costume("dim", firefly(False), 20, 22)],
                     [a.sound("Chime", chime())], 1, 0, 150)
    jar_s = new_sprite("Jar", [a.costume("empty", jar(False), 32, 40), a.costume("glowing", jar(True), 32, 40)],
                       [], 2, 0, -130)
    targets = [stage, fly, jar_s]

    def arrow(key, dx, y):
        emit(jar_s["blocks"], [when_key(key), change_x(dx)], x=20, y=y)

    if not with_code:
        stage["comments"]["note"] = note(OVERVIEW, 20, 20)
        fly["comments"]["note"] = note(FIREFLY_TASK, 20, 20)
        jar_s["comments"]["note"] = note(JAR_TASK, 20, 20)
        arrow("right arrow", 20, jar_s["comments"]["note"]["height"] + 50)
        return package(targets, a, monitors=[])

    stage["variables"] = {score.id: [score.name, 0]}
    for t in targets:
        if t["name"] in SOLUTION_NOTES:
            t["comments"]["note"] = note(SOLUTION_NOTES[t["name"]], 20, 20)

    arrow("right arrow", 20, 160)
    arrow("left arrow", -20, 280)

    to_top = lambda: go_to_xy(random(-200, 200), 150)
    emit(fly["blocks"], [
        when_flag(),
        set_var(score, 0),
        to_top(),
        forever(
            change_y(-4),
            if_(touching("_edge_"), to_top()),
            if_(touching("Jar"),
                change_var(score, 1),
                play("Chime"),
                to_top()),
            if_(equals(score, 10), say_for("You win!", 2), stop_all()),
        ),
    ], x=20, y=160)
    emit(fly["blocks"], [when_flag(), forever(next_costume(), wait(0.3))], x=560, y=160)

    return package(targets, a, monitors=[monitor(score, 5, 5)])


if __name__ == "__main__":
    write_pair(HERE, "Firefly Catcher", build)
