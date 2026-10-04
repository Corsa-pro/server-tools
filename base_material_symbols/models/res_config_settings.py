# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    material_symbols_style = fields.Selection(
        related="company_id.material_symbols_style",
        readonly=False,
    )
