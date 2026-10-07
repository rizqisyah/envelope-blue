<script setup lang="ts">
/*
 * Frame 1 (1:3) band "hero": y 0..1108 of the body frame. The scene the invitation
 * opens onto — toile wallpaper, the couple in their arched plate, and the florals
 * banked down both edges.
 *
 * Art comes from src/lib/bands/hero.ts, which is GENERATED (scripts/gen_band.py) and
 * must be regenerated rather than hand-nudged. Only the three text nodes live here,
 * because they stay live so useWedding() can drive them.
 */
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/hero'
import { useFitText } from '../../composables/useFitText'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'

/*
 * The hero is the band the invitation OPENS on, so it must not wait for a scroll.
 * Its default gate never fires in time: while the cover plays its 2.4s leave it is
 * still in flow above the sheet, which puts the hero's top at ~852px in an 812px
 * viewport, and the reveal only fires once the cover is removed — about 3s after the
 * tap. Until then the reader watches an empty blue sheet rise to meet the receding
 * cover, which is the one moment the choreography is built around.
 *
 * A bottom rootMargin of 100% grows the observer's box by a full viewport, so the
 * band counts as on screen the instant the sheet is displayed and assembles WITH the
 * fade-in instead of after it.
 */
const { el, shown } = useReveal(0, '0px 0px 100% 0px')
const { coupleNickname, hashtag, customHeroPhoto } = useWedding()

// The one box whose content is live and can run long — see the rule on .hero__couple.
const fitCouple = useFitText()

const skipLayers = computed(() => (customHeroPhoto.value ? ['15:94'] : []))
</script>

<template>
  <section :ref="el" class="band hero" :class="{ 'is-in': shown }">
    <BandArt :layers="LAYERS" :skip="skipLayers" :shown="shown" />

    <!-- Custom Hero Photo (Gambar 1: foto setelah buka undangan) -->
    <div
      v-if="customHeroPhoto"
      class="hero__photo-wrapper"
      :class="{ 'is-in': shown }"
    >
      <img
        class="hero__photo"
        :src="customHeroPhoto"
        alt="Foto Mempelai"
        loading="eager"
        decoding="async"
      />
    </div>

    <!--
      z-index on each of these is the node's own GLOBAL Figma child order, not a flat
      "above the art" value. The design stacks two of its light plates (31:321 z191,
      31:322 z192) and both edge botanicals (z266/267) OVER the eyebrow and hashtag,
      and only the couple name (z285) sits above everything. A shared z would lift the
      eyebrow out from under the wash it is authored to sit beneath.
    -->
    <p class="hero__eyebrow">The Wedding Of</p>
    <h1 :ref="fitCouple" class="hero__couple">{{ coupleNickname }}</h1>
    <p v-if="hashtag" class="hero__hashtag">{{ hashtag }}</p>
  </section>
</template>

<style scoped>
/*
 * The band's height is the distance to the NEXT band's top, not the extent of its own
 * children — the florals at the bottom run on past 1108 into the countdown, which is
 * what the design does.
 */
.hero {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * Custom Hero Photo: masked to the exact frame shape via 15-91.webp
 * Sitting at z-index: 55 (between 15:91 backing plate and 15:95 frame overlay).
 */
.hero__photo-wrapper {
  position: absolute;
  z-index: 55;
  top: calc(409 * var(--px));
  left: calc(80 * var(--px));
  width: calc(437 * var(--px));
  height: calc(688 * var(--px));
  overflow: hidden;
  -webkit-clip-path: polygon(24% 1%, 76% 1%, 98.8% 15%, 98.8% 82.5%, 97% 85%, 90% 88.5%, 81% 91.5%, 67% 93.8%, 58.5% 96%, 50% 98.8%, 41.5% 96%, 33% 93.8%, 19% 91.5%, 10% 88.5%, 3% 85%, 1.2% 82.5%, 1.2% 15%);
  clip-path: polygon(24% 1%, 76% 1%, 98.8% 15%, 98.8% 82.5%, 97% 85%, 90% 88.5%, 81% 91.5%, 67% 93.8%, 58.5% 96%, 50% 98.8%, 41.5% 96%, 33% 93.8%, 19% 91.5%, 10% 88.5%, 3% 85%, 1.2% 82.5%, 1.2% 15%);
  visibility: hidden;
  will-change: transform, opacity;
  pointer-events: none;
}

.hero__photo-wrapper.is-in {
  visibility: visible;
  animation: hero-photo-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 440ms;
}

.hero__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
  -webkit-clip-path: polygon(24% 1%, 76% 1%, 98.8% 15%, 98.8% 82.5%, 97% 85%, 90% 88.5%, 81% 91.5%, 67% 93.8%, 58.5% 96%, 50% 98.8%, 41.5% 96%, 33% 93.8%, 19% 91.5%, 10% 88.5%, 3% 85%, 1.2% 82.5%, 1.2% 15%);
  clip-path: polygon(24% 1%, 76% 1%, 98.8% 15%, 98.8% 82.5%, 97% 85%, 90% 88.5%, 81% 91.5%, 67% 93.8%, 58.5% 96%, 50% 98.8%, 41.5% 96%, 33% 93.8%, 19% 91.5%, 10% 88.5%, 3% 85%, 1.2% 82.5%, 1.2% 15%);
}

@keyframes hero-photo-in {
  from {
    opacity: 0;
    transform: translate3d(0, calc(44 * var(--px)), 0) scale(0.86);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

/*
 * The three `top` values below are each Figma's box y PLUS 1. Measured, not nudged: the
 * glyph ink of all three nodes, exported from Figma and template-matched into both the
 * frame render and the live shot, lands dx 0 / dy -1 in the browser. That is the CSS
 * line box centring the glyphs one pixel higher inside the same line-height than Figma
 * does, so the difference is paid back through `top` and the design's own font-size and
 * line-height are left alone. Re-measure if either face is ever swapped.
 */

/*
 * 13:3 — Lancelot 18/27, #3d78a2, centred. Placed in its parent frame's box (13:2
 * "Paragraph", x 97, w 417.25) rather than the tight text box, so a longer live string
 * still centres on the same axis instead of overflowing a 112px box.
 */
.hero__eyebrow {
  --delay: 300ms;
  z-index: 60;
  top: calc(150 * var(--px)); /* 13:3 box y 149 + 1 */
  left: calc(97 * var(--px));
  width: calc(417.25 * var(--px));
  font-family: var(--font-lancelot);
  font-weight: 400;
  font-size: calc(18 * var(--px));
  line-height: calc(27 * var(--px));
  color: var(--ink-deep-blue);
}

/*
 * 61:626 — Roben Elegante 40/74, #65839d, in a 392 box at x 107.05. The design's own
 * face, self-hosted, so every number here is Figma's with no substitute compensation.
 *
 * NO text-transform: this face draws its capitals as a swashed set, so uppercasing
 * swaps the name onto glyphs the render never uses.
 *
 * `height` exists only as the constraint useFitText measures against — nothing is
 * clipped. One line always fits; a nickname long enough to wrap measures two lines and
 * shrinks instead of running past the frame. line-height scales with --fit too, or
 * shrinking the glyphs would never shorten the block and the fit would never converge.
 */
.hero__couple {
  --delay: 450ms;
  z-index: 285;
  top: calc(182 * var(--px)); /* 61:626 box y 181 + 1 */
  left: calc(107.05 * var(--px));
  width: calc(392 * var(--px));
  height: calc(92 * var(--px) * var(--fit, 1));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(40 * var(--px) * var(--fit, 1));
  line-height: calc(74 * var(--px) * var(--fit, 1));
  color: var(--ink-blue);
}

/*
 * 13:5 — Lancelot 18/27, #3d78a2. Its Figma box is x 238 w 132, centred on 304; the
 * eyebrow above it centres on 305.63 and the name on 303.05. The three are NOT
 * concentric, which is the design rather than a rounding slip — so this box is widened
 * for live copy about the design's own 304, not snapped to a shared axis.
 */
.hero__hashtag {
  --delay: 600ms;
  z-index: 61;
  top: calc(260 * var(--px)); /* 13:5 box y 259 + 1 */
  left: calc(95.37 * var(--px));
  width: calc(417.25 * var(--px));
  font-family: var(--font-lancelot);
  font-weight: 400;
  font-size: calc(18 * var(--px));
  line-height: calc(27 * var(--px));
  color: var(--ink-deep-blue);
}
</style>
