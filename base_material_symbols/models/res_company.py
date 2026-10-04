# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models

# The three styles of the font, as Google names them. The default style is
# not marked on the page: the stylesheet falls back to it.
MATERIAL_SYMBOLS_STYLES = [
    ("outlined", "Outlined"),
    ("rounded", "Rounded"),
    ("sharp", "Sharp"),
]
DEFAULT_STYLE = "outlined"


class ResCompany(models.Model):
    _inherit = "res.company"

    material_symbols_style = fields.Selection(
        MATERIAL_SYMBOLS_STYLES,
        string="Icon Style",
        required=True,
        default=DEFAULT_STYLE,
        help="How Material Symbols icons look for this company: Outlined, "
        "Rounded or Sharp.",
    )
