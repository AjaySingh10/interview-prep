# Interview Prep — SDE2 → Senior (3 weeks)

A focused 3-week plan to switch jobs as an SDE2 with 5.5 years of experience, covering **DSA** and **system design** (HLD + LLD). Runs **Wed 21 Oct → Tue 10 Nov 2026**.

| | |
| --- | --- |
| **DSA** | 105 problems — all of [Grind 75](https://www.techinterviewhandbook.org/grind75/) + 30 extras, grouped by pattern → [`dsa/PROBLEMS.md`](dsa/PROBLEMS.md) |
| **System design** | Crash course mapped to Alex Xu [Vol 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf) & 2 → [`system-design/CRASH_COURSE.md`](system-design/CRASH_COURSE.md) |
| **Tracker** | Interactive web tracker (status, time, notes, redo queue, hours, synced to GitHub) → [tracker](tracker/); the original Excel is still in [`tracker/interview_prep_tracker.xlsx`](tracker/interview_prep_tracker.xlsx) |
| **Time budget** | ~3.5 h on weekdays, ~7 h on weekends (~94 h total), roughly 50/50 DSA vs design |

## Repo structure

```
.
├── README.md                     ← you are here: plan + how to use the repo
├── dsa/
│   ├── PROBLEMS.md               ← day-by-day problem list with LeetCode links
│   └── solutions/                ← (add) your solutions, one file per problem
├── system-design/
│   ├── CRASH_COURSE.md           ← principles, patterns, top 16 problems, reading map
│   └── notes/                    ← (add) one file per design you practise
└── tracker/
    └── interview_prep_tracker.xlsx
```

## Why this shape

At 5.5 YOE, interviewers expect DSA to be solid and system design to be strong, with you driving the discussion. Most loops also include a low-level design or machine-coding round, so LLD is folded into the design track. Behavioral and project deep-dives get a slot in Week 3 because they are often what separates SDE2 from senior offers.

## Week 1 — Rebuild fundamentals

Patterns: arrays/hashing, two pointers, sliding window, binary search, stacks, heaps, linked lists, trees. Design: the core building blocks, then the first two full designs.

| Day | Date | DSA | # | System design / LLD | Other | Hours |
| --: | --- | --- | --: | --- | --- | --: |
| 1 | Wed 21 Oct | Arrays & hashing, two pointers | 8 | Scaling & load balancers | – | 3.5 |
| 2 | Thu 22 Oct | Sliding window | 5 | Caching | – | 3.5 |
| 3 | Fri 23 Oct | Binary search (incl. on the answer) | 5 | SQL vs NoSQL, indexing | – | 3.5 |
| 4 | Sat 24 Oct **(weekend)** | Stacks, monotonic stacks & heaps | 11 | Replication, sharding, consistent hashing; CAP, consistency models, queues/Kafka | – | 7 |
| 5 | Sun 25 Oct **(weekend)** | Linked lists & trees | 14 | CDN, rate limiting, estimation; Design: URL shortener | – | 7 |
| 6 | Mon 26 Oct | Timed mock: mixed set | 4 | Design: Rate limiter | – | 3.5 |
| 7 | Tue 27 Oct | Review misses + leftover easies | 3 | LLD: SOLID + design patterns | – | 3.5 |

## Week 2 — Harder patterns and classic designs

Patterns: graphs, union-find, Dijkstra, dynamic programming, backtracking, tries, intervals, greedy. Design: one classic HLD problem per day, plus the first LLD problems.

| Day | Date | DSA | # | System design / LLD | Other | Hours |
| --: | --- | --- | --: | --- | --- | --: |
| 8 | Wed 28 Oct | Graphs: BFS/DFS, topological sort | 6 | Design: News feed | – | 3.5 |
| 9 | Thu 29 Oct | Graphs: union-find, Dijkstra | 5 | Design: Chat app (WhatsApp) | – | 3.5 |
| 10 | Fri 30 Oct | DP: 1D & 2D grid | 4 | Design: Notification system | – | 3.5 |
| 11 | Sat 31 Oct **(weekend)** | DP: knapsack, LIS, strings | 7 | Design: Ride hailing (Uber); LLD: Parking lot | – | 7 |
| 12 | Sun 01 Nov **(weekend)** | Backtracking, tries, intervals, greedy | 9 | Design: Video streaming (YouTube); LLD: LRU cache (LLD version) | – | 7 |
| 13 | Mon 02 Nov | Timed mock: mixed set | 4 | Design: Search autocomplete | – | 3.5 |
| 14 | Tue 03 Nov | Mixed practice | 3 | Design: Distributed cache | Project deep-dive #1 | 3.5 |

## Week 3 — Simulate interviews

Mixed timed DSA, the remaining HLD problems, LLD in 60–90 minute sittings, three mock interviews and behavioral prep.

| Day | Date | DSA | # | System design / LLD | Other | Hours |
| --: | --- | --- | --: | --- | --- | --: |
| 15 | Wed 04 Nov | Mixed practice | 3 | Design: Ticket booking (BookMyShow) | Project deep-dive #2 | 3.5 |
| 16 | Thu 05 Nov | Mixed practice | 3 | Design: Payment system | Mock interview #1 | 3.5 |
| 17 | Fri 06 Nov | Mixed practice | 3 | Design: Key-value store | STAR stories | 3.5 |
| 18 | Sat 07 Nov **(weekend)** | Mixed timed practice | 4 | LLD: Splitwise; LLD: Elevator system | Mock interview #2 | 7 |
| 19 | Sun 08 Nov **(weekend)** | Mixed timed practice | 4 | LLD: Booking system | Mock interview #3; Review all HLD notes | 7 |
| 20 | Mon 09 Nov | Redo failed problems (no solutions) | – | – | Final mistake-log review | 3.5 |
| 21 | Tue 10 Nov | Light redo + rest | – | – | Skim HLD framework + STAR stories | 2.5 |


## Daily routine

1. **DSA first** while you're fresh. Time-box each problem to 25–30 minutes; if stuck, read the approach and re-solve it yourself 2 days later (the tracker sets the redo date automatically).
2. **Log every miss** with the pattern and *why* you missed it. The mistake log is worth more than the problem count.
3. **Design out loud** with a 45-minute timer using the 7-step framework, then compare against the book chapter and note what you missed.
4. **Update the [tracker](tracker/)** — status, actual hours, notes — before you stop for the day.

## Habits that make the difference

- ~80 well-understood problems beats 200 rushed ones. Easy problems are warm-ups at this level: if the solution is obvious, skip or code it fast.
- Lead with clarifying questions in both DSA and design rounds; it's a strong senior signal.
- In design rounds you're graded on trade-off reasoning and driving the conversation, not on a "correct" diagram.
- Mocks expose gaps faster than anything else — do at least three in Week 3.

## Progress

- [ ] Week 1 — fundamentals (50 problems, 6 HLD topics, 2 designs)
- [ ] Week 2 — patterns & classic designs (38 problems, 7 designs, 2 LLD)
- [ ] Week 3 — interview simulation (17 problems, 3 designs, 3 LLD, 3 mocks)
- [ ] All Grind 75 problems attempted
- [ ] Final-day checklist in the crash course complete

## Resources

- [Grind 75](https://www.techinterviewhandbook.org/grind75/) — the DSA backbone
- [*System Design Interview* Vol 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf) (Alex Xu; private PDF, opens for you only) and Vol 2 (Alex Xu & Sahn Lam) — worked design walkthroughs
- *Designing Data-Intensive Applications* (Martin Kleppmann) — selective reading on replication, partitioning, consistency
- Pramp, interviewing.io, or peers — mock interviews

> Vol 1 chapter numbers are checked against the book. Vol 2 chapter numbers and LeetCode links were written from memory; verify them and fix any link that 404s.

## Using this repo

**Tracker:** open the [tracker page](tracker/) on the live site. Progress saves in your browser as you click. To keep it in this repo and sync across devices, click **Local only → Connect GitHub** and paste a fine-grained token with *Contents: read and write* on this repo only; progress is then saved to `progress.json` on the `progress` branch (separate from `main`, so saves don't rebuild the site). Problems and days come from `tracker/data.json`; after editing the plan or problem list, run `python3 scripts/build_tracker_data.py` and commit.

**Serve it as a site with GitHub Pages:**

1. Push the repo to GitHub.
2. Go to **Settings → Pages**, set **Source** to *Deploy from a branch*, pick `main` and `/ (root)`, and save.
3. After a minute the site is live at `https://<your-username>.github.io/<repo-name>/`. This README becomes the home page, and the links to the other `.md` files work as pages.

```bash
git init
git add .
git commit -m "3-week interview prep plan"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

Keep the repo **private** if you'd rather not share your progress; GitHub Pages on private repos needs a paid plan, so make it public if you want the free site.
