#!/usr/bin/env python3
"""Build entry.png for news-image-20261119 round 3 (fresh build).
Draws a 1024x1024 one-page newspaper of Thursday 19 Nov 2026 world news.
All art is drawn in code with Pillow; no external images.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 248, 243)      # paper
INK = (22, 22, 26)
MUT = (92, 88, 84)
RED = (178, 34, 34)
NAVY = (28, 52, 96)
TEAL = (14, 110, 110)
GOLD = (176, 128, 20)
LINE = (200, 194, 186)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def F(path, size):
    return ImageFont.truetype(path, size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

def wrap(text, font, width):
    """Wrap text to pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=font) <= width:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def para(x, y, text, font, fill=INK, width=300, lh=None):
    lh = lh or int(font.size * 1.28)
    for ln in wrap(text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def rule(x0, y, x1, wdt=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)

def num_badge(x, y, n, r=10, fill=RED):
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill)
    f = F(SANSB, 11)
    tw = d.textlength(str(n), font=f)
    d.text((x - tw / 2, y - 8), str(n), font=f, fill=(255, 255, 255))

# ---------------- MASTHEAD ----------------
d.text((512, 10), "THE WORLD IN ONE DAY", font=F(SERIFB, 40),
       fill=INK, anchor="ma")
d.text((512, 58), "THURSDAY 19 NOVEMBER 2026  ·  25 STORIES  ·  ONE PAGE",
       font=F(SANSB, 12), fill=RED, anchor="ma")
rule(14, 86, 1010, 3)
rule(14, 90, 1010, 1)

# ---------------- STAT STRIP ----------------
stats = [
    ("$81.3bn", "Anthropic IPO, the largest ever.\nANT opened $111.50, closed $97.17 (+17%)."),
    ("15.9m", "GTA VI pre-orders, est. Sensor Tower.\n$1.54bn before launch day, 13 yrs on."),
    ("298,676", "people moved to safety in Odisha\nbefore Cyclone Akvan's landfall."),
    ("700,000+", "Rohingya driven from Myanmar in 2017.\nThe World Court ruled: genocide."),
]
sx, sy, sw, sh = 14, 98, 242, 62
for i, (big, lab) in enumerate(stats):
    x = sx + i * (sw + 6)
    d.rectangle([x, sy, x + sw, sy + sh], outline=LINE, width=1, fill=(255, 255, 255))
    d.text((x + 10, sy + 5), big, font=F(SERIFB, 22), fill=NAVY)
    para(x + 10, sy + 33, lab, F(SANS, 9), MUT, sw - 20, 11)
rule(14, 168, 1010, 1, LINE)

# ---------------- HEROES ----------------
d.text((14, 176), "THE THREE BIG STORIES", font=F(SANSB, 12), fill=RED)
HX, HY, HW, HH = 14, 196, 322, 236
GAP = 8

def hero_panel(i, tag, headline, body, src):
    x = HX + i * (HW + GAP)
    d.rectangle([x, HY, x + HW, HY + HH], outline=INK, width=2, fill=(255, 255, 255))
    return x

def hero_text(x, headline, body, src):
    y = HY + 158
    d.text((x + 10, y), headline, font=F(SERIFB, 15), fill=INK)
    y = para(x + 10, y + 21, body, F(SANS, 10.5), INK, HW - 20, 13)
    d.text((x + 10, HY + HH - 16), src, font=F(SANS, 8), fill=MUT)

# Hero 1: Shenzhen summit illustration
x = hero_panel(0, "SUMMIT", "", "", "")
ax, ay, aw, ah = x + 1, HY + 1, HW - 2, 150
d.rectangle([ax, ay, ax + aw, ay + ah], fill=(232, 238, 245))
# skyline
for bx, bw, bh in [(10, 26, 60), (42, 20, 88), (68, 30, 55), (104, 22, 100),
                   (132, 26, 70), (164, 20, 95), (190, 28, 58), (224, 22, 82),
                   (252, 26, 64), (284, 24, 90)]:
    d.rectangle([ax + bx, ay + ah - bh - 42, ax + bx + bw, ay + ah - 42],
                fill=(120, 138, 165))
# flags: US, China, Russia on poles
def flag(fx, kind):
    d.line([(ax + fx, ay + 12), (ax + fx, ay + 62)], fill=INK, width=2)
    if kind == "us":
        d.rectangle([ax + fx, ay + 12, ax + fx + 34, ay + 30], fill=(178, 34, 34))
        for s in range(4):
            d.rectangle([ax + fx, ay + 14 + s * 4, ax + fx + 34, ay + 16 + s * 4],
                        fill=(255, 255, 255))
        d.rectangle([ax + fx, ay + 12, ax + fx + 14, ay + 22], fill=NAVY)
    elif kind == "cn":
        d.rectangle([ax + fx, ay + 12, ax + fx + 34, ay + 30], fill=(222, 41, 16))
        d.text((ax + fx + 4, ay + 14), "*", font=F(SANSB, 12), fill=(255, 215, 0))
    else:
        for j, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
            d.rectangle([ax + fx, ay + 12 + j * 6, ax + fx + 34, ay + 18 + j * 6], fill=c)
flag(28, "us"); flag(143, "cn"); flag(258, "ru")
# round table
d.ellipse([ax + 95, ay + 108, ax + 225, ay + 142], fill=(122, 72, 32))
d.ellipse([ax + 105, ay + 104, ax + 215, ay + 126], fill=(160, 105, 55))
d.text((ax + 118, ay + 108), "TRUMP · XI · PUTIN", font=F(SANSB, 8),
       fill=(255, 255, 255))
num_badge(x + 16, HY + 16, 1)
hero_text(x, "Three leaders, one table",
          "Trump, Xi and Putin meet in Shenzhen in a first-ever trilateral summit, "
          "agreeing nuclear-risk talks and declaring a nuclear war \"cannot be won\".",
          "WSJ · Le Monde · APEC, Shenzhen")

# Hero 2: ICJ illustration
x = hero_panel(1, "JUSTICE", "", "", "")
ax, ay, aw, ah = x + 1, HY + 1, HW - 2, 150
d.rectangle([ax, ay, ax + aw, ay + ah], fill=(238, 232, 222))
# courthouse
d.rectangle([ax + 60, ay + 38, ax + 260, ay + 52], fill=NAVY)
for cx in (75, 115, 155, 195, 235):
    d.rectangle([ax + cx, ay + 52, ax + cx + 12, ay + 118], fill=(240, 236, 228),
                outline=NAVY)
d.rectangle([ax + 55, ay + 118, ax + 265, ay + 130], fill=NAVY)
d.polygon([(ax + 55, ay + 38), (ax + 160, ay + 8), (ax + 265, ay + 38)], fill=NAVY)
# scales
d.line([(ax + 160, ay + 62), (ax + 160, ay + 100)], fill=GOLD, width=3)
d.line([(ax + 128, ay + 68), (ax + 192, ay + 68)], fill=GOLD, width=3)
d.ellipse([ax + 118, ay + 68, ax + 138, ay + 82], outline=GOLD, width=2)
d.ellipse([ax + 182, ay + 68, ax + 202, ay + 82], outline=GOLD, width=2)
d.text((ax + 128, ay + 132), "THE HAGUE", font=F(SANSB, 9), fill=NAVY)
num_badge(x + 16, HY + 16, 2)
hero_text(x, "World Court: it was genocide",
          "The ICJ rules 9-6 that Myanmar committed genocide against the Rohingya in "
          "2017, orders reparations and the return of the displaced.",
          "UN News · Reuters · CNN, The Hague")

# Hero 3: Anthropic IPO illustration
x = hero_panel(2, "MARKETS", "", "", "")
ax, ay, aw, ah = x + 1, HY + 1, HW - 2, 150
d.rectangle([ax, ay, ax + aw, ay + ah], fill=(226, 240, 226))
# rising chart
pts = [(ax + 20, ay + 120), (ax + 60, ay + 112), (ax + 100, ay + 118),
       (ax + 140, ay + 92), (ax + 180, ay + 96), (ax + 220, ay + 58),
       (ax + 260, ay + 62), (ax + 295, ay + 34)]
d.line(pts, fill=TEAL, width=4, joint="curve")
d.polygon(pts + [(ax + 295, ay + 145), (ax + 20, ay + 145)], fill=(14, 110, 110, 40))
d.text((ax + 200, ay + 12), "ANT  $97.17  +17%", font=F(SANSB, 13), fill=TEAL)
d.text((ax + 20, ay + 12), "NASDAQ", font=F(SANSB, 11), fill=MUT)
for gx in (20, 90, 160, 230):
    d.line([(ax + gx, ay + 140), (ax + gx, ay + 146)], fill=MUT, width=1)
num_badge(x + 16, HY + 16, 3)
hero_text(x, "Claude goes public, soars",
          "Anthropic debuts as ANT in the biggest IPO ever, $81.3bn at $83 a share. "
          "It opens at $111.50, closes $97.17, as tech stocks slide.",
          "CNN · Reuters · WSJ, New York")

# ---------------- MEDIUM GRID ----------------
d.text((14, 442), "TEN MORE STORIES FROM THE DAY", font=F(SANSB, 12), fill=RED)
MX, MY, MW, MH, MG = 14, 460, 196, 112, 6

def icon(x, y, kind, bg):
    d.rectangle([x, y, x + 40, y + 40], fill=bg)
    if kind == "climate":  # sun + leaf
        d.ellipse([x + 9, y + 8, x + 31, y + 30], fill=(255, 200, 60))
        d.ellipse([x + 14, y + 26, x + 30, y + 36], fill=(40, 140, 60))
    elif kind == "game":  # controller
        d.rounded_rectangle([x + 6, y + 14, x + 34, y + 30], radius=6, fill=INK)
        d.ellipse([x + 11, y + 19, x + 16, y + 24], fill=(255, 255, 255))
        d.ellipse([x + 24, y + 19, x + 29, y + 24], fill=(255, 80, 80))
    elif kind == "storm":  # spiral
        for r in (15, 10, 5):
            d.arc([x + 20 - r, y + 20 - r, x + 20 + r, y + 20 + r],
                  20, 300, fill=(255, 255, 255), width=3)
    elif kind == "exam":  # pencil
        d.polygon([(x + 10, y + 30), (x + 26, y + 8), (x + 32, y + 14),
                   (x + 16, y + 34)], fill=(255, 200, 60))
        d.polygon([(x + 10, y + 30), (x + 16, y + 34), (x + 13, y + 36)], fill=INK)
    elif kind == "jobs":  # briefcase
        d.rectangle([x + 8, y + 15, x + 32, y + 32], fill=(120, 80, 40))
        d.rectangle([x + 15, y + 10, x + 25, y + 16], outline=(120, 80, 40), width=3)
    elif kind == "strike":  # megaphone
        d.polygon([(x + 8, y + 18), (x + 22, y + 12), (x + 22, y + 28),
                   (x + 8, y + 24)], fill=RED)
        d.rectangle([x + 22, y + 12, x + 32, y + 28], fill=RED)
        d.line([(x + 12, y + 28), (x + 12, y + 34)], fill=INK, width=3)
    elif kind == "run":  # runner
        d.ellipse([x + 20, y + 6, x + 28, y + 14], fill=INK)
        d.line([(x + 24, y + 14), (x + 20, y + 26)], fill=INK, width=4)
        d.line([(x + 20, y + 26), (x + 12, y + 36)], fill=INK, width=3)
        d.line([(x + 20, y + 26), (x + 30, y + 32)], fill=INK, width=3)
        d.line([(x + 22, y + 18), (x + 32, y + 12)], fill=INK, width=3)
    elif kind == "euro":  # coin
        d.ellipse([x + 8, y + 8, x + 32, y + 32], fill=(255, 215, 0))
        d.text((x + 14, y + 12), "€", font=F(SANSB, 16), fill=NAVY)
    elif kind == "drought":  # cracked sun
        d.ellipse([x + 11, y + 9, x + 29, y + 27], fill=(255, 150, 40))
        d.line([(x + 8, y + 34), (x + 16, y + 30), (x + 24, y + 35), (x + 32, y + 31)],
               fill=(150, 100, 40), width=2)
    elif kind == "art":  # framed painting
        d.rectangle([x + 8, y + 8, x + 32, y + 32], outline=GOLD, width=3)
        d.ellipse([x + 16, y + 12, x + 26, y + 22], fill=(255, 200, 60))
        d.rectangle([x + 11, y + 26, x + 29, y + 29], fill=TEAL)

medium = [
    (4, "climate", NAVY, "COP31: $120bn fight",
     "Ministers deadlock in Antalya as the push to lock in $120bn a year in adaptation finance is dropped from the latest draft text.", "Reuters"),
    (5, "game", INK, "GTA VI is finally here",
     "Rockstar's epic launches after 13 years on PS5 and Xbox. Pre-orders hit an estimated 15.9m copies, $1.54bn, per Sensor Tower.", "Forbes / Sensor Tower"),
    (6, "storm", TEAL, "Akvan bears down on Odisha",
     "Nearly 300,000 people are evacuated to shelters as the severe cyclone nears India's east coast, with landfall due Friday.", "IMD / Indian media"),
    (7, "exam", GOLD, "Korea's biggest exam day",
     "551,864 students sit the Suneung college exam at 1,312 centres, scanned for AI cheating gadgets and button cameras.", "Yonhap"),
    (8, "jobs", MUT, "Australia's jobs slump",
     "Unemployment hits 4.9%, a five-year high, as 43,500 jobs vanish in October, the second monthly fall in a row.", "ABS"),
    (9, "strike", RED, "Colombia strikes over tax",
     "Unions stage a national strike against President De la Espriella's rescue bill; marches fill Bogota, Cali and Medellin.", "Colombian media"),
    (10, "run", (90, 60, 120), "Marathon champion banned",
     "Kenya's Peres Jepchirchir gets a three-year ban for EPO use and admits the breach; her Sydney Marathon win is stripped.", "Reuters / AIU"),
    (11, "euro", NAVY, "EU's €45bn for Kyiv",
     "Brussels proposes a €45bn loan to plug Ukraine's 2027 funding gap, as Berlin hosts talks on security guarantees.", "10 Things / EU"),
    (12, "drought", (150, 100, 40), "Fiji declares disaster",
     "An El Nino drought forces a nationwide state of disaster, with severe water shortages across the Pacific islands.", "Daily Maverick"),
    (13, "art", GOLD, "Van Gogh sells for $190.4m",
     "A Van Gogh painting fetches a record $190.4m for the artist at auction in New York, the day's priciest headline.", "Le Monde / Horizon"),
]
for i, (n, kind, bg, head, body, src) in enumerate(medium):
    cx = MX + (i % 5) * (MW + MG)
    cy = MY + (i // 5) * (MH + MG)
    d.rectangle([cx, cy, cx + MW, cy + MH], outline=LINE, width=1, fill=(255, 255, 255))
    icon(cx + 8, cy + 8, kind, bg)
    num_badge(cx + MW - 14, cy + 14, n, r=9)
    para(cx + 54, cy + 8, head, F(SANSB, 9.5), INK, MW - 54 - 30, 12)
    para(cx + 8, cy + 52, body, F(SANS, 9), INK, MW - 16, 11.5)
    d.text((cx + 8, cy + MH - 13), src, font=F(SANS, 7.5), fill=MUT)

# ---------------- MAP + ALSO ON ----------------
MY2 = 700
d.text((14, MY2), "WHERE IT HAPPENED", font=F(SANSB, 12), fill=RED)
d.text((514, MY2), "ALSO ON THURSDAY 19 NOVEMBER", font=F(SANSB, 12), fill=RED)
rule(14, MY2 + 17, 1010, 1, LINE)

# dotted world map (land = ellipses in lon/lat)
land = [(-100, 50, 34, 19), (-95, 30, 19, 11), (-42, 72, 11, 7),
        (-60, -10, 14, 21), (15, 52, 17, 9), (20, 5, 19, 24),
        (90, 50, 44, 17), (105, 15, 14, 9), (134, -25, 17, 9),
        (-2, 54, 4, 4), (138, 37, 6, 8), (172, -41, 5, 6),
        (-155, 63, 12, 6), (45, 62, 20, 8)]
mapx, mapy, mapw, maph = 14, 724, 486, 140
def mxy(lon, lat):
    return (mapx + (lon + 180) / 360 * mapw,
            mapy + (75 - lat) / 150 * maph)
lon = -180
while lon <= 180:
    lat = -58
    while lat <= 74:
        for (clon, clat, rx, ry) in land:
            if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1:
                px, py = mxy(lon, lat)
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(150, 160, 175))
                break
        lat += 3
    lon += 4

pins = [(1, 114.1, 22.5, 0, 0), (2, 4.3, 52.1, 0, 0), (3, -74.0, 40.7, 0, 0),
        (4, 30.7, 36.9, 0, 0), (5, -80.2, 25.8, 0, 0), (6, 84.9, 19.3, 0, 0),
        (7, 127.0, 37.5, 0, 0), (8, 149.1, -35.3, 0, 0), (9, -74.1, 4.7, 0, 0),
        (10, 36.8, -1.3, 0, 0), (11, 4.35, 50.85, 15, 13),
        (12, 178.0, -17.7, 0, 0), (13, -73.0, 41.5, 17, -13)]
for n, lon, lat, dx, dy in pins:
    px, py = mxy(lon, lat)
    if dx or dy:
        d.line([(px, py), (px + dx, py + dy)], fill=RED, width=1)
        px, py = px + dx, py + dy
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    f = F(SANSB, 9)
    tw = d.textlength(str(n), font=f)
    d.text((px - tw / 2, py - 6.5), str(n), font=f, fill=(255, 255, 255))
d.text((mapx, mapy + maph + 2), "Pins 1-13 mark the stories above. Dotted map is schematic, not to scale.",
       font=F(SANS, 7.5), fill=MUT)

briefs = [
    (14, "BANGLADESH", "Violence in 28 districts; Yunus's ancestral home set on fire."),
    (15, "EU-INDONESIA", "Brussels authorises signing of a major trade and investment pact."),
    (16, "NORTH KOREA", "IAEA: Pyongyang is expanding its original uranium enrichment site."),
    (17, "SAUDI ARABIA", "Houthi rocket debris damages the PIF tower in Riyadh."),
    (18, "ETHIOPIA-ERITREA", "Troops mass on the shared border; fears of renewed war grow."),
    (19, "COOK ISLANDS", "Cyclone Xavier, category 5, batters the northern islands."),
    (20, "DENMARK", "Parliament backs the Greenland defence deal, 109 votes to none."),
    (21, "WASHINGTON", "Senate rejects an Iran war-powers resolution, 51-48."),
    (22, "LONDON-OSLO", "UK and Norway fund two Ukrainian naval craft, over £100m."),
    (23, "INDONESIA", "Wildfires this season have burned nearly 3m hectares."),
    (24, "HAITI", "Pastor convicted over the 2021 killing of President Moise."),
    (25, "CHINA", "Homo erectus teeth in Guangxi challenge a theory of human evolution."),
]
by = 726
for n, place, text in briefs:
    d.text((514, by), f"{n}.", font=F(SANSB, 10), fill=RED)
    d.text((540, by), place + "  ", font=F(SANSB, 10), fill=INK)
    w0 = d.textlength(place + "  ", font=F(SANSB, 10))
    d.text((540 + w0, by), text, font=F(SANS, 10), fill=INK)
    by += 13

# ---------------- DATE CHECK + SOURCES ----------------
DY = 878
d.rectangle([14, DY, 1010, DY + 62], outline=RED, width=1, fill=(255, 244, 240))
d.text((24, DY + 6), "DATE CHECK: deliberately left out", font=F(SANSB, 11), fill=RED)
dc_left = ("These big stories were first reported on Wednesday 18 Nov, so they are NOT "
           "counted as 19 Nov news here: the Crimea bridge was hit by Ukrainian missiles; "
           "Iran struck Kuwait and Bahrain; Israeli ground forces crossed Gaza's Yellow Line.")
dc_right = ("Also 18 Nov, not 19 Nov: Anthropic's $83 IPO price was announced (only Thursday's "
            "first trade is counted above); COP31's first draft deal was published Mon 16 Nov "
            "(only Thursday's talks are counted).")
para(24, DY + 24, dc_left, F(SANS, 9), INK, 470, 11.5)
para(516, DY + 24, dc_right, F(SANS, 9), INK, 470, 11.5)

SY = 946
d.text((14, SY), "SOURCES", font=F(SANSB, 10), fill=RED)
para(14, SY + 15,
     "Reuters, WSJ, CNN, UN News, Le Monde, Yonhap, ABS (Australia), India Meteorological Dept, "
     "Athletics Integrity Unit, Sensor Tower estimates via Forbes (GTA VI figures are estimates, "
     "not publisher disclosures), EU, IAEA, Daily Maverick, Horizon / 10 Things round-ups.",
     F(SANS, 8.5), MUT, 996, 11)
d.text((14, SY + 42),
       "Every story above was first reported on Thursday 19 November 2026. Figures are as reported "
       "that day; estimates are labelled. Drawn entirely in code; no photographs.",
       font=F(SANS, 8.5), fill=MUT)
rule(14, SY + 56, 1010, 1, LINE)
d.text((512, SY + 61), "THE WORLD IN ONE DAY  ·  19 NOVEMBER 2026  ·  25 STORIES",
       font=F(SANSB, 9), fill=MUT, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
