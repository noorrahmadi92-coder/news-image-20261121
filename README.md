# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/noorrahmadi92-coder/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/noorrahmadi92-coder/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page that sums up the world's news of Saturday, 21 November
2026, in one 1024×1024 image. Six stories, each with a picture and a short
headline, under a masthead that names the day.

## The six stories

1. **Lead — Riyadh:** Saudi-led coalition interceptors destroy three Houthi
   ballistic missiles fired towards Riyadh early on Saturday, the third
   straight night of air-raid alerts in the capital.
2. **Climate — Antalya:** COP31 talks are extended as nearly 200 nations stay
   deadlocked over fossil fuels.
3. **Markets — New York:** The AI sell-off deepens. Nasdaq dives 5.3%, wiping
   out its 2026 gains; S&P 500 falls 3.7% into correction; Nikkei drops 5.1%.
4. **Business — United States:** A Missouri judge approves Bayer's $7.25bn
   settlement of Roundup lawsuits.
5. **Disaster — Basra:** A fire at the Hartha power station kills at least
   four and injures 30; the 800 MW plant halts.
6. **Tech — United States:** The FBI's criminal database is reportedly hacked
   and under investigation; the USDA was also hit.

## How to run

```sh
python3 draw.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw.py` draws the whole image with Pillow and the DejaVu fonts; it uses no
network and no photos, so its output is byte-identical on every run.
`main.ts` (Node 22, standard library only) copies `entry.png` to the
output directory after checking its PNG magic bytes.
