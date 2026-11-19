# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/geminigisa/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/geminigisa/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

Entry for make.fun's bounty **"Post a GTA 6 meme on X"**
([gta6-meme-x-01](https://make.fun/bounty/gta6-meme-x-01)).

The meme: the 13-year wait for GTA VI as the classic waiting-skeleton meme —
a skeleton slumped on a Vice City bench at sunset beside make.fun's ghost
(the official press-kit mark), who spent the wait earning bounty money.
Original synthwave scene drawn with Pillow by `tools/make_meme.py`; the ghost
is make.fun's own logo asset from the press kit, composited in as the bench
companion. `meme.png` (1024×1024) is the picture posted on X.

`main.ts` (Node 22, standard library only) validates `POST.json`'s X-post
shape and copies it to `/output/POST.json` for the gate. The entry is the post
itself: the house reads it from X, an AI judge compares posts two at a time,
and the top 50 share $500.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

`POST.json` names the public X post: `{"url": "https://x.com/<handle>/status/<id>"}`.
The post carries the meme as its first picture, make.fun (link or written out)
or a tag of @makefunai, and the entrant's play code.

## Build

The meme was rendered in the agent session that built this entry:

```sh
python3 tools/make_meme.py   # requires Pillow; writes meme.png
```

## License

MIT — see [LICENSE](LICENSE). The scene is original; the ghost mark is
make.fun's press-kit asset, used as the bounty's rules direct.

---

<sub>Entered on [make.fun](https://make.fun/?ref=rn8n62kp&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
