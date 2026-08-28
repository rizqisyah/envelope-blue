# Slicing notes — template 6

The cover is sliced; the body frame is not. This file carries the **method** the earlier
templates arrived at plus this template's own measurements. Fill the rest in as the
frames are cut; keep the traps — every one of them cost real time to find.

## The frames

| Frame | Node | Size | State |
|---|---|---|---|
| Frame 2 — cover | `27:9` | 596 x 1183 | sliced → `src/components/cover/CoverSection.vue`, layer table in `src/lib/coverLayers.ts` |
| body | — | — | **not dumped yet** |

`.figma-ref/frame27-9-assets.json` is the cover's full child list with a verdict per
node, its text metrics, and why the one dropped node was dropped. Work from that rather
than re-querying Figma.

**This design frame is 596 wide, not 375.** Every coordinate in the cover is in 596-px
design space and `--px` is `100cqw / 596`; the numbers do not transfer from templates 2-5.

`../slicing-wedding-template-5` is the finished reference implementation. Read its
`SLICING.md`, its `src/components/sections/*.vue` and the worked exception tables in its
`scripts/gen_band.py` when a rule here needs an example.

## What this repo already has

| Path | What it is |
|---|---|
| `src/App.vue` | Desktop split layout (left panel + 430px column), cover→body reveal, document-level scroll lock |
| `src/components/cover/CoverSection.vue` | **Sliced** from Frame 2. Layer table in `src/lib/coverLayers.ts` |
| `src/components/invite/InviteBody.vue` | **Placeholder.** The sheet: declares `--px` and lists the bands |
| `src/components/invite/BandArt.vue` | Renders a `BandLayer[]` table with per-layer entrances. Design-agnostic |
| `src/lib/bandLayer.ts` / `bandAssets.ts` | The layer type, and the glob that turns `src/assets/<band>/parts/*.webp` into urls |
| `src/lib/api.ts` / `composables/useWedding.ts` | Live data + `DESIGN_MODE`. Every band's copy is data-driven |
| `src/composables/useReveal.ts` / `useFitText.ts` / `usePreloadAssets.ts` | Scroll reveal, text fitting, asset preload (glob-driven, no edit needed) |
| `src/style.css` | The `.band` entrance rules (design-agnostic), the font imports, and the self-hosted `@font-face` |
| `src/style/tokens.css` | Colour + font tokens. Sampled off Frame 2; `--body-h` still to come |
| `scripts/` | The slicing toolchain, below |

Dev server runs on **5179** (template-5 is on 5178, template-4 on 5176) so they can run
side by side.

## Palette (sampled off Frame 2's own fills)

| Token | Value | Where |
|---|---|---|
| `--water` / `--paper` | `#e9faff` | the frame's own fill, and the pale edge of the water plate |
| `--ink-blue` | `#65839d` | every text node on the cover |

`--paper` is the water blue, not a cream: the water plate is full-bleed, so any other
value flashes at the seams while it decodes.

## Fonts

| Figma face | Token | Shipping as |
|---|---|---|
| Roben Elegante Script | `--font-script`, `--font-display` | **the real file**, self-hosted from `src/assets/fonts/`. Demo cut, personal-use only |
| Cormorant Infant | `--font-serif`, `--font-body` | fontsource, as authored |

Both cover faces are the design's own, so no size compensation is carried anywhere — every
number in `CoverSection.vue` is Figma's. Retiring a substitute later means re-measuring;
there is nothing to re-measure yet.

## Still to fill in

1. The body frame's node id, size and `--body-h`.
2. `scripts/build_refs.py`'s `BANDS` y-range table, plus its `SHEET_PLATES` and `EMPTY`.
6. `.figma-ref/frame<N>-{zorder,assets}.json` — generate these once and work from them
   rather than re-querying Figma.
7. `solve_alpha.py`'s `GROUND` — the flat CSS plates `InviteBody.vue` paints under the
   bands. An empty `GROUND` composites every band over black and every alpha it solves
   comes back wrong.

## The thing that will bite you: exported bounds are not node bounds

Figma's reported node bounds and the size it actually exports disagree in two directions:

- **Clipped.** Figma clips every export to the frame. A node that bleeds off an edge comes
  back narrower than it claims — its true x is 0, not the negative number it reports.
- **Expanded.** A rotated node, or one with a blur, exports a bbox *larger* than the node.
  Figma grows it around the node's centre, so re-centre it: `x = fx + fw/2 − exportW/2`.
- **Reported bounds can lie outright.** A rotated node can report an x past the right edge
  and still render visibly somewhere else entirely.
- **A rotated node's art exports UNROTATED**, and sometimes unscaled. No translation will
  ever match it; it needs a rotate (and possibly a scale) on the layer itself.

So placement tables are **generated, not hand-written**. Every position is either a
template match against the Figma render (`scripts/locate.py`, err < 40 = real match) or
derived from the clip/expansion rule. Regenerate rather than nudging numbers by hand.

## Toolchain

```sh
python3 scripts/flatten_frame.py <raw node json> <flat json>      # once per Figma re-dump
BODY_FRAME=<n> BODY_H=<h> python3 scripts/build_refs.py           # zorder + assets + webp
BODY_FRAME=<n> BODY_H=<h> python3 scripts/gen_band.py             # every band
BODY_FRAME=<n> BODY_H=<h> python3 scripts/gen_band.py hero        # just one
BODY_FRAME=<n> BODY_H=<h> python3 scripts/solve_alpha.py          # opacity/blend/position

npm run dev &                                                     # port 5179
node scripts/sheet-shot.mjs 5179                                  # 1:1 sheet shot
BODY_FRAME=<n> python3 scripts/sheet-score.py                     # every band, one pass
BAND_REF=<1x body render.png> python3 scripts/band-diff.py <y0> <y1>   # one band, 3-up
LOCATE_REF=<1x frame render.png> python3 scripts/locate.py <asset.webp>
BODY_FRAME=<n> BODY_H=<h> python3 scripts/place_plate.py <id> <x0> <y0> <x1> <y1>
node scripts/shot.mjs 5179                                         # eyeball at 3 viewports
node scripts/cover-shot.mjs 5179                                  # cover at 1:1, + open check
```

`cover-shot.mjs` shoots `.cover__frame` at the frame's own width and
`deviceScaleFactor: 1`, so it diffs against the scale-1 render with no resampling — the
same rule `sheet-shot.mjs` follows for the body.

The loop is: `gen_band` (raw geometry) → `solve_alpha` (refine) → `gen_band` (bake) →
`sheet-shot` → `sheet-score`. `solve_alpha` persists ABSOLUTE positions, so running it
again after a regenerate refines the previous pass instead of doubling it. Two passes
converge; a third moves nothing.

`gen_band.py`'s exception tables — `PAINTS_NOTHING`, `TRUST_CLIP`, `PIN_X`, `PIN_Y`,
`PIN_A`, `PIN_B`, `BAND_OF` — start **empty**. They are per-design, and every entry needs
a before/after delta for that node alone. Measure them one at a time: layers that share a
source asset look like a set and usually are not.

## Figma's MCP does not report opacity or blendMode

`get_node` and `get_design_context` return bounds, fills and type — and nothing else.
Every export therefore comes back at full strength and stacked normally, which is wrong
for two whole classes of layer these designs keep using:

- **Light-leak plates.** Near-black rasters with light streaks, authored to be SCREENED
  over the band. Stacked normally they are a grey slab across everything.
- **Faded texture.** Lace and glitter plates running at a fraction of full opacity.

`scripts/solve_alpha.py` recovers all three properties — opacity, blend mode and a
residual position — by compositing the band offline and scoring it against the render.
Two things make that composite match what the browser paints, and both were bugs first:

- **Bands overlap**, so the window is filled from EVERY band's table in global `z`
  order, not just this band's own layers.
- **The sheet's ground is CSS**, not a layer (`GROUND` in the script). Those plates live
  in `InviteBody.vue` and are in no band table, so the solver has to paint them itself.

**The gates are deliberately blunt.** A free search over ±40px, nine opacities and five
blend modes can almost always shave a hundredth off a busy band by moving a layer
somewhere visibly wrong. `MOVE_GAIN`, `MIN_GAIN` and `DROP_GAIN` make a change pay for
itself before it is kept, and `MIN_SOLVE` skips anything under 24px — a 9px dot matches
any patch of its own colour, so its Figma bounds are better evidence than any search.
Loosening these was measurably worse every time it was tried.

**Solve order is position → paint → position → paint.** Paint-first fades a
correctly-shaped layer out of a band because it is in the wrong place; position-first
chases the grey slab a screened plate makes. Both get a second look.

**A plate hundreds of px from home needs `place_plate.py`, not the solver.** Score it
against a FIXED box over the thing it is supposed to explain — the card it washes, the
panel it edges — so every candidate is measured on the same pixels. A box that moves with
the layer rewards a candidate for sliding off-frame or onto empty ground and fading out.
The "without the layer" number it prints first is the bar to beat.

## Bands overlap

A band's height is the distance to the **next** band's top, not the extent of its own
children — children that overrun simply paint past the boundary, which is what the design
does. `section` in the zorder dump is derived from the y-range table and is a **hint**,
not verified.

**The first band starts at 0, not at its first child.** The frame's first child usually
sits some way below the top edge; honouring that opens a gap the design does not have.
`band_tops()` clamps it.

**Round the tops, then derive the heights.** Rounding a top and its height independently
leaves a 1px seam wherever both round the same way, and the sheet ends up short of
`--body-h`. `sheet-shot.mjs` prints the built sheet height — it must equal the frame's
height exactly.

**`z` is the GLOBAL Figma child order.** Every band shares one stacking context, which is
what keeps cross-band layering correct after the split. Do not give a band `z-index` — it
becomes its own context and the global order stops working. Anything a band draws on top
of its art needs its own node's real global z; a z copied from another band puts the
control underneath the art, and it looks like an opacity bug, not a z bug.

**A layer paints in the band its own y lands in**, not the band Figma filed it under. Left
in the wrong band it renders fine and *reveals* wrong: `useReveal` gates a band's layers
on that band scrolling in. That is what `BAND_OF` is for.

## Off-frame nodes: occluded is not absent

Rotated nodes report boxes outside the frame, but Figma still exports pixels for them and
most land back inside as mirrored decorations. `gen_band.py` searches the full frame width
for those (`rescue()`).

When the search *fails*, the layer is either buried under later layers or genuinely
absent, and `locate.py` cannot tell the two apart — it scores over all of a layer's opaque
pixels, so a mostly-buried layer scores badly even where it belongs. **An err above
`GOOD_ERR` on a layer that overlaps its siblings is not evidence of anything.** A failed
search therefore falls back to the clip rule; only `PAINTS_NOTHING` is dropped, and only
for layers that paint an artifact the render does not have.

**A layer measured at its reported bounds, when those bounds are the fiction, has not been
measured at all.** Place it with `place_plate.py` first, then decide whether it paints
nothing. Template 5 dropped an ornament this way that turned out to be plainly visible
once it was scored where it actually belongs.

Settle the ambiguous ones by compositing the band offline and scoring it against the
render (`scripts/solve_band.py`, `scripts/worth.py`, `scripts/band-diff.py`), not by eye.

**A flat-colour layer defeats `locate.py`.** Cream matches cream anywhere, so a blurred
single-colour plate scores under `GOOD_ERR` a couple of hundred px from where it belongs.
Those go in `TRUST_CLIP`, which `gen_band.py` honours *before* the first `locate` hit.

**Both-edges-bleed breaks the clip rule.** The rule guesses which edge cut an export; a
node bleeding past both gets pinned to the wrong side and stacks on its own mirror. `PIN_X`.

## Live text, and what stays as art

Every text node stays **live** so `useWedding()` can drive it — never bake type into an
image to dodge a missing face. Each family is one token in `tokens.css`, so swapping a
substitute for a licensed file means changing one value.

**Retiring a substitute means re-measuring, not just swapping the family.** Substitutes set
a different number of characters per line and their line boxes sit differently, so both the
font-size compensations *and* the positions have to be re-measured by ink box against the
render (`scripts/ink-box.py`). Compensations that existed only for a substitute's metrics
must be reverted to the Figma spec at the same time.

Two traps that display faces keep repeating:

- **Do not `text-transform: uppercase` a display face without checking its case pairs.**
  Several of these faces put cap-height alternates on lowercase and swash or fraktur forms
  on the capitals, so uppercasing swaps the whole word onto the wrong set.
- **An authored newline in a Figma string cannot survive `useWedding()`** — and `&#10;` in
  a Vue template is folded to a space by the parser too. Put the break in a script
  constant and set `white-space: pre-line`, or force it with `text-wrap: balance` and a
  narrow box.

**`TEXT_PATH` is the one exception to live text.** Lettering outlined and bent along a
curve has no CSS equivalent; Figma exports the GLYPH INK and reports the TEXT BOX, so the
clip rule pins it to the box's left edge. Centre the ink in the box for x, and measure y
by ink box — an arched TEXT_PATH's reported top is its *unrotated* top.

**Chrome that has to work ships as CSS, not as a raster.** A picture of an input cannot be
typed into and a picture of three wish cards cannot grow with a longer message. Skip those
plates from the band's `LAYERS` and redraw them.

**Skipping is per-node and easy to half-do.** A raster left in the table under something
the component also draws is invisible when the two agree and wrong the moment they do not
— a baked bank logo prints over a different bank's account number, and a baked Send plate
sits off the real button while looking right because it landed on something the same
colour. Whatever a band redraws, skip.

**An icon the design exports is not one to redraw in CSS.** Put the exported asset inside
a real `<button>`: less code, and the glyph is Figma's rather than a guess at it.

A live list is a flow, not N plates — but where the art has a fixed number of apertures
(account cards, event cards), cap the list at what the art can hold rather than painting
past the last plate. And a `Show more` that reveals nothing is worse than no button: the
design fallback needs one more item than the design draws.

Record the license beside every self-hosted `@font-face` in `style.css`. Several of the
faces these templates use are demo cuts that are personal-use only.

## Design mode

`DESIGN_MODE` lives in `src/lib/api.ts` — **at the boundary, not in a composable**, because
sections import `submitRsvp` / `submitUcapan` directly and a guard that lived only in
`useWedding` let those POSTs through to production. It is on unless `VITE_LIVE_DATA=1`:
`getHome` is never called, so every band renders the design's own content; the submits
throw; and a wish posted in this state is answered locally so the form still works end to
end.

Design-mode wishes are held in a module ref, **not** in `state.data` — seeding `state.data`
would make `wedding` non-null and every band would abandon its design fallback mid-session.

Anything interactive needs a design-mode fallback of its own, or it is dead in the only
mode the slicing is ever looked at in: template 5's gallery had no photos to swipe until
its fallback list existed.

## Two more that cost real time

**A positioned wrapper eats the coordinate system.** Every band child is
`position: absolute` in design px against the band. Wrapping children in a plain `<div>`
makes that div the containing block, and with no offsets of its own everything inside
lands against a zero-size box — the band renders blank. Use `<template v-for>`.

**Scroll the window, not `.desktop-right-column`,** when screenshotting. That column only
scrolls at >=768px; below that the bands never reveal, which reads as a blank sheet rather
than a scroll bug.

## Cover-specific findings

**The export size is the only honest report of what Figma clipped.** `save_screenshots`
echoes the node's DECLARED bounds in its result, not the file it wrote — measure the PNG
itself. The water plate `27:218` declares 681 x 1211 at x -41.95 and writes 1192 x 2366,
which is the frame's own 596 x 1183 doubled: clipped on both edges, so the clip rule
gives it the whole frame at 0,0. The envelope `27:216` writes exactly 2x its declared
box, so its bounds stand as reported. Everything here exports at **2x**.

**A bare auto-layout wrapper is not a layer.** `32:461` ("Frame 7") holds the two guest
lines and paints nothing; its children report coordinates relative to IT, so their frame
coordinates are the wrapper's origin plus their own (842 + 0 and 842 + 42). Placed
directly, the wrapper disappears with no change to the render.

**The two heading boxes are not concentric.** "The Wedding Of" sits at x 112 and the
couple name at x 102, both 392 wide, so the eyebrow renders 10px right of the name's
centre. That is the design, not a rounding slip — reproduce it.

**This design prints no "click to open" label.** So the whole card is the hit plate and
the envelope carries the affordance: it breathes on a slow loop and lifts on hover and
focus. The button keeps an `sr-only` label since there is no visible text to point at.

**Export first, decide after — the frame's node list is not the layer list.** Flat
rectangles become CSS backgrounds, fully-buried nodes paint nothing, and some nodes export
1x1 transparent. Template 5's cover had four of eight non-text children survive.

**`pointer-events: none` on the cover's decorative layers is load-bearing.** A flower
authored across the "Click to open" box and above it in the global z order swallows the
click, and the cover cannot be opened at all.

**A Figma text box shorter than its own line is a `useFitText` trap.** 32px type in a 27px
box makes `scrollHeight` exceed `clientHeight` on a single line, and the name is silently
shrunk. Give the rule the full line-height and pay the difference back through `top`.

## Worth testing on this template

`figma-mcp-go` reports no `opacity` and no `blendMode`, which is why `solve_alpha.py`
exists at all. The official `plugin:figma:figma` server exposes a `use_figma` tool that
runs JavaScript against the file and may be able to read both directly; it needs an OAuth
round trip template 5 did not have. If it can, one call over every node id replaces the
whole inverse problem with ground truth and `solve_alpha.py` collapses to a position-only
refiner.

## Deployment

`VITE_DEFAULT_SLUG` must be set per deployment — without it `src/lib/api.ts` falls back to
`demo-envelop`, which is a *different* wedding and will render the wrong couple.

## Band fidelity

Track mean abs delta per band here once the sheet is up. It is a **relative** signal across
bands, not an absolute fidelity score: it carries every deliberate deviation from the render
— substitute fonts, the live countdown where the design bakes a static plate, the live wish
list and gallery where it bakes rasters of mock content.

Cover: `.figma-tmp/web-cover-1x.png` (from `cover-shot.mjs`) vs
`.figma-tmp/frame27-9-1x.png`. Per channel, 0-255, unmasked.

| band | delta | band | delta |
|---|---|---|---|
| **cover (Frame 2, whole frame)** | **1.29** | body | — |

Every text ink box on the cover matches the render to 1px (headings, both guest lines),
so what is left in that number is glyph hinting and webp loss, not placement.
