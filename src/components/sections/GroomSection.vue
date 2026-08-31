<script setup lang="ts">
/*
 * Frame 1 (1:3) band "groom": y 3163..4021 of the body frame. The mirror of the bride
 * band — same scene, flipped, with the couple's other half in it. Art comes from
 * src/lib/bands/groom.ts (GENERATED, scripts/gen_band.py).
 *
 * The mirror is exact and it is a real mirror, not a copy: every paired export is the
 * horizontal flip of its twin (measured — `same` err 17..61 against `mirrored` err
 * 3..9 for all eight same-size pairs), the y offset is +1002, and correlating the two
 * scenes puts the axis at x 294. Use that when a placement here is in doubt.
 */
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/groom'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parentLine } from '../../lib/format'
import instagramGlyph from '../../assets/bride/instagram.webp'

const { el, shown } = useReveal(0.15)
const { groom } = useWedding()

// The design prints "El Rumi / Ahmad Jalaluddin Rumi".
const callName = computed(() => groom.value?.nickname?.trim() || 'El Rumi')
const fullName = computed(() => groom.value?.name?.trim() || 'Ahmad Jalaluddin Rumi')

/*
 * 20:616 — the design duplicates the BRIDE's parents line here verbatim, "Putri" and
 * all, rather than writing the groom's. The render is the specification, so the fallback
 * reproduces it; live data replaces it with the groom's own through parentLine().
 * Same leading-space-per-continuation-line shape as 19:546 — see the `pre-wrap` note.
 */
const PARENTS =
  'Putri pertama dari \n Bapak Hari Solehaiman \n dan Ibu Kasih Muhartono Septiana'
const parents = computed(() => parentLine(groom.value) || PARENTS)

// `instagram` is a GUESS at the field name — see the same note in BrideSection.
const handle = computed(() => (groom.value?.instagram || '@elrumiii').trim())
const handleUrl = computed(() => `https://instagram.com/${handle.value.replace(/^@/, '')}`)
</script>

<template>
  <section :ref="el" class="band groom" :class="{ 'is-in': shown }" aria-labelledby="groom-name">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 20:622 — the call name, set beside the portrait. -->
    <p class="groom__call">{{ callName }}</p>

    <!-- 20:614 — the full name, the band's heading. -->
    <h2 id="groom-name" class="groom__full">{{ fullName }}</h2>

    <!-- 20:616 — three authored lines; the box keeps white-space: pre-wrap. -->
    <p class="groom__parents">{{ parents }}</p>

    <!-- 20:618 — the pill, redrawn as a real link. Same treatment as the bride's. -->
    <a class="groom__handle" :href="handleUrl" target="_blank" rel="noopener noreferrer">
      <img :src="instagramGlyph" alt="" width="18" height="18" />
      <span>{{ handle }}</span>
    </a>
  </section>
</template>

<style scoped>
.groom {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * 20:622 — Cavilenny 36, #aa7a3a, centred in a 311 box at x -34. Cavilenny is not on
 * fontsource, so this is the bride's stand-in, Cormorant Infant — but NOT her size. The
 * width match is per WORD, not per face: Cormorant sets "Syifa" 8.8% narrow against
 * Cavilenny and "El Rumi" only 4.2% narrow, because the two faces' per-glyph widths
 * differ unevenly. Measured here: at the bride's 39.2 this word renders 118 against the
 * render's 113, and at 37.5 it lands 114 with its left edge and baseline exactly on the
 * render's. No `top`/`left` correction is needed at this size, unlike hers.
 *
 * Its ink is 27 tall against the render's 29 — the usual width-first trade, and the floor
 * for the node until Cavilenny is licensed.
 */
.groom__call {
  --delay: 80ms;
  z-index: 103;
  top: calc(275 * var(--px)); /* 20:622 box y 3438, band-local 275 */
  left: calc(-34 * var(--px));
  width: calc(311 * var(--px));
  font-family: var(--font-caps);
  font-weight: 400;
  font-size: calc(37.5 * var(--px)); /* 36 x 1.042 — measured on THIS word, see above */
  line-height: calc(45 * var(--px));
  color: #aa7a3a;
}

/*
 * 20:614 — Roben Elegante Script 32, #aa7a3a, centred. The design's own face.
 * Its box is 540 wide at x 19.5 and centres on 289.5; the bride's is 452 at 71.5 and
 * centres on 297.5. The two name blocks are NOT on a shared axis — reproduce, don't snap.
 */
.groom__full {
  --delay: 200ms;
  z-index: 98;
  top: calc(502 * var(--px)); /* 20:614 box y 3665, band-local 502 */
  left: calc(19.5 * var(--px));
  width: calc(540 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
  color: #aa7a3a;
}

/* 20:616 — Cormorant Infant 20/28.4, #8a643c. `pre-wrap` for the leading spaces. */
.groom__parents {
  --delay: 320ms;
  z-index: 99;
  top: calc(559 * var(--px)); /* 20:616 box y 3722, band-local 559 */
  left: calc(147 * var(--px));
  width: calc(286 * var(--px));
  font-family: var(--font-body);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(28.4 * var(--px));
  white-space: pre-wrap;
  color: #8a643c;
}

/*
 * 20:618 — 127 x 46 at x 226.5, so it centres on 290, NOT on the frame's 298 the way the
 * bride's does: its parent container sits 8px left of hers. Centred explicitly rather
 * than with `left: 50%` for that reason.
 */
.groom__handle {
  --delay: 440ms;
  z-index: 100;
  display: inline-flex;
  align-items: center;
  gap: calc(8 * var(--px));
  top: calc(659 * var(--px)); /* 20:618 box y 3822, band-local 659 */
  left: calc(290 * var(--px));
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

.groom__handle img {
  width: calc(18 * var(--px));
  height: calc(18 * var(--px));
}

.groom__handle:hover,
.groom__handle:focus-visible {
  background: #8a643c;
  /* `scale`, not a transform: the band's reveal owns `transform` and would win. */
  scale: 1.04;
}
</style>
