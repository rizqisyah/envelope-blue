#!/usr/bin/env python3
"""Generate one placement table per band of the body frame.

Which frame it reads is env-driven, because every template cuts different frames:

    BODY_FRAME=<n> BODY_H=<h> python3 scripts/gen_band.py

Same job the cover's `coverLayers.ts` does, done for all bands at once.
Two things make this more than a coordinate dump:

1. Figma's reported bounds and the size it actually exports disagree in both
   directions -- see "exported bounds are not node bounds" in SLICING.md. Every
   layer is reconciled per axis against the real export, then template-matched
   against the 1x frame render, and the match wins wherever it fires.

2. Bands overlap. `section` in frame<N>-zorder.json is derived from heading
   positions, so one band's art regularly runs past the next band's top. A band's
   height is therefore the distance to the NEXT band's top, not the extent of
   its own children -- children that overrun simply paint past the boundary,
   which is what the design does anyway. `z` stays the global Figma child order
   so cross-band stacking survives the split.

    python3 scripts/gen_band.py            # every band
    python3 scripts/gen_band.py hero quote # just these

Writes src/lib/bands/<section>.ts and prints a per-band summary.
"""
import hashlib
import json
import os
import pathlib
import sys

from PIL import Image

FRAME = os.environ.get("BODY_FRAME", "")
if not FRAME:
    sys.exit("set BODY_FRAME=<body frame number, e.g. 244>")

os.environ.setdefault("LOCATE_REF", f".figma-tmp/exports{FRAME}/frame{FRAME}-full.png")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import locate  # noqa: E402  -- must follow the LOCATE_REF default above

FRAME_W = int(os.environ.get("FRAME_W", "596"))
# The sheet height is the one number no default can guess -- it is per design.
FRAME_H = int(os.environ.get("BODY_H", "0"))
if not FRAME_H:
    sys.exit("set BODY_H=<body frame height in design px>")
SCALE = 2
GOOD_ERR = 40.0  # locate.py: above this an asset is not visible at that spot
# A full-width rescue is a search over the whole frame, so it will always find SOME
# least-bad spot. Overriding the clip rule on that needs locate.py's stronger bar --
# "under ~15 is a real match" -- or it moves layers the clip rule had right. At 40 it
# took hero from 4.32 to 9.20 and quote from 4.00 to 8.83.
SURE_ERR = 15.0
# A node whose reported box barely overlaps the frame is a rotated or mirrored copy whose
# bounds are fiction -- Figma still exported pixels for it, so it renders SOMEWHERE. The
# clip rule cannot help (the export was not clipped, so neither reconcile branch fires)
# and `locate` never fires either, because a hint outside the frame has nothing to match.
# Below this fraction on-frame, search the full width at the reported y instead.
ON_FRAME_MIN = 0.25
OUT_DIR = pathlib.Path("src/lib/bands")

# Every table below is PER DESIGN and starts EMPTY. Each entry is a hand measurement
# against this design's own render, and each needs a before/after delta for that node
# alone -- layers that share a source asset look like a set and usually are not.
# ../slicing-wedding-template-5/scripts/gen_band.py carries a worked set of all of them,
# with the evidence for every entry, if the shape of one is unclear.

# Rotated nodes whose reported bounds are fiction AND which no position in the frame
# matches. They are buried in the design, so drawing them anywhere paints an artifact the
# render does not have. Dropping merely-occluded layers instead is measurably WORSE:
# `locate.py` scores over all of a layer's opaque pixels, so a buried layer scores badly
# exactly where it belongs, and a high err on an overlapped layer is evidence of nothing.
# Never add a node measured at its reported bounds when those bounds are the fiction --
# place it with scripts/place_plate.py first, then decide.
PAINTS_NOTHING = set()

# Layers where the clip rule is right and the search is wrong. A layer buried under most
# of its band scores badly WHERE IT BELONGS, so the search wanders off to open ground and
# wins on points while being visibly wrong. Flat-colour plates are the usual case: cream
# matches cream anywhere. Same evidence bar as PAINTS_NOTHING.
TRUST_CLIP = set()

# Hand-measured positions, applied AFTER the reconcile chain and after solve_alpha's own
# search, because they are measured against the render and those are not. The two cases
# that land here: a node bleeding past BOTH edges (the clip rule guesses one edge and
# pins it to the wrong side, stacking it on its own mirror), and a rotated node whose
# reported box is off-frame entirely. Use scripts/place_plate.py, with a FIXED scoring
# box over the thing the layer is supposed to explain.
# 15:192 is the right-edge calla lily. Its export grew (a blur), so the re-centre rule
# put it at x 545; solve_alpha then "improved" that by sliding it to 565 and fading it to
# 0.12 multiply -- i.e. by deleting a flower the render plainly draws, which is exactly
# the failure the gain gates exist to prevent and did not catch here. A fine scan over
# x 440..530, y 585..615 has a sharp, unambiguous minimum at (471, 600): 52.55 there
# against 57.38 one pixel right. Its mirror twin 15:190 scans the same way to (29, 600),
# which gen_band already had. The absolute error is high on both because the asset is a
# white lily on the near-white portrait wash -- a sharp minimum, not a low one, is the
# evidence here.
PIN_X = {'15:192': 471}
PIN_Y = {'15:192': 600}

# Opacity and blend mode for the layers whose POSITION is pinned above. solve_alpha
# fitted their alpha against a composite in which they sat hundreds of pixels from home,
# and the only way to make a plate in the wrong place score well is to fade it out. Add
# the same ids to solve_alpha's NO_SOLVE so the next run does not refit them.
# 15:192's alpha came from fitting it 94px from home, where the only way to score is to
# fade out. At its measured position it paints at full strength, stacked normally.
PIN_A = {'15:192': 1.0}
PIN_B = {'15:192': 'normal'}

# A layer paints in the band its own y lands in, not the band Figma filed it under.
# Left in the wrong band it renders fine and REVEALS wrong: useReveal gates a band's
# layers on THAT band scrolling in, so the layer fades up with a band elsewhere on
# the page. Keyed id -> band name.
BAND_OF = {}


def reconcile(pos, node_size, exp_size, frame_size):
    """Reconcile one axis of a Figma node against the size Figma actually exported."""
    if exp_size > node_size:
        # Export grew: a blur or a rotation widened the render bbox, and Figma
        # grows it around the node's centre, so re-centre rather than pin the corner.
        return round(pos + node_size / 2 - exp_size / 2)
    if exp_size < node_size:
        # Export shrank: Figma clipped it at the frame edge the node bleeds past.
        if pos < 0:
            return 0
        if pos + node_size > frame_size:
            return frame_size - exp_size
    return round(pos)


def _scorer(path):
    """Return (score_fn, asset_w, asset_h) for matching this asset against the render."""
    im = locate.load_asset(path)
    pts = locate.opaque_points(im, 400)
    if not pts:
        return None, 0, 0
    ref = Image.open(locate.REF).convert("RGB")
    rp = ref.load()

    def score(ox, oy):
        if ox < 0 or oy < 0 or ox + im.width > ref.width or oy + im.height > ref.height:
            return float("inf")
        return sum(
            abs(rp[x + ox, y + oy][0] - r)
            + abs(rp[x + ox, y + oy][1] - g)
            + abs(rp[x + ox, y + oy][2] - b)
            for x, y, (r, g, b) in pts
        ) / len(pts)

    return score, im.width, im.height


def rescue(path, hint_y, span=700, step=8):
    """Search the whole frame width for a layer whose reported box is off-frame.

    A node reported wholly outside the frame (FRAME_W px) is rotated, so its bounds are
    fiction -- but Figma still exported pixels for it, which means it renders
    SOMEWHERE. Most are mirrored decorations that land back inside the frame.
    A few are buried under later layers and never show at all; those must be
    dropped, or we paint something the design does not.

    Returns (x, y, err) for the best position within +/-span of the reported y.
    """
    score, aw, ah = _scorer(path)
    if score is None:
        return None
    ref = Image.open(locate.REF)
    im = type("S", (), {"width": aw, "height": ah})

    y_lo = max(0, hint_y - span)
    y_hi = min(ref.height - im.height, hint_y + span)
    x_hi = ref.width - im.width
    if y_hi < y_lo or x_hi < 0:
        return None
    best = min(
        (score(ox, oy), ox, oy)
        for oy in range(y_lo, y_hi + 1, step)
        for ox in range(0, x_hi + 1, step)
    )
    err, bx, by = best
    for oy in range(max(y_lo, by - step), min(y_hi, by + step) + 1):
        for ox in range(max(0, bx - step), min(x_hi, bx + step) + 1):
            sc = score(ox, oy)
            if sc < err:
                err, bx, by = sc, ox, oy
    return bx, by, err


def band_tops(children):
    """Band top = its first child's y; band height runs to the next band's top."""
    firsts = {}
    for c in children:
        s = c["section"]
        firsts[s] = min(firsts.get(s, c["y"]), c["y"])
    ordered = sorted(firsts.items(), key=lambda kv: kv[1])
    # The sheet must start at the frame's top edge. The first band's first child can sit
    # below y0 -- these frames usually do -- and honouring that would open a gap above
    # the first band that the design does not have.
    if ordered:
        ordered[0] = (ordered[0][0], 0)
    # Round the tops FIRST, then derive each height from the next rounded top. Rounding
    # top and height independently leaves a 1px seam between bands wherever both round
    # the same way, and the sheet ends up short of FRAME_H.
    ordered = [(name, round(top)) for name, top in ordered]
    spans = {}
    for i, (name, top) in enumerate(ordered):
        nxt = ordered[i + 1][1] if i + 1 < len(ordered) else FRAME_H
        spans[name] = (top, nxt - top)
    return spans, [name for name, _ in ordered]


def main():
    # scripts/solve_alpha.py's output: the opacity Figma's MCP never reports, and the
    # residual offset the clip/re-centre/locate chain could not reach. Both are optional
    # -- an unsolved frame just generates at full opacity and no nudge.
    alpha_path = pathlib.Path(f".figma-ref/frame{FRAME}-alpha.json")
    place_path = pathlib.Path(f".figma-ref/frame{FRAME}-place.json")
    blend_path = pathlib.Path(f".figma-ref/frame{FRAME}-blend.json")
    ALPHA = json.load(alpha_path.open()) if alpha_path.exists() else {}
    PLACE = json.load(place_path.open()) if place_path.exists() else {}
    BLEND = json.load(blend_path.open()) if blend_path.exists() else {}

    zorder = json.load(open(f".figma-ref/frame{FRAME}-zorder.json"))
    children = zorder["children"] if isinstance(zorder, dict) else zorder
    assets = json.load(open(f".figma-ref/frame{FRAME}-assets.json"))["nodes"]

    # A sprite used by more than one node cannot be template-matched: every copy scores
    # the same at every other copy's slot, and `locate` happily reports card 1's plate at
    # card 2's position. Their reported bounds are already right -- trust them.
    # Keyed on the file's BYTES, not its path: Figma exports each repeated node
    # separately, so identical plates are different .webp files with identical content.
    # Hashing is what actually finds them.
    used = {}
    for nid, a in assets.items():
        f = pathlib.Path("src/assets/" + a["asset"])
        if f.exists():
            used.setdefault(hashlib.md5(f.read_bytes()).hexdigest(), []).append(nid)
    twins = {nid for ids in used.values() if len(ids) > 1 for nid in ids}

    spans, order = band_tops(children)
    wanted = sys.argv[1:] or order
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for name in wanted:
        if name not in spans:
            print(f"!! no such band: {name}")
            continue
        top, height = spans[name]
        rows, matched, dropped = [], 0, []

        for c in children:
            if BAND_OF.get(c["id"], c["section"]) != name:
                continue
            if c["id"] in PAINTS_NOTHING:
                dropped.append(f"{c['id']} (z{c['z']}, buried in the design)")
                continue
            a = assets.get(c["id"])
            if not a:
                continue  # TEXT, dropped empty, or a group we walked into
            path = f"src/assets/{a['asset']}"
            if not pathlib.Path(path).exists():
                print(f"!! missing asset for {c['id']}: {path}")
                continue
            im = Image.open(path)
            scale = a.get("assetScale", SCALE)
            w, h = im.width // scale, im.height // scale

            # Fraction of the NODE that overlaps the frame -- against c["w"], never the
            # export width. A blurred or rotated node exports far wider than it claims,
            # and dividing by that understated every such node into a false rescue: the
            # gift band went 5.4 -> 25.3 the one time this read `w`.
            on_frame = max(0.0, min(c["x"] + c["w"], FRAME_W) - max(c["x"], 0)) / max(1.0, c["w"])
            found, err = (None, None)
            if c["id"] not in twins:
                found, err = locate.locate(path, max(0, round(c["x"])), max(0, round(c["y"])))
            if found and found[4] < GOOD_ERR and c["id"] not in TRUST_CLIP:
                x, y = found[0], found[1]
                matched += 1
            elif on_frame < ON_FRAME_MIN and c["id"] not in TRUST_CLIP and c["id"] not in twins:
                # Taken unconditionally, unlike the rescue below: where the reported box
                # puts this layer it is invisible, so ANY match inside the frame is better
                # evidence than bounds that place it off the edge. The error is still
                # meaningless on an occluded layer -- a buried floral scores ~80 where it
                # belongs, the same as it scores anywhere else.
                hit = rescue(path, max(0, round(c["y"])), span=60, step=4)
                if hit:
                    x, y = hit[0], hit[1]
                    matched += 1
                else:
                    x = reconcile(c["x"], c["w"], w, FRAME_W)
                    y = reconcile(c["y"], c["h"], h, FRAME_H)
            elif w < round(c["w"]) or h < round(c["h"]):
                # Figma clipped this export, which means the node bleeds off an edge --
                # and a bleeding node in this file is usually a rotated one, whose
                # reported position is fiction. The clip rule can only guess which edge
                # cut it; the render knows.
                cx = reconcile(c["x"], c["w"], w, FRAME_W)
                cy = reconcile(c["y"], c["h"], h, FRAME_H)
                hit = rescue(path, max(0, round(c["y"])))
                score, _, _ = _scorer(path)
                clip_err = score(cx, cy) if score else float("inf")
                # A full-width search always finds SOME least-bad spot, and for a big
                # mostly-transparent layer that spot is often nowhere near the truth.
                # It has to beat where the clip rule already put it, clearly.
                if (
                    hit
                    and c["id"] not in TRUST_CLIP
                    and hit[2] < SURE_ERR
                    and hit[2] < clip_err - 3
                ):
                    x, y = hit[0], hit[1]
                    matched += 1
                else:
                    # A high error here means occluded OR absent -- locate.py cannot tell
                    # them apart, and guessing "absent" and dropping the layer measurably
                    # hurt the render. Fall through to the clip rule; only the layers in
                    # PAINTS_NOTHING below are actually dropped.
                    x = reconcile(c["x"], c["w"], w, FRAME_W)
                    y = reconcile(c["y"], c["h"], h, FRAME_H)
            else:
                x = reconcile(c["x"], c["w"], w, FRAME_W)
                y = reconcile(c["y"], c["h"], h, FRAME_H)
            x, y = PLACE.get(c["id"], (x, y))
            # PIN_X/PIN_Y last: they are hand-measured against the render, so they beat
            # both the reconcile chain and the solver's own search.
            x = PIN_X.get(c["id"], x)
            y = PIN_Y.get(c["id"], y)
            rows.append((c["z"], c["id"], a["asset"], x, y - top, w, h,
                         PIN_A.get(c["id"], ALPHA.get(c["id"], 1.0)),
                         PIN_B.get(c["id"], BLEND.get(c["id"], "normal"))))

        rows.sort(key=lambda r: r[0])
        if not rows:
            # A text-only band has no placement table to generate;
            # an empty module would just be an unused import.
            print(f"{name:10} y {top:5}..{top + height:5} h {height:5}  text-only, no table")
            (OUT_DIR / f"{name}.ts").unlink(missing_ok=True)
            continue
        body = f"""// Generated by scripts/gen_band.py — do not hand-edit.
// Figma Frame {FRAME} band "{name}": y {top}..{top + height}, height {height} design px.
// x/y are band-local design px; `z` is the GLOBAL Figma child order, so layers still
// stack correctly against the bands above and below this one.
//
// Positions are NOT Figma's reported bounds — see "exported bounds are not node bounds"
// in SLICING.md. Regenerate rather than nudging numbers by hand.
import type {{ BandLayer }} from '../bandLayer'

export const BAND_TOP = {top}
export const BAND_HEIGHT = {height}

export const LAYERS: BandLayer[] = [
"""
        for z, nid, asset, x, y, w, h, alpha, mode in rows:
            extra = "" if alpha == 1.0 else f", a: {alpha}"
            extra += "" if mode == "normal" else f", b: '{mode}'"
            body += (
                f"  {{ z: {z}, id: '{nid}', src: assets['{asset}'],"
                f" x: {x}, y: {y}, w: {w}, h: {h}{extra} }},\n"
            )
        body += "]\n"

        header = """import { assets } from '../bandAssets'

"""
        (OUT_DIR / f"{name}.ts").write_text(header + body)
        print(f"{name:10} y {top:5}..{top + height:5} h {height:5}  {len(rows):3} layers  {matched:3} matched")
        for d in dropped:
            print(f"           dropped: {d}")


if __name__ == "__main__":
    main()
