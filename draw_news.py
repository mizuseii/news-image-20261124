"""Draw the 24 November 2026 world-news infographic (1024x1024 PNG).

Build-time only; run once to produce entry.png. Pillow required.
Layout: navy masthead with the date, a wide lead card (Wall Street rally
as Jensen Huang returns as Nvidia CEO), a 3x3 grid of region blocks
(45 stories in 9 regions), a UTC timeline strip, a numbers panel and a
sources footer. All 45 stories were verified as events that happened, or
were first reported, on Tuesday 24 November 2026.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF = font("DejaVuSerif-Bold.ttf", 40)
F_DATE = font("DejaVuSans-Bold.ttf", 23)
F_TAG = font("DejaVuSans-Bold.ttf", 13)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_LEAD_BODY = font("DejaVuSans.ttf", 15)
F_REGION = font("DejaVuSans-Bold.ttf", 14)
F_STORY = font("DejaVuSans.ttf", 12)
F_TIME = font("DejaVuSans-Bold.ttf", 12)
F_TL = font("DejaVuSans.ttf", 11)
F_NUM = font("DejaVuSans-Bold.ttf", 22)
F_NUM_LBL = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 11)
F_FOOT_B = font("DejaVuSans-Bold.ttf", 11)

PAPER = (247, 242, 231)
NAVY = (18, 38, 63)
NAVY2 = (28, 55, 88)
GOLD = (201, 162, 39)
GOLD_LT = (232, 197, 94)
CARD = (255, 255, 255)
INK = (24, 24, 24)
MUTED = (90, 90, 90)
RED = (178, 34, 34)
LINE = (210, 203, 186)

# (region, header colour, [stories]) - 9 regions x 5 stories = 45
REGIONS = [
    ("MARKETS & ECONOMY", (18, 90, 110), [
        "Wall Street's biggest rally since April 2025: S&P +4.73%, Nasdaq +6.51%",
        "Nvidia +31% in a day as Jensen Huang returns as CEO",
        "Tokyo reopens after holiday; Nikkei fell 5.06% on Friday",
        "South Korea exports strong; chips +294.4% year on year",
        "Gold slides to $3,551.68; dollar strongest since April 2025",
    ]),
    ("MIDDLE EAST", (146, 43, 33), [
        "Israeli airstrike kills at least 3 near police post in Khan Younis",
        "Israeli bombing on Gaza City kills at least 3, media say",
        "Iran warns EU military sites with missiles it claims reach 4,500 km",
        "Israeli army storms West Bank refugee camp and makes arrests",
        "Turkey and Egypt hold phone call on de-escalation and Libya",
    ]),
    ("EUROPE", (31, 68, 120), [
        "About 450 German schools hit by emailed bomb threats",
        "Belgium unveils 22nd package of sanctions on Russia",
        "UN talks on autonomous weapons end with no binding deal",
        "Russian drone briefly violates Poland's airspace",
        "EU sanctions ex-US contractor turned neo-Nazi terror leader",
    ]),
    ("UKRAINE WAR", (90, 40, 90), [
        "Russian strikes kill at least 12 in Kyiv region",
        "Ukraine claims strike on the Benghazi freighter",
        "UK defence minister seeks answers on Starlink in Ukraine",
        "US envoy signals NATO-style guarantees for Ukraine possible",
        "Zelensky and Orban may meet 'soon' in Zakarpattia",
    ]),
    ("ASIA-PACIFIC", (27, 105, 74), [
        "Chinese official sentenced to death for leaking 100 intel reports",
        "North Korean aircraft violated South Korean airspace, Seoul says",
        "Lahore tops global pollution ranking with AQI over 500",
        "More than 30 workers lost in Banten candy-factory fire, Indonesia",
        "Bangladesh garment workers reject latest pay offer",
    ]),
    ("AMERICAS", (110, 58, 124), [
        "O'Hare ground stop over staffing amid Thanksgiving rush",
        "Trump targets Newsom in DOJ speech over 548 commuted death sentences",
        "FBI raids Minnesota child centres in $41m fraud probe",
        "Mossad ex-chief: Swift's Vienna shows saved from ISIS-inspired plot",
        "More than 1,600 Delta services delayed US-wide on technical issue",
    ]),
    ("AFRICA", (176, 112, 22), [
        "Dozens killed in weekend attacks across Nigeria's Niger state",
        "UN criticises airstrikes on Khartoum thought launched from Ethiopia",
        "Three killed, a dozen hurt in drone assault on civilian Khartoum sites",
        "Aid group alleges RSF looting shops and seizing cattle in Kordofan",
        "Erdogan plans first Libya visit in 15 years",
    ]),
    ("SCIENCE & TECH", (58, 110, 140), [
        "Stem-cell 'human-mouse' model to probe how Parkinson's starts",
        "Tooth sensitivity costs Australians up to $2.1bn a year, study finds",
        "UN chief demands AI safety framework within a year",
        "Senate Banking hearing for Huang set for 3 December",
        "German reports: Russia ready to launch a nuclear-armed satellite",
    ]),
    ("SPORT & CULTURE", (40, 120, 60), [
        "Champions League Matchday 5: Arsenal-Dortmund, Man City-Napoli, Real-PSV",
        "Davis Cup Final 8 begins in Bologna",
        "NBA Cup games tip off across the US tonight",
        "Tom Felton invites freed Ukrainian Marine to Harry Potter studio",
        "King Charles reaches out to Meghan after Thomas Markle arrest",
    ]),
]

TIMELINE = [
    ("OVERNIGHT", "Wall Street soars"),
    ("MORNING", "Tokyo reopens"),
    ("MIDDAY", "Gaza strikes kill 6+"),
    ("AFTERNOON", "~450 schools threatened"),
    ("EVENING", "UCL Matchday 5"),
    ("NIGHT", "Davis Cup begins"),
]

NUMBERS = [
    ("+4.73%", "S&P 500"),
    ("+6.51%", "Nasdaq"),
    ("+31%", "Nvidia\nin a day"),
    ("+294.4%", "S. Korea chip\nexports YoY"),
    ("$3,551.68", "Gold\nper ounce"),
    ("~450", "German schools\nthreatened"),
]


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Subtle paper dot texture (adds print feel and image detail) ----
    dot = (238, 232, 216)
    for yy in range(4, H, 7):
        for xx in range(4, W, 7):
            d.point((xx, yy), fill=dot)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.rectangle([0, 88, W, 91], fill=GOLD)
    title = "THE WORLD IN ONE IMAGE"
    tw = d.textlength(title, font=F_SERIF)
    d.text(((W - tw) / 2, 10), title, font=F_SERIF, fill=GOLD_LT)
    date = "TUESDAY  24  NOVEMBER  2026"
    dw = d.textlength(date, font=F_DATE)
    d.text(((W - dw) / 2, 56), date, font=F_DATE, fill=(255, 255, 255))

    # ---- Lead card ----
    lx, ly, lw, lh = 16, 100, W - 32, 118
    d.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=8, fill=CARD,
                        outline=LINE, width=1)
    d.rectangle([lx, ly + 4, lx + 7, ly + lh - 4], fill=GOLD)
    d.rectangle([lx + 20, ly + 14, lx + 20 + 62, ly + 14 + 20], fill=RED)
    d.text((lx + 20 + 8, ly + 17), "LEAD", font=F_TAG, fill=(255, 255, 255))
    head = "WALL STREET SOARS AS HUANG RETURNS"
    d.text((lx + 96, ly + 12), head, font=F_LEAD_HEAD, fill=NAVY)
    body1 = ("Biggest rally since April 2025 - S&P 500 +4.73%, Nasdaq +6.51%, "
             "Dow +3.01% - as Nvidia's board reinstates Jensen Huang as CEO; "
             "Nvidia jumps 31% in a day.")
    for i, line in enumerate(wrap(d, body1, F_LEAD_BODY, lw - 40)):
        d.text((lx + 20, ly + 50 + i * 19), line, font=F_LEAD_BODY, fill=INK)
    body2 = ("Also: Russian strikes kill at least 12 in the Kyiv region; "
             "Israeli strikes in Gaza kill at least 6; ~450 German schools "
             "hit by bomb threats.")
    for i, line in enumerate(wrap(d, body2, F_LEAD_BODY, lw - 40)):
        d.text((lx + 20, ly + 88 + i * 19), line, font=F_LEAD_BODY, fill=MUTED)

    # ---- Region grid: 3 x 3 ----
    gx, gy = 16, 228
    cw, chh, gap = 325, 188, 8
    for idx, (region, colour, stories) in enumerate(REGIONS):
        col, row = idx % 3, idx // 3
        x = gx + col * (cw + gap)
        y = gy + row * (chh + gap)
        d.rounded_rectangle([x, y, x + cw, y + chh], radius=6, fill=CARD,
                            outline=LINE, width=1)
        d.rounded_rectangle([x, y, x + cw, y + 26], radius=6, fill=colour)
        d.rectangle([x, y + 20, x + cw, y + 26], fill=colour)
        d.text((x + 10, y + 5), region, font=F_REGION, fill=(255, 255, 255))
        ty = y + 32
        for story in stories:
            lines = wrap(d, story, F_STORY, cw - 36)[:2]
            d.rectangle([x + 12, ty + 4, x + 17, ty + 9], fill=colour)
            for j, line in enumerate(lines):
                d.text((x + 24, ty + j * 14), line, font=F_STORY, fill=INK)
            ty += len(lines) * 14 + 3
            if ty > y + chh - 4:
                break

    # ---- Timeline strip ----
    tx, ty, tw_, th = 16, 816, W - 32, 66
    d.rounded_rectangle([tx, ty, tx + tw_, ty + th], radius=6, fill=NAVY2)
    lbl = "THE DAY IN ORDER"
    lw_ = d.textlength(lbl, font=F_TAG)
    d.text((tx + tw_ - lw_ - 12, ty + 5), lbl, font=F_TAG, fill=GOLD_LT)
    seg = tw_ / len(TIMELINE)
    d.line([(tx + 20, ty + 40), (tx + tw_ - 20, ty + 40)], fill=GOLD, width=2)
    for i, (when, what) in enumerate(TIMELINE):
        cx = tx + seg * i + seg / 2
        d.ellipse([cx - 5, ty + 35, cx + 5, ty + 45], fill=GOLD)
        wl = d.textlength(when, font=F_TIME)
        d.text((cx - wl / 2, ty + 21), when, font=F_TIME, fill=(255, 255, 255))
        wl2 = d.textlength(what, font=F_TL)
        d.text((cx - wl2 / 2, ty + 49), what, font=F_TL, fill=(220, 225, 235))

    # ---- Numbers panel ----
    nx, ny, nw, nh = 16, 890, W - 32, 64
    d.rounded_rectangle([nx, ny, nx + nw, ny + nh], radius=6, fill=CARD,
                        outline=LINE, width=1)
    seg = nw / len(NUMBERS)
    for i, (num, lbl) in enumerate(NUMBERS):
        cx = nx + seg * i + seg / 2
        nl = d.textlength(num, font=F_NUM)
        d.text((cx - nl / 2, ny + 6), num, font=F_NUM, fill=NAVY)
        for j, line in enumerate(lbl.split("\n")):
            ll = d.textlength(line, font=F_NUM_LBL)
            d.text((cx - ll / 2, ny + 34 + j * 13), line, font=F_NUM_LBL,
                   fill=MUTED)
        if i:
            d.line([(nx + seg * i, ny + 10), (nx + seg * i, ny + nh - 10)],
                   fill=LINE, width=1)

    # ---- Footer ----
    fy = 962
    f1 = "Sources: Reuters  |  MarketIndex  |  Times of India  |  BBC  |  AP  |  AFP"
    fw = d.textlength(f1, font=F_FOOT_B)
    d.text(((W - fw) / 2, fy), f1, font=F_FOOT_B, fill=INK)
    f2 = ("All events happened, or were first reported, on Tuesday 24 November 2026  -  "
          "45 stories  -  9 regions")
    fw2 = d.textlength(f2, font=F_FOOT)
    d.text(((W - fw2) / 2, fy + 18), f2, font=F_FOOT, fill=MUTED)
    f3 = "One image, one day: the world as it happened."
    fw3 = d.textlength(f3, font=F_FOOT)
    d.text(((W - fw3) / 2, fy + 36), f3, font=F_FOOT, fill=MUTED)

    out = os.path.join(HERE, "entry.png")

    # ---- Subtle deterministic paper grain over the whole image ----
    rng = random.Random(20261124)
    grain = Image.new("L", (W, H))
    grain.putdata([rng.randint(0, 255) for _ in range(W * H)])
    grain_rgb = Image.merge("RGB", (grain, grain, grain))
    img = Image.blend(img, grain_rgb, 0.015)

    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    draw()
