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

`FIRST LEGO League (BIOGLOW)/07 Team Docs/competition-playbook.html` is the editable team-doc source.
`docs/playbook.html` is its student-facing website edition. After source edits, run
`python3 scripts/sync-playbook.py`; internal staffing, logistics and coach-planning sections stay private. The tracker links
to this copy so the web playbook updates with the repo. The older Claude artifact is a separate
copy and is not automatically republished by this repository.

The [coach-call alignment review](FIRST%20LEGO%20League%20(BIOGLOW)/coach-call-alignment.md)
records the transcript cross-reference, conflicts, new insights, evidence gaps and priorities.
The supplied transcript is archived privately in `07 Team Docs/coach-connect-transcript.txt`.

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
dated evidence, continuing priorities and an optional next-session plan. Open it locally, or use the existing hosting.

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


## Updating the hub

- Update the status summaries and contributor evidence in `docs/index.html` only after checking the work. Change the **team evidence date** to match the records checked, not merely the day you edit the site.
- Keep submitted, accessible and verified work distinct. Mission values are conditional; log actual full-match results separately.
- `#lesson-plan` has no plan posted. Usually on Thursday night, replace its paragraph with a dated plan or link. Remove/archive it after that session; keep season status independent. Past 9 October notes remain linked as dated evidence and are retained in Git history.
- Board assembly on 9 October was Husayn (Robot Design) and Ammar (Innovation); this did not permanently reassign Mohamed/Mahdi's content roles or Husayn/Ammar's evidence responsibilities.
- The call review does not update Google Docs, Canva or the separate Claude artifact. Confirm completion in those tools before changing status.
