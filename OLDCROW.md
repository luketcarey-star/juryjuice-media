# Old Crow daily posting bot

You are running Luke's Old Crow posting bot. It runs **once a day** (about 16:36) and makes the next day's
**3 posts a day** on the **Old Crow Facebook page only** (no Instagram yet), saved to Buffer.
Jury Juice is NOT handled here. Work from this repo (`luketcarey-star/juryjuice-media`).

**One run a day (Luke, 2026-10-16).** The bot runs once a day at about 16:36 and makes the **whole next day**: posting day = TOMORROW (`TZ=America/Toronto date -d tomorrow +%F`), 3 posts (o1 07:30–08:30, o2 13:30–14:30, o3 21:00–22:00). If Luke asks for a special run for TODAY, the posting day is today instead and the planner simply skips windows that have already passed. Plan with `python3 scripts/plan_day.py <posting day> day oldcrow`. Everywhere below, `<today>`, `<date>` and "today's posts" mean the **posting day**, and `<run>` means `day`. Post `date` in history = the posting day.
**Buffer's scheduled-post limit** (`bufferLimit` in `state/config.json`, 10 on the free plan) is per channel (each Facebook page and the Instagram account has its own 10; Luke 2026-10-16): the planner only returns as many posts as still fit. If `limitedByBuffer` is true, make only what it returns and say in the summary how many posts were skipped because of the Buffer limit (posts skipped; tell Luke).

Everything about how Old Crow posts are written and drawn comes from Hookline itself (the copy in
`renderer/hookline.html`), so the bot's posts match what Luke makes by hand:
- `node scripts/hookline.js write oldcrow <format> illus avoid.json` prints the exact writing prompt
  Hookline uses for that post type (voice, structure, caption, Meta rules, humanizer rules).
- `node scripts/hookline.js images spec.json` prints the exact image prompt for each slide and the
  `reference_urls` to send (the two raven character sheets, or the drawing-style sample).
- `node render.js spec.json <outdir>` draws the finished slides (text, price tags, no-text images).

Also read `state/oldcrow/config.json` (mode, Buffer IDs, windows, image settings) and use the
`meta-posting-rules` and `humanizer` skills if they are available.

## Post types (all single illustrated images with the ravens; Luke's rule)
**UPDATE (Luke 2026-10-16): the illustrated two-raven types, told-or-sold ("WHO SOLD US...?") and question, are REMOVED from the pool. Never make them. All 3 daily posts are one-liner or then vs now (step 4b); ignore the told-or-sold/question rows and instructions below.**

Every post is about one belief or habit we were **told or sold**, shown through the two ravens and
one everyday object, so the images feel like stills from the Old Crow videos. Daily: 3 posts. **Always vary the type** (Luke's rule): the planner rotates told or sold,
question, one-liner and then vs now so the same type never runs twice in a row. **The one-liner and then vs now are most posts (Luke's rule, about 3 in 4):** of the 4 daily posts, 3 are one of these two and 1 is a told-or-sold or question (a different window each day). **Luke (2026-10-13): he wants MORE one-liners** (the cream poster with the old raven), so the planner weights them about 2 to 1 over then vs now; about half of all Old Crow posts are one-liners. Use the types the planner gives.
| id | what | format | images |
|---|---|---|---|
| sold | **Told or sold** (main type): both ravens in a warm everyday place, the young raven holding or pointing at the object, the old raven beside him; the belief as the title ("WHY A DIAMOND RING?"); the caption gives the real history and who benefits | single | 1 |
| question | The old raven's question: the old raven alone with the object, his question as the title | single | 1 |
| oneliner | **One-liner** (Luke's rule, 2026-10-11; replaces the note): a fully AI-drawn cartoon poster in the Raven Remembers style. Cream parchment background, big bold hand-lettered black text at the top with ONE key word in deep crimson, the old raven below (waist up, large) acting the line out. See step 4b | single | 1 |
| thennow | **Then vs Now** (Luke's rule, 2026-10-11): a fully AI-drawn poster in the shrinkflation style. Dark brown background with theatrical spotlights, one tall bold condensed cream headline with a thin underline at the top, the old raven (waist up) holding the THEN version in one hand and the NOW version in the other, each under a curled ribbon banner labelled THEN / NOW. See step 4b | single | 1 |
No price-in-hours posts, no tweet-style posts, no carousels, no animal flashbacks. (The old two-raven "then vs. now" is gone; the new **thennow** type above is different and allowed.)

## Hard rules (never break these)
0. **Every post passes `META_CHECK.md`** (Meta Community Standards and monetization policies)
   before it is saved to Buffer. Luke's pages are monetized; a failed check means fix or replace.
1. **Real facts are verified.** For told-or-sold posts (and any question or then vs now that states a
   fact), every date, company, campaign, study and historical claim must be confirmed with web
   search against reliable sources (historical archives, encyclopedias, major newspapers, museums,
   government statistics). If a fact can't be confirmed, cut it or change the topic. Never guess.
2. **Never repeat a topic or a title.** Check the INDEX from `history_view.py` (topics, titles, objects)
   and pass `work/avoid.json` (written by it) to the writing prompt.
3. **Images stay on model.** Every `generate_image` call uses model `sunburst`, quality `high`,
   aspect `4:5`, and the `reference_urls` that `hookline.js images` gives for that slide. The tool's
   reply must say "using N reference image(s)" with N equal to the number of URLs sent. If it says
   0 (the image connector hasn't been updated yet) or reference downloads fail, stop making images,
   make nothing for that post, and tell Luke at the top of the summary. Never post raven images
   made without the character sheets.
4. **OpenAI credit out = no more image prompts.** If config has `"imagesPaused": true`, make no
   posts at all (Old Crow is image-only) and say so at the top of the summary. If any
   `generate_image` call fails because the account is out of money ("insufficient_quota", "billing",
   "credit", "hard limit", "exceeded your current quota", or a 429 about quota), stop all image
   prompts immediately, set `"imagesPaused": true` and `"imagesPausedReason"` (date + error) in
   `state/oldcrow/config.json` and in `state/config.json` (same OpenAI account), and tell Luke at the
   top of the summary. Only Luke turns images back on.
5. **Mode:** `queue` = schedule at the planned time; `draft` = also `saveToDraft: true`. Never change it.
6. Never publish immediately (`shareNow`). Never touch Jury Juice posts or Jury Juice state.
   Never delete or edit Buffer posts you didn't create in this run.
7. Max 16 images per run. Every Old Crow post is a single slide (no carousels).

## Alerts (Luke wants to know about EVERY problem)
- If anything at all goes wrong in this run, the summary's FIRST line is `⚠️ PROBLEM: <one-line
  plain description>` followed by what happened, what was skipped, and exactly what Luke needs to
  do (if anything). Examples: a post skipped or swapped, an image that failed or came out wrong,
  OpenAI credit out, the image connector or Buffer missing or erroring, Buffer's post limit hit,
  a GitHub push refused, a fact that couldn't be verified, a render error, a post rejected by
  Facebook or Instagram.
- Check recent posts for failures: for every post listed under CHECK (planned in the last 2
  days, with a Buffer `postId`), call Buffer `get_post` (no metrics needed). If its status is
  `error`, or it's more than 1 hour past its planned time and still not `sent`, report it as a
  PROBLEM with the error text, and update its `status` in history.
- Watchdog: write the current time to `lastRun` in this page's config file every run. Then read
  the OTHER page's config (`state/config.json` for Jury Juice, `state/oldcrow/config.json` for Old
  Crow). If its `lastRun` is more than 30 hours old (both bots run once a day, about 16:06 and 16:36, so anything under 30 hours is normal), report
  `⚠️ PROBLEM: the <other page> bot hasn't run since <time>` so Luke can check its scheduled task.
- **Posts Luke deletes are not a problem.** Luke sometimes deletes queued posts in Buffer on
  purpose. If `get_post` says a post is not found (404) and it was never sent, mark it
  `"status": "deleted-by-luke"` in history, skip it in every check and report, and don't raise a
  PROBLEM for it. Posts already marked `deleted-by-luke` are ignored.
- **Every planned post is accounted for.** If the plan gave N posts and you made fewer, save each
  missing one in history as `"status": "skipped"` with `"skipReason"` (the exact reason), and say
  in the summary which post was skipped and why, e.g. "Made 1 of 2: the one-liner was skipped because
  the image failed twice."
- If nothing went wrong, start the summary with `✅ All good` instead.

## Steps

### 1. Setup
- **If the image tool isn't found, wait and retry before giving up.** Run `sleep 180`, then
  ToolSearch again; do this up to 3 times (about 10 minutes). Only then treat images as unavailable.
  There is no backup run any more (Luke removed it), so record each post you couldn't make as
  `"status": "skipped"` with `"skipReason": "image tool unavailable"` (Jury Juice: if you post a
  text version instead, add `"imageFallback": true`) and put it at the top of the summary so Luke knows to fix it.
- **Load the tools first.** In scheduled runs the Hookline Images and Buffer tools are often
  "deferred": they exist but must be loaded before use. Before deciding a connector is missing,
  call ToolSearch with `select:mcp__Hookline_Images__generate_image` (then a keyword search for
  `generate_image` and for `Buffer create_post` if that finds nothing). Only if ToolSearch truly
  finds no image tool is it missing; then report it as a PROBLEM with what ToolSearch returned.
- `cd` into the repo, `git pull`. Work out the run and posting day as described at the top (the posting day: tomorrow's date in America/Toronto, or today for a special run Luke asked for).
- **Read history the cheap way:** run `python3 scripts/history_view.py oldcrow` once. It prints an INDEX of every earlier post (titles, topics, objects, lines, headlines), the last 10 captions in full, the 3 best captions, the posts to failure-check and the posts to refresh metrics for, and writes `work/avoid.json` (every earlier topic and title). Use that output everywhere this guide says "check history". Do NOT open or print `state/oldcrow/history.json` (it is large); only append your new posts to it with a short python snippet.
- `playwright` (with Chromium) is preinstalled.

### 2. Update analytics (only if the last update was 40+ hours ago, i.e. every other day; skip if no posts yet)
- For each post listed under METRICS (sent 1 to 14 days ago, with a Buffer post ID; refresh them every other day; save the time in `lastMetricsAt` in this page's config), call
  Buffer `get_post` with `includeMetrics: true` (max ~30 calls).
- Save under `metrics.facebook`: the raw metrics, plus `engagementRate` = (reactions + comments +
  shares) ÷ reach (impressions if reach is missing; null if neither), and `measuredAt`.

### 2b. Learn from Luke's insights: **Sunday run only.** On Sundays (and only then) read `OLDCROW-WEEKLY.md` and do its step 2b first. Other days skip it.

### 3. Plan
- `python3 scripts/plan_day.py <date> <run> oldcrow` (`<run>` = `day`). It returns this run's posts (type,
  format, planned `facebookAt`), counting today's earlier posts (max 3 a day; **no carousels at all**, Luke's rule:
  carousels do badly on Facebook) and keeping posts well spaced (one per window, 90+ minutes apart). Use them as given. No posts returned = day is full.
- The planner also keeps Buffer under its 10-scheduled-posts limit across BOTH pages (it counts
  future posts in `state/history.json` and `state/oldcrow/history.json`). If `limitedByBuffer` is
  true, make only the posts it returns and mention it in the summary. Always record each scheduled
  post with `"status": "scheduled"` and its `plannedAt` + `postId` so the other bot can count it.

### 4. Write each post
- Before writing, read `state/oldcrow/learnings.md` and apply its **Do more / Do less** lines to the topic, hook,
  slides and caption. About 1 post in 4, try one idea from **Test next** and save it on the post as
  `"experiment": "<what was tested>"` in history so the next review can judge it. Also re-read the
  BEST section (3 best-performing captions) and match what made them work (without copying them).
- Luke's own rules always win over learnings: short captions, no sources in captions, good
  searchable hashtags, no engagement bait, Meta rules, fact-checking, carousel limits.
- **oneliner and thennow posts: follow step 4b instead of `hookline.js` and step 6.** For sold and question:
- `work/avoid.json` (from `history_view.py`) already holds every earlier topic and title. Run
  `node scripts/hookline.js write oldcrow <type> <style> work/avoid.json 1` (style from the plan: `illus`
  or `tweet`; the final `1` makes it a single standalone slide) and follow that prompt exactly.
  **Never make carousels for Old Crow** (Facebook only, and carousels do badly there).
  Produce the same JSON it asks for: `topic`, `slides` (`text` + `scene`), `caption`, and `sources`
  for real types.

### 4b. One-liner and Then vs Now posts (fully AI-drawn, Luke's rule 2026-10-11)
These two types skip `hookline.js` and `render.js`: the image model draws the whole poster, text
included. **Old raven only** (never the young raven). Only the old raven's sheet is the reference:
`reference_urls: ["https://raw.githubusercontent.com/luketcarey-star/juryjuice-media/main/refs/oldcrow-old.jpg"]`,
model `sunburst`, quality `high`, aspect `4:5` (rule 3 applies: the reply must say 1 reference image).

**Writing the line**
- One-liner: an original line of 6 to 14 words, usually split into two short sentences (set-up, then
  twist). Mostly dry, witty and a little sarcastic about people, money, work, buying things, advice
  and modern habits (Luke: "mix but more raven"); about 1 in 4 is a quieter reflective line. Tie it
  to the page's told-or-sold world when it fits. Examples of the level (never reuse these):
  "Everyone wants honest advice. Until they get it." / "They sold you the dream. You're still
  making the payments."
- **Then vs Now variety (Luke 2026-10-16: they were too similar):** "made to last vs made to break / repairable vs disposable" is only ONE of many themes and may be used at most 1 in 5 then-vs-now posts (check the last 5 headlines in INDEX first). Rotate the theme: owning vs subscribing, shrinking portions/prices, free vs "free", skills done by hand vs apps, time (waiting vs instant but busier), community vs screens, repair vs replace, advertising, work and money, food, houses, travel, school. Never reuse a headline pattern ("X THEN. Y NOW.") twice in a row: vary it ("WHAT IT COST. WHAT IT COSTS.", "THEY CALLED IT PROGRESS", a short question, etc.). Vary the two props' shapes, the old raven's pose and the setting too.
- Then vs Now: one everyday thing that got worse while we were told it got better (products made
  to break, smaller portions, subscriptions instead of owning, "free" things that aren't, repairs
  made impossible...). Headline 3 to 8 words (e.g. "BUILT TO LAST. BUILT TO REPLACE."). The THEN and
  NOW objects must be clearly different at a glance. If the comparison states a fact (a size, a
  price, a year), fact-check it like a told-or-sold post; otherwise keep it general and true.
- Since one-liners are now the most common post, vary the picture every time: a different pose, prop, expression and setting for the old raven (not always the armchair and tea cup), and a different kind of line (money, work, advice, habits, buying things, time, technology). Check the INDEX so a line, prop or scene isn't repeated.
- Never copy or reword lines from other pages (Raven Remembers, Human Patterns, quote sites).
  Check the INDEX so a line, headline or object is never repeated.
- No insults about groups of people, no politics, religion, health or bodies. Meta rules apply.

**Image prompt templates** (fill in the parts in <>; keep everything else word for word)
One-liner:
```
A single-panel cartoon poster. At the top, big bold hand-lettered comic text in black, centered, in <3-5> lines, with the word "<KEY WORD>" in deep crimson red:

<LINE 1>
<LINE 2>
...

Spell every word exactly as written above, nothing else written anywhere.

Below the text, large in the frame from the waist up: the old raven <doing something that acts out the line, with one clear prop and a dry, knowing, heavy-lidded expression>. Plain warm cream parchment background with subtle paper texture.

Style: Hand-drawn 2D cartoon with strong dark outlines, simple cel shading and a subtle paper texture; muted navy and walnut colours. The older raven is calm and knowing, with heavy-lidded amber eyes, a navy three-piece suit, cream shirt, muted brown tie and a small round gold lapel pin; black feathers, grey beak and black feathered hands. The reference image is his official character sheet: copy his face, feather shapes, eye shapes, outfit, colours and proportions exactly, in this same line style.

<Any prop with paper or screens: "has only blank lines, no readable writing".> No logos, signatures or watermarks.
```
Then vs Now:
```
A bold cartoon poster on a dark brown background with soft theatrical spotlights from above.

At the top, one line of tall, bold, condensed all-capital headline text in warm cream, with a thin cream underline beneath it:
<HEADLINE>

Spell every word exactly as written, nothing else written except the two banner labels below.

Below the headline, large in the frame from the waist up: the old raven faces the viewer with a sly, knowing, heavy-lidded half-smile. In his left hand (viewer's left) he holds up <THEN object, described so it looks better/bigger/sturdier>; above it, a curled ribbon banner labelled "THEN". In his right hand (viewer's right) he holds up <NOW object, clearly worse/smaller/flimsier>; above it, a curled ribbon banner labelled "NOW". The objects have no brand names or other writing.

Style: Bold, polished 2D cartoon illustration with thick clean dark outlines, rich cel shading and warm dramatic lighting; browns, creams, deep navy and a touch of red. The older raven is calm and knowing, with heavy-lidded amber eyes, a navy three-piece suit, cream shirt, muted brown tie and a small round gold lapel pin; black feathers, grey beak and black feathered hands. The reference image is his official character sheet: copy his face, feather shapes, eye shapes, outfit, colours and proportions exactly.

No logos, signatures or watermarks.
```

**Check the image (always)**: look at it and read every word on it letter by letter against your
line. Any misspelling, missing or extra word, extra text, a brand logo, or a raven that doesn't
match the sheet → regenerate once with the same prompt. Still wrong → write a different line and
try once more; if that fails, skip the post with a skipReason. Never post a misspelled image.
Save the good image as `posts/oldcrow/<date>/<n>-<type>/slide1.jpg` (convert to JPEG if needed) and resize it to exactly 1080x1350 (the AI model returns 1024x1280, same 4:5 shape; use PIL `resize((1080,1350), Image.LANCZOS)`).
In history save `"line"` (one-liner) or `"headline"`, `"then"`, `"now"` (then vs now).

**Captions for these two types (Luke's rules; NO hashtags on either)**
- One-liner: one short deadpan line in the old raven's voice, 1 to 6 words, adding a dry twist
  instead of repeating the image ("Still paying." / "Every single time." / "Confidential, of course.").
  Never the same caption twice; check history.
- Then vs Now: Human Patterns format, always freshly written and varied:
  line 1 = a curious question about the reader's own experience, optionally with one emoji at the
  end (👀 🤔 😏, not every time); blank line; 2 or 3 short sentences that name the thing and add one
  sharp observation; optionally a final short reflective line. No hashtags, no sources, and never
  "tell us / comment / share / tag" (Meta engagement-bait rule); a plain question is fine.
  Vary the question shape and wording every time (check the CAPTIONS section, last 10).
- The hashtag rules in step 5 apply only to told-or-sold and question posts.

### 5. Fact-check (sold, question, and any fact in a then vs now)
- Search the web for every claim and figure. One reliable source per claim is enough: stop searching a claim once it is confirmed and don't re-search facts you already confirmed. Fix or drop anything wrong; if the post's core claim
  can't be confirmed, choose a new topic and rewrite.
- Keep `sources` in history only. **Captions must be engaging and inspiring** (Luke's rule; length
  is free, quality is what matters): a strong first line that hooks, the story in 2 to 4 short
  paragraphs (told or sold: where the belief came from, who started it, who benefits today), and a
  reflective question at the end, in the old raven's warm voice. Every line earns its place. No
  sources, links or `References:` in the caption, no engagement bait, never preachy.
- **Told-or-sold images show only the title** (the belief, e.g. "WHO MADE BREAKFAST SO IMPORTANT?").
  No subtitle or second line on the image; everything else goes in the caption.
- **Hashtags (told-or-sold and question posts only):** the page tag first, then 1 or 2 popular, widely searched tags that name the post's
  actual subject, in CamelCase (e.g. #McDonalds #LawFacts, #GuineaPigs #WeirdLaws, #Nostalgia,
  #SlowLiving, #EngagementRing). Never made-up or niche tags nobody searches (#oldcrowasks,
  #thingswearesold, #notes, #busy) and never vague filler (#history, #facts).

### 6. Make the images and slides
- (Not for oneliner / thennow: those are finished in step 4b.)
- Check rules 3, 4 and 7 first.
- Write `work/p<n>/spec.json`: `{"page":"oldcrow","style":"<illus|tweet>","format":"<type>","caption":"...","slides":[{"text":"...","scene":"..."}]}`.
  Tweet-style posts: add `"theme"` from the plan (`black`, `light` = white with black text, `dim` =
  classic Twitter navy). The planner rotates them so tweet posts cycle through all three; save
  `theme` in history for every tweet post so the rotation continues.
- Tweet-style posts need no images: skip straight to `node render.js`.
- `node scripts/hookline.js images work/p<n>/spec.json` → for each slide call `generate_image`
  with that `prompt` exactly as given (it ends with `REFERENCE_URL:` lines that the image server
  reads), model `sunburst`, quality `high`, aspect `4:5`. Also pass `reference_urls` if the tool
  offers that field. The result
  names the saved file; copy it to `work/p<n>/img<k>.jpg` and add `"image":"img<k>.jpg"` to that slide.
- `node render.js work/p<n>/spec.json posts/oldcrow/<date>/<n>-<type>/`.
- Look at every rendered slide. Check the ravens look like the character sheets (outfits, colours, eyes), the
  object is clear, there is no text in the art, and the title is readable.
  Regenerate an image once if it's clearly wrong; if it's still wrong, swap the post for another
  type and say so in the summary.

### 6b. Meta check (every post, no exceptions)
- Run the full checklist in `META_CHECK.md` on every finished post (slides, caption, hashtags,
  alt text). Only posts that pass go any further. Fix or replace anything that fails.

### 7. Publish images
- `git add posts/oldcrow state/oldcrow && git commit -m "Old Crow posts for <date> <run>" && git push`.
- Image URL: `https://raw.githubusercontent.com/luketcarey-star/juryjuice-media/main/posts/oldcrow/<date>/<n>-<type>/slideK.jpg`

### 8. Save to Buffer (Facebook only)
- `create_post` with channel `facebookChannelId` from config, `metadata: {facebook: {type: "post"}}`,
  `schedulingType: "automatic"`, `text` = caption, `assets` = slide URLs in order with short
  `altText`, `mode: "customScheduled"`, `dueAt` = planned `facebookAt` (must be in the future; if
  it isn't, move it 1 to 2 hours later inside the same day). Draft mode: add `saveToDraft: true`.
- Buffer's free plan allows only 10 scheduled posts across all pages at once. If Buffer refuses
  because of that limit, keep the post in history as `"status": "not-scheduled"` with its images
  and say so in the summary.

### 9. Record and clean up
- Append each post to `state/oldcrow/history.json` → `posts`:
  `{date, n, type, format, style, theme, title, topic, slides, sources, imageFolder,
    facebook: {postId, plannedAt}, status, metrics: {}}`
- Delete `posts/oldcrow/<date>` folders older than `keepImagesDays`. Commit and push.

### 10. Weekly report and tune-up: **Sunday run only.** On Sundays (and only then) do step 10 from `OLDCROW-WEEKLY.md` before the summary. Other days skip it.

### 11. Summary for Luke (always, short)
- Each post: type, title, planned time, scheduled or draft.
- Anything that couldn't be confirmed and was swapped, and why.
- Any errors (images, Buffer limit, GitHub) and what's needed from Luke.
- A post idea when a good one comes up (always on Sundays).
