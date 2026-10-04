// Copyright 2026 CORSA.pro (https://www.corsa.pro)
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import {session} from "@web/session";
import {user} from "@web/core/user";

/**
 * Draw the Material Symbols in the style of the active company. The server
 * sends every company's style that is not the default one; only the browser
 * knows which company is active. Switching company reloads the page.
 *
 * @param {Object} [styles] style by company id
 * @param {Number} [companyId]
 * @param {HTMLElement} [root]
 */
export function applyMaterialSymbolsStyle(
    styles = session.material_symbols_styles,
    companyId = user.activeCompany?.id,
    root = document.documentElement
) {
    const style = styles?.[companyId];
    if (style) {
        root.dataset.materialSymbols = style;
    } else {
        delete root.dataset.materialSymbols;
    }
}

applyMaterialSymbolsStyle();
