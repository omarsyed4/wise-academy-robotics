# Weekly Scratch projects

One project a week, kept simple: two or three sprites, about four missions, and one example script students can copy from.

**Build from Scratch's own library.** Use sprites, sounds and backdrops students can pick with Choose a Sprite and Choose a Backdrop, and don't make the game depend on the backdrop. Students should be able to build it in a blank project with nothing downloaded. Week 2's first version, Deep Sea Maze, was a maze whose walls were a custom backdrop, and Omar turned it down for exactly that reason. It's in Git history (commit f9d4eb8) if it's ever wanted.

Students follow the **Scratch** tab on the team website (https://omarsyed4.github.io/wise-academy-robotics/#scratch). Each week has a Set up step, every mission drawn as Scratch blocks, and an optional Starter file.

| Week | Project | What it teaches |
|---|---|---|
| 01 | Firefly Catcher | when-key-pressed, forever, if touching, random positions, a Score variable |
| 02 | Shark Chase | if key pressed inside a forever, point towards, go to random position, a variable as a block's number (`move (Score) steps`), a countdown on the Stage. All library sprites (Fish, Shark, Starfish) |

## What's in each week's folder

- **`<Title> - Starter.sb3`** is what students open. It has the art, sounds and sprites, plus one example script. Each sprite has a yellow note with its missions written out block by block, and the Stage's note lists the order to do them in. "Done? Try these" ideas go at the bottom of the last note.
- **`<Title> - Solution.sb3`** is the answer key: the finished game with the missions only. Leave the try-these ideas out. Week 2's first Solution had them built in (a second script, an Operators sum), and Omar found it "way too complex".
- **`build.py`** generates both files. For the website it also copies the Starter to `docs/scratch/<slug>.sb3`. A week with its own art (`pieces=True`, like week 1) is also split into `docs/scratch/<slug>/backdrop.svg` and one `.sprite3` per sprite, so students can use Upload Backdrop and Upload Sprite. Change it and rerun it instead of editing the `.sb3` files by hand. Rebuilds are byte-identical, so Git only shows real changes.
- **`art.py`**, when there is one, holds that week's own pictures and sounds. Library sprites don't need one. `Assets.library_costume()` and `library_sound()` take the file names from Scratch's library (scratch-gui's `sprites.json` and `backdrops.json`), download them once into `.library/` (not in Git), and pack them into the `.sb3`.

```bash
python3 "Scratch Projects/01 Firefly Catcher/build.py"
```

`scratchkit.py` holds what every week shares: the block helpers (named after the Scratch palette), sound synthesis, notes that size themselves to their text, sprites and packaging.

To add a new week to the website: run its `build.py`, save a 640×480 picture of the stage as `docs/scratch/<slug>.jpg`, and add a card at the top of the Scratch tab in `docs/index.html`. Then write that week's missions under "the code" as `<pre class="blocks">` text in [scratchblocks syntax](https://scratchblocks.github.io/), which the page draws as real Scratch blocks. Move the previous week's code into a collapsed `<details>`, like Firefly Catcher's. Only the Starter goes on the website. The Solution stays here, but the repo is public, so a determined student could find it.

Week 1 also has a `Full version/` folder with a harder game built from the same art. It has a 30-second timer, a bat to dodge and a TIME'S UP banner, and takes students about an hour. Use it as a follow-up week if the class is ready.

## Things learned building week 1

- The first version (six missions, four sprites, broadcasts) was too much. Aim for something a beginner finishes in about half an hour, with extras for fast students.
- Scratch notes don't grow, and students won't scroll inside one. `note()` sizes itself from its text and leaves room for Chromebook fonts.
- Scratch 3 calls the block **start sound**, not "play sound". Use the exact block names in the notes.
- `touching edge?` is easier for students than `y position < -170`. Start falling sprites low enough that they aren't already touching the top edge (y: 150 for a 44-unit-tall sprite).

## Things learned building week 2

- The first cut had five missions, a countdown, sounds, and `set size` and `set rotation style` blocks in every script. Omar said "way too complex". The simpler version was four missions of five to seven blocks each, with the extras as try-these ideas in words, not block pictures. Omar then asked for the timer back and "the most minimal" way to speed the shark up, which became Missions 5 and 6: drop Score into `move 2 steps`, and the Stage countdown. The shark sits still until the first starfish, which reads as a feature. On a restart it takes one step at the old score before the Starfish resets it, too small to notice.
- Library sprites are big (the Shark is 290 wide). Set up has students type 50 in each sprite's Size box instead of adding a `set size` block. On the website, say which library sprite to pick by its exact name: **Shark**, not Shark 2.
- Library sprites rotate all around by default, so a shark that points towards something on its left swims upside down. The fix is a tip on the website (Direction box → Left/Right), not a block. `build.py` sets it on the sprite for the Starter and Solution.
- Put a game-over check inside the moving sprite's own forever loop. If a sound goes before `stop all`, it has to be `play sound until done`, because `stop all` cuts sounds off.
- Sprites with no `go to` in their scripts can land somewhere else when uploaded into a blank project, so every sprite that matters to the game gets a starting position under its green flag.
- To test a game in the browser pane, package it with `@turbowarp/packager`, serve it on localhost, and press keys with `scaffolding.vm.postIOData('keyboard', {key: 'ArrowRight', isDown: true})`. Headless `scratch-vm` runs loops much faster than real time, because nothing is drawing frames.
