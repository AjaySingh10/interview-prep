"""Turn "Vol 1 ch. N" references in the guide into links to that chapter's PDF.

The chapter PDFs live in the private repo AjaySingh10/interview-prep-books, so links only open for you.
Safe to re-run: lines that already link to the book are left alone.
    python3 scripts/link_book_refs.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKS = "https://github.com/AjaySingh10/interview-prep-books/blob/main/"
CHAPTERS = {
    1: "ch01-scale-from-zero-to-millions-of-users", 2: "ch02-back-of-the-envelope-estimation",
    3: "ch03-a-framework-for-system-design-interviews", 4: "ch04-design-a-rate-limiter",
    5: "ch05-design-consistent-hashing", 6: "ch06-design-a-key-value-store",
    7: "ch07-design-a-unique-id-generator-in-distributed-systems", 8: "ch08-design-a-url-shortener",
    9: "ch09-design-a-web-crawler", 10: "ch10-design-a-notification-system",
    11: "ch11-design-a-news-feed-system", 12: "ch12-design-a-chat-system",
    13: "ch13-design-a-search-autocomplete-system", 14: "ch14-design-youtube",
    15: "ch15-design-google-drive", 16: "ch16-the-learning-continues",
}
REF = re.compile(r"(Vol 1,? )(ch\. \d+(?:(?:, |–)(?:ch\. )?\d+)*)")


def chapter_url(n):
    return f"{BOOKS}chapters/{CHAPTERS[int(n)]}.pdf"


def linkify_run(m):
    run = re.sub(r"(ch\. )?(\d+)", lambda x: f"[{x.group(0)}]({chapter_url(x.group(2))})", m.group(2))
    return m.group(1) + run


def main():
    path = ROOT / "system-design/CRASH_COURSE.md"
    lines = path.read_text().splitlines(keepends=True)
    # Headings stay plain so their anchors don't change; lines with links are already done.
    out = [l if l.startswith("#") or BOOKS in l else REF.sub(linkify_run, l) for l in lines]
    path.write_text("".join(out))
    print(f"{path.relative_to(ROOT)}: {sum(l.count(BOOKS + 'chapters/') for l in out)} chapter links")


if __name__ == "__main__":
    main()
