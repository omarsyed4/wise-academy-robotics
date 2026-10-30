#!/usr/bin/env python3
"""Week 2: Deep Sea Maze.

Three sprites, five missions. Steer an anglerfish through a cave to a pearl. The walls
and a gliding jellyfish send it back to the start, and the Stage keeps a stopwatch.
New since week 1: if key pressed inside a forever, touching color, glide, and a
script on the Stage. The fish's right-arrow script comes already built.

    python3 build.py

writes  Deep Sea Maze - Starter.sb3   art, sounds, instructions, one example script
        Deep Sea Maze - Solution.sb3  the finished game plus the try-these ideas
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from scratchkit import *  # noqa: E402,F403  the block helpers read like the Scratch palette
from art import ROCK, anglerfish, bonk, cave_backdrop, jellyfish, pearl, stage_xy, win, zap  # noqa: E402

START = stage_xy(0, 0)      # -192, 116
PEARL = stage_xy(6, 4)      # 192, -140
JELLY_TOP = stage_xy(3, 0)  # 0, 116
JELLY_BOTTOM = stage_xy(3, 4)
JELLY2 = (stage_xy(2, 4), stage_xy(0, 4))  # solution only: guards the bottom-left tunnel
SPEED = 4
WALL_SLIDERS = (49, 84, 56)  # Color, Saturation, Brightness in Scratch's color menu: close enough to ROCK to match


# ---------------------------------------------------------------- missions

OVERVIEW = f"""
DEEP SEA MAZE

Swim the little anglerfish through the cave to the pearl. If it touches a wall or the jellyfish, it goes back to the start.

Click a sprite under the stage to see its missions:
1. Fish: swim with the arrow keys
2. Fish: walls send you back
3. Pearl: sparkle, and win when the fish gets home
4. Jellyfish: float up and down, and sting
5. Stage: a stopwatch (it's at the bottom of this note)

Click the green flag after each mission to test it.


MISSION 5: STOPWATCH
1. Go to Variables, click Make a Variable, and name it Seconds.
2. Build this here, on the Stage:

when green flag clicked
   set Seconds to 0
   forever
      wait 1 seconds
      change Seconds by 1

How fast can you get home? Write down your best time, then try to beat it.


DONE? TRY THESE
- Make the jellyfish glow. In the Jellyfish, add a second green flag script: forever, change color effect by 25, wait 0.5 seconds.
- Count bumps. Make a variable called Bumps. Set it to 0 at the start, and change it by 1 every time the fish hits a wall.
- Add a second jellyfish. Right-click the Jellyfish under the stage and choose duplicate. Move it to another tunnel and change its glide blocks. The Fish needs a "touching Jellyfish2" check too.
- Too easy? Make the jellyfish glide faster (try 1 secs), or make the fish swim slower.
- Draw your own maze. Click the Backdrops tab and paint a new one. Use the same teal for the walls: the paint editor's color menu has an eyedropper too. Leave room at the start and at the pearl.
"""

FISH_TASK = f"""
FISH: MISSIONS 1 AND 2

Get the anglerfish home to the pearl. The list of all five missions is on the Stage.


MISSION 1: SWIM
The right arrow already works. Click the green flag and press it.

Make the other three arrows work:
1. Right-click the bottom "if" block in the script below and choose Duplicate. Drop the copy under it, still inside the forever.
2. Do that twice more, so you have four ifs.
3. Change the copies to:

   if <key left arrow pressed?> then
      point in direction -90
      change x by -{SPEED}

   if <key up arrow pressed?> then
      change y by {SPEED}

   if <key down arrow pressed?> then
      change y by -{SPEED}

For up and down, drag "point in direction" out of the if, and swap "change x" for "change y" from Motion.


MISSION 2: WALLS
Inside the forever, under the four ifs, add:

   if <touching color ?> then
      start sound Bonk
      go to x: {START[0]} y: {START[1]}

To set the color: click the color circle in the touching block, click the eyedropper at the bottom of the menu, then click the thick teal border on the stage. Or set the sliders to Color {WALL_SLIDERS[0]}, Saturation {WALL_SLIDERS[1]}, Brightness {WALL_SLIDERS[2]}.

Test it: bump a wall. The fish should jump back to the start.

Next: click the Pearl for Mission 3.
"""

PEARL_TASK = f"""
PEARL: MISSION 3

MISSION 3: HOME!
Part A: make the pearl sparkle. The Pearl has two costumes, shine and plain.

when green flag clicked
   go to x: {PEARL[0]} y: {PEARL[1]}
   forever
      next costume
      wait 0.3 seconds

Part B: click the Fish. Inside the Fish's forever, add:

   if <touching Pearl?> then
      start sound Win
      say I made it home! for 2 seconds
      stop all

Test it: swim the fish all the way to the pearl.

Next: click the Jellyfish for Mission 4.
"""

JELLY_TASK = f"""
JELLYFISH: MISSION 4

MISSION 4: STING!
Part A: make the jellyfish float up and down the middle tunnel.

when green flag clicked
   go to x: {JELLY_TOP[0]} y: {JELLY_TOP[1]}
   forever
      glide 2 secs to x: {JELLY_BOTTOM[0]} y: {JELLY_BOTTOM[1]}
      glide 2 secs to x: {JELLY_TOP[0]} y: {JELLY_TOP[1]}

Part B: click the Fish. Inside the Fish's forever, add:

   if <touching Jellyfish?> then
      start sound Zap
      go to x: {START[0]} y: {START[1]}

Test it: wait for the jellyfish to float past, then sneak through.

Next: click the Stage for Mission 5.
"""

SOLUTION_NOTES = {
    "Stage": "SOLUTION. Mission 5.",
    "Fish": "SOLUTION. Missions 1, 2, 3B and 4B. The Bumps counter and the Jellyfish2 check are from Try These.",
    "Pearl": "SOLUTION. Mission 3A.",
    "Jellyfish": "SOLUTION. Mission 4A. The glow script is from Try These.",
    "Jellyfish2": "SOLUTION. Try These: a second jellyfish guarding the bottom-left tunnel.",
}


def build(with_code):
    a = Assets()
    seconds, bumps = Var("Seconds"), Var("Bumps")

    stage = new_stage([a.costume("cave", cave_backdrop(), 240, 180)])
    jelly_art = a.costume("jellyfish", jellyfish(), 20, 25)
    pearl_s = new_sprite("Pearl", [a.costume("shine", pearl(True), 23, 21), a.costume("plain", pearl(False), 23, 21)],
                         [], 1, *PEARL)
    jelly = new_sprite("Jellyfish", [jelly_art], [], 2, *JELLY_TOP)
    fish = new_sprite("Fish", [a.costume("anglerfish", anglerfish(), 16, 12)],
                      [a.sound("Bonk", bonk()), a.sound("Zap", zap()), a.sound("Win", win())], 4, *START,
                      rotation="left-right")
    targets = [stage, fish, pearl_s, jelly]

    def swim(key, dx=0, dy=0, direction=None):
        turn = [point_in_direction(direction)] if direction is not None else []
        return if_(key_pressed(key), *turn, change_x(dx) if dx else change_y(dy))

    def back_to_start(*first):
        return [*first, go_to_xy(*START)]

    if not with_code:
        stage["comments"]["note"] = note(OVERVIEW, 20, 20)
        fish["comments"]["note"] = note(FISH_TASK, 20, 20)
        pearl_s["comments"]["note"] = note(PEARL_TASK, 20, 20)
        jelly["comments"]["note"] = note(JELLY_TASK, 20, 20)
        emit(fish["blocks"], [when_flag(), go_to_xy(*START), forever(swim("right arrow", dx=SPEED, direction=90))],
             x=20, y=fish["comments"]["note"]["height"] + 50)
        return package(targets, a, monitors=[])

    jelly2 = new_sprite("Jellyfish2", [jelly_art], [], 3, *JELLY2[0])
    targets.append(jelly2)
    stage["variables"] = {seconds.id: [seconds.name, 0], bumps.id: [bumps.name, 0]}
    for t in targets:
        t["comments"]["note"] = note(SOLUTION_NOTES[t["name"]], 20, 20)

    emit(stage["blocks"], [
        when_flag(),
        set_var(seconds, 0),
        forever(wait(1), change_var(seconds, 1)),
    ], x=20, y=140)

    emit(fish["blocks"], [
        when_flag(),
        go_to_xy(*START),
        set_var(bumps, 0),
        forever(
            swim("right arrow", dx=SPEED, direction=90),
            swim("left arrow", dx=-SPEED, direction=-90),
            swim("up arrow", dy=SPEED),
            swim("down arrow", dy=-SPEED),
            if_(touching_color(ROCK), *back_to_start(change_var(bumps, 1), play("Bonk"))),
            if_(touching("Pearl"), play("Win"), say_for("I made it home!", 2), stop_all()),
            if_(touching("Jellyfish"), *back_to_start(play("Zap"))),
            if_(touching("Jellyfish2"), *back_to_start(play("Zap"))),
        ),
    ], x=20, y=140)

    emit(pearl_s["blocks"], [when_flag(), go_to_xy(*PEARL), forever(next_costume(), wait(0.3))], x=20, y=140)
    emit(jelly["blocks"], [when_flag(), forever(change_effect("COLOR", 25), wait(0.5))], x=520, y=140)

    def patrol(sprite, here, there, secs):
        emit(sprite["blocks"], [
            when_flag(),
            go_to_xy(*here),
            forever(glide_to_xy(secs, *there), glide_to_xy(secs, *here)),
        ], x=20, y=140)

    patrol(jelly, JELLY_TOP, JELLY_BOTTOM, 2)
    patrol(jelly2, *JELLY2, 1.5)

    return package(targets, a, monitors=[monitor(seconds, 5, 3), monitor(bumps, 115, 3)])


if __name__ == "__main__":
    write_pair(HERE, "Deep Sea Maze", build)
