# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from io import BytesIO
from urllib.parse import quote

from PIL import Image

from odoo.tests import HttpCase, TransactionCase, tagged
from odoo.tools import html_sanitize

from ..tools import material_symbols, symbol_codepoint


def icon_url(name, style="outlined", fill=0, size=48):
    # Colors encoded as the email conversion does (encodeURIComponent).
    color = quote("rgb(113, 75, 103)", safe="")
    background = quote("rgba(0, 0, 0, 0)", safe="")
    return (
        f"/base_material_symbols/icon/{style}/{fill}/{name}"
        f"/{color}/{background}/{size}x{size}"
    )


def ink(image):
    return sum(1 for pixel in image.getdata() if pixel[3] > 128)


@tagged("post_install", "-at_install")
class TestIconImages(HttpCase):
    def png(self, url):
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "image/png")
        return Image.open(BytesIO(response.content))

    def test_an_icon_is_drawn_in_its_color(self):
        image = self.png(icon_url("local_shipping"))
        self.assertEqual(image.size, (48, 48))
        self.assertGreater(ink(image), 100)
        drawn = {pixel[:3] for pixel in image.getdata() if pixel[3] == 255}
        self.assertIn((113, 75, 103), drawn)

    def test_filled_and_every_style(self):
        outlined = ink(self.png(icon_url("local_shipping")))
        self.assertGreater(ink(self.png(icon_url("local_shipping", fill=1))), outlined)
        for style in ("rounded", "sharp"):
            self.assertGreater(ink(self.png(icon_url("local_shipping", style))), 100)

    def test_aliases_draw_their_icon(self):
        symbol = next(symbol for symbol in material_symbols() if symbol.get("aliases"))
        alias = symbol["aliases"][0]
        self.assertEqual(symbol_codepoint(alias), symbol_codepoint(symbol["name"]))
        self.assertGreater(ink(self.png(icon_url(alias))), 0)

    def test_unknown_icon_or_style(self):
        for url in (icon_url("no_such_icon"), icon_url("flag", style="bold")):
            self.assertEqual(self.url_open(url).status_code, 404)


@tagged("post_install", "-at_install")
class TestSanitizer(TransactionCase):
    def test_data_icon_is_kept(self):
        html = html_sanitize(
            '<p><i class="oi oi-filled" data-icon="flag"></i></p>',
            sanitize_attributes=True,
        )
        self.assertIn('data-icon="flag"', html)

    def test_html_fields_keep_material_symbols(self):
        partner = self.env["res.partner"].create(
            {"name": "Icons", "comment": '<p><i class="oi" data-icon="flag"></i></p>'}
        )
        self.assertIn('data-icon="flag"', partner.comment)
