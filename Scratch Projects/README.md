# Weekly Scratch projects

One project a week, kept simple: two or three sprites, about four missions, and one example script students can copy from.

Students download the Starters from the **Scratch** tab on the team website (https://omarsyed4.github.io/wise-academy-robotics/#scratch).

| Week | Project | What it teaches |
|---|---|---|
| 01 | Firefly Catcher | when-key-pressed, forever, if touching, random positions, a Score variable |
| 02 | Deep Sea Maze | if key pressed inside a forever, touching color (with the eyedropper), glide, a script on the Stage, a stopwatch |

## What's in each week's folder

- **`<Title> - Starter.sb3`** is what students open. It has the art, sounds and sprites, plus one example script. Each sprite has a yellow note with its missions written out block by block, and the Stage's note lists the order to do them in. "Done? Try these" ideas go at the bottom of the last note.
- **`<Title> - Solution.sb3`** is the answer key: the finished game, including the try-these ideas.
- **`build.py`** generates both files, and copies the Starter to `docs/scratch/<title>.sb3` for the website. Change it and rerun it instead of editing the `.sb3` files by hand. Rebuilds are byte-identical, so Git only shows real changes.
- **`art.py`**, when there is one, holds that week's pictures and sounds.

```bash
python3 "Scratch Projects/01 Firefly Catcher/build.py"
```

`scratchkit.py` holds what every week shares: the block helpers (named after the Scratch palette), sound synthesis, notes that size themselves to their text, sprites and packaging.

To add a new week to the website: run its `build.py`, save a 640×480 picture of the stage as `docs/scratch/<title>.jpg`, and add a card at the top of the Scratch tab in `docs/index.html`. Only the Starter goes on the website. The Solution stays here, but the repo is public, so a determined student could find it.

Week 1 also has a `Full version/` folder with a harder game built from the same art. It has a 30-second timer, a bat to dodge and a TIME'S UP banner, and takes students about an hour. Use it as a follow-up week if the class is ready.

## Things learned building week 1

- The first version (six missions, four sprites, broadcasts) was too much. Aim for something a beginner finishes in about half an hour, with extras for fast students.
- Scratch notes don't grow, and students won't scroll inside one. `note()` sizes itself from its text and leaves room for Chromebook fonts.
- Scratch 3 calls the block **start sound**, not "play sound". Use the exact block names in the notes.
- `touching edge?` is easier for students than `y position < -170`. Start falling sprites low enough that they aren't already touching the top edge (y: 150 for a 44-unit-tall sprite).

## Things learned building week 2

- `touching color` only works if the walls are one flat color: no outlines, gradients or decorations on them. The maze is drawn as flat rock with water tunnels cut into it, and the thick border gives students a big target for the eyedropper.
- Put a win check that says something for 2 seconds inside the moving sprite's own forever loop. Then the sprite freezes while it celebrates. When the check sat on the Pearl, the fish could keep swimming, hit a wall and jump back to the start in the middle of "You made it!".
- The fish is about 31 × 21 in tunnels 50 wide. A scripted run at 4 steps per frame got through the whole maze without touching a wall, and the jellyfish crossing leaves about a second to get through.
- To test a game in the browser pane, package it with `@turbowarp/packager`, serve it on localhost, and press keys with `scaffolding.vm.postIOData('keyboard', {key: 'ArrowRight', isDown: true})`.
