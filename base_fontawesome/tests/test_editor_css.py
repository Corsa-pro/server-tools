# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import importlib.util
import pathlib
import re

from odoo.tests import TransactionCase, tagged
from odoo.tools.misc import file_open, file_path

EDITOR_CSS = "base_fontawesome/static/src/css/fontawesome_editor.css"


RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")


def rule(css, name):
    """The declarations of the rule holding ``.fa-<name>::before``."""
    for selectors, body in RULE.findall(css):
        if f".fa-{name}::before" in (part.strip() for part in selectors.split(",")):
            return body
    return ""


@tagged("post_install", "-at_install")
class TestEditorCss(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        with file_open(EDITOR_CSS) as css_file:
            cls.css = css_file.read()

    def test_loaded_in_the_backend(self):
        paths = [
            asset[0]
            for asset in self.env["ir.asset"]._get_asset_paths("web.assets_backend", {})
        ]
        self.assertIn(f"/{EDITOR_CSS}", paths)

    def test_names_and_aliases_share_their_icon(self):
        self.assertIn('content: "\\f002";', rule(self.css, "search"))
        self.assertEqual(rule(self.css, "magnifying-glass"), rule(self.css, "search"))

    def test_v4_names_keep_their_v4_icon(self):
        # Font Awesome 6 redefines "repeat"; "fa fa-repeat" still draws the
        # v4 icon through v4-shims.css.
        self.assertIn('content: "\\f01e";', rule(self.css, "repeat"))
        self.assertIn('content: "\\f000";', rule(self.css, "glass"))

    def test_up_to_date_with_the_bundled_font_awesome(self):
        script = pathlib.Path(file_path("base_fontawesome/scripts/build_editor_css.py"))
        spec = importlib.util.spec_from_file_location("build_editor_css", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        (lib,) = sorted((script.parent.parent / "static/lib").glob("fontawesome-*"))
        content, _names, _glyphs = module.build(lib)
        self.assertEqual(content, self.css, "Run scripts/build_editor_css.py")
