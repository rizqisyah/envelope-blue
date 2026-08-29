<script setup lang="ts">
import type { BandLayer } from '../../lib/bandLayer'

const props = withDefaults(
  defineProps<{
    layers: BandLayer[]
    /** Layer ids this band draws itself — an API photo standing in for a sliced plate. */
    skip?: string[]
    /** Whether the band has scrolled into view; layers hold still until it has. */
    shown?: boolean
    /** Stagger between layers, back to front. */
    step?: number
  }>(),
  { skip: () => [], shown: true, step: 150 },
)

const FRAME_W = 596 // the body frame's own width — see SLICING.md

/*
 * Each layer gets its own entrance, derived from where it sits and how big it is,
 * so the band assembles like a set being built rather than a picture fading up.
 *
 *   - full-bleed backdrops swell in from behind, slowest and first
 *   - anything hugging a side edge sweeps in from off that edge, rotating as it lands
 *   - small foreground props drop in late, overshooting slightly before settling
 *
 * All of it is transform + opacity, so it stays on the compositor.
 */
const styleFor = (l: BandLayer, i: number): Record<string, string> => ({
  zIndex: String(l.z),
  left: `calc(${l.x} * var(--px))`,
  top: `calc(${l.y} * var(--px))`,
  width: `calc(${l.w} * var(--px))`,
  height: `calc(${l.h} * var(--px))`,
  /*
   * Figma's MCP reports neither `opacity` nor `blendMode`, so both are solved off the
   * render by scripts/solve_alpha.py and carried on the layer. Absent means the layer
   * paints at full strength, stacked normally.
   *
   * The opacity goes through a custom property rather than straight onto `opacity`,
   * because the entrance animation also drives opacity — its `to` frame has to land on
   * the layer's own value or a faded plate would flash to full strength as it arrives.
   */
  '--a': String(l.a ?? 1),
  mixBlendMode: l.b ?? 'normal',
  ...entrance(l, i),
})

const entrance = (l: BandLayer, i: number) => {
  const isBackdrop = l.w >= FRAME_W * 0.9 && l.h > 200
  const centre = l.x + l.w / 2
  const offLeft = centre < FRAME_W * 0.34
  const offRight = centre > FRAME_W * 0.66
  const small = l.w < 130 && l.h < 180

  let tx = 0
  let ty = 44
  let rot = 0
  let scale = 0.86

  if (isBackdrop) {
    ty = 26
    scale = 1.08 // settles inward, so the scene opens up rather than rising
  } else if (offLeft || offRight) {
    const dir = offLeft ? -1 : 1
    tx = dir * 92
    ty = 30
    rot = dir * 7
    scale = 0.92
  } else if (small) {
    ty = -34 // drops in from above
    rot = (i % 2 ? 1 : -1) * 9
    scale = 0.7
  }

  return {
    '--tx': `${tx}`,
    '--ty': `${ty}`,
    '--rot': `${rot}deg`,
    '--scale': `${scale}`,
    '--dur': isBackdrop ? '3400ms' : small ? '2100ms' : '2700ms',
    // Backdrops lead; everything in front of them queues up behind, front-most last.
    animationDelay: `${Math.round((isBackdrop ? 0 : 440) + i * stagger())}ms`,
  }
}

const visible = () => props.layers.filter((l) => !props.skip.includes(l.id))

/*
 * Groom is 36 layers. At a flat 150ms step its last layer would start 5.2s in and the
 * band would still be assembling 8s after it came into view, long after the reader has
 * scrolled past. Cap the total stagger instead of the per-layer step, so short bands
 * get the full leisurely spacing and long ones tighten up to fit the same window.
 */
const MAX_STAGGER = 2600
const stagger = () => Math.min(props.step, MAX_STAGGER / Math.max(1, visible().length - 1))
</script>

<template>
  <img
    v-for="(layer, i) in visible()"
    :key="layer.id"
    class="band-art"
    :class="{ 'is-in': shown }"
    :src="layer.src"
    alt=""
    :width="layer.w"
    :height="layer.h"
    loading="lazy"
    decoding="async"
    :style="styleFor(layer, i)"
  />
</template>

<style scoped>
/*
 * Held in the start state by `visibility` rather than a paused animation: the
 * animation only exists once `.is-in` lands, so nothing has to be un-paused and
 * the element still fetches its image while hidden.
 */
.band-art {
  position: absolute;
  max-width: none; /* several layers are authored wider than the frame */
  visibility: hidden;
  opacity: var(--a, 1);
  will-change: transform, opacity;
}

.band-art.is-in {
  visibility: visible;
  animation: layer-in var(--dur, 2700ms) cubic-bezier(0.16, 1, 0.28, 1) backwards;
}

@keyframes layer-in {
  from {
    opacity: 0;
    transform: translate3d(calc(var(--tx) * var(--px)), calc(var(--ty) * var(--px)), 0)
      rotate(var(--rot)) scale(var(--scale));
  }
  to {
    opacity: var(--a, 1);
    transform: none;
  }
}

/*
 * Motion this large is exactly what a vestibular disorder cannot tolerate, so the
 * reduced-motion path is not a shortened version of it — it is no movement at all.
 */
@media (prefers-reduced-motion: reduce) {
  .band-art,
  .band-art.is-in {
    visibility: visible;
    animation: none;
    will-change: auto;
  }
}
</style>
