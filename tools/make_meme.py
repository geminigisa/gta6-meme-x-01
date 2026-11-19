#!/usr/bin/env python3
"""Render the GTA VI meme for make.fun's gta6-meme-x-01 bounty.

The joke: the 13-year wait for GTA VI as the classic waiting-skeleton meme —
a skeleton on a Vice City bench at sunset, next to make.fun's ghost (the
official press-kit mark) who spent the wait earning bounty money. Original
scene drawn with Pillow; the ghost mark is make.fun's own press-kit asset,
composited in as the bench companion. 1024x1024, deterministic.

Run:  python3 tools/make_meme.py   (writes meme.png at the repository root)
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W = H = 1024
INK = (22, 18, 26)
BONE = (246, 244, 238)
WOOD = (96, 64, 44)
WOOD_D = (64, 42, 30)
MAGENTA = (226, 44, 138)

F_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(p, s):
    return ImageFont.truetype(p, s)


def outlined_text(d, xy, text, fnt, fill, anchor="mm", ow=5):
    x, y = xy
    for dx in range(-ow, ow + 1, ow):
        for dy in range(-ow, ow + 1, ow):
            if dx or dy:
                d.text((x + dx, y + dy), text, font=fnt, fill=INK, anchor=anchor)
    d.text((x, y), text, font=fnt, fill=fill, anchor=anchor)


def palm(d, x, y, h, col):
    topx, topy = x + 6, y - h
    d.polygon([(x - 5, y), (x + 5, y), (topx + 3, topy), (topx - 3, topy)], fill=col)
    for a in (-170, -135, -95, -55, -15, 25):
        ar = math.radians(a)
        L = h * 0.42
        tipx = topx + L * math.cos(ar)
        tipy = topy + L * math.sin(ar) * 0.5 + h * 0.10
        midx = topx + L * 0.55 * math.cos(ar)
        midy = topy + L * 0.55 * math.sin(ar) * 0.25 - h * 0.05
        d.polygon([(topx, topy), (midx, midy - 5), (tipx, tipy), (midx, midy + 5)], fill=col)


def skeleton(d, cx, seat):
    """A slouched waiting skeleton, bones outlined in ink."""
    hy = seat - 150                      # skull centre
    # skull
    d.ellipse([cx - 40, hy - 40, cx + 40, hy + 34], fill=BONE, outline=INK, width=6)
    d.rectangle([cx - 24, hy + 22, cx + 24, hy + 48], fill=BONE, outline=INK, width=5)
    d.ellipse([cx - 26, hy - 14, cx - 6, hy + 10], fill=INK)
    d.ellipse([cx + 6, hy - 14, cx + 26, hy + 10], fill=INK)
    d.polygon([(cx, hy + 12), (cx - 6, hy + 22), (cx + 6, hy + 22)], fill=INK)
    for tx in range(cx - 18, cx + 19, 9):
        d.line([(tx, hy + 26), (tx, hy + 44)], fill=INK, width=3)
    # spine + ribs
    d.line([(cx, hy + 48), (cx, seat - 40)], fill=BONE, width=10)
    d.line([(cx, hy + 48), (cx, seat - 40)], fill=INK, width=2)
    for i in range(4):
        ry = hy + 62 + i * 18
        d.arc([cx - 34, ry - 8, cx + 34, ry + 12], 0, 180, fill=BONE, width=8)
        d.arc([cx - 34, ry - 8, cx + 34, ry + 12], 0, 180, fill=INK, width=2)
    # pelvis
    d.polygon([(cx - 26, seat - 44), (cx + 26, seat - 44), (cx + 16, seat - 16), (cx - 16, seat - 16)],
              fill=BONE, outline=INK, width=5)
    # left arm draped on the bench back, right arm on the knee
    d.line([(cx - 30, hy + 66), (cx - 78, hy + 40), (cx - 118, hy + 52)], fill=BONE, width=9)
    d.line([(cx - 30, hy + 66), (cx - 78, hy + 40), (cx - 118, hy + 52)], fill=INK, width=2)
    d.ellipse([cx - 126, hy + 44, cx - 110, hy + 60], fill=BONE, outline=INK, width=4)
    d.line([(cx + 30, hy + 66), (cx + 56, seat - 60), (cx + 40, seat - 18)], fill=BONE, width=9)
    d.line([(cx + 30, hy + 66), (cx + 56, seat - 60), (cx + 40, seat - 18)], fill=INK, width=2)
    # legs: thigh forward, shin down, feet on the ground
    for sx in (-14, 14):
        d.line([(cx + sx, seat - 24), (cx + sx + 44, seat - 6)], fill=BONE, width=10)
        d.line([(cx + sx, seat - 24), (cx + sx + 44, seat - 6)], fill=INK, width=2)
        d.line([(cx + sx + 44, seat - 6), (cx + sx + 38, seat + 78)], fill=BONE, width=9)
        d.line([(cx + sx + 44, seat - 6), (cx + sx + 38, seat + 78)], fill=INK, width=2)
        d.ellipse([cx + sx + 26, seat + 72, cx + sx + 62, seat + 88], fill=BONE, outline=INK, width=4)


def ghost_mark(size):
    """The official press-kit mark, circular-masked if its corners are opaque."""
    m = Image.open(ROOT / "tools" / "mark-1024.png").convert("RGBA")
    if m.getpixel((2, 2))[3] > 128:
        mask = Image.new("L", m.size, 0)
        ImageDraw.Draw(mask).ellipse([4, 4, m.size[0] - 4, m.size[1] - 4], fill=255)
        m.putalpha(mask)
    return m.resize((size, size), Image.LANCZOS)


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    # ── Vice City sunset ──
    for y in range(820):
        t = y / 820
        if t < 0.55:
            u = t / 0.55
            c = (int(38 + 116 * u), int(18 + 34 * u), int(72 + 34 * u))
        else:
            u = (t - 0.55) / 0.45
            c = (int(154 + 96 * u), int(52 + 92 * u), int(106 - 16 * u))
        d.rectangle([0, y, W, y + 1], fill=c)
    # slitted sun
    sx, sy, sr = 764, 330, 96
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 148, 96))
    for i in range(6):
        yy = sy + 6 + i * 15
        half = math.sqrt(max(sr * sr - (yy - sy) ** 2, 0))
        t = yy / 820
        c = (int(154 + 96 * ((t - 0.55) / 0.45)), int(52 + 92 * ((t - 0.55) / 0.45)), int(106 - 16 * ((t - 0.55) / 0.45))) if t > 0.55 else (154, 52, 106)
        d.rectangle([sx - half, yy, sx + half, yy + 5], fill=c)
    # skyline strip + palms
    for bx, bw, bh in [(40, 46, 90), (100, 34, 130), (150, 50, 70), (820, 40, 110), (876, 54, 80), (944, 40, 140)]:
        d.rectangle([bx, 820 - bh, bx + bw, 820], fill=(30, 16, 44))
    palm(d, 96, 820, 250, (24, 12, 36))
    palm(d, 950, 820, 210, (24, 12, 36))
    # neon ground
    d.rectangle([0, 820, W, 900], fill=(28, 14, 40))
    for gx in range(0, W + 1, 64):
        x2 = W / 2 + (gx - W / 2) * 1.7
        d.line([(gx, 820), (min(max(x2, 0), W), 900)], fill=(120, 40, 100), width=2)
    for gy in (838, 862, 888):
        d.line([(0, gy), (W, gy)], fill=(120, 40, 100), width=2)

    # ── top caption ──
    outlined_text(d, (W / 2, 78), "WAITING FOR GTA VI LIKE…", font(F_B, 58), (255, 255, 255), ow=6)

    # ── the bench ──
    seat = 700
    d.rectangle([180, seat, 844, seat + 22], fill=WOOD, outline=INK, width=5)
    d.rectangle([180, seat + 30, 844, seat + 44], fill=WOOD_D, outline=INK, width=4)
    for lx in (210, 800):
        d.rectangle([lx, seat + 44, lx + 16, 812], fill=WOOD_D, outline=INK, width=4)
    d.rectangle([180, seat - 96, 196, seat], fill=WOOD_D, outline=INK, width=4)
    d.rectangle([828, seat - 96, 844, seat], fill=WOOD_D, outline=INK, width=4)
    d.rectangle([180, seat - 96, 844, seat - 76], fill=WOOD, outline=INK, width=5)

    # ── sign: the release-date wait ──
    d.rectangle([872, 560, 888, 812], fill=WOOD_D, outline=INK, width=4)
    d.rectangle([856, 470, 1010, 566], fill=(246, 240, 226), outline=INK, width=5)
    d.text((933, 494), "GTA VI", font=font(F_B, 30), fill=INK, anchor="mm")
    d.text((933, 524), "RELEASE DATE", font=font(F_B, 21), fill=INK, anchor="mm")
    d.text((933, 548), "2013 → 2026", font=font(F_B, 24), fill=MAGENTA, anchor="mm")

    # ── the waiting skeleton ──
    skeleton(d, 330, seat)

    # ── make.fun's ghost, fresh as ever, coin in hand ──
    g = ghost_mark(236)
    img.paste(g, (560, 470), g)
    d = ImageDraw.Draw(img)

    # ── the ghost's speech bubble ──
    d.rounded_rectangle([470, 300, 980, 452], radius=22, fill=(255, 255, 255), outline=INK, width=5)
    d.polygon([(640, 450), (680, 450), (628, 492)], fill=(255, 255, 255), outline=INK)
    d.line([(642, 450), (628, 490)], fill=(255, 255, 255), width=6)
    d.text((725, 330), "13 years? I earned $500", font=font(F_B, 30), fill=INK, anchor="mm")
    d.text((725, 368), "on make.fun bounties", font=font(F_B, 30), fill=INK, anchor="mm")
    d.text((725, 406), "while you waited.", font=font(F_B, 30), fill=INK, anchor="mm")

    # ── bottom band: the pitch, in the meme's voice ──
    d.rectangle([0, 900, W, H], fill=INK)
    d.text((W / 2, 940), "make.fun", font=font(F_B, 46), fill=(255, 255, 255), anchor="mm")
    d.text((W / 2, 986), "people + AI agents win real money in bounties", font=font(F_R, 28), fill=MAGENTA, anchor="mm")

    out = ROOT / "meme.png"
    img.save(out, optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
