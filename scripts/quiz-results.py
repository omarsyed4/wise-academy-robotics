#!/usr/bin/env python3
"""Reads the quiz results sheet and says who knew what, and where someone may have cheated.

    python3 scripts/quiz-results.py results.csv [--day 2026-11-20] [--bank admin/quiz-bank.json]

results.csv is the Google Sheet "Ctrl+Alt+Defeat quiz results (Responses)", downloaded with
File > Download > Comma-separated values. Columns: Timestamp, name, quiz, score, details.

The rule: only a student's FIRST try at each part counts. Later tries come after seeing the questions.

Two kinds of rows:
  v1  the 13 November quiz. It showed the right answer after every question, had a "Start over"
      button, and every "What would you do?" answer was the second option. Its first tries are the
      only scores worth anything, and even those can't tell knowing from always clicking B.
  v2  from build-quiz.mjs on. Details hold set=, time=, left= (times the student left the page),
      device=, missed= and picks=. Scores are recomputed from the picks against the hashed answers
      in docs/index.html (or --page), so an edited score shows up.

--bank adds the right answer and the explanation to each question, for going over it in class.
"""
import argparse, collections, csv, datetime, hashlib, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SIX = ['Discovery', 'Innovation', 'Impact', 'Inclusion', 'Teamwork', 'Fun']
STUDENTS = ['Abbas', 'Ali', 'Mohamed', 'Husayn', 'Haider', 'Elias', 'Mahdi', 'Ammar']

# The 13 November questions, by number, for the v1 "Missed questions 3, 7" rows.
V1 = {
    'Core Values': ['Discovery definition', 'Innovation definition', 'Impact definition', 'Inclusion definition',
                    'Teamwork definition', 'Fun definition', 'Not a Core Value (Winning)', "Champion's share (25%)",
                    'When Core Values are watched', 'Scrimmage GP scores (4, 3, 4)', 'Ali and Tangled (Innovation)',
                    'New teammate (Inclusion)'],
    'What would you do?': ['Robot stalls, second touch', "Judge asks about Ali's code", 'Spare part for another team',
                           'Teammate freezes', 'Referee says No', 'Bluetooth at the table', "Teammate's attachment idea",
                           '30 seconds left', 'What did you learn?', 'Kid alone at lunch', 'Bad round'],
}
FAST = 4  # seconds per question: anything quicker wasn't reading


def when(text):
    text = text.strip()
    for fmt in ('%m/%d/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise SystemExit(f'Unreadable timestamp: {text!r}')


def read_rows(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
    head, body = [h.lower() for h in rows[0]], rows[1:]

    def col(words, fallback):
        for i, h in enumerate(head):
            if any(w in h for w in words):
                return i
        return fallback
    c = dict(t=col(['timestamp'], 0), name=col(['name', 'student', 'who'], 1), quiz=col(['quiz', 'round', 'part'], 2),
             score=col(['score'], 3), details=col(['detail', 'missed'], 4))
    out = []
    for r in body:
        if not any(r):
            continue
        r = r + [''] * (5 - len(r))
        d = r[c['details']].strip()
        kv = dict(p.split('=', 1) for p in d.split(' | ') if '=' in p) if d.startswith('set=') else {}
        out.append(dict(t=when(r[c['t']]), name=r[c['name']].strip(), quiz=r[c['quiz']].strip(),
                        score=r[c['score']].strip(), details=d, kv=kv, v=2 if kv else 1))
    return sorted(out, key=lambda x: x['t'])


def page_bank(path):
    m = re.search(r'<script type="application/json" id="quiz-bank">(.*?)</script>', Path(path).read_text(encoding='utf-8'))
    return json.loads(m.group(1)) if m else None


def frac(s):
    m = re.match(r'\s*(\d+)\s*/\s*(\d+)', s)
    return (int(m.group(1)), int(m.group(2))) if m else (None, None)


def secs(s):
    m = re.match(r'(\d+)m(\d+)s', s or '')
    return int(m.group(1)) * 60 + int(m.group(2)) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('csv')
    ap.add_argument('--day', help='the quiz day, YYYY-MM-DD: rows from other days are flagged and left out')
    ap.add_argument('--bank', help='the coach-only bank, to print answers and explanations')
    ap.add_argument('--page', default=ROOT / 'docs' / 'index.html', help='the page the v2 quiz was built into')
    a = ap.parse_args()

    rows = read_rows(a.csv)
    if a.day:
        day = datetime.date.fromisoformat(a.day)
        other = [r for r in rows if r['t'].date() != day]
        rows = [r for r in rows if r['t'].date() == day]
        if other:
            print(f"Left out {len(other)} rows sent on other days, from: {', '.join(sorted({r['name'] for r in other}))}.\n")
    if not rows:
        raise SystemExit('No rows to read.')
    pb = page_bank(a.page)
    bank = json.loads(Path(a.bank).read_text()) if a.bank else None
    sets = list(dict.fromkeys(r['kv'].get('set', 'v1') for r in rows))
    for s in sets:
        report([r for r in rows if r['kv'].get('set', 'v1') == s], s, pb, bank, a.page)


def report(rows, set_id, pb, bank, page):
    flags = collections.defaultdict(list)
    if pb and set_id not in ('v1', pb['set']):
        print(f'# Quiz {set_id}\n\nThe page holds set {pb["set"]}, not {set_id}. Pass --page with the page this set was built into.\n')
        pb = None
    qs = {q['id']: q for r in pb['rounds'] for q in r['qs']} if pb else {}
    full = {q['id']: q for r in bank['rounds'] for q in r['qs']} if bank and bank.get('set') == set_id else {}

    def right(qid, letter):
        q = qs[qid]
        text = q['opts']['ABCD'.index(letter)]
        return hashlib.sha256(f"{pb['salt']}|{qid}|{text}".encode()).hexdigest()[:16] == q['key']

    # Group by student and part. The first row is the try that counts.
    tries = collections.defaultdict(list)
    for r in rows:
        tries[(r['name'], r['quiz'])].append(r)
    parts = list(dict.fromkeys(r['quiz'] for r in rows))
    names = [n for n in STUDENTS if any(k[0] == n for k in tries)] + sorted({k[0] for k in tries} - set(STUDENTS))

    devices = collections.defaultdict(set)
    per_q = collections.defaultdict(lambda: [0, 0, collections.Counter()])  # right, asked, wrong picks
    v1_missed = collections.defaultdict(collections.Counter)
    v1_firsts = collections.Counter()

    for (name, quiz), rs in tries.items():
        first = rs[0]
        if len(rs) > 1:
            later = ', '.join(r['score'] for r in rs[1:])
            flags[name].append(f'{quiz}: {len(rs)} tries. First {first["score"]}, then {later}. Only the first counts.')
        for r in rs:
            if r['v'] == 2:
                devices[r['kv'].get('device', '?')].add(name)
        if first['v'] == 1:
            v1_firsts[quiz] += 1
            m = re.search(r'Missed questions ([\d, ]+)', first['details'])
            for n in (int(x) for x in re.findall(r'\d+', m.group(1))) if m else []:
                v1_missed[quiz][n] += 1
            continue
        kv = first['kv']
        if int(kv.get('left', 0)):
            flags[name].append(f'{quiz}: left the quiz page {kv["left"]} time(s) during the part.')
        picks = [p.split(':') for p in kv.get('picks', '').split(',') if ':' in p]
        took = secs(kv.get('time'))
        n = len(picks) or 6
        if took is not None and took < FAST * n:
            flags[name].append(f'{quiz}: {n} questions in {kv["time"]}. Too fast to have read them.')
        if picks and qs:
            got = 0
            for qid, letter in picks:
                ok = right(qid, letter)
                got += ok
                s = per_q[qid]
                s[0] += ok
                s[1] += 1
                if not ok:
                    s[2][qs[qid]['opts']['ABCD'.index(letter)]] += 1
            if frac(first['score'])[0] != got:
                flags[name].append(f'{quiz}: sheet says {first["score"]} but the picks add up to {got}. Edited?')

    by_name = collections.defaultdict(set)
    for dev, who in devices.items():
        for n in who:
            by_name[n].add(dev)
            if len(who) > 1:
                flags[n].append(f'Same laptop as {", ".join(sorted(who - {n}))} (device {dev}).')
    for n, ds in by_name.items():
        if len(ds) > 1:
            flags[n].append(f'Sent from {len(ds)} different laptops or browsers.')
    flags = {n: list(dict.fromkeys(f)) for n, f in flags.items()}

    title = 'the 13 November quiz (v1)' if set_id == 'v1' else set_id
    span = f"{rows[0]['t']:%a %d %b %Y}" + (f" to {rows[-1]['t']:%a %d %b}" if rows[-1]['t'].date() != rows[0]['t'].date() else '')
    print(f'# Quiz results: {title}\n')
    print(f'{len(rows)} rows, {span}. First try only.\n')
    print('| Student | ' + ' | '.join(parts) + ' | Flags |')
    print('|---|' + '---|' * len(parts) + '---|')
    for n in names:
        cells = []
        for p in parts:
            rs = tries.get((n, p))
            cells.append('–' if not rs else rs[0]['score'] + (f' ({len(rs)} tries)' if len(rs) > 1 else ''))
        print(f'| {n} | ' + ' | '.join(cells) + f' | {len(flags.get(n, [])) or ""} |')
    missing = [n for n in STUDENTS if n not in names]
    if missing:
        print(f'\nNo results from: {", ".join(missing)}.')

    totals = collections.defaultdict(lambda: [0, 0])
    for (n, p), rs in tries.items():
        g, t = frac(rs[0]['score'])
        if t:
            totals[p][0] += g
            totals[p][1] += t
    print('\nTeam average, first tries: ' + ' · '.join(f'{p} {100 * g / t:.0f}%' for p, (g, t) in totals.items() if t))

    if flags:
        print('\n## Flags\n')
        for n in names:
            for f in flags.get(n, []):
                print(f'- **{n}**: {f}')

    if v1_missed:
        print('\n## Most missed, first tries\n')
        for quiz, c in v1_missed.items():
            print(f'**{quiz}** ({v1_firsts[quiz]} first tries)\n')
            for num, k in c.most_common():
                label = V1.get(quiz, [])[num - 1] if num <= len(V1.get(quiz, [])) else ''
                print(f'- Q{num} {label}: missed by {k}')
            print()
    if set_id == 'v1' and 'What would you do?' in parts:
        print('Every "What would you do?" answer on 13 November was the second option, so a full score there '
              "can't be told apart from clicking B every time. Treat that part as not measured.\n")

    if per_q:
        print('\n## Question by question, first tries, hardest first\n')
        print('| Question | Right | Most picked wrong answer |' + (' Answer |' if full else ''))
        print('|---|---|---|' + ('---|' if full else ''))
        order = sorted(per_q, key=lambda q: per_q[q][0] / per_q[q][1])
        for qid in order:
            ok, asked, wrong = per_q[qid]
            top = f'{wrong.most_common(1)[0][0]} ({wrong.most_common(1)[0][1]})' if wrong else ''
            ans = f" {full[qid]['opts'][full[qid]['answer']]} |" if qid in full else (' |' if full else '')
            print(f'| {qid}: {qs[qid]["ask"][:70]} | {ok}/{asked} | {top} |' + ans)
        if full:
            print('\n## For going over it in class\n')
            for qid in order:
                q = full.get(qid)
                if q:
                    print(f'- **{q["ask"]}** {q["opts"][q["answer"]].rstrip(".!")}. {q["why"]}')

    six = [tries[k][0] for k in tries if k[1] == 'Name all six' and tries[k][0]['v'] == 2]
    if six:
        forgot = collections.Counter()
        for r in six:
            typed = ' ' + re.sub(r'[^a-z]+', ' ', r['kv'].get('typed', '').lower()).replace('team work', 'teamwork') + ' '
            forgot.update(v for v in SIX if f' {v.lower()} ' not in typed)
        if forgot:
            print('\nName all six, forgotten or misspelled: ' + ', '.join(f'{v} ({k})' for v, k in forgot.most_common()))
            print('Check the typed words in the sheet: a near miss like "Inovation" scores zero but shows they knew it.')
    print()


if __name__ == '__main__':
    main()
