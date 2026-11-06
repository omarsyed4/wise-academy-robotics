#!/usr/bin/env python3
"""Week 3: Math Cat, a test of the Operators blocks.

It replaced Space Dodge, which Omar turned down because it was the same lesson as Shark
Chase: arrow keys, something to collect, something to dodge, a countdown. Math Cat is a
quiz instead. The cat asks sums made from two random numbers, checks the answer, and walks
across the stage, 30 steps for every right answer. Ten right answers win.

Every mission needs an Operators block: pick random, join (one inside another), + and =,
not, times and minus inside one another, and >. The only other new blocks are Sensing's
ask and wait and answer. Students build it alone, in a blank project, with the cat that
every new project starts with, so Set up is just making three variables.

    python3 build.py

writes  Math Cat - Solution.sb3   the finished game, and a copy at docs/scratch/math-cat/math-cat.sb3
                                  for the teacher (File, then Load from your computer)

There's no Starter: like week 3's first version, it's a test, built from Create.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from scratchkit import *  # noqa: E402,F403  the block helpers read like the Scratch palette

LOW, HIGH = 1, 10          # pick random 1 to 10, so every sum is 20 or less
STEP, START = 30, 150      # the cat stands at x = Score * 30 - 150: -150 at 0, 150 at 10
WIN_ABOVE = 9              # Score > 9, so ten right answers win

# The cat every new project starts with, and its library files (sprites.json in scratch-gui)
CAT_COSTUMES = [("cat-a", "bcf454acf82e4504149f7ffe07081dbc.svg", 48, 50),
                ("cat-b", "0fb9be3e8397c983338cb71dc84d0b25.svg", 46, 53)]
CAT_SOUNDS = [("Meow", "83c36d806dc92327b9e7049a565c6bff.wav", 44100, 37376)]
BACKDROP = ("backdrop1", "cd21514d0531fdffb22204e0ec5ed84a.svg")  # the plain white one


def build():
    a = Assets()
    score, num_a, num_b = Var("Score"), Var("A"), Var("B")

    stage = new_stage([a.library_costume(BACKDROP[0], BACKDROP[1], 240, 180)])
    cat = new_sprite("Sprite1", [a.library_costume(*c) for c in CAT_COSTUMES],
                     [a.library_sound(*s) for s in CAT_SOUNDS], 1, -START, 0)
    stage["variables"] = {score.id: [score.name, 0], num_a.id: [num_a.name, 0], num_b.id: [num_b.name, 0]}
    stage["comments"]["note"] = note("SOLUTION. Everything is on the cat (Sprite1).", 20, 20)
    cat["comments"]["note"] = note("SOLUTION. Missions 1 to 4 and 6 are the first script. Mission 5 is the second.", 20, 20)

    def the_sum():
        return plus(num_a, num_b)

    emit(cat["blocks"], [
        when_flag(),
        set_var(score, 0),
        forever(
            set_var(num_a, random(LOW, HIGH)),                                       # Mission 1
            set_var(num_b, random(LOW, HIGH)),
            ask_and_wait(join(num_a, join(" + ", num_b))),                           # Mission 2
            if_(equals(answer(), the_sum()),                                         # Mission 3
                change_var(score, 1),
                say_for("Correct!", 1)),
            if_(not_(equals(answer(), the_sum())),                                   # Mission 4
                say_for(join("It was ", the_sum()), 1)),
            if_(greater_than(score, WIN_ABOVE),                                      # Mission 6
                say_for("You win!", 2),
                stop_all()),
        ),
    ], x=20, y=120)

    emit(cat["blocks"], [                                                            # Mission 5
        when_flag(),
        forever(set_x(minus(times(score, STEP), START))),
    ], x=20, y=820)

    # Only Score is on the stage. A and B would show the question twice.
    return package([stage, cat], a, monitors=[monitor(score, 5, 5)])


if __name__ == "__main__":
    out = HERE / "Math Cat - Solution.sb3"
    out.write_bytes(build())
    print(f"wrote {out.name}  ({out.stat().st_size // 1024} KB)")
    site = WEBSITE / "math-cat"
    site.mkdir(parents=True, exist_ok=True)
    (site / "math-cat.sb3").write_bytes(out.read_bytes())
    print("copied it to docs/scratch/math-cat/math-cat.sb3")
