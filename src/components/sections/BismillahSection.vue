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

/*
 * 19:558 — the design breaks this line itself, and the break has to live in a script
 * constant. Written inline in the template it does not survive: Vue's parser folds the
 * source newline to a space, so `white-space: pre-line` has nothing left to preserve and
 * the sentence wraps wherever it happens to fit. That is exactly what the first pass did
 * — and it silently invalidates every width measured off it, because the measurement is
 * then of a wrap point rather than of the design's own line.
 */
const GREETING = "Assalamu'alaikum Warahmatullahi Wabarakatuh\nWith grateful hearts, we begin this sacred"
</script>

<template>
  <section :ref="el" class="band bismillah" :class="{ 'is-in': shown }" aria-labelledby="basmala">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->
    <p id="basmala" class="bismillah__basmala" lang="ar" dir="rtl">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</p>

    <!-- 19:558 — the design folds the line break itself; the box keeps white-space: pre-line. -->
    <p class="bismillah__greeting">{{ GREETING }}</p>

    <!-- 19:569 — the sentence's last line, set as its own node in the design. -->
    <p class="bismillah__script">journey together</p>
  </section>
</template>

<style scoped>
.bismillah {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * All three faces here are SUBSTITUTES, so unlike the hero and the countdown none of
 * these sizes is Figma's own. Per SLICING.md, retiring a face means re-measuring: each
 * font-size below is the design's, scaled by the ratio of the Figma render's ink WIDTH to
 * the live one's, measured by keying on each node's own fill colour (the toile defeats
 * ink-box.py's most-common-colour threshold). line-heights stay at the design's values so
 * the lines keep their baselines. `top`s are Figma's box y exactly — the hero's +1 is
 * Lancelot/Roben's line-box offset and does not transfer.
 */

/*
 * 19:567 — #c18e3f, centred. Figma names Alex Brush, which carries no Arabic at all, so
 * the render is Figma's own fallback Naskh; ours is Amiri. Amiri sets this line 273 wide
 * against the render's 344, so the design's 40 is scaled by 344/273 = 1.26 -> 50.4.
 * Matching the WIDTH is the right call over the height: Amiri's diacritics stack taller
 * than the render's face and no single size satisfies both.
 */
.bismillah__basmala {
  --delay: 60ms;
  z-index: 106;
  top: calc(-10 * var(--px)); /* 19:567 box y 1802, less the 10px Amiri sets low — measured */
  /*
   * Widened from Figma's 348 box, keeping its centre axis (124 + 348/2 = 298), and held
   * to one line. The render's own ink is 344 wide inside a 348 box, so ANY substitute
   * that sets even slightly wider wraps — which is what the first compensated pass did,
   * and a wrapped line measures NARROWER, so the tuning loop then chases it the wrong way.
   */
  left: calc(51.5 * var(--px));
  width: calc(493 * var(--px));
  white-space: nowrap;
  font-family: var(--font-basmala);
  font-weight: 400;
  font-size: calc(50.4 * var(--px)); /* 40 x 1.26 — see above */
  line-height: calc(50 * var(--px));
  color: #c18e3f;
}

/*
 * 19:558 — #2c4b34. Perpetua -> Ibarra Real Nova, which of the loaded serifs needs the
 * LEAST distortion: measured in the browser at the design's own 22px, Ibarra sets this
 * line 446.5 wide, Lancelot 437.1, EB Garamond 475.5 and Cormorant Infant 482, against
 * the render's 372. So 372/446.5 = 0.833 and the design's 22 becomes 18.3. line-height
 * stays 33 so both lines keep the design's baselines.
 */
.bismillah__greeting {
  --delay: 140ms;
  z-index: 104;
  top: calc(72 * var(--px)); /* 19:558 box y 1874, band-local 72 */
  left: calc(51 * var(--px));
  width: calc(493 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(18.3 * var(--px)); /* 22 x 0.833 — see above */
  line-height: calc(33 * var(--px));
  white-space: pre-line;
  color: #2c4b34;
}

/*
 * 19:569 — #679ece. The Figma string is lowercase "journey together" and the face is
 * "Activists", but the RENDER draws wide-spaced CAPITALS: Activists puts cap-height forms
 * on its lowercase, which is the case-pair trap SLICING.md warns about — read the render,
 * not the string. Setting this in a script face (the first pass used Pinyon) reproduces
 * the characters and not the design.
 *
 * Activists is a condensed high-contrast didone — 16 tracked capitals in 227.5px at a
 * 24px cap height — and nothing loaded here is that narrow. Cormorant Infant is the
 * closest in colour and contrast, so the WIDTH is matched (SLICING.md's rule: width moves
 * far more than height when a face is swapped) at font-size 23, and the caps land ~21.6
 * against the render's 24. That ~10% short cap height is a recorded deviation, not a
 * placement error, and it is the floor for this node until the real face is licensed.
 */
.bismillah__script {
  --delay: 220ms;
  z-index: 105;
  top: calc(162 * var(--px)); /* 19:569 box y 1964, band-local 162 */
  left: calc(51 * var(--px));
  width: calc(493 * var(--px));
  font-family: var(--font-caps);
  font-weight: 400;
  font-size: calc(23 * var(--px)); /* width-matched to the render's 227.5 ink — see above */
  line-height: calc(33 * var(--px));
  text-transform: uppercase;
  color: #679ece;
}
</style>
