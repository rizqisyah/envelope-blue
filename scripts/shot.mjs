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
  // The gift band's Copy button writes to the clipboard, which is permission-gated:
  // without this its handler throws and the check below reads as a broken button.
  permissions: ['clipboard-write'],
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

/*
 * The gift band's Copy button is the other stateful control. Click it, confirm the label
 * confirms the copy, and confirm it reverts -- a rejected clipboard write leaves the label
 * alone, which is exactly the failure a screenshot cannot see.
 */
const copyBtn = await sheet.evaluate(async () => {
  const btn = document.querySelector('.gift__copy')
  if (!btn) return 'no copy button'
  const before = btn.textContent.trim()
  btn.click()
  await new Promise((r) => setTimeout(r, 300))
  const after = document.querySelector('.gift__copy').textContent.trim()
  await new Promise((r) => setTimeout(r, 1700))
  const back = document.querySelector('.gift__copy').textContent.trim()
  if (before === after) return `label did not change (${before})`
  return back === before ? 'ok' : `confirmed but stuck on "${back}"`
})

await sheet.evaluate(() => window.scrollTo(0, 0))
await sheet.waitForTimeout(400)
await sheet.locator('.sheet').screenshot({ path: `${OUT}/web-sheet.png` })

/*
 * The rsvp form is the fourth stateful control. In design mode `submitRsvp` throws by
 * design, so a submitted form must ANSWER — an empty error line means the click never
 * reached the handler, which looks identical to a working form in a screenshot.
 */
const rsvpForm = await sheet.evaluate(async () => {
  const setValue = (el, v) => {
    const proto = Object.getPrototypeOf(el)
    Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, v)
    el.dispatchEvent(new Event('input', { bubbles: true }))
    el.dispatchEvent(new Event('change', { bubbles: true }))
  }
  const form = document.querySelector('.rsvp__form')
  if (!form) return 'no rsvp form'
  // The name arrives filled in -- design mode's guest is "Ahmad & Salma" -- so the
  // empty-name branch is reached by clearing it, not by submitting as loaded.
  setValue(form.querySelector('input[type="text"]'), '')
  form.requestSubmit()
  await new Promise((r) => setTimeout(r, 200))
  const blank = document.querySelector('.rsvp__error')?.textContent.trim()
  if (blank !== 'Nama masih kosong.') return `no name validation (${blank})`
  setValue(form.querySelector('input[type="text"]'), 'Playwright')
  form.requestSubmit()
  await new Promise((r) => setTimeout(r, 200))
  const noPick = document.querySelector('.rsvp__error')?.textContent.trim()
  if (noPick !== 'Pilih kehadiran dulu.') return `no attendance validation (${noPick})`
  setValue(form.querySelector('select'), 'hadir')
  form.requestSubmit()
  await new Promise((r) => setTimeout(r, 600))
  // Design mode makes submitRsvp throw on purpose; the form has to say so.
  const answered = document.querySelector('.rsvp__error')?.textContent.trim()
  return answered && answered !== noPick ? 'ok' : `submitted but silent (${answered})`
})


/*
 * The wish form is the third stateful control, and the only one that writes: in design
 * mode `sendWish` answers locally, so a submitted wish must appear at the top of the list
 * with the guest's name on it. A silent failure here looks exactly like a working form.
 */
const wishForm = await sheet.evaluate(async () => {
  const setValue = (el, v) => {
    const proto = Object.getPrototypeOf(el)
    Object.getOwnPropertyDescriptor(proto, 'value').set.call(el, v)
    el.dispatchEvent(new Event('input', { bubbles: true }))
  }
  const name = document.querySelector('.wishes__name')
  const msg = document.querySelector('.wishes__message')
  const form = document.querySelector('.wishes__form')
  if (!name || !msg || !form) return 'no wish form'
  const before = document.querySelectorAll('.wishes__card').length
  setValue(name, 'Playwright')
  setValue(msg, 'shot.mjs was here')
  form.requestSubmit()
  await new Promise((r) => setTimeout(r, 600))
  const first = document.querySelector('.wishes__card .wishes__from')?.textContent.trim()
  const after = document.querySelectorAll('.wishes__card').length
  if (first !== 'Playwright') return `wish not at top (${first})`
  return after >= before ? 'ok' : 'list shrank'
})

await sheet.close()
await browser.close()

console.log(`invite visible after click: ${opened}`)
console.log(`cover removed after transition: ${coverGone}`)
console.log(`hero reveal fired: ${revealed}`)
for (const b of bands) console.log(`${b.name} reveal fired on scroll: ${b.shown}`)
console.log(`gallery carousel advances: ${carousel}`)
console.log(`gift copy button confirms: ${copyBtn}`)
console.log(`rsvp form answers: ${rsvpForm}`)
console.log(`wish form posts: ${wishForm}`)
if (errors.length) console.log(errors.join('\n'))
if (
  !opened ||
  !revealed ||
  bands.some((b) => !b.shown) ||
  carousel !== 'ok' ||
  copyBtn !== 'ok' ||
  rsvpForm !== 'ok' ||
  wishForm !== 'ok'
)
  process.exitCode = 1
