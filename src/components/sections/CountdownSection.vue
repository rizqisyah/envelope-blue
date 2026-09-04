<script setup lang="ts">
/*
 * Frame 1 (1:3) band "countdown": y 1108..1802 of the body frame. The ornate frame and
 * the floral edges — art from src/lib/bands/countdown.ts (GENERATED, scripts/gen_band.py)
 * — sit on the toile wallpaper that runs up from the hero.
 *
 * The four "0" placeholders in the design are live here. Figma baked zeroes, but the
 * band is a countdown to the akad: the first acara with a parseable date wins, and
 * without one the counter sits at 0/0/0/0 — which is exactly what the render shows.
 */
import { computed, onUnmounted, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { parseEventStart, remainingUntil } from '../../lib/format'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/countdown'

const { el, shown } = useReveal(0.15)
const { acara, wedding } = useWedding()

const now = ref(Date.now())
const timer = window.setInterval(() => (now.value = Date.now()), 1000)
onUnmounted(() => window.clearInterval(timer))

const target = computed(() => {
  if (wedding.value?.countdown_date) {
    const raw = wedding.value.countdown_date
    const at = raw instanceof Date ? raw : new Date(String(raw).trim().replace(' ', 'T'))
    if (!Number.isNaN(at.getTime())) return at
  }
  for (const a of acara.value as any[]) {
    const at = parseEventStart(a?.event_date, a?.event_time)
    if (at) return at
  }
  return null
})

const left = computed(() => remainingUntil(target.value, now.value))

// 16:498 — the design folds the line break itself; the box keeps `white-space: pre-line`.
const TITLE = 'Save \nThe Date'
</script>

<template>
  <section :ref="el" class="band countdown" :class="{ 'is-in': shown }" aria-labelledby="save-the-date">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->
    <h2 id="save-the-date" class="countdown__title">{{ TITLE }}</h2>

    <!-- 16:454/16:461/16:468/16:475 — Ibarra Real Nova 48 Italic, #623c2a. -->
    <p class="countdown__n countdown__n--days">{{ left.days }}</p>
    <p class="countdown__n countdown__n--hours">{{ left.hours }}</p>
    <p class="countdown__n countdown__n--minutes">{{ left.minutes }}</p>
    <p class="countdown__n countdown__n--seconds">{{ left.seconds }}</p>

    <!-- 16:457/16:464/16:471/16:478 — Ibarra Real Nova 20, #623c2a. -->
    <p class="countdown__l countdown__l--days">Days</p>
    <p class="countdown__l countdown__l--hours">Hours</p>
    <p class="countdown__l countdown__l--minutes">Minutes</p>
    <p class="countdown__l countdown__l--seconds">Seconds</p>
  </section>
</template>

<style scoped>
.countdown {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * `top`s are Figma's box y (band-local) EXACTLY — no offset.
 *
 * The hero pays its text back +1px, and that number was copied here; measuring showed it
 * over-corrects. The line-box offset is PER FACE, not per project: the hero's Lancelot and
 * Roben Elegante sit 1px high in the browser, Pinyon Script and Ibarra Real Nova do not.
 * All six of this band's nodes, measured by locating their Figma glyph ink in both the
 * frame render and the live shot, came back dx 0 / dy +1 against the +1 tops — i.e. the
 * raw Figma y is right. Re-measure per face; never carry another band's compensation.
 */

/* 16:498 — Pinyon Script 32/38, #700f06, centred in a 199 box at x 202. */
.countdown__title {
  --delay: 60ms;
  z-index: 62;
  top: calc(214 * var(--px)); /* 16:498 box y */
  left: calc(202 * var(--px));
  width: calc(199 * var(--px));
  font-family: var(--font-script-date);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(38 * var(--px));
  white-space: pre-line;
  color: #700f06;
}

/*
 * The figures. A live two-digit value overflows the 29-wide box symmetrically
 * (centred, nothing clipped); the seconds tick every second, so tabular-nums keeps the
 * column from shuffling.
 */
.countdown__n {
  --delay: 200ms;
  width: calc(29 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-style: italic;
  font-size: calc(48 * var(--px));
  line-height: calc(60 * var(--px));
  color: #623c2a;
  font-variant-numeric: tabular-nums;
}

.countdown__l {
  --delay: 260ms;
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(25 * var(--px));
  color: #623c2a;
}

.countdown__n--days {
  z-index: 83;
  top: calc(290 * var(--px)); /* 16:454 box y */
  left: calc(236 * var(--px));
}

.countdown__n--hours {
  z-index: 85;
  top: calc(290 * var(--px)); /* 16:461 box y */
  left: calc(330 * var(--px));
}

.countdown__n--minutes {
  z-index: 87;
  top: calc(383.93 * var(--px)); /* 16:468 box y */
  left: calc(236 * var(--px));
}

.countdown__n--seconds {
  z-index: 89;
  top: calc(383.93 * var(--px)); /* 16:475 box y */
  left: calc(330 * var(--px));
}

.countdown__l--days {
  z-index: 84;
  top: calc(358 * var(--px)); /* 16:457 box y */
  left: calc(230 * var(--px));
  width: calc(41 * var(--px));
}

.countdown__l--hours {
  z-index: 86;
  top: calc(358 * var(--px)); /* 16:464 box y */
  left: calc(318.5 * var(--px));
  width: calc(52 * var(--px));
}

.countdown__l--minutes {
  z-index: 88;
  top: calc(451.93 * var(--px)); /* 16:471 box y */
  left: calc(216 * var(--px));
  width: calc(69 * var(--px));
}

.countdown__l--seconds {
  z-index: 90;
  top: calc(451.93 * var(--px)); /* 16:478 box y */
  left: calc(310 * var(--px));
  width: calc(69 * var(--px));
}
</style>
