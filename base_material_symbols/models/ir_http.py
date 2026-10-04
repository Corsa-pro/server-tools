# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, models

from .res_company import DEFAULT_STYLE


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        """Add each company's icon style.

        The server only knows the user's default company; the company active
        in the browser is known on the client, which picks its style.
        """
        result = super().session_info()
        if self.env.user._is_internal():
            # sudo: a user reads the icon style of the companies they may
            # switch to, nothing else of them.
            companies = (
                self.env["res.company"].sudo().browse(self.env.user._get_company_ids())
            )
            result["material_symbols_styles"] = {
                company.id: company.material_symbols_style
                for company in companies
                if company.material_symbols_style != DEFAULT_STYLE
            }
        return result

    @api.model
    def _material_symbols_frontend_style(self):
        """The icon style of frontend pages, None for the default one.

        The company's here; website_material_symbols lets a website choose
        its own.
        """
        # sudo: visitors read the icon style of the page's company.
        style = self.env.company.sudo().material_symbols_style
        return style if style != DEFAULT_STYLE else None
