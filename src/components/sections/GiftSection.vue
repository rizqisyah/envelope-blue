<script setup lang="ts">
/*
 * Frame 1 (1:3) band "gift": y 8865..9565 of the body frame. Two bank cards inside one
 * floral arch. Art comes from src/lib/bands/gift.ts (GENERATED, scripts/gen_band.py).
 *
 * The band is the cleanest run of the right-edge rule in the frame: every left-side node
 * declares its RIGHT edge and every right-side node declares its left one, in five
 * matched pairs. See the block above PIN_Y in scripts/gen_band.py.
 *
 * The Copy pill is not in the node dump at all. Its "Copy" label (31:408) reports a
 * parent-relative origin of 24,8 inside a box the flatten never emitted, and the render
 * shows a 92x41 plate at (252, 9250) filled #80a2ba. It has to be a real button anyway,
 * so it is drawn here — the same treatment the bride band's Instagram pill got.
 */
import { computed, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gift'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'

const { el, shown } = useReveal(0.15)
const { gift } = useWedding()

type Card = { bank: string; number: string; owner: string }

/*
 * The design prints the SAME account twice — its mock data, not a mistake to correct.
 * An unconfigured render therefore matches the frame; live rows replace both.
 * `bank_name` / `account_number` / `account_name` are the field names template 5's gift
 * band settled on; getHome's `rekening` rows are undocumented here.
 */
const DESIGN: Card[] = [
  { bank: 'Bank Bca (014)', number: '7402004234', owner: 'Alexander James Whitmore' },
  { bank: 'Bank Bca (014)', number: '7402004234', owner: 'Alexander James Whitmore' },
]

const cards = computed<Card[]>(() => {
  const live = (gift.value as any[])
    .map((g) => ({
      bank: (g?.bank_name || '').trim(),
      number: (g?.account_number || '').trim(),
      owner: (g?.account_name || '').trim(),
    }))
    .filter((c) => c.number || c.owner)
  // Two slots: the arch behind them draws two cards, so a third account has nowhere to
  // go and falls off the end rather than painting past the last one.
  return live.length ? live.slice(0, 2) : DESIGN
})

/*
 * Clipboard is permission-gated and absent over plain http, so a failure is not an
 * error worth surfacing — the number is on screen either way. The label confirms the
 * copy for a moment instead; the button carries `aria-live` so that swap is announced
 * rather than only seen.
 */
const copied = ref(-1)
async function copy(i: number, text: string) {
  if (!text) return
  try {
    await navigator.clipboard.writeText(text)
    copied.value = i
    window.setTimeout(() => (copied.value = -1), 1600)
  } catch {
    /* no clipboard: leave the label alone */
  }
}

/*
 * Both cards are the same six boxes 204px apart — 31:390/397/401/404/408 and
 * 31:432/434/436/437/442 pair up exactly — so the offset drives the layout rather than
 * ten hand-written rules.
 */
const CARD_GAP = 204
const ROWS = [
  { key: 'bank', z: 195, top: 264, left: 218, width: 160, cls: 'gift__bank' },
  { key: 'number', z: 196, top: 294, left: 243, width: 110, cls: 'gift__number' },
  { key: 'ownerLabel', z: 197, top: 323, left: 248.5, width: 107, cls: 'gift__owner-label' },
  { key: 'owner', z: 198, top: 348, left: 178.5, width: 239, cls: 'gift__owner' },
] as const
</script>

<template>
  <section :ref="el" class="band gift" :class="{ 'is-in': shown }" aria-labelledby="gift-title">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 31:415 — the heading. -->
    <h2 id="gift-title" class="gift__title">Wedding Gift</h2>

    <!-- 31:382 — the invitation to give. -->
    <p class="gift__lede">
      Should you wish to leave a token of affection for the happy couple, you may kindly do
      so below.
    </p>

    <template v-for="(card, i) in cards" :key="i">
      <p
        v-for="row in ROWS"
        :key="row.key"
        :class="row.cls"
        :style="{
          zIndex: row.z + i,
          top: `calc(${row.top + i * CARD_GAP} * var(--px))`,
          left: `calc(${row.left} * var(--px))`,
          width: `calc(${row.width} * var(--px))`,
          '--delay': `${300 + i * 260 + ROWS.indexOf(row) * 60}ms`,
        }"
      >
        {{ row.key === 'ownerLabel' ? 'Account Owner' : card[row.key as keyof Card] }}
      </p>

      <!-- The plate the dump never emitted, plus 31:408 / 31:442 on top of it. -->
      <button
        type="button"
        class="gift__copy"
        aria-live="polite"
        :style="{
          zIndex: 199 + i,
          top: `calc(${385 + i * CARD_GAP} * var(--px))`,
          '--delay': `${300 + i * 260 + 300}ms`,
        }"
        @click="copy(i, card.number)"
      >
        {{ copied === i ? 'Tersalin' : 'Copy' }}
      </button>
    </template>
  </section>
</template>

<style scoped>
.gift {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 31:415 — Roben Elegante Script 32, #aa7a3a. Box's own 57 for line-height. */
.gift__title {
  --delay: 80ms;
  z-index: 226;
  top: calc(90 * var(--px)); /* 31:415 box y 8955, band-local 90 */
  left: calc(190 * var(--px));
  width: calc(216 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
  color: #aa7a3a;
}

/*
 * 31:382 — Ibarra Real Nova 20/30, #616161, three lines wrapped by its own 380 box.
 * The +1 here and on the 20px rows below is Ibarra's line box at that size; the 16px
 * "Account Owner" takes none. Measured on the akad band, holds here.
 */
.gift__lede {
  --delay: 180ms;
  z-index: 194;
  top: calc(164 * var(--px)); /* 31:382 box y 9028 + 1 */
  left: calc(108 * var(--px));
  width: calc(380 * var(--px));
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #616161;
}

/*
 * 31:390 / 31:432 — Ibarra Real Nova SemiBold 20/30, #623c2a.
 *
 * The render sets the bank line in CAPS while Figma's `characters` are "Bank Bca (014)".
 * `get_nodes_info` reports no `textCase`, the same blind spot as opacity and blendMode, so
 * the only evidence is the render: its ink is 157 wide where mixed case gives 129.
 * Uppercased in CSS rather than in the string, so live `bank_name` gets it too.
 */
.gift__bank {
  text-transform: uppercase;
}

.gift__bank,
.gift__number,
.gift__owner {
  font-family: var(--font-countdown);
  font-weight: 600;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #623c2a;
}

/* 31:401 / 31:436 — Ibarra Real Nova 16, #4e685c. Figma declares no line-height. */
.gift__owner-label {
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(16 * var(--px));
  line-height: calc(20 * var(--px));
  color: #4e685c;
}

/*
 * The Copy plate: 92x41 at x 252, radius fully rounded, #80a2ba — all measured off the
 * render, since the node itself never reached the dump. Its label is 31:408 / 31:442,
 * Ibarra Real Nova 20 in #f5f5f5.
 */
.gift__copy {
  left: calc(252 * var(--px));
  width: calc(92 * var(--px));
  height: calc(41 * var(--px));
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: #80a2ba;
  font-family: var(--font-countdown);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(41 * var(--px));
  color: #f5f5f5;
  cursor: pointer;
  /* `scale`, not a transform: the band's reveal owns `transform` and would win. */
  transition: background 240ms ease, scale 240ms ease;
}

.gift__copy:hover,
.gift__copy:focus-visible {
  background: #6b8ca6;
  scale: 1.04;
}

@media (prefers-reduced-motion: reduce) {
  .gift__copy {
    transition: none;
  }
}
</style>
