# TemaEnvelopBlue Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the `envelope-blue` frontend wedding template into the Qinvi backend system and Admin Dashboard, matching the architecture and custom override capabilities established by `TemaEnvelopRed` plus dedicated Dresscode and Quranic Arabic text support.

**Architecture:** 
- The Qinvi backend manages theme definitions via `theme_config` objects in `src/config/themes/`, seeded to PostgreSQL via Drizzle ORM, and serves SSR previews routing to local port `5179`.
- The Admin Dashboard (`admin-dashboard`) enables administrators to customize theme colors, cover/prewedding photo scale and positioning, Quranic quotes with Arabic text, and dresscode palettes via `TabThemeOverride.tsx`.
- The frontend client (`envelope-blue`) resolves wedding data by slug or query parameter through `src/lib/api.ts` and `src/composables/useWedding.ts`, injecting CSS variable tokens and binding dynamic acara, couple, dresscode, quote, gift, and wish data.

**Tech Stack:** TypeScript, Vue 3, Vite, React (Admin Dashboard), Drizzle ORM / Express (Backend Qinvi), CSS Variables.

## Global Constraints

- Theme Code: `TemaEnvelopBlue`
- Default Slug: `tema-envelop-blue`
- Local Development Port for envelope-blue: `5179`
- Preserve design mode fallbacks so components never break if API data is missing or partial.
- Maintain strict type safety across Vue 3 and React TypeScript modules.

---

### Task 1: Backend Theme Configuration & SSR Redirection

**Files:**
- Create: `f:/Undangan/qinvi/src/config/themes/tema-envelop-blue.config.ts`
- Modify: `f:/Undangan/qinvi/src/db/seed-themes.ts`
- Modify: `f:/Undangan/qinvi/src/modules/ssr/ssr.controller.ts:170-184`

**Interfaces:**
- Produces: `temaEnvelopBlueConfig` object conforming to theme config schema (`code`, `name`, `category`, `theme_config` with colors, fonts, backgrounds, images).
- Modifies: `ssr.controller.ts` to route `TemaEnvelopBlue` requests to `http://localhost:5179`.

- [ ] **Step 1: Create `tema-envelop-blue.config.ts`**
Define `temaEnvelopBlueConfig` with the blue palette tokens (`#3d78a2`, `#65839d`, `#9bccdb`, `#e9faff`, `#e7f9fe`), typography tokens, and default asset slots.

- [ ] **Step 2: Register config in `seed-themes.ts`**
Import `temaEnvelopBlueConfig` and append it to `themesToSeed` array in `f:/Undangan/qinvi/src/db/seed-themes.ts`.

- [ ] **Step 3: Update SSR Controller port mapping in `ssr.controller.ts`**
Add `else if (themeCode === 'TemaEnvelopBlue') { frontendBase = 'http://localhost:5179'; }` in `f:/Undangan/qinvi/src/modules/ssr/ssr.controller.ts`.

- [ ] **Step 4: Verify Backend TypeScript build**
Run: `npx tsc --noEmit` in `f:/Undangan/qinvi`.
Expected: Exit code 0 without type errors in theme config or ssr controller.

- [ ] **Step 5: Commit changes**
Run git commit in `f:/Undangan/qinvi`:
`git add src/config/themes/tema-envelop-blue.config.ts src/db/seed-themes.ts src/modules/ssr/ssr.controller.ts; git commit -m "feat(backend): register TemaEnvelopBlue theme config and SSR route"`

---

### Task 2: Backend Wedding Seed Script for TemaEnvelopBlue

**Files:**
- Create: `f:/Undangan/qinvi/src/db/seed-wedding-envelop-blue.ts`
- Modify: `f:/Undangan/qinvi/package.json` (add seed script shortcut if appropriate)

**Interfaces:**
- Consumes: `profiles`, `weddings`, `pengantin`, `acara` tables from Drizzle schema.
- Produces: Seeded wedding row with slug `tema-envelop-blue`, `theme_code: 'TemaEnvelopBlue'`, couple profiles (Ahmad & Salma), and event schedules (Akad & Resepsi).

- [ ] **Step 1: Write `seed-wedding-envelop-blue.ts`**
Create the database seeder that queries an active client profile, inserts or updates a wedding with slug `tema-envelop-blue`, sets `theme_code: 'TemaEnvelopBlue'`, and seeds initial `theme_override` containing quote (text, verse, arabic) and dresscode (note, colors).

- [ ] **Step 2: Verify Seeder script syntax & execution**
Run: `npx tsx src/db/seed-wedding-envelop-blue.ts` in `f:/Undangan/qinvi` (or test with dry-run check).
Expected: Seeding output showing wedding slug `tema-envelop-blue` created or updated.

- [ ] **Step 3: Commit changes**
Run git commit in `f:/Undangan/qinvi`:
`git add src/db/seed-wedding-envelop-blue.ts; git commit -m "feat(db): add wedding seed script for tema-envelop-blue"`

---

### Task 3: Admin Dashboard Theme & Custom Override Controls

**Files:**
- Modify: `f:/Undangan/qinvi/admin-dashboard/src/views/ThemeManagement.tsx`
- Modify: `f:/Undangan/qinvi/admin-dashboard/src/tabs/TabThemeOverride.tsx`

**Interfaces:**
- Consumes: Wedding `theme_code` and `theme_override` JSONB from backend API.
- Produces: UI inputs for `spousePhotoTransform`, `theme_override.quote.arabic`, and `theme_override.dresscode` for `TemaEnvelopBlue`.

- [ ] **Step 1: Update `ThemeManagement.tsx`**
Ensure `TemaEnvelopBlue` is registered and handled cleanly in theme selection filters.

- [ ] **Step 2: Enable Spouse Photo Zoom & Position for `TemaEnvelopBlue` in `TabThemeOverride.tsx`**
Update the theme code condition in `TabThemeOverride.tsx` (around lines 1197 & 1352) to explicitly include `(wedding as any)?.theme_code === 'TemaEnvelopBlue'`.

- [ ] **Step 3: Add Arabic Quranic Quote & Verse Editor in `TabThemeOverride.tsx`**
Add an input/textarea for Arabic verse (`theme_override.quote.arabic`) displayed when editing `TemaEnvelopBlue`.

- [ ] **Step 4: Add Dresscode Section Editor in `TabThemeOverride.tsx`**
Add a dedicated Dresscode editor block when `theme_code === 'TemaEnvelopBlue'`:
- Text input for attire instruction (`theme_override.dresscode.note`).
- 4 color inputs for dresscode swatches (`theme_override.dresscode.colors`).

- [ ] **Step 5: Verify Admin Dashboard Build**
Run: `npm run build` in `f:/Undangan/qinvi/admin-dashboard`.
Expected: Successful build with 0 TypeScript/ESLint errors.

- [ ] **Step 6: Commit changes**
Run git commit in `f:/Undangan/qinvi/admin-dashboard`:
`git add src/views/ThemeManagement.tsx src/tabs/TabThemeOverride.tsx; git commit -m "feat(dashboard): add TemaEnvelopBlue override controls for photos, arabic quote, and dresscode"`

---

### Task 4: Frontend Envelope Blue API, Routing & Live Data Wire-up

**Files:**
- Modify: `f:/Undangan/qinvi/envelope-blue/src/lib/api.ts`
- Modify: `f:/Undangan/qinvi/envelope-blue/src/composables/useWedding.ts`
- Modify: `f:/Undangan/qinvi/envelope-blue/.env.example`

**Interfaces:**
- Produces: `resolveSlug()` supporting query parameter `?slug=` and default `tema-envelop-blue`.
- Produces: `dresscode` computed property and CSS variable bindings for blue tokens in `useWedding()`.

- [ ] **Step 1: Update `resolveSlug()` in `envelope-blue/src/lib/api.ts`**
Update `resolveSlug` to inspect `?slug=` query parameter and ignore path segment `/TemaEnvelopBlue` or `/tema-envelop-blue`, falling back to `DEFAULT_SLUG = 'tema-envelop-blue'`.

- [ ] **Step 2: Extend `applyTheme()` in `useWedding.ts`**
Map `colors.primary` to `--ink-deep-blue` and `--maroon-title`, `colors.secondary` to `--ink-blue` and `--maroon-text`, `colors.accent` to `--gold`, and `colors.bg_body` to `--bg-body` / `--paper` / `--sheet`.

- [ ] **Step 3: Add `dresscode` computed state in `useWedding.ts`**
Expose `dresscode` computed property that retrieves `theme_override?.dresscode?.note` and `theme_override?.dresscode?.colors` with default fallback to Figma's 4 swatches (`#dbc58e`, `#9bccdb`, `#bde0b5`, `#edcbe3`).

- [ ] **Step 4: Verify `envelope-blue` TypeScript build**
Run: `npm run build` in `f:/Undangan/qinvi/envelope-blue`.
Expected: Successful build with 0 TypeScript errors.

- [ ] **Step 5: Commit changes**
Run git commit in `f:/Undangan/qinvi/envelope-blue`:
`git add src/lib/api.ts src/composables/useWedding.ts; git commit -m "feat(api): support query slug and theme override bindings for TemaEnvelopBlue"`

---

### Task 5: Frontend Dynamic Section Bindings & End-to-End Verification

**Files:**
- Modify: `f:/Undangan/qinvi/envelope-blue/src/components/sections/DresscodeSection.vue`
- Modify: `f:/Undangan/qinvi/envelope-blue/src/components/sections/BismillahSection.vue`
- Inspect: `f:/Undangan/qinvi/envelope-blue/src/components/sections/AkadSection.vue`
- Inspect: `f:/Undangan/qinvi/envelope-blue/src/components/sections/ResepsiSection.vue`

**Interfaces:**
- Consumes: `dresscode`, `quoteArabic`, `quoteText`, `quoteVerse` from `useWedding()`.
- Produces: Dynamic rendering of dresscode swatches, notes, and Arabic quotes.

- [ ] **Step 1: Update `DresscodeSection.vue` to consume dynamic dresscode**
Replace hardcoded swatches and copy with `dresscode.colors` and `dresscode.note` from `useWedding()`.

- [ ] **Step 2: Update `BismillahSection.vue` to consume dynamic `quoteArabic`**
Bind the Arabic script element to `quoteArabic` from `useWedding()`.

- [ ] **Step 3: Verify end-to-end frontend build**
Run: `npm run build` in `f:/Undangan/qinvi/envelope-blue`.
Expected: Successful build with 0 errors.

- [ ] **Step 4: Run manual preview check**
Run dev server or verify output in browser on `http://localhost:5179?slug=tema-envelop-blue`.

- [ ] **Step 5: Commit changes**
Run git commit in `f:/Undangan/qinvi/envelope-blue`:
`git add src/components/sections/DresscodeSection.vue src/components/sections/BismillahSection.vue; git commit -m "feat(ui): bind dynamic dresscode and arabic quote in envelope-blue"`
