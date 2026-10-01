#!/usr/bin/env bash
# Re-download the official FIRST LEGO League BIOGLOW materials (Founders Edition, Grades 4-8).
# These are gitignored because they run to ~1.5 GB. Source:
#   https://www.firstinspires.org/resources/library/fll/season-materials
#
#   ./scripts/fetch-materials.sh           core + judging + robot game + slides  (~300 MB)
#   ./scripts/fetch-materials.sh --video   also the 1.4 GB mission video
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SEASON="$ROOT/FIRST LEGO League (BIOGLOW)"
B="https://firstinspires.blob.core.windows.net/fll/challenge/2026-27"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
WANT_VIDEO="${1:-}"

get () { # dir  url  filename
  local dir="$SEASON/$1" out="$3"
  mkdir -p "$dir"
  if [[ -s "$dir/$out" ]]; then printf '  skip  %s\n' "$out"; return; fi
  if curl -fsSL -A "$UA" -C - --retry 3 --retry-delay 2 -o "$dir/$out" "$2"; then
    printf '  ok    %-52s %s\n' "$out" "$(du -h "$dir/$out" | cut -f1)"
  else
    printf '  FAIL  %s\n' "$out"; rm -f "$dir/$out"
  fi
}

echo "==> Core documents"
get "01 Core Documents" "$B/fll-challenge-bioglow-tmg.pdf"                      "bioglow-TEAM-MEETING-GUIDE.pdf"
get "01 Core Documents" "$B/fll-challenge-bioglow-en.pdf"                       "bioglow-ENGINEERING-NOTEBOOK.pdf"
get "01 Core Documents" "$B/fll-challenge-bioglow-rgr.pdf"                      "bioglow-ROBOT-GAME-RULEBOOK.pdf"
get "01 Core Documents" "$B/fll-challenge-bioglow-updates.pdf"                  "bioglow-challenge-updates.pdf"
get "01 Core Documents" "$B/fll-challenge-bioglow-season-overview.pdf"          "bioglow-season-overview.pdf"
get "01 Core Documents" "$B/fll-challenge-bioglow-multimedia-resources.pdf"     "bioglow-multimedia-resources.pdf"

echo "==> Judging"
get "02 Judging" "$B/fll-challenge-bioglow-rubrics-color.pdf"                   "bioglow-rubrics-COLOR.pdf"
get "02 Judging" "$B/fll-challenge-bioglow-rubrics-grayscale.pdf"               "bioglow-rubrics-grayscale.pdf"
get "02 Judging" "$B/fll-challenge-bioglow-judging-session-flowchart.pdf"       "bioglow-judging-session-flowchart.pdf"
get "02 Judging" "$B/fll-challenge-bioglow-awards.pdf"                          "bioglow-awards.pdf"
get "02 Judging" "$B/fll-challenge-bioglow-coach-mentor-nomination-print.pdf"   "bioglow-coach-mentor-nomination-print.pdf"
get "02 Judging" "$B/fll-challenge-bioglow-coach-mentor-nomination-fillable.pdf" "bioglow-coach-mentor-nomination-fillable.pdf"
get "02 Judging" "$B/fll-challenge-bioglow-participation-rules.pdf"             "bioglow-participation-rules.pdf"

echo "==> Robot game"
get "03 Robot Game" "$B/fll-challenge-bioglow-software-scoresheet.pdf"          "bioglow-SCORESHEET-software.pdf"
get "03 Robot Game" "$B/fll-challenge-bioglow-classpack-scoresheet.pdf"         "bioglow-scoresheet-classpack.pdf"
get "03 Robot Game" "$B/fll-challenge-bioglow-excel-scorer.xlsm"                "bioglow-excel-scorer.xlsm"
get "03 Robot Game" "$B/fll-challenge-bioglow-field-setup-reference-guide.pdf"  "bioglow-field-setup-reference-guide.pdf"
get "03 Robot Game" "$B/fll-challenge-bioglow-table-building-instructions.pdf"  "bioglow-table-building-instructions.pdf"
get "03 Robot Game" "$B/fll-challenge-bioglow-wireframe-grid.pdf"               "bioglow-wireframe-grid.pdf"

echo "==> Building instructions"
get "04 Building Instructions" "$B/fll-challenge-bioglow-bi-enus-eop.pdf"       "00-element-overview.pdf"
get "04 Building Instructions" "$B/fll-challenge-bioglow-bi-enus-prepack.pdf"   "00-prepack-overview.pdf"
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13; do
  get "04 Building Instructions"            "$B/fll-challenge-bioglow-bi-enus-book-$i.pdf"    "model-$i.pdf"
  get "04 Building Instructions/Text Based" "$B/fll-challenge-bioglow-text-based-bi-$i.pdf"   "model-$i-text.pdf"
done

echo "==> Session slides"
get "05 Session Slides" "$B/fll-challenge-bioglow-session-slide-intro.pptx"     "session-slide-intro.pptx"
for i in $(seq 1 12); do
  get "05 Session Slides" "$B/fll-challenge-bioglow-session-slide-$i.pptx" "session-slide-$(printf %02d "$i").pptx"
done
get "05 Session Slides" "$B/guided-mission-bioglow-11.llsp3"                    "guided-mission-bioglow-11.llsp3"

echo "==> Event resources"
get "06 Event Resources" "https://firstinspires.blob.core.windows.net/fll/first_canopy_fll_bioglow_certificatewelcome_ppt_ltr.pptx"        "welcome-certificate.pptx"
get "06 Event Resources" "https://firstinspires.blob.core.windows.net/fll/first_canopy_fll_foundersedition_bioglow_certificate_ppt_ltr.pptx" "participation-certificate.pptx"

if [[ "$WANT_VIDEO" == "--video" ]]; then
  echo "==> Mission video (1.4 GB, resumable)"
  get "03 Robot Game" "$B/fll-challenge-bioglow-robot-game-missions.mp4" "bioglow-robot-game-missions-VIDEO.mp4"
else
  echo "==> Skipping the 1.4 GB mission video. Pass --video to include it."
  echo "    Or watch it at https://youtu.be/uhZZ8O1StiQ"
fi

echo
echo "Done. Interactive rulebook: $B/interactive-rgr/index.html"
echo "Live score calculator:      https://eventhub.firstinspires.org/scoresheet"
