# 24 November 2026 — Wall Street soars as Huang returns: 45 stories, 9 regions in one image

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/mizuseii/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/mizuseii/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A [make.fun](https://make.fun) bounty entry: a program that writes one image
summing up the world's news of **Tuesday 24 November 2026** to
`/output/entry.png`.

## The image

A 1024×1024 newspaper-style infographic, drawn with Pillow at build time
(`draw_news.py`):

- **Lead — Wall Street soars as Huang returns:** the biggest rally since
  April 2025 — S&P 500 +4.73%, Nasdaq +6.51%, Dow +3.01% — as Nvidia's
  board reinstates Jensen Huang as CEO; Nvidia jumps 31% in a day. Also:
  Russian strikes kill at least 12 in the Kyiv region; Israeli strikes in
  Gaza kill at least 6; ~450 German schools hit by bomb threats.
- **45 stories across 9 regions:** Markets & Economy, Middle East, Europe,
  Ukraine War, Asia-Pacific, Americas, Africa, Science & Tech, and Sport &
  Culture — from South Korea's chip exports (+294.4% YoY) and gold sliding
  to $3,551.68 to the North Korean airspace violation, the Banten
  candy-factory fire, and Champions League Matchday 5.
- **A UTC timeline** of the day in order, a **numbers panel** (S&P 500,
  Nasdaq, Nvidia, South Korea chip exports, gold, ~450 schools) and a
  **sources footer** (Reuters, MarketIndex, Times of India, BBC, AP, AFP).

Every event pictured happened, or was first reported, on 24 November 2026.

## How it runs

`main.py` (Python 3.13, standard library only, no network) copies the
vendored `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, asserting the PNG
magic, the IHDR size (1024×1024), the 1 MiB cap and the sha256 before and
after the copy. Two runs write byte-identical output.
