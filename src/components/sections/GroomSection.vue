<script setup lang="ts">
/*
 * Frame 1 (1:3) band "groom": y 3163..4021 of the body frame. The mirror of the bride
 * band — same scene, flipped, with the couple's other half in it. Art comes from
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

const { el, shown } = useReveal(0.15)
const { bride, groom, isGroomFirst } = useWedding()

const person = computed(() => (isGroomFirst.value ? bride.value : groom.value))

const callName = computed(() => {
  if (person.value?.nickname?.trim()) return person.value.nickname.trim()
  if (person.value?.name?.trim()) return person.value.name.trim().split(' ')[0]
  return isGroomFirst.value ? 'Syifa' : 'El Rumi'
})

const fullName = computed(() => {
  if (person.value?.name?.trim()) return person.value.name.trim()
  return isGroomFirst.value ? 'Syifa Hadju' : 'Ahmad Jalaluddin Rumi'
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
    ? 'Putri pertama dari \n Bapak Hari Solehaiman \n dan Ibu Kasih Muhartono Septiana'
    : 'Putra pertama dari \n Bapak Solehaiman \n dan Ibu Kasih',
)

const parents = computed(() => parentLine(person.value) || fallbackParents.value)
</script>

<template>
  <section :ref="el" class="band groom" :class="{ 'is-in': shown }" aria-labelledby="person-2-name">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 20:622 — the call name, set beside the portrait. -->
    <p class="groom__call">{{ callName }}</p>

    <!-- 20:614 — the full name, the band's heading. -->
    <h2 id="person-2-name" class="groom__full" :style="fullNameStyle">
      <span v-for="line in fullNameLines" :key="line">{{ line }}</span>
    </h2>

    <!-- 20:616 — three authored lines; the box keeps white-space: pre-wrap. -->
    <p class="groom__parents" :style="{ top: `calc(${559 + detailsOffset} * var(--px))` }">{{ parents }}</p>

  </section>
</template>

<style scoped>
.groom {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * 20:622 — Cavilenny 36, #aa7a3a, centred in a 311 box at x -34. The bride's face and,
 * now that it is the design's own file, the bride's size too.
 *
 * That pairing is new. The substitute could not share a size with her: a width match is
 * per WORD, not per face, and Cormorant set "Syifa" 8.8% narrow against Cavilenny but
 * "El Rumi" only 4.2%, so the two nodes carried 39.2 and 37.5 for the same authored 36.
 * A real face has no such split — same file, same 36, both words land.
 */
.groom__call {
  --delay: 80ms;
  z-index: 103;
  top: calc(275 * var(--px)); /* 20:622 box y 3438, band-local 275 */
  left: calc(-34 * var(--px));
  width: calc(311 * var(--px));
  font-family: var(--font-call);
  font-weight: 400;
  font-size: calc(36 * var(--px));
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
}

.groom__full span {
  display: block;
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
