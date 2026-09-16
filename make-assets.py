"""Rebuild the page's images from the App Store assets.

Writes the three device crops in img/ and img/og.png, the 1200x630 link-preview card.

Palette and type come from Marketing/BRAND-KIT.md: olive ground, one accent
(chartreuse), Inter Tight Black for the headline, Inter for everything else.
Run from the repo root: python3 make-og.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

APP = Path("/Users/matthewedwards/Documents/Developer/Footy Offseason")
TIGHT = APP / "Marketing/instagram/fonts/InterTight.ttf"
TEXT = APP / "Marketing/instagram/fonts/Inter.ttf"
ICON = APP / "FootyReady/FootyReady/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png"
SHOTS = APP / "AppStoreAssets/screenshots/6.5"

# Each App Store screenshot is a headline over a device frame on olive. The page
# wants the device alone, still on its olive ground, bleeding off the bottom the
# way it does in the original. The frame sits at the same x in every file; only
# its top moves, so that is measured rather than hard-coded.
CROPS = [("02-know-why", "shot-why"),
         ("03-check-in", "shot-checkin"),
         ("01-season-built", "shot-season")]


def crop_devices():
    for name, tag in CROPS:
        im = Image.open(SHOTS / f"{name}.png").convert("RGB")
        black = np.asarray(im).astype(int).max(2) < 30
        top = np.where(black.sum(1) > 400)[0].min() - 6
        shot = im.crop((118, top, 1160, im.height))
        shot.thumbnail((640, 4000), Image.LANCZOS)
        shot.save(f"img/{tag}.png", optimize=True)
        print(f"img/{tag}.png", shot.size)

OLIVE, CHARTREUSE, BONE = "#15200A", "#C7F04F", "#F5F4EE"
W, H = 1200, 630


def font(path, size, wght):
    f = ImageFont.truetype(str(path), size)
    f.set_variation_by_axes([wght] if path == TIGHT else [size, wght])
    return f


crop_devices()

# The avatar and the tab icon are the shipped App Store icon, unchanged.
app_icon = Image.open(ICON).convert("RGB")
app_icon.resize((180, 180), Image.LANCZOS).save("img/icon.png", optimize=True)
app_icon.resize((64, 64), Image.LANCZOS).save("img/favicon.png", optimize=True)

card = Image.new("RGB", (W, H), OLIVE)
d = ImageDraw.Draw(card)

icon = Image.open(ICON).convert("RGB").resize((72, 72), Image.LANCZOS)
mask = Image.new("L", (72, 72), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, 71, 71), radius=16, fill=255)
card.paste(icon, (64, 56), mask)
d.text((152, 78), "Footy Ready", font=font(TEXT, 30, 600), fill=BONE, anchor="lm")

COLUMN = 580  # the text column, so nothing runs under the device shot

lines = ["THE PRE-SEASON", "THAT KNOWS YOU"]
size = 76
while size > 40:
    head = font(TIGHT, size, 900)
    if max(d.textlength(l, font=head) for l in lines) <= COLUMN:
        break
    size -= 2
advance = int(size * 0.95)
for i, line in enumerate(lines):
    d.text((64, 268 + i * advance), line, font=head, fill=CHARTREUSE, anchor="ls")

body = font(TEXT, 26, 400)
d.text((64, 356), "Aussie rules / rugby league / rugby union / soccer",
       font=body, fill=CHARTREUSE, anchor="lt")
d.text((64, 424), "Training built around your season dates,",
       font=body, fill=BONE, anchor="lt")
d.text((64, 462), "your body and the gear you actually have.",
       font=body, fill=BONE, anchor="lt")

shot = Image.open("img/shot-why.png")
width = 400
shot = shot.resize((width, int(shot.height * width / shot.width)), Image.LANCZOS)
card.paste(shot, (730, 140))

card.save("img/og.png", optimize=True)
print("img/og.png", card.size)
