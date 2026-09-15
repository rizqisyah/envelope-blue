<script setup lang="ts">
/*
 * Frame 1 (1:3) band "bride": y 2161..3163 of the body frame. The bride's portrait
 * scene at the top, her name and parents under it, and the "And" that hands over to
 * the groom. Art comes from src/lib/bands/bride.ts (GENERATED, scripts/gen_band.py).
 *
 * The band is the mirror of "groom" at +1002px: 20:605↔20:608, 20:594↔20:610,
 * 19:574↔20:607, 20:592↔20:632, 19:572↔20:609 all pair up exactly. That mirror is the
 * corroboration for every hard placement here, and it is how the groom band should be
 * checked when it is cut.
 */
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/bride'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parentLine } from '../../lib/format'

const { el, shown } = useReveal(0.15)
const { bride, groom, isGroomFirst, groomTransform } = useWedding()

const person = computed(() => (isGroomFirst.value ? groom.value : bride.value))

const groomPhotoStyle = computed(() => ({
  objectPosition: `${groomTransform.value.x}% ${groomTransform.value.y}%`,
  transformOrigin: `${groomTransform.value.x}% ${groomTransform.value.y}%`,
  transform: `scale(${groomTransform.value.scale})`,
}))

const callName = computed(() => {
  if (person.value?.nickname?.trim()) return person.value.nickname.trim()
  if (person.value?.name?.trim()) return person.value.name.trim().split(' ')[0]
  return isGroomFirst.value ? 'El Rumi' : 'Syifa'
})

const fullName = computed(() => {
  if (person.value?.name?.trim()) return person.value.name.trim()
  return isGroomFirst.value ? 'Ahmad Jalaluddin Rumi' : 'Syifa Hadju'
})

const fullNameLines = computed(() => {
  const words = fullName.value.split(/\s+/)
  if (words.length < 3 || fullName.value.length <= 20) return [fullName.value]
  let best = 1
  let distance = Infinity
  for (let i = 1; i < words.length; i++) {
    const next = Math.abs(words.slice(0, i).join(' ').length - words.slice(i).join(' ').length)
    if (next < distance) {
      distance = next
      best = i
    }
  }
  return [words.slice(0, best).join(' '), words.slice(best).join(' ')]
})

const fullNameStyle = computed(() => {
  const scale = fullNameLines.value.length > 1 ? 0.82 : 1
  return {
    fontSize: `calc(${Math.round(32 * scale)} * var(--px))`,
    lineHeight: `calc(${Math.round(57 * scale)} * var(--px))`,
  }
})

const detailsOffset = computed(() =>
  fullNameLines.value.length > 1 ? Math.round(57 * 0.82 * 2 - 57) : 0,
)

const fallbackParents = computed(() =>
  isGroomFirst.value
    ? 'Putra pertama dari \n Bapak Solehaiman \n dan Ibu Kasih'
    : 'Putri pertama dari \n Bapak Hari Solehaiman \n dan Ibu Kasih Muhartono Septiana',
)

const parents = computed(() => parentLine(person.value) || fallbackParents.value)

// Layer 20:623 is the groom portrait (x: 244, y: 881, w: 352, h: 503).
const hasGroomPhoto = computed(() => Boolean(groom.value?.photo_url))
</script>

<template>
  <section :ref="el" class="band bride" :class="{ 'is-in': shown }" aria-labelledby="person-1-name">
    <BandArt :layers="LAYERS" :skip="hasGroomPhoto ? ['20:623'] : []" :shown="shown" />

    <div
      v-if="hasGroomPhoto"
      class="band-art band__portrait"
      :class="{ 'is-in': shown }"
      :style="{
        zIndex: String(108),
        left: 'calc(244 * var(--px))',
        top: 'calc(881 * var(--px))',
        width: 'calc(352 * var(--px))',
        height: 'calc(503 * var(--px))',
      }"
    >
      <img :src="groom.photo_url" alt="" :style="groomPhotoStyle" />
    </div>

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 20:596 — the call name, set beside the portrait rather than under it. -->
    <p class="bride__call">{{ callName }}</p>

    <!-- 20:641 — the full name, the band's heading. -->
    <h2 id="person-1-name" class="bride__full" :style="fullNameStyle">
      <span v-for="line in fullNameLines" :key="line">{{ line }}</span>
    </h2>

    <!-- 19:546 — three authored lines; the box keeps white-space: pre-wrap. -->
    <p class="bride__parents" :style="{ top: `calc(${554 + detailsOffset} * var(--px))` }">{{ parents }}</p>

    <!-- 19:543 — the hand-off to the next band. Always present at bottom of Slot 1. -->
    <p class="bride__and" aria-hidden="true">And</p>
  </section>
</template>

<style scoped>
.bride {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * 20:596 — Cavilenny 36, #aa7a3a, centred in a 311 box at x 311. The design's own face,
 * now self-hosted, so this is Figma's box and Figma's size with nothing fitted on top.
 * Figma declares no line-height, so the box's own 45 stands in for it.
 *
 * It replaces a Cormorant Infant width-match at 39.2 with a 1px nudge each way in `top`
 * and `left` — both of them properties of that substitute's line box and side bearings,
 * not of this node, which is why they go with it. Cavilenny's own metrics put the ink
 * where Figma's coordinates say.
 */
.bride__call {
  --delay: 80ms;
  z-index: 102;
  top: calc(275 * var(--px)); /* 20:596 box y 2436, band-local 275 */
  left: calc(311 * var(--px));
  width: calc(311 * var(--px));
  font-family: var(--font-call);
  font-weight: 400;
  font-size: calc(36 * var(--px));
  line-height: calc(45 * var(--px));
  color: #aa7a3a;
}

/* 20:641 — Roben Elegante Script 32, #aa7a3a, centred. The design's own face. */
.bride__full {
  --delay: 200ms;
  z-index: 93;
  top: calc(497 * var(--px)); /* 20:641 box y 2658, band-local 497 */
  left: calc(71.5 * var(--px));
  width: calc(452 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
}

.bride__full span {
  display: block;
}

/*
 * 19:546 — Cormorant Infant 20/28.4, #8a643c, centred. The design's own face, so every
 * number here is Figma's.
 *
 * `pre-wrap`, not `pre-line`: the Figma string carries a LEADING space on both
 * continuation lines, and the longest of the three is one of them. A centred line is
 * centred including that space, which puts the render's ink 2px right of the box's own
 * centre — `pre-line` strips it and the block lands 2px left of the render. Trailing
 * spaces hang and change nothing, in Figma and in CSS alike.
 */
.bride__parents {
  --delay: 320ms;
  z-index: 94;
  top: calc(554 * var(--px)); /* 19:546 box y 2715, band-local 554 */
  left: calc(155 * var(--px));
  width: calc(286 * var(--px));
  font-family: var(--font-body);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(28.4 * var(--px));
  white-space: pre-wrap;
  color: #8a643c;
}

/*
 * 19:549 — the pill: 151 x 46 at x 222.5, radius 999, #aa7a3a, 8/12 padding. Its two
 * children are 19:551 (the Brands glyph, exported) and 19:553 (Cormorant Infant 20/30,
 * #f7f6f1). Laid out rather than positioned absolutely, so a longer handle grows the
 * plate the way the design's auto-layout does.
 */
.bride__handle {
  --delay: 440ms;
  z-index: 95;
  display: inline-flex;
  align-items: center;
  gap: calc(8 * var(--px));
  top: calc(654 * var(--px)); /* 19:549 box y 2815, band-local 654 */
  left: 50%;
  translate: -50% 0;
  padding: calc(8 * var(--px)) calc(12 * var(--px));
  border-radius: 999px;
  background: #aa7a3a;
  font-family: var(--font-body);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #f7f6f1;
  text-decoration: none;
  transition: background 240ms ease, scale 240ms ease;
}

.bride__handle img {
  width: calc(18 * var(--px));
  height: calc(18 * var(--px));
}

.bride__handle:hover,
.bride__handle:focus-visible {
  background: #8a643c;
  /* `scale`, not a transform: the band's reveal owns `transform` and would win. */
  scale: 1.04;
}

/* 19:543 — Roben Elegante Script 40, #aa7a3a. Its box centres on 293, not the 297.5 of
 * the name above it; that is the design, so it is reproduced rather than snapped. */
.bride__and {
  --delay: 560ms;
  z-index: 133;
  top: calc(770 * var(--px)); /* 19:543 box y 2931, band-local 770 */
  left: calc(67 * var(--px));
  width: calc(452 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(40 * var(--px));
  line-height: calc(71 * var(--px));
  color: #aa7a3a;
}

.band__portrait {
  position: absolute;
  overflow: hidden;
  visibility: hidden;
}

.band__portrait img {
  width: 100%;
  height: 100%;
  max-width: none;
  object-fit: cover;
}

.band__portrait.is-in {
  visibility: visible;
}
</style>
