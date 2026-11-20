"""Build entry.png: one-day world news infographic, 19 Nov 2026. Stdlib + PIL only."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
NAVY = (16, 36, 62)
RED = (178, 34, 34)
GRAY = (90, 90, 90)
DARK = (30, 30, 30)
SEA = (198, 216, 228)
LAND = (232, 221, 194)

def font(bold, size):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(p, size)
    except Exception:
        return ImageFont.load_default()

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

STORIES = [
    (1, "ICJ: Myanmar guilty of genocide", "World court: first genocide ruling against a state", 52.07, 4.30, "court"),
    (2, "Trump, Xi, Putin meet in Shenzhen", "First trilateral summit ends in joint peace declaration", 22.54, 114.06, "flags"),
    (3, "Kerch Bridge hit a third time", "Rail span struck; road arch already down, trains halted", 45.31, 36.51, "bridge"),
    (4, "Tanker attacks in Hormuz Strait", "ADNOC ship hit: 11 hurt, 1 missing; mines reported", 26.60, 56.20, "tanker"),
    (5, "Anthropic debuts on Nasdaq", "Priced at $83 a share; valued near $1.5 trillion", 40.71, -74.00, "chart"),
    (6, "Wall Street slides again", "S&P 500 down 2.02%; Nikkei off 4.68%; gold sinks", 35.68, 139.69, "down"),
    (7, "Haiti police kill 34 in raid", "Martissant operation targets gangs; no police hurt", 18.54, -72.34, "shield"),
    (8, "Denmark backs Greenland deal", "Parliament votes 109-0 for US security agreement", 55.68, 12.57, "snow"),
    (9, "Migrant boat sinks off Senegal", "Survivors say about 100 aboard; dozens missing", 14.69, -17.45, "boat"),
    (10, "Israel ends Gaza tank raid", "First ground push past Yellow Line since the truce", 31.50, 34.47, "tank"),
    (11, "COP31 draft drops fossil fuels", "Draft drops all fossil-fuel language; talks stall", 36.90, 30.71, "leaf"),
    (12, "Van Gogh sells for $190.4m", "Record for the artist at Sotheby's in New York", 49.07, 2.17, "paint"),
    (13, "Bangladesh burns in protests", "Yunus home torched; unrest reported in 28 districts", 23.81, 90.41, "flame"),
    (14, "North Korea expands enrichment", "IAEA: new Yongbyon extension finished in October", 39.80, 125.30, "atom"),
    (15, "Jeffries nominated for speaker", "Democrats back him 251-11; first Black speaker", 38.90, -77.04, "dome"),
    (16, "Binance wins $6.5bn freeze order", "Abu Dhabi court acts after record October hack", 24.45, 54.38, "coin"),
    (17, "US signs Venezuela military pact", "Hegseth visits Caracas; training, intelligence shared", 10.48, -66.88, "shake"),
    (18, "EU-Mexico farm tariffs fall", "Pact cuts 95% of duties on farm goods", 19.43, -99.13, "wheat"),
]

REST = [
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

STATS = [
    ("48", "stories from six continents"),
    ("$190.4m", "record price for a Van Gogh"),
    ("879,000", "AI chips cleared for China"),
    ("589m", "children living in conflict zones"),
    ("$83", "Anthropic IPO price per share"),
    ("109-0", "Denmark's Greenland deal vote"),
]

TINTS = {"court": (214, 222, 235), "flags": (235, 220, 205), "bridge": (205, 220, 228),
         "tanker": (200, 215, 225), "chart": (210, 232, 210), "down": (240, 205, 205),
         "shield": (205, 215, 235), "snow": (225, 232, 240), "boat": (200, 220, 235),
         "tank": (220, 225, 205), "leaf": (210, 232, 205), "paint": (245, 225, 180),
         "flame": (245, 215, 190), "atom": (215, 225, 240), "dome": (220, 220, 230),
         "coin": (245, 225, 170), "shake": (225, 215, 225), "wheat": (240, 230, 190)}

def draw_icon(d, kind, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=TINTS.get(kind, (220, 220, 220)))
    cx, cy = x + s / 2, y + s / 2
    if kind == "court":
        d.polygon([(x + 6, y + 18), (cx, y + 6), (x + s - 6, y + 18)], fill=NAVY)
        for i in range(3):
            px = x + 10 + i * 16
            d.rectangle([px, y + 20, px + 7, y + 42], fill=(120, 130, 150))
        d.rectangle([x + 6, y + 42, x + s - 6, y + 48], fill=NAVY)
    elif kind == "flags":
        for i, c in enumerate([(178, 34, 34), (16, 36, 62), (200, 160, 40)]):
            px = x + 8 + i * 16
            d.line([px, y + 8, px, y + 46], fill=(60, 60, 60), width=2)
            d.rectangle([px, y + 8, px + 13, y + 20], fill=c)
    elif kind == "bridge":
        d.arc([x + 6, y + 14, x + s - 6, y + 44], 180, 360, fill=RED, width=3)
        d.rectangle([x + 4, y + 30, x + s - 4, y + 35], fill=NAVY)
        for i in range(4):
            px = x + 12 + i * 11
            d.line([px, y + 31, px, y + 20], fill=NAVY, width=1)
    elif kind == "tanker":
        d.rectangle([x + 8, y + 26, x + s - 8, y + 40], fill=(40, 60, 90))
        d.rectangle([x + 14, y + 16, x + 26, y + 26], fill=RED)
        d.rectangle([x + 28, y + 18, x + 40, y + 26], fill=(200, 160, 40))
        d.line([x + 4, y + 44, x + s - 4, y + 44], fill=(60, 120, 160), width=2)
    elif kind == "chart":
        pts = [(x + 8, y + 40), (x + 20, y + 32), (x + 30, y + 36), (x + 42, y + 18), (x + 48, y + 12)]
        d.line(pts, fill=(20, 120, 60), width=3, joint="curve")
        d.polygon([(x + 44, y + 8), (x + 52, y + 12), (x + 44, y + 16)], fill=(20, 120, 60))
    elif kind == "down":
        for i, h in enumerate([30, 24, 18, 12]):
            px = x + 8 + i * 11
            d.rectangle([px, y + 44 - h, px + 7, y + 44], fill=RED)
        d.line([(x + 8, y + 14), (x + 46, y + 40)], fill=(120, 20, 20), width=3)
    elif kind == "shield":
        d.polygon([(x + 10, y + 8), (x + s - 10, y + 8), (x + s - 10, y + 28), (cx, y + 48), (x + 10, y + 28)], fill=NAVY)
        d.line([(x + 18, y + 26), (x + 25, y + 33), (x + 38, y + 18)], fill=(255, 255, 255), width=3)
    elif kind == "snow":
        d.polygon([(x + 4, y + 44), (x + 18, y + 20), (x + 32, y + 44)], fill=(255, 255, 255))
        d.polygon([(x + 24, y + 44), (x + 40, y + 14), (x + s - 4, y + 44)], fill=(180, 200, 220))
        for px, py in [(x + 12, y + 10), (x + 44, y + 8), (x + 34, y + 26)]:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))
    elif kind == "boat":
        d.polygon([(cx, y + 8), (cx, y + 30), (x + s - 12, y + 30)], fill=(255, 255, 255))
        d.polygon([(x + 8, y + 32), (x + s - 8, y + 32), (x + s - 14, y + 42), (x + 14, y + 42)], fill=(120, 60, 30))
        d.line([x + 4, y + 46, x + s - 4, y + 46], fill=(60, 120, 160), width=2)
    elif kind == "tank":
        d.rectangle([x + 10, y + 24, x + 40, y + 38], fill=(90, 100, 70))
        d.line([x + 40, y + 28, x + s - 6, y + 22], fill=(70, 80, 55), width=4)
        for i in range(3):
            d.ellipse([x + 12 + i * 10, y + 38, x + 19 + i * 10, y + 45], fill=(40, 40, 40))
    elif kind == "leaf":
        d.ellipse([x + 12, y + 10, x + s - 12, y + 44], fill=(40, 140, 60))
        d.line([cx, y + 10, cx, y + 46], fill=(20, 90, 40), width=2)
    elif kind == "paint":
        for a in range(8):
            ang = a * math.pi / 4
            px, py = cx + 13 * math.cos(ang), cy + 13 * math.sin(ang)
            d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(240, 180, 30))
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(120, 70, 20))
    elif kind == "flame":
        d.polygon([(cx, y + 6), (x + s - 10, y + 28), (x + s - 14, y + 44), (x + 12, y + 44), (x + 10, y + 28)], fill=(230, 90, 20))
        d.ellipse([cx - 7, cy + 2, cx + 7, cy + 16], fill=(245, 180, 40))
    elif kind == "atom":
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
        for a in (0, 60, 120):
            d.ellipse([x + 6, y + 10, x + s - 6, y + s - 10], outline=NAVY, width=2)
    elif kind == "dome":
        d.pieslice([x + 14, y + 10, x + s - 14, y + 34], 180, 360, fill=NAVY)
        d.rectangle([x + 12, y + 34, x + s - 12, y + 44], fill=(120, 130, 150))
    elif kind == "coin":
        d.ellipse([x + 10, y + 10, x + s - 10, y + s - 10], fill=(220, 170, 40), outline=(150, 110, 20), width=2)
        d.ellipse([x + 18, y + 18, x + s - 18, y + s - 18], outline=(150, 110, 20), width=2)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(150, 110, 20))
    elif kind == "shake":
        d.line([(x + 8, y + 20), (cx, y + 34), (x + s - 8, y + 20)], fill=NAVY, width=4)
        d.ellipse([cx - 8, cy - 2, cx + 8, cy + 14], fill=(200, 140, 100))
    elif kind == "wheat":
        d.line([cx, y + 12, cx, y + 46], fill=(150, 110, 40), width=2)
        for i in range(4):
            py = y + 14 + i * 8
            d.ellipse([cx - 8, py, cx - 2, py + 6], fill=(210, 170, 60))
            d.ellipse([cx + 2, py, cx + 8, py + 6], fill=(210, 170, 60))

# Simple continent outlines in lon/lat (rough, recognisable).
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 69), (-80, 73), (-60, 62), (-55, 47), (-70, 42), (-80, 32), (-97, 26), (-105, 20), (-117, 32), (-125, 40), (-150, 60)],
    [(-80, 10), (-62, 9), (-50, 0), (-40, -8), (-35, -20), (-48, -28), (-58, -38), (-70, -52), (-73, -30), (-80, -5)],
    [(-10, 37), (-6, 36), (10, 37), (20, 40), (30, 36), (36, 36), (30, 30), (20, 32), (10, 34), (0, 36)],
    [(-18, 35), (-15, 28), (-10, 15), (0, 5), (9, 4), (14, -5), (20, -18), (28, -32), (35, -25), (40, -12), (42, 0), (48, 11), (43, 12), (35, 28), (32, 31), (20, 32)],
    [(30, 70), (45, 68), (60, 69), (70, 72), (90, 75), (110, 76), (130, 72), (160, 66), (178, 65), (162, 60), (140, 40), (127, 35), (120, 22), (108, 10), (100, 6), (95, 15), (88, 22), (80, 8), (72, 20), (60, 25), (55, 26), (48, 30), (43, 12), (40, 15)],
    [(113, -22), (114, -32), (130, -32), (140, -38), (150, -37), (153, -27), (146, -19), (142, -11), (132, -12), (122, -14)],
]

def project(lon, lat, mx, my, mw, mh):
    px = mx + (lon + 180) / 360 * mw
    py = my + (84 - lat) / (84 + 58) * mh
    return px, py

def build(out="entry.png"):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 56], fill=NAVY)
    d.text((16, 11), "THE WORLD IN ONE DAY", font=font(True, 34), fill=(255, 255, 255))
    d.rectangle([W - 316, 8, W - 12, 48], fill=RED)
    dt = "THURSDAY, 19 NOVEMBER 2026"
    fdt = font(True, 15)
    d.text((W - 164 - d.textlength(dt, font=fdt) / 2, 19), dt, font=fdt, fill=(255, 255, 255))
    # Ticker
    d.rectangle([0, 56, W, 82], fill=RED)
    tick = "THURSDAY, 19 NOVEMBER 2026  |  ICJ: MYANMAR GUILTY  |  TRUMP, XI, PUTIN IN SHENZHEN  |  ANTHROPIC IPO $83  |  S&P 500 DOWN 2.02%"
    ft = font(True, 12)
    while d.textlength(tick, font=ft) > W - 20 and ft.size > 9:
        ft = font(True, ft.size - 1)
    d.text((10, 62), tick, font=ft, fill=(255, 255, 255))
    # Story grid 3x6
    gx, gy, cw, chh, gap = 12, 90, 328, 61, 6
    for i, (n, head, deck, lat, lon, kind) in enumerate(STORIES):
        r, c = divmod(i, 3)
        x, y = gx + c * (cw + 8), gy + r * (chh + gap)
        d.rectangle([x, y, x + cw, y + chh], fill=(255, 255, 255), outline=(200, 195, 185), width=1)
        draw_icon(d, kind, x + 3, y + 3, 55)
        tx = x + 64
        tw = cw - 64 - 26
        hl = wrap(d, head, font(True, 13), tw)[:2]
        yy = y + 4
        for line in hl:
            d.text((tx, yy), line, font=font(True, 13), fill=DARK)
            yy += 15
        dl = wrap(d, deck, font(False, 10), tw)[:2]
        for line in dl:
            d.text((tx, yy), line, font=font(False, 10), fill=GRAY)
            yy += 12
        bx, by = x + cw - 13, y + 12
        d.ellipse([bx - 10, by - 10, bx + 10, by + 10], fill=NAVY)
        num = str(n)
        nf = font(True, 10 if n < 10 else 9)
        d.text((bx - d.textlength(num, font=nf) / 2, by - 7), num, font=nf, fill=(255, 255, 255))
    # Map label
    d.text((12, 494), "WHERE IT HAPPENED \u2014 18 STORIES ON THE MAP", font=font(True, 13), fill=NAVY)
    # Map
    mx, my, mw, mh = 12, 516, 640, 200
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=(180, 180, 175), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(190, 180, 160))
    # Pins with nudges for overlaps (true point -> drawn pin)
    nudge = {1: (0, -12), 8: (10, -8), 12: (-14, 10), 10: (-12, -8), 15: (-16, 10), 16: (14, 12), 11: (18, 14)}
    for (n, head, deck, lat, lon, kind) in STORIES:
        px, py = project(lon, lat, mx, my, mw, mh)
        dx, dy = nudge.get(n, (0, 0))
        qx, qy = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.line([px, py, qx, qy], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED, outline=(255, 255, 255), width=2)
        num = str(n)
        nf = font(True, 9 if n < 10 else 8)
        d.text((qx - d.textlength(num, font=nf) / 2, qy - 6), num, font=nf, fill=(255, 255, 255))
    # Sidebar
    sx = 664
    d.text((sx, 494), "BY THE NUMBERS", font=font(True, 13), fill=NAVY)
    d.rectangle([sx, 516, 1012, 716], fill=(255, 255, 255), outline=(200, 195, 185), width=1)
    yy = 524
    for val, lab in STATS:
        d.text((sx + 10, yy), val, font=font(True, 16), fill=RED)
        d.text((sx + 110, yy + 3), lab, font=font(False, 10), fill=DARK)
        yy += 28
    src = "Sources: Reuters, AP, UN News, IAEA, Sotheby's. All stories reported on 19 Nov 2026."
    for line in wrap(d, src, font(False, 8), 348 - 20):
        d.text((sx + 10, yy + 2), line, font=font(False, 8), fill=GRAY)
        yy += 11
    # Rest header
    d.rectangle([12, 724, 1012, 750], fill=NAVY)
    d.text((20, 730), "THE REST OF THE DAY \u2014 STORIES 19\u201348", font=font(True, 13), fill=(255, 255, 255))
    rh = "48 STORIES \u00b7 6 CONTINENTS"
    d.text((1012 - 8 - d.textlength(rh, font=font(True, 11)), 732), rh, font=font(True, 11), fill=(255, 255, 255))
    # Rest list 3 cols x 10 rows
    for i, title in enumerate(REST):
        col, row = divmod(i, 10)
        x = 12 + col * 336
        y = 758 + row * 20
        n = 19 + i
        fnum = font(True, 10)
        d.text((x, y), str(n) + ".", font=fnum, fill=RED)
        tw = 328 - d.textlength(str(n) + ". ", font=fnum) - 4
        ft2 = font(False, 10)
        if d.textlength(title, font=ft2) > tw:
            ft2 = font(False, 9)
        d.text((x + d.textlength(str(n) + ". ", font=fnum), y), title, font=ft2, fill=DARK)
    # Footer
    foot = "ALL 48 STORIES REPORTED ON THURSDAY 19 NOVEMBER 2026"
    ff = font(False, 9)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 972), foot, font=ff, fill=GRAY)
    img.save(out, "PNG", optimize=True)
    return img

if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    build(os.path.join(here, "entry.png"))
