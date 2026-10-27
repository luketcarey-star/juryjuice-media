#!/usr/bin/env python3
"""Compact view of a page's history so the bot doesn't have to read the whole history.json.

  python3 scripts/history_view.py <jury|oldcrow> [outdir]

Prints:
  INDEX    one short line per earlier post (date:n, type, title, topic, subtopic/object/line, status, eng rate)
           -> use it for "never repeat a topic or title" and for the subtopic rotation
  CAPTIONS the last 10 captions in full (vary their openings, shapes and closing questions)
  BEST     the 3 best-performing captions (match what made them work, don't copy)
  CHECK    posts planned in the last 2 days with a Buffer postId (failure check, step "Alerts")
  METRICS  posts sent 1-14 days ago with a Buffer postId (analytics step), and when they were last measured
Also writes <outdir>/avoid.json (default work/avoid.json), the array that `hookline.js write` takes:
  jury    = last 20 titles + subtopics
  oldcrow = every earlier topic and title
The real file (state/.../history.json) is still where new posts get appended.
"""
import json, sys, pathlib, datetime as dt
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
page = sys.argv[1] if len(sys.argv) > 1 else "jury"
outdir = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "work"
SD = ROOT / "state" / ("oldcrow" if page == "oldcrow" else "")
hist = json.loads((SD / "history.json").read_text())
posts = hist["posts"]
cfg = json.loads((SD / "config.json").read_text())
now = dt.datetime.now(ZoneInfo(cfg.get("timezone", "America/Toronto")))
chan = "facebook"


def rate(p):
    m = p.get("metrics") or {}
    v = [m[k]["engagementRate"] for k in ("facebook", "instagram")
         if isinstance(m.get(k), dict) and isinstance(m[k].get("engagementRate"), (int, float))]
    return sum(v) / len(v) if v else None


def extra(p):
    bits = [p.get(k) for k in ("subtopic", "object", "line", "headline") if p.get(k)]
    if p.get("then") or p.get("now"):
        bits.append(f'{p.get("then", "")} -> {p.get("now", "")}')
    return " / ".join(str(b) for b in bits)


def planned(p):
    t = ((p.get("facebook") or {}).get("plannedAt")) or ((p.get("instagram") or {}).get("plannedAt"))
    return dt.datetime.fromisoformat(t) if t else None


print(f"=== INDEX ({len(posts)} posts) ===")
for p in posts:
    r = rate(p)
    print(f'{p.get("date")}:{p.get("n")} {p.get("type")}/{p.get("style")} | {p.get("title")} | {p.get("topic")} | {extra(p)} | '
          f'{p.get("status")}{" | eng %.2f%%" % r if r is not None else ""}')

print("\n=== CAPTIONS (last 10, full) ===")
for p in posts[-10:]:
    print(f'--- {p.get("date")}:{p.get("n")} {p.get("type")}\n{(p.get("caption") or "").strip()}')

best = sorted((p for p in posts if rate(p) is not None), key=rate, reverse=True)[:3]
print("\n=== BEST (top 3 by engagement) ===")
if not best:
    print("(none measured yet)")
for p in best:
    print(f'--- {p.get("date")}:{p.get("n")} {p.get("type")} eng {rate(p):.2f}%\n{(p.get("caption") or "").strip()}')

print("\n=== CHECK (planned in the last 2 days, with a Buffer postId) ===")
for p in posts:
    if p.get("status") in ("deleted-by-luke", "skipped"):
        continue
    t = planned(p)
    ids = {k: (p.get(k) or {}).get("postId") for k in ("facebook", "instagram") if (p.get(k) or {}).get("postId")}
    if t and ids and now - dt.timedelta(days=2) <= t <= now:
        print(f'{p.get("date")}:{p.get("n")} status={p.get("status")} planned={t.isoformat()} ids={ids}')

print("\n=== METRICS (sent 1-14 days ago, with a Buffer postId) ===")
print(f'lastMetricsAt: {cfg.get("lastMetricsAt")}')
for p in posts:
    if p.get("status") in ("deleted-by-luke", "skipped"):
        continue
    t = planned(p)
    ids = {k: (p.get(k) or {}).get("postId") for k in ("facebook", "instagram") if (p.get(k) or {}).get("postId")}
    if t and ids and now - dt.timedelta(days=14) <= t <= now - dt.timedelta(days=1):
        print(f'{p.get("date")}:{p.get("n")} ids={ids} measured={bool(p.get("metrics"))}')

if page != "oldcrow":
    from collections import Counter
    last = [p.get("topicGroup") or "other" for p in [q for q in posts if q.get("type") != "text"][-20:]]  # text posts are extra and outside the topic mix
    cnt = Counter(last)
    print("\n=== TOPIC GROUPS of the last %d posts (target: police ~70%%, county ~20%%, hoa ~5%%, other ~5%%) ===" % len(last))
    print(", ".join(f"{g}: {cnt.get(g, 0)}" for g in ("police", "county", "hoa", "other")))
    pol = [p.get("subtopic") or p.get("title") for p in posts if (p.get("topicGroup") == "police")][-8:]
    print("Last 8 police subjects (don't repeat any of these):", "; ".join(str(x) for x in pol) or "(none)")

if page == "oldcrow":
    avoid = [x for p in posts for x in (p.get("topic"), p.get("title")) if x]
else:
    avoid = [x for p in posts[-20:] for x in (p.get("title"), p.get("subtopic")) if x]
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "avoid.json").write_text(json.dumps(avoid, indent=1))
print(f"\nWrote {outdir / 'avoid.json'} ({len(avoid)} entries)")
