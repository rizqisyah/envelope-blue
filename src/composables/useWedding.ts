import { ref, computed, onMounted } from 'vue'


import { resolveSlug, getHome, submitUcapan, DESIGN_MODE } from '../lib/api'

const state = ref<{
  loading: boolean
  error: string | null
  data: any | null
}>({
  loading: true,
  error: null,
  data: null,
})

function applyTheme(themeData: any, weddingData: any) {
  const cfg = themeData?.theme_config
  let override = weddingData?.theme_override
  if (typeof override === 'string') {
    try {
      override = JSON.parse(override)
    } catch {
      override = {}
    }
  }
  override = override || {}

  const root = document.documentElement
  const colors = { ...(cfg?.colors || {}), ...(override?.colors || {}) }
  const fonts = { ...(cfg?.fonts || {}), ...(override?.fonts || {}) }

  if (colors.primary) {
    root.style.setProperty('--maroon-title', colors.primary)
    root.style.setProperty('--ink-deep-blue', colors.primary)
  }
  if (colors.secondary) {
    root.style.setProperty('--maroon-text', colors.secondary)
    root.style.setProperty('--ink-blue', colors.secondary)
  }
  if (colors.accent) root.style.setProperty('--gold', colors.accent)
  if (colors.bg_body) {
    root.style.setProperty('--bg-body', colors.bg_body)
    root.style.setProperty('--paper', colors.bg_body)
    root.style.setProperty('--water', colors.bg_body)
  }
  if (colors.sheet) root.style.setProperty('--sheet', colors.sheet)
  if (colors.ink_deep_blue) root.style.setProperty('--ink-deep-blue', colors.ink_deep_blue)
  if (colors.ink_blue) root.style.setProperty('--ink-blue', colors.ink_blue)

  if (fonts.script) root.style.setProperty('--font-script', fonts.script)
  if (fonts.hand) root.style.setProperty('--font-hand', fonts.hand)
}

/*
 * 18 components call useWedding(), and they all mount in the same tick. The old guard
 * checked `state.loading`, which is still true at that point for every one of them, so
 * all 18 fired the same getHome request. Hold the first promise instead: the other 17
 * mounts see it and skip. Only the explicit `refetch` bypasses this.
 */
let inflight: Promise<void> | null = null

const slug = ref(resolveSlug())
const guestCode = ref(typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('to') || '' : '')

async function fetchWeddingData() {
  if (DESIGN_MODE) return
  state.value.loading = true
  state.value.error = null
  try {
    const data = await getHome(slug.value, guestCode.value)
    state.value.data = data
    if (data?.theme || data?.wedding) {
      applyTheme(data.theme, data.wedding)
    }
    if (data?.wedding?.title) {
      document.title = `${data.wedding.title} - Undangan Pernikahan`
    }
  } catch (err: any) {
    console.error('Failed to load wedding data:', err)
    state.value.error = err.message
  } finally {
    state.value.loading = false
  }
}

// Listen for live preview messages from the admin dashboard ("Mode Imajinasi")
if (typeof window !== 'undefined') {
  window.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'QINVI_PREVIEW_UPDATE') {
      const { wedding: previewWedding, theme: previewTheme, refetch } = event.data

      if (previewWedding) {
        let resolvedWedding = { ...previewWedding }
        if (typeof resolvedWedding.theme_override === 'string') {
          try {
            resolvedWedding.theme_override = JSON.parse(resolvedWedding.theme_override)
          } catch (e) {
            console.error('Failed to parse theme_override:', e)
          }
        }

        const existingOverride = state.value.data?.wedding?.theme_override || {}
        const mergedOverride = {
          ...existingOverride,
          ...(resolvedWedding.theme_override || {}),
        }

        state.value.data = {
          ...(state.value.data || {}),
          wedding: {
            ...(state.value.data?.wedding || {}),
            ...resolvedWedding,
            theme_override: mergedOverride,
          },
        }
      }

      if (previewTheme) {
        state.value.data = {
          ...(state.value.data || {}),
          theme: previewTheme,
        }
      }

      // Re-apply theme styles dynamically
      if (state.value.data?.theme || state.value.data?.wedding) {
        applyTheme(state.value.data.theme, state.value.data.wedding)
      }

      if (refetch) {
        inflight = null
        fetchWeddingData()
      }
    }
  })
}

/*
 * Wishes posted while in design mode. Kept outside `state` on purpose: seeding
 * state.data to hold them would make `wedding` non-null, and every band would drop
 * its design fallback mid-session.
 */
const designWishes = ref<any[]>([])

export function useWedding() {
  onMounted(() => {
    if (DESIGN_MODE || state.value.data) return
    inflight ??= fetchWeddingData().finally(() => {
      inflight = null
    })
  })

  const wedding = computed(() => state.value.data?.wedding ?? null)
  const theme = computed(() => state.value.data?.theme ?? null)
  const guest = computed(() => state.value.data?.guest ?? null)
  /*
   * getHome nests every list under `data.content` -- these were read straight off `data`,
   * so all five were permanently empty. No pixel diff could catch it: an empty list falls
   * back to the design's own copy and scores perfectly. Same class of bug as the `ucapan`
   * / `wishes` guess below. Read `content` first, then the flat key, so a payload of
   * either shape works.
   */
  const content = computed(() => state.value.data?.content ?? state.value.data ?? null)
  const pengantin = computed(() => content.value?.pengantin ?? [])
  const acara = computed(() => content.value?.acara ?? [])
  const gallery = computed(() => content.value?.gallery ?? [])
  // The API calls the account list `rekening`.
  const gift = computed(() => content.value?.rekening ?? content.value?.gift ?? [])
  const wishes = computed(() => designWishes.value.length ? designWishes.value : content.value?.ucapan ?? content.value?.wishes ?? [])

  /**
   * Post a wish and get it into the list without a refetch. The API may answer with the
   * refreshed list, with just the created row, or with neither, so all three are handled
   * — otherwise a guest submits and sees nothing happen.
   */
  // Writes `ucapan` back where `content` reads it from, or the new row is invisible.
  function putWishes(list: any[]) {
    const data = state.value.data
    if (!data) return
    state.value.data = data.content
      ? { ...data, content: { ...data.content, ucapan: list } }
      : { ...data, ucapan: list }
  }

  async function sendWish(body: { guest_name: string; message: string }): Promise<any> {
    /*
     * Design mode must not write to the live backend. The wish form is real and has
     * to keep working -- validation, pending, success, and the new wish appearing in
     * the list -- so the post is answered locally instead of being sent.
     */
    if (DESIGN_MODE) {
      const row = { id: `local-${Date.now()}`, ...body, created_at: new Date().toISOString() }
      designWishes.value = [row, ...designWishes.value]
      return { success: true, data: row }
    }
    const res = await submitUcapan(slug.value, body)
    if (!state.value.data) return res

    const list = Array.isArray(res) ? res : Array.isArray(res?.data) ? res.data : null
    if (list) {
      putWishes(list)
      return res
    }

    const row =
      res?.data && typeof res.data === 'object' && !Array.isArray(res.data)
        ? res.data
        : { id: `local-${Date.now()}`, ...body, created_at: new Date().toISOString() }
    putWishes([row, ...(Array.isArray(wishes.value) ? wishes.value : [])])
    return res
  }

  const groom = computed(() => pengantin.value.find((p: any) => p.type === 'groom') || null)
  const bride = computed(() => pengantin.value.find((p: any) => p.type === 'bride') || null)

  const isGroomFirst = computed(() => wedding.value?.order_groom_first !== false)

  const coupleNickname = computed(() => {
    if (groom.value?.name && bride.value?.name) {
      const gName = groom.value?.nickname?.trim() || groom.value.name.split(' ')[0]
      const bName = bride.value?.nickname?.trim() || bride.value.name.split(' ')[0]
      return isGroomFirst.value ? `${gName} & ${bName}` : `${bName} & ${gName}`
    }
    if (wedding.value?.title) return wedding.value.title
    // Frame 2 prints "Ahmad & Salma", so an unconfigured render matches the design.
    return isGroomFirst.value ? 'Ahmad & Salma' : 'Salma & Ahmad'
  })

  const parsedOverride = computed(() => {
    let ov = wedding.value?.theme_override
    if (typeof ov === 'string') {
      try {
        ov = JSON.parse(ov)
      } catch {
        ov = {}
      }
    }
    return ov || {}
  })

  const quoteText = computed(
    () =>
      parsedOverride.value?.quote?.text ||
      parsedOverride.value?.words?.quote_text ||
      '"Dan di antara tanda-tanda (kebesaran)-Nya ialah Dia menciptakan pasangan-pasangan untukmu dari jenismu sendiri, agar kamu cenderung dan merasa tenteram kepadanya, dan Dia menjadikan di antaramu rasa kasih dan sayang"',
  )

  const hashtag = computed(
    () =>
      parsedOverride.value?.words?.hashtag ||
      wedding.value?.hashtag ||
      '#AhmadSALMAnya',
  )

  const quoteVerse = computed(
    () =>
      parsedOverride.value?.quote?.verse ||
      parsedOverride.value?.words?.quote_verse ||
      '(Qs. Ar-Rum: 21)',
  )

  const quoteArabic = computed(
    () =>
      parsedOverride.value?.quote?.arabic ||
      parsedOverride.value?.words?.quote_arabic ||
      'وَمِنْ اٰيٰتِهٖٓ اَنْ خَلَقَ لَكُمْ مِّنْ اَنْفُسِكُمْ اَزْوَاجًا لِّتَسْكُنُوْٓا اِلَيْهَا وَجَعَلَ بَيْنَكُمْ مَّوَدَّةً وَّرَحْمَةًۗ اِنَّ فِيْ ذٰلِكَ لَاٰيٰتٍ لِّقَوْمٍ يَّتَفَكَّرُوْنَ',
  )

  const dresscode = computed(() => {
    const ov = parsedOverride.value
    return {
      note: ov?.dresscode?.note || 'Attire: Formal / Traditional Elegance',
      colors:
        Array.isArray(ov?.dresscode?.colors) && ov.dresscode.colors.length === 4
          ? ov.dresscode.colors
          : ['#dbc58e', '#9bccdb', '#bde0b5', '#edcbe3'],
    }
  })

  return {
    slug,
    guestCode,
    loading: computed(() => state.value.loading),
    error: computed(() => state.value.error),
    wedding,
    theme,
    guest,
    pengantin,
    acara,
    gallery,
    gift,
    wishes,
    sendWish,
    groom,
    bride,
    isGroomFirst,
    coupleNickname,
    hashtag,
    quoteText,
    quoteVerse,
    quoteArabic,
    dresscode,
    refetch: fetchWeddingData,
  }
}
