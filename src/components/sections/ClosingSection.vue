<script setup lang="ts">
/*
 * Frame 1 (1:3) band "closing": y 11452..12818 of the body frame — the last one. A toile
 * backdrop, the thank-you, a framed photo and the credit line. Art comes from
 * src/lib/bands/closing.ts (GENERATED, scripts/gen_band.py).
 *
 * `40:76`, the toile, is the only node in the frame clipped on its BOTTOM edge: it
 * declares 671x1565 at y 11452 and exports 596x1366, which is exactly what is left of the
 * frame (12818 - 11452). Both axes clip for the same reason, one against the sides and
 * one against the end of the sheet.
 */
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/closing'
import { useReveal } from '../../composables/useReveal'

const { el, shown } = useReveal(0.15)

/*
 * 41:92 — three authored lines; the middle one wraps inside the 486 box, which is why
 * the render shows four. Written as a constant because Vue folds a template's own
 * newlines into spaces (see SLICING.md, "The Vue newline trap").
 */
const MESSAGE =
  'And So, Our Story Begins\nWith hearts full of love, we look forward to celebrating this beautiful beginning with you.\nWith Love,'

/*
 * 42:3 — the design signs off with the ROLES, not the names, and that stays a literal.
 * Driving it from `coupleNickname` looked tempting and was wrong twice over: that
 * computed never returns empty (it falls back to "Ahmad & Salma", the design's OTHER
 * mock), so the fallback here could never fire, and swapping names in changes what the
 * design says rather than what it shows.
 */
</script>

<template>
  <section
    :ref="el"
    class="band closing"
    :class="{ 'is-in': shown }"
    aria-labelledby="closing-title"
  >
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 99:7 — the sign-off. -->
    <h2 id="closing-title" class="closing__title">Thank You !</h2>

    <!-- 41:92 — the message. -->
    <p class="closing__message">{{ MESSAGE }}</p>

    <!--
      42:3 — the design's string begins with U+2028, a line separator, so its first line
      is empty and the words sit on the second. Reproduced with the break rather than by
      moving `top`, so the box still matches Figma's.
    -->
    <p class="closing__signature"><br />The Bride &amp; Groom</p>

    <!-- 45:8 — the maker's credit, at the very foot of the sheet. -->
    <p class="closing__credit">Created by 25ribuaja x Qinvi</p>
  </section>
</template>

<style scoped>
.closing {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 99:7 — Roben Elegante Script 40, #aa7a3a. Figma declares no line-height; the box's 61. */
.closing__title {
  --delay: 80ms;
  z-index: 261;
  top: calc(116 * var(--px)); /* 99:7 box y 11563 + 5 — Roben Elegante at 40/61 */
  left: calc(55.05 * var(--px));
  width: calc(486 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(40 * var(--px));
  line-height: calc(61 * var(--px));
  color: #aa7a3a;
}

/*
 * 41:92 — Roben Elegante Script 20, #aa7a3a, centred. Figma declares no line-height, and
 * the obvious guess — the box's 162 over the four lines the render shows, 40.5 — is WRONG:
 * measured line by line the render's pitch is 36, which is Roben Elegante's own leading at
 * 20 (1.8em). The box is simply taller than the text block it holds. Setting 40.5 matched
 * the first line and drifted 16px by the fourth.
 *
 * So: when Figma declares no line-height, the FACE's natural leading is the first guess and
 * box-height/lines is only a coincidence when the two agree.
 */
.closing__message {
  --delay: 200ms;
  z-index: 260;
  top: calc(206 * var(--px)); /* 41:92 box y 11657 + 3 — measured */
  left: calc(55.05 * var(--px));
  width: calc(486 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(36 * var(--px)); /* NOT the box's 162/4 — see the note above */
  white-space: pre-line;
  color: #aa7a3a;
}

/*
 * 42:3 — Comtic Hiden 24 at 178% line-height, #aa7a3a. Comtic Hiden is a monoline brush
 * script and is not on fontsource, so this is Sacramento again (--font-hand). Unlike the
 * akad and resepsi headings the trade here is not size alone: the render's ink is 286 x 31
 * where Sacramento at 24 gives 180 x 27, which is 38% wider PER UNIT HEIGHT. That is
 * tracking, not a size, so the height is matched with the size (27.6) and the width with
 * a letter-spacing — the mirror of the gallery band's promo caps, which needed the
 * opposite sign.
 */
.closing__signature {
  --delay: 320ms;
  z-index: 262;
  top: calc(344 * var(--px)); /* 42:3 box y 11797 - 1 — measured */
  left: calc(105.05 * var(--px)); /* 42:3 box x 104.05 + 1 — measured */
  width: calc(387 * var(--px));
  font-family: var(--font-hand);
  font-weight: 400;
  font-size: calc(27.6 * var(--px));
  line-height: calc(42.72 * var(--px)); /* Figma's 178% of 24 */
  letter-spacing: calc(4.9 * var(--px));
  /* Trailing letter-spacing widens the line to the right; pull the block back by half. */
  text-indent: calc(4.9 * var(--px));
  color: #aa7a3a;
}

/* 45:8 — Roben Elegante Script 20, #aa7a3a. The box's own 56 for line-height. */
.closing__credit {
  --delay: 440ms;
  z-index: 290;
  top: calc(1317 * var(--px)); /* 45:8 box y 12779 - 10 — Roben Elegante at 20/56 */
  left: calc(55.05 * var(--px));
  width: calc(486 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(56 * var(--px));
  color: #aa7a3a;
}
</style>
