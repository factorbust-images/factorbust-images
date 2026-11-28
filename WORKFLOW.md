# Fact or Bust? – weekly workflow

Image host and toolkit for the Instagram account **@factorbust.darts** (English, fan account, not affiliated with the PDC).
Posts are published through Buffer (Instagram channel `factorbust.darts`), which pulls media from
`https://raw.githubusercontent.com/factorbust-images/factorbust-images/main/posts/<file>`.
**Never delete or rename files in `posts/`** – scheduled posts fetch them at publish time.

## Weekly mix (since 2026-11-28)
Reach to non-followers comes mainly from Reels; carousels mostly reach existing followers.
- **Reel every day at 19:30 Europe/Berlin** (18:30 UK) – 7 per week, one new fact each.
- **Carousel 3× per week (Fri, Sun, Tue) at 12:30 Europe/Berlin** – a *different* fact each (deep-dive for followers).
- = **10 new facts per batch**, batch runs Thursday → Wednesday. Buffer free plan allows max 10 scheduled posts,
  so a batch is created on Thursday morning when the previous batch has fully published.
- Transition week 29.11.–02.12.2026 was special (reels of #001–#004 at 12:30, carousels #003–#007 at 19:30).

## Formats
- **Reel** (9:16, 1080×1920, ~14 s, H.264 + silent AAC): claim 3.5 s → countdown 3-2-1 → reveal 9 s.
  Render: `python3 tools/render_reel.py data/week-YYYY-WW.json posts [numbers…]` → `posts/fob-NNN-reel.mp4`.
  Buffer: `assets=[{video:{url, metadata:{title:"Fact or Bust #NNN", thumbnailOffset:1000}}}]`,
  `metadata.instagram = {type:"reel", shouldShareToFeed:true, isAiGenerated:false}`.
- **Carousel** (4:5, 1080×1350, 2 slides): claim + FACT/BUST pills, then verdict stamp + answer + sources.
  Render: `python3 tools/render.py data/week-YYYY-WW.json posts` → `posts/fob-NNN-1.png`, `-2.png`.
  Buffer: two image assets with alt text, `metadata.instagram = {type:"post", shouldShareToFeed:true, isAiGenerated:false}`.
- Same JSON format for both (`no`, `claim`, `verdict` Fact/Bust/Legend, `answer` ≤ ~55 words, `sources`). Add `"format": "reel"` or `"carousel"`.
- Mix verdicts across the week. Numbering continues from the last post in `data/topics.md`.
- Always look at every rendered frame/slide before publishing (text must not overflow).

## Captions
- Line 1: short hook. Line 2: `Fact or Bust? Comment your guess BEFORE the reveal 👀` (reel) or `Fact or Bust? Guess first, then swipe 👉` (carousel).
- Line 3: `Send this to the mate who thinks he knows darts 🎯` (DM sends are the strongest signal for reaching new people).
- Blank line, then **max. 5 hashtags** (Instagram hard limit since Dec 2025): `#darts #dartsfacts #factorbust` + 2 topical. No `#pdc`.

## World Championship 11 Dec 2026 – 3 Jan 2027 (Alexandra Palace)
- Prefer facts about players who play that day or the next (check the official schedule), Ally Pally history, records, walk-ons, nicknames.
- Facts only – no predictions, no results we cannot verify yet, no betting odds.
- No play 24–27 Dec: use evergreen facts.

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
- AI Act: texts are AI-assisted; the account owner reviews and approves every post before scheduling (editorial control). Graphics/videos are template renders, not AI images → `isAiGenerated: false`.

## Scheduling
- Buffer `customScheduled` with correct Europe/Berlin UTC offset.
- **Nothing is scheduled without the owner's explicit approval in chat.**
