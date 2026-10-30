Team photos. Name them to match `docs/index.html`:

abbas.jpg · ali.jpg · mohamed.jpg · husayn.jpg · haider.jpg · elias.jpg · mahdi.jpg · ammar.jpg

Square crops look best — they are masked to a circle at 52px. Until a file exists,
the card falls back to the student's initials, so missing photos never break the page.

Phone photos carry GPS location in their metadata. Crop and re-save them (which drops it)
before committing, and check with `exiftool` or PIL that nothing is left.
