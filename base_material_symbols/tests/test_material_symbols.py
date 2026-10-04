# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import TransactionCase, tagged
from odoo.tools.misc import file_path

from ..tools import is_material_symbol, material_symbols, symbol_names


@tagged("post_install", "-at_install")
class TestMaterialSymbols(TransactionCase):
    def test_every_icon_is_listed_once_by_name(self):
        symbols = material_symbols()
        names = [symbol["name"] for symbol in symbols]
        self.assertGreaterEqual(len(symbols), 3999)
        self.assertEqual(names, sorted(names))
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(
            len({symbol["codepoint"] for symbol in symbols}),
            len(symbols),
            "one entry per glyph",
        )

    def test_names_and_aliases(self):
        for name in ("flag", "sports_motorsports", "local_gas_station", "warehouse"):
            self.assertTrue(is_material_symbol(name), name)
        aliased = next(symbol for symbol in material_symbols() if symbol.get("aliases"))
        for alias in aliased["aliases"]:
            self.assertIn(alias, symbol_names())
            self.assertTrue(is_material_symbol(alias))

    def test_unknown_names(self):
        for name in ("", None, "not_an_icon", "oi-search", "Flag", "oi_odoo"):
            self.assertFalse(is_material_symbol(name), name)

    def test_files_are_shipped(self):
        folder = "base_material_symbols/static/lib/material_symbols/"
        for name in (
            "material_symbols_outlined.woff2",
            "material_symbols_rounded.woff2",
            "material_symbols_sharp.woff2",
            "LICENSE",
            "SOURCE.md",
        ):
            self.assertTrue(file_path(folder + name), name)
