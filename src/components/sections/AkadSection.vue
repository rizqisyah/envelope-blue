<script setup lang="ts">
/*
 * Frame 1 (1:3) band "akad": y 4425..5907 of the body frame. Three scenes in one band —
 * the blue valley that hands over from the quote, the ornate date cartouche, and the
 * akad card itself. They share one floral arch whose layers cross all three, so
 * splitting them would put that arch in three coordinate spaces for no gain.
 * Art comes from src/lib/bands/akad.ts (GENERATED, scripts/gen_band.py).
 *
 * Both seams are ground plates and both are the render's own: 54:20 opens the band at
 * 4425, and 22:822 (the card frame) ends at 5907 exactly where resepsi's first node
 * begins. Nine of its twenty-four layers are position-pinned — see the block above
 * PIN_Y in scripts/gen_band.py for what the chain got wrong and why.
 *
 * The design prints the CARTOUCHE date in Indonesian ("Kamis / 27 / Desember 2026") and
 * the CARD date in English ("Saturday, / 06 September 2025"), and they are not even the
 * same day. That is the design's own inconsistency in its mock copy; both are reproduced,
 * and live data drives both from the same acara entry.
 */
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/akad'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { formatEventDate, formatEventDateId, formatEventTime } from '../../lib/format'

const { el, shown } = useReveal(0.15)
const { acara } = useWedding()

/*
 * The akad is the first acara entry with anything in it. Field names follow the ones
 * template 5's AcaraSection settled on (`name`, `event_date`, `event_time`,
 * `location_name`, `address`, `maps_url`); getHome's rows are undocumented here.
 */
const event = computed(() => (acara.value as any[]).find((a) => a?.name || a?.event_date) || null)

/*
 * Design copy is printed ONLY when there is no live event. Topping a live event up with
 * the design's venue would send guests to a real address in Cumbria, and "Family Only"
 * and "United Kingdom" have no API field at all, so they cannot be anything but the
 * design's own placeholder.
 */
const card = computed(() => {
  const e = event.value
  if (!e) {
    return {
      title: 'Akad Nikah',
      note: 'Family Only',
      date: 'Saturday,\n06 September 2025',
      time: '1:00 PM - End',
      venue: 'Melmerby Hall & Stag Cottage',
      address: 'Melmerby, Penrith CA10 1HB',
      country: 'United Kingdom',
      maps: '',
    }
  }
  const when = formatEventDate(e.event_date)
  return {
    title: e.name || 'Akad Nikah',
    note: '',
    date: when ? `${when.weekday},\n${when.date}` : '',
    time: formatEventTime(e.event_time) || '',
    venue: e.location_name || '',
    address: e.address || '',
    country: '',
    maps: e.maps_url || '',
  }
})

// 22:845 / 22:844 — the cartouche, in Indonesian and on its own three lines.
const stamp = computed(() => {
  const id = formatEventDateId(event.value?.event_date)
  return id
    ? { weekday: id.weekday, date: `${id.day}\n${id.monthYear}` }
    : { weekday: 'Kamis', date: '27\nDesember 2026' }
})
</script>

<template>
  <section :ref="el" class="band akad" :class="{ 'is-in': shown }" aria-labelledby="akad-title">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 22:845 / 22:844 — the date cartouche. Decorative repeat of the card's date. -->
    <p class="akad__stampDay" aria-hidden="true">{{ stamp.weekday }}</p>
    <p class="akad__stampDate" aria-hidden="true">{{ stamp.date }}</p>

    <!-- 23:856 — the card's heading. -->
    <h2 id="akad-title" class="akad__title">{{ card.title }}</h2>

    <!-- 99:6 — design-only note; empty once a live event replaces the card. -->
    <p class="akad__note">{{ card.note }}</p>

    <!-- 23:860 — weekday and date on two authored lines. -->
    <p class="akad__date">{{ card.date }}</p>

    <!-- 23:863 — the time range. -->
    <p class="akad__time">{{ card.time }}</p>

    <!-- 23:869 / 23:872 / 23:875 — venue, street, country. -->
    <p class="akad__venue">{{ card.venue }}</p>
    <p class="akad__address">{{ card.address }}</p>
    <p class="akad__country">{{ card.country }}</p>

    <!--
      23:879 — underlined in the render, so it reads as a link whether or not the API
      sends one. With no url it stays a label rather than a dead anchor.
    -->
    <a
      v-if="card.maps"
      class="akad__maps"
      :href="card.maps"
      target="_blank"
      rel="noopener noreferrer"
      >View Maps</a
    >
    <p v-else class="akad__maps">View Maps</p>
  </section>
</template>

<style scoped>
.akad {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 22:845 — Pinyon Script 40/36, #aa7a3a, centred. The design's own face. */
.akad__stampDay {
  --delay: 80ms;
  z-index: 155;
  top: calc(539 * var(--px)); /* 22:845 box y 4964, band-local 539 */
  left: calc(248 * var(--px));
  width: calc(99 * var(--px));
  font-family: var(--font-script-date);
  font-weight: 400;
  font-size: calc(40 * var(--px));
  line-height: calc(36 * var(--px));
  color: #aa7a3a;
}

/* 22:844 — Cinzel Bold 20/21, #aa7a3a, two authored lines. */
.akad__stampDate {
  --delay: 200ms;
  z-index: 154;
  top: calc(579 * var(--px)); /* 22:844 box y 5004, band-local 579 */
  left: calc(186 * var(--px));
  width: calc(226 * var(--px));
  font-family: var(--font-verse);
  font-weight: 700;
  font-size: calc(20 * var(--px));
  line-height: calc(21 * var(--px));
  white-space: pre-line;
  color: #aa7a3a;
}

/*
 * 23:856 — Kaleagnetta 48, #4e685c, centred in a 189 box. Kaleagnetta has no file, so
 * this is still a substitute — but Palisade now, not Sacramento (see --font-hand).
 *
 * Sacramento was picked from the faces already on fontsource. Measured against the
 * render's OWN ink — isolated by shooting the sheet with these two headings hidden and
 * differencing — Kaleagnetta sets this phrase at an ink density of 0.144 and an aspect of
 * 4.02. Sacramento is 0.185 and 6.21: a third heavier and half again as wide for its
 * height, which is why its width match left the ink 31 tall against the render's 48.
 * Palisade, swept out of the 126 local font files, is 0.143 and 4.22 — the same weight of
 * line and very nearly the same proportion.
 *
 * Width-matched the same way: Palisade sets this phrase 3.685 design px wide per px of
 * font-size, so the render's 193 wants 52.4. Its ink then stands 46 against the render's
 * 48, where Sacramento stood 31.
 *
 * Figma declares no line-height, so the box's own 66 stands in for it.
 */
.akad__title {
  --delay: 320ms;
  z-index: 271;
  top: calc(926 * var(--px)); /* 23:856 box y 5349 + 2 — Palisade's line box, measured */
  left: calc(204.4 * var(--px)); /* 23:856 box x 203.4 + 1 — measured */
  width: calc(189 * var(--px));
  font-family: var(--font-hand);
  font-weight: 400;
  font-size: calc(52.4 * var(--px)); /* 193 / 3.685 — measured on THIS phrase */
  line-height: calc(66 * var(--px));
  color: #4e685c;
}

/*
 * 99:6 — Ibarra Real Nova Italic 20/30, #4e685c.
 *
 * The +1 on `top` here and on the four nodes below it is Ibarra Real Nova's own line-box
 * offset AT 20px: colour-keying #4e685c and #623c2a in both images puts every 20px node
 * exactly 1px high at Figma's own y and every 16px node (23:872, 23:875) exactly on it.
 * The offset is per (face, size), not per face — see SLICING.md.
 */
.akad__note {
  --delay: 400ms;
  z-index: 272;
  top: calc(991 * var(--px)); /* 99:6 box y 5415 + 1 — Ibarra line box, see above */
  left: calc(244.1 * var(--px));
  width: calc(106 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-style: italic;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #4e685c;
}

/* 23:860 — Ibarra Real Nova 20/30, #4e685c, two authored lines. */
.akad__date {
  --delay: 480ms;
  z-index: 273;
  top: calc(1031 * var(--px)); /* 23:860 box y 5455 + 1 */
  left: calc(216.6 * var(--px));
  width: calc(163 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  white-space: pre-line;
  color: #4e685c;
}

/* 23:863 — Ibarra Real Nova Bold 20/26.6, #4e685c. */
.akad__time {
  --delay: 560ms;
  z-index: 274;
  top: calc(1095 * var(--px)); /* 23:863 box y 5519 + 1 */
  left: calc(233.1 * var(--px));
  width: calc(130 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 700;
  font-size: calc(20 * var(--px));
  line-height: calc(26.6 * var(--px));
  color: #4e685c;
}

/* 23:869 — Ibarra Real Nova SemiBold 20/30, #623c2a. */
.akad__venue {
  --delay: 640ms;
  z-index: 275;
  top: calc(1130 * var(--px)); /* 23:869 box y 5554 + 1 */
  left: calc(164.6 * var(--px));
  width: calc(267 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 600;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #623c2a;
}

/* 23:872 — Ibarra Real Nova 16/24, #623c2a. */
.akad__address {
  --delay: 700ms;
  z-index: 276;
  top: calc(1159 * var(--px)); /* 23:872 box y 5584, band-local 1159 */
  left: calc(196.6 * var(--px));
  width: calc(203 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(16 * var(--px));
  line-height: calc(24 * var(--px));
  color: #623c2a;
}

/* 23:875 — Ibarra Real Nova 16/24, #623c2a. */
.akad__country {
  --delay: 760ms;
  z-index: 277;
  top: calc(1191 * var(--px)); /* 23:875 box y 5616, band-local 1191 */
  left: calc(241.6 * var(--px));
  width: calc(113 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(16 * var(--px));
  line-height: calc(24 * var(--px));
  color: #623c2a;
}

/* 23:879 — Ibarra Real Nova Bold 20/30, #4e685c, underlined in the render. */
.akad__maps {
  --delay: 840ms;
  z-index: 278;
  top: calc(1228 * var(--px)); /* 23:879 box y 5652.1 + 1 */
  left: calc(249.1 * var(--px));
  width: calc(98 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 700;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #4e685c;
  /*
   * The render's rule is a single 1px line at y 5682 -- 9px under the baseline, not the
   * 3-4 a default underline draws, and one design pixel thick rather than two. Measured
   * off the render's own row profile: 98 px wide at (121, 140, 131), which is #4e685c
   * anti-aliased across one row.
   */
  text-decoration: underline;
  text-underline-offset: calc(8 * var(--px));
  text-decoration-thickness: calc(1 * var(--px));
  transition: color 240ms ease;
}

a.akad__maps:hover,
a.akad__maps:focus-visible {
  color: #2f4238;
}
</style>
