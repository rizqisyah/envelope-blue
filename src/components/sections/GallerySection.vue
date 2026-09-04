<script setup lang="ts">
/*
 * Frame 1 (1:3) band "gallery": y 7750..8865 of the body frame. An oval carousel with
 * two arrows, a row of three thumbnails, and the promo card at the foot. Art comes from
 * src/lib/bands/gallery.ts (GENERATED, scripts/gen_band.py).
 *
 * The band's four photos are MASKED, and Figma exports a masked node already clipped:
 * 31:289 declares 403.6x504.6 and exports 308x403, which is exactly its mask 31:288's
 * box. So the mask's box is the photo's position, and the mask nodes themselves paint
 * nothing — all six of the band's ELLIPSEs are in build_refs.py's CSS_SHAPES, four as
 * masks and two as the arrow buttons, which are solid #d9d9d9 (sampled opaque off the
 * render, not translucent).
 *
 * The photos are drawn here rather than by BandArt so live gallery rows can replace them.
 * A live photo is rectangular, so its oval comes from the container's border-radius; the
 * design's own exports are already oval and the radius is a no-op over them.
 */
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import BandArt from '../invite/BandArt.vue'
import { BAND_HEIGHT, LAYERS } from '../../lib/bands/gallery'
import { useReveal } from '../../composables/useReveal'
import { useWedding } from '../../composables/useWedding'
import { assets } from '../../lib/bandAssets'
import { DESIGN_MODE } from '../../lib/api'

const { el, shown } = useReveal(0.15)
const { gallery, videoPrewed, wedding } = useWedding()

// Drawn below instead of pasted: the four photos, the two chevrons (which sit on
// real buttons), and the promo card 31:318 which is never drawn as Figma promo placeholder.
const DRAWN = ['31:289', '31:295', '31:301', '31:304', '31:314', '31:315', '31:318']

const chevronLeft = assets['gallery/parts/31-314.webp']
const chevronRight = assets['gallery/parts/31-315.webp']

/*
 * `image_url` / `caption` are the field names template 5's gallery settled on. With no
 * live gallery the design's own four exports stand in, so an unconfigured render matches
 * the frame and the carousel still works.
 */
const DESIGN_PHOTOS = [
  { src: assets['gallery/parts/31-289.webp'], caption: '' },
  { src: assets['gallery/parts/31-295.webp'], caption: '' },
  { src: assets['gallery/parts/31-301.webp'], caption: '' },
  { src: assets['gallery/parts/31-304.webp'], caption: '' },
]

const photos = computed(() => {
  const live = ((gallery.value as any[]) || [])
    .map((g) => ({ src: g?.image_url as string, caption: (g?.caption as string) || '' }))
    .filter((p) => p.src && String(p.src).trim() !== '')
  if (live.length) return live
  if (DESIGN_MODE && !wedding.value) return DESIGN_PHOTOS
  return []
})

const active = ref(0)
watch(photos, () => (active.value = 0))

const step = (d: number) => {
  const n = photos.value.length
  if (n) active.value = (active.value + d + n) % n
}

/*
 * The thumbnail row is a window that FOLLOWS the active photo — the three after it,
 * wrapping. A fixed first-three row would leave photo 8 of 10 unreachable by tap; this
 * way the arrows and the thumbnails both reach everything, and with the design's own
 * four the row shows exactly the three the render shows.
 */
const THUMBS = [
  { id: '31:295', x: 146 },
  { id: '31:301', x: 255 },
  { id: '31:304', x: 364 },
]
const thumbs = computed(() =>
  THUMBS.map((t, i) => {
    const n = photos.value.length
    const at = n ? (active.value + i + 1) % n : 0
    return { ...t, at, photo: photos.value[at] }
  }),
)

// 31:307 / 31:308 — 48x57 at y 8246, band-local 496.
const BUTTONS = [
  { id: '31:307', x: 128, z: 186, chev: chevronLeft, chevX: 12, dir: -1, label: 'Foto sebelumnya' },
  { id: '31:308', x: 436, z: 187, chev: chevronRight, chevX: 21, dir: 1, label: 'Foto berikutnya' },
]

// --- Auto-Slide (Auto Geser) for Thumbnails & Photos ---
let autoTimer: ReturnType<typeof setInterval> | null = null
const isHovered = ref(false)
const isInteracting = ref(false)

function startAutoSlide() {
  stopAutoSlide()
  if (photos.value.length > 1) {
    autoTimer = setInterval(() => {
      if (!isHovered.value && !isInteracting.value && !zoomed.value) {
        step(1)
      }
    }, 3500)
  }
}

function stopAutoSlide() {
  if (autoTimer) {
    clearInterval(autoTimer)
    autoTimer = null
  }
}

// --- Touch Swipe & Drag Gestures (Geser-geser) ---
let touchStartX = 0
let touchStartY = 0
const isDragging = ref(false)

function onTouchStart(e: TouchEvent) {
  touchStartX = e.touches[0].clientX
  touchStartY = e.touches[0].clientY
  isInteracting.value = true
  stopAutoSlide()
}

function onTouchEnd(e: TouchEvent) {
  const touchEndX = e.changedTouches[0].clientX
  const touchEndY = e.changedTouches[0].clientY
  const dx = touchEndX - touchStartX
  const dy = touchEndY - touchStartY
  isInteracting.value = false

  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 35) {
    if (dx < 0) step(1)
    else step(-1)
  }
  startAutoSlide()
}

function onPointerDown(e: PointerEvent) {
  touchStartX = e.clientX
  touchStartY = e.clientY
  isDragging.value = true
  isInteracting.value = true
  stopAutoSlide()
}

function onPointerUp(e: PointerEvent) {
  if (!isDragging.value) return
  const dx = e.clientX - touchStartX
  isDragging.value = false
  isInteracting.value = false

  if (Math.abs(dx) > 35) {
    if (dx < 0) step(1)
    else step(-1)
  }
  startAutoSlide()
}

// --- Click to Zoom (Fullscreen Lightbox Modal) ---
const zoomed = ref(false)

function openZoom(index?: number) {
  if (typeof index === 'number') active.value = index
  zoomed.value = true
  stopAutoSlide()
}

function closeZoom() {
  zoomed.value = false
  startAutoSlide()
}

function onKey(e: KeyboardEvent) {
  if (!zoomed.value) return
  if (e.key === 'Escape') closeZoom()
  else if (e.key === 'ArrowLeft') step(-1)
  else if (e.key === 'ArrowRight') step(1)
}

watch(zoomed, (open) => {
  if (typeof document !== 'undefined') {
    document.body.style.overflow = open ? 'hidden' : ''
  }
  if (open) window.addEventListener('keydown', onKey)
  else window.removeEventListener('keydown', onKey)
})

onMounted(() => {
  startAutoSlide()
})

onUnmounted(() => {
  stopAutoSlide()
  if (typeof window !== 'undefined') {
    window.removeEventListener('keydown', onKey)
    document.body.style.overflow = ''
  }
})

// --- Prewedding Video (YouTube / MP4) ---
const hasVideo = computed(() => {
  const v = videoPrewed.value
  return typeof v === 'string' && v.trim().length > 0
})

const youtubeId = computed(() => {
  if (!hasVideo.value) return null
  const match = videoPrewed.value.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&]{11})/)
  return match ? match[1] : null
})

// Dynamically adjust section height: eliminate empty gap if prewed video is absent
const bandHeight = computed(() => {
  // If video is present AND photos are present: original Figma height 1115
  if (hasVideo.value && photos.value.length > 0) {
    return BAND_HEIGHT
  }
  // If video only (no photos): compact height for video
  if (hasVideo.value && photos.value.length === 0) {
    return 750
  }
  // If photos only (no video): tidy up the bottom, eliminating the ~175px empty slot
  if (photos.value.length > 0 && !hasVideo.value) {
    return 940
  }
  return BAND_HEIGHT
})

// Dynamically position bottom pearl necklace layer 31:309 to gracefully frame the 3 thumbnails
const dynamicLayers = computed(() => {
  return LAYERS.map((layer) => {
    // When there is no video prewed, shift the bottom pearl necklace (31:309)
    // up to cleanly underline and frame the 3 thumbnails (y: 820)
    if (layer.id === '31:309' && !hasVideo.value && photos.value.length > 0) {
      return { ...layer, y: 820 }
    }
    // If video-only, shift 31:309 under the video
    if (layer.id === '31:309' && hasVideo.value && photos.value.length === 0) {
      return { ...layer, y: 640 }
    }
    return layer
  })
})

const skipLayers = computed(() => {
  const base = [...DRAWN]
  // If there are no photos, also skip layer '31:287' (the photo oval background halo)
  if (photos.value.length === 0) {
    base.push('31:287')
  }
  return base
})
</script>

<template>
  <section
    :ref="el"
    class="band gallery"
    :class="{ 'is-in': shown, 'gallery--video-only': photos.length === 0 && hasVideo }"
    aria-labelledby="gallery-title"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <BandArt :layers="dynamicLayers" :skip="skipLayers" :shown="shown" />

    <!-- z-index is each node's GLOBAL Figma child order (see HeroSection for the rule). -->

    <!-- Photo Memories carousel (rendered only when there are gallery photos) -->
    <template v-if="photos.length > 0">
      <!-- 31:284 / 31:317 — the heading and its line. -->
      <h2 id="gallery-title" class="gallery__title">Our Dearest Memories</h2>
      <p class="gallery__lede">Scenes from a love story we shall cherish evermore.</p>

      <!-- 31:288 + 31:289 — the oval photo, clickable to zoom and swipeable. -->
      <div
        class="gallery__oval"
        role="button"
        tabindex="0"
        :aria-label="`Perbesar foto ${active + 1}`"
        @click="openZoom()"
        @touchstart.passive="onTouchStart"
        @touchend="onTouchEnd"
        @pointerdown="onPointerDown"
        @pointerup="onPointerUp"
      >
        <img
          v-if="photos[active]"
          :src="photos[active].src"
          :alt="photos[active].caption || 'Foto pasangan'"
          loading="lazy"
          decoding="async"
        />
        <span class="gallery__zoom-hint" aria-hidden="true" title="Klik untuk memperbesar">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            <line x1="11" y1="8" x2="11" y2="14"></line>
            <line x1="8" y1="11" x2="14" y2="11"></line>
          </svg>
        </span>
      </div>

      <!-- 31:307 / 31:308 + their chevrons — real buttons, so the arrows work. -->
      <button
        v-for="b in BUTTONS"
        :key="b.id"
        type="button"
        class="gallery__nav"
        :style="{ zIndex: b.z, left: `calc(${b.x} * var(--px))` }"
        :aria-label="b.label"
        @click="step(b.dir); startAutoSlide()"
      >
        <img :src="b.chev" alt="" :style="{ left: `calc(${b.chevX} * var(--px))` }" />
      </button>

      <!-- 31:310 — the thumbnail row's heading. -->
      <p class="gallery__strip-title">Portraits of Affection</p>

      <!-- 31:294 / 31:300 / 31:303 + their photos — the strip, live, auto-sliding with active photo. -->
      <button
        v-for="t in thumbs"
        :key="t.id"
        type="button"
        class="gallery__thumb"
        :style="{ left: `calc(${t.x} * var(--px))` }"
        :aria-label="`Lihat foto ${t.at + 1}`"
        @click="active = t.at; startAutoSlide()"
      >
        <img
          v-if="t.photo"
          :src="t.photo.src"
          :alt="t.photo.caption || ''"
          loading="lazy"
          decoding="async"
        />
      </button>
    </template>

    <!-- If photos are empty but video exists, show heading for prewedding video -->
    <template v-if="photos.length === 0 && hasVideo">
      <h2 id="gallery-title" class="gallery__title gallery__title--video-only">Prewedding Moments</h2>
      <p class="gallery__lede gallery__lede--video-only">Scenes from a love story we shall cherish evermore.</p>
    </template>

    <!-- Prewedding Video Player: ONLY rendered when videoPrewed is present and non-empty -->
    <div
      v-if="hasVideo"
      class="gallery__video-box"
      :class="{ 'gallery__video-box--video-only': photos.length === 0 }"
    >
      <iframe
        v-if="youtubeId"
        :src="`https://www.youtube.com/embed/${youtubeId}?rel=0`"
        title="Prewedding Video"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        class="gallery__video-frame"
      ></iframe>
      <video
        v-else
        :src="videoPrewed"
        controls
        playsinline
        class="gallery__video-frame"
      ></video>
    </div>

    <!-- Fullscreen Lightbox Modal -->
    <Teleport to="body">
      <Transition name="lb">
        <div
          v-if="zoomed && photos.length > 0"
          class="gallery__lightbox"
          role="dialog"
          aria-modal="true"
          @click.self="closeZoom"
          @touchstart="onTouchStart"
          @touchend="onTouchEnd"
        >
          <button
            type="button"
            class="gallery__lb-btn gallery__lb-close"
            aria-label="Tutup foto"
            @click="closeZoom"
          >
            ✕
          </button>
          <button
            type="button"
            class="gallery__lb-btn gallery__lb-prev"
            aria-label="Foto sebelumnya"
            @click="step(-1)"
          >
            ‹
          </button>
          <div class="gallery__lb-body" @click.self="closeZoom">
            <img
              v-if="photos[active]"
              :src="photos[active].src"
              :alt="photos[active].caption || `Foto galeri ${active + 1}`"
              class="gallery__lb-img"
            />
            <p v-if="photos[active]?.caption" class="gallery__lb-caption">
              {{ photos[active].caption }}
            </p>
          </div>
          <button
            type="button"
            class="gallery__lb-btn gallery__lb-next"
            aria-label="Foto berikutnya"
            @click="step(1)"
          >
            ›
          </button>
          <div class="gallery__lb-count">
            {{ active + 1 }} / {{ photos.length }}
          </div>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<style scoped>
.gallery {
  height: calc(v-bind(bandHeight) * var(--px));
  transition: height 300ms ease;
}

/* 31:284 — Roben Elegante Script 32, #aa7a3a, centred. Box's own 57 for line-height. */
.gallery__title {
  --delay: 80ms;
  z-index: 225;
  top: calc(184 * var(--px)); /* 31:284 box y 7934, band-local 184 */
  left: calc(106.05 * var(--px));
  width: calc(383 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(32 * var(--px));
  line-height: calc(57 * var(--px));
  color: #aa7a3a;
}

/* 31:317 — Roben Elegante Script 20/24, #aa7a3a, LEFT aligned and wrapped by its box. */
.gallery__lede {
  --delay: 180ms;
  z-index: 229;
  top: calc(255 * var(--px)); /* 31:317 box y 8005, band-local 255 */
  left: calc(51 * var(--px));
  width: calc(208 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(20 * var(--px));
  line-height: calc(24 * var(--px));
  text-align: left;
  color: #aa7a3a;
}

/* 31:288's box, 308x403 at y 8062. The photo fills it and the radius cuts the oval. */
.gallery__oval {
  --delay: 300ms;
  z-index: 179;
  top: calc(312 * var(--px)); /* 31:288 box y 8062, band-local 312 */
  left: calc(152 * var(--px));
  width: calc(308 * var(--px));
  height: calc(403 * var(--px));
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  touch-action: pan-y;
  user-select: none;
}

.gallery__zoom-hint {
  position: absolute;
  bottom: calc(20 * var(--px));
  right: calc(20 * var(--px));
  width: calc(36 * var(--px));
  height: calc(36 * var(--px));
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(4px);
  color: #aa7a3a;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.85;
  pointer-events: none;
  transition: opacity 200ms ease, transform 200ms ease;
  box-shadow: 0 calc(2 * var(--px)) calc(6 * var(--px)) rgba(0, 0, 0, 0.15);
}

.gallery__oval:hover .gallery__zoom-hint {
  opacity: 1;
  transform: scale(1.1);
}

.gallery__oval img,
.gallery__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 31:307 / 31:308 — 48x57, solid #d9d9d9, opaque. */
.gallery__nav {
  --delay: 420ms;
  top: calc(496 * var(--px)); /* 31:307 box y 8246, band-local 496 */
  width: calc(48 * var(--px));
  height: calc(57 * var(--px));
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: #d9d9d9;
  cursor: pointer;
  /* `scale`, not a transform: the band's reveal owns `transform` and would win. */
  transition: background 240ms ease, scale 240ms ease;
}

.gallery__nav img {
  position: absolute;
  top: calc(16 * var(--px)); /* 31:314 / 31:315 y 8262 against the button's 8246 */
  width: calc(13.5 * var(--px));
  height: calc(25.5 * var(--px));
}

.gallery__nav:hover,
.gallery__nav:focus-visible {
  background: #ececeb;
  scale: 1.08;
}

/* 31:310 — Roben Elegante Script 24/34, #aa7a3a, centred. */
.gallery__strip-title {
  --delay: 520ms;
  z-index: 228;
  top: calc(652 * var(--px)); /* 31:310 box y 8402, band-local 652 */
  left: calc(405.05 * var(--px));
  width: calc(195 * var(--px));
  font-family: var(--font-display);
  font-weight: 400;
  font-size: calc(24 * var(--px));
  line-height: calc(34 * var(--px));
  color: #aa7a3a;
}

/* 31:294 / 31:300 / 31:303 — 102x119 at y 8478, band-local 728. */
.gallery__thumb {
  --delay: 620ms;
  z-index: 181;
  top: calc(728 * var(--px));
  width: calc(102 * var(--px));
  height: calc(119 * var(--px));
  padding: 0;
  border: 0;
  border-radius: 50%;
  overflow: hidden;
  background: none;
  cursor: pointer;
  transition: scale 240ms ease;
}

.gallery__thumb:hover,
.gallery__thumb:focus-visible {
  scale: 1.05;
}

/* Video Box inside Frame at slot 31:318 */
.gallery__video-box {
  position: absolute;
  z-index: 195;
  top: calc(901 * var(--px));
  left: calc(112 * var(--px));
  width: calc(388 * var(--px));
  height: calc(213 * var(--px));
  border-radius: calc(14 * var(--px));
  overflow: hidden;
  box-shadow: 0 calc(6 * var(--px)) calc(20 * var(--px)) rgba(0, 0, 0, 0.18);
  background: #000;
  transition: top 300ms ease, width 300ms ease, height 300ms ease;
}

/* Video-only mode layout when there are no gallery photos */
.gallery__title--video-only {
  top: calc(240 * var(--px));
  left: 0;
  width: 100%;
  text-align: center;
}

.gallery__lede--video-only {
  top: calc(315 * var(--px));
  left: 0;
  width: 100%;
  text-align: center;
}

.gallery__video-box--video-only {
  top: calc(390 * var(--px));
  left: calc(88 * var(--px));
  width: calc(420 * var(--px));
  height: calc(236 * var(--px));
  box-shadow: 0 calc(10 * var(--px)) calc(30 * var(--px)) rgba(0, 0, 0, 0.22);
}

.gallery__video-frame {
  width: 100%;
  height: 100%;
  border: 0;
  display: block;
}

/* ===== Fullscreen Lightbox ===== */
.gallery__lightbox {
  position: fixed;
  inset: 0;
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(15, 23, 42, 0.94);
  backdrop-filter: blur(8px);
  cursor: zoom-out;
  touch-action: pan-y;
}

.gallery__lb-body {
  position: relative;
  max-width: 92vw;
  max-height: 86vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.gallery__lb-img {
  max-width: min(92vw, 840px);
  max-height: 80vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.6);
  animation: lbPop 280ms cubic-bezier(0.16, 1, 0.3, 1) both;
  cursor: default;
}

.gallery__lb-caption {
  margin-top: 14px;
  color: #f1f5f9;
  font-family: var(--font-body, serif);
  font-size: 1rem;
  text-align: center;
}

.gallery__lb-btn {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  color: #ffffff;
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
  transition: background 180ms ease, transform 180ms ease;
  z-index: 100000;
}

.gallery__lb-btn:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: scale(1.1);
}

.gallery__lb-btn:active {
  transform: scale(0.95);
}

.gallery__lb-close {
  top: 24px;
  right: 24px;
  font-size: 20px;
}

.gallery__lb-prev {
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
}

.gallery__lb-prev:hover {
  transform: translateY(-50%) scale(1.1);
}

.gallery__lb-next {
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
}

.gallery__lb-next:hover {
  transform: translateY(-50%) scale(1.1);
}

.gallery__lb-count {
  position: absolute;
  bottom: 24px;
  left: 0;
  right: 0;
  text-align: center;
  color: rgba(255, 255, 255, 0.75);
  font-family: monospace;
  font-size: 14px;
  letter-spacing: 1.5px;
}

@keyframes lbPop {
  from {
    opacity: 0;
    transform: scale(0.94);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.lb-enter-active,
.lb-leave-active {
  transition: opacity 220ms ease;
}

.lb-enter-from,
.lb-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .gallery__nav,
  .gallery__thumb {
    transition: none;
  }
  .gallery__lb-img {
    animation: none;
  }
}
</style>
