import { ref } from 'vue'

/*
 * Assets are discovered by glob so a new slice needs no edit here.
 * Cover = the splash screen, sliced into `src/assets/opening/`. Body = the invitation
 * frame, sliced band by band; each new `src/assets/<band>/` directory joins the body
 * glob automatically.
 */
const coverImages = Object.values(
  import.meta.glob('../assets/opening/**/*.webp', { eager: true, import: 'default' }),
) as string[]

const bodyImages = Object.values(
  import.meta.glob(['../assets/**/*.webp', '!../assets/opening/**'], {
    eager: true,
    import: 'default',
  }),
) as string[]

const coverLoaded = ref(false)
const bodyLoaded = ref(false)

function preloadImage(url: string): Promise<void> {
  return new Promise((resolve) => {
    const img = new Image()
    img.src = url
    if (img.complete) {
      resolve()
    } else {
      img.onload = () => resolve()
      img.onerror = () => resolve() // resolve even on error so the app won't stall
    }
  })
}

export function usePreloadAssets() {
  async function preloadCover() {
    if (coverLoaded.value) return
    await Promise.all(coverImages.map(preloadImage))
    coverLoaded.value = true
  }

  function preloadInviteBody() {
    if (bodyLoaded.value) return
    const loadBody = () => {
      Promise.all(bodyImages.map(preloadImage)).then(() => {
        bodyLoaded.value = true
      })
    }
    if ('requestIdleCallback' in window) {
      window.requestIdleCallback(loadBody, { timeout: 2000 })
    } else {
      setTimeout(loadBody, 200)
    }
  }

  return {
    coverLoaded,
    bodyLoaded,
    preloadCover,
    preloadInviteBody,
  }
}
