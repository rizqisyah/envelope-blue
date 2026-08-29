#!/usr/bin/env python3
"""Score every band of the LIVE sheet against the Figma render, in one pass.

band-diff.py takes one window and writes a 3-up strip; this one walks the band table
and prints the whole sheet, which is what you want while the bands are still moving.
Same measurement — mean abs delta per channel, 0-255, no masking — so the numbers are
comparable to the ones recorded in SLICING.md.

    node    scripts/sheet-shot.mjs
    BODY_FRAME=<n> python3 scripts/sheet-score.py
"""
import os
import re
import sys

from PIL import Image, ImageChops

Image.MAX_IMAGE_PIXELS = None

FRAME = os.environ.get("BODY_FRAME", "")
if not FRAME:
    sys.exit("set BODY_FRAME=<body frame number, e.g. 253 for template 5>")
REF = os.environ.get("BAND_REF") or f".figma-tmp/exports{FRAME}/frame{FRAME}-full.png"
# The design frame width. Template 6 is 596 wide, not the 375 templates 2-5 used.
FRAME_W = int(os.environ.get("FRAME_W", "596"))
LIVE = ".figma-tmp/web-sheet-1x.png"

ref = Image.open(REF).convert("RGB")
live = Image.open(LIVE).convert("RGB")
if live.width != FRAME_W:
    sys.exit(f"{LIVE} is {live.width} wide, not {FRAME_W} -- shoot it with scripts/sheet-shot.mjs")

bands = []
for f in sorted(os.listdir("src/lib/bands")):
    if not f.endswith(".ts"):
        continue
    src = open("src/lib/bands/" + f).read()
    top = int(re.search(r"BAND_TOP = (\d+)", src).group(1))
    height = int(re.search(r"BAND_HEIGHT = (\d+)", src).group(1))
    bands.append((f[:-3], top, top + height))
bands.sort(key=lambda b: b[1])

total = 0
for name, y0, y1 in bands:
    d = ImageChops.difference(ref.crop((0, y0, FRAME_W, y1)), live.crop((0, y0, FRAME_W, y1)))
    m = sum(i * n for i, n in enumerate(d.convert("L").histogram())) / (FRAME_W * (y1 - y0))
    total += m * (y1 - y0)
    print(f"{name:9} {y0:5}-{y1:<5} {m:7.3f}")
print(f"{'SHEET':9} {bands[0][1]:5}-{bands[-1][2]:<5} {total / bands[-1][2]:7.3f}")
