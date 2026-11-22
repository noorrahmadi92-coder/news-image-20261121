#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

Run:  python3 draw.py            (writes entry.png next to this file)
The image is a newspaper front page: a masthead naming the day, a wide
hero panel on the Saudi missile interception over Riyadh, two stories
in the middle row (COP31 deadlock, the market sell-off), and three
smaller stories along the bottom (Bayer settlement, Basra power-plant
fire, the reported FBI database hack). Everything is drawn with Pillow
and the DejaVu fonts shipped on this machine; no network, no photos,
no randomness, so the output bytes are identical on every run.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
MAROON = (96, 18, 30)        # masthead
MAROON_DARK = (66, 12, 20)
GOLD = (235, 190, 80)
CREAM = (248, 244, 233)      # page background
CARD = (255, 255, 255)
INK = (22, 22, 22)
GREY = (96, 96, 96)
RED = (176, 30, 30)
TEAL = (13, 106, 106)
GREEN = (32, 116, 58)
BLUE = (26, 82, 148)
AMBER = (196, 120, 20)
LINE = (216, 210, 196)
NIGHT = (10, 18, 44)         # night-sky illustration
NIGHT_LOW = (24, 40, 84)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_bold(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def sans_bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width pixels."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading=None):
    """Draw lines of text; return the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def kicker(draw, x, y, label, color, size=20):
    """Small bold coloured kicker line; returns y below it."""
    draw.text((x, y), label, font=sans_bold(size), fill=color)
    return y + size + 7


def card(draw, x, y, w, h, accent=None):
    """White card with a thin outline and an optional left accent bar."""
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=CARD, outline=LINE, width=2)
    if accent is not None:
        draw.rectangle([x + 2, y + 8, x + 8, y + h - 8], fill=accent)


# --- masthead --------------------------------------------------------------
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 118], fill=MAROON)
    draw.rectangle([0, 112, W, 118], fill=GOLD)
    draw.text((28, 14), "THE WORLD IN ONE DAY", font=sans_bold(22), fill=GOLD)
    draw.text((28, 32), "WORLD NEWS", font=serif_bold(50), fill=(255, 255, 255))
    draw.text((28, 90), "Saturday, 21 November 2026",
              font=sans_bold(20), fill=GOLD)
    right = "SIX STORIES"
    tw = draw.textlength(right, font=sans_bold(30))
    draw.text((W - 28 - tw, 22), right, font=sans_bold(30), fill=(255, 255, 255))
    sub = "that defined the day"
    tw2 = draw.textlength(sub, font=sans(22))
    draw.text((W - 28 - tw2, 58), sub, font=sans(22), fill=(220, 205, 190))


# --- hero: Riyadh missile interception -------------------------------------
def draw_hero_sky(draw, x, y, w, h):
    """Night sky over the Riyadh skyline: interceptor trails and bursts."""
    draw.rectangle([x, y, x + w, y + h], fill=NIGHT)
    # stars
    for sx, sy, r in [(40, 18, 2), (120, 42, 2), (210, 14, 3), (300, 36, 2),
                      (390, 20, 2), (470, 48, 3), (560, 16, 2), (640, 40, 2),
                      (720, 22, 3), (800, 44, 2), (880, 18, 2), (950, 38, 3),
                      (160, 70, 2), (520, 66, 2), (760, 70, 2)]:
        draw.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                     fill=(255, 255, 255))
    # skyline silhouettes with lit windows (kept low so the trails show)
    base = y + h
    buildings = [(0, 90, 120), (120, 70, 110), (230, 84, 130),
                 (360, 64, 120), (480, 88, 110), (590, 66, 130),
                 (720, 90, 110), (830, 62, 120), (950, 86, 120)]
    for bx, bh, bw in buildings:
        draw.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(6, 10, 28))
        for wx in range(bx + 14, bx + bw - 10, 26):
            for wy in range(base - bh + 16, base - 14, 30):
                if (wx * 7 + wy * 3) % 5 < 2:
                    draw.rectangle([x + wx, wy, x + wx + 8, wy + 10],
                                   fill=(255, 214, 120))
    # tall tower (PIF Tower silhouette) with a red beacon, kept inside the sky
    draw.rectangle([x + 430, base - 140, x + 470, base], fill=(6, 10, 28))
    draw.ellipse([x + 446, base - 148, x + 454, base - 140], fill=(255, 60, 60))
    # rising interceptor trails, drawn over the skyline so they read clearly
    for tx, top in [(180, 30), (520, 18), (830, 34)]:
        pts = [(x + tx, y + h - 8), (x + tx - 14, y + h - 60),
               (x + tx - 20, y + top + 26)]
        draw.line(pts, fill=(255, 214, 110), width=7)
        draw.ellipse([x + tx - 34, y + top - 6, x + tx - 6, y + top + 22],
                     fill=(255, 176, 66))
        draw.ellipse([x + tx - 26, y + top + 2, x + tx - 14, y + top + 14],
                     fill=(255, 240, 190))
    # distant burst, above the rooftops
    draw.ellipse([x + 330, y + 40, x + 380, y + 90], fill=(255, 120, 40))
    draw.ellipse([x + 342, y + 52, x + 368, y + 78], fill=(255, 220, 130))


def draw_hero(draw):
    x, y, w, h = 24, 132, W - 48, 372
    card(draw, x, y, w, h)
    draw_hero_sky(draw, x + 2, y + 2, w - 4, 150)
    ty = y + 162
    ty = kicker(draw, x + 24, ty, "LEAD STORY  \u2022  RIYADH, SAUDI ARABIA", RED, 21)
    head = wrap(draw, "Saudi interceptors down three missiles aimed at Riyadh",
                serif_bold(42), w - 48)
    ty = text_block(draw, x + 24, ty, head, serif_bold(42), INK, leading=47)
    body = ("The Saudi-led coalition said it destroyed three Houthi ballistic "
            "missiles fired towards the capital early on Saturday, the third "
            "straight night of air-raid alerts in Riyadh.")
    ty = text_block(draw, x + 24, ty + 6,
                    wrap(draw, body, sans(22), w - 48), sans(22), (52, 52, 52),
                    leading=27)
    return y + h


# --- middle row: COP31 and markets -----------------------------------------
def draw_cop31_scene(draw, x, y, w, h):
    """Globe over a warm horizon: climate talks in Antalya."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 74, 96))
    draw.ellipse([x + w // 2 - 36, y + 8, x + w // 2 + 36, y + 80],
                 fill=(52, 148, 96))
    draw.ellipse([x + w // 2 - 36, y + 8, x + w // 2 + 36, y + 80],
                 outline=(220, 240, 220), width=3)
    for gx, gy in [(x + w // 2 - 20, y + 32), (x + w // 2 + 12, y + 56),
                   (x + w // 2 - 4, y + 66)]:
        draw.ellipse([gx - 7, gy - 4, gx + 8, gy + 5], fill=(34, 110, 70))
    draw.arc([x + w // 2 - 36, y + 34, x + w // 2 + 36, y + 62],
             start=200, end=340, fill=(220, 240, 220), width=3)
    draw.rectangle([x, y + h - 12, x + w, y + h], fill=(232, 178, 58))


def draw_market_scene(draw, x, y, w, h):
    """Falling red chart on a dark board."""
    draw.rectangle([x, y, x + w, y + h], fill=(28, 28, 34))
    for gy in range(y + 24, y + h - 10, 26):
        draw.line([(x + 10, gy), (x + w - 10, gy)], fill=(58, 58, 66), width=1)
    pts = [(x + 14, y + 26), (x + 90, y + 44), (x + 170, y + 38),
           (x + 250, y + 66), (x + 330, y + 62), (x + 410, y + 96),
           (x + w - 14, y + 118)]
    draw.line(pts, fill=(232, 64, 64), width=6)
    draw.ellipse([x + w - 26, y + 106, x + w - 2, y + 130], fill=(232, 64, 64))
    label = "-5.3%"
    tw = draw.textlength(label, font=sans_bold(28))
    draw.text((x + w - 16 - tw, y + 8), label, font=sans_bold(28),
              fill=(255, 120, 120))


def draw_middle(draw, top):
    y = top + 14
    h = 236
    w = (W - 48 - 16) // 2
    # COP31, left
    x = 24
    card(draw, x, y, w, h, accent=GREEN)
    draw_cop31_scene(draw, x + 2, y + 2, w - 4, 96)
    ty = kicker(draw, x + 20, y + 106, "CLIMATE  \u2022  ANTALYA", GREEN, 20)
    head = wrap(draw, "COP31 talks extended as fossil-fuel row drags on",
                serif_bold(28), w - 40)
    ty = text_block(draw, x + 20, ty, head, serif_bold(28), INK, leading=32)
    body = "Nearly 200 nations stay deadlocked."
    text_block(draw, x + 20, ty + 4,
               wrap(draw, body, sans(21), w - 40), sans(21), (52, 52, 52),
               leading=26)
    # Markets, right
    x = 24 + w + 16
    card(draw, x, y, w, h, accent=RED)
    draw_market_scene(draw, x + 2, y + 2, w - 4, 96)
    ty = kicker(draw, x + 20, y + 106, "MARKETS  \u2022  NEW YORK", RED, 20)
    head = wrap(draw, "AI sell-off deepens: Nasdaq dives 5.3%",
                serif_bold(28), w - 40)
    ty = text_block(draw, x + 20, ty, head, serif_bold(28), INK, leading=32)
    body = "S&P 500 falls 3.7%; Nikkei drops 5.1%."
    text_block(draw, x + 20, ty + 4,
               wrap(draw, body, sans(21), w - 40), sans(21), (52, 52, 52),
               leading=26)
    return y + h


# --- bottom row: Bayer, Basra, FBI -----------------------------------------
def draw_gavel(draw, x, y, s):
    """Simple gavel icon in a square."""
    draw.rectangle([x, y, x + s, y + s], fill=(238, 232, 214))
    draw.rectangle([x + s // 2 - 5, y + s - 34, x + s // 2 + 5, y + s - 8],
                   fill=(120, 84, 40))
    draw.rectangle([x + 14, y + 16, x + s - 14, y + 34], fill=(120, 84, 40))
    draw.rectangle([x + 20, y + 40, x + s - 20, y + 48], fill=(90, 60, 28))


def draw_flame(draw, x, y, s):
    """Simple flame icon in a square."""
    draw.rectangle([x, y, x + s, y + s], fill=(30, 22, 22))
    cx, cy = x + s // 2, y + s // 2 + 12
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 22], fill=(255, 140, 40))
    draw.ellipse([cx - 15, cy - 8, cx + 15, cy + 22], fill=(255, 214, 90))
    draw.ellipse([cx - 7, cy + 4, cx + 7, cy + 22], fill=(255, 240, 190))


def draw_screen(draw, x, y, s):
    """Simple monitor with a warning triangle."""
    draw.rectangle([x, y, x + s, y + s], fill=(16, 40, 64))
    draw.rectangle([x + 12, y + 12, x + s - 12, y + s - 26],
                   outline=(160, 200, 240), width=3)
    cx, cy = x + s // 2, y + s // 2 - 2
    draw.polygon([(cx, cy - 18), (cx - 18, cy + 12), (cx + 18, cy + 12)],
                 fill=(255, 196, 66))
    draw.text((cx - 3, cy - 8), "!", font=sans_bold(22), fill=(16, 40, 64))
    draw.rectangle([cx - 16, y + s - 14, cx + 16, y + s - 10],
                   fill=(160, 200, 240))


def draw_bottom(draw, top):
    y = top + 14
    h = 208
    w = (W - 48 - 32) // 3
    stories = [
        ("BUSINESS  \u2022  UNITED STATES", BLUE,
         "Bayer's $7.25bn deal approved",
         "A Missouri judge approves the settlement.",
         draw_gavel),
        ("DISASTER  \u2022  BASRA, IRAQ", AMBER,
         "Power-plant fire kills at least four",
         "Hartha blaze injures 30; 800 MW plant halts.",
         draw_flame),
        ("TECH  \u2022  UNITED STATES", TEAL,
         "FBI crime database reportedly hacked",
         "NCIC under investigation; USDA also hit.",
         draw_screen),
    ]
    for i, (kick, color, head, body, icon) in enumerate(stories):
        x = 24 + i * (w + 16)
        card(draw, x, y, w, h, accent=color)
        icon(draw, x + 18, y + 14, 56)
        ty = kicker(draw, x + 18, y + 80, kick, color, 16)
        ty = text_block(draw, x + 18, ty,
                        wrap(draw, head, serif_bold(22), w - 36),
                        serif_bold(22), INK, leading=25)
        text_block(draw, x + 18, ty + 5,
                   wrap(draw, body, sans(18), w - 36), sans(18), (52, 52, 52),
                   leading=22)
    return y + h


# --- footer and main ---------------------------------------------------------
def draw_footer(draw):
    y = H - 34
    draw.text((28, y), "Sources: Reuters, BBC, AFP, Al Jazeera  \u2022  21 November 2026",
              font=sans(19), fill=GREY)
    right = "make.fun  \u2022  news-image-20261121"
    tw = draw.textlength(right, font=sans(19))
    draw.text((W - 28 - tw, y), right, font=sans(19), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    hero_bottom = draw_hero(draw)
    mid_bottom = draw_middle(draw, hero_bottom)
    draw_bottom(draw, mid_bottom)
    draw_footer(draw)
    img.save(OUT, format="PNG", optimize=True)
    print("Wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
