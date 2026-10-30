#!/usr/bin/env python3
"""Week 2: Shark Chase.

Three sprites from Scratch's own library (Fish, Shark, Starfish) and six short missions.
Swim the fish to collect starfish while the shark chases you, for 30 seconds. Every
starfish makes the shark faster. The backdrop is only decoration, so students can build
the whole thing in a blank project without downloading anything. New since week 1: if
key pressed inside a forever, point towards, go to random position, a variable used as
a number (move Score steps), and a countdown on the Stage.

The first cut also had sounds, set size and set rotation style blocks, and a shark that
sped up with an Operators sum. Omar found that "way too complex", so sizes are set in
the sprite pane, the speed-up is just Score dropped into the move block, and the rest
are Try These ideas.

    python3 build.py

writes  Shark Chase - Starter.sb3   the library sprites and backdrop, notes, one example script
        Shark Chase - Solution.sb3  the finished game: the six missions and nothing else
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from scratchkit import *  # noqa: E402,F403  the block helpers read like the Scratch palette

FISH_START = (-150, 0)
SHARK_START = (180, 120)
SPEED, SHARK_SPEED, SECONDS, SIZE = 5, 2, 30, 50

# Straight from Scratch's library (sprites.json and backdrops.json in scratch-gui), so the
# files match what students get from Choose a Sprite and Choose a Backdrop.
FISH_COSTUMES = [("Fish-a", "a9b3d163756621f8395592ad77fb9369.svg"), ("Fish-b", "7a0c31c0087f342867d4754f8dc57541.svg"),
                 ("Fish-c", "4a3478b3cdc3e8688a671be88c2775fd.svg"), ("Fish-d", "886e0bb732453eb8d3a849b4eab54943.svg")]
FISH_SOUNDS = [("Bubbles", "78b0be9c9c2f664158b886bc7e794095.wav", 44100, 180224),
               ("Ocean Wave", "c904610d770398b98872a708a2f75611.wav", 22050, 99569)]
SHARK_COSTUMES = [("Shark-a", "6c8008ae677ec51af8da5023fa2cd521.svg"), ("Shark-b", "b769db8fcbbf2609f0552db62ec1f94a.svg")]
SHARK_SOUNDS = [("Chomp", "0b1e3033140d094563248e61de4039e5.wav", 44100, 11648)]
STARFISH_COSTUMES = [("Starfish-a", "69dca6e42d45d3fef89f81de40b11bef.svg", 75, 75),
                     ("Starfish-b", "be2ca55a5688670302e7c3f79d5040d1.svg", 53, 60)]
STARFISH_SOUNDS = [("Collect", "32514c51e03db680e9c63857b840ae78.wav", 22050, 14225)]
BACKDROP = ("Underwater 1", "d3344650f594bcecdf46aa4a9441badd.svg")


# ---------------------------------------------------------------- missions

OVERVIEW = f"""
SHARK CHASE

Swim the fish around to collect starfish, and don't let the shark catch you. You have {SECONDS} seconds.

Everything here comes from Scratch's library: the Fish, Shark and Starfish sprites, and the Underwater 1 backdrop. Any backdrop works.

Click a sprite under the stage to see its missions:
1. Fish: swim with the arrow keys
2. Starfish: score a point when the fish touches it
3. Shark: chase the fish
4. Shark: chomp! The game ends when it catches you
5. Shark: get faster with every starfish
6. Stage: a {SECONDS}-second countdown (it's at the bottom of this note)

Click the green flag after each mission to test it.


MISSION 6: COUNTDOWN
1. Go to Variables, click Make a Variable, and name it Time.
2. Build this here, on the Stage. The set and change blocks start out showing Score: click the little arrow on each one and pick Time.

when green flag clicked
   set Time to {SECONDS}
   repeat {SECONDS}
      wait 1 seconds
      change Time by -1
   stop all

How many starfish can you get before time runs out?


DONE? TRY THESE
- Add sounds. Put "start sound Collect" inside the Starfish's if, and "play sound Chomp until done" just above the Shark's "stop all".
- Give yourself more time: change both {SECONDS}s in the countdown to 60.
- Add a second shark. Right-click the Shark and choose duplicate, then change where it starts.
- Change your fish. The Fish has four costumes: add "when space key pressed, next costume".
- Pick a different backdrop. The game works with any of them.
"""

FISH_TASK = f"""
FISH: MISSION 1

MISSION 1: SWIM
The right arrow already works. Click the green flag and press it.

Make the other three arrows work:
1. Right-click the "if" block in the script below and choose Duplicate. Drop the copy under it, still inside the forever.
2. Do that twice more, so you have four ifs.
3. Change the copies to:

   if <key left arrow pressed?> then
      change x by -{SPEED}

   if <key up arrow pressed?> then
      change y by {SPEED}

   if <key down arrow pressed?> then
      change y by -{SPEED}

For up and down, swap "change x" for "change y" from Motion.

Next: click the Starfish for Mission 2.
"""

STARFISH_TASK = """
STARFISH: MISSION 2

MISSION 2: COLLECT
1. Go to Variables, click Make a Variable, and name it Score.
2. Build this on the Starfish:

when green flag clicked
   set Score to 0
   forever
      if <touching Fish?> then
         change Score by 1
         go to random position

Test it: swim the fish to the starfish. It should jump somewhere new.

Next: click the Shark for Missions 3 and 4.
"""

SHARK_TASK = f"""
SHARK: MISSIONS 3, 4 AND 5

MISSION 3: CHASE
when green flag clicked
   go to x: {SHARK_START[0]} y: {SHARK_START[1]}
   forever
      point towards Fish
      move {SHARK_SPEED} steps

Test it: the shark should follow the fish everywhere.


MISSION 4: CHOMP!
Inside the forever, under "move {SHARK_SPEED} steps", add:

   if <touching Fish?> then
      stop all


MISSION 5: FASTER
Go to Variables and drag the orange Score block into the "2" of "move {SHARK_SPEED} steps", so it says:

   move Score steps

Now every starfish makes the shark 1 step faster. It waits for you to grab the first one.

Next: click the Stage for Mission 6.
"""

SOLUTION_NOTES = {
    "Stage": "SOLUTION. Mission 6.",
    "Fish": "SOLUTION. Mission 1.",
    "Starfish": "SOLUTION. Mission 2.",
    "Shark": "SOLUTION. Missions 3, 4 and 5.",
}


def build(with_code):
    a = Assets()
    score, time_left = Var("Score"), Var("Time")

    stage = new_stage([a.library_costume(BACKDROP[0], BACKDROP[1], 240, 180)])
    fish = new_sprite("Fish", [a.library_costume(n, m, 63, 45) for n, m in FISH_COSTUMES],
                      [a.library_sound(*s) for s in FISH_SOUNDS], 3, *FISH_START)
    starfish = new_sprite("Starfish", [a.library_costume(*c) for c in STARFISH_COSTUMES],
                          [a.library_sound(*s) for s in STARFISH_SOUNDS], 1, 60, -80)
    # left-right is set on the sprite, not with a block, so the shark never swims upside down
    shark = new_sprite("Shark", [a.library_costume(n, m, 150, 60) for n, m in SHARK_COSTUMES],
                       [a.library_sound(*s) for s in SHARK_SOUNDS], 2, *SHARK_START, rotation="left-right")
    for sprite in (fish, starfish, shark):
        sprite["size"] = SIZE  # students type 50 in the Size box during Set up
    shark["direction"] = -90  # facing the fish at the start
    targets = [stage, fish, starfish, shark]

    def swim(key, dx=0, dy=0):
        return if_(key_pressed(key), change_x(dx) if dx else change_y(dy))

    fish_setup = [when_flag(), go_to_xy(*FISH_START)]

    if not with_code:
        stage["comments"]["note"] = note(OVERVIEW, 20, 20)
        fish["comments"]["note"] = note(FISH_TASK, 20, 20)
        starfish["comments"]["note"] = note(STARFISH_TASK, 20, 20)
        shark["comments"]["note"] = note(SHARK_TASK, 20, 20)
        emit(fish["blocks"], [*fish_setup, forever(swim("right arrow", dx=SPEED))],
             x=20, y=fish["comments"]["note"]["height"] + 50)
        return package(targets, a, monitors=[])

    stage["variables"] = {score.id: [score.name, 0], time_left.id: [time_left.name, SECONDS]}
    for t in targets:
        t["comments"]["note"] = note(SOLUTION_NOTES[t["name"]], 20, 20)

    emit(stage["blocks"], [
        when_flag(),
        set_var(time_left, SECONDS),
        repeat(SECONDS, wait(1), change_var(time_left, -1)),
        stop_all(),
    ], x=20, y=140)

    emit(fish["blocks"], [
        *fish_setup,
        forever(
            swim("right arrow", dx=SPEED),
            swim("left arrow", dx=-SPEED),
            swim("up arrow", dy=SPEED),
            swim("down arrow", dy=-SPEED),
        ),
    ], x=20, y=140)

    emit(starfish["blocks"], [
        when_flag(),
        set_var(score, 0),
        forever(if_(touching("Fish"), change_var(score, 1), go_to_random())),
    ], x=20, y=140)

    emit(shark["blocks"], [
        when_flag(),
        go_to_xy(*SHARK_START),
        forever(
            point_towards("Fish"),
            move_steps(score),  # Mission 5: one step faster per starfish
            if_(touching("Fish"), stop_all()),
        ),
    ], x=20, y=140)

    return package(targets, a, monitors=[monitor(score, 5, 5), monitor(time_left, 100, 5)])


if __name__ == "__main__":
    write_pair(HERE, "Shark Chase", build, pieces=False)  # students pick everything from the library
