#!/usr/bin/env python3
"""Flatten a Figma frame's raw node dump into the leaf list build_refs.py consumes.

`get_node` on a 268-node frame is too large to read into context, so the MCP writes it to
a file; this reads that file and emits one row per LEAF, in global paint order.

    python3 scripts/flatten_frame.py .figma-tmp/frame<N>-node.json .figma-tmp/frame<N>-flat.json

See build_refs.py for why the walk looks the way it does (bottom-first children, and the
GROUP/FRAME coordinate-space split).
"""
import json
import sys

src, out = sys.argv[1], sys.argv[2]
flat = []


def walk(node, ox=0, oy=0):
    for c in node.get("children", []):
        b = c["bounds"]
        x, y = b["x"] + ox, b["y"] + oy
        if c.get("children"):
            # A FRAME opens a new coordinate space for its descendants; a GROUP does not
            # -- a group's children report coordinates in the group's OWN space, which is
            # its nearest FRAME ancestor's. Resetting to (0, 0) for a GROUP is only right
            # when the group sits at the top level; nested inside a frame it silently
            # drops that frame's offset and lands the subtree at the top of the sheet.
            walk(c, *((x, y) if c["type"] == "FRAME" else (ox, oy)))
            continue
        flat.append(
            dict(z=len(flat) + 1, id=c["id"], name=c["name"], type=c["type"],
                 x=round(x, 2), y=round(y, 2),
                 w=round(b["width"], 2), h=round(b["height"], 2))
        )


walk(json.load(open(src)))
json.dump(flat, open(out, "w"), indent=1)
print(f"{len(flat)} leaves -> {out}")
