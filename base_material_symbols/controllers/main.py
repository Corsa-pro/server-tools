# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import io
import re
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont

from odoo import http
from odoo.http import request
from odoo.tools.misc import file_path

from ..models.res_company import MATERIAL_SYMBOLS_STYLES
from ..tools import symbol_codepoint

FONT = (
    "base_material_symbols/static/lib/material_symbols/material_symbols_{style}.woff2"
)
STYLES = frozenset(style for style, _label in MATERIAL_SYMBOLS_STYLES)
MAX_SIZE = 512
COLOR_RE = re.compile(
    r"^rgba?\((\d+),(\d+),(\d+)(?:,([\d.]+))?\)$|^#?([0-9a-f]{6})([0-9a-f]{2})?$",
    re.IGNORECASE,
)


def parse_color(value, default):
    """An RGBA tuple from "rgb(r,g,b)", "rgba(r,g,b,a)" or a hex code."""
    match = COLOR_RE.match((value or "").replace(" ", ""))
    if not match:
        return default
    red, green, blue, alpha, hex_rgb, hex_alpha = match.groups()
    if hex_rgb:
        rgb = tuple(int(hex_rgb[i : i + 2], 16) for i in (0, 2, 4))
        return (*rgb, int(hex_alpha, 16) if hex_alpha else 255)
    opacity = float(alpha) if alpha is not None else 1.0
    return (
        min(int(red), 255),
        min(int(green), 255),
        min(int(blue), 255),
        round(max(0.0, min(opacity, 1.0)) * 255),
    )


@lru_cache(maxsize=len(STYLES))
def font_data(style):
    with open(file_path(FONT.format(style=style)), "rb") as font_file:
        return font_file.read()


def render_icon(style, codepoint, fill, color, background, width, height):
    """A PNG of the symbol, as large as fits in width x height."""
    font = ImageFont.truetype(io.BytesIO(font_data(style)), min(width, height))
    font.set_variation_by_axes([1 if fill else 0])
    glyph = chr(codepoint)
    left, top, right, bottom = font.getbbox(glyph)
    image = Image.new("RGBA", (width, height), background)
    ImageDraw.Draw(image).text(
        ((width - (right - left)) / 2 - left, (height - (bottom - top)) / 2 - top),
        glyph,
        font=font,
        fill=color,
    )
    output = io.BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


class MaterialSymbolsController(http.Controller):
    @http.route(
        "/base_material_symbols/icon/<string:style>/<int:fill>/<string:name>"
        "/<string:color>/<string:background>/<int:width>x<int:height>",
        type="http",
        auth="none",
        readonly=True,
    )
    def icon(self, style, fill, name, color, background, width, height):
        """A Material Symbol as a PNG image, for emails: mail clients do not
        load icon fonts. Images in sent emails keep pointing here, so the URL
        must stay stable.
        """
        codepoint = symbol_codepoint(name)
        if style not in STYLES or codepoint is None:
            raise request.not_found()
        width = max(1, min(width, MAX_SIZE))
        height = max(1, min(height, MAX_SIZE))
        image = render_icon(
            style,
            codepoint,
            fill,
            parse_color(color, (0, 0, 0, 255)),
            parse_color(background, (255, 255, 255, 0)),
            width,
            height,
        )
        return request.make_response(
            image,
            headers=[
                ("Content-Type", "image/png"),
                ("Cache-Control", "public, max-age=604800"),
            ],
        )
