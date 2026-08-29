<script setup lang="ts">
/*
 * Frame 1 (1:3) band "bismillah": y 1802..2161 of the body frame. The gold Basmala
 * opens the invitation proper; under it the dark-green greeting and the blue script
 * line close the sentence the greeting begins. Art comes from
 * src/lib/bands/bismillah.ts (GENERATED, scripts/gen_band.py).
 *
 * Fonts: Figma set Perpetua (greeting), Activists ("journey together") and Alex Brush
 * (Basmala) — none on fontsource. Perpetua → Ibarra Real Nova (same old-style serif
 * bones), Activists → Pinyon Script (the loaded script), and Alex Brush cannot render
 * Arabic at all, so the Basmala is set in Amiri, an Arabic Naskh, instead. Sizes,
 * line-heights and colours are Figma's own; only the faces were swapped.
 */
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/bismillah'
import { useReveal } from '../../composables/useReveal'

const { el, shown } = useReveal(0.15)
</script>

<template>
  <section :ref="el" class="band bismillah" :class="{ 'is-in': shown }" aria-labelledby="basmala">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->
    <p id="basmala" class="bismillah__basmala" lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</p>

    <!-- 19:558 — the design folds the line break itself; the box keeps white-space: pre-line. -->
    <p class="bismillah__greeting">
      Assalamu'alaikum Warahmatullahi Wabarakatuh
      With grateful hearts, we begin this sacred
    </p>

    <!-- 19:569 — the sentence's last line, set as its own node in the design. -->
    <p class="bismillah__script">journey together</p>
  </section>
</template>

<style scoped>
.bismillah {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * `top`s are Figma's box y (band-local) PLUS 1 — same measured line-box offset as the
 * hero's and countdown's text nodes. The design's font-size/line-height are untouched.
 */

/* 19:567 — Amiri 40, #c18e3f, centred. Alex Brush (Figma's face) has no Arabic glyphs. */
.bismillah__basmala {
  --delay: 60ms;
  z-index: 106;
  top: calc(1 * var(--px)); /* box y 1802 + 1 */
  left: calc(124 * var(--px));
  width: calc(348 * var(--px));
  font-family: var(--font-basmala);
  font-weight: 400;
  font-size: calc(40 * var(--px));
  line-height: calc(50 * var(--px));
  color: #c18e3f;
}

/* 19:558 — Ibarra Real Nova 22/33, #2c4b34. Perpetua (Figma's face) → Ibarra. */
.bismillah__greeting {
  --delay: 140ms;
  z-index: 104;
  top: calc(73 * var(--px)); /* box y 1874 + 1 */
  left: calc(51 * var(--px));
  width: calc(493 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(22 * var(--px));
  line-height: calc(33 * var(--px));
  white-space: pre-line;
  color: #2c4b34;
}

/* 19:569 — Pinyon Script 32/33, #679ece. Activists (Figma's face) → Pinyon. */
.bismillah__script {
  --delay: 220ms;
  z-index: 105;
  top: calc(163 * var(--px)); /* box y 1964 + 1 */
  left: calc(51 * var(--px));
  width: calc(493 * var(--px));
  font-family: var(--font-script-date);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(33 * var(--px));
  color: #679ece;
}
</style>
