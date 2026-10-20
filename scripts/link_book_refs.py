"""Turn "Vol 1 ch. N" references in the guide into links to that chapter's page in the book PDF.

The PDF lives in the private repo AjaySingh10/interview-prep-books, so links only open for you.
Safe to re-run: already-linked references are left alone.
    python3 scripts/link_book_refs.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = "https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf"
# Chapter → physical PDF page, from the PDF's bookmarks.
VOL1_PAGES = {1: 5, 2: 34, 3: 42, 4: 51, 5: 71, 6: 87, 7: 110, 8: 119, 9: 132, 10: 151,
              11: 166, 12: 178, 13: 200, 14: 220, 15: 244, 16: 264}
REF = re.compile(r"(Vol 1,? )(ch\. \d+(?:(?:, |–)(?:ch\. )?\d+)*)")


def link(n, text):
    return f"[{text}]({BOOK}#page={VOL1_PAGES[int(n)]})"


def linkify_run(m):
    run = re.sub(r"(ch\. )?(\d+)", lambda x: link(x.group(2), x.group(0)), m.group(2))
    return m.group(1) + run


def main():
    path = ROOT / "system-design/CRASH_COURSE.md"
    lines = path.read_text().splitlines(keepends=True)
    # Headings stay plain so their anchors don't change; lines with links are already done.
    out = [l if l.startswith("#") or BOOK in l else REF.sub(linkify_run, l) for l in lines]
    path.write_text("".join(out))
    print(f"{path.relative_to(ROOT)}: {sum(l.count(BOOK) for l in out)} book links")


if __name__ == "__main__":
    main()
