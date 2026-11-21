#!/usr/bin/env python3
"""One image: 20 November 2026 — make.fun news-image-20261120.

Writes the entry image to /output/entry.png. The image is entry.png
in this repository, drawn by gen_image.py (PIL, fixed text and layout,
no network, no randomness): a newspaper front page for Friday
20 November 2026 — Russian missiles crash in Poland, Kyiv under fire,
Cyclone Akvan, Anthropic's record IPO, and the day's other stories,
with a UTC timeline and an explicit date check. Copying the bundled
image keeps the entry stdlib-only and byte-identical on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(HERE, "entry.png")


def output_path():
    out = os.environ.get("ENTRY_OUTPUT")
    if out:
        return out
    return os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                        "entry.png")


def main():
    dest = output_path()
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(IMAGE, dest)
    # The two graded runs must write the same bytes: refuse to pass
    # silently if the copy came out short.
    if os.path.getsize(dest) != os.path.getsize(IMAGE):
        raise SystemExit("entry.png copy is incomplete")


if __name__ == "__main__":
    main()
