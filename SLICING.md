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

- **State: the frame is COMPLETE.** Cover sliced (1.29) and all fourteen body bands sliced
  (1.710 / 1.822 / 4.251 / 1.307 / 1.298 / 1.817 / 1.240 / 1.173 / 1.104 † / 2.149 /
  **0.898** / 1.554 / 1.195 / 2.156), covering y 0..12818 — the whole of Frame 1, at a
  sheet-wide 1.614 †. `npm install` is done; dev server is `npm run dev` on 5179. The countdown and bismillah were cut once by an
  earlier pass at 5.542 and 20.202 and then reworked — the findings sections below are all
  from that rework, and all of them apply to the bands still to come. `npm install` is done;
  dev server is `npm run dev` on 5179.
- **What is left is polish, not slicing.** The faces the frame needs and does not have are
  the whole of the remaining gap on every band above 2, and licensing one is worth more
  than any further measurement. Activists, Cavilenny and Comtic Hiden have now been found
  and self-hosted, which took four nodes to an exact match; still missing are Kaleagnetta
  (akad/resepsi headings), Perpetua and the bismillah's Arabic, and whatever condensed
  serif sets the gallery band's promo caps. The known residuals are listed at the foot of
  this file.
- **Only the bands already cut have their PNG exports on disk.** `.figma-tmp/parts1/` was
  pulled band by band, so the next band's nodes have to come out of Figma first or
  `build_refs.py` reports `!! missing export` and generates a band with zero assets. Pull
  them with `save_screenshots` at scale 2 into `.figma-tmp/parts1/<id with : as ->.png`.
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
  session rooted in THIS directory — done that way it takes an absolute path into this
  repo and writes straight to `.figma-tmp/parts1/`, no detour (confirmed on the quote
  band's six).
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
| `src/components/sections/GroomSection.vue` | **Sliced** from Frame 1 y 3163..4021. Placed entirely by mirroring the bride |
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
| Roben Elegante Script | `--font-script`, `--font-display` | **the real file**, self-hosted from `src/assets/fonts/`. Demo cut, personal-use only |
| Activists | `--font-caps` | **the real file**, self-hosted. `19:569` at Figma's own 32 |
| Cavilenny | `--font-call` | **the real file**, self-hosted. `20:596` / `20:622` at Figma's own 36. Demo cut, personal-use only |
| Comtic Hiden | `--font-comtic` | **the real file**, self-hosted. `42:3` at Figma's own 24. Demo cut, personal-use only |
| Kaleagnetta | `--font-hand` | **substituted** — Palisade, self-hosted, width-matched per word, akad/resepsi headings |
| Cormorant Infant | `--font-serif`, `--font-body` | fontsource, as authored |
| Lancelot | `--font-lancelot` | fontsource, as authored — the hero's eyebrow and hashtag |

The body frame uses **21 faces** in all (`Ibarra Real Nova` 33 nodes, `Roben Elegante` 14,
`Bellefair` 13, then a long tail). Most are on fontsource. Four were not — `Kaleagnetta`,
`Cavilenny`, `Activists` and `Comtic Hiden` — and three of those now ship as the design's
own file, self-hosted the way Roben Elegante already was. Only Kaleagnetta is still a
stand-in, so `--font-hand` is its token alone.

**Retiring a substitute deletes numbers rather than re-measuring them.** Every one of these
nodes had a compensation fitted to the face that was standing in, and each one goes:

- `19:569` "journey together" lost a `text-transform: uppercase` and a width match at 23.
  The transform was Cormorant mimicking Activists' cap-height lowercase; the real face
  needs none, because the design's lowercase string IS the render's capitals.
- `20:596` / `20:622` lost 39.2 and 37.5 — two sizes for one authored 36, because a width
  match is per WORD and Cormorant ran 8.8% narrow on "Syifa" against 4.2% on "El Rumi".
  One real file, one size, both words. Her `top`/`left` 1px nudges went with it: those
  were the substitute's line box and side bearings, not the node's.
- `42:3` lost the frame's only TRACKING case — `letter-spacing: 4.9` with a matching
  `text-indent`, plus a 27.6 size, all of it fitted because Sacramento sets this line 38%
  narrow PER UNIT HEIGHT and no font-size can reach that.

Measured after the swap, keying each node's own fill against the 1x render: all four ink
boxes land at **dx 0, dy 0**, with `19:569` and `20:622` exact in width and height as well.
The bismillah band drops 4.929 → 4.251, bride 1.402 → 1.307, groom 1.478 → 1.298, closing
2.953 → 2.846, and the sheet 1.856 → 1.806.

Both cover faces are the design's own, so no size compensation is carried anywhere — every
number in `CoverSection.vue` is Figma's.

## Still to fill in

1. ~~The body frame's node id, size and `--body-h`.~~ Frame 1 (`1:3`), 596 x 12818.
2. `scripts/build_refs.py`'s `BANDS` — filled, and verified down to **6970**: 1108 is the
   top of `26:8`, 2161 and 3163 come out of the bride/groom mirror, 4021 is `54:17`'s top,
   4425 is `54:20`'s, 5907 is where `22:822` (the akad card frame) ends and resepsi's first
   node begins, and 6970 is where `29:242` (the resepsi card frame) ends. The six entries
   below it were read off heading positions in the frame render and must be re-measured as
   each band is cut — 7750 and 8865 are verified too, where `31:316` / `29:235` open the
   gallery, `45:12` / `45:11` open the gift band, `32:456` / `32:454` open wishes and
   `35:534` opens rsvp and `40:76` opens closing. Note
   the resepsi band still *derives* 5907..7034: nothing sits in the 64px of plain ground
   between the card and the dresscode heading, so the gap falls to resepsi. `SHEET_PLATES` is correctly empty — the frame paints its ground with its own
   fill. `EMPTY` holds `54:35` and `54:41`, 1x1 transparent files declaring the same box and
   the same name ("dbfb") as their own band's card plate (`23:851`, `29:241`) — dead
   duplicates rather than layers, and there is one per event card.
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

## A width match is per WORD, not per face

Both call names are Cavilenny 36 in the design and both are set in Cormorant Infant here,
and they need **different sizes**: "Syifa" wants 39.2 (Cormorant sets it 8.8% narrow) and
"El Rumi" wants 37.5 (4.2% narrow). Two faces' per-glyph widths do not differ by a constant
ratio, so a compensation fitted on one string is only right for that string. Measure each
node; a substitute's size belongs beside the node, never in the token.

The second-order effect: the line-box correction moves with the size. "Syifa" at 39.2
needs x −1 / y +1 and "El Rumi" at 37.5 needs neither, same face, same line-height.

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

## The bride and groom bands are an exact mirror — and a mirror places a band for free

Fourteen pairs, 1002px apart, and it is a real mirror rather than a copy: every same-size
pair's export is the horizontal FLIP of its twin (mean abs delta 3..9 mirrored, against
17..61 unflipped). Correlating the two scene crops puts the axis at **x 294**, not the
frame's 298, which matches the constant every pair's declared origins already showed:
`bride_x + groom_x = 588`.

    groom_x = 588 - bride_x - bride_w        groom_y = bride_y + 1002

That is not a sanity check, it is the placement method. Nine of the fourteen pairs came
out of the ordinary chain already agreeing with it — including every clipped one, which is
what makes the remaining five safe to pin outright rather than search for. Pinning those
five took the band **5.958 -> 1.516** in one pass, and a 1px scan afterwards puts `20:626`
at a sharp minimum on the predicted 294 (1.914 / 1.702 / **1.478** / 1.678 / 1.903 across
292..296). The prediction is exact, not approximate.

**Figma reports a mirrored node's `bounds.x` as its RIGHT edge.** That is why the chain
missed the five: `20:627` declares 333 for 141-wide art that renders at 192, `20:609`
declares 433 for 342-wide art that renders at 91, `20:625` declares 679 for 183 that
renders at 496. Every one of those boxes sits comfortably inside the frame, so no clip
branch fires and the number falls straight through to `round()` — the same structural
blind spot as `16:397`, arrived at by a different route. `rescue()` did fire on two of
them and returned err 154 and 41, i.e. noise.

So: **when a band has a mirror, resolve the pairs before searching anything.**

## `locate` cannot see a plate whose edges are soft, and its answer is not noise-free

`23:882`, the quote band's white cartouche, is 396x594 declared and exports 396x598.
`locate` offered (105, 4066) at err 21.0 — inside `GOOD_ERR`, so the chain took it. A 1px
scan of the same scorer preferred (102, 4071). **Both were wrong.** Scoring the whole sheet
instead puts a sharp minimum on Figma's own box, (101, 4071):

| x at y 4071 | 99 | 100 | **101** | 102 | 103 |
|---|---|---|---|---|---|
| sheet delta | 2.232 | 2.035 | **1.817** | 2.015 | 2.217 |

and y is the same shape: 2.028 / **1.817** / 2.032 / 2.223 across 4070..4073.

The reason the render scan misled is structural. `locate.opaque_points` samples only pixels
with **alpha > 240**; this plate's edges top out at alpha 64 for their whole length, so not
one edge pixel is in the sample. Everything it matched was flat interior texture, which is
nearly translation-invariant — hence a shallow, wandering minimum. A soft-edged plate gives
`locate` nothing to bite on, and its err lands in the 15..40 gray zone precisely because of
that.

So: **when the export's width equals the declared width, there is no growth to reconcile
and the declared x is the answer** — do not let a gray-zone `locate` hit talk you out of it.
And when a placement is worth a pixel, A/B it against the SHEET SCORE, which weights every
pixel of the layer equally, rather than against a scorer that only sees the opaque ones.

## Byte-identical twins skip `locate` entirely, and the clip rule can be 74px wrong

`20:762` / `20:763` are twins — same bytes, so `gen_band` refuses to template-match them
(every copy scores the same at every other copy's slot) and the re-centre rule stands
unchallenged. It put `20:763` at x 507, where it scores **err 107.8**. Its real x is 433.

Both are 80x156.3 declared and export 92.5x162.5, and **the 12.5px of width lands entirely
on one side — a different side for each**: the left for `20:762` (73 = 85.4 − 12.4), the
right for `20:763`, whose declared 512.8 is its node's right edge in the bride/groom sense
(433 = 512.8 − 79.8). Both then land at err 12.4. Their declared *y* is exact for both, so
all 6.2px of height growth is at the bottom — the fourth, fifth and sixth one-sided growth
in this frame, counting `23:882`.

**The bounding can mirror without the art mirroring.** The pair looks like a mirror and its
boxes behave like one, but scoring each export against its own horizontal flip is decisive
the other way — 12.4 unflipped against 87..94 flipped. They ship unflipped; only the boxes
are mirrored. Run the flip test before assuming a `scaleX(-1)`; `BandLayer` has no transform
channel and adding one for a pair that does not need it is the expensive mistake here.

So: **a twin is a layer with no evidence behind its position.** Score it by hand — the
scorer is three lines around `locate.opaque_points` — before believing anything the chain
did with it.

## Flat shapes are CSS, and a VECTOR rasterises like anything else

The dresscode band brought the frame's first `ELLIPSE` and `VECTOR` nodes, and they want
opposite treatment.

Its four palette swatches (`29:275` / `29:276` / `29:277` / `30:281`, 68x71 at y 7115,
fills `#dbc58e` `#9bccdb` `#bde0b5` `#edcbe3`) are solid fills and nothing else, so they go
in **`build_refs.py`'s new `CSS_SHAPES`**: skipped for export the way `TEXT` is, but KEPT in
the z-order so the stacking stays intact, and drawn by the band as `border-radius: 50%`
divs. All four land 0px on all four edges — a `border-radius` is exact where a 68x71 webp
is resampled. Note they are ellipses, not circles (68 wide, 71 tall), so `50%` both ways.

`29:233`, a 602x161 `VECTOR`, needs none of that: `save_screenshots` rasterises it like any
rectangle, and the ordinary clip rule places it (declared x 4, so 4..606 bleeds off the
right edge, export comes back 592 wide, `locate` err 2.3). **Type is not the question —
whether the node is one flat fill is.** The gallery band below has `ELLIPSE`es used as photo
MASKS; those are not CSS shapes.

**A CSS shape has to be masked in `solve_alpha` the way TEXT is**, and it was not at first.
Its composite neither paints a `CSS_SHAPES` node (there is no asset) nor knew to ignore it,
so four solid ellipses against plain ground put **~1.46 of phantom error** into the band's
composite score — 2.438 where the corrected mask gives 0.977. It changed no verdict here,
because no solvable layer's search box comes within `SEARCH` of the swatches and the live
sheet score is the authority anyway. It would change one on a band where a CSS shape sits
beside a genuinely faded layer: that layer's local score is inflated, and `refine_paint`
pays for it by fading something that should not fade. `text_mask` now masks **anything in
the z-order with no asset**, which is the honest statement of what it was always for — the
composite cannot draw it, so it must not be scored.

## The clean-band number is 0.683

Dresscode scores **0.683**, less than half the next-best band, and it is worth knowing why
because it calibrates every other number in the table:

- Both its faces are the design's own (Roben Elegante, Ibarra Real Nova). No substitution,
  no width compensation, no per-word size.
- Nothing needed a position pin. All five art layers either sit inside the frame or bleed
  off BOTH edges, so the clip rule and `locate` agree — the two failure modes this frame is
  full of (a flipped node's declared edge, a one-sided export growth) simply do not arise.
- Its flat shapes are CSS rather than resampled art.
- `solve_alpha` found nothing to fade.

So 0.683 is roughly what this pipeline costs when nothing is substituted: webp loss on the
art and glyph rasterisation, and no more. Read the other bands against it — the ~1.4-2.1
range is placement that is right but art that is compressed, and the bismillah's 4.9 is
three substitute faces.

## Figma reports a flipped node's bounds as its RIGHT and/or BOTTOM edge

The bride/groom band established the x half of this. The akad band has both axes, and
several nodes flipped on only one of them:

| node | declared | export | truth | rule |
|---|---|---|---|---|
| `52:4` | −182.9, 4902, 366x366 | 183x366 | 0, **4536** | y − h |
| `52:5` | 785, 4902, 366x366 | 177x366 | **419**, **4536** | x − w, y − h |
| `22:837` | −83, 5610, 223x301 | 140x301 | 0, **5309** | y − h |
| `22:846` | −154.1, 5395.1, 435x322 | 167x**454** | 0, **4941** | y − EXPORT h |
| `22:827` | 445.9, 5866.1, 435x322 | 177x**454** | **419**, **5412** | x − w, y − EXPORT h |
| `32:450` | 75, 5828, 130x383 | **75**x383 | **0**, 5828 | x − w, then clip |

Two things to take from the table. **Where the export grew, the edge is measured against
the EXPORT's height, not the declared one** — `22:846` and `22:827` both land exactly on
`y − 454`, and `y − 322` is 132px wrong. And **the flip is per node, not per motif**:
`52:2` / `52:3` are the same botanical at the same card's foot and are NOT flipped
vertically, so both keep their declared y (their flip-height alternative scores 197..200
against 10..13). Derive it per node; never carry it across from a sibling.

`32:450` is the same blind spot as `16:397`, reached by a third route: its declared 75 is
its right edge, so the node really spans −55..75 and the clip is on the LEFT. Because the
export IS narrower than the box, the clip branch does fire — it simply guesses the wrong
edge. 520 at the declared 75 against 235 at 0.

## The resepsi band is the akad band flipped, and the flip is in the DATA

Twelve of resepsi's seventeen layers declare a right edge where the chain reads a left one,
and four of those declare a bottom edge as well. The card itself is the tell: `29:242`
declares x 572 for a 548-wide export, which cannot be a clip (572 + 548 overruns the frame,
so Figma would have cut it) — read as a right edge it gives **x 24, the same x as akad's
`22:822`**. Same card, flipped, same place. Its plate `29:241` then lands at 62 with insets
38/39/29/28 against the frame, which is akad's 39/38/29/28 with left and right swapped.

`29:274` is the cleanest match in the band at **err 4.2** on `x − w` plus `y − EXPORT h`,
and it is worth noting against its akad twin `24:916`, which is buried and paints nothing.
**The same source art in the mirrored slot is not the same layer.** Check each one.

What did NOT transfer: the y offsets. The cartouche is 1061px below akad's, the card frame
1063, the text block 1048. The band is a flip, not a translation — do not try to derive
positions from the akad band arithmetically the way the bride/groom mirror allowed.

## A single-line `<input>` centres its text whatever `padding-top` says

The rsvp band's four field plates put their label 12.8 down from the plate's top, which is
2.7 ABOVE the centre of a 54px box. That inset cannot be written as `padding-top`: a
one-line `<input>` centres its value in the CONTENT box, so raising the top padding pushes
the content box down and the text stays centred in it. The lever is the DIFFERENCE between
top and bottom padding — `8.8 / 16.8` here, measured, with the horizontal inset carried
separately at 11.8.

A `<textarea>` behaves the other way (its text starts at the top padding), which is why the
wishes band's message field takes a plain 12.8 and its name field does not.

## A band's own chrome is invisible to every script in the toolchain

The wishes band draws four things that are in no node table at all — the two white fields,
the Send pill and the Show more pill, all auto-layout frames `flatten_frame.py` never
emitted. Measured off the render:

| what | box | fill |
|---|---|---|
| name field | (92, 9742) 424 x 54 | `#ffffff`, radius 8 |
| message field | (92, 9812) 424 x 88 | `#ffffff`, radius 8 |
| Send | (91, 9915) 426 x 54 | `#b2d3e2`, fully rounded |
| Show more | (85, 10344) 426 x 54 | `#b2d3e2`, fully rounded |

All four land 0px on all four edges once drawn from those numbers. **The trap is what
happens next:** `solve_alpha` composites nodes, so where the render has a white field it
composites plain ground and scores the difference as error. The wishes band's offline
number was **3.562** against a live sheet score of 1.582 — the gap is almost entirely those
four rectangles. `text_mask` can find a `CSS_SHAPES` node by "in the z-order with no asset",
but reconstructed chrome has no node to find, so `solve_alpha` now carries **`DRAWN_BOXES`**,
a hand-listed set of frame-space rectangles a band draws itself. It changed no verdict here
(0.627 for gift, down from 1.456 unmasked) but a faded layer whose search box overlaps one
of these would have been refitted to pay for the phantom.

**Every band that reconstructs chrome has to add its boxes there.** The rsvp band below has
the same form shape and will need the same entries.

## A repeated sprite can rescue onto its SIBLING, not just confuse `locate`

The twins guard was already in the `locate` branch and in the off-frame rescue. It was
missing from the third one — the clip branch's rescue — and the wishes band found it:
`31:424` and `31:426` are byte-identical to the gift band's `31:427` and `31:428`, and they
rescued straight onto them at **err 5.6, 414px from home**, beating a clip rule that was
already right. Both bands now look correct only because the pins overrule it. The guard is
in all three branches now.

The lesson generalises past this repo: **a confident low error from a search is evidence
that the ASSET is somewhere, never that this NODE is there.** Only the geometry ties an
error to an id.

There is a scheduling corollary. **The twins set GROWS as later bands are cut**, so a node
`locate` placed correctly can silently lose `locate` on a later regenerate. `31:427` was
matched by `locate` at err 5.5 when the gift band was cut, because its byte-twin `31:424`
did not exist yet; once the wishes band's assets landed both became twins and `locate` is
skipped for them. It still lands at 0 — `reconcile` reads the declared 108 as a right edge
and the clip rule is deterministic — but that was luck, not design. **Read the `route`
column in `GEN_TRACE`, not just the position**: a layer whose only evidence is `locate` is
a layer that can change answer when a later band is dumped.

## Figma's MCP does not report `textCase` either

`31:390` and `31:432`, the gift band's bank lines, come back as `characters: "Bank Bca
(014)"`. The render prints **BANK BCA (014)**. `get_nodes_info` reports fills, family, size,
weight and line-height and nothing about case, so this joins `opacity`, `blendMode` and
`letterSpacing` on the list of things only the render knows.

The tell is the width: the render's ink is **157** where mixed case sets 129. Toggling the
rule with everything else in the band held fixed puts it at **1.542 without, 0.898 with** —
one `text-transform` is worth 0.644 on a 700px band, because the line is set twice and each
copy misses on every glyph. Put it in CSS rather than in
the string — a live `bank_name` from the API has to get the same treatment, and the design's
own copy is not the source of truth for case.

So: **when a text node's ink is wider than its `characters` can explain, check the case
before reaching for letter-spacing or a substitute face.**

## Where a band repeats a sprite, trust the geometry over `locate`

`32:457` is the trap in its purest form. `locate` placed it at (30, 9250) with **err 5.1** —
a real match, and a confident one. It is a match of `31:427`'s copy of the same floral,
which really does sit at (0, 9250). Its own geometry — a mirrored left bleed, declared y —
puts it at (0, 9109) at err 5.2, statistically the same number in the right place.

The twins guard did not fire because the four `Photoroom` crops in this band are
near-identical without being byte-identical, and the guard hashes bytes. A hash cannot see
this; only the geometry can. When a band draws the same sprite more than once, resolve every
copy from its declared box and use `locate` to confirm, never to decide.

## A masked PHOTO exports clipped too — so the mask's box is its position

`54:33`'s fountain was the first case; the gallery band has four more and they make the rule
worth stating on its own. `31:289` declares 403.6x504.6 and exports **308x403**, which is
exactly the box of `31:288`, the `ELLIPSE` above it. It lands there at err 28.8 against 96.9
at its own declared origin. The three thumbnails do the same: declared 126.2x157.8, exported
102x119, and they belong 12px up and left of where the clip rule puts them (28.8 against
91..96).

So a photo in an oval needs no CSS clip to be *placed* — the export already carries the
oval. The band still draws it inside a `border-radius: 50%` container, because a LIVE photo
from the API is rectangular and needs the shape; over the design's own export the radius is
a no-op.

**The mask nodes themselves paint nothing.** All six of the band's `ELLIPSE`es are
`#d9d9d9`, Figma's placeholder grey: four are masks fully covered by their photo, and two
are the carousel buttons, which the render shows at that exact colour, fully opaque
(sampled (217, 217, 217) dead centre). All six go in `CSS_SHAPES` — four because there is
nothing left to draw, two because a `border-radius` div is exact.

## A masked node exports clipped to its MASK

`54:33`, the fountain at the foot of the akad card, declares 620x310 and exports **471x261
— smaller on both axes**. Frame-clipping cannot do that at y 5618 in a 12818-tall frame,
and no growth rule produces it either. 471 is exactly the width of `23:851`, the card's
inner plate, and 63 is that plate's left edge: Figma exported the node clipped to its mask,
so **the mask's box is the position**. 89.2 at (63, 5618) against 130.9 where the clip rule
put it, and the export's 261 rows end at 5879, which is the plate's own bottom edge.

So: when an export is smaller than its box on BOTH axes, look for a mask, and look for
another node whose box explains the export's exact size.

## `NO_SOLVE` was too blunt: pinning a position must not pin the paint

`solve_alpha.py`'s `NO_SOLVE` skipped a layer entirely, and every hand-pinned id was told
to go in it. That is right for the layers it was written for — a plate 200px from home is
only made to score by fading it out, so its fitted alpha is a symptom, not a measurement.
It is wrong for a layer the design genuinely fades. `54:33` is masked into the card and
painted back at **0.55 darken**; blocked from the paint search it sat at full opacity and
cost the band 0.4 on its own (4.105 -> 2.476 once solved).

There is now a second set, **`NO_MOVE`**: position held, paint still searched. Use it for a
layer whose position you measured and trust, and `NO_SOLVE` only when the fitted alpha was
itself an artefact of the bad position. Every akad and resepsi pin lives in `NO_MOVE`.

`NO_MOVE` also **overrides the twins guard**, and `54:42` is why. It is byte-identical to
`54:33`, so `solve_alpha` skipped it outright and the resepsi fountain sat at full opacity
where the akad one is 0.55 — 4.167 against 2.138 for the band. A twin whose position is held
cannot slide into its sibling's slot, so only its paint gets searched, which is exactly what
a repeated faded sprite needs. Expect this on every band that redraws a card.

## Before calling a layer buried, prove it has no LEGAL position

The `20:584` finding says a free search rating a layer "worthless" is not evidence it is
absent. The converse test is what settles it, and `24:916` is the worked example:

- Its export is clipped 239 -> 107 wide, so the geometry allows exactly two x values,
  0 and 489. Sweeping y at both — **past the band's own edges, because bands overlap and a
  layer's declared band is only a bucket** — bottoms out at err 43.4 and 42.4, and extending
  the sweep to 6300 only reaches 45.9.
- A free 2-D search over the whole band does no better — 39.9 — and it lands at x 373,
  which the clip forbids. That is the "least-bad spot" pattern, not a match.
- Scored over **the box it would EXPLAIN** rather than its whole export — the flower head
  alone, against the rows where the render actually has a pale-blue chrysanthemum — its
  declared (0, 5790) gives 189.8. That is the `20:584` technique run the other way, and it
  is the check that has to be done before the verdict: a full-box err near 190 says nothing
  by itself, because an occluded layer scores ~190 everywhere.
- Dropping the layer takes the band **2.476 -> 2.251**.

Four signals, one conclusion: it is buried, and it goes in `PAINTS_NOTHING`. Note the
order — enumerate the legal positions FIRST, because a free search will always answer, and
sweep past the band edge, and score the explained box rather than the export.

## A design underline is not a browser underline

`23:879` "View Maps" is underlined in the render. The default `text-decoration: underline`
put a 2px line at y 5677; the render's own row profile has a **single 1px line at 5682**,
98 wide, at (121, 140, 131) — `#4e685c` anti-aliased across one row. `text-underline-offset:
8px` and `text-decoration-thickness: 1px` land it. Measure the rule's row and width off the
render before accepting the browser's defaults; it is worth 0.04 on the band.

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
| `19:546` / `20:616` parents | Cormorant Infant 20/28.4 | **0** (once `pre-wrap` lands) |
| `20:614` "Ahmad Jalaluddin Rumi" | Roben Elegante 32/57 | **0** |
| `20:596` "Syifa" | Cormorant Infant for Cavilenny, 39.2 | x −1, y +1 |
| `20:622` "El Rumi" | Cormorant Infant for Cavilenny, 37.5 | **0** |

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
| **countdown** (1108..1802) | **1.822** | **bismillah** (1802..2161) | **4.251** |
| **bride** (2161..3163) | **1.307** | **groom** (3163..4021) | **1.298** |
| **quote** (4021..4425) | **1.817** | **akad** (4425..5907) | **1.240** |
| **resepsi** (5907..7034) | **1.173** | **dresscode** (7034..7750) | 1.104 † |
| | | | |
| **gallery** (7750..8865) | **2.149** | **gift** (8865..9565) | **0.898** |
| **wishes** (9565..10763) | **1.554** | **rsvp** (10763..11452) | **1.195** |
| **closing** (11452..12818) | **2.156** | **SHEET** (0..12818) | 1.614 † |

† **dresscode carries a deliberate deviation and its number is no longer a fidelity
signal.** `29:233`, the lace scallop that closes the band, is at x 4 in the render —
`locate.py` scores err 2.34 there, the ref's and the build's leftmost ink agree row for
row, and the band is at a sharp minimum: 0.683 at 4 against 1.104 at 2 and 1.309 at 0. The
4px inset on the left is the design's own. It is pinned to 2 on the owner's call, who
wants it nearer flush with the frame edge; 1.104 is what that costs, and the sheet's 1.614
carries it. `PIN_X['29:233'] = 4` restores the measured position.

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

The bismillah's 4.251 is **not** comparable to the other bands: its faces are substitutes
(Perpetua, and an Arabic fallback Figma reached for when Alex Brush could not set the
Basmala). Its art diffs clean; effectively the whole number is glyph shape, and it is the
floor until those faces are licensed. It was 4.929 when Activists was the third of them —
that face now ships as the design's own file and its node matches the render exactly, which
is what the 0.678 buys and what the two remaining faces are still costing.

The hero's three text nodes match the render to **0px in both axes** (measured by locating
their exported glyph ink in both images), and the amplified difference map shows no
doubled edge or offset silhouette anywhere in the band — what is left in 1.720 is webp
compression on the toile and the botanicals. It is a busier band than the cover by 29
layers, which is most of the gap between the two numbers.

The quote band is the first with **no substitute face**: Cinzel and Cormorant Infant are
both the design's own and both ship from fontsource, so no width compensation was needed
anywhere in it. Colour-keying `#c04935` in both images puts `20:669` at **0px on all four
edges** and `20:670` at 0 on left, right and bottom with its top 2px high — one glyph's
ascender on the opening quote mark, not a placement offset. What is left in 1.817 is glyph
rasterisation and webp loss on the botanicals.

The akad band's ten text nodes all match the render to **0px in both axes**, measured by
colour-keying `#4e685c`, `#623c2a` and `#aa7a3a` in both images. Two things had to be
measured to get there. **Ibarra Real Nova's line-box offset is +1 at 20px and 0 at 16px** —
every 20px node in the band sat 1px high at Figma's own y and both 16px nodes sat exactly
on it, which is one more confirmation that the offset belongs to the (face, size) pair
rather than the face. And its heading is the band's only substitute: Kaleagnetta, a thin
monoline signature script, set in **Sacramento** at 39.3 (48 x 190/232, width-matched on
"Akad Nikah"). Sacramento was picked against Roben Elegante, Pinyon Script, Mr De Haviland
and Herr Von Muellerhoff by rendering all five side by side — the other four all carry
stroke contrast Kaleagnetta does not have. Its ink stands 31 tall against the render's 46,
which is the width-first trade and the band's floor until Kaleagnetta is licensed.

The design's own copy is inconsistent in this band and is reproduced rather than
reconciled: the ornate cartouche prints **Kamis / 27 / Desember 2026** in Indonesian and
the card underneath prints **Saturday, / 06 September 2025** in English. Not the same day,
not the same language. Live data drives both from one `acara` entry
(`formatEventDateId` / `formatEventDate`).

The resepsi band's nine text nodes all match the render to **0px in both axes**, and its
heading is the third node in this frame to prove the width match is per WORD: Sacramento
sets "Resepsi" 126 wide at Figma's own 48 against the render's 113, so it wants **43.8**
where "Akad Nikah" wanted 39.3. At that size it also takes a 1px `top` and a 2px `left`
correction the akad heading did not — the line-box offset moves with the size, exactly as
Ibarra Real Nova's does.

`24:897` is the band's one unresolved layer. It is ornate scrollwork almost entirely buried
under `29:254`; x 0 is the only clip-legal value it can take, its best y scores err 68.7
against 111.9 at its declared y, and **dropping it changes the band by 0.002** — so unlike
`24:916` it is not worth calling `PAINTS_NOTHING`, and unlike the rest of the band its
position is not really known. `solve_alpha` fits it 0.20 screen, which is a fit to noise on
a layer that is invisible either way. Revisit it if the band is ever pushed below 2.

**Resepsi has an unowned residual and it is not `24:916`.** The render carries a pale-blue
chrysanthemum at roughly x 30..90, y 5880..5990 that nothing sliced so far explains: every
exported asset in the repo under 300x450 was scored across that window and the best is 30.2,
which is a bride-band floral and not plausible. `24:916` was the obvious suspect — same art,
and its clip-legal (0, 5790) spans exactly those rows — but scored over the flower head
alone it gives 189.8 there, so it stays in `PAINTS_NOTHING`. The layer therefore belongs to a
band not yet cut, painting upward into resepsi's rows; a flipped node declares a y far below
where it renders, so it will not look like it belongs here until its own band is dumped.
Expect it to close on its own, and re-score resepsi when it does.

Roben Elegante at 32/57 takes **no line-box offset** in the dresscode band, the same as in
the bride and groom bands and unlike the hero's +1. Three bands now agree, so the hero's is
the outlier and the offset belongs to the (face, size, line-height) triple rather than the
face — which is what the table under "The line-box offset is per FACE" already warns.

The gallery band's three Roben Elegante nodes land 0px in both axes. Its fourth text node,
`31:319`, is the frame's hardest and is worth reading before the remaining bands: Figma
reports its family as **"mixed"** at 40 and gives nothing else, and the two runs really are
two faces. "Buat" is Ibarra Real Nova to within a -2px letter-spacing, at the render's own
cap height. "VIDEO PREWED" is not: the render sets those caps 235 wide at a 28 cap height,
with an 'O' 17 wide — 0.61 of cap, where Ibarra needs 0.75 — so glyph for glyph the render's
D, O and E are 35-40% narrower. That is a condensed face this repo does not have, or a text
node squeezed horizontally in Figma; either way the caps take the width-first trade at 28.2
instead of 40, which puts the line's right edge on the render's 473 to the pixel and costs
9px of cap height. On the sheet: 2.465 at 40, 2.210 at 33.2, **2.134** at 28.2.

Two notes on that node beyond its metrics. **A "mixed" family report means measure each run
separately** — one size for the whole string cannot fit both. And the copy itself
("Buat video prewed") advertises a prewedding-video service rather than saying anything
about the wedding; it is reproduced because the render is the specification, and it is the
first thing to delete before the template ships to a real couple.

`shot.mjs` grew one more assertion with this band. The carousel is the only stateful thing
in the sheet, so it is the only thing a screenshot cannot check: the run now clicks "next"
and confirms the oval's `src` actually changed. A wrong modulo reads as a still picture,
which every other check in that file would pass.

The gift band is the cleanest run of the right-edge rule in the frame, and it is worth
keeping as the reference case: **every left-side node declares its RIGHT edge and every
right-side node declares its left one**, in five matched pairs — `45:12`/`45:11`,
`31:417`/`31:418`, `31:423`/`31:422`, `32:457`/`32:458`, `31:427`/`31:428` — plus `31:419`
(an ordinary left bleed at -196) and `31:421` (a mirrored one at 791 -> 417). Only four
needed a pin; the clip rule guessed the right edge for the rest.

**The Copy pill is not in the node dump at all.** Its label `31:408` reports a
parent-relative origin of 24,8 inside a box `flatten_frame.py` never emitted, and the render
shows a 92x41 plate at (252, 9250) filled `#80a2ba`. Both pills land 0px on all four edges
once drawn from those measurements. A paint-bearing auto-layout wrapper is the mirror image
of the cover's `32:461` finding — that one was a wrapper that painted nothing and could be
dropped; this one paints and has to be reconstructed. **When a text node's reported bounds
are parent-relative and no parent is in the dump, the parent is a missing layer, not a
coordinate bug** — its box is `text.abs - text.rel`, and its size is the text's plus twice
that offset.

`shot.mjs` grew a second interaction assertion with this band: it clicks Copy, confirms the
label changes and confirms it reverts. The page context now grants `clipboard-write`, without
which the handler throws and a working button reads as broken.

The wishes band brought two more of the design's own faces, both on fontsource and neither
substituted: **Bellefair** (the form, the timestamps and the message copy) and **Abhaya
Libre ExtraBold** (the card names). Every text node and all four plates land 0px, but three
of them needed a nudge and they do not agree with each other — Abhaya's line box sits 1px
LOW at this size and Bellefair's sits 1px HIGH at both 18 and 20, and the two pills want
their labels centred in 56 rather than the plate's 54. Same per-(face, size) rule as
Ibarra's +1 in the akad band; it is never safe to carry one node's offset to the next.

`33:510`'s size is the odd one: Abhaya Libre ExtraBold sets "Satrio & Istri" **113 x 13** at
Figma's declared 20 where the render has **104 x 12** — the same 0.92 on BOTH axes, which is
a uniform scale rather than the width-vs-height trade every substitute face has forced so
far. One number (18.4) fixes both. Weight 700 renders identically to 800 in this family, so
it is not a weight mismatch; the design's node is simply scaled.

**The cards are a flow, not absolute boxes.** A live message is any number of lines and the
Show more button has to move with them, so the list is one positioned block at `33:510`'s
origin holding cards in normal flow: 147 of copy, a 27 gap, and the button 27 below the
last card. That reproduces the render's rows exactly and still grows. Note the design
itself puts card 2 one pixel right of card 1 (91/91/90 against 92/92/91) — that is
designer noise, not a pattern, and it is deliberately NOT reproduced.

One behaviour bug this band exposed, worth knowing for rsvp: in **design mode** `sendWish`
answers locally, so `wishes` only ever holds rows this visitor just posted. A plain
`live.length ? live : DESIGN` therefore *empties* the guest book the moment someone tries
the form — the default deploy IS design mode, so that is what most people would have seen.
The section keeps the design's cards underneath a locally-posted wish and never mixes them
into live data.

`shot.mjs` now carries three interaction assertions — the gallery carousel, the gift Copy
button and the wish form. The wish check runs **after** the `.sheet` screenshot on purpose:
design mode has no way to un-post a wish, so run earlier it would leave its own test card in
the artifact every later band is eyeballed against.

The rsvp band answers the question its handoff left open: **`submitRsvp` already exists**,
in `lib/api.ts`, posting to `/v1/service/menu/hadir2/{slug}` — and api.ts's own comment
names `RsvpSection` as the reason `DESIGN_MODE` is enforced at the boundary rather than in
`useWedding`. So the section imports it directly, and in design mode the throw is the
designed answer: the form validates, submits, and reports "undangan ini belum terhubung ke
server" in its error line. `shot.mjs` asserts exactly that, in three steps — empty name,
no attendance, then a valid submit — because a form whose click never reaches its handler
looks identical to a working one in a screenshot.

Its five plates are reconstructed from the parent-offset rule the gift band established:
the four fields at (85, 11139 / 11200 / 11261 / 11322), 426 x 54, white with a 1px `#8d9879`
rule and a radius of 10, and Send at (85, 11398) in `#b2d3e2`. All five land 0px, as do all
seven text nodes. `39:7`, the white oval behind the heading, IS a flat `#ffffff` ellipse —
it goes in `CSS_SHAPES` — but that had to be checked rather than assumed: the gallery band's
six ellipses at the same `#d9d9d9` were four masks and two buttons.

One more note on its Send button: the design draws it at full strength, so it is NOT
disabled until the form is valid. A control that greys out before the guest has typed
anything reads as broken rather than as guidance, and the render is the specification.

## The closing band, and what Figma's silence about line-height means

The last band is the busiest: a full-bleed toile (`40:76`), an ornate envelope, a framed
photo and four text nodes. It is also the only node in the frame **clipped on its BOTTOM
edge** — `40:76` declares 671x1565 at y 11452 and exports 596x1366, which is exactly what
is left of the sheet (12818 − 11452). The clip rule handles it unchanged; it is worth
knowing only because every other vertical surprise in this frame has been growth, not a cut.

**When Figma declares no line-height, the FACE's own leading is the first guess** — not the
box height over the line count. `41:92` is four rendered lines in a 162 box, so 40.5 looks
obvious and is wrong: measured line by line the render's pitch is **36**, which is Roben
Elegante's natural 1.8em at 20. Setting 40.5 matched the first line exactly and drifted 16px
by the fourth, which is the shape of this mistake — it always looks right where you check it
first. The box is simply taller than the block it holds.

Its signature `42:3` is the frame's fourth substitute and its second tracking case, in the
opposite direction to the gallery band's promo: Comtic Hiden is a monoline brush script, and
the render sets "The Bride & Groom" 286 x 31 where Sacramento at 24 gives 180 x 27 — 38%
wider PER UNIT HEIGHT. So the height comes from the size (27.6) and the width from a
`letter-spacing` of 4.9, with a matching `text-indent` because CSS also adds the space after
the last glyph and would otherwise push the centred line half a space right.

One thing that is NOT a substitution problem: `42:3` reads "The Bride & Groom" and it stays
a literal. Driving it from `coupleNickname` was wrong twice over — that computed never
returns empty (it falls back to "Ahmad & Salma", the design's other mock), so a fallback
behind it could never fire, and swapping names in changes what the design SAYS rather than
what it shows.

## A masked export carries the mask's BOX and not its SHAPE

Figma clips a masked child to the mask's bounding box and stops there — the mask's own
alpha is never applied — so a child under a SHAPED mask comes back as a full opaque
rectangle of the mask's size.

That is invisible while the mask is a placeholder the size of its child. The gallery's
photo ovals are exactly that (`31:289` declares 403.6x504.6 and exports 308x403, its
oval's box), and they are in `CSS_SHAPES` precisely because the mask has nothing left to
draw once the clip has happened.

It is very visible when the mask is a shaped plate that also PAINTS. `54:33` is the
fountain garden at the foot of the akad card, masked by `23:851`, the card's inner plate,
whose bottom edge is a scallop. Clipped to the plate's box the garden painted straight
through that scallop and ended on a hard horizontal cut 67 rows below where the render has
it — the plate's rectangle, drawn over the card's own edge. Its resepsi twin `54:42` did
the same against `29:241`.

`build_refs.py`'s `MASKED` table now multiplies the child's alpha by the mask's before the
webp is written. **Do not derive the offset by differencing the two declared x values.** A
masked node's declared box is the UNCLIPPED node (`54:33` declares 620x310 at x −11.95),
and a flipped mask reports its RIGHT edge (`29:241` declares x 533 and sits at 62): both
numbers are wrong in the same subtraction, and it is the kind of wrong that looks plausible
on one pair and erases the layer outright on the other. What survives the clip is the
child's own Y — 5618 − 5173 = 445 for akad, 6688 − 6236 = 452 for resepsi, each matching
the position `gen_band` derives independently — and the fact that the export starts at the
mask's LEFT edge by construction. So dx is 0 and dy comes from the declared Ys.

Measured after: akad 1.922 → **1.246**, resepsi 2.102 → **1.175**, the sheet 1.806 →
**1.646**. A ±14 row scan over the akad plate bottoms out at a sharp minimum on 0, so the
plate is aligned as well as shaped.

## Choosing a substitute: measure STROKE WEIGHT, not overlap

Kaleagnetta is the frame's one face with no file, so the akad and resepsi headings stay a
substitute — but the substitute changed, and how it was chosen is the transferable part.

The old choice, Sacramento, was the best of the faces already on fontsource. Sweeping the
126 local font files against the render's own ink — isolated by shooting the sheet with
those two headings hidden and differencing, `text-ink.mjs`'s method — turned up a far
closer cut: **Palisade**.

**Two obvious metrics both rank it wrong, in opposite directions.** Plain IoU on the glyph
masks puts every fat brush face on top and Sacramento LAST of 127, because a hairline
stroke 2px out of place overlaps nothing while a blob overlaps everything. Dilating both
masks first and scoring F1-within-2px inverts the bias but not the outcome: the fat faces
still win, now on recall. Both are measuring stroke weight and calling it letterform.

**What works is measuring stroke weight on purpose.** Ink density (lit px over ink-box
area) plus aspect, at a common width:

| face | density | aspect |
|---|---|---|
| Kaleagnetta (the render) | 0.144 | 4.02 |
| **Palisade** | **0.143** | **4.22** |
| Sacramento (old stand-in) | 0.185 | 6.21 |

Sacramento is a third heavier and half again as wide for its height, which is exactly why
its width match left the ink 31 tall against the render's 48. Palisade width-matched leaves
it at 48 — `23:856`'s ink box now lands at **dx 0, dy 0, dw 0, dh 0** against the render,
the first time a substituted node in this frame has done that.

Width is still matched per WORD, not per face: Palisade sets "Akad Nikah" at 3.685 design
px per px of font-size and "Resepsi" at 1.89, so Figma's one authored 48 becomes 52.4 and
60.8. `103:11` keeps a height deviation — 63 against the render's 52, Palisade's 'p'
descender running deeper than Kaleagnetta's — which is the usual width-first trade and the
floor until the real file is licensed.

## A rotated node reports its transform ORIGIN, not its render box

The closing band's four botanicals — `52:11`, `52:12`, `61:619`, `61:620` — were the
frame's last real placement error, and they were held in place by two mistakes propping
each other up.

**The position.** All four are ROTATED, and a rotated node's reported x is the corner of
its UNROTATED box at the transform origin, not the left edge of the box it renders into.
Rotate `52:12`'s 251x251 by its own −159.09° about that origin and the bbox left comes out
at 483.51 − 234.5 = **249.0**, against the **249.05** Figma's own properties panel shows.
The dump has no `rotation` field and neither does the MCP read, so nothing in the pipeline
could see this; `reconcile()`'s "export grew, so re-centre" branch fires (324 > 251) and
produces a plausible-looking wrong answer.

**The alpha on top of it.** `solve_alpha.py` then fitted each layer where it had been put,
and from 90–230px off its home the only way to score is to fade out — `52:12` came back at
0.4/screen, `61:619` at 0.55/screen. That is the same trap `15:192` and `16:491`/`16:493`
fell into, recorded above, and it is worth stating as a rule: **a solved alpha near zero is
evidence about the POSITION, not about the design.** It also blinds the recovery, because
`locate.py` has no ink left to match — err 56 and 140, which read as "occluded" and mean
"we faded it out ourselves".

**How they were recovered, with no rotation data.** Difference the 1x render against a
sheet built with the four hidden; what is left is exactly the ink the design draws and the
build does not. Then Hough-vote it: every (asset ink point → residual point) pair votes for
one offset, and the winning bin is the placement. `52:12` came back at 250, 11934 —
Figma's own panel to 1px, derived independently of it. All four then want full strength,
and every axis is a sharp minimum: ±3 and ±6 on each of x and y scores worse, as does
restoring either solved alpha. Pinned in `gen_band.py`'s `PIN_X` / `PIN_Y` / `PIN_A` /
`PIN_B`; the band goes **2.846 → 2.156** and the sheet 1.646 → **1.588**.

The pattern across all four is worth carrying to the next rotated node: **Y was already
right and only X moved.**

(Checked while doing this: a fresh 1x export of Frame 1 diffs against the stored
`.figma-tmp/frame1-3-1x.png` at 0.017/255, and 0.000 on every band. The reference render on
disk is current — if a band disagrees with it, the build is wrong, not the ref.)

## A probe that does not walk the sheet scores nothing

Band art is `loading="lazy"` and every band below the fold is viewport-gated, so a
screenshot taken without scrolling the page first catches a sheet with almost no artwork
on it. `sheet-shot.mjs` walks the whole scroll height in 400px steps for exactly this
reason. A one-off probe script that skips the walk does NOT come back with a slightly
worse number -- it comes back with the SAME number for every variant, because what it is
measuring is the empty sheet.

That cost a wrong conclusion here: three different overrides on the closing band all
scored 24.5, which read as "every one of these is catastrophic" when it meant "none of
these was rendered". Any probe that reports an identical score for changes that cannot
possibly be identical is measuring its own harness. Re-run the canonical loop before
believing it.

With the walk in place the same overrides read: baseline **2.846**, `61:619` at full
strength 3.247, `52:12` at full strength 3.021, and both sprigs hidden outright 2.840. So
the solved `a`/`b` on those layers are right, and `52:11` / `52:12` contribute nothing
either way -- the closing band's edge botanicals are not a blend problem.

## Known residuals, now that every band is cut

| where | what | worth |
|---|---|---|
| bismillah | two substitute faces (Perpetua, and an Arabic fallback for Alex Brush) | ~2.5 of its 4.251 |
| closing | the blurred botanicals `52:11` / `52:12` / `40:81` | most of its 2.846 |
| gallery | the promo caps' condensed face, and photo webp loss | ~0.5 |
| resepsi | `24:897`, buried scrollwork whose position is not really known | ~0 |
| resepsi | a pale-blue chrysanthemum at x 30..90, y 5880..5990 that no asset explains | unknown |
| akad | the left column, x 0..99 — pinned layers `22:837` / `22:846` at scan positions | ~0.2 |
| closing | the blurred botanicals — glyph diff and webp loss are most of what is left | ~0.4 of its 2.156 |

The closing band's edge botanicals turned out to be a solved problem rather than an open
one — see "a rotated node reports its transform origin" below.

The chrysanthemum is the older open QUESTION of the same kind: it belongs to a node
that renders far from where it is declared, and every band is now cut, so it is either a
layer this frame draws twice or one whose declared y is a bottom edge nothing tested.
