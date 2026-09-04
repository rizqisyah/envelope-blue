<script setup lang="ts">
/*
 * Frame 1 (1:3) band "closing": y 11452..12818 of the body frame — the last one. A toile
 * backdrop, the thank-you, a framed photo and the credit line. Art comes from
 * src/lib/bands/closing.ts (GENERATED, scripts/gen_band.py).
 */
import { computed } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/closing'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'

const { el, shown } = useReveal(0.15)
const { closingTitle, closingMessage, closingSignature, customSpousePhoto } = useWedding()

const skipClosingLayers = computed(() => (customSpousePhoto.value ? ['40:82', '40:84'] : []))

// Parse closing message: if it starts with a title line (e.g. "Thank You !", "Terima Kasih !") or has closingTitle
const parsedClosing = computed(() => {
  if (closingTitle.value && closingTitle.value.trim()) {
    return {
      title: closingTitle.value.trim(),
      body: closingMessage.value.trim(),
    }
  }

  const raw = closingMessage.value.trim()
  const lines = raw.split('\n')
  // If first line is a short title-like line (e.g. "Thank You !", "Terima Kasih !")
  if (lines.length > 1 && lines[0].trim().length > 0 && lines[0].trim().length <= 35) {
    const title = lines[0].trim()
    let bodyStartIndex = 1
    while (bodyStartIndex < lines.length && !lines[bodyStartIndex].trim()) {
      bodyStartIndex++
    }
    const body = lines.slice(bodyStartIndex).join('\n').trim()
    return { title, body }
  }

  return { title: '', body: raw }
})
</script>

<template>
  <section
    :ref="el"
    class="band closing"
    :class="{ 'is-in': shown }"
    aria-labelledby="closing-title"
  >
    <BandArt :layers="LAYERS" :skip="skipClosingLayers" :shown="shown" />

    <!-- Dynamic closing content container -->
    <div class="closing__body" :class="{ 'has-no-title': !parsedClosing.title }">
      <!-- 99:7 — the sign-off / title -->
      <h2 v-if="parsedClosing.title" id="closing-title" class="closing__title">
        {{ parsedClosing.title }}
      </h2>

      <!-- 41:92 — the message -->
      <p v-if="parsedClosing.body" class="closing__message">
        {{ parsedClosing.body }}
      </p>

      <!-- 42:3 — the signature (nama undangan) -->
      <p class="closing__signature">{{ closingSignature }}</p>
    </div>

    <!-- Custom Spouse Photo (Gambar 2: spouse-image url) -->
    <div
      v-if="customSpousePhoto"
      class="closing__photo-wrapper"
      :class="{ 'is-in': shown }"
    >
      <img
        class="closing__photo"
        :src="customSpousePhoto"
        alt="Foto Pasangan"
        loading="lazy"
        decoding="async"
      />
    </div>

    <!-- 45:8 — the maker's credit, at the very foot of the sheet. -->
    <p class="closing__credit">Created by 25ribuaja x Qinvi</p>
  </section>
</template>

<style scoped>
.closing {
  height: calc(v-bind(BAND_HEIGHT) * var(--px));
}

/*
 * Dynamic flow container for title, message and signature. Positioned at 99:7's origin.
 */
.closing__body {
  --delay: 120ms;
  z-index: 260;
  top: calc(116 * var(--px)); /* 99:7 box y 11563 + 5 */
  left: calc(55.05 * var(--px));
  width: calc(486 * var(--px));
  text-align: center;
}

.closing__body.has-no-title {
  top: calc(165 * var(--px));
}

/* 99:7 — Roben Elegante Script 40, #aa7a3a. Figma declares no line-height; the box's 61. */
.closing__title {
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(40 * var(--px));
  line-height: calc(61 * var(--px));
  color: #aa7a3a;
  text-align: center;
  margin: 0 0 calc(24 * var(--px)) 0;
}

.closing__message {
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(36 * var(--px));
  white-space: pre-line;
  color: #aa7a3a;
  margin: 0;
  text-align: center;
}

.closing__signature {
  margin-top: calc(18 * var(--px));
  font-family: var(--font-comtic);
  font-weight: 400;
  font-size: calc(24 * var(--px));
  line-height: calc(38 * var(--px));
  color: #aa7a3a;
  text-align: center;
}

/*
 * Custom Spouse Photo (Gambar 2):
 * Placed in front of white paper card 40:81 (z: 256), behind bottom wax seal 40:86 (z: 259).
 * Size 205 x 347 at (206, 532).
 */
.closing__photo-wrapper {
  position: absolute;
  z-index: 258;
  top: calc(532 * var(--px));
  left: calc(206 * var(--px));
  width: calc(205 * var(--px));
  height: calc(347 * var(--px));
  border-radius: calc(6 * var(--px));
  overflow: hidden;
  box-shadow: 0 calc(4 * var(--px)) calc(12 * var(--px)) rgba(0, 0, 0, 0.08);
  visibility: hidden;
  will-change: transform, opacity;
  pointer-events: none;
}

.closing__photo-wrapper.is-in {
  visibility: visible;
  animation: closing-photo-in 2700ms cubic-bezier(0.16, 1, 0.28, 1) backwards;
  animation-delay: 590ms;
}

.closing__photo {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top;
}

@keyframes closing-photo-in {
  from {
    opacity: 0;
    transform: translate3d(0, calc(44 * var(--px)), 0) scale(0.86);
  }
  to {
    opacity: 1;
    transform: none;
  }
}

/* 45:8 — Roben Elegante Script 20, #aa7a3a. The box's own 56 for line-height. */
.closing__credit {
  --delay: 440ms;
  z-index: 290;
  top: calc(1317 * var(--px)); /* 45:8 box y 12779 - 10 — Roben Elegante at 20/56 */
  left: calc(55.05 * var(--px));
  width: calc(486 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(56 * var(--px));
  color: #aa7a3a;
  text-align: center;
}
</style>
