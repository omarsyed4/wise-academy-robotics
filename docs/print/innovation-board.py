#!/usr/bin/env python3
"""The Innovation Project trifold: one list of boxes, two outputs.

    python3 docs/print/innovation-board.py   # rewrites both outputs
    node docs/print/print.mjs                # makes the PDFs and checks every box fits

Outputs:
  1. docs/index.html, between the INNOVATION BOARD markers: the to-scale drawing in #boards.
  2. docs/print/innovation-board.html: the board at true size, one page per panel
     (left wing 12 x 36 in, centre 24 x 36 in, right wing 12 x 36 in).

Box positions are in inches on the 48 x 36 in board (folds at 12 and 36 in). The website
gets them as percentages, the print file as inches inside each panel.

Students do the work. Only put words here that a student is recorded as saying or writing,
or the team-agreed solution text. Anything nobody has written yet goes in `needs`, with who
owns it and a one-line prompt they can answer in class. When a student supplies the words,
move them into `text`, delete the need, and run both commands again.
"""
import html, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
BOARD_W, BOARD_H = 48.0, 36.0
PANELS = [("left", 0.0, 12.0), ("centre", 12.0, 24.0), ("right", 36.0, 12.0)]


def need(what, who, prompt):
    return {"what": what, "who": who, "prompt": prompt}


# ---------------------------------------------------------------- the boxes
# kind: bar | text | photo | quote | timeline | compare | keys
# state: done (recorded) | need (nothing recorded yet) | part (some recorded, some not) | check (recorded, but flagged)
# window: for photos, (caption height in) above the glue-in window
B = []

def box(**k):
    k.setdefault("state", "done")
    k.setdefault("who", [])
    k.setdefault("needs", [])
    k.setdefault("pt", 18)
    B.append(k)

# ---- LEFT WING ---------------------------------------------------------------
box(kind="bar", x=.75, y=.75, w=10.5, h=1.4, label="1 · IDENTIFY")

box(kind="text", x=.75, y=2.55, w=10.5, h=2.8, label="PROBLEM STATEMENT", accent=True, state="check",
    who=["Mahdi"], pt=34,
    text="We are working together to find an innovative solution to help protect forests and the animals that depend on them.",
    flag=("This says our goal, not the problem. Judges look for a clear definition of the problem.", "Mahdi",
          "Rewrite it as the problem: what is happening to forests, and who it hurts. One sentence."))

box(kind="photo", x=.75, y=5.65, w=5.1, h=5.0, label="Photo of the problem", caption="Taken in class, 25 September",
    state="need", needs=[need("print it from Drive", "Ammar", "The photo from 25 Sep is in Drive. Print it at the size shown.")])

box(kind="text", x=6.15, y=5.65, w=5.1, h=5.0, label="Why it matters", who=["Mahdi"], pt=20, state="check",
    text="<b>Habitat destruction:</b> animals lose their homes and food when trees are cut down.<br>"
         "<b>Soil erosion:</b> without tree roots, rain washes the soil away.<br>"
         "<b>Disrupted food chains:</b> when species lose their food, others struggle.<br>"
         "<b>Loss of pollinators:</b> forests find it harder to grow back.",
    web="Habitat destruction<br>Soil erosion<br>Disrupted food chains<br>Loss of pollinators",
    flag=("Mahdi's own note: trim to 2–3.", "Mahdi", "Cross out the points you wouldn't say out loud. Keep 2 or 3."))

for i, (x, name) in enumerate([(.75, "National Geographic Education · “Deforestation”"),
                                (4.35, "WWF · “Deforestation and forest degradation”"),
                                (7.95, "World Health Organization · “Biodiversity” fact sheet")], 1):
    short = ["National Geographic · Deforestation", "WWF · Deforestation and forest degradation",
             "WHO · Biodiversity fact sheet"][i - 1]
    box(kind="text", x=x, y=10.95, w=3.3, h=2.9, label=f"Source {i}", narrow=True, state="part", who=["Mahdi"], pt=18,
        text=name, web=short,
        needs=[need("what it told us", "Mahdi + Ammar",
                    "What is one thing this website told us? One line, in your own words.")])

box(kind="photo", x=.75, y=14.15, w=3.1, h=3.1, label="Our expert", caption="Mr. Hussain", narrow=True, cap=.8,
    state="need", needs=[need("print his photo", "Ammar",
                              "Print the photo you held up in the interview. Don't upload it to the website.")])

box(kind="text", x=4.15, y=14.15, w=7.1, h=3.1, label="The expert we talked to", state="part", who=["Ammar", "Mahdi"], pt=21,
    text="<b>Our expert, Mr. Hussain</b>, told us forests are cut down to build roads, homes, malls and supermarkets, "
         "and for wood to build houses and to cook.",
    web="Our expert, Mr. Hussain. Forests are cut down for roads, homes, malls, supermarkets, and wood to build and cook.",
    needs=[need("his job", "Mahdi", "What does Mr. Hussain do for work, and how does he know about forests?")])

box(kind="bar", x=.75, y=18.0, w=10.5, h=1.4, label="2 · DESIGN")

TIMELINE = [  # (date, what, done?)
    ("25 Sep", "Picked deforestation. Photographed the problem.", True),
    ("9 Oct", "Board day: first drafts, sources written down.", True),
    ("24 Oct", "Presented at the scrimmage, Montverde Academy.", True),
    ("30 Oct", "Mock interviews. Talking points and board draft.", True),
    ("13 Nov", "Full rounds. Built this board.", True),
    ("5 Dec", "Qualifier.", False),
]
box(kind="timeline", x=.75, y=19.8, w=10.5, h=6.2, label="Our project plan", state="part", pt=24,
    needs=[need("3 dates", "Mahdi + Ammar",
                "When did we talk to our expert, share with the Red team, and run the survey? Check your notebooks.")])

STUDENTS = ["Abbas", "Ali", "Mohamed", "Husayn", "Haider", "Elias", "Mahdi", "Ammar"]
for n, name in enumerate(STUDENTS):
    x = [.75, 3.45, 6.15, 8.85][n % 4]
    y = [26.4, 30.8][n // 4]
    box(kind="photo", x=x, y=y, w=2.4, h=2.6, label=name, narrow=True, cap=.42, student=True, state="need",
        needs=[need("photo", "Elias",
                    "A photo of " + name + " working (Elias's 9 Oct photos). Fallback: Mohamed's headshot.")])
    box(kind="quote", x=x, y=y + 2.7, w=2.4, h=1.1, label="Quote", narrow=True, pt=16, state="need", student_of=name,
        needs=[need("quote", name, "One sentence, about 10 words: what I did on the Innovation Project.")])

# ---- CENTRE -----------------------------------------------------------------
box(kind="keys", x=12.75, y=.75, w=22.5, h=6.0, label="Ctrl+Alt+Defeat")

box(kind="bar", x=12.75, y=7.75, w=22.5, h=1.4, label="3 · CREATE")

SOLUTION = ("When a tree has to come down, plant two new trees for every one, before the cutting starts. "
            "Where you can, cut it only halfway and leave the trunk standing, so animals still have a home "
            "while the new trees grow.")
box(kind="text", x=12.75, y=9.55, w=22.5, h=4.0, label="OUR SOLUTION", accent=True, state="part", who=["Team"], pt=42,
    text=SOLUTION, name_slot=True,
    needs=[need("its name", "Mahdi + Ammar",
                "“Forest Guardian” (Mahdi's draft) or another name? Decide together, then everyone uses it.")])

box(kind="photo", x=12.75, y=13.95, w=16.0, h=14.0, label="Our solution, drawn and labelled",
    caption="Arrows point at each part", cap=.95, state="need",
    needs=[need("the drawing", "Mahdi",
                "Draw our solution. Label every part with an arrow: what's cut, what's left standing, what's planted, and when. "
                "Abbas or Elias can help in Tinkercad.")])

STEPS = [("1 · Before cutting", "Plant two new trees for every tree that has to come down."),
         ("2 · When cutting", "Where you can, cut it only halfway and leave the trunk standing."),
         ("3 · While they grow", "Animals still have a home in the trunk while the new trees grow.")]
for i, (lab, txt) in enumerate(STEPS):
    extra = ""
    if i == 0:
        extra = "<br><span class='sub'>Companies that cut trees for wood and houses carry seeds and plant new ones every time they cut.</span>"
    box(kind="text", x=29.15, y=[13.95, 18.7, 23.45][i], w=6.1, h=4.25, label="How it works · " + lab,
        who=["Team"] + (["Mahdi"] if i == 0 else []), pt=27, text=txt + extra,
        web=txt + (" Companies that cut trees carry seeds and plant every time they cut." if i == 0 else ""))

COMPARE = [("People plant trees back after they cut.", "Two new trees for every one, planted <b>before</b> the cutting starts."),
           ("People protest and ask builders to stop.", "Something hands-on: if you cut a tree, you plant more."),
           ("Whole trees are cut down.", "Cut only halfway. The trunk left standing is still a home for animals. "
                                         "Cutting half is a new idea our whole team discussed.")]
box(kind="compare", x=12.75, y=28.35, w=22.5, h=6.9, label="What already exists → What we made, and what is new",
    who=["Mahdi", "Ammar"], pt=30, accent=True)

# ---- RIGHT WING -------------------------------------------------------------
box(kind="bar", x=36.75, y=.75, w=10.5, h=1.4, label="4 · ITERATE")

SHARED = [("The Red team", None, "Ammar", "On what date did we show our idea to the Red team?"),
          ("Our expert, Mr. Hussain", None, "Mahdi", "On what date did we talk to Mr. Hussain?"),
          ("Judges at the scrimmage", "Sat 24 Oct · Montverde Academy", None, None)]
for i, (who_, date, owner, prompt) in enumerate(SHARED):
    box(kind="text", x=[36.75, 40.35, 43.95][i], y=2.55, w=3.3, h=3.2, label=f"Shared with #{i+1}", narrow=True, pt=20,
        state="part" if owner else "done", who=["Ammar", "Mahdi"] if i < 2 else [],
        text=f"<b>{who_}</b>" + (f"<br>{date}" if date else ""), web=who_ + (f" · {date}" if date else ""),
        needs=[need("date", owner, prompt)] if owner else [])

box(kind="text", x=36.75, y=6.05, w=10.5, h=1.45, label="What they said #1", pt=20, state="need",
    needs=[need("Red team's words + name", "Elias", "What did the Red team say about our idea? One sentence, and who said it.")])
box(kind="text", x=36.75, y=7.7, w=10.5, h=1.45, label="What they said #2", pt=19, who=["Mahdi"],
    text="“If you cut a tree halfway, animals can use what's left as a home.” <span class='by'>— our expert, Mr. Hussain</span>",
    web="“If you cut a tree halfway, animals can use what's left as a home.” Our expert, Mr. Hussain")
box(kind="text", x=36.75, y=9.35, w=10.5, h=1.45, label="What they said #3", pt=20, state="need",
    needs=[need("a judge's words", "Elias", "What did a scrimmage judge say about our project? One sentence.")])

box(kind="photo", x=36.75, y=11.25, w=4.8, h=4.6, label="BEFORE", caption="Cut the whole tree and plant more.",
    cap=1.3, pt=20, who=["Mahdi"], state="need",
    needs=[need("sketch", "Ammar", "Sketch the old idea: a whole tree cut down, new trees planted afterwards.")])
box(kind="photo", x=42.45, y=11.25, w=4.8, h=4.6, label="AFTER",
    caption="Also cut only halfway: animals can use what's left as a home.", cap=1.3, pt=20, who=["Mahdi"], state="need",
    needs=[need("sketch", "Ammar", "Sketch the new idea: a half-cut trunk with animals using it, two young trees beside it.")])

box(kind="text", x=36.75, y=16.0, w=10.5, h=1.25, label="The change we made from feedback", pt=20, state="check",
    who=["Mahdi"], inline=True,
    text="Our expert said a half-cut tree is still a home, so we added cutting only halfway.",
    flag=("Ammar tells it differently: a teammate said a half-cut tree is already dead, so we changed to planting two. "
          "Don't print until you agree which happened.", "Mahdi + Ammar",
          "Which happened, and in what order? Agree one story, then both tell it the same way."))

box(kind="bar", x=36.75, y=18.0, w=10.5, h=1.4, label="5 · COMMUNICATE")
box(kind="text", x=36.75, y=19.8, w=10.5, h=2.8, label="Who it helps", who=["Mahdi"], pt=34,
    text="Animals and plants · Local communities · Farmers · Future generations")
box(kind="text", x=36.75, y=22.9, w=10.5, h=3.5, label="What changes for them", accent=True, who=["Mahdi"], pt=38,
    text="Protects animal habitats and biodiversity, so animals don't lose their homes.")
box(kind="photo", x=36.75, y=26.8, w=10.5, h=8.45, label="TEAM PHOTO", caption="All eight of us", state="need",
    needs=[need("team photo", "Elias + everyone", "All eight together, in team shirts, looking proud. Elias takes it.")])


# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=True)

def strip(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def pct(v, total):
    return f"{v / total * 100:.3f}%"

def window(b):
    """The glue-in area of a photo frame, in inches relative to the box."""
    cap = b.get("cap", .85)
    return .1, cap, b["w"] - .2, b["h"] - cap - .1

def fmt_in(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------- website
def web_box(b):
    style = (f'left:{pct(b["x"], BOARD_W)};top:{pct(b["y"], BOARD_H)};'
             f'width:{pct(b["w"], BOARD_W)};height:{pct(b["h"], BOARD_H)}')
    k = b["kind"]
    if k == "bar":
        return f'<div class="bbar" style="{style}">{b["label"]}</div>'
    if k == "keys":
        return ('<div class="bkey" style="left:32.708%;top:2.778%;width:8.333%;height:7.222%">Ctrl</div>'
                '<div class="bkey" style="left:43.958%;top:2.778%;width:7.083%;height:7.222%">Alt</div>'
                '<div class="bkey blue" style="left:53.958%;top:2.778%;width:13.333%;height:7.222%">Defeat</div>'
                '<div class="bplus" style="left:42.500%;top:6.389%" aria-hidden="true">+</div>'
                '<div class="bplus" style="left:52.500%;top:6.389%" aria-hidden="true">+</div>'
                '<div class="btitle" style="left:26.562%;top:10.417%;width:46.875%;height:5.833%">INNOVATION PROJECT</div>'
                '<div class="binfo" style="left:26.562%;top:16.528%;width:46.875%;height:2.222%">Our problem: DEFORESTATION · '
                'WISE Academy · Orlando, Florida · FIRST LEGO League Challenge · BIOGLOW 2026–27</div>')

    cls = ["bx", "photo" if k == "photo" else "box"]
    if b.get("accent"): cls.append("accent")
    if b.get("narrow"): cls.append("narrow")
    st = b["state"]
    cls.append({"done": "done", "part": "done part", "check": "done check", "need": "need"}[st])

    head = f'<b>{esc(b["label"])}</b>'
    small = b["h"] < 1.6 or b.get("student") or b.get("narrow")   # no room for a needs line: the tag goes in the header
    tags = ""
    if st in ("done", "part", "check") and k != "photo":
        tags += '<span class="tick" aria-label="recorded">✓</span>'
    if b["w"] >= 6:
        for w in b["who"]:
            if w != "Team":
                tags += f'<span class="pill recorded">{w}</span>'
    if b.get("flag"):
        tags += '<span class="pill chk">Check</span>'
    if small and k != "quote":
        for n in b["needs"]:
            tags += f'<span class="pill needp">{n["who"] if b["h"] < 1.6 else n["what"].split(" ")[-1] + " · " + n["who"]}</span>'
    if tags:
        head += f'<span class="btags">{tags}</span>'

    body = ""
    title = [b["label"]]
    if k == "timeline":
        body = ('<p class="real tl">' + " · ".join(f"<span class='d'>{d}</span> {strip(t).split('.')[0]}" for d, t, _ in TIMELINE) + "</p>")
        title.append("; ".join(f"{d}: {strip(t)}" for d, t, _ in TIMELINE))
    elif k == "compare":
        body = ('<div class="cmp"><span class="ch">What already exists</span><span class="ch">What we made, and what is new</span>'
                + "".join(f"<span>{strip(a)}</span><span>{strip(c)}</span>" for a, c in COMPARE) + "</div>")
        title += [f"{strip(a)} → {strip(c)}" for a, c in COMPARE]
    elif k == "photo":
        wx, wy, ww, wh = window(b)
        if b.get("caption") and not b.get("student"):
            body += f'<p class="real">{b["caption"]}</p>'
            title.append(b["caption"])
        title.append(f"Print the photo at {fmt_in(ww)} × {fmt_in(wh)} in")
    elif b.get("text"):
        txt = b.get("web", b["text"])
        if b.get("name_slot"):
            txt = "<span class='nm'>Name: Mahdi + Ammar decide</span> " + txt
        body += f'<p class="real">{txt}</p>'
        title.append(strip(b["text"]))

    if b.get("flag"):
        note, owner, prompt = b["flag"]
        title.append(f"Check ({owner}): {note} {prompt}")
    for n in b["needs"]:
        if not small:
            body += f'<p class="need">Needs {n["what"]} · <i>{n["who"]}</i></p>'
        title.append(f'Needs {n["what"]}, from {n["who"]}: {n["prompt"]}')
    if b["who"]:
        title.append("Recorded from: " + ", ".join(b["who"]))

    out = (f'<div class="{" ".join(cls)}" style="{style}" title="{esc(" · ".join(title))}">'
           f'<div class="bh">{head}</div>{body}</div>')
    if k == "compare":
        out += '<div class="bvline" style="left:50.000%;top:83.194%;height:13.889%"></div>'
    if b["label"] == "BEFORE":
        out += '<div class="barrow" style="left:87.500%;top:37.639%" aria-hidden="true">→</div>'
    return out


def web_board():
    parts = ['<div class="bscroll"><div class="bd" role="img" aria-label="Innovation Project board, drawn to scale">',
             '<div class="bfold" style="left:25.000%"></div><div class="bfold" style="left:75.000%"></div>']
    parts += [web_box(b) for b in B]
    parts.append("</div></div>")
    return "".join(parts) + "\n    " + web_todo()


def todo():
    """Everything still to come, grouped by the student who owns it."""
    owners = {}
    def add(who, item):
        owners.setdefault(who, []).append(item)
    for b in B:
        for n in b["needs"]:
            if b.get("student") or b["kind"] == "quote":
                continue
            add(n["who"], (b["label"], n["what"], n["prompt"]))
        if b.get("flag"):
            note, who, prompt = b["flag"]
            add(who, (b["label"], "check", prompt))
    return owners


def web_todo():
    o = todo()
    order = ["Mahdi", "Mahdi + Ammar", "Ammar", "Elias", "Elias + everyone"]
    rows = []
    for who in order:
        items = "".join(f"<li><b>{esc(lab)}:</b> {esc(prompt)}</li>" for lab, what, prompt in o.get(who, []))
        rows.append(f"<div><h4>{who}</h4><ul>{items}</ul></div>")
    rows.append("<div><h4>Everyone</h4><ul><li><b>Your quote</b> (the strip under your photo): one sentence, about "
                "10 words, about what you did on the Innovation Project.</li><li><b>Your photo</b>: Elias has the "
                "9 October photos of us working. If yours isn't there, Mohamed's headshot is the fallback.</li></ul></div>")
    return ('<div class="bfix"><div class="bfix-h"><h4>Still to come before it prints</h4>'
            '<span><a class="btn" href="print/innovation-print-list.pdf" target="_blank" rel="noopener">Print list (Letter)</a> '
            '<a class="btn" href="print/innovation-board.pdf" target="_blank" rel="noopener">Board at true size (PDF)</a></span></div>'
            '<div class="bfix-g">' + "".join(rows) + "</div></div>")


# ---------------------------------------------------------------- print
def credit(b):
    names = [w for w in b["who"] if w != "Team"]
    return f'<span class="cr">{" · ".join(names)}</span>' if names else ""

def slot(n, big=False):
    return (f'<div class="slot{" big" if big else ""}"><span>To add: {esc(n["what"])} · {esc(n["who"])}</span></div>')

def print_box(b, ox):
    k = b["kind"]
    x = b["x"] - ox
    style = f'left:{x:.3f}in;top:{b["y"]:.3f}in;width:{b["w"]:.3f}in;height:{b["h"]:.3f}in'
    if k == "bar":
        return f'<div class="bar" style="{style}">{b["label"]}</div>'
    if k == "keys":
        def key(t, l, w, blue=False):
            return f'<div class="key{" blue" if blue else ""}" style="left:{l:.2f}in;top:1.0in;width:{w:.2f}in;height:2.6in">{t}</div>'
        return (key("Ctrl", 15.7 - ox, 4.0) + key("Alt", 21.1 - ox, 3.4) + key("Defeat", 25.9 - ox, 6.4, True)
                + f'<div class="plus" style="left:{20.4 - ox:.2f}in;top:2.3in">+</div>'
                + f'<div class="plus" style="left:{25.2 - ox:.2f}in;top:2.3in">+</div>'
                + f'<div class="title" style="left:{12.75 - ox}in;top:3.75in;width:22.5in;height:2.1in">INNOVATION PROJECT</div>'
                + f'<div class="info" style="left:{12.75 - ox}in;top:5.95in;width:22.5in;height:.8in">Our problem:&nbsp;<b>DEFORESTATION</b>&nbsp;'
                  ' · WISE Academy · Orlando, Florida · FIRST LEGO League Challenge · BIOGLOW 2026–27</div>')

    cls = ["bx", k]
    if b.get("accent"): cls.append("accent")
    inner = ""
    fs = f'style="font-size:{b["pt"]}pt"'

    if k == "photo":
        wx, wy, ww, wh = window(b)
        cap = f'<b class="lab">{b["label"]}</b>'
        if b.get("caption") and not b.get("student"):
            cap += f'<span class="capt" {fs}>{b["caption"]}</span>'
        inner = (f'<div class="caprow" style="height:{wy:.2f}in">{cap}{credit(b) if b["who"] else ""}</div>'
                 f'<div class="win" style="left:{wx}in;top:{wy}in;width:{ww:.2f}in;height:{wh:.2f}in">'
                 f'<span>Glue {"photo" if "sketch" not in b["needs"][0]["what"] and "drawing" not in b["needs"][0]["what"] else b["needs"][0]["what"]} here'
                 f'<br><b>{fmt_in(ww)} × {fmt_in(wh)} in</b></span></div>')
    elif k == "quote":
        inner = f'<div class="q" {fs}>“<span class="qslot">{b["student_of"]}: to add</span>”</div>'
    elif k == "timeline":
        rows = "".join(f'<div class="tr{"" if done else " future"}"><span class="dot"></span><b>{d}</b><span>{t}</span></div>'
                       for d, t, done in TIMELINE)
        inner = (f'<b class="lab">{b["label"]}</b><div class="tl" {fs}>{rows}</div>'
                 + slot(b["needs"][0]).replace("To add: 3 dates", "To add to the line: dates we talked to our expert, "
                                                "shared with the Red team, ran the survey"))
    elif k == "compare":
        rows = "".join(f'<div class="ca">{a}</div><div class="arr">→</div><div class="cb">{c}</div>' for a, c in COMPARE)
        inner = (f'<b class="lab">{b["label"]}</b>'
                 f'<div class="cmp" {fs}><div class="ch">What already exists</div><div></div>'
                 f'<div class="ch">What we made, and what is new</div>{rows}</div>{credit(b)}')
    else:
        txt = b.get("text", "")
        head = f'<b class="lab">{b["label"]}</b>'
        if b.get("name_slot"):
            head = (f'<div class="lrow"><b class="lab">{b["label"]}:</b>'
                    f'<span class="nameslot">name · Mahdi + Ammar decide</span></div>')
        if b.get("inline"):
            inner = f'<div class="txt" {fs}><b class="lab il">{b["label"]}:</b> {txt}</div>'
        else:
            inner = head + (f'<div class="txt" {fs}>{txt}</div>' if txt else "")
        for n in b["needs"]:
            if b.get("name_slot"):
                continue
            inner += slot(n, big=not txt)
        inner += credit(b)
    return f'<div class="{" ".join(cls)}" style="{style}">{inner}</div>'


PRINT_CSS = """
@page left{size:12in 36in;margin:0}
@page centre{size:24in 36in;margin:0}
@page right{size:12in 36in;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff}
body{font-family:"Open Sans",Arial,sans-serif;color:#14213D;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.panel{position:relative;height:36in;overflow:hidden;break-after:page;background:#fff}
.panel:last-child{break-after:auto}
.left{page:left;width:12in}.centre{page:centre;width:24in}.right{page:right;width:12in}
.bar{position:absolute;display:flex;align-items:center;padding-left:.32in;background:#2F6FDE;color:#fff;border-radius:.06in;
  font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:44pt;letter-spacing:.01em}
.bx{position:absolute;overflow:hidden;border:2px solid #C3CBDA;border-radius:.08in;padding:.14in .18in;display:flex;flex-direction:column;background:#fff}
.bx.accent{border:4px solid #1F8A5B}
.bx.accent > .lab,.bx.accent .lrow .lab{color:#1F8A5B}
.lab{display:block;font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:24pt;line-height:1.1;color:#14213D}
.lab.il{display:inline;font-size:inherit}
.txt{margin-top:.08in;line-height:1.28}
.txt .sub{display:block;margin-top:.12in;font-size:.78em;color:#33415C}
.txt .by{white-space:nowrap;font-weight:700}
.cr{position:absolute;right:.14in;bottom:.05in;font-size:12pt;font-weight:700;color:#7A879E}
.slot{flex:1 1 auto;min-height:.38in;margin:.1in 0 .2in;border:2px dashed #C3CBDA;border-radius:.06in;display:flex;align-items:flex-end;padding:.04in .1in}
.slot span{font-size:11pt;font-style:italic;color:#9AA5B8}
.lrow{display:flex;align-items:baseline;gap:.2in}
.nameslot{flex:1;border-bottom:2px dashed #9AA5B8;font-size:11pt;font-style:italic;color:#9AA5B8;padding-bottom:.02in}
.photo{padding:0}
.caprow{position:absolute;left:.12in;right:.12in;top:0;display:flex;flex-direction:column;justify-content:center}
.caprow .capt{line-height:1.2;margin-top:.04in}
.photo .lab{font-size:22pt}
.win{position:absolute;border:2px dashed #9AA5B8;background:#F4F6FA;display:flex;align-items:center;justify-content:center;text-align:center}
.win span{font-size:13pt;color:#9AA5B8;line-height:1.35}
.quote{padding:.08in .12in;justify-content:center}
.q{line-height:1.2;font-weight:600;color:#9AA5B8}
.qslot{font-size:11pt;font-style:italic;font-weight:400}
.tl{position:relative;margin-top:.18in;display:flex;flex-direction:column;gap:.12in}
.tl::before{content:"";position:absolute;left:.11in;top:.2in;bottom:.2in;border-left:4px solid #14213D}
.tr{position:relative;display:grid;grid-template-columns:.42in 1.5in 1fr;align-items:baseline;line-height:1.25}
.tr .dot{width:.26in;height:.26in;border-radius:50%;background:#1F8A5B;align-self:center;position:relative;z-index:1}
.tr.future .dot{background:#fff;border:4px solid #14213D}
.tr b{font-family:Montserrat,Arial,sans-serif;font-weight:800}
.cmp{margin-top:.16in;display:grid;grid-template-columns:1fr .7in 1.3fr;gap:.22in .1in;line-height:1.25;align-items:center}
.cmp .ch{font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:17pt;text-transform:uppercase;letter-spacing:.04em;color:#55657F}
.cmp .ca{color:#33415C}
.cmp .cb{font-weight:700;color:#14213D;border-left:5px solid #1F8A5B;padding-left:.14in}
.cmp .arr{font-size:28pt;font-weight:800;color:#8A96AD;text-align:center}
.key{position:absolute;display:flex;align-items:center;justify-content:center;background:#EEF1F6;border:.08in solid #14213D;border-radius:.3in;
  box-shadow:0 .1in 0 #14213D;font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:90pt;color:#14213D}
.key.blue{color:#2F6FDE}
.plus{position:absolute;transform:translate(-50%,-50%);font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:72pt;color:#8A96AD}
.title{position:absolute;display:flex;align-items:center;justify-content:center;white-space:nowrap;font-family:Montserrat,Arial,sans-serif;font-weight:800;font-size:118pt;letter-spacing:-.01em}
.info{position:absolute;display:flex;align-items:center;justify-content:center;font-size:24pt;white-space:nowrap}
.arrow{position:absolute;transform:translate(-50%,-50%);font-size:40pt;font-weight:800;color:#8A96AD}
"""


def print_board():
    out = ["<!doctype html>",
           "<!-- GENERATED by docs/print/innovation-board.py. Edit that file, not this one.",
           "     Print with: node docs/print/print.mjs  (one page per panel, true size, and a fit check) -->",
           '<html lang="en"><head><meta charset="utf-8"><title>Innovation board · true size</title>',
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap">',
           f"<style>{PRINT_CSS}</style></head><body>"]
    for name, ox, w in PANELS:
        out.append(f'<section class="panel {name}" data-panel="{name}">')
        for b in B:
            cx = b["x"] + b["w"] / 2
            if ox <= cx < ox + w:
                out.append(print_box(b, ox))
                if b["label"] == "BEFORE":
                    out.append(f'<div class="arrow" style="left:{42.0 - ox}in;top:13.55in">→</div>')
        out.append("</section>")
    out.append("</body></html>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- write
def main():
    (ROOT / "docs/print/innovation-board.html").write_text(print_board(), encoding="utf-8")
    idx = ROOT / "docs/index.html"
    s = idx.read_text(encoding="utf-8")
    start, end = "<!-- INNOVATION BOARD: generated by docs/print/innovation-board.py -->", "<!-- /INNOVATION BOARD -->"
    a, z = s.index(start) + len(start), s.index(end)
    s = s[:a] + "\n    " + web_board() + "\n    " + s[z:]
    idx.write_text(s, encoding="utf-8")
    print(f"{len(B)} boxes · wrote docs/print/innovation-board.html and the #boards drawing in docs/index.html")


if __name__ == "__main__":
    main()
