# WISE Academy Robotics — FIRST LEGO League

Coaching repo for **Ctrl+Alt+Defeat**, WISE Academy's FIRST LEGO League Challenge team.
Season: **BIOGLOW 2026–27**, Founders Edition, Grades 4–8.

> **Private repo.** It names eight students. Keep it that way.

## What lives here

| | |
|---|---|
| `FIRST LEGO League (BIOGLOW)/07 Team Docs/` | The competition-day playbook — procedures, judging scripts, trifold specs, rubric map |
| `scripts/fetch-materials.sh` | Re-downloads every official FIRST BIOGLOW document |

Everything else in the season folder is official FIRST material. It is gitignored because it
runs to ~1.5 GB, and it is all freely downloadable — run the fetch script instead of committing it.

## Getting set up on another machine

```bash
git clone <this repo>
cd "WISE Academy"
./scripts/fetch-materials.sh          # ~300 MB
./scripts/fetch-materials.sh --video  # adds the 1.4 GB mission video
```

## The playbook

`07 Team Docs/competition-playbook.html` is the source of truth for competition day. Open it
locally in a browser, or read the published version:

**https://claude.ai/artifact/3McC9jgD8gBL2BNkuFZ3bp**

Edit the HTML here, and it gets republished to that same URL.

## Things that live in Google Drive, not here

Google Docs cannot be version-controlled, so these stay in Drive:

- **Robotics🔥** — one folder per student, each with an engineering notebook and reflections
- **Game plans** — Red Team and Blue Team, one per practice squad
- **Trifold worksheet** — Robot Design, in Mohamed's folder
- **Test Log** (Husayn) and **Resource Log** (Ammar)
- **FLL_BIOGLOW_Friday_Lesson_Plans** — one doc per Friday through 13 November

## Season reference

- Robot game: three 2.5-minute matches, **only the best single score counts**
- Judging: 30 minutes — 2 welcome, 5+5 project, 5+5 robot design, up to 8 feedback
- Four equally weighted ranks decide Champion's: Core Values, Innovation Project, Robot Design, Robot Game
- 70 points are procedural: 20 for passing inspection inside one launch area, 50 for keeping precision tokens
- [BIOGLOW season materials](https://www.firstinspires.org/resources/library/fll/season-materials)

## The season tracker

`docs/index.html` is a static status board — roster, missions, trifold panel progress,
evidence logs, and today's action items. Open it locally, or publish it.

**Before you publish it:** GitHub Pages sites are **public on the open internet even when the
repo is private** — that only changes on GitHub Enterprise. This page names eight students and
their school. Decide that deliberately.

```bash
# makes the tracker public at https://omarsyed4.github.io/wise-academy-robotics/
gh api -X POST repos/omarsyed4/wise-academy-robotics/pages \
  -f 'source[branch]=main' -f 'source[path]=/docs'

# turns it back off
gh api -X DELETE repos/omarsyed4/wise-academy-robotics/pages
```

A private alternative that needs no decision: the tracker is also published as a
link-shared Claude Artifact, same content, not indexed and not public.
