<script setup lang="ts">
/*
 * Frame 1 (1:3) band "wishes": y 9565..10763 of the body frame. A heading, a two-field
 * form, and the guest book. Art comes from src/lib/bands/wishes.ts (GENERATED,
 * scripts/gen_band.py) — only seven of the band's eighteen nodes are art; everything
 * else is live.
 *
 * NONE of the form's chrome is in the node dump: the two white fields, the Send pill and
 * the Show more pill are auto-layout frames the flatten never emitted, exactly like the
 * gift band's Copy pill. Their boxes are measured off the render and reproduced here:
 *
 *   name field   (92, 9742)  424 x 54, white
 *   wish field   (92, 9812)  424 x 88, white
 *   Send pill    (91, 9915)  426 x 54, #b2d3e2, fully rounded
 *   Show more    (85, 10344) 426 x 54, #b2d3e2, fully rounded
 *
 * The cards below the form are a FLOW, not absolute boxes: a live message is any number
 * of lines, and the Show more button has to move with them. Laid out at the first card's
 * origin, the design's own two cards and their button land on the render's rows.
 */
import { computed, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/wishes'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { formatWishStamp } from '../../lib/format'
import { DESIGN_MODE } from '../../lib/api'

const { el, shown } = useReveal(0.15)
const { wishes, sendWish, guest } = useWedding()

type Wish = { guest_name?: string; message?: string; created_at?: string | null }

/*
 * Frame 1 prints the same card twice — its mock data, reproduced so an unconfigured
 * render matches. A third is added so the design fallback's "Show more" reveals
 * something: the button is part of the design's layout, and one that does nothing is
 * worse than no button.
 */
const DESIGN_MESSAGE =
  'Wishing you a lifetime filled with endless love, gentle laughter, and countless beautiful moments together. Happy Wedding!'
const DESIGN: Wish[] = [
  { guest_name: 'Satrio & Istri', message: DESIGN_MESSAGE, created_at: '2025-06-09 09:00:00' },
  { guest_name: 'Satrio & Istri', message: DESIGN_MESSAGE, created_at: '2025-06-09 09:00:00' },
  {
    guest_name: 'Rian & Keluarga',
    message: 'Selamat menempuh hidup baru, semoga sakinah mawaddah warahmah.',
    created_at: '2025-06-09 09:00:00',
  },
]

/*
 * In DESIGN MODE the only rows `wishes` ever holds are the ones this visitor just posted
 * — `sendWish` answers locally rather than calling the API — so a plain
 * `live.length ? live : DESIGN` empties the guest book the moment someone tries the form.
 * Keep the design's cards underneath instead. On live data the API's list is the whole
 * truth and the design's mock guests must never appear beneath it.
 */
const list = computed<Wish[]>(() => {
  const live = (wishes.value as Wish[]).filter((w) => w?.guest_name || w?.message)
  if (!live.length) return DESIGN
  return DESIGN_MODE ? [...live, ...DESIGN] : live
})

// The design shows two and hides the rest behind the button.
const PAGE = 2
const shownCount = ref(PAGE)
const visible = computed(() => list.value.slice(0, shownCount.value))
const hasMore = computed(() => shownCount.value < list.value.length)

const name = ref(guest.value?.name || '')
const message = ref('')
const sending = ref(false)
const error = ref('')

async function send() {
  error.value = ''
  if (!message.value.trim()) {
    error.value = 'Ucapannya masih kosong.'
    return
  }
  sending.value = true
  try {
    await sendWish({
      guest_name: name.value.trim() || 'Tamu',
      message: message.value.trim(),
    })
    message.value = ''
  } catch (err: any) {
    error.value = err?.message || 'Gagal mengirim ucapan. Coba lagi.'
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <section
    :ref="el"
    class="band wishes"
    :class="{ 'is-in': shown }"
    aria-labelledby="wishes-title"
  >
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 33:525 — the heading. -->
    <h2 id="wishes-title" class="wishes__title">Wedding Wishes</h2>

    <!-- 33:478 / 33:481 / 33:484 — the form. The plates are reconstructed, see above. -->
    <form class="wishes__form" @submit.prevent="send">
      <input v-model="name" class="wishes__name" type="text" placeholder="Name" />
      <textarea v-model="message" class="wishes__message" placeholder="Give your wish" />
      <button class="wishes__send" type="submit" :disabled="sending">
        {{ sending ? 'Mengirim…' : 'Send' }}
      </button>
      <p v-if="error" class="wishes__error" role="alert">{{ error }}</p>
    </form>

    <!-- 33:510..33:517 — the guest book, plus 33:524's button at its foot. -->
    <div class="wishes__list">
      <article v-for="(w, i) in visible" :key="i" class="wishes__card">
        <p class="wishes__from">{{ w.guest_name || 'Tamu' }}</p>
        <p class="wishes__when">{{ formatWishStamp(w.created_at) }}</p>
        <p class="wishes__body">{{ w.message }}</p>
      </article>
      <button
        v-if="hasMore"
        class="wishes__more"
        type="button"
        @click="shownCount = list.length"
      >
        Show more
      </button>
    </div>
  </section>
</template>

<style scoped>
.wishes {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 33:525 — Roben Elegante Script 32, #aa7a3a. Box's own 57 for line-height. */
.wishes__title {
  --delay: 80ms;
  z-index: 227;
  top: calc(88 * var(--px)); /* 33:525 box y 9653, band-local 88 */
  left: calc(163 * var(--px));
  width: calc(270 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
  color: #aa7a3a;
}

/*
 * The form. Positioned as one block at the name field's origin so the three controls
 * keep their measured gaps; `.band > *` already makes it absolute.
 */
.wishes__form {
  --delay: 180ms;
  z-index: 232;
  top: calc(177 * var(--px)); /* name plate y 9742, band-local 177 */
  left: calc(85 * var(--px));
  width: calc(426 * var(--px));
  text-align: left;
}

.wishes__name,
.wishes__message {
  display: block;
  box-sizing: border-box;
  margin-left: calc(7 * var(--px)); /* the fields sit at x 92, the Send pill at 91 */
  width: calc(424 * var(--px));
  border: 0;
  border-radius: calc(8 * var(--px));
  background: #ffffff;
  padding: calc(15.5 * var(--px)) calc(11.8 * var(--px));
  font-family: var(--font-wish);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(23 * var(--px));
  color: #3f3f3f;
}

.wishes__name {
  height: calc(54 * var(--px));
}

/* 33:481's box is 88 tall and its first line starts 11.8 down, not 15.5. */
.wishes__message {
  margin-top: calc(16 * var(--px)); /* 9812 - (9742 + 54) */
  height: calc(88 * var(--px));
  /* 33:481's first line starts 12.8 down and 10.8 in, a pixel off the name field's. */
  padding-top: calc(12.8 * var(--px));
  padding-left: calc(10.8 * var(--px));
  line-height: calc(30 * var(--px));
  resize: none;
}

.wishes__name::placeholder,
.wishes__message::placeholder {
  /* 33:478 / 33:481 — #757575 at 50%, which is what Figma's "#75757580" means. */
  color: #75757580;
}

/* 33:484's plate: 426 x 54 at x 91, #b2d3e2, fully rounded. */
.wishes__send,
.wishes__more {
  display: block;
  box-sizing: border-box;
  width: calc(426 * var(--px));
  height: calc(54 * var(--px));
  padding: 0;
  border: 0;
  border-radius: 999px;
  background: #b2d3e2;
  font-family: var(--font-wish);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  /* 56, not the plate's 54: Bellefair's line box centres 1px high in a 54 box. */
  line-height: calc(56 * var(--px));
  color: #445c68;
  text-align: center;
  cursor: pointer;
  /* `scale`, not a transform: the band's reveal owns `transform` and would win. */
  transition: background 240ms ease, scale 240ms ease;
}

.wishes__send {
  margin-top: calc(15 * var(--px)); /* 9915 - (9812 + 88) */
  margin-left: calc(6 * var(--px)); /* the pill sits at x 91 against the block's 85 */
}

.wishes__send:hover,
.wishes__more:hover,
.wishes__send:focus-visible,
.wishes__more:focus-visible {
  background: #9cc4d6;
  scale: 1.02;
}

.wishes__send:disabled {
  cursor: progress;
  opacity: 0.7;
}

.wishes__error {
  margin: calc(6 * var(--px)) 0 0 calc(6 * var(--px));
  font-family: var(--font-wish);
  font-size: calc(16 * var(--px));
  color: #a3401f;
}

/*
 * 33:510..33:517 and 33:524. A flow rather than eight absolute boxes: the design's two
 * cards are 174 apart with a 147-tall stack of copy in each, which is a 27 gap, and the
 * button sits 27 below the second card. Reproducing THAT lets a longer live message push
 * the button down instead of running underneath it.
 */
.wishes__list {
  --delay: 420ms;
  z-index: 238;
  top: calc(431 * var(--px)); /* 33:510 box y 9996, band-local 431 */
  left: calc(85 * var(--px));
  width: calc(426 * var(--px));
  text-align: left;
}

.wishes__card + .wishes__card,
.wishes__more {
  margin-top: calc(27 * var(--px));
}

/* 33:510 — Abhaya Libre ExtraBold 20/30, #455d69, at x 91. */
/*
 * The three rows each want a 1px nudge, and they do not want the same one: Abhaya's
 * line box sits 1 low at this size and Bellefair's sits 1 high at both 18 and 20. Same
 * per-(face, size) rule as Ibarra's +1 in the akad band, measured by colour-keying
 * #455d69 in both images.
 */
.wishes__from {
  position: relative;
  top: calc(-1 * var(--px));
  margin-left: calc(6 * var(--px));
  font-family: var(--font-wish-name);
  font-weight: 800;
  /*
   * 18.4, not Figma's 20. Abhaya Libre ExtraBold sets "Satrio & Istri" 113 wide and 13
   * tall at 20 where the render has 104 x 12 — the SAME 0.92 on both axes, which is a
   * scale rather than the usual width-vs-height trade, so one number fixes both. Weight
   * 700 renders identically to 800 in this family, so it is not a weight mismatch.
   */
  font-size: calc(18.4 * var(--px));
  line-height: calc(30 * var(--px));
  color: #455d69;
}

/* 33:512 — Bellefair 18/27, #455d69, at x 91. */
.wishes__when {
  position: relative;
  top: calc(1 * var(--px));
  margin-left: calc(6 * var(--px));
  font-family: var(--font-wish);
  font-weight: 400;
  font-size: calc(18 * var(--px));
  line-height: calc(27 * var(--px));
  color: #455d69;
}

/* 33:514 — Bellefair 20/30, #455d69, in a 427 box at x 90. */
.wishes__body {
  position: relative;
  top: calc(1 * var(--px));
  margin-left: calc(5 * var(--px));
  width: calc(427 * var(--px));
  font-family: var(--font-wish);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(30 * var(--px));
  color: #455d69;
}

@media (prefers-reduced-motion: reduce) {
  .wishes__send,
  .wishes__more {
    transition: none;
  }
}
</style>
