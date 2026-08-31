#!/usr/bin/env python3
"""Recover the per-layer opacity a band needs, by compositing it offline.

Figma's MCP reports a node's bounds and fills but not its `opacity` or `blendMode`,
so a layer the design fades to 20% comes out of `save_screenshots` at full strength
and paints a slab over the band. `gen_band.py` cannot see this — the position it
solves is right, the layer is simply too opaque.

So composite the band's rows offline, mask out every TEXT box (the composite carries
no live copy), and score against the frame render. Then, one layer at a time, try a
ladder of alphas plus dropping the layer entirely, and keep whatever lowers the error.

Two things make the composite match what the browser actually paints:

- **Bands overlap.** A layer belongs to one band but paints across the boundary, so
  the window is filled from EVERY band's table — anything whose box intersects these
  rows, in global `z` order — not just this band's own layers.
- **The sheet's ground is CSS, not a layer.** `GROUND` below is whatever flat plates
  InviteBody.vue paints under the bands; they are in no band table, so this script has
  to paint them itself. Fill it in from the sheet's own stylesheet -- an empty GROUND
  composites every band over black and every alpha comes back wrong.

    BODY_FRAME=<n> BODY_H=<h> python3 scripts/solve_alpha.py <band>
    BODY_FRAME=<n> BODY_H=<h> python3 scripts/solve_alpha.py            # every band

Writes -alpha / -place / -blend json beside the frame dumps, which gen_band.py reads
back. Positions are persisted ABSOLUTE, so this is idempotent: run it, regenerate, run
it again, and the second pass refines the first instead of doubling it. Two or three
passes converge -- the search is greedy and per-layer, so a layer solved early is worth
revisiting once its neighbours have moved.
"""
import hashlib
import json
import os
import re
import sys

from PIL import Image, ImageChops, ImageDraw

Image.MAX_IMAGE_PIXELS = None

FRAME = os.environ.get("BODY_FRAME", "")
if not FRAME:
    sys.exit("set BODY_FRAME=<body frame number, e.g. 253 for template 5>")
FRAME_H = int(os.environ.get("BODY_H", "0"))
if not FRAME_H:
    sys.exit("set BODY_H=<body frame height in design px>")

REF = os.environ.get("LOCATE_REF") or f".figma-tmp/exports{FRAME}/frame{FRAME}-full.png"
ALPHA_FILE = f".figma-ref/frame{FRAME}-alpha.json"
PLACE_FILE = f".figma-ref/frame{FRAME}-place.json"
BLEND_FILE = f".figma-ref/frame{FRAME}-blend.json"
FRAME_W = int(os.environ.get("FRAME_W", "596"))  # this template's frame, not the 375 of 2-5
SCALE = 2
# The CSS plates in InviteBody.vue: (top, bottom, colour), painted in this order.
# PER DESIGN -- read them off the sheet's own stylesheet, e.g.
# [(0, FRAME_H, (247, 248, 238)), (0, 3881, (83, 9, 21))] for a cream sheet with a
# wine block over its top half.
# Frame 1 paints one flat ground: the frame's OWN fill, #e7f9fe. Note this is not
# --paper (#e9faff) -- that was sampled off the cover frame, and the two differ by a
# couple of counts per channel. Compositing over the cover's value biases every alpha.
GROUND = [(0, FRAME_H, (231, 249, 254))]
if not GROUND:
    sys.exit("fill in GROUND from InviteBody.vue's CSS plates -- see the docstring")
# 1.0 first so a layer that is already right is never traded for a marginal gain.
LADDER = [1.0, 0.85, 0.7, 0.55, 0.4, 0.3, 0.2, 0.12, 0.0]
# Below this the change is inside the noise of a lossy webp and a substitute font.
# Deliberately blunt: the search is free to move a layer 40px and fade it to nothing, and
# on a busy band there is almost always SOME such move that shaves a hundredth off the
# score while being visibly wrong. A gain has to be worth seeing before it is kept.
MIN_GAIN = 0.30
MOVE_GAIN = 0.50
# Dropping a layer outright is the one move that cannot be recovered from by eye later,
# so it has to pay for itself several times over.
DROP_GAIN = 2.00
# A layer smaller than this matches anywhere -- a 9px dot scores the same on any patch of
# its own colour -- so its Figma bounds are better evidence than any search. Same trap as
# gen_band.py's TRUST_CLIP, one size class down.
MIN_SOLVE = 24
# A move has to pay for itself in proportion to how far it is. A 4px nudge on a layer the
# clip rule nearly had is cheap to believe; a 40px jump on a big soft plate is the search
# finding a false minimum, and the flat gate alone let it move a band's card tabs a whole
# slot down. dist * this, added to MOVE_GAIN.
MOVE_GAIN_PER_PX = 0.015
# Half-window, design px, for the position refinement.
SEARCH = 40
# Light-leak plates are authored to blend, not to stack.
# Figma's MCP does not report blendMode either, so it is solved the same way as alpha.
MODES = ["normal", "screen", "multiply", "lighten", "darken"]

# Layers whose paint is settled by hand and must not be re-solved. gen_band.py's PIN_X /
# PIN_Y already protect their POSITION (pins are applied after PLACE), but nothing
# protects their alpha, and a hand-placed layer is exactly the kind the solver got wrong
# in the first place: a big plate sitting 200px from home is only made to score by fading
# it to nothing. Every id pinned in gen_band.py belongs here too. Per design, starts empty.
# 15:192 -- hand-measured in gen_band.py's PIN_X/PIN_Y. Left solvable, the search
# refits it 94px away at 0.12 multiply and the lily disappears.
NO_SOLVE = {'15:192', '16:397', '16:491', '16:493'}

# No closing brace in the pattern: gen_band appends `, a: ...` and `, b: '...'` to any
# row this script has already solved, and anchoring on `h: N }` silently dropped every
# such row from all_layers() on the SECOND run -- the composite then had a hole exactly
# where the solved plates are, and the solver refit its neighbours against it.
ROW = re.compile(
    r"\{ z: (\d+), id: '([^']+)', src: assets\['([^']+)'\], "
    r"x: (-?[\d.]+), y: (-?[\d.]+), w: ([\d.]+), h: ([\d.]+)"
    r"(?:, a: ([\d.]+))?(?:, b: '([a-z]+)')?"
)


def all_layers():
    """Every band's table, flattened to sheet-global y and sorted by global z."""
    rows = []
    for f in sorted(os.listdir("src/lib/bands")):
        if not f.endswith(".ts"):
            continue
        src = open("src/lib/bands/" + f).read()
        top = int(re.search(r"BAND_TOP = (\d+)", src).group(1))
        for z, i, a, x, y, w, h, alpha, blend in ROW.findall(src):
            # The generated table, not the solver's own JSON, is what the browser renders
            # -- gen_band.py's PIN_A / PIN_B override the JSON on the way out, so reading
            # the JSON back composites a plate at an opacity nothing on the page uses.
            rows.append(dict(z=int(z), id=i, asset=a, band=f[:-3],
                             x=round(float(x)), y=round(float(y)) + top,
                             w=float(w), h=float(h),
                             a=float(alpha) if alpha else 1.0,
                             b=blend or "normal"))
    rows.sort(key=lambda r: r["z"])
    return rows


def band_spans():
    spans = {}
    for f in sorted(os.listdir("src/lib/bands")):
        if not f.endswith(".ts"):
            continue
        src = open("src/lib/bands/" + f).read()
        spans[f[:-3]] = (int(re.search(r"BAND_TOP = (\d+)", src).group(1)),
                         int(re.search(r"BAND_HEIGHT = (\d+)", src).group(1)))
    return spans


def load(path):
    im = Image.open(path).convert("RGBA")
    return im.resize((max(1, im.width // SCALE), max(1, im.height // SCALE)), Image.LANCZOS)


def blend_pixels(base, src, mode):
    """CSS blend modes, on two RGB images of the same size."""
    if mode == "screen":
        return ImageChops.screen(base, src)
    if mode == "multiply":
        return ImageChops.multiply(base, src)
    if mode == "lighten":
        return ImageChops.lighter(base, src)
    if mode == "darken":
        return ImageChops.darker(base, src)
    return src


def paste(canvas, im, x, y, alpha, mode="normal"):
    """Composite onto the window, cropping whatever hangs off any edge."""
    if alpha <= 0:
        return
    if alpha < 1:
        im = im.copy()
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    cx, cy = max(0, -x), max(0, -y)
    if cx >= im.width or cy >= im.height:
        return
    px, py = x + cx, y + cy
    if px >= canvas.width or py >= canvas.height:
        return
    piece = im.crop(
        (cx, cy, min(im.width, cx + canvas.width - px), min(im.height, cy + canvas.height - py))
    )
    if mode == "normal":
        canvas.alpha_composite(piece, (px, py))
        return
    # Blend against what is already on the canvas, then composite the result back
    # through the source alpha -- which is how mix-blend-mode behaves in the browser.
    box = (px, py, px + piece.width, py + piece.height)
    under = canvas.crop(box).convert("RGB")
    mixed = blend_pixels(under, piece.convert("RGB"), mode)
    mixed = mixed.convert("RGBA")
    mixed.putalpha(piece.getchannel("A"))
    canvas.alpha_composite(mixed, (px, py))


def text_mask(y0, y1):
    """White where the render carries live copy the composite cannot draw."""
    mask = Image.new("L", (FRAME_W, y1 - y0), 0)
    d = ImageDraw.Draw(mask)
    for c in json.load(open(f".figma-ref/frame{FRAME}-zorder.json"))["children"]:
        if c["type"] not in ("TEXT", "TEXT_PATH"):
            continue
        # 4px of slack: several faces overshoot their Figma box by a pixel or two.
        d.rectangle([c["x"] - 4, c["y"] - y0 - 4, c["x"] + c["w"] + 4, c["y"] - y0 + c["h"] + 4],
                    fill=255)
    return mask


def ground_for(y0, y1):
    g = Image.new("RGBA", (FRAME_W, y1 - y0), (0, 0, 0, 255))
    d = ImageDraw.Draw(g)
    for top, bot, colour in GROUND:
        if bot <= y0 or top >= y1:
            continue
        d.rectangle([0, max(top, y0) - y0, FRAME_W, min(bot, y1) - y0 - 1], fill=colour + (255,))
    return g


def main():
    ref = Image.open(REF).convert("RGB")
    alphas = json.load(open(ALPHA_FILE)) if os.path.exists(ALPHA_FILE) else {}
    place = json.load(open(PLACE_FILE)) if os.path.exists(PLACE_FILE) else {}
    blends = json.load(open(BLEND_FILE)) if os.path.exists(BLEND_FILE) else {}
    spans = band_spans()
    layers = all_layers()
    # Keyed on the file's BYTES, not its path: Figma exports each node separately, so the
    # gift band's three identical plates are three different .webp files with identical
    # content. Hashing is what actually finds them.
    seen = {}
    for r in layers:
        seen.setdefault(hashlib.md5(open("src/assets/" + r["asset"], "rb").read()).hexdigest(),
                        []).append(r["id"])
    twins = {i for ids in seen.values() if len(ids) > 1 for i in ids}
    bands = sys.argv[1:] or sorted(spans)

    for band in bands:
        top, height = spans[band]
        y0, y1 = top, top + height
        window = [r for r in layers if r["y"] < y1 and r["y"] + r["h"] > y0]
        target = ref.crop((0, y0, FRAME_W, y1))
        mask = text_mask(y0, y1)
        images = {r["id"]: load("src/assets/" + r["asset"]) for r in window}
        base_ground = ground_for(y0, y1)

        def score(trial):
            canvas = base_ground.copy()
            for r in window:
                paste(canvas, images[r["id"]], r["x"], r["y"] - y0, trial.get(r["id"], 1.0))
            d = ImageChops.difference(target, canvas.convert("RGB")).convert("L")
            d.paste(0, (0, 0), mask)
            return sum(i * n for i, n in enumerate(d.histogram())) / (FRAME_W * height)

        trial = {r["id"]: r["a"] for r in window}
        # Offsets are relative to whatever the table already holds, and the solved
        # ABSOLUTE position is what gets persisted -- so re-running is idempotent
        # rather than applying the same nudge on top of itself.
        offs = {r["id"]: (0, 0) for r in window}
        modes = {r["id"]: r["b"] for r in window}
        idx = {r["id"]: n for n, r in enumerate(window)}

        def compose(canvas, rows, trial, offs, modes, x0, y0w):
            for r in rows:
                dx, dy = offs.get(r["id"], (0, 0))
                paste(canvas, images[r["id"]], r["x"] + dx - x0, r["y"] + dy - y0 - y0w,
                      trial.get(r["id"], 1.0), modes.get(r["id"], "normal"))

        def score(trial, offs, modes, box=None):
            """Mean abs delta over `box` (window-local x0,y0,x1,y1), text masked out."""
            x0, ya, x1, yb = box or (0, 0, FRAME_W, height)
            canvas = base_ground.crop((x0, ya, x1, yb))
            compose(canvas, window, trial, offs, modes, x0, ya)
            d = ImageChops.difference(target.crop((x0, ya, x1, yb)),
                                      canvas.convert("RGB")).convert("L")
            d.paste(0, (0, 0), mask.crop((x0, ya, x1, yb)))
            return sum(i * n for i, n in enumerate(d.histogram())) / ((x1 - x0) * (yb - ya))

        base = score(trial, offs, modes)
        start = base
        # Only this band's own layers are solved here; a neighbour's overrun is solved
        # when that band's turn comes, against its own rows.
        for r in [r for r in window if r["band"] == band]:
            im = images[r["id"]]
            if im.width < MIN_SOLVE or im.height < MIN_SOLVE:
                continue
            if r["id"] in NO_SOLVE:
                continue
            if r["id"] in twins:
                # Repeated sprite: the gift band draws the same card plate three times,
                # 119px apart. The search cannot tell one copy from another, so it will
                # happily slide card 1's tab into card 2's slot and score the same. Their
                # Figma positions are already right -- leave them alone.
                continue
            # Score over what this layer can reach, plus the search margin — a 40x40
            # floral scored across the whole band is drowned out by everything else.
            box = (max(0, r["x"] - SEARCH), max(0, r["y"] - y0 - SEARCH),
                   min(FRAME_W, r["x"] + im.width + SEARCH),
                   min(height, r["y"] - y0 + im.height + SEARCH))
            if box[2] <= box[0] or box[3] <= box[1]:
                continue
            local = score(trial, offs, modes, box)
            best = [local, offs[r["id"]], trial[r["id"]], modes[r["id"]]]
            # Position first: an offset layer scores badly at every alpha, and the
            # ladder would then "fix" it by fading it out of the band entirely.
            def refine_position():
                for step in (4, 1):
                    cx, cy = best[1]
                    span = SEARCH if step == 4 else step * 6
                    for dy in range(cy - span, cy + span + 1, step):
                        for dx in range(cx - span, cx + span + 1, step):
                            s_ = score(trial, dict(offs, **{r["id"]: (dx, dy)}), modes, box)
                            dist = max(abs(dx), abs(dy))
                            if s_ < best[0] - MOVE_GAIN - dist * MOVE_GAIN_PER_PX:
                                best[0], best[1] = s_, (dx, dy)
                    offs[r["id"]] = best[1]

            def refine_paint():
                """Blend mode and opacity together — they trade off, so a greedy pass over
                one then the other settles for whichever it happened to try first."""
                for m in MODES:
                    for a in LADDER:
                        if (m, a) == (best[3], best[2]):
                            continue
                        s_ = score(dict(trial, **{r["id"]: a}), offs,
                                   dict(modes, **{r["id"]: m}), box)
                        gate = DROP_GAIN if a == 0.0 else MIN_GAIN
                        if s_ < best[0] - gate:
                            best[0], best[2], best[3] = s_, a, m
                trial[r["id"]], modes[r["id"]] = best[2], best[3]

            # Position first, then paint, then position again: a layer in the wrong place
            # scores badly at every alpha, and solving paint first "fixes" that by fading
            # the layer out of the band entirely. Solving position first against a plate
            # that should be screened has the mirror problem, so both get a second look.
            refine_position()
            refine_paint()
            refine_position()
            refine_paint()
            trial[r["id"]], offs[r["id"]], modes[r["id"]] = best[2], best[1], best[3]
            if best[1] != (0, 0) or best[2] != 1.0 or best[3] != "normal":
                print(f"  {r['id']:12} d{best[1]}  alpha {best[2]:.2f}  {best[3]:9}"
                      f" local {local:.2f} -> {best[0]:.2f}")
            alphas[r["id"]] = trial[r["id"]]
            place[r["id"]] = [r["x"] + offs[r["id"]][0], r["y"] + offs[r["id"]][1]]
            blends[r["id"]] = modes[r["id"]]
        base = score(trial, offs, modes)
        print(f"{band:9} {start:7.3f} -> {base:7.3f}   ({len(window)} layers in window)")

    json.dump({k: v for k, v in sorted(alphas.items()) if v != 1.0},
              open(ALPHA_FILE, "w"), indent=1)
    json.dump(dict(sorted(place.items())), open(PLACE_FILE, "w"), indent=1)
    json.dump({k: v for k, v in sorted(blends.items()) if v != "normal"},
              open(BLEND_FILE, "w"), indent=1)
    print(f"wrote {ALPHA_FILE}, {PLACE_FILE} and {BLEND_FILE}")


if __name__ == "__main__":
    main()
