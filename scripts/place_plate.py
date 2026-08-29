#!/usr/bin/env python3
"""Find where ONE layer belongs when it is hundreds of pixels from where the tables put it.

solve_alpha.py refines a layer inside a +/-40px window, which is the right window for a
layer the clip rule nearly had. It is useless for the class this file exists for: a
rotated or off-frame node whose reported bounds are outright fiction. locate.py cannot
help either -- it matches raw RGB, so a plate authored to be SCREENED (a light leak, a
lace overlay) has nothing to lock onto and scores over 80 wherever you put it.

    BODY_FRAME=<n> BODY_H=<h> python3 scripts/place_plate.py <node-id> <x0> <y0> <x1> <y1>

The four numbers are the SCORING BOX in frame-global design px, and giving one is the
whole point of this script. Two earlier cuts scored each candidate over its own moving
footprint, and both returned nonsense for every plate:

  - over a footprint clipped by the frame edge, a candidate pushed 90% off-frame is
    scored across a 20px sliver of flat ground and wins with a perfect 0.000;
  - over a footprint free to move, the cheapest thing a layer can do is land on ground
    the rest of the band already renders correctly and fade to 0.12, which is what all
    three light-leak plates returned. Scoring the layer's CONTRIBUTION instead of its
    absolute error does not fix this: a near-invisible plate still contributes a small
    negative, and that beats a correctly placed plate whose shape is not yet perfect.

A box that does not move removes both. Pick one over the area the layer is supposed to
explain -- the card it washes, the panel it edges -- and every candidate is measured on
the same pixels. The "without the layer" number printed first is the bar to beat; a
placement that does not clearly beat it is not a placement.

Search bounds default to the box grown by MARGIN and the asset's own size. EXTRA
overrides where other layers sit, for placing several plates that overlap in sequence:

    EXTRA='{"<other-node>":[x,y]}' python3 scripts/place_plate.py <node-id> ...

Nothing is written. Put what it finds in gen_band.py's PIN_X / PIN_Y (and solve_alpha's
NO_SOLVE, so the refiner cannot walk it back) once you have looked at the crop.
"""
import json
import os
import sys

from PIL import Image, ImageChops

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import solve_alpha as S  # noqa: E402  -- reuses its ground, mask, blend and paste

Image.MAX_IMAGE_PIXELS = None

if len(sys.argv) < 6:
    sys.exit(__doc__)
NID = sys.argv[1]
BX0, BY0, BX1, BY1 = (int(v) for v in sys.argv[2:6])
# How far outside the scoring box a candidate may sit. A plate usually overhangs the
# thing it explains, so the default is generous; narrow it when the search wanders.
MARGIN = int(os.environ.get("MARGIN", "260"))
# A full-width plate has almost no horizontal freedom -- frame-wide in a frame -- and
# giving it 260px of it turns a 3-minute search into a 30-minute one for no gain.
X_MARGIN = int(os.environ.get("X_MARGIN", str(MARGIN)))
EXTRA = json.loads(os.environ.get("EXTRA", "{}"))
STEP = int(os.environ.get("STEP", "4"))
# Coarse position runs on a handful of paint settings, not all 40. Full strength and
# something near half, in the three modes a leak or an overlay is plausibly authored in:
# the point of the coarse pass is to find the SHAPE, and shape does not move with alpha.
COARSE_PAINT = [(a, m) for m in ("normal", "screen", "lighten") for a in (1.0, 0.4)]
# PAINT="1.0:normal" fixes the paint and searches position only. Use it for a plate that
# is plainly a solid object rather than a light effect: a thin pale ornament on cream
# moves the score by less than the noise elsewhere in any box big enough to contain it,
# and a free alpha then "wins" by picking `darken`, which renders it invisible. Fixing
# the paint makes the search answer the only question actually in doubt.
PAINT = os.environ.get("PAINT")
# Figma exports a rotated node's art UNROTATED -- a necklace draped at -35 degrees in the
# render exports as an upright one. No translation can match that, and the search just
# reports a tiny gain wherever it lands.
# ROT="-60:60:5" searches rotation as a third axis; the winning angle goes in gen_band's
# PIN_R and comes out as a CSS rotate on the layer.
ROT = os.environ.get("ROT")


def main():
    ref = Image.open(S.REF).convert("RGB")
    alphas = json.load(open(S.ALPHA_FILE)) if os.path.exists(S.ALPHA_FILE) else {}
    blends = json.load(open(S.BLEND_FILE)) if os.path.exists(S.BLEND_FILE) else {}
    layers = S.all_layers()

    zorder = {c["id"]: c for c in
              json.load(open(f".figma-ref/frame{S.FRAME}-zorder.json"))["children"]}
    assets = json.load(open(f".figma-ref/frame{S.FRAME}-assets.json"))["nodes"]

    def raw(nid):
        c = zorder[nid]
        return dict(id=nid, asset=assets[nid]["asset"],
                    x=round(c["x"]), y=round(c["y"]), w=c["w"], h=c["h"])

    # EXTRA may name a layer that is not in any table -- placing a plate and then the
    # ornament that drapes over it means injecting the plate, which PAINTS_NOTHING drops.
    # Without this the "without the layer" baseline silently ignores the EXTRA entry and
    # every candidate is scored against a composite missing the thing it overlaps.
    have = {r["id"] for r in layers}
    for nid in EXTRA:
        if nid not in have and nid in zorder and nid in assets:
            layers = layers + [raw(nid)]

    row = next((r for r in layers if r["id"] == NID), None)
    if row is None:
        # gen_band.py's PAINTS_NOTHING drops a layer from the tables outright, and an
        # entry there often turns out to be a layer that measured as invisible only
        # because it was measured where its fictional bounds put it -- which is the exact
        # case this script is for.
        if NID not in zorder or NID not in assets:
            sys.exit(f"{NID} is in no band table and has no exported asset")
        row = raw(NID)
        print(f"({NID} is in no band table -- read from its raw node record)")

    im = S.load("src/assets/" + row["asset"])
    if ROT:
        lo, hi, st = (int(v) for v in ROT.split(":"))
        # expand=True so a rotated corner is not clipped; the origin shifts with it, which
        # is why the reported best x/y is the rotated art's own top-left, not the node's.
        angles = [(a, im.rotate(-a, Image.BICUBIC, expand=True)) for a in range(lo, hi + 1, st)]
    else:
        angles = [(0, im)]
    y0 = max(0, BY0 - MARGIN - im.height)
    y1 = min(S.FRAME_H, BY1 + MARGIN + im.height)
    target = ref.crop((0, y0, S.FRAME_W, y1))
    mask = S.text_mask(y0, y1)
    base = S.ground_for(y0, y1)
    for r in layers:
        if r["id"] == NID:
            continue
        # [x, y] or [x, y, alpha, mode] -- the paint matters when the override is a plate
        # whose solved alpha was fitted in the wrong place, which is every plate here.
        o = EXTRA.get(r["id"])
        x, y = (o[0], o[1]) if o else (r["x"], r["y"])
        a = o[2] if o and len(o) > 2 else r.get("a", 1.0)
        m = o[3] if o and len(o) > 3 else r.get("b", "normal")
        if y < y1 and y + r["h"] > y0 and a > 0:
            S.paste(base, S.load("src/assets/" + r["asset"]), x, y - y0, a, m)

    box = (BX0, BY0 - y0, BX1, BY1 - y0)
    area = (BX1 - BX0) * (BY1 - BY0)

    def score(x, y, a, mode, art=None):
        canvas = base.crop(box)
        S.paste(canvas, art if art is not None else im, x - BX0, y - BY0, a, mode)
        d = ImageChops.difference(target.crop(box), canvas.convert("RGB")).convert("L")
        d.paste(0, (0, 0), mask.crop(box))
        return sum(i * n for i, n in enumerate(d.histogram())) / area

    now = (row["x"], row["y"], row.get("a", 1.0), row.get("b", "normal"))
    print(f"without the layer            {score(-99999, -99999, 1.0, 'normal'):7.3f}")
    print(f"where it sits now  {now[0]},{now[1]}    {score(*now):7.3f}")

    xs = range(max(-im.width + 20, BX0 - X_MARGIN), min(S.FRAME_W - 20, BX1 + X_MARGIN), STEP)
    ys = range(y0, min(y1 - 20, BY1 + MARGIN), STEP)
    best = None
    coarse = [tuple(PAINT.split(":")) for _ in (0,)] if PAINT else COARSE_PAINT
    if PAINT:
        coarse = [(float(PAINT.split(":")[0]), PAINT.split(":")[1])]
    for a, mode in coarse:
        for rot, art in angles:
            for y in ys:
                for x in xs:
                    v = score(x, y, a, mode, art)
                    if best is None or v < best[0]:
                        best = (v, x, y, a, mode, rot)
    v, bx, by, ba, bm, brot = best
    art = dict(angles)[brot]
    print(f"coarse             {bx},{by} a{ba} {bm:9} rot {brot:4}  {v:7.3f}")
    # Paint at the position the shape found, then position again at that paint.
    for mode in ([bm] if PAINT else S.MODES):
        for a in ([ba] if PAINT else S.LADDER):
            if a == 0.0:
                continue
            t = score(bx, by, a, mode, art)
            if t < v:
                v, ba, bm = t, a, mode
    for y in range(by - STEP * 2, by + STEP * 2 + 1):
        for x in range(bx - STEP * 2, bx + STEP * 2 + 1):
            t = score(x, y, ba, bm, art)
            if t < v:
                v, bx, by = t, x, y
    print(f"best               {bx},{by} a{ba} {bm:9} rot {brot:4}  {v:7.3f}"
          f"   (art {art.width}x{art.height})")


main()
