<script setup lang="ts">
/*
 * Frame 1 (1:3) band "resepsi": y 5907..7034 of the body frame. The akad band's scene
 * again — date cartouche, then the event card — but flipped, and with the reception's
 * copy in it. Art comes from src/lib/bands/resepsi.ts (GENERATED, scripts/gen_band.py).
 *
 * The flip is in the DATA, not the art: twelve of the band's seventeen layers declare a
 * right edge where the chain reads a left one, and four of those also declare a bottom
 * edge. `29:242`, the card frame, resolves to x 24 — the same x as akad's `22:822`,
 * because it is the same card. See the block above PIN_Y in scripts/gen_band.py.
 *
 * `54:41` is this band's dead 1x1 duplicate of the card plate, the twin of akad's
 * `54:35`; both live in build_refs.py's EMPTY.
 */
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/resepsi'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { formatEventDate, formatEventDateId, formatEventTime } from '../../lib/format'

const { el, shown } = useReveal(0.15)
const { acara } = useWedding()

const live = computed(() => (acara.value as any[]).filter((a) => a?.name || a?.event_date))

/*
 * The reception is the SECOND acara entry. All or nothing, never a mix: once the API
 * sends any event at all, a wedding with only an akad leaves this card empty rather than
 * printing the design's placeholder reception under a real invitation — Melmerby Hall is
 * a real address in Cumbria and a guest would drive to it.
 */
const event = computed(() => (live.value.length ? live.value[1] || null : null))
const isDesign = computed(() => live.value.length === 0)

const card = computed(() => {
  if (isDesign.value) {
    return {
      title: 'Resepsi',
      date: 'Saturday,\n06 September 2025',
      time: '1:00 PM - End',
      venue: 'Melmerby Hall & Stag Cottage',
      address: 'Melmerby, Penrith CA10 1HB',
      country: 'United Kingdom',
      maps: '',
    }
  }
  const e = event.value
  const when = formatEventDate(e?.event_date)
  return {
    title: e?.name || 'Resepsi',
    date: when ? `${when.weekday},\n${when.date}` : '',
    time: formatEventTime(e?.event_time) || '',
    venue: e?.location_name || '',
    address: e?.address || '',
    country: '',
    maps: e?.maps_url || '',
  }
})

// 29:273 / 29:272 — the cartouche, in Indonesian, exactly as the akad band's.
const stamp = computed(() => {
  const id = formatEventDateId(event.value?.event_date)
  return id
    ? { weekday: id.weekday, date: `${id.day}\n${id.monthYear}` }
    : { weekday: 'Kamis', date: '27\nDesember 2026' }
})
</script>

<template>
  <section
    :ref="el"
    class="band resepsi"
    :class="{ 'is-in': shown }"
    aria-labelledby="resepsi-title"
  >
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 29:273 / 29:272 — the date cartouche. -->
    <p class="resepsi__stampDay" aria-hidden="true">{{ stamp.weekday }}</p>
    <p class="resepsi__stampDate" aria-hidden="true">{{ stamp.date }}</p>

    <!-- 103:11 — the card's heading. -->
    <h2 id="resepsi-title" class="resepsi__title">{{ card.title }}</h2>

    <!-- 103:14 — weekday and date on two authored lines. -->
    <p class="resepsi__date">{{ card.date }}</p>

    <!-- 103:15 — the time range. -->
    <p class="resepsi__time">{{ card.time }}</p>

    <!-- 103:20 / 103:22 / 103:24 — venue, street, country. -->
    <p class="resepsi__venue">{{ card.venue }}</p>
    <p class="resepsi__address">{{ card.address }}</p>
    <p class="resepsi__country">{{ card.country }}</p>

    <!-- 103:26 — the same 1px rule as the akad band's; see AkadSection for the numbers. -->
    <a
      v-if="card.maps"
      class="resepsi__maps"
      :href="card.maps"
      target="_blank"
      rel="noopener noreferrer"
      >View Maps</a
    >
    <p v-else class="resepsi__maps">View Maps</p>
  </section>
</template>

<style scoped>
.resepsi {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 29:273 — Pinyon Script 40/36, #aa7a3a. */
.resepsi__stampDay {
  --delay: 80ms;
  z-index: 160;
  top: calc(118 * var(--px)); /* 29:273 box y 6025, band-local 118 */
  left: calc(248.5 * var(--px));
  width: calc(99 * var(--px));
  font-family: var(--font-script-date);
  font-weight: 400;
  font-size: calc(40 * var(--px));
  line-height: calc(36 * var(--px));
  color: #aa7a3a;
}

/* 29:272 — Cinzel Bold 20/21, #aa7a3a, two authored lines. */
.resepsi__stampDate {
  --delay: 180ms;
  z-index: 161;
  top: calc(166 * var(--px)); /* 29:272 box y 6073, band-local 166 */
  left: calc(185 * var(--px));
  width: calc(226 * var(--px));
  font-family: var(--font-verse);
  font-weight: 700;
  font-size: calc(20 * var(--px));
  line-height: calc(21 * var(--px));
  white-space: pre-line;
  color: #aa7a3a;
}

/*
 * 103:11 — Kaleagnetta 48 in Sacramento, like the akad heading, but NOT at the akad
 * heading's size: the render's ink here is 113 wide and Sacramento sets "Resepsi" 126
 * wide at Figma's own 48, so this word wants ~43.8 where "Akad Nikah" wanted 39.3. The
 * width match is per WORD, which is the third node in this frame to demonstrate it.
 */
.resepsi__title {
  --delay: 280ms;
  z-index: 31;
  top: calc(494 * var(--px)); /* 103:11 box y 6397 + 4 — Palisade's line box, measured */
  left: calc(240.4 * var(--px)); /* 103:11 box x */
  width: calc(114 * var(--px));
  font-family: var(--font-hand);
  font-weight: 400;
  font-size: calc(60.8 * var(--px)); /* 115 / 1.89 — measured on THIS word, see the akad band */
  line-height: calc(66 * var(--px));
  color: #4e685c;
}

/*
 * 103:14 — Ibarra Real Nova 20/30, #4e685c. The +1 on `top` here and on the three 20px
 * nodes below it is Ibarra's line-box offset at that size; the 16px nodes take none.
 * Measured on the akad band, confirmed here.
 */
.resepsi__date {
  --delay: 380ms;
  z-index: 32;
  top: calc(597 * var(--px)); /* 103:14 box y 6503 + 1 */
  left: calc(216.6 * var(--px));
  width: calc(163 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  white-space: pre-line;
  color: #4e685c;
}

/* 103:15 — Ibarra Real Nova Bold 20/26.6, #4e685c. */
.resepsi__time {
  --delay: 460ms;
  z-index: 33;
  top: calc(661 * var(--px)); /* 103:15 box y 6567 + 1 */
  left: calc(233.1 * var(--px));
  width: calc(130 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 700;
  font-size: calc(20 * var(--px));
  line-height: calc(26.6 * var(--px));
  color: #4e685c;
}

/* 103:20 — Ibarra Real Nova SemiBold 20/30, #623c2a. */
.resepsi__venue {
  --delay: 540ms;
  z-index: 34;
  top: calc(696 * var(--px)); /* 103:20 box y 6602 + 1 */
  left: calc(164.6 * var(--px));
  width: calc(267 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 600;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #623c2a;
}

/* 103:22 — Ibarra Real Nova 16/24, #623c2a. */
.resepsi__address {
  --delay: 600ms;
  z-index: 35;
  top: calc(725 * var(--px)); /* 103:22 box y 6632, band-local 725 */
  left: calc(196.6 * var(--px));
  width: calc(203 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(16 * var(--px));
  line-height: calc(24 * var(--px));
  color: #623c2a;
}

/* 103:24 — Ibarra Real Nova 16/24, #623c2a. */
.resepsi__country {
  --delay: 660ms;
  z-index: 36;
  top: calc(757 * var(--px)); /* 103:24 box y 6664, band-local 757 */
  left: calc(241.6 * var(--px));
  width: calc(113 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(16 * var(--px));
  line-height: calc(24 * var(--px));
  color: #623c2a;
}

/* 103:26 — Ibarra Real Nova Bold 20/30, #4e685c, with the design's own 1px rule. */
.resepsi__maps {
  --delay: 740ms;
  z-index: 37;
  top: calc(794 * var(--px)); /* 103:26 box y 6700.1 + 1 */
  left: calc(249.1 * var(--px));
  width: calc(98 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 700;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #4e685c;
  text-decoration: underline;
  text-underline-offset: calc(8 * var(--px));
  text-decoration-thickness: calc(1 * var(--px));
  transition: color 240ms ease;
}

a.resepsi__maps:hover,
a.resepsi__maps:focus-visible {
  color: #2f4238;
}
</style>
