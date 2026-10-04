#!/usr/bin/env python3
# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
"""Rebuild the Material Symbols files shipped in static/lib/material_symbols/.

Downloads Google's three variable Material Symbols fonts (Outlined, Rounded
and Sharp) at a pinned commit of https://github.com/google/material-design-icons,
fixes their weight (400), grade (0) and optical size (24) the way Odoo 20 does,
keeps the FILL axis (the ``oi-filled`` class), and writes:

* ``material_symbols_<style>.woff2``: one font per style; a browser only
  downloads the style in use. Every browser Odoo supports reads WOFF2;
* ``symbols.json``: every icon name, with its aliases, for pickers and checks.
  The three styles have the same icons: the script stops if they do not;
* ``SOURCE.md``: where and how the files were made.

This is a maintainer tool, not part of the module at run time. It needs
``fonttools`` and ``brotli``, which Odoo does not::

    python3 -m venv /tmp/msvenv && /tmp/msvenv/bin/pip install fonttools brotli
    /tmp/msvenv/bin/python scripts/build_font.py [--commit SHA]
"""

import argparse
import json
import pathlib
import sys
import tempfile
import urllib.request
from collections import defaultdict

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

COMMIT = "737e3324305806514d7909874fa1818ae1808232"
REPOSITORY = "https://github.com/google/material-design-icons"
RAW = "https://raw.githubusercontent.com/google/material-design-icons/{commit}/{path}"
STYLES = ("Outlined", "Rounded", "Sharp")
SOURCE = "variablefont/MaterialSymbols{style}%5BFILL,GRAD,opsz,wght%5D.{ext}"
# Odoo 20 pins the same values for its own Material Symbols subset.
AXES = {"wght": 400, "GRAD": 0, "opsz": 24}
OUT = pathlib.Path(__file__).resolve().parent.parent / "static/lib/material_symbols"


def download(commit, path, target):
    url = RAW.format(commit=commit, path=path)
    with urllib.request.urlopen(url, timeout=120) as response:  # noqa: S310
        target.write_bytes(response.read())


def build_font(source, target):
    font = TTFont(source)
    instancer.instantiateVariableFont(font, AXES, inplace=True)
    font.flavor = "woff2"
    font.save(target)
    return target.stat().st_size


def build_symbols(codepoints_file, commit):
    """Group the names by glyph: one entry per icon, its other names aliases."""
    names_by_codepoint = defaultdict(list)
    for line in codepoints_file.read_text().splitlines():
        if line.strip():
            name, codepoint = line.split()
            names_by_codepoint[codepoint].append(name)
    symbols = []
    for codepoint, names in names_by_codepoint.items():
        names.sort()
        entry = {"name": names[0], "codepoint": codepoint}
        if names[1:]:
            entry["aliases"] = names[1:]
        symbols.append(entry)
    symbols.sort(key=lambda entry: entry["name"])
    return {
        "source": {"repository": REPOSITORY, "commit": commit},
        "symbols": symbols,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--commit", default=COMMIT, help="material-design-icons commit")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    sizes = {}
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        codepoints = {}
        for style in STYLES:
            font = tmp / f"{style}.woff2"
            codepoints[style] = tmp / f"{style}.codepoints"
            download(args.commit, SOURCE.format(style=style, ext="woff2"), font)
            download(
                args.commit,
                SOURCE.format(style=style, ext="codepoints"),
                codepoints[style],
            )
            target = OUT / f"material_symbols_{style.lower()}.woff2"
            sizes[target.name] = build_font(font, target)
        reference = codepoints[STYLES[0]].read_text().split()
        for style in STYLES[1:]:
            if codepoints[style].read_text().split() != reference:
                raise SystemExit(f"{style} does not have the icons of {STYLES[0]}")
        download(args.commit, "LICENSE", OUT / "LICENSE")
        data = build_symbols(codepoints[STYLES[0]], args.commit)
    (OUT / "symbols.json").write_text(json.dumps(data, separators=(",", ":")) + "\n")
    axes = ", ".join(f"{tag}={value}" for tag, value in AXES.items())
    names = sum(1 + len(s.get("aliases", [])) for s in data["symbols"])
    files = "\n".join(f"- `{name}`: {size} bytes." for name, size in sizes.items())
    (OUT / "SOURCE.md").write_text(
        f"""# Material Symbols

Built by `scripts/build_font.py` from
{REPOSITORY}/tree/{args.commit}
(`variablefont/MaterialSymbols{{Outlined,Rounded,Sharp}}[FILL,GRAD,opsz,wght]`),
under the Apache License 2.0 (`LICENSE` in this folder).

- Axes fixed: {axes}. The FILL axis is kept.
- {len(data["symbols"])} icons, {names} names (`symbols.json`), the same in
  every style.
{files}
"""
    )
    sys.stdout.write(f"{len(data['symbols'])} icons; {sizes}\n")


if __name__ == "__main__":
    main()
