#!/usr/bin/env python3
"""Compare one text node's ink box between the Figma render and the live sheet.

This is what a substitute face gets measured with. Both crops are thresholded against
their OWN most common colour rather than a fixed ground, because the body frame's copy
sits on wine, on cream, on a linen card and on a dark plate, and a fixed background
would find the plate's edge instead of the glyphs.

Pick a window that contains the node's glyphs and nothing else — a floral inside it is
counted as ink and the numbers become meaningless.

    node    scripts/sheet-shot.mjs
    BODY_FRAME=<n> python3 scripts/ink-box.py <y0> <y1> [x0] [x1]

Width is the number to compensate against: a script face's height is dominated by one
or two ascenders, so it moves much less than the set width when the size changes.
"""
import os
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

FRAME = os.environ.get("BODY_FRAME", "1")
REF = os.environ.get("BAND_REF") or f".figma-tmp/exports{FRAME}/frame{FRAME}-full.png"
LIVE = ".figma-tmp/web-sheet-1x.png"
THRESHOLD = 45

y0, y1 = int(sys.argv[1]), int(sys.argv[2])
x0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
x1 = int(sys.argv[4]) if len(sys.argv) > 4 else int(os.environ.get("FRAME_W", "596"))


def ink(im):
    px = im.load()
    ground = max(im.getcolors(im.width * im.height))[1]
    pts = [
        (x, y)
        for y in range(im.height)
        for x in range(im.width)
        if sum(abs(a - b) for a, b in zip(px[x, y], ground)) > THRESHOLD
    ]
    if not pts:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs) + x0, max(xs) + x0, min(ys) + y0, max(ys) + y0, len(pts)


def show(label, box):
    if not box:
        return print(f"{label:5} no ink")
    a, b, c, d, n = box
    print(f"{label:5} x {a}..{b} w {b - a:<4} | y {c}..{d} h {d - c:<4} n={n}")


ref = ink(Image.open(REF).convert("RGB").crop((x0, y0, x1, y1)))
live = ink(Image.open(LIVE).convert("RGB").crop((x0, y0, x1, y1)))
show("FIG", ref)
show("WEB", live)
if ref and live and live[1] > live[0]:
    print(f"width ratio FIG/WEB = {(ref[1] - ref[0]) / (live[1] - live[0]):.3f}")
