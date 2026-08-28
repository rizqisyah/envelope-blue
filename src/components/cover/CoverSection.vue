<script setup lang="ts">
/*
 * Placeholder cover. Frame <cover> has not been sliced yet — replace the markup below
 * with the sliced plates (see SLICING.md). The props and the `open` event are the
 * contract App.vue depends on; keep them.
 */
defineProps<{
  guestName: string
  coupleName: string
  ready: boolean
}>()

defineEmits<{ open: [] }>()
</script>

<template>
  <div class="cover">
    <p class="cover__eyebrow">The Wedding Of</p>
    <h1 class="cover__name">{{ coupleName }}</h1>
    <p class="cover__guest">{{ guestName }}</p>
    <button class="cover__open" type="button" :disabled="!ready" @click="$emit('open')">
      Click to open
    </button>
  </div>
</template>

<style scoped>
.cover {
  container-type: inline-size;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  min-height: 100vh;
  padding: 32px;
  background: var(--paper);
  text-align: center;
}

.cover__eyebrow {
  font-family: var(--font-script);
  font-size: 20px;
}

.cover__name {
  font-family: var(--font-display);
  font-size: 44px;
  font-weight: 400;
}

.cover__guest {
  font-family: var(--font-serif);
  font-style: italic;
}

.cover__open {
  margin-top: 20px;
  padding: 10px 22px;
  border: 1px solid currentColor;
  border-radius: 999px;
  background: none;
  font-family: var(--font-sans);
  font-size: 13px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  cursor: pointer;
}

.cover__open:disabled {
  opacity: 0.4;
  cursor: default;
}
</style>
