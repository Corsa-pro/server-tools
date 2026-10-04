# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
"""The Material Symbols shipped with the module, for server-side checks.

Other modules use these to validate an icon name before storing it::

    from odoo.addons.base_material_symbols.tools import is_material_symbol
"""

import json
from functools import lru_cache

from odoo.tools.misc import file_path

SYMBOLS_FILE = "base_material_symbols/static/lib/material_symbols/symbols.json"


@lru_cache(maxsize=1)
def material_symbols():
    """Every icon: ``{"name", "codepoint", "aliases"?}``, sorted by name."""
    with open(file_path(SYMBOLS_FILE), encoding="utf-8") as symbols_file:
        return tuple(json.load(symbols_file)["symbols"])


@lru_cache(maxsize=1)
def _codepoints():
    codepoints = {}
    for symbol in material_symbols():
        codepoint = int(symbol["codepoint"], 16)
        for name in (symbol["name"], *symbol.get("aliases", ())):
            codepoints[name] = codepoint
    return codepoints


def symbol_names():
    """Every usable icon name, aliases included."""
    return frozenset(_codepoints())


def symbol_codepoint(name):
    """The font's codepoint for a name or alias, None for an unknown name."""
    return _codepoints().get(name)


def is_material_symbol(name):
    """Whether ``<i class="oi" data-icon="NAME"/>`` draws an icon."""
    return bool(name) and name in symbol_names()
