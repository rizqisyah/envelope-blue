<script setup lang="ts">
/*
 * Frame 1 (1:3) band "quote": y 4021..4425 of the body frame. The Ar-Rum verse on a
 * white cartouche, over the green valley. Art comes from src/lib/bands/quote.ts
 * (GENERATED, scripts/gen_band.py).
 *
 * The first band with no mirror to lean on, and the first with no substitute face:
 * Cinzel and Cormorant Infant are both the design's own and both ship from fontsource,
 * so every number below is Figma's, with no width compensation anywhere.
 *
 * Its cartouche (23:882) and both florals (20:762 / 20:763) are position-pinned — see
 * the block above PIN_Y in scripts/gen_band.py for what the chain got wrong and why.
 */
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/quote'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'

const { el, shown } = useReveal(0.15)
const { quoteText, quoteVerse } = useWedding()
</script>

<template>
  <section :ref="el" class="band quote" :class="{ 'is-in': shown }" aria-labelledby="quote-verse">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 20:669 — the credit, and the band's heading. -->
    <h2 id="quote-verse" class="quote__verse">{{ quoteVerse }}</h2>

    <!-- 20:670 — one sentence, no authored breaks: it wraps inside its own 245 box. -->
    <blockquote class="quote__text">{{ quoteText }}</blockquote>
  </section>
</template>

<style scoped>
.quote {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 20:669 — Cinzel Bold 24/36, #c04935, centred in a 198 box at x 199.6. */
.quote__verse {
  --delay: 120ms;
  z-index: 136;
  top: calc(205 * var(--px)); /* 20:669 box y 4226, band-local 205 */
  left: calc(199.6 * var(--px));
  width: calc(198 * var(--px));
  font-family: var(--font-verse);
  font-weight: 700;
  font-size: calc(24 * var(--px));
  line-height: calc(36 * var(--px));
  color: #c04935;
}

/*
 * 20:670 — Cormorant Infant Medium 18/25.56, #c04935, centred in a 245 box at x 176.05.
 * No `white-space` override, unlike the bride's and groom's parents lines: this is a
 * single string with no authored newlines, and the render's eight lines are the box's
 * own wrap. If a line ever breaks a word early, check the WIDTH before reaching for a
 * manual break — the box is the specification.
 */
.quote__text {
  --delay: 260ms;
  z-index: 137;
  top: calc(254 * var(--px)); /* 20:670 box y 4275, band-local 254 */
  left: calc(176.05 * var(--px));
  width: calc(245 * var(--px));
  font-family: var(--font-body);
  font-weight: 500;
  font-size: calc(18 * var(--px));
  line-height: calc(25.56 * var(--px));
  color: #c04935;
}
</style>
