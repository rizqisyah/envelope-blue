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
PAINTS_NOTHING = {'24:916'}

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
# 16:397 and 16:493 are both cases the reconcile chain structurally cannot reach, and
# both were found by reading the EXPORT'S EDGE ALPHA rather than by any search:
#
#   16:397 declares x 116 w 191 -- inside the frame on both sides -- yet exports 116 wide.
#   reconcile() only clips a node whose REPORTED box bleeds, so neither branch fires and it
#   falls through to round(116). Its export's left column carries the plate's maximum alpha
#   (212) against 90 on the right: the ink is cut off flat at the left, so the node really
#   bleeds 75px past x 0 and its reported x is fiction. x -> 0. Its mirror 16:398 has the
#   profile the other way round (L 90, R 212) and its reported 480 is right.
#
#   16:493 reports x 739.8 -- wholly off-frame -- so it took the rescue path, which landed
#   it at 288 in open ground. Its final x and y are NOT from the edge-alpha rule: see the
#   ink-crop measurement under PIN_A below, which settles both it and its mirror 16:491.
#
# locate.py cannot settle either one: all three of 40:91, 16:397 and 16:398 have NO pixel
# above alpha 240, so opaque_points() returns nothing and every search scores them blind.
#
# 16:397 needs no PIN_A/PIN_B: once its x is right it paints at the default full strength,
# and the stale 0.2/screen the earlier pass had fitted for it is gone from frame1-alpha.json.
# Only the pair below needed their paint pinned as well as their position.
#
# 20:640 is the third instance of the 16:397 case, in the bride band: it declares x 52.8
# w 97.4 -- comfortably inside the frame on both sides -- and exports 53 wide, so no
# reconcile branch fires and it falls through to round(52.8). Its export's LEFT column
# carries the plate's maximum alpha (255) against 0 on the right, so the ink is cut off
# flat at the left and the node bleeds past x 0. Locating its own ink crop against the
# render independently returns x 0. -> 0.
# Its y comes from the same ink crop, which lands at 2776 -- nine px above where
# reconcile() re-centred it (2785). Cross-correlating the live band against the render
# over that flower alone agrees: dy +9 with a clear minimum. Growth is not symmetric.
#
# 20:589 is the bride's rose-and-magnolia bouquet. Its export grew 204x199 -> 285x285, so
# reconcile() re-centred BOTH axes; only the x was ever wrong. Its ink crop locates at
# ink 22,2483, i.e. layer origin 10,2413 -- and 2413 is Figma's own declared y, unrounded.
# The re-centre had put it at 104,2369, which paints the bouquet 94px right of home.
# Pinning it took the band 4.47 -> 3.11. A 1px scan afterwards has a sharp minimum one
# further left, so the final x is 9: 1.882 / 1.761 / 1.580 / 1.402 / 1.574 / 1.753 at
# x 6..11, and 1.734 / 1.439 / 1.402 / 1.716 at y 2411..2414. Both axes fall away on
# either side, which is the corroboration -- an ink crop gets within a pixel, not to it.
#
# 20:584 is the sweet-pea sprig hanging below that bouquet, and it is the case that
# needs BOTH rules at once: its export is clipped on one axis and grown on the other.
# 291 wide against a declared 342 with the left column at the plate's maximum alpha
# (254) and the right at 0 -- cut at the LEFT, so x -> 0; and 372 tall against a declared
# 253, grown downward, so its y is Figma's own 2389 rather than the 2330 the re-centre
# gives. Neither number is findable by search: a free search over the whole scene rates
# every position within 0.04 of not drawing it at all, because the sprig is 291x372 and
# the render only shows the ~140x140 of it that is not buried under the bouquet. Scoring
# a FIXED box over just that visible corner (place_plate.py, 0 2560 160 2720) separates
# them at once -- 14.13 without the layer, 7.41 at (0, 2389). Pick the box over what the
# layer is supposed to explain, not over the layer.
#
# The five groom pins are not measurements at all -- they are the BRIDE's, mirrored. The
# two scenes are an exact horizontal mirror: every paired export is the flip of its twin
# (`same` err 17..61 against `mirrored` err 3..9 across all eight same-size pairs), the y
# offset is +1002, and correlating the two scene crops puts the axis at x 294, i.e.
#
#     groom_x = 588 - bride_x - bride_w        groom_y = bride_y + 1002
#
# Nine of the fourteen pairs already agreed with that after the ordinary chain, including
# every clipped one, which is what makes the other five safe to pin rather than search.
# The band went 5.958 -> 1.516 on those five alone, and a 1px scan afterwards puts 20:626
# at a sharp minimum on the predicted 294 (1.914 / 1.702 / 1.478 / 1.678 / 1.903 at
# 292..296) -- the prediction is exact, not approximate.
#
# The reason the chain missed them is worth keeping: **Figma reports a mirrored node's
# bounds.x as its RIGHT edge.** 20:627 declares 333 for art 141 wide that renders at 192;
# 20:609 declares 433 for art 342 wide that renders at 91; 20:625 declares 679 for 183
# that renders at 496. Every one of those boxes is inside the frame, so no clip branch
# fires and the value falls straight through -- the same structural blind spot as 16:397,
# reached by a different route. When a band has a mirror, check the pairs before searching.
PIN_X = {'15:192': 471, '16:397': 0, '16:493': 396, '16:491': 0, '20:640': 0, '20:589': 9, '20:584': 0,
         '20:625': 496, '20:627': 192, '20:609': 91, '20:626': 294,
         '23:882': 101, '20:762': 73, '20:763': 433,
         '52:4': 0, '52:5': 419, '22:846': 0, '22:827': 419, '32:450': 0,
         '54:33': 63, '23:851': 63,
         '29:242': 24, '29:241': 62, '29:253': 146, '29:254': 0, '24:897': 0, '29:244': 0,
         '29:248': 0, '29:243': 456, '29:246': 429, '29:249': 0, '29:274': 0, '54:42': 62,
         '45:9': 0, '29:235': 10, '31:287': 78, '31:289': 152, '52:6': 17, '52:8': 293,
         '31:295': 146, '31:301': 255, '31:304': 364, '31:314': 140, '31:315': 457,
         '45:12': 0, '31:417': 0, '31:423': 0, '32:457': 0,
         '31:424': 0, '31:426': 488}
PIN_Y = {'15:192': 600, '16:493': 984, '16:491': 984, '20:589': 2413, '20:640': 2776, '20:584': 2389,
         '20:625': 3321, '20:611': 3391, '20:626': 3415,
         '23:882': 4071, '20:762': 4323, '20:763': 4329,
         '52:4': 4536, '52:5': 4536, '22:846': 4941, '22:827': 5412, '22:837': 5309,
         '54:33': 5618, '23:851': 5173,
         '29:242': 6207, '29:241': 6236, '29:253': 5907, '29:254': 6028, '24:897': 6081,
         '29:244': 6393, '29:248': 6541, '29:243': 6372, '29:246': 6004, '29:249': 6475,
         '29:274': 6004, '54:42': 6688,
         '29:235': 7750, '31:289': 8062, '52:6': 8155, '52:8': 8155,
         '31:295': 8478, '31:301': 8478, '31:304': 8478, '31:314': 8262, '31:315': 8262,
         '32:457': 9109, '31:424': 9664, '31:426': 9664}

# The gift band is the cleanest demonstration of the right-edge rule in the frame: every
# LEFT-side node declares its right edge and every RIGHT-side node declares its left one.
#
#   45:12  140.1 -> 0     45:11  460.1 stands   (280-wide pair)
#   31:417 225   -> 0     31:418 351   stands   (466-wide pair)
#   31:423 235   -> 0     31:422 361   stands   (466-wide pair)
#   32:457  78   -> 0     32:458 518   stands   (194-wide pair)
#   31:427 108   -> 0     31:428 488   stands   (194-wide pair)
#   31:419 -196  -> 0 (an ordinary left bleed) and 31:421 791 -> 417 (a mirrored one)
#
# Only four needed pinning; the clip rule guessed the right edge for the rest. 45:12,
# 31:417 and 31:423 each scored 210..214 where it put them against 39..140 at 0.
#
# 32:457 is a different trap: locate placed it at (30, 9250) with err 5.1 -- a REAL match,
# but of 31:427's copy of the same floral, which really is at (0, 9250). The four
# Photoroom crops in this band are near-identical without being byte-identical, so the
# twins guard never fires. Its own geometry (mirror bleed left, declared y) gives
# (0, 9109) at err 5.2, statistically the same score in the right place. When a band
# repeats a sprite, trust the geometry over locate even when locate is confident.

# The gallery band. Its photos are the useful find: **a masked photo exports ALREADY
# CLIPPED, so the mask's box is its position.** 31:289 declares 403.6x504.6 and exports
# 308x403, which is exactly 31:288's box, and lands there at err 28.8 against 96.9 at its
# own declared origin; the three thumbnails do the same 12px up and left of where the clip
# rule puts them (28.8 against 91..96). Same mechanism as 54:33's fountain, one band up.
#
# Two more mirrors, both the now-familiar right-edge read: 45:9 (declared 181.1 for a
# 181-wide export -> x 0, err 13.1 against 223.2) and 29:235 (declared 313 for a 303-wide
# export that is NOT clipped, so 313 is its right edge -> x 10, err 11.0). 31:287's 528 is
# the same read (528 - 450 = 78) and rescue found it independently.
#
# 52:6 / 52:8 grow 248 -> 295.5 on BOTH axes and the growth is one-sided on both: 52:6
# keeps its declared x and grows right, 52:8 takes the mirror read and grows left
# (588.1 - 248 - 47.5 = 292.6). Their y is 52.8 above the declared, measured, not derived --
# both scans landed on 8155 independently, which is the only corroboration available for a
# pair this buried (err 86 and 104 under the oval photo).
#
# 31:314 / 31:315, the carousel chevrons, are NOT a mirrored pair despite pointing opposite
# ways: scoring 31:315 against its own flip gives 39.8 unflipped against 174.4 flipped.
# Their offsets inside their buttons differ (12 and 21), which is the design, not a slip.

# The resepsi band is the akad band FLIPPED, and every rule the akad band cost us transfers
# to it -- but the flip is per node there too, so each one still has to be checked.
# Twelve of its seventeen layers declare a right edge where the chain reads a left one:
#
#   29:242 card frame   572 - 548 = 24    (the same x as akad's 22:822 -- same card, flipped)
#   29:241 card plate   533 - 471 = 62    insets 38/39/29/28 against the frame, akad's
#                                          39/38/29/28 with left and right swapped
#   29:253 / 29:254 / 24:897 / 29:244 / 29:248 / 29:249 / 29:274  all bleed off the LEFT
#   29:243 / 29:246 / 29:247 / 29:251                             all bleed off the RIGHT
#
# and four of those also report a bottom edge: 29:243 at y - h, and 29:246 / 29:249 /
# 29:274 at y - EXPORT h. 29:274 lands at err 4.2 that way, the cleanest match in the band.
#
# 54:42 is 54:33's twin (byte-identical, so locate never runs) and is masked the same way:
# 62 is 29:241's left edge, exactly as 63 was 23:851's. 88.4 there against 132.6 at the
# clip rule's 0.
#
# 24:897 is the one that is only measured: err 68.7 at (0, 6081) against 111.9 at its
# declared y and 70.0 where the chain put it. It is scrollwork almost entirely buried under
# 29:254, so nothing scores well; x 0 is the only clip-legal value it can take.

# The akad band, and a rule this frame had only shown on the x axis until now:
# **Figma reports a flipped node's bounds as its RIGHT and/or BOTTOM edge**, and where the
# export grew, the edge is measured against the EXPORT's size, not the declared one.
#
#   52:4  (-182.9, 4902) 366x366, exports 183x366 -> (0,   4536) = y - h        err 12.0
#   52:5  ( 785.0, 4902) 366x366, exports 177x366 -> (419, 4536) = x - w, y - h  err  9.0
#   22:837 (-83, 5610)  223x301, exports 140x301 -> (0,   5309) = y - h         err 68.5
#   22:846 (-154.1, 5395.1) 435x322, exports 167x454 -> (0,   4941) = y - EXPORT h
#   22:827 ( 445.9, 5866.1) 435x322, exports 177x454 -> (419, 5412) = y - EXPORT h
#   32:450 (75, 5828) 130x383, exports 75x383 -> x 0: the 75 is its RIGHT edge, so the
#          node spans -55..75 and the clip is on the LEFT. At the declared 75 it scores
#          520 against 235 at 0.
#
# 52:2 / 52:3 are the same botanical at the card's foot and are NOT flipped vertically --
# both keep y 5695 (200/197 one flip-height away). So the flip is per node; derive it,
# never assume it from a sibling.
#
# 54:33 is a different animal: it is MASKED. Its export is 471x261 against a declared
# 620x310, smaller on BOTH axes, which the clip rule cannot produce at y 5618 in a
# 12818-tall frame. 471 is exactly the width of 23:851, the akad card's inner plate, and
# x 63 is that plate's left edge -- Figma exported the node clipped to its mask, so the
# mask's box is the position. 89.2 at (63, 5618) against 130.9 at the clip rule's (0, 5618).
#
# 24:916 is in PAINTS_NOTHING instead. Its export is clipped 239 -> 107 wide, so the only
# positions the geometry allows are x 0 and x 489, and scanning every y in the band at both
# bottoms out at err 43.4 and 42.4 -- no match anywhere. A free 2-D search over the whole
# band does no better (39.9, and it lands at x 373, which the clip forbids). Dropping it
# takes the band 2.476 -> 2.251. It is buried.

# The quote band's three, all three of them cases the chain gets wrong in a NEW way:
# **Figma grew these exports on ONE side and it is not always the same side.** All three
# report a y the export matches EXACTLY, so every pixel of vertical growth is at the
# BOTTOM and reconcile()'s re-centre pushes them up by half of it.
#
# 23:882, the white cartouche, is 396x594 declared and exports 396x598. locate offered
# (105, 4066) at err 21.0 -- a gray-zone match on a big soft-edged plate, exactly the class
# locate is weakest on. The truth is Figma's own box, (101, 4071): the sheet score is a
# sharp minimum there, 1.817 against 2.03 one px away in any direction and 2.22 two px
# away. Note a 1px render scan preferred 102 (err 21.47 to 101's 22.50) and was WRONG --
# locate samples only alpha > 240, this plate's edges top out at alpha 64, so the scan
# never saw an edge and was matching flat interior texture. Trust the declared x whenever
# the export width equals the declared width; there is no growth to reconcile.
#
# 20:762 / 20:763 are BYTE-IDENTICAL twins, so locate never ran on them and the clip rule's
# re-centre stood unchallenged: it put 20:763 at 507, where it scores err 107.8. They are
# 80x156.3 declared and export 92.5x162.5, and the 12.5 of width lands entirely on ONE
# side -- the left for 20:762 (73 = 85.4 - 12.4), the RIGHT for 20:763, whose declared
# 512.8 is its node's right edge in the bride/groom sense (433 = 512.8 - 79.8). Both land
# at err 12.4. They are NOT a mirror pair despite the bounding behaving like one: scoring
# each export against its own horizontal flip is decisive the other way (12.4 same against
# 87..94 flipped), so the art ships unflipped and only the boxes mirror.

# Opacity and blend mode for the layers whose POSITION is pinned above. solve_alpha
# fitted their alpha against a composite in which they sat hundreds of pixels from home,
# and the only way to make a plate in the wrong place score well is to fade it out. Add
# the same ids to solve_alpha's NO_SOLVE so the next run does not refit them.
#
# 16:491 / 16:493 are ORDINARY OPAQUE ART -- a mirrored pair of white sweet-pea sprigs --
# and the solver's 0.3 screen / 0.12 lighten was hiding a placement error, not describing
# a light leak. Their export grew 219.6 -> 368 tall, but Figma grew it upward rather than
# around the centre, so reconcile()'s re-centre put them 181px low; at that position the
# only way to score is to fade them out, and a symmetric sweep still preferred screen
# because every variant was choosing between two wrong pictures. Cropping each asset to
# its own alpha bbox and locating THAT lands both at y 984 -- independently, and at INK x
# 0 and 431, which is a perfect mirror in a 596 frame. Those are ink positions; each layer's
# own x is the ink position less its ink's offset inside the export, giving PIN_X 0 and 396.
# At y 984 they paint at full strength, stacked normally, and the band goes 3.20 -> 1.82.
# 15:192's alpha came from fitting it 94px from home, where the only way to score is to
# fade out. At its measured position it paints at full strength, stacked normally.
PIN_A = {'15:192': 1.0, '16:491': 1.0, '16:493': 1.0}
PIN_B = {'15:192': 'normal', '16:491': 'normal', '16:493': 'normal'}

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
            route = "clip"
            if found and found[4] < GOOD_ERR and c["id"] not in TRUST_CLIP:
                x, y = found[0], found[1]
                route = f"locate err={found[4]:.1f}"
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
                    route = f"rescue err={hit[2]:.1f}"
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
                # `c["id"] not in twins` matters here as much as it does in the branch
                # above: a repeated sprite's rescue lands on a SIBLING's copy and reports a
                # tiny error for it. The wishes band's 31:424 / 31:426 are byte-identical to
                # the gift band's 31:427 / 31:428 and rescued onto them at err 5.6, 414px
                # from home, beating a clip that was already right.
                if (
                    hit
                    and c["id"] not in TRUST_CLIP
                    and c["id"] not in twins
                    and hit[2] < SURE_ERR
                    and hit[2] < clip_err - 3
                ):
                    x, y = hit[0], hit[1]
                    route = f"rescue err={hit[2]:.1f} < clip {clip_err:.1f}"
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
            if os.environ.get("GEN_TRACE"):
                pin = "".join(k for k, t in (("X", PIN_X), ("Y", PIN_Y)) if c["id"] in t)
                print(f"   {c['id']:9} z{c['z']:<4} box {c['x']:7.1f},{c['y']:7.1f}"
                      f" {c['w']:6.1f}x{c['h']:6.1f} export {w:4}x{h:4}"
                      f" -> {x:4},{y:6}  twin={c['id'] in twins:d} pin={pin or '-':2} {route}")
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
