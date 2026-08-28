/*
 * Every sliced sprite, keyed by its `<section>/parts/<id>.webp` path so the generated
 * band tables can name assets as plain strings instead of one import line each.
 */
const modules = import.meta.glob('../assets/**/parts/*.webp', {
  eager: true,
  import: 'default',
}) as Record<string, string>

export const assets = Object.fromEntries(
  Object.entries(modules).map(([path, url]) => [path.replace('../assets/', ''), url]),
) as Record<string, string>
