<script setup lang="ts">
// The invitation sheet. One component per band of the body frame, in Figma order;
// each band positions its own children relative to its own top, so inserting a band
// never renumbers the others. Band map and asset inventory: ../../../SLICING.md
//
// No bands sliced yet — import them from ../sections/ and list them in the template.
</script>

<template>
  <div class="sheet">
    <p class="sheet__empty">No bands sliced yet.</p>
  </div>
</template>

<style scoped>
/*
 * One design pixel = 1cqw / 3.75, the same unit CoverSection uses. Declared once here
 * so every band inherits it and can place children in raw Figma coordinates.
 */
.sheet {
  container-type: inline-size;
  position: relative;
  width: 100%;
  overflow: hidden;
  background: var(--paper);
}

.sheet > * {
  --px: 0.26667cqw;
}

.sheet__empty {
  padding: 80px 24px;
  font-family: var(--font-sans);
  text-align: center;
  opacity: 0.5;
}
</style>
