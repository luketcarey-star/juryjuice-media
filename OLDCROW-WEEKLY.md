# OLDCROW weekly steps (Sunday run only)

Only read this file on a Sunday run. Same rules as the main guide.

### 2b. Learn from Luke's insights (Sunday run only, once 6+ posts have metrics)
- Rank every measured post in this page's history by `engagementRate` (also look at shares and
  comments on their own: shares spread the page, comments show a caption landed).
- Compare the top third with the bottom third and look for real patterns, not one-offs: hook and
  title style, topic, post type, single vs. carousel, tweet vs. image, tweet background (`theme`),
  caption length, kind of closing question, hashtags, posting hour.
- Rewrite `state/oldcrow/learnings.md` (keep it under ~40 lines): **Do more**, **Do less**, **Test next**. Each line
  names the evidence (e.g. "short question captions: 4.1% avg over 6 posts vs 2.3% for longer
  ones"). Drop lines the newer data no longer supports. Only claim a pattern seen in 3+ posts.
- If a post's comments show confusion or complaints (via Buffer metrics/notes when available),
  note it there too.

### 10. Weekly report and tune-up (Sunday run only)
Write `reports/oldcrow/<date>.md` (commit it) and put the short version at the top of the summary.
1. **The week in numbers** (last 7 days vs the 7 before): posts made, total reach, reactions,
   comments, shares, average engagement rate. Use Buffer `get_aggregated_post_metrics` for
   the totals (the Old Crow Facebook channel) and the per-post `metrics` in `state/oldcrow/history.json`.
2. **Top 3 and bottom 3 posts** of the week: title, type, style, time posted, reach, engagement
   rate, and one line on why it likely worked or didn't (hook, topic, image, timing).
3. **What's working:** engagement by post type, topic, style, posting hour.
   Only call something a pattern if it shows in 3+ posts.
4. **What changes next week** (make these changes now, then list them):
   - Rewrite `state/oldcrow/learnings.md` with the new Do more / Do less / Test next.
   - The planner already shifts post types and hours toward what earns the most engagement; note
     any big shift it will make.
   - Add 2 or 3 new post ideas to `ideas` in `state/oldcrow/history.json`, based on the top posts.
   - Never change Luke's rules to chase numbers (posts per day, platforms, no Facebook
     carousels, caption style, fact-checking, Meta check). If the data suggests one of those should
     change, recommend it to Luke in the report instead of doing it.
5. Summary for Luke (push): 5 to 8 short lines: the headline numbers vs last week, the best post,
   the weakest post, the 2 or 3 changes made, and any recommendation that needs his OK.

