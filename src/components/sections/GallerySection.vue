<script setup lang="ts">
/*
 * Frame 1 (1:3) band "gallery": y 7750..8865 of the body frame. An oval carousel with
 * two arrows, a row of three thumbnails, and the promo card at the foot. Art comes from
 * src/lib/bands/gallery.ts (GENERATED, scripts/gen_band.py).
 *
 * The band's four photos are MASKED, and Figma exports a masked node already clipped:
 * 31:289 declares 403.6x504.6 and exports 308x403, which is exactly its mask 31:288's
 * box. So the mask's box is the photo's position, and the mask nodes themselves paint
 * nothing — all six of the band's ELLIPSEs are in build_refs.py's CSS_SHAPES, four as
 * masks and two as the arrow buttons, which are solid #d9d9d9 (sampled opaque off the
 * render, not translucent).
 *
 * The photos are drawn here rather than by BandArt so live gallery rows can replace them.
 * A live photo is rectangular, so its oval comes from the container's border-radius; the
 * design's own exports are already oval and the radius is a no-op over them.
 */
import { computed, ref, watch } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gallery'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { assets } from '../../lib/bandAssets'

const { el, shown } = useReveal(0.15)
const { gallery } = useWedding()

// Drawn below instead of pasted: the four photos and the two chevrons (which sit on
// real buttons). Everything else in the table is art.
const DRAWN = ['31:289', '31:295', '31:301', '31:304', '31:314', '31:315']

const chevronLeft = assets['gallery/parts/31-314.webp']
const chevronRight = assets['gallery/parts/31-315.webp']

/*
 * `image_url` / `caption` are the field names template 5's gallery settled on. With no
 * live gallery the design's own four exports stand in, so an unconfigured render matches
 * the frame and the carousel still works.
 */
const DESIGN_PHOTOS = [
  { src: assets['gallery/parts/31-289.webp'], caption: '' },
  { src: assets['gallery/parts/31-295.webp'], caption: '' },
  { src: assets['gallery/parts/31-301.webp'], caption: '' },
  { src: assets['gallery/parts/31-304.webp'], caption: '' },
]

const photos = computed(() => {
  const live = (gallery.value as any[])
    .map((g) => ({ src: g?.image_url as string, caption: (g?.caption as string) || '' }))
    .filter((p) => p.src)
  return live.length ? live : DESIGN_PHOTOS
})

const active = ref(0)
watch(photos, () => (active.value = 0))

const step = (d: number) => {
  const n = photos.value.length
  if (n) active.value = (active.value + d + n) % n
}

/*
 * The thumbnail row is a window that FOLLOWS the active photo — the three after it,
 * wrapping. A fixed first-three row would leave photo 8 of 10 unreachable by tap; this
 * way the arrows and the thumbnails both reach everything, and with the design's own
 * four the row shows exactly the three the render shows.
 */
const THUMBS = [
  { id: '31:295', x: 146 },
  { id: '31:301', x: 255 },
  { id: '31:304', x: 364 },
]
const thumbs = computed(() =>
  THUMBS.map((t, i) => {
    const n = photos.value.length
    const at = n ? (active.value + i + 1) % n : 0
    return { ...t, at, photo: photos.value[at] }
  }),
)

// 31:307 / 31:308 — 48x57 at y 8246, band-local 496. Their chevrons sit at different
// offsets inside them (12 and 21); that is the design, measured, not a slip.
const BUTTONS = [
  { id: '31:307', x: 128, z: 186, chev: chevronLeft, chevX: 12, dir: -1, label: 'Foto sebelumnya' },
  { id: '31:308', x: 436, z: 187, chev: chevronRight, chevX: 21, dir: 1, label: 'Foto berikutnya' },
]
</script>

<template>
  <section
    :ref="el"
    class="band gallery"
    :class="{ 'is-in': shown }"
    aria-labelledby="gallery-title"
  >
    <BandArt :layers="LAYERS" :skip="DRAWN" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 31:284 / 31:317 — the heading and its line. -->
    <h2 id="gallery-title" class="gallery__title">Our Dearest Memories</h2>
    <p class="gallery__lede">Scenes from a love story we shall cherish evermore.</p>

    <!-- 31:288 + 31:289 — the oval, live. -->
    <div class="gallery__oval">
      <img
        v-if="photos[active]"
        :src="photos[active].src"
        :alt="photos[active].caption || 'Foto pasangan'"
        loading="lazy"
        decoding="async"
      />
    </div>

    <!-- 31:307 / 31:308 + their chevrons — real buttons, so the arrows work. -->
    <button
      v-for="b in BUTTONS"
      :key="b.id"
      type="button"
      class="gallery__nav"
      :style="{ zIndex: b.z, left: `calc(${b.x} * var(--px))` }"
      :aria-label="b.label"
      @click="step(b.dir)"
    >
      <img :src="b.chev" alt="" :style="{ left: `calc(${b.chevX} * var(--px))` }" />
    </button>

    <!-- 31:310 — the thumbnail row's heading. -->
    <p class="gallery__strip-title">Portraits of Affection</p>

    <!-- 31:294 / 31:300 / 31:303 + their photos — the strip, live. -->
    <button
      v-for="t in thumbs"
      :key="t.id"
      type="button"
      class="gallery__thumb"
      :style="{ left: `calc(${t.x} * var(--px))` }"
      :aria-label="`Lihat foto ${t.at + 1}`"
      @click="active = t.at"
    >
      <img
        v-if="t.photo"
        :src="t.photo.src"
        :alt="t.photo.caption || ''"
        loading="lazy"
        decoding="async"
      />
    </button>

    <!--
      31:319 — the design's own promo copy over 31:318's photo card. It advertises a
      prewedding-video service rather than saying anything about this wedding, so it is
      the first thing to delete if the template ships to a real couple; it is reproduced
      here because the render is the specification.
    -->
    <p class="gallery__promo"><span>Buat </span>VIDEO PREWED</p>
  </section>
</template>

<style scoped>
.gallery {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 31:284 — Roben Elegante Script 32, #aa7a3a, centred. Box's own 57 for line-height. */
.gallery__title {
  --delay: 80ms;
  z-index: 225;
  top: calc(184 * var(--px)); /* 31:284 box y 7934, band-local 184 */
  left: calc(106.05 * var(--px));
  width: calc(383 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
  color: #aa7a3a;
}

/* 31:317 — Roben Elegante Script 20/24, #aa7a3a, LEFT aligned and wrapped by its box. */
.gallery__lede {
  --delay: 180ms;
  z-index: 229;
  top: calc(255 * var(--px)); /* 31:317 box y 8005, band-local 255 */
  left: calc(51 * var(--px));
  width: calc(208 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(24 * var(--px));
  text-align: left;
  color: #aa7a3a;
}

/* 31:288's box, 308x403 at y 8062. The photo fills it and the radius cuts the oval. */
.gallery__oval {
  --delay: 300ms;
  z-index: 179;
  top: calc(312 * var(--px)); /* 31:288 box y 8062, band-local 312 */
  left: calc(152 * var(--px));
  width: calc(308 * var(--px));
  height: calc(403 * var(--px));
  border-radius: 50%;
  overflow: hidden;
}

.gallery__oval img,
.gallery__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 31:307 / 31:308 — 48x57, solid #d9d9d9, opaque. */
.gallery__nav {
  --delay: 420ms;
  top: calc(496 * var(--px)); /* 31:307 box y 8246, band-local 496 */
  width: calc(48 * var(--px));
  height: calc(57 * var(--px));
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #d9d9d9;
  cursor: pointer;
  /* `scale`, not a transform: the band's reveal owns `transform` and would win. */
  transition: background 240ms ease, scale 240ms ease;
}

.gallery__nav img {
  position: absolute;
  top: calc(16 * var(--px)); /* 31:314 / 31:315 y 8262 against the button's 8246 */
  width: calc(13.5 * var(--px));
  height: calc(25.5 * var(--px));
}

.gallery__nav:hover,
.gallery__nav:focus-visible {
  background: #ececeb;
  scale: 1.08;
}

/* 31:310 — Roben Elegante Script 24/34, #aa7a3a, centred. */
.gallery__strip-title {
  --delay: 520ms;
  z-index: 228;
  top: calc(652 * var(--px)); /* 31:310 box y 8402, band-local 652 */
  left: calc(405.05 * var(--px));
  width: calc(195 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(24 * var(--px));
  line-height: calc(34 * var(--px));
  color: #aa7a3a;
}

/* 31:294 / 31:300 / 31:303 — 102x119 at y 8478, band-local 728. */
.gallery__thumb {
  --delay: 620ms;
  z-index: 181;
  top: calc(728 * var(--px));
  width: calc(102 * var(--px));
  height: calc(119 * var(--px));
  padding: 0;
  border: 0;
  border-radius: 50%;
  overflow: hidden;
  background: none;
  cursor: pointer;
  transition: scale 240ms ease;
}

.gallery__thumb:hover,
.gallery__thumb:focus-visible {
  scale: 1.05;
}

/*
 * 31:319 — the design's promo line, and the band's only real fight.
 *
 * Figma reports its family as "mixed" at 40 and gives no more, and the two runs really are
 * two faces. "Buat" is close to Ibarra Real Nova: at Figma's own 40 it sets 76 wide against
 * the render's 70, and a -2px letter-spacing closes that exactly, at the render's own cap
 * height. "VIDEO PREWED" is not: the render's caps are 235 wide at a 28 cap height, an 'O'
 * only 17 wide (0.61 of cap), where Ibarra at the same cap height needs 325. That is not
 * tracking — measured glyph by glyph the render's D, O and E are 35-40% narrower — it is a
 * condensed face this repo does not have, or a text node squeezed horizontally in Figma.
 *
 * So the caps take the width-first trade SLICING.md calls for: 28.2 instead of 40, which
 * puts the line's right edge on the render's 473 to the pixel and costs the caps 9px of
 * height. Scoring the alternatives on the sheet: caps at 40 gives the band 2.465, at 33.2
 * 2.210, at 28.2 **2.134**.
 */
.gallery__promo {
  --delay: 760ms;
  z-index: 268;
  top: calc(960 * var(--px)); /* 31:319 box y 8725 - 15 — measured, see above */
  left: calc(153 * var(--px)); /* 31:319 box x 154 - 1 — measured */
  width: calc(323 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(28.2 * var(--px));
  line-height: calc(48 * var(--px));
  white-space: nowrap;
  color: #000000;
}

/* "Buat" is the other half of Figma's "mixed". */
.gallery__promo span {
  font-size: calc(40 * var(--px));
  letter-spacing: calc(-2 * var(--px));
}

@media (prefers-reduced-motion: reduce) {
  .gallery__nav,
  .gallery__thumb {
    transition: none;
  }
}
</style>
