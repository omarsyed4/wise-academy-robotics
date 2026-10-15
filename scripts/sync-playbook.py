#!/usr/bin/env python3
"""Publish the student-facing sections of the coach playbook into docs/."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
source = root / 'FIRST LEGO League (BIOGLOW)/07 Team Docs/competition-playbook.html'
page = source.read_text()
# Internal staffing assessments, registration decisions and coach planning stay in
# the private team-doc source. Only the shared preparation reference is published.
for number in (2, 4, 10, 11, 12):
    page = re.sub(rf'<section id="s{number}">.*?</section>', '', page, flags=re.S)
    page = re.sub(rf'\s*<li><a href="#s{number}">.*?</a></li>', '', page)
page = page.replace('<a href="../coach-call-alignment.md">Coach-call cross-reference</a>. ', '')
page = page.replace(' — see section 12.', '.')
page = page.replace('<a href="#s12">section 12</a>', 'the current season status')
page = page.replace(' — see section 12', '')
page = page.replace('Current event packet and official Challenge Updates', '<a href="index.html">Back to season hub</a>. Current event packet and official Challenge Updates')
(root / 'docs/playbook.html').write_text(page)
