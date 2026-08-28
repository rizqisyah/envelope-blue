// Generated from the Figma dump — do not hand-edit. Frame 2 (27:9), 596 x 1183.
// `z` is Figma child order, which IS the paint order; the text nodes in
// CoverSection.vue carry their own slots in the same sequence (3..6).
//
// Both layers export at 2x. `27:218` is the only one whose numbers are NOT its
// reported bounds: it declares 681 x 1211 at x -41.95 and exports 1192 x 2366 — the
// frame's own 596 x 1183 doubled — so Figma clipped it to the frame on both edges.
// The clip rule therefore gives it the whole frame, not its declared box.
// `27:216` exports 948 x 976, exactly 2x its declared 474 x 488, so its bounds stand.
const modules = import.meta.glob('../assets/opening/parts/*.webp', {
  eager: true,
  import: 'default',
}) as Record<string, string>

const parts = Object.fromEntries(
  Object.entries(modules).map(([path, url]) => [path.split('/').pop()!.replace('.webp', ''), url]),
) as Record<string, string>

export type CoverLayer = {
  z: number
  id: string
  src: string
  x: number
  y: number
  w: number
  h: number
}

export const COVER_LAYERS: CoverLayer[] = [
  { z: 1, id: '27:218', src: parts['27-218'], x: 0, y: 0, w: 596, h: 1183 },
  { z: 2, id: '27:216', src: parts['27-216'], x: 61, y: 302, w: 474, h: 488 },
]
