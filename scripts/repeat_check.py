#!/usr/bin/env python3
"""Flag wording a new post repeats from recent posts (Luke's rule: vary the wording).

Usage: python3 scripts/repeat_check.py <jury|oldcrow> draft.json [--skip DATE:N]
(--skip leaves out that post from history, when you are rewriting a post that is already recorded)
draft.json = {"slides": ["..."], "caption": "..."} (slides may also be [{"text": ...}]).
Prints every 3+ word phrase the draft shares with the last 30 posts' slides or captions
(hashtags and Source lines ignored), plus any stock phrase on the banned list.
Exit code 1 if anything was found: rewrite those parts in fresh words and run it again.
"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
page, draft_path = sys.argv[1], sys.argv[2]
skip = sys.argv[sys.argv.index("--skip") + 1] if "--skip" in sys.argv else None
hist = ROOT / "state" / ("oldcrow/history.json" if page == "oldcrow" else "history.json")
STOP = set("a an the of to in on at for and or but is was were be it its this that with as by from you your they their he she his her we our i my me not no so if did do does".split())
BANNED = ["the court upheld", "a court upheld", "court upheld the", "the supreme court ruled", "would you have ruled",
          "would you have decided", "the same way", "what's the strangest", "should the court have",
          "took this traffic stop all the way", "all the way to the supreme court"]

def text_of(p):
    sl = p.get("slides") or []
    parts = [s if isinstance(s, str) else s.get("text", "") for s in sl] if isinstance(sl, list) else []
    cap = (p.get("caption") or "")
    cap = "\n".join(l for l in cap.splitlines() if not l.strip().startswith(("#", "Source")))
    return " ".join(parts) + " " + cap

def words(t):
    return re.findall(r"[a-z0-9$']+", t.lower().replace("**", "").replace("__", ""))

def grams(w, n):
    return {" ".join(w[i:i+n]) for i in range(len(w) - n + 1)}

posts = [p for p in json.loads(hist.read_text())["posts"] if f'{p.get("date")}:{p.get("n")}' != skip][-30:]
old = set()
for p in posts:
    w = words(text_of(p))
    for n in (3, 4, 5):
        old |= grams(w, n)
draft = json.loads(pathlib.Path(draft_path).read_text())
dtext = text_of(draft)
dw = words(dtext)
covered = [False] * len(dw)
for n in (3, 4, 5):
    for i in range(len(dw) - n + 1):
        g = " ".join(dw[i:i+n])
        if g in old and not all(x in STOP for x in dw[i:i+n]):
            for k in range(i, i + n): covered[k] = True
final, cur = [], []
for k, c in enumerate(covered + [False]):
    if c: cur.append(dw[k])
    elif cur: final.append(" ".join(cur)); cur = []
banned = [b for b in BANNED if b in " ".join(dw)]
if final or banned:
    for g in final: print("REPEATED:", g)
    for b in banned: print("STOCK PHRASE:", b)
    sys.exit(1)
print("OK: no repeated wording")
