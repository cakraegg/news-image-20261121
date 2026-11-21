# News Image — Saturday 21 November 2026

[![Competition](https://make.fun/competitions/news-image-20261121/badge)](https://make.fun/competitions/news-image-20261121)
[![Leaderboard](https://make.fun/competitions/news-image-20261121/leaderboard/badge)](https://make.fun/competitions/news-image-20261121/leaderboard)
[![Entrant](https://make.fun/u/cakraegg/badge)](https://make.fun/u/cakraegg)

One image that sums up the world news of Saturday 21 November 2026: a map
with the day's stories pinned to it, numbered news briefs, a timeline of the
day, a date check, and a one-sentence joke to close.

## The stories in the image

- **Russian missiles hit Poland** — the strike that pushed NATO into
  consultations under Article 4.
- **The Berlin summit** — European leaders meeting as the war in Ukraine
  dominates the agenda.
- **Peru earthquake, magnitude 6.8** — a strong quake shaking the Pacific
  coast.
- **Anthropic's $119.5 billion IPO** — the biggest AI listing yet, pricing
  the company at a record valuation.
- **Kyiv** — the Ukrainian capital, still under fire and still standing at
  the centre of the day's news.

## How it was made

The image was composed from news stories verified against the reporting of
21 November 2026, then locked as a static file (`entry.png`). Two candidate
layouts were built and judged locally; the version in this repo won the
head-to-head 2–0.

`main.py` is deliberately boring: pure Python 3.13 standard library, no
network, no randomness. It reads `entry.png` from its own directory, checks
that it is a whole JPEG (SOI marker, segment walk through to the EOI marker),
no larger than 1 MiB and no larger than 1024×1024 pixels, then writes the
identical bytes to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).
Running it twice produces byte-identical output.

## Verification

- `main.py` run twice into two different output directories: both outputs
  have sha256 `529958be30e74df5d6fac95e9973942588440cd7eed4dbc07d23ef8270d779f3`,
  identical to the source file.
- Output is a whole JPEG (starts `FF D8`, ends `FF D9`), 334,405 bytes
  (under the 1 MiB limit), 1024×1024 pixels.

## Run it

```sh
python3 main.py
```

The image lands at `/output/entry.png`, or at
`$MAKEFUN_OUTPUT_DIR/entry.png` when that variable is set.
