# System Design Crash Course — 3-Week Prep

> Exported from the Claude Doc version of this guide. Vol 1 chapter numbers are checked against the book; Vol 2 chapter numbers are from memory, so check them against your copy.

## Contents

1. [How to use this guide](#1-how-to-use-this-guide)
2. [The interview framework](#2-the-interview-framework-vol-1-ch-3)
3. [Core principles](#3-core-principles)
4. [Common design patterns](#4-common-design-patterns)
5. [Most frequently asked problems](#5-most-frequently-asked-problems)
6. [LLD quick reference](#6-lld-quick-reference)
7. [Day-by-day reading map](#7-day-by-day-reading-map)

## 1. How to use this guide

Read one section of this guide alongside each HLD day in the tracker (plan Day 1 = Wed 21 Oct), then do the matching Alex Xu chapter for depth. The guide gives you the 80% that interviews test; the book gives the worked walkthroughs.

- **Vol 1** = [*System Design Interview – An Insider's Guide*](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf) (Alex Xu, 2020). Every "Vol 1 ch. N" link opens your private copy at that chapter. **Vol 2** = the follow-up with Sahn Lam (2022).
- At 5.5 years of experience you are graded as a near-senior: you drive the conversation, state trade-offs before the interviewer asks, and go deep on one or two components.
- For each design, practise out loud with a 45-minute timer, then compare against the book chapter and write down what you missed.
- Skip in the book: anything you already do at work daily. Spend the saved time on deep dives (section 5).

## 2. The interview framework (Vol 1, ch. 3)

Use the same seven steps in every design round; most candidates fail on time management, not knowledge.

1. **Clarify requirements (5 min).** Functional: the 3–4 core features only. Non-functional: scale (DAU, QPS), latency, availability vs consistency, durability. Say what is out of scope.
2. **Estimate (3–5 min).** QPS (average and peak ≈ 2–3× average), storage per year, bandwidth, read:write ratio. Round aggressively; the point is which component becomes the bottleneck.
3. **API (3 min).** 3–5 endpoints with request and response fields. Mention pagination, idempotency keys and auth.
4. **Data model (5 min).** Entities, key fields, access patterns, then the store that fits those access patterns (SQL vs NoSQL) and the partition key.
5. **High-level design (10 min).** Client → CDN → load balancer → stateless services → cache → database, plus queues and workers for async work. Walk one request end to end.
6. **Deep dives (10–15 min).** Pick the 1–2 hardest parts (hot keys, fan-out, consistency, ordering) or follow the interviewer's lead. This is where seniority is scored.
7. **Wrap up (3 min).** Bottlenecks, failure modes, monitoring and alerting, and what you would build next at 10× scale.

**What seniors are graded on:** naming trade-offs unprompted ("I'll pick X because Y; the cost is Z"), handling failure cases, keeping the design simple until the numbers force complexity, and steering the 45 minutes yourself.

**Numbers worth memorising:** 1 day ≈ 86,400 s (use 10^5); 1M requests/day ≈ 12 QPS; memory read ≈ 100 ns; SSD read ≈ 100 µs; same-datacenter round trip ≈ 0.5 ms; cross-continent round trip ≈ 150 ms; one commodity server handles roughly 1–10k simple QPS.

## 3. Core principles

These thirteen building blocks appear in almost every design; know each one's main trade-off well enough to state it in one sentence.

| Concept | What to know | Key trade-off to say out loud | Book |
| --- | --- | --- | --- |
| Scaling | Vertical (bigger box) vs horizontal (more boxes); keep services stateless and move session state to Redis or a DB | Horizontal scales further but adds coordination and consistency problems | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) |
| Load balancing | L4 (TCP) vs L7 (HTTP, path-based routing); round robin, least connections, consistent hashing; health checks | L7 is smarter but costs more CPU; sticky sessions hurt even load spread | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) |
| Caching | Cache-aside (most common), write-through, write-back; TTLs; LRU/LFU eviction; client, CDN, app and DB layers | Faster reads at the cost of staleness; plan for invalidation, stampedes (locks or request coalescing) and hot keys | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) |
| SQL vs NoSQL | SQL for relations, transactions, ad-hoc queries; key-value for simple lookups; wide-column (Cassandra) for heavy writes; document stores for flexible schema | Choose by access pattern and consistency needs, not hype | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5), [6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87) |
| Indexing | B-tree (read-optimised, Postgres/MySQL) vs LSM-tree (write-optimised, Cassandra/RocksDB); secondary and composite indexes | Every index speeds reads but slows writes and uses storage | DDIA ch. 3 |
| Replication | Leader–follower (read scaling), multi-leader, leaderless with quorum (W + R > N); sync vs async | Async is fast but can lose recent writes on failover and gives replication lag | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5), [6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87) |
| Sharding | Partition by hash (even spread) or range (efficient scans); choose the shard key from the main query | Cross-shard joins and transactions become hard; hot shards need key salting or splitting | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) |
| Consistent hashing | Hash ring with virtual nodes; adding or removing a node moves only about K/N keys | Virtual nodes even out load at the cost of more metadata | Vol 1 [ch. 5](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=71) |
| CAP and consistency | During a partition, choose consistency (CP) or availability (AP); strong, read-your-writes, eventual consistency | Banking and inventory lean CP; feeds, likes and presence lean AP | Vol 1 [ch. 6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87) |
| Message queues | Decouple producers and consumers, absorb spikes, retries and dead-letter queues; Kafka partitions keep order per key | At-least-once delivery means consumers must be idempotent; exactly-once is expensive | Vol 2 ch. 4 |
| CDN | Serve static and media content from the edge; push vs pull; cache TTLs and invalidation | Lower latency and origin load, but cost and stale content | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) |
| Rate limiting | Token bucket (allows bursts), leaky bucket (smooths output), fixed window, sliding window log or counter; Redis for distributed counts | Accuracy vs memory; where to enforce (gateway vs service) | Vol 1 [ch. 4](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=51) |
| Unique IDs | Auto-increment (single point of failure), UUID (large, unordered), Snowflake (time + machine + sequence, sortable) | Snowflake depends on clock sync between machines | Vol 1 [ch. 7](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=110) |

Two more you will be asked about: **fault tolerance** (replicas, health checks, failover, multi-AZ deployment) and **observability** (metrics, logs, traces, alerts on latency and error rate).

## 4. Common design patterns

Naming the right pattern, and the problem it solves, is the fastest way to sound senior in a deep dive.

### Reliability

| Pattern | Problem it solves | Where it shows up |
| --- | --- | --- |
| Retries with exponential backoff and jitter | Transient failures without stampeding the server | Any network call, payment retries |
| Idempotency keys | Safe retries; no double charge or duplicate message | Payments, notifications, order APIs |
| Circuit breaker | Stop calling a failing dependency so failures don't cascade | Service-to-service calls |
| Bulkhead | Isolate thread or connection pools so one slow dependency can't starve the rest | Gateways, multi-tenant services |
| Timeouts and backpressure | Bound waiting; slow producers down when consumers fall behind | Queues, streaming pipelines |
| Leader election | One node coordinates (via ZooKeeper, etcd or Raft) | Schedulers, primary database, lock services |

### Data

| Pattern | Problem it solves | Where it shows up |
| --- | --- | --- |
| Cache-aside | Read-heavy data with tolerable staleness | Profiles, product pages |
| CQRS | Separate write model from read-optimised views | Feeds, dashboards, search |
| Event sourcing | Store events, derive state; full audit trail | Ledgers, wallets |
| Transactional outbox | Write to the DB and publish an event atomically | Order → payment → notification |
| Saga | Multi-service transaction with compensating actions instead of 2PC | Booking, checkout |
| Two-phase commit | Atomic commit across nodes; blocking and slow | Rare in interviews; mention why you avoid it |
| Write-ahead log | Durability and crash recovery | Databases, KV stores, queues |

### Communication

| Pattern | Problem it solves | Where it shows up |
| --- | --- | --- |
| Pub/sub | One event, many independent consumers | Notifications, analytics, fan-out |
| Fan-out on write vs on read | Precompute feeds vs assemble at read time; hybrid for celebrities | News feed, timelines |
| API gateway | Auth, rate limiting and routing in one place | Every microservice design |
| Long polling, WebSockets, SSE | Server push to clients | Chat, live location, notifications |
| Change data capture | Stream DB changes to caches, search indexes, warehouses | Search sync, cache invalidation |

### Specialised structures

| Pattern | Problem it solves | Where it shows up |
| --- | --- | --- |
| Bloom filter | Fast "definitely not seen" check with little memory | Web crawler, username check |
| Geohash, quadtree, S2 | Find nearby points | Uber, Yelp, nearby friends |
| Trie | Prefix lookup | Autocomplete |
| Count-min sketch, HyperLogLog | Approximate frequency and unique counts | Top-K, analytics |
| Merkle tree | Detect differences between replicas cheaply | KV store anti-entropy |
| Gossip protocol | Membership and failure detection without a central node | Dynamo-style KV stores |

## 5. Most frequently asked problems

The 16 designs below cover the large majority of SDE2–SDE3 design rounds; the first 13 are in the plan, and the last 3 are stretch reading if you finish early.

| # | Problem | Core insight to lead with | Deep dives to prepare | Plan day | Book |
| --: | --- | --- | --- | --- | --- |
| 1 | URL shortener | Read-heavy (~100:1); short code via base62 of a unique ID beats hashing plus collision checks | 301 vs 302 redirects, cache hot links, ID generation, analytics via async events | 5 | Vol 1 [ch. 8](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=119) |
| 2 | Rate limiter | Token bucket in Redis with atomic Lua or INCR + EXPIRE | Distributed counts, race conditions, sliding window accuracy, returning 429 with retry headers | 6 | Vol 1 [ch. 4](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=51) |
| 3 | News feed | Hybrid fan-out: push to followers' feed caches, pull for celebrities | Feed cache layout, ranking, pagination by cursor, fan-out workers on a queue | 8 | Vol 1 [ch. 11](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=166) |
| 4 | Chat (WhatsApp) | Stateful WebSocket servers plus a service that maps user to connection | Message ordering per conversation, delivery and read receipts, offline sync, group fan-out, presence | 9 | Vol 1 [ch. 12](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=178) |
| 5 | Notification system | Queue per channel (push, SMS, email) with workers calling third-party providers | Retries and dead-letter queue, idempotency, user preferences, rate limits per user | 10 | Vol 1 [ch. 10](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=151) |
| 6 | Ride hailing (Uber) | Driver locations in a geo-index (geohash or quadtree) held in memory, updated every few seconds | Matching, surge pricing, location write volume, trip state machine | 11 | Vol 2 ch. 1–3 |
| 7 | Video streaming (YouTube) | Upload to object storage → transcoding pipeline (DAG of tasks) → CDN with adaptive bitrate | Pre-signed upload URLs, resumable uploads, CDN cost vs popularity, view counts | 12 | Vol 1 [ch. 14](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=220) |
| 8 | Search autocomplete | Trie of top-K suggestions per prefix, rebuilt offline from query logs | Trie storage and sharding, update frequency, client debouncing, browser cache | 13 | Vol 1 [ch. 13](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=200) |
| 9 | Distributed cache | Consistent hashing across nodes, replication for availability | Eviction, hot keys, cache stampede, write strategy | 14 | Vol 1 [ch. 5](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=71)–[6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87) |
| 10 | Ticket booking (BookMyShow) | Temporary seat hold with a TTL, then confirm on payment | Double-booking prevention (row locks, optimistic concurrency), flash-sale traffic, waiting room | 15 | Vol 2 ch. 7 |
| 11 | Payment system | Idempotent API plus a double-entry ledger; payment service orchestrates a third-party processor | Retries, reconciliation, exactly-once effects, state machine, handling processor timeouts | 16 | Vol 2 ch. 11 |
| 12 | Key-value store | Dynamo style: consistent hashing, replication factor N, tunable quorum W + R > N | Vector clocks, hinted handoff, Merkle-tree repair, gossip, LSM storage engine | 17 | Vol 1 [ch. 6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87) |
| 13 | Unique ID generator | Snowflake: timestamp + datacenter + machine + sequence | Clock skew, sequence overflow, sortability | 4–5 | Vol 1 [ch. 7](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=110) |
| 14 | Web crawler | BFS frontier in queues with politeness per host | URL dedupe (Bloom filter), content dedupe, robots.txt, traps | Stretch | Vol 1 [ch. 9](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=132) |
| 15 | Google Drive / Dropbox | Split files into blocks, upload only changed blocks, metadata in SQL | Sync conflicts, notification of changes, storage tiering | Stretch | Vol 1 [ch. 15](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=244) |
| 16 | Leaderboard | Redis sorted sets for real-time rank | Sharding by score range, ties, top-K vs a user's own rank | Stretch | Vol 2 ch. 10 |

Other Vol 2 chapters worth skimming if a target company is in that domain: proximity service (Yelp), metrics and alerting, ad click aggregation, distributed message queue, S3-like storage, digital wallet and stock exchange.

## 6. LLD quick reference

In machine-coding rounds you are scored on clean, extensible, working code; eight patterns cover nearly every problem in the plan.

**SOLID in one line each:** single responsibility (one reason to change); open–closed (extend with new classes, don't edit old ones); Liskov substitution (subclasses must work anywhere the parent does); interface segregation (small, focused interfaces); dependency inversion (depend on interfaces, inject implementations).

| Pattern | Use it when | Plan problem |
| --- | --- | --- |
| Strategy | Swappable algorithms chosen at runtime | Parking fee rules, Splitwise split types (equal, exact, percent) |
| Factory | Creating the right subtype from input | Vehicle or spot types, notification channels |
| Observer | Notify many listeners of a change | Elevator display panels, booking confirmations |
| State | Behaviour changes with an object's state | Elevator (idle, moving, door open), booking lifecycle |
| Singleton | Exactly one shared instance (use sparingly; state why) | Parking lot manager, config |
| Builder | Objects with many optional fields | Booking request, notification message |
| Decorator | Add behaviour without subclassing | Pricing add-ons, logging around a service |
| Command | Encapsulate requests to queue, retry or undo | Elevator requests, undo in editors |

**Machine-coding checklist:** clarify requirements and list entities first (5 min); define interfaces before classes; keep models, services and storage in separate layers; use in-memory maps for storage; handle concurrency where it matters (seat booking, parking spot allocation) with locks or atomic operations; write a small driver or tests that demo the main flows; leave 10 minutes to walk through extensibility.

## 7. Day-by-day reading map

This map follows the HLD and LLD rows in the tracker, so each day's reading matches what you practise.

| Day | Date | Topic | Read |
| --- | --- | --- | --- |
| 1 | Wed 21 Oct | Framework, scaling, load balancers | Vol 1 [ch. 3](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=42), [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) (first half); this guide §2–3 |
| 2 | Thu 22 Oct | Caching | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) (cache, CDN); §3 |
| 3 | Fri 23 Oct | SQL vs NoSQL, indexing | Vol 1 [ch. 1](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=5) (database); DDIA ch. 3 (optional) |
| 4 | Sat 24 Oct | Replication, sharding, consistent hashing, CAP, queues | Vol 1 [ch. 5](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=71)–[6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87); Vol 2 ch. 4 (skim) |
| 5 | Sun 25 Oct | Estimation, unique IDs, URL shortener | Vol 1 [ch. 2](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=34), [7](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=110), [8](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=119) |
| 6 | Mon 26 Oct | Rate limiter | Vol 1 [ch. 4](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=51) |
| 7 | Tue 27 Oct | SOLID and design patterns | §6 |
| 8 | Wed 28 Oct | News feed | Vol 1 [ch. 11](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=166); §4 fan-out |
| 9 | Thu 29 Oct | Chat system | Vol 1 [ch. 12](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=178) |
| 10 | Fri 30 Oct | Notification system | Vol 1 [ch. 10](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=151); §4 reliability patterns |
| 11 | Sat 31 Oct | Ride hailing; LLD parking lot | Vol 2 ch. 1–3 |
| 12 | Sun 1 Nov | Video streaming; LLD LRU cache | Vol 1 [ch. 14](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=220) |
| 13 | Mon 2 Nov | Search autocomplete | Vol 1 [ch. 13](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=200) |
| 14 | Tue 3 Nov | Distributed cache | Vol 1 [ch. 5](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=71)–[6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87) (re-read deep dives) |
| 15 | Wed 4 Nov | Ticket booking | Vol 2 ch. 7; §4 saga |
| 16 | Thu 5 Nov | Payment system | Vol 2 ch. 11; §4 idempotency, outbox |
| 17 | Fri 6 Nov | Key-value store | Vol 1 [ch. 6](https://github.com/AjaySingh10/interview-prep-books/blob/main/system-design-interview-vol1.pdf#page=87) |
| 18–19 | 7–8 Nov | LLD: Splitwise, elevator, booking; mocks | §6 |
| 20–21 | 9–10 Nov | Review | This guide end to end |

### Final-day checklist

- [ ] I can run the 7-step framework from memory with time checkpoints
- [ ] I can state the main trade-off for every row in Core principles
- [ ] I can do a back-of-envelope estimate in under 5 minutes
- [ ] I have drawn all 13 planned designs at least once out loud
- [ ] I can explain 2 deep dives for each of those designs
- [ ] I have coded 4 LLD problems end to end
- [ ] I have 2 work projects ready to discuss at design depth
