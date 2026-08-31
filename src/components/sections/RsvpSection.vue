<script setup lang="ts">
/*
 * Frame 1 (1:3) band "rsvp": y 10763..11452 of the body frame. A heading on a white
 * oval, a line of copy, four fields and Send. Art comes from src/lib/bands/rsvp.ts
 * (GENERATED, scripts/gen_band.py).
 *
 * Like the wishes band, none of the form's chrome is in the node dump. The four field
 * plates and the Send pill are auto-layout frames the flatten never emitted; each one's
 * origin is its label's absolute position minus the parent-relative one Figma reports
 * (12.8, 12.8 for the fields, 194, 12 for Send), and the render confirms all five:
 *
 *   fields  (85, 11139 / 11200 / 11261 / 11322)  426 x 54, white, 1px #8d9879, radius 10
 *   Send    (85, 11398)                          426 x 54, #b2d3e2, fully rounded
 *
 * They are listed in solve_alpha.py's DRAWN_BOXES so the offline composite masks them.
 *
 * `submitRsvp` is imported from lib/api directly rather than through useWedding — that is
 * where DESIGN_MODE is enforced, and api.ts's own comment names this component as the
 * reason. In design mode it throws and the form reports it, which is the honest thing for
 * a template that is not wired to a wedding yet.
 */
import { onMounted, ref } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/rsvp'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { submitRsvp } from '../../lib/api'

const { el, shown } = useReveal(0.15)
const { slug, guest } = useWedding()

const name = ref('')
const phone = ref('')
const attendance = ref('')
const guests = ref('')
const sending = ref(false)
const error = ref('')
const done = ref(false)

/* The `?to=` link names the guest, so the field starts filled in for them. */
onMounted(() => {
  const known = guest.value?.name || new URLSearchParams(location.search).get('to')
  if (known) name.value = String(known)
})

/*
 * The button is NOT disabled until the form is valid: the render draws it at full
 * strength, and a control that greys out before the guest has typed anything reads as
 * broken rather than as guidance. Validation happens on submit and answers in the error
 * line under it.
 */
async function send() {
  error.value = ''
  if (!name.value.trim()) {
    error.value = 'Nama masih kosong.'
    return
  }
  if (!attendance.value) {
    error.value = 'Pilih kehadiran dulu.'
    return
  }
  sending.value = true
  try {
    await submitRsvp(slug.value, {
      guest_name: name.value.trim(),
      phone: phone.value.trim(),
      attendance_status: attendance.value,
      // The design asks for a count; an absent one means one seat for the guest named.
      guest_count: attendance.value === 'hadir' ? Number(guests.value) || 1 : 0,
    })
    done.value = true
  } catch (err: any) {
    error.value = err?.message || 'Gagal mengirim. Coba lagi.'
  } finally {
    sending.value = false
  }
}
</script>

<template>
  <section :ref="el" class="band rsvp" :class="{ 'is-in': shown }" aria-labelledby="rsvp-title">
    <BandArt :layers="LAYERS" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- 39:7 — the white oval the heading sits on. A flat #ffffff ellipse (CSS_SHAPES). -->
    <div class="rsvp__plate" aria-hidden="true" />

    <!-- 39:8 — the heading. -->
    <h2 id="rsvp-title" class="rsvp__title">Rsvp</h2>

    <!-- 40:10 — two authored lines. -->
    <p class="rsvp__lede">Mohon konfirmasi kehadiran Anda<br />melalui formulir reservasi di bawah:</p>

    <!-- 40:16 / 40:28 / 40:39 / 40:41 / 40:36 — the form; its plates are reconstructed. -->
    <form class="rsvp__form" @submit.prevent="send">
      <input v-model="name" class="rsvp__field" type="text" placeholder="Nama" />
      <input v-model="phone" class="rsvp__field" type="tel" placeholder="No Hp" />
      <select v-model="attendance" class="rsvp__field" :class="{ 'is-empty': !attendance }">
        <option value="" disabled>Will you be joining us?</option>
        <option value="hadir">Ya, saya akan hadir</option>
        <option value="tidak">Maaf, saya berhalangan</option>
      </select>
      <input
        v-model="guests"
        class="rsvp__field"
        type="number"
        min="1"
        placeholder="Number of Guests:"
      />
      <button class="rsvp__send" type="submit" :disabled="sending">
        {{ sending ? 'Mengirim…' : done ? 'Terkirim' : 'Send' }}
      </button>
      <p v-if="error" class="rsvp__error" role="alert">{{ error }}</p>
    </form>
  </section>
</template>

<style scoped>
.rsvp {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/* 39:7 — 270 x 119 at (163, 10932), flat #ffffff. Hard-edged, so a CSS ellipse is exact. */
.rsvp__plate {
  --delay: 60ms;
  z-index: 244;
  top: calc(169 * var(--px)); /* 39:7 box y 10932, band-local 169 */
  left: calc(163 * var(--px));
  width: calc(270 * var(--px));
  height: calc(119 * var(--px));
  border-radius: 50%;
  background: #ffffff;
}

/* 39:8 — Roben Elegante Script 32, #aa7a3a. Box's own 57 for line-height. */
.rsvp__title {
  --delay: 140ms;
  z-index: 245;
  top: calc(200 * var(--px)); /* 39:8 box y 10963, band-local 200 */
  left: calc(252 * var(--px));
  width: calc(92 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
  color: #aa7a3a;
}

/*
 * 40:10 — EB Garamond 20/20, #aa7a3a, centred. The design's own face, from fontsource.
 * Its box is 296 wide and the string breaks after "Anda"; a 296 box wraps it there on its
 * own, but the break is authored in the markup so a longer live line cannot move it.
 */
.rsvp__lede {
  --delay: 220ms;
  z-index: 246;
  top: calc(311 * var(--px)); /* 40:10 box y 11074, band-local 311 */
  left: calc(150 * var(--px));
  width: calc(296 * var(--px));
  font-family: var(--font-garamond);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(20 * var(--px));
  color: #aa7a3a;
}

/* The form block, positioned at the first field plate's origin. */
.rsvp__form {
  --delay: 320ms;
  z-index: 247;
  top: calc(376 * var(--px)); /* field plate y 11139, band-local 376 */
  left: calc(85 * var(--px));
  width: calc(426 * var(--px));
  text-align: left;
}

/*
 * The four plates: 426 x 54, 61 apart (so a 7px gap), white with a 1px #8d9879 rule and
 * a radius of 10 — all measured off the render, since none of them is a node. Their
 * labels are Bellefair 20 in #1e3c7280, inset 12.8 both ways.
 */
.rsvp__field {
  display: block;
  box-sizing: border-box;
  width: calc(426 * var(--px));
  height: calc(54 * var(--px));
  border: calc(1 * var(--px)) solid #8d9879;
  border-radius: calc(10 * var(--px));
  background: #ffffff;
  /*
   * A single-line <input> centres its text in the content box whatever `padding-top`
   * says, so the design's 12.8 inset cannot be expressed as padding alone: the render
   * puts the ink 12.8 from the plate's top, which is 2.7 ABOVE centre in a 54 box.
   * The extra padding-bottom is what buys that back — measured, not derived.
   */
  padding: calc(8.8 * var(--px)) calc(11.8 * var(--px)) calc(16.8 * var(--px));
  font-family: var(--font-wish);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(23 * var(--px));
  color: #1e3c72;
  appearance: none;
}

.rsvp__field + .rsvp__field {
  margin-top: calc(7 * var(--px));
}

.rsvp__field::placeholder,
.rsvp__field.is-empty {
  color: #1e3c7280;
}

.rsvp__field:focus-visible {
  outline: calc(2 * var(--px)) solid #8d9879;
  outline-offset: calc(1 * var(--px));
}

/* 40:36's plate: 426 x 54 at the same x, #b2d3e2, fully rounded. */
.rsvp__send {
  display: block;
  box-sizing: border-box;
  margin-top: calc(22 * var(--px)); /* 11398 - (11322 + 54) */
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

.rsvp__send:hover:enabled,
.rsvp__send:focus-visible {
  background: #9cc4d6;
  scale: 1.02;
}

.rsvp__send:disabled {
  cursor: not-allowed;
  opacity: 0.65;
}

.rsvp__error {
  margin-top: calc(6 * var(--px));
  font-family: var(--font-wish);
  font-size: calc(16 * var(--px));
  color: #a3401f;
}

@media (prefers-reduced-motion: reduce) {
  .rsvp__send {
    transition: none;
  }
}
</style>
