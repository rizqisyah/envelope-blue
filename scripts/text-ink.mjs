// Isolate a band's LIVE text ink by difference, not by colour.
//
// ink-box.py thresholds a crop against its own most common colour, which the toile
// wallpaper defeats; keying on each node's fill colour fails too, because the greeting's
// dark green IS the foliage's green. Shooting the sheet twice — once normally, once with
// the text nodes hidden — and differencing leaves exactly the glyph ink and nothing else,
// whatever it is sitting on.
//
//   node scripts/text-ink.mjs <port> <selector,selector,...>
// Writes .figma-tmp/web-sheet-1x.png and .figma-tmp/web-sheet-notext.png
import { chromium } from 'playwright'

const PORT = process.argv[2] || 5179
const SELECTORS = (process.argv[3] || '').split(',').filter(Boolean)
const FRAME_W = Number(process.env.FRAME_W || 596)

const browser = await chromium.launch()
const page = await browser.newPage({
  viewport: { width: FRAME_W, height: 900 },
  deviceScaleFactor: 1,
  reducedMotion: 'reduce',
})
await page.goto(`http://localhost:${PORT}/`, { waitUntil: 'networkidle' })
await page.waitForTimeout(600)
await page.click('.cover__hit')
await page.waitForTimeout(2400)
const h = await page.evaluate(() => document.documentElement.scrollHeight)
for (let y = 0; y < h; y += 400) {
  await page.evaluate((t) => window.scrollTo(0, t), y)
  await page.waitForTimeout(120)
}
await page.evaluate(() => window.scrollTo(0, 0))
await page.waitForTimeout(600)

await page.locator('.sheet').screenshot({ path: '.figma-tmp/web-sheet-1x.png' })

// Report what the browser actually computed, so a rule that silently failed to apply is
// visible instead of being inferred from a width that did not move.
for (const sel of SELECTORS) {
  const info = await page.evaluate((s) => {
    const el = document.querySelector(s)
    if (!el) return null
    const cs = getComputedStyle(el)
    const r = el.getBoundingClientRect()
    return { fontSize: cs.fontSize, lineHeight: cs.lineHeight, fontFamily: cs.fontFamily.split(',')[0],
             letterSpacing: cs.letterSpacing, box: `${Math.round(r.width)}x${Math.round(r.height)}` }
  }, sel)
  console.log(`${sel}  ${info ? JSON.stringify(info) : 'NOT FOUND'}`)
}

await page.addStyleTag({ content: `${SELECTORS.join(',')} { visibility: hidden !important }` })
await page.waitForTimeout(200)
await page.locator('.sheet').screenshot({ path: '.figma-tmp/web-sheet-notext.png' })
await browser.close()
console.log('wrote web-sheet-1x.png and web-sheet-notext.png')
