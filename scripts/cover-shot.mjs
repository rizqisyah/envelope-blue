// Shoot the cover at exactly the frame's own width and deviceScaleFactor 1, so it lines
// up 1:1 with the scale-1 Figma frame render and needs no resampling.
//
//   npm run dev & node scripts/cover-shot.mjs [port]
import { chromium } from 'playwright'

const PORT = process.argv[2] || 5179
const W = Number(process.env.FRAME_W || 596)
const H = Number(process.env.FRAME_H || 1183)
const OUT = '.figma-tmp/web-cover-1x.png'

const browser = await chromium.launch()
const page = await browser.newPage({
  viewport: { width: W, height: H },
  deviceScaleFactor: 1,
  // Pins the entrance stagger and the envelope's breathing loop to their end state, so
  // the shot is deterministic *and* exercises the reduced-motion path.
  reducedMotion: 'reduce',
})
const errors = []
page.on('pageerror', (e) => errors.push(e.message))
await page.goto(`http://localhost:${PORT}/`, { waitUntil: 'networkidle' })
await page.waitForTimeout(1200)
const box = await page.locator('.cover__frame').boundingBox()
console.log(`cover ${box.width} x ${box.height}`)
await page.locator('.cover__frame').screenshot({ path: OUT })
await page.click('.cover__hit')
await page.waitForTimeout(2500)
console.log(`invite visible after click: ${await page.locator('#invite').isVisible()}`)
console.log(`cover removed: ${(await page.locator('.cover').count()) === 0}`)
if (errors.length) console.log(errors.join('\n'))
await browser.close()
console.log(`wrote ${OUT}`)
