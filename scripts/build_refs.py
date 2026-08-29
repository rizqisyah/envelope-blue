#!/usr/bin/env python3
"""Turn the raw Figma dump of the body frame into the two files gen_band.py reads.

Flattens the node tree to leaves in global paint order, assigns each one a band, and
converts every exported PNG to webp under src/assets/<band>/parts/.

Two things about the flatten are easy to get wrong and both were bugs first:

- Figma's `children` are BOTTOM-FIRST, so a depth-first walk over them is already the
  global paint order. `z` is just the index.
- A GROUP's children report ABSOLUTE (frame-local) coordinates; a FRAME's children report
  coordinates relative to that frame. Only the FRAME case needs the parent offset added.

Band assignment is a y-range table, because Figma has no section marker to read. It is a
HINT -- gen_band.py derives each band's real top from the nodes assigned to it, and a
layer that renders outside its band still lands in the right place, since positions are
absolute within the sheet and no section clips.

    BODY_FRAME=<n> BODY_H=<h> python3 scripts/build_refs.py

Reads .figma-tmp/frame<N>-flat.json (the flattened dump, from flatten_frame.py) and
.figma-tmp/parts<N>/*.png (one export per node, scale 2). Re-dump those from Figma if
the design changes.

BANDS, SHEET_PLATES and EMPTY below are PER DESIGN and start empty. Fill them from this
template's own frame; ../slicing-wedding-template-5/scripts/build_refs.py has a worked
set if the shape of an entry is unclear.
"""
import json, os, subprocess, sys
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

FRAME = os.environ.get('BODY_FRAME', '')
if not FRAME:
    sys.exit('set BODY_FRAME=<body frame number>')
FRAME_H = int(os.environ.get('BODY_H', '0'))
if not FRAME_H:
    sys.exit('set BODY_H=<body frame height in design px>')
# The node id of the frame itself, recorded in both output files.
FRAME_ID = os.environ.get('BODY_FRAME_ID', FRAME)

FLAT = json.load(open(f'.figma-tmp/frame{FRAME}-flat.json'))

# Band tops, in design px. A node lands in the last band whose top is <= its y.
# Derived by eye from the frame render's headings, then refined by gen_band.py.
# Only the hero/countdown boundary is VERIFIED: 1108 is the top of `26:8`, the ornate
# countdown frame, and the render's own seam. Everything below it is provisional -- read
# off heading positions in the frame render, good enough to keep the nodes in roughly the
# right buckets, and to be re-measured when each band is actually cut.
BANDS = [
    ('hero', 0),          # verified
    ('countdown', 1108),  # verified -- 26:8 "Open (16) 1"
    ('bismillah', 1700),
    ('bride', 2150),
    ('groom', 3150),
    ('quote', 4000),
    ('akad', 4800),
    ('resepsi', 5900),
    ('dresscode', 6900),
    ('gallery', 7700),
    ('gift', 8800),
    ('wishes', 9550),
    ('rsvp', 10700),
    ('closing', 11450),
]

# Full-sheet flat-colour plates: CSS on the sheet in InviteBody.vue, not images.
# Frame 1 paints its ground with its own #e7f9fe fill and no flat rectangle, so this
# stays empty; the sheet's `background: var(--sheet)` is that fill.
SHEET_PLATES = set()
# Exports that came back fully transparent. Every hero export carries ink -- the sparsest
# is 20:647 at 7.4% opaque, which is the light wash over the portrait, not an empty file.
EMPTY = set()

if not BANDS:
    sys.exit('fill in BANDS first -- see the docstring')

def section(y):
    name = BANDS[0][0]
    for n, top in BANDS:
        if y >= top:
            name = n
    return name

zorder, nodes = [], {}
for f in FLAT:
    if f['id'] in SHEET_PLATES or f['id'] in EMPTY:
        continue
    sec = section(f['y'])
    row = dict(z=f['z'], id=f['id'], name=f['name'], type=f['type'],
               x=f['x'], y=f['y'], w=f['w'], h=f['h'], section=sec)
    zorder.append(row)
    # TEXT stays live so useWedding() can drive it -- never baked into an image.
    # TEXT_PATH (lettering bent along a curve) is the exception and ships as art;
    # Figma reports it as TEXT, so pull those ids out by hand when the frame has any.
    if f['type'] == 'TEXT':
        continue
    src = f".figma-tmp/parts{FRAME}/{f['id'].replace(':', '-')}.png"
    if not os.path.exists(src):
        print('!! missing export', f['id']); continue
    out_dir = f"src/assets/{sec}/parts"
    os.makedirs(out_dir, exist_ok=True)
    out = f"{out_dir}/{f['id'].replace(':', '-')}.webp"
    # q95, not the 88 templates 2-5 used. Measured on this band: 88 -> 1.956, 92 -> 1.819,
    # 95 -> 1.720 mean abs delta, for 2.3M / 2.2M / 2.6M of hero art. Nearly all of what
    # is left in the score is compression on the toile's high-contrast edges, so quality
    # is the only lever still moving it. Drop to 92 if page weight ever matters more --
    # it beats 88 on both axes.
    subprocess.run(['cwebp', '-quiet', '-q', '95', '-alpha_q', '100', src, '-o', out], check=True)
    nodes[f['id']] = dict(asset=f"{sec}/parts/{f['id'].replace(':', '-')}.webp",
                          figmaName=f['name'], x=f['x'], y=f['y'], w=f['w'], h=f['h'])

json.dump({'frame': FRAME_ID, 'height': FRAME_H, 'children': zorder},
          open(f'.figma-ref/frame{FRAME}-zorder.json', 'w'), indent=1)
json.dump({'frame': FRAME_ID, 'scale': 2, 'assetDir': 'src/assets/', 'nodes': nodes},
          open(f'.figma-ref/frame{FRAME}-assets.json', 'w'), indent=1)

from collections import Counter
c = Counter(r['section'] for r in zorder)
ca = Counter(nodes[i]['asset'].split('/')[0] for i in nodes)
for n, _ in BANDS:
    print(f"{n:9} nodes={c[n]:3}  assets={ca[n]:3}")
print('total assets', len(nodes))
