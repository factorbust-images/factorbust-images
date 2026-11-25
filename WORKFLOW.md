# Fact or Bust? – weekly workflow

Image host and toolkit for the Instagram account **@factorbust.darts** (English, fan account, not affiliated with the PDC).
Posts are published through Buffer (Instagram channel `factorbust.darts`), which pulls images from
`https://raw.githubusercontent.com/factorbust-images/factorbust-images/main/posts/<file>.png`.
**Never delete or rename images in `posts/`** – scheduled posts fetch them at publish time.

## Format
- Carousel, 2 slides, 1080×1350 (4:5).
- Slide 1: a darts claim + "FACT or BUST" pills. Slide 2: verdict stamp (`Fact`, `Bust` or `Legend`), short answer (max ~55 words), sources line.
- Mix verdicts across the week (not predictable). Numbering continues from the last post in `data/topics.md`.
- Render: `python3 tools/render.py data/week-YYYY-WW.json posts` (needs Playwright + Chrome at `/usr/bin/google-chrome`, fonts Anton + Inter).
- Caption: one short hook line, then `Fact or Bust? Guess first, then swipe 👉`, blank line, 6 hashtags (`#darts #dartsfacts #factorbust` + 3 topical).
- Alt text on every image (slide 1 = claim, slide 2 = verdict + answer).

## Fact-check rules (non-negotiable)
- Every claim needs **at least two independent sources**, at least one reliable/primary (darts historian Dr Patrick Chaplin, PDC, Sky Sports, BBC, AP/Reuters, Wikipedia with references, MasterCaller, DartsNews).
- Sources disagree or only one source → mark as **Legend** (if it's a famous story) or **drop it**. Better no post than a wrong one.
- Numbers that change (followers, rankings) → say "more than X" and only from a recent source.
- Write everything in our own words. No quotes longer than a few words.

## Legal / taste rules
- No photos of players, no TV screenshots or clips, no logos. Only our own graphics.
- No private matters (health, family, relationships), nothing defamatory, no mocking.
- No betting odds, no bookmaker links or promotion.
- Fan account: never imply we are official.
- AI Act: texts are AI-assisted; the account owner reviews and approves every post before scheduling (editorial control). Images are template graphics, not AI images → `isAiGenerated: false`.

## Scheduling
- One post per day at **19:30 Europe/Berlin** (18:30 UK), via Buffer `customScheduled`.
- New batch continues the day after the last scheduled post.
- Buffer free plan: max 10 scheduled posts at a time – check before adding.
- **Nothing is scheduled without the owner's explicit approval in chat.**
