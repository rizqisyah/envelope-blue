<script setup lang="ts">
import { COVER_LAYERS } from '../../lib/coverLayers'
import { useFitText } from '../../composables/useFitText'

// `ready` gates the reveal on the layers being decoded — see App.vue.
defineProps<{ guestName: string; guestGroup?: string; coupleName: string; ready: boolean }>()
defineEmits<{ open: [] }>()

/*
 * The water settles first and the envelope rises out of it, so the scene assembles the
 * way it was stacked rather than all at once.
 */
const delayFor = (z: number) => Math.min(z * 260, 1080)

// The couple name is the one box whose content is live and can run long — see its rule.
const fitCouple = useFitText()
</script>

<template>
  <!-- Figma Frame 2 (27:9), 596 x 1183. Coords below are frame-local design px. -->
  <section class="cover">
    <div class="cover__frame" :class="{ 'cover__frame--ready': ready }">
      <img
        v-for="layer in COVER_LAYERS"
        :key="layer.id"
        class="cover__layer"
        :class="{ 'cover__layer--envelope': layer.id === '27:216' }"
        :src="layer.src"
        alt=""
        :width="layer.w"
        :height="layer.h"
        :style="{
          zIndex: layer.z,
          left: `calc(${layer.x} * var(--px))`,
          top: `calc(${layer.y} * var(--px))`,
          width: `calc(${layer.w} * var(--px))`,
          height: `calc(${layer.h} * var(--px))`,
          animationDelay: `${delayFor(layer.z)}ms`,
        }"
      />

      <!-- 32:462 / 28:222 — z 3 and 4 in Figma child order. -->
      <p class="cover__eyebrow">The Wedding Of</p>
      <h1 :ref="fitCouple" class="cover__couple">{{ coupleName }}</h1>

      <!-- 28:223 / 32:460 — the lines of Frame 7, placed directly. -->
      <p class="cover__dear">kepada Yth.</p>
      <p class="cover__guest">{{ guestName }}</p>
      <p v-if="guestGroup" class="cover__group">{{ guestGroup }}</p>

      <!--
        The design prints no "click to open" label at all, so the whole card is the hit
        area and the envelope carries the affordance: it breathes, and it lifts on hover
        and focus. The button keeps a screen-reader label of its own since there is no
        visible text to point at.
      -->
      <button type="button" class="cover__hit" @click="$emit('open')">
        <span class="sr-only">Buka undangan</span>
      </button>
    </div>
  </section>
</template>

<style scoped>
.cover {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 100dvh;
  overflow: hidden;
  background: var(--water);
}

/*
 * One design pixel = 1cqw / 596, so the whole composition scales as a unit instead of
 * reflowing. Width is driven by the viewport height so the card fills the screen; on
 * screens too narrow for that width, `.cover`'s `overflow: hidden` crops the sides
 * evenly. `max()`, not the bare height-derived width: Safari's dvh excludes the
 * toolbars, so the derived width lands short of the screen and leaves a gutter down
 * both sides. Filling the width and letting `.cover` crop the extra height keeps the
 * scene full-bleed.
 *
 * The desktop column (430px, App.vue) gets the SAME rule, not a `min()` clamp against
 * the column width. This frame is 596 x 1183 — narrower per unit of height than the
 * column — so clamping left it ~47px short of the viewport and the water plate stopped
 * partway down the screen. Filling the height and cropping ~11px off each side instead
 * costs nothing: the composition is centred and its edges are open water.
 */
.cover__frame {
  container-type: inline-size;
  position: relative;
  overflow: hidden;
  /* flex-shrink: 0 — otherwise the 430px column squashes the width-driven frame back down */
  flex: 0 0 auto;
  width: max(100%, calc(100dvh * 596 / 1183));
  aspect-ratio: 596 / 1183;
  background: var(--water);
}

.cover__frame > * {
  --px: 0.167785cqw; /* 100cqw / 596 */
  position: absolute;
  margin: 0;
  text-align: center;
  /*
   * Held until the layers are decoded. `animation-play-state` rather than `display`
   * so the images are still in the document and actually fetching while hidden.
   */
  visibility: hidden;
  animation-play-state: paused;
}

.cover__frame--ready > * {
  visibility: visible;
  animation-play-state: running;
}

.cover__layer {
  max-width: none;
  /* The envelope covers the middle of the card; without this it swallows every tap
     meant for the hit plate underneath it. */
  pointer-events: none;
  animation: rise 2200ms cubic-bezier(0.16, 1, 0.3, 1) backwards;
}

/*
 * `backwards`, not `forwards`: the end state is the element's normal state, so once
 * the animation finishes it stops applying and the hover transition gets its transform.
 */
@keyframes rise {
  from {
    opacity: 0;
    transform: translateY(calc(18 * var(--px)));
  }
}

.cover__eyebrow,
.cover__couple,
.cover__dear,
.cover__guest,
.cover__group {
  animation: rise 2400ms cubic-bezier(0.16, 1, 0.3, 1) var(--delay, 0ms) backwards;
}

/* 32:462 — Roben Elegante 24/74, #65839d, centred in a 392 box. Its box sits 10px
   right of the couple's, which is where the render has it — not a rounding slip. */
.cover__eyebrow {
  --delay: 900ms;
  z-index: 3;
  top: calc(154 * var(--px));
  left: calc(112 * var(--px));
  width: calc(392 * var(--px));
  font-family: var(--font-script);
  font-weight: 400;
  font-size: calc(24 * var(--px));
  line-height: calc(74 * var(--px));
  color: var(--ink-blue);
}

/*
 * 28:222 — Roben Elegante 40/74, #65839d. The design's own face, self-hosted, so every
 * number here is Figma's and there is no substitute compensation to carry.
 *
 * NO text-transform: the Figma string is title case and this face draws its capitals as
 * a swashed set, so uppercasing swaps the whole name onto glyphs the render never uses.
 *
 * `height` exists only as the constraint useFitText measures against — nothing is
 * clipped, `overflow` stays visible. One line always fits; a nickname long enough to
 * wrap measures two lines and shrinks instead of running past the card. line-height
 * scales with --fit too, or shrinking the glyphs would never shorten the block and the
 * fit would never converge.
 */
.cover__couple {
  --delay: 1150ms;
  z-index: 4;
  top: calc(206 * var(--px));
  left: calc(102 * var(--px));
  width: calc(392 * var(--px));
  height: calc(74 * var(--px) * var(--fit, 1));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(40 * var(--px) * var(--fit, 1));
  line-height: calc(74 * var(--px) * var(--fit, 1));
  color: var(--ink-blue);
}

/* 28:223 — Cormorant Infant 28/62, #65839d. */
.cover__dear {
  --delay: 1450ms;
  z-index: 5;
  top: calc(842 * var(--px));
  left: calc(112 * var(--px));
  width: calc(373 * var(--px));
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: calc(28 * var(--px));
  line-height: calc(62 * var(--px));
  color: var(--ink-blue);
}

/* 32:460 — the same face and size, 42px below its sibling inside Frame 7. */
.cover__guest {
  --delay: 1600ms;
  z-index: 6;
  top: calc(884 * var(--px));
  left: calc(112 * var(--px));
  width: calc(373 * var(--px));
  font-family: var(--font-serif);
  font-weight: 400;
  font-size: calc(28 * var(--px));
  line-height: calc(62 * var(--px));
  color: var(--ink-blue);
}

.cover__group {
  --delay: 1750ms;
  z-index: 7;
  top: calc(940 * var(--px));
  left: calc(112 * var(--px));
  width: calc(373 * var(--px));
  font-family: var(--font-body);
  font-weight: 500;
  font-size: calc(16 * var(--px));
  letter-spacing: calc(1.5 * var(--px));
  text-transform: uppercase;
  line-height: calc(24 * var(--px));
  color: var(--ink-blue);
  opacity: 0.85;
}

/*
 * The whole card opens the invitation, because the design gives no button to point at.
 * The plate is invisible, so its own hover state would be too — the envelope carries it.
 */
.cover__hit {
  z-index: 20;
  inset: 0;
  width: 100%;
  height: 100%;
  border: 0;
  background: none;
  cursor: pointer;
  /* No entrance of its own — it is invisible, and animating it would gate the tap. */
  animation: none;
}

.cover__layer--envelope {
  transition: transform 320ms cubic-bezier(0.16, 1, 0.3, 1);
}

.cover__frame--ready .cover__layer--envelope {
  animation:
    rise 2200ms cubic-bezier(0.16, 1, 0.3, 1) backwards,
    breathe 5200ms ease-in-out 2600ms infinite;
}

.cover__frame:has(.cover__hit:hover) .cover__layer--envelope,
.cover__frame:has(.cover__hit:focus-visible) .cover__layer--envelope {
  transform: translateY(calc(-6 * var(--px)));
}

@keyframes breathe {
  50% {
    transform: translateY(calc(-5 * var(--px)));
  }
}

.cover__hit:focus-visible {
  outline: calc(1.5 * var(--px)) solid var(--ink-blue);
  outline-offset: calc(-6 * var(--px));
}

@media (prefers-reduced-motion: reduce) {
  .cover__frame > * {
    animation: none;
  }

  .cover__frame--ready .cover__layer--envelope {
    animation: none;
  }
}
</style>
