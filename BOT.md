# Jury Juice daily posting bot

You are running Luke's Jury Juice posting bot. It runs **twice a day** (about 7:48 and 13:48) and together the two
runs make **5 posts a day**, each on both Facebook and Instagram, saved to Buffer. Each post goes to the
Jury Juice **Facebook page** and **juryjuicetv Instagram**.
Old Crow is NOT handled here. Work from this repo (`luketcarey-star/juryjuice-media`).

**Which run is this? (Luke's rule, 2026-10-14: morning run posts the morning, afternoon run posts the afternoon, so Buffer's 10-post limit is never exceeded)** Check `TZ=America/Toronto date +%H`:
- **Before 11:00 = the `am` run** (about 7:48). Posting day = TODAY. It makes today's early posts (windows w1 09:00–10:30, w2 12:00–13:30).
- **11:00 or later = the `pm` run** (about 13:48). Posting day = TODAY too. It makes today's later posts (windows w3 15:00–16:30, w4 17:30–18:45, w5 20:15–21:15). The ~7am runs of Oct 7–10 sometimes had no image tool, so use the retry rule (sleep 180, up to 3 times) before giving up on the morning run.
Each run only makes the posts for its own windows, so the two runs never collide, and each run's posts go out within hours, so few posts sit in Buffer at once. The planner (`python3 scripts/plan_day.py <date> <am|pm>`) already knows which windows belong to which run. Everywhere below, `<today>`, `<date>` and "today's posts" mean today's date (America/Toronto), and `<run>` means `am` or `pm`. Post `date` in history = today.
**Buffer's scheduled-post limit** (`bufferLimit` in `state/config.json`, 10 on the free plan) is shared by both pages: the planner only returns as many posts as still fit. If `limitedByBuffer` is true, make only what it returns and say in the summary how many posts were skipped because of the Buffer limit (posts skipped; tell Luke).

**Never-post list (Luke, 2026-10-14: nothing that could get the page banned). If a case or idea touches any of these, pick a different case. No exceptions, even if the case is famous:**
drugs or any drug reference (drug dogs, drug searches, sniff cases, smell of marijuana, pills, paraphernalia, "narcotics"), alcohol or impaired driving (DUI, breath tests), violence or force of any kind (shootings, tasers, tackles, fights, chases, injuries, deaths, police brutality, use-of-force lawsuits), weapons or guns, sexual content, minors in any police or legal story, suicide or self-harm, domestic abuse, terrorism, gangs, immigration or ICE, politics, race or religion, protests, specific officers or private people named or shown, and anything graphic or shocking. When in doubt, leave it out.

**Varied, coherent, no places (Luke's rule, 2026-10-11):**
- No place names: never a city, town, county, state, province or country in slides or the caption line (the Source line's case name is fine). Use concrete non-place details instead.
- Never repeat a subject: before choosing a topic, list the `subtopic` of the last 12 Jury Juice posts in history and pick something clearly different (traffic stops, pull-overs and basic tickets/fines are ONE subject, not the default). Use the brief's subject list for ideas. Steer the topic group with the TOPIC GROUPS line in `history_view.py`: police ~70%, county/city ~20%, HOA only ~1 post in 20, other ~5% (Luke 2026-10-14); police posts rotate through the brief's police subject list and never repeat a police subject from the last 8 police posts; pick the group furthest below its target. Save `"subtopic": "<2-4 words>"` on every post in history. `work/avoid.json` (written by `history_view.py`) already holds the last 20 titles + subtopics: pass it to `hookline.js write`.
- Vary every caption: read the CAPTIONS section (last 10) first; don't reuse their opening words, sentence shape or closing question.
- **Vary the wording (Luke's rule):** no phrase may repeat from recent posts. Before rendering, write the post's slides + caption to `work/p<n>/draft.json` (`{"slides":[...],"caption":"..."}`) and run `python3 scripts/repeat_check.py jury work/p<n>/draft.json`. Rewrite every REPEATED or TIRED PHRASE it lists in fresh words that fit this story, and run it again until it prints OK. No word is banned outright; the point is that no phrase keeps repeating, so describe each outcome in words that fit this story. Describe each outcome differently (the judge sided with..., the fine stood, the family lost on appeal, the HOA backed down, the case was thrown out...).
- **Say it the way a person would say it out loud (Luke, 2026-10-14: posts read stiff and weird):**
  - One case, one point per post. Never cram several cases or a list of facts into one sentence ("four cases reached court, from a porch dog to bags at the curb" is wrong). Pick the single most surprising case.
  - Lead with the surprising or relatable part, not the procedure. Plain words, short sentences, a normal person's wording: "He got pulled over because of someone else's license" beats "A deputy ran a plate, saw the owner's license was revoked, and pulled the truck over."
  - Don't write legal-brief phrasing: "sided with the village", "reached court", "upheld the stop", "the court found". Say what actually happened to the people: who won, what it cost them, what they had to do.
  - **Two caption styles, tested 50/50 (Luke, 2026-10-14).** The planner gives every non-question post a `captionStyle`; use it and save it on the post in history:
    - `payoff`: the image is the hook. It sets up the situation and the conflict so a stranger instantly gets it, then stops right before the ending: who won, what it cost, what the judge said is NEVER on the image. End the slide on the tension ("He said the cop was only guessing.", "The village wanted $50 a day."). The caption delivers the ending: 2 to 4 short spoken sentences (max ~60 words), how it ended, one detail that makes it land, then an open question.
    - `classic`: the image tells the whole story including the outcome, in plain spoken words. The caption is one short teasing line (max ~20 words) ending in an open question.
    - Both: then a blank line, 2-3 hashtags, and the Source line for real cases. Never write "read the caption", "see below" or 👇. These rules override Hookline's own caption instruction.
  - Read it aloud: if you wouldn't say it that way to a friend, rewrite it. The caption never repeats the slide word for word.
- Coherence: re-read every slide and the caption before rendering; each sentence complete, grammatical and sensible on its own and after the previous slide. Same amount of text as before.

**Photo first (Luke's rule):** most Jury Juice posts are photo posts. Real cases, weird laws and strangest trials are always photo style (single or Instagram carousel); only quick questions are tweet slides, at most 1 a day. Use the style the planner gives.

Read these before writing anything:
- `jury-juice-brief.md`: voice, caption rules, every post type's slide structure, photo rules,
  Meta platform rules, humanizer rules and banned words. Follow it exactly.
- The `meta-posting-rules` and `humanizer` skills if they are available in this session.
- `state/config.json`: mode (draft or queue), Buffer IDs, windows, formats.

## Hard rules (never break these)
0. **Every post passes `META_CHECK.md`** (Meta Community Standards and monetization policies)
   before it is saved to Buffer. Luke's pages are monetized; a failed check means fix or replace.
1. **Real facts are verified.** For types list, laws and history, every case, law, name,
   date, amount and outcome must be confirmed with web search against at least one reliable source
   (court records, major news outlets, government or legal sites, encyclopedias). If a fact can't
   be confirmed, cut it or replace the case. If a whole post can't be verified, replace it with
   another topic of the same type. Never guess.
2. **Engagement questions** never mention violence, injuries, death, real people,
   minors, politics or anything that could get the page restricted. Everyday police, HOA and
   county topics (traffic stops, tickets, HOA letters, permits) are fine as long as nobody is hurt. Never ask people to
   comment, vote, like, share or tag.
3. **No realistic images of real people.** Photo posts about real cases show objects, places or
   generic anonymous scenes, never someone made to look like the real person.
4. **Never repeat a topic or a title.** Check the INDEX from `history_view.py` before writing: no case, law or
   trial that appeared in any earlier post, and no hook or caption title that matches or closely
   resembles an earlier one (e.g. never reuse "5 lawsuits too bizarre to be real"; vary the angle:
   "Lawsuits judges threw out in minutes", "Companies sued over the dumbest things"). Save each
   post's `title` in history. Also skip cases used in Hookline's built-in example (Brock v. Brock,
   Leonard v. PepsiCo, Heckard v. Jordan, Junior Mints, Red Bull wings) for list posts.
5. **Mode:** if `state/config.json` mode is `draft`, every post is saved with `saveToDraft: true`.
   Only switch behaviour if the file says `queue`. Never change the mode yourself.
6. **OpenAI credit out = no more image prompts.** If `state/config.json` has `"imagesPaused": true`,
   never call `generate_image`; make every post tweet style. If any `generate_image` call fails
   because the OpenAI account is out of money (errors like "insufficient_quota", "billing",
   "credit", "hard limit", "exceeded your current quota", or a 429 that mentions quota), stop
   sending image prompts immediately for the rest of the run, switch the remaining photo posts to
   tweet style, set `"imagesPaused": true` and `"imagesPausedReason"` (date + error) in
   `state/config.json`, and tell Luke at the top of the summary. Only Luke turns images back on.
7. Never publish immediately (`shareNow`). Never delete or edit posts you didn't create in this run,
   except clearing old image files from this repo.

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
  Crow). If its `lastRun` is more than 20 hours old (both bots run twice a day, about 7:48/13:48 and 8:12/14:12, so anything under 20 hours is normal; or missing after its first day), report
  `⚠️ PROBLEM: the <other page> bot hasn't run since <time>` so Luke can check its scheduled task.
- **Posts Luke deletes are not a problem.** Luke sometimes deletes queued posts in Buffer on
  purpose. If `get_post` says a post is not found (404) and it was never sent, mark it
  `"status": "deleted-by-luke"` in history, skip it in every check and report, and don't raise a
  PROBLEM for it. Posts already marked `deleted-by-luke` are ignored.
- **Every planned post is accounted for.** If the plan gave N posts and you made fewer, save each
  missing one in history as `"status": "skipped"` with `"skipReason"` (the exact reason), and say
  in the summary which post was skipped and why, e.g. "Made 1 of 2: the note was skipped because
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
- `cd` into the repo, `git pull`. Work out the run and posting day as described at the top (always today's date in America/Toronto).
- **Read history the cheap way:** run `python3 scripts/history_view.py jury` once. It prints an INDEX of every earlier post (titles, topics, subtopics), the last 10 captions in full, the 3 best captions, the posts to failure-check and the posts to refresh metrics for, and writes `work/avoid.json`. Use that output everywhere this guide says "check history". Do NOT open or print `state/history.json` (it is large); only append your new posts to it with a short python snippet.
- Install nothing new unless needed; `playwright` (with Chromium) is preinstalled. Run renders with `node render.js`.

### 2. Update analytics (only if the last update was 40+ hours ago, i.e. every other day; skip if no posts yet)
- For each post listed under METRICS (sent 1 to 14 days ago, has a Buffer post ID; refresh them
  every other day; save the time in `lastMetricsAt` in this page's config),
  call Buffer `get_post` with `includeMetrics: true` (only for those posts; mind rate limits:
  max ~40 calls per run).
- Save per platform under `metrics.facebook` / `metrics.instagram`: the raw metrics, plus
  `engagementRate` = (reactions/likes + comments + shares + saves) ÷ reach (use impressions if
  reach is missing; leave null if neither). Record `measuredAt`.
- If a draft was never approved (still draft/not sent after 3 days), mark it `"status": "skipped"`.

### 2b. Learn from Luke's insights: **Sunday `pm` run only (the ~13:48 run on a Sunday).** On Sundays (and only then) read `BOT-WEEKLY.md` and do its step 2b first. Other days skip it.

### 3. Plan the day
- Run `python3 scripts/plan_day.py <date> <run>` (`<run>` = `am` or `pm`). It returns this run's posts (the windows of this run only) with
  window, type, format, style, an optional topic hint and planned `facebookAt` / `instagramAt` times.
  It already counts today's earlier posts (max 5 a day; max 1 quick question a day; max 1 carousel a day and 4 a week, and
  carousels only ever go to Instagram, see step 8) and keeps posts well spaced (one in each window, 90+ minutes apart). Use them as given.
  If it returns no posts, today is full: skip to the summary.
- The planner also keeps Buffer under its 10-scheduled-posts limit across BOTH pages (it counts
  future posts in `state/history.json` and `state/oldcrow/history.json`). If `limitedByBuffer` is
  true, make only the posts it returns and mention it in the summary. Always record each scheduled
  post with `"status": "scheduled"` and its `plannedAt` + `postId` so the other bot can count it.
- If a planned time is already in the past, add 1 to 3 hours (random minute) within the same day.

### 4. Write each post
- Before writing, read `state/learnings.md` and apply its **Do more / Do less** lines to the topic, hook,
  slides and caption. About 1 post in 4, try one idea from **Test next** and save it on the post as
  `"experiment": "<what was tested>"` in history so the next review can judge it. Also re-read the
  BEST section (3 best-performing captions) and match what made them work (without copying them).
- Luke's own rules always win over learnings: short captions, no sources in captions, good
  searchable hashtags, no engagement bait, Meta rules, fact-checking, carousel limits.
- Follow `jury-juice-brief.md` for the post's type and style. Carousels use the type's default
  slide count (7) unless the content needs fewer; singles are exactly 1 slide.
- If the topic hint is empty, choose a fresh topic for that type. **Follow the brief's "Audience
  focus"**: about 70% police (always varied, see the brief's police subject list), 20% county/city government, and only about 1 in 20 HOA (Luke 2026-10-14: mostly police, HOA rarely),
  and the brief's police safety rules on every police post.
- Output for each post: `slides` (text, and `scene` for photo style), `caption`, and for real
  types a `sources` list (item + source URL or citation).
- Run the humanizer rules over the slides and caption. Check the banned words list.

### 5. Fact-check (types list, laws, history)
- Search the web for every claim. Fix or drop anything wrong. One reliable source per claim is enough: stop searching a claim once it is confirmed, don't re-search facts you already confirmed, and don't search at all for engagement questions.
- **Short sources go at the bottom of the caption** (Luke's rule), never on the slides: after the
  hashtags, a blank line and `Source: <case (year)>` or `Sources: <case (year)>; <case (year)>`,
  using the sources you actually confirmed. Engagement questions get no source line.
- **Captions** follow the post's `captionStyle` (see "Two caption styles" above): `payoff` = 2-4 short
  sentences with the ending, `classic` = one short teasing line (max ~20 words); both end with an open
  question, then a blank line, 2 or 3 hashtags starting with #JuryJuice, then for real cases/laws a blank
  line and the one short source line above. No `References:` block, no headlines, no links, no
  legal-brief wording. Quick-question (engage) posts keep one short line.
- **Hashtags:** the page tag first, then 1 or 2 popular, widely searched tags that name the post's
  actual subject, in CamelCase (e.g. #McDonalds #LawFacts, #GuineaPigs #WeirdLaws, #Nostalgia,
  #SlowLiving, #EngagementRing). Never made-up or niche tags nobody searches (#oldcrowasks,
  #thingswearesold, #notes, #busy) and never vague filler (#history, #facts).

### 6. Make the slides
- First check hard rule 6 (`imagesPaused`). If images are paused, render photo posts as tweet style.
- Photo style: for each slide, call `generate_image` (Hookline Images connector) with the scene,
  then the photo style + composition lines from the brief, ending with the no-text line.
  Use model `flare`, quality `medium`, aspect `4:5`. The tool result names the saved file path;
  copy it into the post folder (e.g. `work/p1/img1.jpg`). Max 8 images per run; if a carousel
  would go over, switch that post to tweet style.
- **The photo must match the text.** If the slide says man, woman, he, she, a couple, etc., the person in the photo must match (state the gender and number of people in the scene prompt), or show no person at all (objects, hands, a doorway). Look at the generated photo for this before rendering; regenerate if it doesn't match.
- Write a spec file and render:
  `{"page":"jury","style":"tweet"|"photo","caption":"...","slides":[{"text":"...","image":"img1.jpg"}]}`
  Tweet-style posts: add `"theme"` from the plan (`black`, `light` = white with black text, `dim` =
  classic Twitter navy). The planner rotates them so tweet posts cycle through all three; save
  `theme` in history for every tweet post so the rotation continues.
  then `node render.js work/p1/spec.json posts/<date>/<n>-<type>/`.
- Look at every rendered slide (read the JPGs). Fix overflowing or awkward text and re-render.

### 6b. Meta check (every post, no exceptions)
- Run the full checklist in `META_CHECK.md` on every finished post (slides, caption, hashtags,
  alt text). Only posts that pass go any further. Fix or replace anything that fails.

### 7. Publish images
- `git add posts/ state/ && git commit -m "Posts for <date> <run>" && git push`.
- Image URL: `https://raw.githubusercontent.com/luketcarey-star/juryjuice-media/main/posts/<date>/<n>-<type>/slideK.jpg`

### 8. Save to Buffer
For each post, two `create_post` calls:
- **No carousels on Facebook (Luke's rule).** Carousels go to the Jury Juice Instagram only. When
  the plan says `carousel`, also make a single-image version of the same post for Facebook: one
  standalone slide in the same style with the hook and payoff together (photo: up to 25 words;
  tweet: the strongest line or two), rendered to `posts/<date>/<n>-<type>/fb/slide1.jpg`, with
  the same caption. Record it as `facebook.format: "single"` in history. Singles go to both as is.
- Facebook: channel `facebookChannelId`, `metadata: {facebook: {type: "post"}}`, `schedulingType: "automatic"`.
- Instagram: channel `instagramChannelId`, `metadata: {instagram: {type: "post", shouldShareToFeed: true}}`, `schedulingType: "automatic"`.
- Both: `text` = caption, `assets` = all slide URLs in order with short `altText`,
  `mode: "customScheduled"`, `dueAt` = that platform's planned time.
  Draft mode: also `saveToDraft: true`. If Buffer rejects scheduling info on drafts, retry with
  only `saveToDraft: true` and put the planned time in the run summary.
- Buffer free plan allows only 10 scheduled posts at a time; never queue more than one day ahead.

### 9. Record and clean up
- Append each post to `state/history.json` → `posts`:
  `{date, n, type, topicGroup (police | hoa | county | other), format, style, theme, title, topic, slides, sources, imageFolder,
    facebook: {postId, plannedAt}, instagram: {postId, plannedAt}, status: "draft"|"scheduled", metrics: {}}`
- Delete `posts/<date>` folders older than `keepImagesDays` (already posted; Meta keeps its own copy).
- Commit and push.

### 10. Weekly report and tune-up: **Sunday `pm` run only.** On Sundays (and only then) do step 10 from `BOT-WEEKLY.md` before the summary. Other days skip it.

### 11. Summary for Luke (always, keep it short)
- What was made: for each post, type, title, planned FB and IG times, draft or scheduled.
- Fact-check: anything that couldn't be confirmed and was swapped out, and why.
- Any errors or skipped steps.
- Any post idea worth suggesting (always on Sundays; other days only if a good one came up).
