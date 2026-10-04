# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import HttpCase, new_test_user, tagged


def hoot_id(name):
    """Hoot's id of a test suite, computed as web's HOOTCommon does."""
    value = 0
    for char in name:
        value = ((value << 5) - value + ord(char)) & 0xFFFFFFFF
    return f"{value:08x}"


@tagged("post_install", "-at_install")
class TestJs(HttpCase):
    def test_unit_tests(self):
        """The module's browser unit tests (static/tests), headless."""
        # Own login: dev databases are production copies, without "admin".
        # partner_email_check (when installed) would refuse the generated
        # test address; the key is ignored everywhere else.
        new_test_user(
            self.env,
            login="base_material_symbols_js",
            groups="base.group_user",
            email="base.material.symbols.js@corsa.pro",
            context={"partner_email_check_skip_syntax": True},
        )
        self.browser_js(
            "/web/tests?headless&loglevel=2&preset=desktop&timeout=15000"
            f"&id={hoot_id('@base_material_symbols')}",
            "",
            "",
            login="base_material_symbols_js",
            timeout=1800,
            success_signal="[HOOT] Test suite succeeded",
            error_checker=lambda message: "[HOOT]" not in message,
        )
