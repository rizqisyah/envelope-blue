<script setup lang="ts">
/*
 * Frame 1 (1:3) band "dresscode": y 7034..7750 of the body frame. A heading, four
 * palette swatches, one line of copy, and the tall floral arch that carries the sheet
 * into the gallery. Art comes from src/lib/bands/dresscode.ts (GENERATED,
 * scripts/gen_band.py).
 *
 * The first band in this frame that needed no position pin at all: all five of its art
 * layers are either fully inside the frame or bleed off BOTH edges, so the clip rule and
 * locate agree on every one (err 2.3 / 7.4 / 27.8).
 *
 * Its four swatches are the frame's first CSS shapes. They are ELLIPSE nodes with a
 * single solid fill and nothing else, so they are listed in build_refs.py's CSS_SHAPES
 * and drawn here instead of exported — a border-radius reproduces them exactly where a
 * 68x71 webp only approximates.
 */
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/dresscode'
import { useReveal } from '../../composables/useReveal'

const { el, shown } = useReveal(0.15)

/*
 * 29:275 / 29:276 / 29:277 / 30:281 — Figma's own fills and x positions, all at y 7115
 * and all 68x71 (an ellipse, not a circle). No API field carries a palette, so these are
 * the design's values full stop.
 */
const SWATCHES = [
  { id: '29:275', z: 173, x: 102, fill: '#dbc58e' },
  { id: '29:276', z: 174, x: 210, fill: '#9bccdb' },
  { id: '29:277', z: 175, x: 318, fill: '#bde0b5' },
  { id: '30:281', z: 176, x: 426, fill: '#edcbe3' },
]
</script>

<template>
  <section
    :ref="el"
    class="band dresscode"
    :class="{ 'is-in': shown }"
    aria-labelledby="dresscode-title"
  >
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 29:236 — the heading. -->
    <h2 id="dresscode-title" class="dresscode__title">Dresscode</h2>

    <!-- The palette. Decorative: the line below names what it means. -->
    <div
      v-for="(s, i) in SWATCHES"
      :key="s.id"
      class="dresscode__swatch"
      aria-hidden="true"
      :style="{
        zIndex: s.z,
        left: `calc(${s.x} * var(--px))`,
        background: s.fill,
        '--delay': `${200 + i * 90}ms`,
      }"
    />

    <!-- 29:279 — the instruction. -->
    <p class="dresscode__copy">Kindly dress in shades of our wedding palette.</p>
  </section>
</template>

<style scoped>
.dresscode {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * 29:236 — Roben Elegante Script 32, #aa7a3a, centred in a 452 box at x 72. The design's
 * own face. Figma declares no line-height, so the box's own 57 stands in for it.
 */
.dresscode__title {
  --delay: 80ms;
  z-index: 224;
  top: 0; /* 29:236 box y 7034, band-local 0 */
  left: calc(72 * var(--px));
  width: calc(452 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
  color: #aa7a3a;
}

/* 68 x 71 at y 7115, band-local 81. Ellipses, so 50% both ways rather than a circle. */
.dresscode__swatch {
  top: calc(81 * var(--px));
  width: calc(68 * var(--px));
  height: calc(71 * var(--px));
  border-radius: 50%;
}

/* 29:279 — Ibarra Real Nova 20/30, #4e685c. +1 is the face's line box at 20px. */
.dresscode__copy {
  --delay: 620ms;
  z-index: 177;
  top: calc(153 * var(--px)); /* 29:279 box y 7186 + 1 */
  left: calc(53 * var(--px));
  width: calc(490 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #4e685c;
}
</style>
