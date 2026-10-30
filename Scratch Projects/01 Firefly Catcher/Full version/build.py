#!/usr/bin/env python3
"""Week 1, full version: Firefly Catcher with a timer, a bat, and a game-over banner.

The simple version one folder up is the one for class. This one is about an hour
of work for a student, so it works as a follow-up week.

    python3 build.py

writes  Firefly Catcher Full - Starter.sb3   art, sounds and instructions, no code
        Firefly Catcher Full - Solution.sb3  the finished game, every bonus but clones

Both come from the same art and sounds, so a change here reaches both files.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))  # scratchkit
sys.path.insert(0, str(HERE.parent))  # art

from scratchkit import *  # noqa: E402,F403  the block helpers read like the Scratch palette

from art import *  # noqa: E402,F403


# ---------------------------------------------------------------- missions

OVERVIEW = """
FIREFLY CATCHER

BIOGLOW is all about biodiversity, and fireflies have one of nature's coolest tricks: they make their own light. That's called bioluminescence.

Your job: build a game where you catch as many fireflies as you can in 30 seconds.

Your instructions are in notes like this one. Click each sprite below the stage to read its note. Do the missions in this order:

1. Jar: move with the arrow keys
2. Firefly: fall from the sky
3. Firefly: get caught and score
4. Firefly: glow
5. Stage (you're here): the 30-second timer
6. Banner: TIME'S UP!

Click the green flag after EVERY mission to test it. Don't wait until the end.

Finished early? The Bat sprite has bonus missions.
"""

STAGE_TASK = """
MISSION 5: THE TIMER

The game should end after 30 seconds.

1. Go to Variables and click "Make a Variable". Call it Time, and choose "For all sprites".
2. When the green flag is clicked, set Time to 30.
3. Use a loop that keeps going UNTIL Time = 0. Inside the loop, wait 1 second, then change Time by -1.
4. After the loop ends, broadcast a new message called: game over

Blocks you'll need:
when green flag clicked · set [Time] to · repeat until · ( ) = ( ) · wait 1 seconds · change [Time] by · broadcast

Test: click the flag and watch Time count down to 0.
"""

JAR_TASK = """
MISSION 1: MOVE THE JAR

The jar should slide left and right along the ground when you press the arrow keys.

1. When the green flag is clicked, move the jar to x: 0, y: -130.
2. Then, forever:
   - if the right arrow key is pressed, change x by 8
   - if the left arrow key is pressed, change x by -8

Blocks you'll need:
when green flag clicked · go to x: y: · forever · if < > then · key [ ] pressed? · change x by

Test: click the flag, then hold each arrow key.

Why not use "when key pressed" hats? Try it and feel the difference. The forever loop is smoother.
"""

FIREFLY_TASK = """
MISSION 2: FALL FROM THE SKY

1. When the green flag is clicked, go to a random spot at the top:
   x: (pick random -220 to 220)   y: 180
2. Forever, change y by -4.
3. Still inside the forever: if y position < -170 (it hit the ground), go back to a random spot at the top.

Test: the firefly should fall, then start again from a new place.


MISSION 3: CATCH IT

1. Go to Variables. Make a Variable called Score, For all sprites.
2. At the start of your green-flag script, set Score to 0.
3. Inside the forever, add another if: if touching Jar,
   - change Score by 1
   - start sound Chime
   - go back to a random spot at the top

Test: catch some fireflies and watch Score go up.


MISSION 4: GLOW

Real fireflies flicker. This sprite has two costumes: "bright" and "dim".

Make a SECOND green-flag script for the firefly. Forever: next costume, then wait 0.3 seconds.

A sprite can run two scripts at the same time!


MISSION 6 needs this sprite too. The instructions are in the Banner's note.
"""

BANNER_TASK = """
MISSION 6: TIME'S UP!

When the timer runs out, the Stage broadcasts "game over". EVERY sprite hears a broadcast, so two sprites can react to it.

In the Banner sprite (this one):
1. When the green flag is clicked, hide.
2. When I receive "game over":
   - show
   - go to front layer
   - play sound Times Up until done
   - stop all

In the Firefly sprite:
3. When I receive "game over": stop [other scripts in sprite], then hide. Now no one can sneak in a catch after time is up.
4. The firefly will still be hidden next game, so add show to the top of its green-flag script.

Blocks you'll need:
when green flag clicked · hide · show · when I receive [game over] · go to [front] layer · play sound until done · stop [all] · stop [other scripts in sprite]

Test: play a whole game. After 30 seconds the sign should pop up, the firefly should disappear, and Score should stop changing.

You built a whole game. Now try the bonus missions in the Bat sprite.
"""

BAT_TASK = """
BONUS MISSIONS

Do these in any order.

A. BAT ATTACK
The bat is hidden. Make it show, then fall from the sky like the firefly, but a little faster (try -6). If it touches the Jar, change Score by -2, start sound Screech, and send it back to the top. Give it a second script that flaps its wings: next costume, wait 0.15. When it receives "game over", it should stop and hide, just like the firefly.

B. FASTER AND FASTER
Make the firefly fall faster every time you catch one. Make a variable called Speed (For this sprite only), set it to 4 at the start, change y by (0 - Speed), and change Speed by 0.4 on every catch.

C. JAR FLASH
When you catch a firefly, the jar should light up for a moment. Broadcast a message called "caught" from the firefly. When the Jar receives it: switch costume to "glowing", wait 0.2, switch costume to "empty".

D. HIGH SCORE
Make a variable called High Score. When the Stage receives "game over": if Score > High Score, set High Score to Score. Do NOT reset it when the flag is clicked. It should remember your best game.

E. EXPERT: A SWARM
Use "create clone of myself" and "when I start as a clone" to have three fireflies falling at once.
"""


SOLUTION_NOTES = {
    "Stage": "SOLUTION. Mission 5 is the timer. The game-over script is bonus D (High Score).",
    "Jar": "SOLUTION. Mission 1. The second script is bonus C (Jar Flash).",
    "Firefly": "SOLUTION. Missions 2, 3, 4 and the Firefly half of 6. The Speed variable is bonus B; broadcast caught is bonus C.",
    "Banner": "SOLUTION. Mission 6.",
    "Bat": "SOLUTION. Bonus A. Bonus E (clones) is left open on purpose.",
}


def build(with_code):
    a = Assets()
    score, time, high = Var("Score"), Var("Time"), Var("High Score")
    speed = Var("Speed")
    game_over, caught = Msg("game over"), Msg("caught")

    stage = new_stage([a.costume("night forest", forest_backdrop(), 240, 180)])
    bat_s = new_sprite("Bat", [a.costume("wings up", bat(True), 36, 22), a.costume("wings down", bat(False), 36, 22)],
                   [a.sound("Screech", screech())], 1, 120, 150, visible=False)
    fly = new_sprite("Firefly", [a.costume("bright", firefly(True), 20, 22), a.costume("dim", firefly(False), 20, 22)],
                 [a.sound("Chime", chime())], 2, 0, 150)
    jar_s = new_sprite("Jar", [a.costume("empty", jar(False), 32, 40), a.costume("glowing", jar(True), 32, 40)],
                   [], 3, 0, -130)
    ban = new_sprite("Banner", [a.costume("times up", banner(), 160, 75)], [a.sound("Times Up", fanfare())],
                 4, 0, 20, visible=False)
    targets = [stage, bat_s, fly, jar_s, ban]

    if not with_code:
        # Heights measured in the editor at width 480, plus room for Chromebook fonts.
        stage["comments"]["note-overview"] = note(OVERVIEW, 20, 20, 480, 540)
        stage["comments"]["note-stage"] = note(STAGE_TASK, 530, 20, 480, 430)
        jar_s["comments"]["note-jar"] = note(JAR_TASK, 20, 20, 480, 440)
        fly["comments"]["note-fly"] = note(FIREFLY_TASK, 20, 20, 480, 800)
        ban["comments"]["note-banner"] = note(BANNER_TASK, 20, 20, 480, 670)
        bat_s["comments"]["note-bat"] = note(BAT_TASK, 20, 20, 480, 730)
        return package(targets, a, monitors=[])

    stage["variables"] = {v.id: [v.name, 0] for v in (score, time, high)}
    stage["broadcasts"] = {m.id: m.name for m in (game_over, caught)}
    fly["variables"] = {speed.id: [speed.name, 4]}

    for t in targets:
        if t["name"] in SOLUTION_NOTES:
            t["comments"]["note-solution"] = note(SOLUTION_NOTES[t["name"]], 20, 20, 480, 110)

    to_top = lambda: go_to_xy(random(-220, 220), 180)

    emit(stage["blocks"], [
        when_flag(),
        set_var(time, 30),
        repeat_until(equals(time, 0), wait(1), change_var(time, -1)),
        broadcast(game_over),
    ], x=20, y=140)
    emit(stage["blocks"], [
        when_receive(game_over),
        if_(greater_than(score, high), set_var(high, score)),
    ], x=20, y=560)

    emit(jar_s["blocks"], [
        when_flag(),
        switch_costume("empty"),
        go_to_xy(0, -130),
        forever(
            if_(key_pressed("right arrow"), change_x(8)),
            if_(key_pressed("left arrow"), change_x(-8)),
        ),
    ], x=20, y=140)
    emit(jar_s["blocks"], [
        when_receive(caught),
        switch_costume("glowing"),
        wait(0.2),
        switch_costume("empty"),
    ], x=560, y=140)

    emit(fly["blocks"], [
        when_flag(),
        show(),
        set_var(score, 0),
        set_var(speed, 4),
        to_top(),
        forever(
            change_y(minus(0, speed)),
            if_(touching("Jar"),
                change_var(score, 1),
                change_var(speed, 0.4),
                play("Chime"),
                broadcast(caught),
                to_top()),
            if_(less_than(y_position(), -170), to_top()),
        ),
    ], x=20, y=140)
    emit(fly["blocks"], [when_flag(), forever(next_costume(), wait(0.3))], x=560, y=140)
    emit(fly["blocks"], [when_receive(game_over), stop_other_scripts(), hide()], x=560, y=460)

    emit(bat_s["blocks"], [
        when_flag(),
        hide(),
        wait(2),
        to_top(),
        show(),
        forever(
            change_y(-6),
            if_(touching("Jar"),
                change_var(score, -2),
                play("Screech"),
                to_top()),
            if_(less_than(y_position(), -170), to_top()),
        ),
    ], x=20, y=140)
    emit(bat_s["blocks"], [when_flag(), forever(next_costume(), wait(0.15))], x=560, y=140)
    emit(bat_s["blocks"], [when_receive(game_over), stop_other_scripts(), hide()], x=560, y=460)

    emit(ban["blocks"], [when_flag(), hide()], x=20, y=140)
    emit(ban["blocks"], [
        when_receive(game_over),
        show(),
        go_to_front(),
        play_until_done("Times Up"),
        stop_all(),
    ], x=20, y=320)

    return package(targets, a, monitors=[monitor(score, 5, 5), monitor(time, 5, 32), monitor(high, 5, 59)])


if __name__ == "__main__":
    write_pair(HERE, "Firefly Catcher Full", build)
