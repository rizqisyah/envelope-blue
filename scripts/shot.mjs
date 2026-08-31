// Visual check for the sliced screens: screenshots the running dev server at three
// viewports, then clicks the cover open. Compare .figma-tmp/web-*.png against the
// Figma reference render. Usage: pnpm dev & node scripts/shot.mjs [port]
import { chromium } from 'playwright'

const PORT = process.argv[2] || 5179
const URL = `http://localhost:${PORT}/?to=Ahmad%20%26%20Salma`
const OUT = '.figma-tmp'
const VIEWPORTS = [
  ['mobile', 375, 725], // a narrow phone (the design frame is 596 — see the sheet page below)
  ['phone812', 375, 812], // a real phone
  ['desktop', 1440, 900],
]

const browser = await chromium.launch()
const errors = []

// reducedMotion pins the entrance stagger and the hint's breathing loop to their
// end state, so these shots are deterministic *and* exercise the reduced-motion path.
for (const [name, width, height] of VIEWPORTS) {
  const page = await browser.newPage({
    viewport: { width, height },
    deviceScaleFactor: 2,
    reducedMotion: 'reduce',
  })
  page.on('pageerror', (e) => errors.push(`[${name}] pageerror: ${e.message}`))
  await page.goto(URL, { waitUntil: 'networkidle' })
  await page.waitForTimeout(1500)
  await page.screenshot({ path: `${OUT}/web-${name}.png` })
  await page.close()
}

// Frames mid-stagger, to eyeball the entrances themselves.
const motion = await browser.newPage({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2 })
await motion.goto(URL, { waitUntil: 'networkidle' })
await motion.waitForTimeout(1100)
await motion.screenshot({ path: `${OUT}/web-entrance.png` })
await motion.click('.cover__hit')
await motion.waitForTimeout(2200)
await motion.screenshot({ path: `${OUT}/web-hero-reveal.png` })
// The reduced-motion shots below force everything visible, so they can't tell us
// whether useReveal actually fired. This can.
const revealed = (await motion.locator('.hero.is-in').count()) === 1
await motion.close()

// The cover's only job is to open the invitation — assert it actually does.
const page = await browser.newPage({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2 })
await page.goto(URL, { waitUntil: 'networkidle' })
await page.waitForTimeout(1000)
await page.click('.cover__hit')
await page.waitForTimeout(3000)
const opened = await page.locator('#invite').isVisible()
// `.cover`, not template 5's `.opening`: that class does not exist in this template, so
// the check was vacuously true and could not have caught the cover failing to unmount.
const coverGone = (await page.locator('.cover').count()) === 0
await page.screenshot({ path: `${OUT}/web-opened.png` })
await page.close()

// The invitation sheet at exactly the design frame width, so it lines up 1:1 with the
// Figma frame render for a pixel diff. Reduced motion pins every reveal open.
const sheet = await browser.newPage({
  viewport: { width: 596, height: 900 },
  deviceScaleFactor: 2,
  reducedMotion: 'reduce',
})
await sheet.goto(URL, { waitUntil: 'networkidle' })
await sheet.waitForTimeout(800)
await sheet.click('.cover__hit')
await sheet.waitForTimeout(2500)
await sheet.locator('.hero').screenshot({ path: `${OUT}/web-hero.png` })
// Scroll the whole sheet past the viewport first: the reveals are viewport-gated
// and the fit-to-box pass needs each block to have been rendered at least once.
const sheetHeight = await sheet.evaluate(() => document.documentElement.scrollHeight)
for (let y = 0; y < sheetHeight; y += 400) {
  await sheet.evaluate((to) => window.scrollTo(0, to), y)
  await sheet.waitForTimeout(250)
}
await sheet.waitForTimeout(1500)
// Every band below the fold is viewport-gated, so the scroll above is what fires
// them. Read the band list off the DOM rather than naming them: a hard-coded list is
// a list of ANOTHER template's bands the moment it is copied, and every entry then
// reports a band that does not exist as a failed reveal.
const bands = await sheet.evaluate(() =>
  [...document.querySelectorAll('.sheet > section.band')].map((el) => ({
    name: [...el.classList].find((c) => c !== 'band' && c !== 'is-in') || '?',
    shown: el.classList.contains('is-in'),
  })),
)
/*
 * The gallery carousel is the only thing in the sheet that has state, so it is the only
 * thing a screenshot cannot check. Click "next" and confirm the oval's photo actually
 * changed -- a wrong modulo or a broken index reads as a still picture, which every other
 * check in this file would pass.
 */
const carousel = await sheet.evaluate(async () => {
  const oval = document.querySelector('.gallery__oval img')
  const next = document.querySelectorAll('.gallery__nav')[1]
  if (!oval || !next) return 'no carousel'
  const prev = document.querySelectorAll('.gallery__nav')[0]
  const before = oval.getAttribute('src')
  next.click()
  await new Promise((r) => setTimeout(r, 200))
  const after = document.querySelector('.gallery__oval img')?.getAttribute('src')
  // Put it back before the sheet screenshot below: left on photo 2 this check would
  // bake its own leftover state into web-sheet.png and every later band's eyeball pass
  // would show a "regression" that is only the test.
  prev.click()
  await new Promise((r) => setTimeout(r, 200))
  const restored = document.querySelector('.gallery__oval img')?.getAttribute('src')
  if (before === after) return `unchanged (${before})`
  return restored === before ? 'ok' : 'advanced but did not restore'
})

await sheet.evaluate(() => window.scrollTo(0, 0))
await sheet.waitForTimeout(400)
await sheet.locator('.sheet').screenshot({ path: `${OUT}/web-sheet.png` })
await sheet.close()
await browser.close()

console.log(`invite visible after click: ${opened}`)
console.log(`cover removed after transition: ${coverGone}`)
console.log(`hero reveal fired: ${revealed}`)
for (const b of bands) console.log(`${b.name} reveal fired on scroll: ${b.shown}`)
console.log(`gallery carousel advances: ${carousel}`)
if (errors.length) console.log(errors.join('\n'))
if (!opened || !revealed || bands.some((b) => !b.shown) || carousel !== 'ok') process.exitCode = 1
