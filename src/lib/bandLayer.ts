/** One sliced sprite of the body frame, placed in band-local design px. */
export type BandLayer = {
  /** Global Figma child order — bands share one stacking context, so this is comparable across them. */
  z: number
  id: string
  src: string
  x: number
  y: number
  w: number
  h: number
  /**
   * Opacity, when the design fades this layer. Figma's MCP reports neither `opacity`
   * nor `blendMode`, so every export comes back at full strength; scripts/solve_alpha.py
   * recovers the value by compositing the band and scoring it against the render.
   * Absent means 1.
   */
  a?: number
  /**
   * `mix-blend-mode`, when the layer is a light-leak plate the design blends rather
   * than stacks. Solved the same way as `a`, and for the same reason. Absent means
   * `normal`.
   */
  b?: string
}
