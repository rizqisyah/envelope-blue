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
import instagramGlyph from '../../assets/bride/instagram.webp'

const props = withDefaults(defineProps<{ showAnd?: boolean }>(), {
  showAnd: true,
})

const { el, shown } = useReveal(0.15)
const { bride } = useWedding()

const bandHeight = computed(() => (props.showAnd ? BAND_HEIGHT : 858))

/*
 * The design prints "Syifa / Syifa Hadju", so an unconfigured render matches the frame.
 */
const callName = computed(() => bride.value?.nickname?.trim() || 'Syifa')
const fullName = computed(() => bride.value?.name?.trim() || 'Syifa Hadju')

/*
 * 19:546 — the design authors two breaks in this line, and they have to live in a
 * script constant: written inline in the template Vue folds the source newlines to
 * spaces and `white-space: pre-line` has nothing left to preserve. Live data arrives
 * as one sentence from parentLine() and wraps inside the box instead.
 */
const PARENTS =
  'Putri pertama dari \n Bapak Hari Solehaiman \n dan Ibu Kasih Muhartono Septiana'
const parents = computed(() => parentLine(bride.value) || PARENTS)

// `instagram` is a GUESS at the field name -- getHome's pengantin rows are undocumented
// here and nothing in this repo reads one. The design fallback keeps the band correct
// either way; check this first if a live handle does not appear.
const handle = computed(() => (bride.value?.instagram || '@Syifahadju').trim())
const handleUrl = computed(
  () => `https://instagram.com/${handle.value.replace(/^@/, '')}`,
)
</script>

<template>
  <section :ref="el" class="band bride" :class="{ 'is-in': shown }" aria-labelledby="bride-name">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 20:596 — the call name, set beside the portrait rather than under it. -->
    <p class="bride__call">{{ callName }}</p>

    <!-- 20:641 — the full name, the band's heading. -->
    <h2 id="bride-name" class="bride__full">{{ fullName }}</h2>

    <!-- 19:546 — three authored lines; the box keeps white-space: pre-line. -->
    <p class="bride__parents">{{ parents }}</p>

    <!--
      19:549 — a rounded gold plate with a Font Awesome Brands glyph and the handle.
      Redrawn as a real link: the design's plate is chrome that has to work, and the
      glyph is Figma's own export rather than a guess at the Instagram mark.
    -->
    <a class="bride__handle" :href="handleUrl" target="_blank" rel="noopener noreferrer">
      <img :src="instagramGlyph" alt="" width="18" height="18" />
      <span>{{ handle }}</span>
    </a>

    <!-- 19:543 — the hand-off to the next band. -->
    <p v-if="props.showAnd" class="bride__and" aria-hidden="true">And</p>
  </section>
</template>

<style scoped>
.bride {
  height: calc(v-bind(bandHeight) * var(--px));
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
  color: #aa7a3a;
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
</style>
