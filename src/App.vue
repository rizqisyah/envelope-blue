<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watchEffect } from 'vue'
import CoverSection from './components/cover/CoverSection.vue'
import InviteBody from './components/invite/InviteBody.vue'
import { usePreloadAssets } from './composables/usePreloadAssets'
import { useWedding } from './composables/useWedding'

const { guest, wedding, coupleNickname, quoteText, quoteVerse } = useWedding()
const { coverLoaded, preloadCover, preloadInviteBody } = usePreloadAssets()

const isOpen = ref(false)
// The column cannot scroll while the cover owns the screen, or a stray wheel event
// scrolls the invitation behind it before it has been opened.
const isLocked = ref(true)
const contentVisible = ref(false)

/*
 * Falls back to the design's own printed guest name, so an unconfigured render matches
 * the design instead of whatever wedding the default slug points at.
 */
const guestName = computed(
  () => new URLSearchParams(location.search).get('to') || guest.value?.name || 'Nama Tamu',
)
const coupleName = coupleNickname

const leftBackgroundStyle = computed(() => {
  const img = wedding.value?.image_bg1 || wedding.value?.image_cover || ''
  return img ? { backgroundImage: `url(${img})` } : {}
})

/*
 * The cover animates its layers in. Holding the reveal until they are decoded keeps a
 * real phone from assembling the scene out of half-loaded images.
 */
onMounted(async () => {
  await preloadCover()
  preloadInviteBody()
})

async function openInvitation() {
  isOpen.value = true
  /*
   * Released here, not when the cover has finished leaving. The lock's job is to stop a
   * stray wheel event scrolling the invitation while the cover still OWNS the screen —
   * once it has been tapped, it does not. Holding it through the 2.4s leave also clips
   * the sheet: `html.is-cover-locked` and `.is-locked` both set `overflow: hidden`, and
   * the cover is still in flow above the sheet, so the first band sits at ~852px in an
   * 812px viewport and is clipped out of the viewport entirely. Its IntersectionObserver
   * therefore could not fire until the cover unmounted, and the reader watched an empty
   * sheet rise to meet the receding cover — the one moment the whole opening is built
   * around. Measured: the hero revealed at ~3.0s after the tap, now at ~0.1s.
   */
  isLocked.value = false
  await nextTick()
  requestAnimationFrame(() => {
    contentVisible.value = true
  })
}

/*
 * The lock has to sit on the document, not on the column. `.is-locked` clipped the
 * column at 100vh, but iOS Safari's 100vh is the toolbar-less height — taller than what
 * is actually on screen — so the page itself still scrolled by the height of the
 * toolbar and the invitation peeked out from under the cover.
 */
watchEffect(() => {
  document.documentElement.classList.toggle('is-cover-locked', isLocked.value)
})
</script>

<template>
  <main class="app-shell">
    <!-- Desktop only: the invitation is a 430px column, this fills the rest. -->
    <div class="desktop-left-column" :style="leftBackgroundStyle">
      <div class="left-overlay"></div>
      <div class="left-content">
        <div class="left-header">
          <p class="left-subtitle">The Wedding Of</p>
          <!--
            A <p>, not an <h1>: this panel is decorative chrome that reprints the sheet's
            own title beside it, and it is display:none below 768px. The document's one
            real heading is the cover's <h1> before it is opened and the hero band's
            after — leaving an <h1> here as well would make two on desktop and, since
            this one is hidden on mobile, still none there once the cover unmounts.
          -->
          <p class="left-title">{{ coupleName }}</p>
        </div>
        <div class="left-quote-container">
          <!-- quoteText carries the design's own quotation marks — do not add a second pair. -->
          <p class="left-quote">{{ quoteText }}</p>
          <span class="left-quote-verse">{{ quoteVerse }}</span>
        </div>
      </div>
    </div>

    <div class="desktop-right-column" :class="{ 'is-locked': isLocked }">
      <Transition name="splash">
        <CoverSection
          v-if="!isOpen"
          :guest-name="guestName"
          :couple-name="coupleName"
          :ready="coverLoaded"
          @open="openInvitation"
        />
      </Transition>

      <div
        v-show="isOpen"
        id="invite"
        class="invitation-content"
        :class="{ 'is-visible': contentVisible }"
      >
        <InviteBody />
      </div>
    </div>
  </main>
</template>

<style>
/*
 * The cover pushes past the viewer rather than sliding away — it reads as walking
 * through the gate into the garden, which then rises out of the blur behind it.
 */
/*
 * Taken OUT OF FLOW for the leave. Left in flow, the cover still occupies a full screen
 * above the sheet for the whole 2.4s, so the invitation sits below the fold and only
 * snaps up when the cover unmounts — the reader sees the cover go, then an empty screen,
 * then the sheet appear at once. Out of flow, the sheet holds the screen from the tap
 * and the cover recedes over the top of it, which is the effect the timings below were
 * written for.
 */
.splash-leave-active {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  z-index: 10;
  transition:
    opacity 2.2s cubic-bezier(0.4, 0, 0.2, 1),
    transform 2.4s cubic-bezier(0.16, 1, 0.3, 1),
    filter 2.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  will-change: opacity, transform, filter;
}

.splash-leave-to {
  opacity: 0 !important;
  transform: scale(1.16) !important;
  filter: blur(14px) !important;
}

/* Held back 0.8s so the cover has visibly receded before this rises to meet it. */
.invitation-content {
  opacity: 0;
  transform: translateY(28px) scale(0.965);
  filter: blur(10px);
  transition:
    opacity 2.3s cubic-bezier(0.16, 1, 0.3, 1) 0.8s,
    transform 2.7s cubic-bezier(0.16, 1, 0.3, 1) 0.8s,
    filter 2.3s cubic-bezier(0.16, 1, 0.3, 1) 0.8s;
  will-change: opacity, transform, filter;
}

.invitation-content.is-visible {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}

@media (prefers-reduced-motion: reduce) {
  .splash-leave-active,
  .invitation-content {
    transition: opacity 0.2s linear !important;
  }

  .splash-leave-to {
    transform: none !important;
    filter: none !important;
  }

  .invitation-content {
    transform: none;
    filter: none;
  }
}

@media (min-width: 768px) {
  .app-shell {
    display: flex;
    flex-direction: row;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    background: #1a1a1a;
  }

  .desktop-left-column {
    display: flex;
    flex: 1;
    height: 100vh;
    position: relative;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
    background-color: var(--bg-body);
    color: #fff;
    overflow: hidden;
  }

  .left-overlay {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 1;
  }

  .left-content {
    position: relative;
    z-index: 2;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    width: 100%;
    padding: 60px;
  }

  .left-subtitle {
    margin-bottom: 16px;
    font-family: var(--font-script);
    font-size: 20px;
    letter-spacing: 0.06em;
    opacity: 0.9;
  }

  .left-title {
    margin: 0;
    font-family: var(--font-display);
    font-size: 56px;
    font-weight: 400;
    line-height: 1.15;
    letter-spacing: -0.04em;
    color: #f0d9a8;
  }

  .left-quote-container {
    max-width: 480px;
    margin-top: auto;
    margin-bottom: 40px;
  }

  .left-quote {
    margin-bottom: 12px;
    font-family: var(--font-serif);
    font-size: 15px;
    font-style: italic;
    line-height: 1.6;
    opacity: 0.9;
  }

  .left-quote-verse {
    font-family: var(--font-sans);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    opacity: 0.8;
  }

  /* Exactly --card-max: the sheet fills it, so the art has no gutter beside it. */
  .desktop-right-column {
    width: var(--card-max);
    height: 100vh;
    overflow-x: hidden;
    overflow-y: auto;
    position: relative;
    background: var(--paper);
    box-shadow: -8px 0 32px rgba(0, 0, 0, 0.3);
  }

  .desktop-right-column.is-locked {
    overflow: hidden !important;
  }
}

@media (max-width: 767px) {
  .app-shell {
    width: 100%;
    overflow-x: hidden;
  }

  .desktop-left-column {
    display: none;
  }

  .desktop-right-column {
    position: relative; /* containing block for the cover's out-of-flow leave */
    width: 100%;
    overflow-x: hidden;
  }

  .desktop-right-column.is-locked {
    overflow: hidden !important;
    height: 100dvh;
  }
}
</style>
