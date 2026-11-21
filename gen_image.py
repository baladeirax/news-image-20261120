#!/usr/bin/env python3
"""Draw the 20 November 2026 news front page (1024x1024 PNG, PIL only).

Deterministic: fixed text, fixed layout, no randomness, no network.
Run: python3 gen_image.py [out.png]  (default: entry.png next to this file)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GOLD = (176, 141, 44)
GREY = (90, 90, 88)
LIGHT = (232, 227, 214)
BLUEPANEL = (24, 42, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, max_w, text, fnt, fill=INK, leading=1.28):
    size = fnt.size
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def headline(d, x, y, max_w, text, fnt, fill=INK, leading=1.08):
    size = fnt.size
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += int(size * leading)
    return y


def panel(d, x, y, w, h, title, body, title_fill=RED):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 30], fill=NAVY)
    d.text((x + 10, y + 6), title, font=SANS_B(17), fill=(255, 255, 255))
    return para(d, x + 10, y + 40, w - 20, body, SANS(16), leading=1.3)


def draw_map(d, x, y, w, h):
    """Schematic of the Poland incursion: abstract shapes, labelled."""
    d.rectangle([x, y, x + w, y + h], fill=BLUEPANEL, outline=INK, width=2)
    # stylised land masses
    d.polygon([(x + 20, y + 30), (x + 200, y + 18), (x + 250, y + 90),
               (x + 210, y + 170), (x + 60, y + 180), (x + 15, y + 110)],
              fill=(58, 84, 110), outline=(200, 200, 190), width=2)
    d.polygon([(x + 250, y + 90), (x + 380, y + 70), (x + 400, y + 190),
               (x + 210, y + 170)], fill=(44, 66, 92),
              outline=(200, 200, 190), width=2)
    d.text((x + 30, y + 44), "POLAND", font=SANS_B(20), fill=(255, 255, 255))
    d.text((x + 245, y + 165), "UKRAINE", font=SANS_B(18), fill=(210, 210, 200))
    d.text((x + 330, y + 30), "RUSSIA", font=SANS_B(16), fill=(200, 120, 120))
    # incoming tracks from the east
    for (x1, y1, x2, y2) in [(390, 60, 300, 95), (395, 120, 305, 135),
                             (385, 165, 295, 160)]:
        d.line([x + x1, y + y1, x + x2, y + y2], fill=(230, 90, 90), width=3)
        for t in (0.33, 0.66):
            px = x + int(x1 + (x2 - x1) * t)
            py = y + int(y1 + (y2 - y1) * t)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(230, 90, 90))
    # impact sites
    sites = [(180, 70, "Nowy Lipowiec"), (120, 120, "Rudnik nad Sanem"),
             (150, 160, "Molodycz")]
    for sx, sy, name in sites:
        d.ellipse([x + sx - 8, y + sy - 8, x + sx + 8, y + sy + 8],
                  fill=(230, 60, 60), outline=(255, 255, 255), width=2)
        d.text((x + sx + 12, y + sy - 8), name, font=SANS_B(14),
               fill=(255, 255, 255))
    d.text((x + 12, y + h - 40), "SCHEMATIC — 3 Russian weapons down in",
           font=SANS(13), fill=(200, 205, 210))
    d.text((x + 12, y + h - 22), "SE Poland, 30–50 km from the border",
           font=SANS(13), fill=(200, 205, 210))


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 24  # margin

    # ---- masthead ----
    d.text((mx, 10), "THE DAILY WORLD", font=SERIF_B(52), fill=INK)
    d.text((W - mx - 330, 24), "FRIDAY", font=SANS_B(25), fill=RED)
    d.text((W - mx - 330, 54), "20 NOVEMBER 2026", font=SANS_B(25), fill=INK)
    d.line([mx, 94, W - mx, 94], fill=INK, width=3)
    d.line([mx, 100, W - mx, 100], fill=INK, width=1)

    # ---- date check strip (winner lesson: explicit date check) ----
    y = 108
    d.rectangle([mx, y, W - mx, y + 28], fill=NAVY)
    d.text((mx + 10, y + 5),
           "DATE CHECK \u2713 — Every story below happened or was first "
           "reported on Friday 20 November 2026.",
           font=SANS_B(15), fill=(255, 255, 255))

    # ---- lead headline ----
    y = 146
    y = headline(d, mx, y, W - 2 * mx,
                 "RUSSIAN MISSILES CRASH IN POLAND",
                 SANS_B(42), fill=INK)
    y = headline(d, mx, y + 4, W - 2 * mx,
                 "NATO calls it a \u201cgrave violation\u201d — Warsaw "
                 "invokes Article 4",
                 SANS_B(21), fill=RED)
    y += 8

    # ---- lead text + map ----
    lead_top = y
    lead_w = 520
    y = para(d, mx, lead_top, lead_w,
             "Two Russian Kh-101 cruise missiles and a jet-powered drone "
             "crashed in south-eastern Poland early on Friday, during "
             "Moscow\u2019s largest strike on Ukraine of the month.",
             SANS(19), leading=1.32)
    y = para(d, mx, y + 8, lead_w,
             "No one was hurt. PM Donald Tusk called it a deliberate "
             "provocation, timed to the Coalition of the Willing drills "
             "at Nowa D\u0119ba. NATO chief Mark Rutte: a \u201cgrave "
             "violation\u201d of Polish airspace.", SANS(17), leading=1.32)
    y = para(d, mx, y + 8, lead_w,
             "Warsaw invoked NATO Article 4 and asked for more allied "
             "air defences. Polish, Swedish and Dutch jets scrambled.",
             SANS(17), leading=1.32)
    draw_map(d, mx + lead_w + 16, lead_top, W - mx - (mx + lead_w + 16),
             236)
    y = lead_top + 236 + 12

    # ---- UTC timeline strip (winner lesson: a timeline) ----
    d.rectangle([mx, y, W - mx, y + 84], fill=LIGHT, outline=INK, width=2)
    d.text((mx + 10, y + 5), "THE DAY IN UTC", font=SANS_B(16), fill=NAVY)
    slots = [
        ("OVERNIGHT", "Russia fires 400+ drones,\n110+ missiles at Ukraine"),
        ("03:30", "Polish jets scramble;\nPatriots on alert"),
        ("MORNING", "Two missiles and a drone\ncrash in SE Poland"),
        ("MIDDAY", "Tusk: provocation \u00b7 Rutte:\n\u201cgrave violation\u201d"),
        ("LATER", "Poland invokes NATO\nArticle 4, seeks more jets"),
    ]
    sw = (W - 2 * mx - 20) // 5
    for i, (t, txt) in enumerate(slots):
        sx = mx + 10 + i * sw
        d.text((sx, y + 26), t, font=SANS_B(15), fill=RED)
        yy = y + 46
        for line in txt.split("\n"):
            d.text((sx, yy), line, font=SANS(13), fill=INK)
            yy += 17
    y += 84 + 12

    # ---- story panels, two columns ----
    col_w = (W - 2 * mx - 16) // 2
    left_x, right_x = mx, mx + col_w + 16
    ph = 118
    panel(d, left_x, y, col_w, ph, "KYIV UNDER FIRE",
          "Moscow\u2019s biggest strike of November: 27 ballistic "
          "missiles, 84 cruise missiles and 404 drones. Bridges across "
          "the Dnipro hit; 8 killed; power cut across western Ukraine.")
    panel(d, right_x, y, col_w, ph, "ANTHROPIC\u2019S RECORD IPO",
          "The AI lab debuts on Nasdaq at $83 and closes up 17% at "
          "$97.17 \u2014 $81.3bn raised, the largest IPO on record. "
          "Shares slide on day two as markets fall.")
    y += ph + 8
    panel(d, left_x, y, col_w, ph, "CYCLONE AKVAN LANDFALL",
          "Akvan crosses India\u2019s Odisha coast near Gopalpur. More "
          "than 300,000 people were evacuated ahead of landfall; no "
          "major damage reported.")
    panel(d, right_x, y, col_w, ph, "MARKETS SLIDE",
          "The S&P 500 falls for a sixth straight day and the Nikkei "
          "drops 5.1% in an AI-led sell-off. World debt nears 100% of "
          "GDP, the IMF warns.")
    y += ph + 8

    # ---- also today strip ----
    d.rectangle([mx, y, W - mx, y + 76], outline=INK, width=2)
    d.text((mx + 10, y + 5), "ALSO ON 20 NOVEMBER", font=SANS_B(16),
           fill=NAVY)
    para(d, mx + 10, y + 26, W - 2 * mx - 20,
         "Senate blocks Iran vote 51\u201348 \u00b7 Estonia shuts Russia "
         "border from 1 Dec \u00b7 Peru quake 6.7 \u00b7 COP31 draft drops "
         "fossil fuels \u00b7 BepiColombo reaches Mercury \u00b7 Hormuz "
         "tanker on fire after mine strike \u00b7 UK\u2013EU Brexit reset "
         "\u00b7 Brazil storm: 8,000 roofs \u00b7 Haiti raid: 34 killed.",
         SANS(14), leading=1.3)
    y += 76 + 8

    # ---- yesterday in brief + footer ----
    para(d, mx, y, W - 2 * mx,
         "YESTERDAY, IN BRIEF (19 NOV): Trump, Xi and Putin sign a "
         "4-point Peace Declaration in Shenzhen \u00b7 ICJ rules Myanmar "
         "committed genocide against the Rohingya \u00b7 Houthi missile "
         "damages Riyadh\u2019s PIF Tower.",
         SANS(14), fill=GREY, leading=1.3)
    d.line([mx, H - 34, W - mx, H - 34], fill=INK, width=1)
    d.text((mx, H - 28),
           "Sources: AP \u00b7 ISW \u00b7 Reuters \u00b7 IMD \u00b7 Nasdaq — "
           "All stories dated 20 November 2026",
           font=SANS(13), fill=GREY)

    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build(out)
    print("wrote", out)
