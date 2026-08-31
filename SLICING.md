# Slicing notes — template 6

The cover is sliced, and the body frame's first band with it. This file carries the
**method** the earlier templates arrived at plus this template's own measurements. Fill
the rest in as the frames are cut; keep the traps — every one of them cost real time to
find.

## The frames

| Frame | Node | Size | State |
|---|---|---|---|
| Frame 2 — cover | `27:9` | 596 x 1183 | sliced → `src/components/cover/CoverSection.vue`, layer table in `src/lib/coverLayers.ts` |
| Frame 1 — body | `1:3` | 596 x 12818 | dumped; **hero, countdown, bismillah and bride sliced** (y 0..3163) |

The body frame flattens to **290 leaves** across 14 bands. `.figma-ref/frame1-zorder.json`
carries all of them with a band hint each; `.figma-ref/frame1-assets.json` carries the 63
that are exported so far (hero, countdown, bismillah and bride). Its own fill is `#e7f9fe`, which is the sheet's
ground — see the palette below.

`.figma-ref/frame27-9-assets.json` is the cover's full child list with a verdict per
node, its text metrics, and why the one dropped node was dropped. Work from that rather
than re-querying Figma.

**This design frame is 596 wide, not 375.** Every coordinate in the cover is in 596-px
design space and `--px` is `100cqw / 596`; the numbers do not transfer from templates 2-5.

`../slicing-wedding-template-5` is the finished reference implementation. Read its
`SLICING.md`, its `src/components/sections/*.vue` and the worked exception tables in its
`scripts/gen_band.py` when a rule here needs an example.

## Picking this up in a new session

- **State:** cover sliced (1.29); body frame dumped; **hero, countdown, bismillah and
  bride sliced** (1.710 / 1.822 / 4.929 / 1.402), covering y 0..3163 of 12818. Ten bands
  remain, each with nothing but a provisional y-range. The countdown and bismillah were cut
  once by an earlier pass at 5.542 and 20.202 and then reworked — the findings sections
  below are all from that rework, and all of them apply to the bands still to come.
  `npm install` is done; dev server is `npm run dev` on 5179.
- **Cut the groom band next, against the bride as a template.** The two are an exact
  mirror at **+1002px** (20:605↔20:608, 20:594↔20:610, 19:574↔20:607, 20:592↔20:632,
  19:572↔20:609), which makes every bride placement a prediction for its groom twin:
  a groom layer should land at `(mirror-x, bride-y + 1002)`. A pair that does not is a
  measurement to redo, not a coincidence.
- **Every script call needs the frame env**, or they silently run against templates 2-5's
  375-px assumptions: `BODY_FRAME=1 BODY_H=12818 FRAME_W=596 BODY_FRAME_ID=1:3`.
- **`.figma-tmp/exports1/frame1-full.png` is the reference render** (scale 1, so 1px == 1
  design px). It is `locate.py`'s `LOCATE_REF` default and `sheet-score.py`'s `BAND_REF`.
- **Scratch renders** live in `.figma-tmp/` (gitignored, still on disk): the cover's 1x
  and 2x frame renders, `parts27/*.png` before webp conversion, and the fit shots.
  `.figma-ref/` is the tracked dump — read that, not Figma, for anything already sliced.
- **`save_screenshots` writes only inside the MCP server's own working directory.** From a
  session rooted elsewhere it refuses the path outright; the cover's exports had to be
  written into the other template's `.figma-tmp` and moved. Run the Figma work from a
  session rooted in THIS directory, or expect the same detour.
- **Its `result` echoes the node's declared bounds, not the file it wrote.** Measure the
  PNG on disk — that is the only way to see what Figma clipped. See the cover findings.

## What this repo already has

| Path | What it is |
|---|---|
| `src/App.vue` | Desktop split layout (left panel + 430px column), cover→body reveal, document-level scroll lock |
| `src/components/cover/CoverSection.vue` | **Sliced** from Frame 2. Layer table in `src/lib/coverLayers.ts` |
| `src/components/invite/InviteBody.vue` | The sheet: declares `--px` and lists the bands. Renders `HeroSection` |
| `src/components/sections/HeroSection.vue` | **Sliced** from Frame 1 y 0..1108. Layer table in `src/lib/bands/hero.ts` |
| `src/components/sections/CountdownSection.vue` | **Sliced** from Frame 1 y 1108..1802 |
| `src/components/sections/BismillahSection.vue` | **Sliced** from Frame 1 y 1802..2161. Three substituted faces |
| `src/components/sections/BrideSection.vue` | **Sliced** from Frame 1 y 2161..3163. The Instagram pill is CSS + the exported glyph |
| `scripts/text-ink.mjs` | Isolates a band's LIVE text ink by difference; prints computed font sizes |
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
| `--water` / `--paper` | `#e9faff` | the COVER frame's own fill, and the pale edge of the water plate |
| `--sheet` | `#e7f9fe` | the BODY frame's own fill — the invitation sheet's ground |
| `--ink-blue` | `#65839d` | every text node on the cover, and the hero's couple name |
| `--ink-deep-blue` | `#3d78a2` | the hero's eyebrow and hashtag |

`--paper` and `--sheet` are two counts per channel apart and look identical. Keep them
apart anyway: `solve_alpha.py` composites bands over `--sheet`, and fitting opacities
against the cover's value biases every one of them.

`--paper` is the water blue, not a cream: the water plate is full-bleed, so any other
value flashes at the seams while it decodes.

## Fonts

| Figma face | Token | Shipping as |
|---|---|---|
| Cavilenny | `--font-caps` | **substituted** — Cormorant Infant at 39.2 for Figma's 36 (bride call name) |
| Roben Elegante Script | `--font-script`, `--font-display` | **the real file**, self-hosted from `src/assets/fonts/`. Demo cut, personal-use only |
| Cormorant Infant | `--font-serif`, `--font-body` | fontsource, as authored |
| Lancelot | `--font-lancelot` | fontsource, as authored — the hero's eyebrow and hashtag |

The body frame uses **21 faces** in all (`Ibarra Real Nova` 33 nodes, `Roben Elegante` 14,
`Bellefair` 13, then a long tail). Only the hero's two are wired up. Most of the rest are
on fontsource; `Kaleagnetta`, `Cavilenny`, `Activists` and `Comtic Hiden` are not, and will
need the same self-hosted treatment — and the same re-measure — as Roben Elegante. Until
then `Cavilenny` and `Activists` are both standing in as width-matched Cormorant Infant;
retiring either means reverting its size compensation as well as its family.

Both cover faces are the design's own, so no size compensation is carried anywhere — every
number in `CoverSection.vue` is Figma's. Retiring a substitute later means re-measuring;
there is nothing to re-measure yet.

## Still to fill in

1. ~~The body frame's node id, size and `--body-h`.~~ Frame 1 (`1:3`), 596 x 12818.
2. `scripts/build_refs.py`'s `BANDS` — filled, but **only the hero/countdown boundary at
   1108 is verified** (it is the top of `26:8`, the ornate countdown frame, and the
   render's own seam). The twelve entries below it were read off heading positions in the
   frame render and must be re-measured as each band is cut. `SHEET_PLATES` and `EMPTY`
   are both correctly empty: the frame paints its ground with its own fill, and every
   hero export carries ink.
3. ~~`.figma-ref/frame1-{zorder,assets}.json`~~ — generated. Work from them, not Figma.
4. ~~`solve_alpha.py`'s `GROUND`~~ — `[(0, FRAME_H, (231, 249, 254))]`, the frame's own
   `#e7f9fe` fill. Note this is NOT `--paper` (`#e9faff`), which was sampled off the
   *cover* frame; the two differ by a couple of counts per channel, and compositing a
   band over the wrong one biases every opacity the solver fits.

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

All of these need the frame env. Export it once per shell:

```sh
export BODY_FRAME=1 BODY_H=12818 FRAME_W=596 BODY_FRAME_ID=1:3
```

```sh
python3 scripts/flatten_frame.py <raw node json> <flat json>      # once per Figma re-dump
BODY_FRAME=<n> BODY_H=<h> python3 scripts/build_refs.py           # zorder + assets + webp
BODY_FRAME=<n> BODY_H=<h> python3 scripts/gen_band.py             # every band
BODY_FRAME=<n> BODY_H=<h> python3 scripts/gen_band.py hero        # just one
GEN_TRACE=1 BODY_FRAME=<n> BODY_H=<h> python3 scripts/gen_band.py bride  # + one line per layer
BODY_FRAME=<n> BODY_H=<h> python3 scripts/solve_alpha.py          # opacity/blend/position

npm run dev &                                                     # port 5179
node scripts/sheet-shot.mjs 5179                                  # 1:1 sheet shot
BODY_FRAME=<n> python3 scripts/sheet-score.py                     # every band, one pass
FRAME_W=596 node scripts/text-ink.mjs 5179 "<sel>,<sel>"          # live text ink, by difference
BAND_REF=<1x body render.png> python3 scripts/band-diff.py <y0> <y1>   # one band, 3-up
LOCATE_REF=<1x frame render.png> python3 scripts/locate.py <asset.webp>
BODY_FRAME=<n> BODY_H=<h> python3 scripts/place_plate.py <id> <x0> <y0> <x1> <y1>
node scripts/shot.mjs 5179                                         # eyeball at 3 viewports
node scripts/cover-shot.mjs 5179                                  # cover at 1:1, + open check
```

`GEN_TRACE=1` prints, per layer, its declared box, its export size, the position it ended
up at, and **which branch of the reconcile chain produced it** — `locate`, `rescue`, or the
bare clip rule. That last column is the one that matters: a layer routed to `clip` whose
export is smaller than its declared box but whose box does not bleed is the `16:397` case
below, and nothing else in the toolchain flags it.

**Three scripts were carried over from template 5 and lied quietly until they were used.**
`fit-text.mjs` and `sweep-text.mjs` still opened a 375-px viewport, so every design px they
measured came back scaled by 375/596; and `sweep-text.mjs` clicked `.opening__envelope`
while `shot.mjs` asserted on `.opening` — neither class exists in this template, so the
sweep could not run at all and the "cover removed" guard was vacuously true. `shot.mjs`
also asserted on a hard-coded list of template 5's band classes, nine of which do not exist
here, so it printed nine false "reveal fired: false" lines and exited 1 on every run —
it now reads the band list off the DOM. All of them are fixed. **Anything not exercised
while slicing the hero should be assumed to carry the same faults** until it is run once.

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

**One `<h1>` per breakpoint, and the sheet owns it.** The invitation's real title is the
couple name on the band; the desktop side panel only reprints it and is `display: none`
below 768px. Leaving an `<h1>` in the panel made two on desktop and — once the cover
unmounted — none at all on mobile, where a screen-reader user then met an `<h2>` with
nothing above it. The panel's copy is a `<p>`; the cover's `<h1>` hands off to the hero's
when it unmounts.

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

## Body-frame findings (from the hero)

**`flatten_frame.py` had the GROUP coordinate space wrong, and it was silent.** A GROUP's
children report coordinates in the GROUP's OWN space — which is its nearest FRAME
ancestor's, not the root frame's. The old walk reset the offset to `(0, 0)` for every
group, which is right only for a group sitting at the top level; nested inside a frame it
dropped that frame's offset and parked the whole subtree at the top of the sheet. Six
leaves landed in the hero that belong 8000px down. It reads as a plausible layout, so
nothing catches it but a trace. **`../slicing-wedding-template-5` carries the same bug** —
leave it alone unless that template is re-cut.

**Every 375 in the toolchain was a template-2-5 assumption.** `gen_band.py`'s `FRAME_W`
default, `solve_alpha.py` and `solve_band.py`'s constants, `sheet-score.py` and
`band-diff.py`'s crop widths and width assertions, `ink-box.py`'s default `x1`, and
`sheet-shot.mjs`'s viewport are now all `FRAME_W`, defaulting to 596. `shot.mjs` keeps 375
for its two *device* viewports — those are real phones, not the design frame — but its
1:1 sheet page is 596. `InviteBody.vue`'s `--px` and `BandArt.vue`'s `FRAME_W` are the two
in `src/`; a 375-derived `--px` renders the whole sheet at 63% and diffs as garbage.

**`--px` is `calc(100cqw / 596)`, not a rounded decimal.** `0.167785cqw` leaves the built
sheet 1107.98px against `--body-h`'s 1108, and `sheet-shot.mjs` exists to catch exactly
that.

**webp quality is the last lever on a band like this.** Measured on the hero: q88 → 1.956,
q92 → 1.819, q95 → 1.720, for 2.3M / 2.2M / 2.6M of art. Nearly all of what is left in the
score is compression on the toile's high-contrast edges, not placement. `build_refs.py`
ships q95; **q92 beats q88 on both axes**, so drop to 92 rather than 88 if page weight ever
matters more. Note the whole sheet at this rate would be ~35MB — worth revisiting once
more bands land.

**The solver deleted a flower and scored better for it.** `15:192`, the right-edge calla
lily, exports wider than its node (a blur), so the re-centre rule put it at x 545;
`solve_alpha` then "improved" that by sliding it to 565 and fading it to 0.12 multiply —
i.e. by removing something the render plainly draws. `MOVE_GAIN` and friends did not catch
it. A fine scan over the neighbourhood has a sharp minimum at (471, 600): 52.55 there
against 57.38 one pixel right. It is now in `PIN_X`/`PIN_Y`/`PIN_A`/`PIN_B` and in
`solve_alpha`'s `NO_SOLVE`. **A sharp minimum, not a low one, is the evidence** — a white
lily on a near-white wash never scores low anywhere.

**Text ink lands 1px high in the browser.** All three hero text nodes, measured by
exporting the node's glyph ink from Figma and template-matching it into both the frame
render and the live shot, came back dx 0 / dy **-1**. The CSS line box centres glyphs one
pixel higher inside the same `line-height` than Figma does. Pay it back through `top`
(Figma's y + 1) and leave `font-size` and `line-height` at the design's own numbers. This
is per-face: re-measure when a face is swapped.

**`ink-box.py` is useless on the toile.** It thresholds each crop against its own most
common colour, and a blue-on-cream wallpaper pattern reads as ink everywhere — every
window it was given returned the window's own bounds. The export-the-glyphs-and-locate
method above is what to use on a busy ground.

## Read the export's EDGE ALPHA to find which edge Figma cut

This is the single most useful measurement in the toolchain and it is not in any script
yet — it is what unblocked the countdown band after `locate` and the solver both failed.

An export whose pixel size is smaller than its node's declared size was clipped, and the
edge that clipped it is the one whose **alpha runs right up to the boundary**. Compare the
first and last column (or row) of the export's alpha channel against the plate's own
maximum:

| node | declared | export | L alpha | R alpha | verdict |
|---|---|---|---|---|---|
| `16:397` | 191 wide at x 116 | 116 | **212** (its max) | 90 | cut at the LEFT -> x 0 |
| `16:398` | 191 wide at x 480 | 116 | 90 | **212** | cut at the RIGHT -> x 480 |
| `40:91` | 653 wide at x -19 | 596 | **102** (its max) | **102** | cut BOTH -> full bleed, x 0 |

`16:397` is the case that matters: its reported box, x 116..307, is comfortably inside a
596 frame, so **neither branch of `reconcile()` fires** — it only clips a node whose
REPORTED box bleeds — and the value falls straight through to `round(116)`. Nothing in the
chain can catch it, and the render is 75px wrong with no warning. Its edge alpha says the
node really bleeds past x 0 and its reported x is fiction.

## `locate.py` is blind to translucent plates

`opaque_points()` keeps only pixels above alpha **240**. Three of the countdown band's
eight layers — `40:91`, `16:397`, `16:398` — have no such pixel anywhere, so it returns an
empty list and every search scores them at random. That is why `gen_band` reported only 4
of 8 matched, and why the solver's answers for them were noise.

**A layer that `locate` cannot see is not a layer the solver can place.** Use the edge-alpha
rule above for those, and settle the rest by A/B against the live band.

## A faded or screened plate is usually a MISPLACED plate

The countdown's `16:491`/`16:493` came out of the other agent's pass as light-leak plates —
0.3 screen and 0.12 lighten. They are nothing of the kind: they are a mirrored pair of
opaque white sweet-pea sprigs, sitting **181px too low**.

Two things hid it, and both are worth knowing:

- **Figma grew the export asymmetrically.** The node declares 219.6 tall and exports 368.
  `reconcile()` assumes a blur or rotation grows the bbox around the node's CENTRE and
  re-centres accordingly, landing on y 1165. Figma had grown it upward instead; the true
  top is y 984. The re-centre rule is an assumption, not a law.
- **The solver cannot reach 181px.** `SEARCH` is 40. Every position it could try was wrong,
  so the only way to improve the score was to fade the plate out — and a symmetric sweep
  over the whole alpha/blend ladder still preferred `screen`, because it was choosing
  between two wrong pictures. The sweep looked like evidence and was not.

**The fix that works: crop the asset to its OWN alpha bbox and locate that.** A big plate is
mostly empty, so a search over the whole export scores mostly transparent pixels; the ink
crop is what the render actually shows. Both mirrors then landed at y 984 independently, at
x 0 and x 431 — a perfect mirror, which is the corroboration that makes it safe to pin.
At full strength, stacked normally, the band went 3.20 -> 1.82.

So: **settle position before paint, and distrust any opacity under ~0.5 on a layer that
looks like ordinary art.** Every one of the three found so far — the hero's lily, and this
pair — was a placement error wearing an opacity.

## The line-box offset is per FACE, never per project

The hero pays its text back **+1px** and that number was copied to the countdown and the
bismillah. It is wrong for both. Measured the same way — export the node's glyph ink from
Figma, template-match it into the frame render and into the live shot, take the delta —
all six countdown nodes come back **dy +1 against the +1 tops**, i.e. Pinyon Script and
Ibarra Real Nova want Figma's y with **no** offset at all.

| face | offset |
|---|---|
| Lancelot, Roben Elegante (hero) | Figma y **+1** |
| Pinyon Script, Ibarra Real Nova (countdown) | Figma y **+0** |

Re-measure per face. Carrying another band's compensation is not a shortcut, it is a bug.

## Measuring text on a busy ground

Both of the obvious methods fail on this design:

- `ink-box.py` thresholds a crop against its own most common colour — the toile wallpaper
  defeats it, and every window returns the window's own bounds.
- Keying on the node's fill colour fails too, because the greeting's dark green `#2c4b34`
  IS the foliage's green.

Two that work:

- **`scripts/text-ink.mjs`** shoots the sheet twice, once normally and once with the text
  nodes `visibility: hidden`, and differences them. That isolates the live glyph ink
  exactly, whatever it is sitting on. It also prints each node's COMPUTED font-size, which
  is how you catch a rule that silently failed to apply.
- **`Range.getClientRects()`** in the browser gives exact per-line advance widths with no
  image processing at all. Pair it with the Figma side, where a TEXT node's **export is its
  render bounds** — so the export's own pixel size IS the ink extent.

**A text export's origin is NOT the node box's origin.** Figma exports a TEXT node at its
render bounds, so the export tells you the ink's SIZE but not where it starts. For a
centred node, derive the ink's x from the box centre and the ink width; do not add the
export's bbox to the node's x.

## The Vue newline trap bites twice

SLICING.md already says an authored newline cannot survive the template. The bismillah's
greeting was written as two indented source lines with `white-space: pre-line`, and Vue
folded the newline to a space — so the sentence wrapped wherever it happened to fit.

The second-order damage is the part worth remembering: **every width measured off a wrapped
line is a measurement of the wrap point, not of the design's line.** Three rounds of
font-size compensation were fitted against it and all three were meaningless — the numbers
even moved the wrong way when the size changed, which is the tell. Put the break in a
script constant, confirm the rendered line contents, and only then measure.

## Read the render, not the string

`19:569`'s characters are the lowercase `"journey together"` and its face is `Activists`.
The render draws **wide-spaced CAPITALS** — Activists puts cap-height forms on its
lowercase, the case-pair trap this file already warns about, seen from the other side. The
first pass set it in a script face and reproduced the characters instead of the design.

When a face is unavailable, the render is the specification. Here that means uppercase with
tracking, and the substitute chosen by measurement: at the design's own 22px, Ibarra sets
the greeting 446.5 wide, Lancelot 437.1, EB Garamond 475.5 and Cormorant Infant 482,
against the render's 372 — so Ibarra needs the least distortion and keeps the design's size
closest.

**Match the WIDTH and record the height as a deviation.** Activists is condensed enough that
no loaded face reaches its 24px cap height at its 227.5px measure; width-matched, Cormorant
Infant's caps land ~14px. That gap is the floor for the node until the real face is
licensed, and it is a recorded deviation rather than a placement error.

## Score the box over what the layer EXPLAINS, not over the layer

The bride's `20:584` is the sharpest case of this the file has. It is a sweet-pea sprig
291 x 372, and the render shows about 140 x 140 of it — the rest is buried under the
bouquet. A free search over the whole scene (`place_plate.py`, box `0 2300 596 2680`)
rated its best position **0.035** better than not drawing it at all, which reads as "this
layer paints nothing". Dropping it outright scored better than every position tried.

The same script, given a box over just the corner the render actually shows
(`0 2560 160 2720`), separates them immediately: **14.13 without the layer, 7.41 at
(0, 2389)**. Same asset, same composite, same scorer — only the box changed.

Two reusable rules fall out:

- **A big layer that is mostly occluded cannot be scored over its own footprint.** The
  buried 85% is scored identically wherever it goes, and it drowns the 15% that carries
  all the evidence. `MIN_GAIN`-style gates then read the diluted number and refuse.
- **"Dropping it scores better" is not evidence it paints nothing** — it is evidence that
  where it currently sits is wrong. Both statements were true here, and only one of them
  was actionable.

## One export can be clipped on one axis and grown on the other

`20:584` again: declared 342 x 253, exported 291 x 372. `reconcile()` treats each axis
independently, which is right, but the *reasons* differ per axis and only reading both
gets it home:

| axis | declared | export | evidence | answer |
|---|---|---|---|---|
| x | 342 | 291 | left column at the plate's max alpha (254), right at 0 | cut at LEFT → x 0 |
| y | 253 | 372 | grown, and grown DOWNWARD | Figma's own y 2389, not the re-centred 2330 |

The re-centre rule assumed a symmetric blur; that is the third time in this frame Figma
has grown an export in one direction only (`16:491`, `16:493`, `20:640`, now `20:584`).
**Treat the re-centre as a guess and the declared top as the better prior**, then confirm
against the render.

## The bride and groom bands are an exact mirror at +1002

`20:605↔20:608`, `20:594↔20:610`, `19:574↔20:607`, `20:592↔20:632`, `19:572↔20:609` —
every pair sits exactly 1002px apart. That fixes both band tops (2161 and 3163) without
measuring a heading, and it gives every hard placement in one band a free check in the
other: a groom layer belongs at `(mirror-x, bride-y + 1002)`, and a pair that disagrees is
a measurement to redo.

## A centred Figma line is centred INCLUDING its leading space

`19:546`'s string is `"Putri pertama dari \n Bapak Hari Solehaiman \n dan Ibu Kasih
Muhartono Septiana"` — a leading space on both continuation lines, and the longest of the
three is one of them. Figma centres that line with the space, which puts the render's ink
**2px right of the box's own centre**. `white-space: pre-line` strips leading whitespace,
so the block landed 2px left; `pre-wrap` keeps it and the ink matches to the pixel.
Trailing spaces hang and change nothing, in Figma and in CSS alike.

So: reproduce the design's string EXACTLY, spaces included, and use `pre-wrap` when it has
them. This is the same family as the newline trap above — the characters in the Figma node
are part of the layout, not just the copy.

## Colour-keying beats the difference shot when the ink has its own colour

`text-ink.mjs`'s two-shot difference isolates ink on any ground, but its bbox includes
every pixel of anti-aliasing, and neighbouring nodes bleed into whatever window you give
it — the bride's name and the parents line overlap by a few rows of descender, and the
first measurement of each was of the other. Where a node's fill is nowhere else in the
neighbourhood (the bride's `#aa7a3a` gold and `#8a643c` brown against pale toile), keying
on the fill in BOTH images and comparing the two boxes is tighter and needs no window
tuning at all. It is what settled every text node in this band:

| node | face | offset |
|---|---|---|
| `20:641` "Syifa Hadju" | Roben Elegante 32/57 | **0** |
| `19:543` "And" | Roben Elegante 40/71 | **0** |
| `19:546` parents | Cormorant Infant 20/28.4 | **0** (once `pre-wrap` lands) |
| `20:596` "Syifa" | Cormorant Infant for Cavilenny | x −1, y +1 |

Note the hero's Roben Elegante wants **+1** and this band's wants **0**. The offset is a
property of the (face, size, line-height) triple, not of the face alone — the table in
"The line-box offset is per FACE" is a floor, not a shortcut. Measure per node.

## The first band is not scroll-gated, and finding that out took a while

Two separate things kept the hero invisible for the first three seconds after the cover
was tapped, and the reduced-motion screenshots could not show either — the reduced-motion
CSS forces every band visible regardless of `.is-in`, so the 1:1 sheet diff was already
scoring 1.72 while a real viewer saw an empty blue screen.

- **The scroll lock clips the sheet.** `html.is-cover-locked` and `.is-locked` both set
  `overflow: hidden`, and the lock was held until the cover's `@after-leave`. The cover is
  a full screen tall, so the sheet sat below the fold and was clipped clean out of the
  viewport; `useReveal`'s IntersectionObserver cannot fire on a clipped element no matter
  what `rootMargin` says. Released in `openInvitation()` instead: the lock's job is to stop
  a stray wheel event while the cover OWNS the screen, and once tapped it does not.
- **The leaving cover held the flow.** In flow for its whole 2.4s leave, it pushed the
  sheet to ~852px in an 812px viewport, so the invitation snapped up when the cover
  unmounted rather than rising into it. `.splash-leave-active` is now
  `position: absolute` (and `.desktop-right-column` is `position: relative` at every
  breakpoint, not just >= 768px, or that resolves against the viewport).

With both fixed the hero still needs `useReveal(0, '0px 0px 100% 0px')`: during the leave
its top is a viewport-height below the fold, and the default `-12%` bottom margin makes it
later, not earlier. **A band that is on screen when the sheet opens should not wait for a
scroll it will never get.**

**Check the reveal with motion ON.** `shot.mjs`'s `hero reveal fired` line is the only
thing in the toolchain that can see this class of bug; its `false` was real, and its
timing (2.2s after the click) is what caught it. The other bands' `false` lines are just
bands that do not exist yet.

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
| **cover (Frame 2, whole frame)** | **1.29** | **hero** (y 0..1108) | **1.710** |
| **countdown** (1108..1802) | **1.822** | **bismillah** (1802..2161) | **4.929** |
| **bride** (2161..3163) | **1.402** | groom | — |
| quote | — | akad | — |
| resepsi | — | dresscode | — |
| | | | |
| gallery | — | gift | — |
| wishes | — | rsvp | — |
| closing | — | | |

Every text ink box on the cover matches the render to 1px (headings, both guest lines),
so what is left in that number is glyph hinting and webp loss, not placement.

The bismillah's four assets were shipped by an earlier pass as **lossless** webp — 1.4MB
for the four, against 0.6MB at the q95 `build_refs.py` uses for every other asset. Running
the generator over the frame re-encoded them to match, which is where 4.884 -> 4.929 comes
from. The 0.045 is not worth 800KB, and an asset the toolchain cannot reproduce is worse
than a slightly softer one; if the number ever matters, raise the quality for the whole
frame in `build_refs.py` rather than for four files by hand.

The countdown was cut by another pass at **5.542** and the bismillah at **20.202**; the
numbers above are after the rework described in the findings sections. Both bands now carry
**no opacity or blend override at all** — every layer paints at full strength, stacked
normally, which is what the design does. The five overrides the earlier pass carried were
each compensating for a placement error.

The bismillah's 4.929 is **not** comparable to the other bands: all three of its faces are
substitutes (Perpetua, Activists and an Arabic fallback Figma reached for when Alex Brush
could not set the Basmala). Its art diffs clean; effectively the whole number is glyph
shape, and it is the floor until those faces are licensed.

The hero's three text nodes match the render to **0px in both axes** (measured by locating
their exported glyph ink in both images), and the amplified difference map shows no
doubled edge or offset silhouette anywhere in the band — what is left in 1.720 is webp
compression on the toile and the botanicals. It is a busier band than the cover by 29
layers, which is most of the gap between the two numbers.
