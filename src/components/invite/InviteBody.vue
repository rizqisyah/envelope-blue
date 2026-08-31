<script setup lang="ts">
// The invitation sheet. One component per band of the body frame, in Figma order;
// each band positions its own children relative to its own top, so inserting a band
// never renumbers the others. Band map and asset inventory: ../../../SLICING.md
//
// Sliced so far: hero (y 0..1108), countdown (y 1108..1802), bismillah (y 1802..2161),
// bride (y 2161..3163), groom (y 3163..4021), quote (y 4021..4425), akad (y 4425..5907).
// The rest of Frame 1 is still to cut — add each band's component here in Figma order
// as it lands.
import HeroSection from '../sections/HeroSection.vue'
import CountdownSection from '../sections/CountdownSection.vue'
import BismillahSection from '../sections/BismillahSection.vue'
import BrideSection from '../sections/BrideSection.vue'
import GroomSection from '../sections/GroomSection.vue'
import QuoteSection from '../sections/QuoteSection.vue'
import AkadSection from '../sections/AkadSection.vue'
</script>

<template>
  <div class="sheet">
    <HeroSection />
    <CountdownSection />
    <BismillahSection />
    <BrideSection />
    <GroomSection />
    <QuoteSection />
    <AkadSection />
  </div>
</template>

<style scoped>
/*
 * One design pixel = 100cqw / 596, the same unit CoverSection uses. This frame is 596
 * wide, NOT the 375 of templates 2-5 — every coordinate in every band table is in that
 * space, so a 375-derived --px renders the whole sheet at 63%.
 *
 * Declared once here so every band inherits it and can place children in raw Figma
 * coordinates.
 */
.sheet {
  container-type: inline-size;
  position: relative;
  width: 100%;
  overflow: hidden;
  background: var(--sheet);
}

.sheet > * {
  --px: calc(100cqw / 596); /* exact — a rounded decimal leaves the sheet 0.02px short of --body-h */
}
</style>
