#!/usr/bin/env python3
"""Build the front page image for Thursday 19 November 2026 world news.

Draws a 1024x1024 front page with PIL only: masthead, red ticker, a 3x6
grid of 18 illustrated story cards, a numbered world map, a numbered list
of stories 19-48, and a by-the-numbers sidebar. All artwork is procedural
flat-vector shapes; no external images, no network, deterministic output.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (16, 36, 62)
NAVY2 = (24, 52, 88)
RED = (178, 34, 34)
RED2 = (200, 48, 48)
PAPER = (246, 241, 231)
CARD = (255, 255, 255)
INK = (24, 24, 24)
GREY = (90, 90, 90)
LINE = (216, 210, 196)
OCEAN = (198, 216, 228)
LAND = (232, 221, 194)
LANDLINE = (178, 164, 122)
GOLD = (201, 162, 39)
GREEN = (46, 125, 72)
TEAL = (32, 120, 120)

_cache = {}


def font(size, bold=False):
    key = (size, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(FONTB if bold else FONT, size)
    return _cache[key]


def text_w(s, f):
    return f.getlength(s)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, s, f, max_w, fill, max_lines=2, lh=None):
    lines = wrap(draw, s, f, max_w)[:max_lines]
    if lh is None:
        lh = f.size + 2
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


# ---------------------------------------------------------------- stories
# Each grid story: (headline, deck, illustration kind, lat, lon)
GRID = [
    ("ICJ: Myanmar guilty of genocide",
     "World court: first genocide ruling against a state",
     "court", 52.07, 4.30),
    ("Trump, Xi, Putin meet in Shenzhen",
     "First trilateral summit ends in joint peace declaration",
     "flags", 22.54, 114.06),
    ("Kerch Bridge hit a third time",
     "Rail span struck; road arch already down, trains halted",
     "bridge", 45.31, 36.51),
    ("Tanker attacks in Hormuz Strait",
     "ADNOC ship hit: 11 hurt, 1 missing; mines reported",
     "tanker", 26.60, 56.20),
    ("Anthropic debuts on Nasdaq",
     "Priced at $83 a share; valued near $1.5 trillion",
     "chart", 40.71, -74.00),
    ("Wall Street slides again",
     "S&P 500 down 2.02%; Nikkei off 4.68%; gold sinks",
     "down", 35.68, 139.69),
    ("Haiti police kill 34 in raid",
     "Martissant operation targets gangs; no police hurt",
     "shield", 18.54, -72.34),
    ("Denmark backs Greenland deal",
     "Parliament votes 109-0 for US security agreement",
     "snow", 55.68, 12.57),
    ("Migrant boat sinks off Senegal",
     "Survivors say about 100 aboard; dozens missing",
     "boat", 14.69, -17.45),
    ("Israel ends Gaza tank raid",
     "First ground push past Yellow Line since the truce",
     "tank", 31.50, 34.47),
    ("COP31 draft drops fossil fuels",
     "Draft drops all fossil-fuel language; talks stall",
     "leaf", 36.90, 30.71),
    ("Van Gogh sells for $190.4m",
     "Record for the artist at Sotheby's in New York",
     "paint", 49.07, 2.17),
    ("Bangladesh burns in protests",
     "Yunus home torched; unrest reported in 28 districts",
     "flame", 23.81, 90.41),
    ("North Korea expands enrichment",
     "IAEA: new Yongbyon extension finished in October",
     "atom", 39.80, 125.30),
    ("Jeffries nominated for speaker",
     "Democrats back him 251-11; first Black speaker",
     "dome", 38.90, -77.04),
    ("Binance wins $6.5bn freeze order",
     "Abu Dhabi court acts after record October hack",
     "coin", 24.45, 54.38),
    ("US signs Venezuela military pact",
     "Hegseth visits Caracas; training, intelligence shared",
     "shake", 10.48, -66.88),
    ("EU-Mexico farm tariffs fall",
     "Pact cuts 95% of duties on farm goods",
     "wheat", 19.43, -99.13),
]

# List stories 19-48, one line each.
LIST = [
    "Japan to hold first live-fire drills in India",
    "EU confirms AI-driven cyberattack on its systems",
    "UK tribunal confirms secret Apple data order",
    "Nearly 1 in 4 children live in conflict zones",
    "Nvidia halts Hopper chip shipments to China",
    "Pakistan says 22 militants killed in raids",
    "Iraq: Kataib Hezbollah given days to leave town",
    "Sanchez admits mistakes in Spanish TV debate",
    "Drone, artillery fire reported near Badme",
    "Yemen: 356,000 displaced; UN says let aid in",
    "Philippines, Chile sign first free trade deal",
    "Earth found to have four radiation belts",
    "US test-fires unarmed Minuteman III missile",
    "House: 879,000 AI chips cleared for China",
    "US panel: do not certify Chinese aircraft",
    "Houthi strike damages Riyadh's PIF Tower",
    "Kuwait repels first Iranian attack in months",
    "EU proposes 45bn euro loan to Ukraine",
    "Ukraine allies meet in Berlin show of support",
    "Russian strikes kill at least 5 in Ukraine",
    "Drone attack on Kursk injures at least 11",
    "Aid groups grade Gaza peace plan 4 of 26",
    "Takaichi holds first talks with Putin in 7 years",
    "Brent crude $89.72, up 0.31%",
    "France: 15,000 detained in weeks of protests",
    "Gold falls 2.42% to 14-month low",
    "S&P 500 closes at 7,176",
    "FTSE 100 down 0.93% to six-week low",
    "US Senate blocks measure to end Iran war",
    "Kushner: Russia 'comfortable' with guarantees",
]

TICKER = ("THURSDAY, 19 NOVEMBER 2026  |  ICJ: MYANMAR GUILTY  |  "
          "TRUMP, XI, PUTIN IN SHENZHEN  |  ANTHROPIC IPO $83  |  "
          "S&P 500 DOWN 2.02%")

STATS = [
    ("48", "stories from six continents"),
    ("$190.4m", "record price for a Van Gogh"),
    ("879,000", "AI chips cleared for China"),
    ("589m", "children living in conflict zones"),
    ("$83", "Anthropic IPO price per share"),
    ("109-0", "Denmark's Greenland deal vote"),
]

SOURCES = ("Sources: Reuters, AP, UN News, IAEA, Sotheby's. "
           "All stories reported on 19 Nov 2026.")

# Small nudges (px) for pins that would otherwise overlap.
PIN_OFF = {3: (8, -7), 4: (10, -4), 5: (7, -7), 6: (6, 4), 7: (-4, -11),
           8: (8, -6), 10: (9, 3), 11: (-9, -5), 12: (-16, 12),
           14: (-6, -6), 15: (-9, 6), 16: (-10, 6), 17: (12, 9)}

# Simplified continent outlines as (lon, lat) lists.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-105, 73),
     (-95, 80), (-85, 79), (-80, 73), (-70, 62), (-65, 60), (-60, 55),
     (-55, 52), (-60, 47), (-65, 44), (-70, 42), (-75, 35), (-80, 32),
     (-81, 26), (-84, 30), (-90, 21), (-94, 18), (-90, 14), (-86, 13),
     (-83, 9), (-79, 9), (-83, 12), (-90, 14), (-95, 16), (-97, 16),
     (-102, 18), (-105, 20), (-110, 23), (-114, 28), (-117, 33),
     (-122, 37), (-124, 42), (-124, 48), (-130, 55), (-140, 60),
     (-150, 61), (-160, 58), (-168, 66)],
    # Greenland
    [(-55, 60), (-48, 60), (-42, 63), (-38, 65), (-32, 68), (-25, 70),
     (-20, 73), (-22, 76), (-30, 78), (-45, 79), (-55, 77), (-60, 74),
     (-58, 70), (-55, 65), (-55, 60)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-71, -50),
     (-68, -55), (-65, -50), (-62, -41), (-57, -38), (-52, -33),
     (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6),
     (-40, -3), (-44, -2), (-50, 0), (-52, 5), (-55, 6), (-60, 8),
     (-65, 10), (-70, 11), (-75, 11), (-79, 9)],
    # Africa
    [(-17, 15), (-16, 20), (-12, 25), (-10, 31), (-6, 35), (-1, 35),
     (5, 37), (10, 37), (11, 34), (15, 32), (20, 32), (25, 32),
     (30, 31), (32, 31), (34, 28), (35, 24), (37, 20), (39, 15),
     (41, 12), (44, 11), (48, 11), (51, 11), (50, 8), (46, 5),
     (42, 0), (40, -5), (40, -10), (37, -15), (35, -20), (33, -26),
     (30, -30), (27, -33), (22, -35), (19, -34), (17, -29), (15, -25),
     (13, -20), (12, -15), (12, -10), (12, -5), (9, 4), (5, 5),
     (0, 6), (-5, 5), (-8, 5), (-12, 8), (-15, 10), (-17, 12),
     (-17, 15)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-4, 44), (-2, 44), (-2, 47),
     (-4, 48), (-2, 49), (0, 50), (1, 51), (3, 53), (5, 53),
     (8, 54), (8, 57), (5, 58), (6, 59), (5, 60), (8, 61),
     (11, 62), (14, 63), (18, 64), (21, 65), (24, 66), (28, 68),
     (30, 70), (35, 68), (40, 68), (45, 68), (50, 69), (55, 68),
     (60, 69), (65, 68), (60, 66), (55, 64), (50, 62), (45, 60),
     (40, 58), (35, 56), (30, 55), (28, 55), (24, 57), (21, 55),
     (18, 55), (15, 54), (12, 54), (9, 53), (6, 52), (3, 51),
     (1, 49), (0, 46), (-1, 44), (-3, 43), (-6, 43), (-9, 43),
     (-9, 39), (-6, 36), (-3, 36), (0, 38), (2, 39), (3, 42),
     (7, 44), (10, 44), (12, 44), (15, 44), (18, 40), (20, 40),
     (23, 36), (26, 38), (23, 39), (20, 41), (18, 42), (15, 44),
     (12, 45), (9, 44), (6, 43), (3, 43), (0, 40), (-2, 37),
     (-6, 36), (-10, 36)],
    # Asia
    [(-10, 36), (30, 36), (33, 36), (36, 36), (36, 33), (35, 30),
     (36, 28), (39, 21), (41, 18), (43, 16), (45, 13), (48, 14),
     (52, 15), (55, 17), (58, 20), (58, 23), (56, 26), (52, 27),
     (50, 29), (48, 30), (50, 29), (54, 27), (57, 26), (59, 25),
     (61, 25), (65, 25), (67, 25), (70, 23), (72, 20), (75, 18),
     (77, 8), (80, 10), (80, 13), (84, 18), (87, 21), (89, 22),
     (91, 22), (93, 18), (95, 16), (98, 10), (100, 7), (103, 8),
     (105, 9), (107, 11), (109, 13), (109, 17), (108, 18), (106, 20),
     (108, 21), (111, 22), (114, 22), (117, 23), (120, 25), (121, 28),
     (122, 31), (120, 34), (122, 37), (124, 39), (127, 40), (129, 42),
     (132, 43), (135, 44), (138, 46), (141, 50), (142, 52), (140, 54),
     (142, 56), (146, 59), (150, 60), (155, 60), (158, 56), (160, 60),
     (162, 62), (162, 66), (158, 68), (155, 69), (150, 70), (145, 72),
     (140, 73), (135, 74), (130, 73), (125, 75), (120, 76), (115, 76),
     (110, 76), (105, 77), (100, 77), (95, 76), (90, 75), (85, 76),
     (80, 74), (75, 73), (70, 73), (65, 69), (60, 69), (55, 68),
     (50, 69), (45, 68), (40, 68), (35, 68), (30, 70), (28, 68),
     (24, 66), (21, 65), (18, 64), (14, 63), (11, 62), (8, 61),
     (5, 60), (5, 58), (8, 57), (8, 54), (5, 53), (3, 53),
     (1, 51), (0, 50), (-2, 49), (-4, 48), (-2, 47), (-2, 44),
     (-4, 44), (-9, 43), (-9, 38), (-10, 36)],
    # Australia
    [(113, -22), (114, -28), (114, -32), (115, -35), (118, -35),
     (122, -34), (126, -32), (129, -32), (132, -32), (135, -35),
     (137, -35), (140, -38), (144, -39), (147, -39), (150, -37),
     (153, -32), (153, -27), (151, -24), (149, -20), (146, -19),
     (143, -15), (142, -11), (141, -13), (140, -17), (137, -15),
     (135, -12), (132, -12), (130, -13), (127, -14), (124, -15),
     (121, -17), (118, -20), (115, -21), (113, -22)],
]


def project(lon, lat, x0, y0, w, h, lat_min=-58.0, lat_max=84.0):
    x = x0 + (lon + 180.0) / 360.0 * w
    y = y0 + (lat_max - lat) / (lat_max - lat_min) * h
    return x, y


# ---------------------------------------------------------------- icons
def icon(draw, kind, x, y, s, bg):
    """Draw one flat-vector illustration inside the s x s box at (x, y)."""
    draw.rectangle([x, y, x + s, y + s], fill=bg)
    c = NAVY
    if kind == "court":
        # courthouse: steps, columns, pediment
        draw.polygon([(x + 8, y + 22), (x + s - 8, y + 22), (x + s - 14, y + 12),
                      (x + 14, y + 12)], fill=c)
        for i in range(4):
            cx = x + 16 + i * 14
            draw.rectangle([cx, y + 24, cx + 6, y + 50], fill=c)
        draw.rectangle([x + 10, y + 52, x + s - 10, y + 56], fill=c)
        draw.rectangle([x + 6, y + 58, x + s - 6, y + 62], fill=c)
        draw.rectangle([x + 28, y + 34, x + s - 28, y + 50], fill=(255, 255, 255))
        draw.rectangle([x + 32, y + 38, x + s - 32, y + 50], fill=GOLD)
    elif kind == "flags":
        # three flagpoles with waving flags
        cols = [RED2, GOLD, TEAL]
        for i, col in enumerate(cols):
            px = x + 14 + i * 20
            draw.line([px, y + 14, px, y + 62], fill=c, width=3)
            draw.polygon([(px, y + 12), (px + 16, y + 18), (px, y + 24)],
                         fill=col)
        draw.rectangle([x + 8, y + 62, x + s - 8, y + 66], fill=c)
    elif kind == "bridge":
        # suspension bridge over water, one span down
        draw.rectangle([x, y + 52, x + s, y + 72], fill=(120, 170, 205))
        draw.line([x + 6, y + 52, x + s - 6, y + 52], fill=c, width=3)
        draw.rectangle([x + 8, y + 18, x + 12, y + 52], fill=c)
        draw.rectangle([x + s - 12, y + 18, x + s - 8, y + 52], fill=c)
        draw.line([x + 10, y + 20, x + s // 2, y + 44], fill=c, width=2)
        draw.line([x + s - 10, y + 20, x + s // 2 + 8, y + 44], fill=c, width=2)
        draw.polygon([(x + s // 2 - 2, y + 44), (x + s // 2 + 14, y + 44),
                      (x + s // 2 + 10, y + 56), (x + s // 2 - 6, y + 56)],
                     fill=RED2)
    elif kind == "tanker":
        draw.rectangle([x, y + 50, x + s, y + 72], fill=(120, 170, 205))
        draw.polygon([(x + 8, y + 34), (x + s - 8, y + 34), (x + s - 14, y + 50),
                      (x + 14, y + 50)], fill=c)
        draw.rectangle([x + 14, y + 22, x + 26, y + 34], fill=c)
        draw.rectangle([x + 46, y + 16, x + 52, y + 34], fill=RED2)
        draw.rectangle([x + 18, y + 38, x + s - 18, y + 42], fill=GOLD)
    elif kind == "chart":
        draw.rectangle([x + 8, y + 56, x + s - 8, y + 60], fill=c)
        draw.line([x + 8, y + 56, x + 8, y + 12], fill=c, width=3)
        pts = [(x + 10, y + 46), (x + 24, y + 38), (x + 36, y + 42),
               (x + 50, y + 26), (x + 62, y + 16)]
        draw.line(pts, fill=GREEN, width=4)
        draw.polygon([(x + 62, y + 16), (x + 54, y + 14), (x + 60, y + 24)],
                     fill=GREEN)
    elif kind == "down":
        draw.rectangle([x + 8, y + 56, x + s - 8, y + 60], fill=c)
        draw.line([x + 8, y + 56, x + 8, y + 12], fill=c, width=3)
        pts = [(x + 10, y + 18), (x + 24, y + 28), (x + 36, y + 26),
               (x + 50, y + 42), (x + 62, y + 52)]
        draw.line(pts, fill=RED2, width=4)
        draw.polygon([(x + 62, y + 52), (x + 54, y + 54), (x + 60, y + 44)],
                     fill=RED2)
    elif kind == "shield":
        draw.polygon([(x + s // 2, y + 8), (x + s - 10, y + 16),
                      (x + s - 10, y + 38), (x + s // 2, y + 64),
                      (x + 10, y + 38), (x + 10, y + 16)], fill=c)
        draw.polygon([(x + s // 2, y + 14), (x + s - 16, y + 20),
                      (x + s - 16, y + 36), (x + s // 2, y + 56),
                      (x + 16, y + 36), (x + 16, y + 20)], fill=GOLD)
        draw.text((x + s // 2 - 4, y + 26), "!", font=font(20, True),
                  fill=NAVY)
    elif kind == "snow":
        # iceberg + flag
        draw.polygon([(x + 8, y + 56), (x + 26, y + 20), (x + 40, y + 44),
                      (x + 52, y + 14), (x + s - 8, y + 56)], fill=(255, 255, 255),
                     outline=c)
        draw.line([x + 8, y + 56, x + s - 8, y + 56], fill=c, width=3)
        draw.line([x + 52, y + 14, x + 52, y + 34], fill=c, width=2)
        draw.polygon([(x + 52, y + 14), (x + 64, y + 18), (x + 52, y + 22)],
                     fill=RED2)
    elif kind == "boat":
        draw.rectangle([x, y + 48, x + s, y + 72], fill=(120, 170, 205))
        draw.polygon([(x + 10, y + 40), (x + s - 10, y + 40),
                      (x + s - 18, y + 54), (x + 18, y + 54)], fill=c)
        draw.line([x + s // 2, y + 12, x + s // 2, y + 40], fill=c, width=3)
        draw.polygon([(x + s // 2, y + 12), (x + s // 2 + 18, y + 26),
                      (x + s // 2, y + 38)], fill=RED2)
    elif kind == "tank":
        draw.rectangle([x + 10, y + 40, x + s - 10, y + 54], fill=c)
        draw.rectangle([x + 22, y + 28, x + 44, y + 40], fill=c)
        draw.line([x + 44, y + 32, x + s - 4, y + 32], fill=c, width=4)
        for i in range(5):
            cx = x + 14 + i * 10
            draw.ellipse([cx, y + 54, cx + 8, y + 62], fill=GOLD)
    elif kind == "leaf":
        draw.ellipse([x + 12, y + 12, x + s - 12, y + 60], outline=GREEN,
                     width=4)
        draw.polygon([(x + s // 2, y + 16), (x + s - 16, y + 34),
                      (x + s // 2, y + 56), (x + 16, y + 34)], fill=GREEN)
        draw.line([x + s // 2, y + 18, x + s // 2, y + 56], fill=(255, 255, 255),
                  width=2)
    elif kind == "paint":
        # palette with brush
        draw.ellipse([x + 8, y + 16, x + s - 8, y + 62], fill=(255, 255, 255),
                     outline=c, width=3)
        for (bx, by, col) in [(22, 26, RED2), (44, 22, GOLD), (52, 40, GREEN),
                              (30, 46, TEAL)]:
            draw.ellipse([x + bx, y + by, x + bx + 10, y + by + 10], fill=col)
        draw.line([x + 46, y + 48, x + 60, y + 64], fill=c, width=4)
    elif kind == "flame":
        draw.polygon([(x + s // 2, y + 8), (x + s - 12, y + 30),
                      (x + s - 18, y + 24), (x + s - 10, y + 48),
                      (x + s // 2, y + 62), (x + 10, y + 48),
                      (x + 18, y + 24), (x + 12, y + 30)], fill=RED2)
        draw.polygon([(x + s // 2, y + 30), (x + s - 18, y + 44),
                      (x + s // 2, y + 58), (x + 18, y + 44)], fill=GOLD)
    elif kind == "atom":
        cx, cy = x + s // 2, y + s // 2
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED2)
        for a in (0, 60, 120):
            import math
            rx, ry = 26, 10
            pts = []
            for t in range(0, 361, 10):
                r = math.radians(t)
                px = cx + rx * math.cos(r) * math.cos(math.radians(a)) - \
                    ry * math.sin(r) * math.sin(math.radians(a))
                py = cy + rx * math.cos(r) * math.sin(math.radians(a)) + \
                    ry * math.sin(r) * math.cos(math.radians(a))
                pts.append((px, py))
            draw.line(pts, fill=c, width=2)
    elif kind == "dome":
        draw.pieslice([x + 18, y + 10, x + s - 18, y + 44], 180, 360, fill=c)
        draw.rectangle([x + 14, y + 42, x + s - 14, y + 50], fill=c)
        for i in range(4):
            cx = x + 18 + i * 12
            draw.rectangle([cx, y + 50, cx + 5, y + 62], fill=c)
        draw.rectangle([x + 10, y + 62, x + s - 10, y + 66], fill=c)
    elif kind == "coin":
        draw.ellipse([x + 12, y + 10, x + s - 12, y + 62], fill=GOLD,
                     outline=c, width=3)
        draw.text((x + s // 2 - 9, y + 22), "$", font=font(26, True),
                  fill=NAVY)
        draw.line([x + 14, y + 14, x + 30, y + 30], fill=(255, 255, 255),
                  width=3)
    elif kind == "shake":
        # two hands meeting
        draw.ellipse([x + 10, y + 30, x + 30, y + 50], fill=c)
        draw.ellipse([x + s - 30, y + 30, x + s - 10, y + 50], fill=TEAL)
        draw.polygon([(x + 22, y + 34), (x + s // 2, y + 24),
                      (x + s - 22, y + 34), (x + s // 2, y + 46)], fill=GOLD)
        draw.rectangle([x + 16, y + 52, x + s - 16, y + 58], fill=c)
    elif kind == "wheat":
        draw.line([x + s // 2, y + 18, x + s // 2, y + 64], fill=GREEN, width=3)
        for i in range(4):
            yy = y + 20 + i * 10
            draw.polygon([(x + s // 2, yy), (x + s // 2 - 12, yy + 5),
                          (x + s // 2, yy + 10)], fill=GOLD)
            draw.polygon([(x + s // 2, yy), (x + s // 2 + 12, yy + 5),
                          (x + s // 2, yy + 10)], fill=GOLD)
        draw.ellipse([x + s // 2 - 5, y + 12, x + s // 2 + 5, y + 22],
                     fill=GOLD)


ICON_BG = [(233, 236, 239), (250, 235, 215), (222, 235, 222), (235, 222, 222),
           (222, 228, 245), (240, 240, 220)]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 56], fill=NAVY)
    d.text((14, 8), "THE WORLD IN ONE DAY", font=font(34, True),
           fill=(255, 255, 255))
    # date block, right side
    date_txt = "THURSDAY, 19 NOVEMBER 2026"
    dw = text_w(date_txt, font(15, True))
    d.rectangle([W - 14 - dw - 16, 10, W - 14, 46], fill=RED)
    d.text((W - 14 - dw - 8, 15), date_txt, font=font(15, True),
           fill=(255, 255, 255))

    # ---- ticker
    d.rectangle([0, 56, W, 82], fill=RED)
    d.text((10, 63), TICKER, font=font(12, True), fill=(255, 255, 255))

    # ---- grid of 18 cards: 3 cols x 6 rows
    gx, gy = 10, 88
    cw = (W - 2 * gx - 2 * 6) // 3
    ch = 80
    for i, (head, deck, kind, lat, lon) in enumerate(GRID):
        row, col = divmod(i, 3)
        x0 = gx + col * (cw + 6)
        y0 = gy + row * (ch + 2)
        d.rectangle([x0, y0, x0 + cw, y0 + ch], fill=CARD, outline=LINE)
        ix, iy, s = x0 + 5, y0 + 5, ch - 10
        icon(d, kind, ix, iy, s, ICON_BG[i % len(ICON_BG)])
        # number badge
        bx, by = x0 + 2, y0 + 2
        d.ellipse([bx, by, bx + 20, by + 20], fill=NAVY)
        num = str(i + 1)
        nw = text_w(num, font(11, True))
        d.text((bx + 10 - nw / 2, by + 3), num, font=font(11, True),
               fill=(255, 255, 255))
        tx = ix + s + 8
        tw = x0 + cw - 6 - tx
        draw_wrapped(d, tx, y0 + 6, head, font(13, True), tw, INK,
                     max_lines=2, lh=16)
        draw_wrapped(d, tx, y0 + 40, deck, font(10, False), tw, GREY,
                     max_lines=2, lh=13)

    grid_bottom = gy + 6 * (ch + 2)

    # ---- map label
    my = grid_bottom + 6
    d.text((10, my), "WHERE IT HAPPENED  —  18 STORIES ON THE MAP",
           font=font(13, True), fill=NAVY)
    d.line([10, my + 20, W - 10, my + 20], fill=NAVY, width=2)

    # ---- map
    mx, mtop = 10, my + 26
    mw, mh = 640, 200
    d.rectangle([mx, mtop, mx + mw, mtop + mh], fill=OCEAN, outline=LINE)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, mtop, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LANDLINE)
    # pins
    for i, (head, deck, kind, lat, lon) in enumerate(GRID):
        n = i + 1
        px, py = project(lon, lat, mx, mtop, mw, mh)
        dx, dy = PIN_OFF.get(n, (0, 0))
        cx, cy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.line([px, py, cx, cy], fill=RED, width=1)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        num = str(n)
        nw = text_w(num, font(9, True))
        d.text((cx - nw / 2, cy - 7), num, font=font(9, True),
               fill=(255, 255, 255))

    # ---- sidebar: by the numbers
    sx = 660
    sw = W - 10 - sx
    d.rectangle([sx, mtop, sx + sw, mtop + mh], fill=CARD, outline=LINE)
    d.text((sx + 10, mtop + 8), "BY THE NUMBERS", font=font(13, True),
           fill=NAVY)
    d.line([sx + 10, mtop + 28, sx + sw - 10, mtop + 28], fill=NAVY, width=2)
    sy = mtop + 34
    for big, label in STATS:
        d.text((sx + 10, sy), big, font=font(16, True), fill=RED)
        bw = text_w(big, font(16, True))
        d.text((sx + 18 + bw, sy + 3), label, font=font(10, False),
               fill=INK)
        sy += 22
    draw_wrapped(d, sx + 10, sy + 2, SOURCES, font(8, False), sw - 20,
                 GREY, max_lines=2, lh=11)

    map_bottom = mtop + mh

    # ---- list of stories 19-48
    ly = map_bottom + 8
    d.rectangle([0, ly, W, ly + 22], fill=NAVY)
    d.text((10, ly + 3), "THE REST OF THE DAY  —  STORIES 19–48",
           font=font(13, True), fill=(255, 255, 255))
    d.text((W - 10 - text_w("48 STORIES · 6 CONTINENTS", font(11, True)),
            ly + 5), "48 STORIES · 6 CONTINENTS", font=font(11, True),
           fill=(220, 220, 220))

    col_w = (W - 2 * 10 - 2 * 8) // 3
    row_h = 16
    ly0 = ly + 26
    for i, item in enumerate(LIST):
        col, row = divmod(i, 10)
        x0 = 10 + col * (col_w + 8)
        y0 = ly0 + row * row_h
        n = str(19 + i) + "."
        nf = font(10, True)
        d.text((x0, y0), n, font=nf, fill=RED)
        nw = text_w(n, nf)
        f = font(10, False)
        # shrink if needed, but never below 9
        while text_w(item, f) > col_w - nw - 4 and f.size > 9:
            f = font(f.size - 1, False)
        d.text((x0 + nw + 3, y0), item, font=f, fill=INK)

    # ---- footer
    foot = "ALL 48 STORIES REPORTED ON THURSDAY 19 NOVEMBER 2026"
    fw = text_w(foot, font(9, True))
    d.text(((W - fw) / 2, H - 18), foot, font=font(9, True), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    return OUT


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print(path, size, "bytes")
    if size > 1048576:
        print("ERROR: over 1 MiB", file=sys.stderr)
        sys.exit(1)
