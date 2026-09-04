<script setup lang="ts">
import { computed } from 'vue'
import { useWedding } from '../../composables/useWedding'

const { wedding, videoUrl } = useWedding()

const src = computed(() => {
  return (videoUrl?.value as string) || (wedding.value?.video_url as string) || ''
})

const poster = computed(() => (wedding.value?.image_cover as string) || undefined)

const youtubeId = computed(() => {
  if (!src.value) return null
  const match = src.value.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&]{11})/)
  return match ? match[1] : null
})

function onVolume(e: Event) {
  const v = e.target as HTMLVideoElement
  if (!v.muted && v.volume > 0) document.querySelector('audio')?.pause()
}

function onEnded() {
  const hero = document.querySelector('.hero')
  if (!hero) return
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  hero.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' })
}
</script>

<template>
  <section v-if="src" class="video" aria-label="Video pernikahan">
    <iframe
      v-if="youtubeId"
      class="video__player"
      :src="`https://www.youtube.com/embed/${youtubeId}?autoplay=1&mute=1&loop=0&controls=1`"
      frameborder="0"
      allow="autoplay; encrypted-media"
      allowfullscreen
    ></iframe>
    <video
      v-else
      class="video__player"
      :src="src"
      :poster="poster"
      autoplay
      muted
      controls
      playsinline
      preload="auto"
      @volumechange="onVolume"
      @ended="onEnded"
    />
  </section>
</template>

<style scoped>
/*
 * svh, not vh: on mobile the toolbar makes vh taller than what is actually on screen, so
 * a 100vh band gets its bottom cropped for as long as the toolbar is showing. #1a1a1a
 * matches the desktop shell, so a portrait clip letterboxes into the same dark surround.
 */
.video {
  position: relative;
  width: 100%;
  height: 100vh;
  height: 100svh;
  background: #1a1a1a;
  z-index: 2;
}

.video__player {
  display: block;
  width: 100%;
  height: 100%;
  /* cover, so the clip fills the column edge to edge like a title card. */
  object-fit: cover;
}
</style>
