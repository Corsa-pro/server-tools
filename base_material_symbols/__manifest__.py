# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Material Symbols",
    "summary": "All 4,000 Google Material Symbols, with Odoo 20's icon markup",
    "version": "19.0.1.0.0",
    "development_status": "Beta",
    "category": "Hidden/Tools",
    "website": "https://github.com/OCA/server-tools",
    "author": "CORSA.pro,Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
    "depends": ["base_setup", "web"],
    "data": [
        "views/res_config_settings_views.xml",
        "views/webclient_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "base_material_symbols/static/src/scss/material_symbols.scss",
            "base_material_symbols/static/src/js/material_symbols.esm.js",
            "base_material_symbols/static/src/js/material_symbols_style.esm.js",
        ],
        "web.assets_frontend": [
            "base_material_symbols/static/src/scss/material_symbols.scss",
        ],
        "web.assets_unit_tests": [
            "base_material_symbols/static/tests/**/*",
        ],
    },
}
