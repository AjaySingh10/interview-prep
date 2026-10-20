"""Build tracker/data.json from README.md, dsa/PROBLEMS.md and system-design/CRASH_COURSE.md.

Run from the repo root after editing the plan or problem list:
    python3 scripts/build_tracker_data.py
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YEAR = 2026
MONTHS = {"Oct": 10, "Nov": 11}
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def rows(lines):
    """Yield cell lists for markdown table rows, skipping header separators."""
    for line in lines:
        if line.startswith("|") and not re.match(r"^\|\s*:?-", line):
            yield [c.strip() for c in line.strip().strip("|").split("|")]


def iso(label):
    _, d, m = label.replace("**", "").split()[:3]
    return date(YEAR, MONTHS[m], int(d)).isoformat()


def split_items(cell):
    return [] if cell in ("–", "-", "") else [s.strip() for s in cell.split(";")]


def plan_days(readme):
    days, week = [], 0
    for line in readme:
        if line.startswith("## Week "):
            week = int(line.split()[2])
        cells = next(rows([line]), None) if line.startswith("|") else None
        if not cells or not cells[0].isdigit() or len(cells) != 7:
            continue
        n, label, dsa, _, design, other, hours = cells
        days.append({
            "day": int(n),
            "week": week,
            "label": label.replace(" **(weekend)**", ""),
            "date": iso(label),
            "weekend": "weekend" in label,
            "dsaTopic": dsa,
            "design": split_items(design),
            "other": split_items(other),
            "hours": float(hours),
        })
    return days


def problems(md):
    out, day = [], None
    for line in md:
        m = re.match(r"^### Day (\d+)", line)
        if m:
            day = int(m.group(1))
        elif line.startswith("|") and day:
            cells = next(rows([line]), None)
            if cells and len(cells) == 6 and cells[1].isdigit():
                title, url = LINK.match(cells[2]).groups()
                out.append({"n": int(cells[1]), "title": title, "url": url, "difficulty": cells[3],
                            "pattern": cells[4], "source": cells[5], "day": day})
    return out


def section(md, heading):
    start = next(i for i, l in enumerate(md) if l.startswith(heading))
    end = next((i for i in range(start + 1, len(md)) if md[i].startswith("## ")), len(md))
    return md[start:end]


def crash_course(md):
    reading = {}
    for cells in rows(section(md, "## 7.")):
        if cells[0] == "Day":
            continue
        span = [int(x) for x in re.findall(r"\d+", cells[0])]
        for d in range(span[0], span[-1] + 1):
            reading[d] = cells[3]
    designs = []
    for cells in rows(section(md, "## 5.")):
        if cells[0].isdigit():
            designs.append({"name": cells[1], "insight": cells[2], "deepDives": cells[3],
                            "planDay": cells[4], "book": cells[5]})
    checklist = [l[6:].strip() for l in section(md, "### Final-day checklist") if l.startswith("- [ ]")]
    return reading, designs, checklist


def main():
    readme = (ROOT / "README.md").read_text().splitlines()
    problems_md = (ROOT / "dsa/PROBLEMS.md").read_text().splitlines()
    course_md = (ROOT / "system-design/CRASH_COURSE.md").read_text().splitlines()
    reading, designs, checklist = crash_course(course_md)
    days = plan_days(readme)
    for d in days:
        d["read"] = reading.get(d["day"], "")
    data = {"start": days[0]["date"], "days": days, "problems": problems(problems_md),
            "designs": designs, "checklist": checklist}
    out = ROOT / "tracker/data.json"
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print(f"{out.relative_to(ROOT)}: {len(days)} days, {len(data['problems'])} problems, "
          f"{len(designs)} designs, {len(checklist)} checklist items")


if __name__ == "__main__":
    main()
