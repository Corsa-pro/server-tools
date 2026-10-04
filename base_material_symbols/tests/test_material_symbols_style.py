# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from lxml import etree, html

from odoo import Command
from odoo.tests import HttpCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestMaterialSymbolsStyle(HttpCase):
    def page_style(self, url="/web/login"):
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        return html.fromstring(response.content).get("data-material-symbols")

    def test_companies_start_outlined(self):
        company = self.env["res.company"].create({"name": "Icons Default"})
        self.assertEqual(company.material_symbols_style, "outlined")

    def test_session_info_sends_the_other_styles(self):
        # Own login: dev databases are production copies, without admin/admin.
        # partner_email_check (when installed) would refuse the generated
        # test address; the key is ignored everywhere else.
        user = new_test_user(
            self.env,
            login="material_symbols_style",
            password="material_symbols_style",
            groups="base.group_user",
            email="material.symbols.style@corsa.pro",
            context={"partner_email_check_skip_syntax": True},
        )
        sharp = self.env["res.company"].create(
            {"name": "Icons Sharp", "material_symbols_style": "sharp"}
        )
        user.write({"company_ids": [Command.link(sharp.id)]})
        user.company_id.material_symbols_style = "rounded"
        self.authenticate("material_symbols_style", "material_symbols_style")
        info = self.make_jsonrpc_request("/web/session/get_session_info")
        styles = info["material_symbols_styles"]
        self.assertEqual(styles[str(user.company_id.id)], "rounded")
        self.assertEqual(styles[str(sharp.id)], "sharp")

        user.company_id.material_symbols_style = "outlined"
        info = self.make_jsonrpc_request("/web/session/get_session_info")
        self.assertNotIn(str(user.company_id.id), info["material_symbols_styles"])

    def test_frontend_pages_carry_the_company_style(self):
        companies = self.env["res.company"].search([])
        if (
            "website" in self.env
            and "material_symbols_style" in self.env["website"]._fields
        ):
            # website_material_symbols: an empty website style falls back to
            # its company's.
            self.env["website"].search([]).material_symbols_style = False
        companies.material_symbols_style = "sharp"
        self.assertEqual(self.page_style(), "sharp")
        companies.material_symbols_style = "outlined"
        self.assertIsNone(self.page_style(), "the default style is not marked")

    def test_style_is_a_company_setting(self):
        arch = self.env["res.config.settings"].get_view(view_type="form")["arch"]
        setting = etree.fromstring(arch).xpath(
            "//setting[@id='material_symbols_style_setting']"
        )
        self.assertTrue(setting)
        self.assertEqual(setting[0].get("company_dependent"), "1")
