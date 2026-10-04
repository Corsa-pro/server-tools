// Copyright 2026 CORSA.pro (https://www.corsa.pro)
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import {_t} from "@web/core/l10n/translation";
import {browser} from "@web/core/browser/browser";
import {registry} from "@web/core/registry";

/** Every icon of the module: name, codepoint and aliases. */
export const SYMBOLS_URL =
    "/base_material_symbols/static/lib/material_symbols/symbols.json";

let symbolsPromise = null;

/**
 * Load the list of Material Symbols once per page.
 *
 * @returns {Promise<{name: String, codepoint: String, aliases?: String[]}[]>}
 */
export function loadMaterialSymbols() {
    if (!symbolsPromise) {
        symbolsPromise = browser
            .fetch(SYMBOLS_URL)
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Cannot load ${SYMBOLS_URL}: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => data.symbols);
        // A failed load must not stick: let the next call try again.
        symbolsPromise.catch(() => {
            symbolsPromise = null;
        });
    }
    return symbolsPromise;
}

/** Forget the loaded list (tests start from a clean page this way). */
export function clearMaterialSymbolsCache() {
    symbolsPromise = null;
}

/**
 * The Material Symbols tab of the icon picker (web_widget_icon_picker). A
 * plain registry entry: neither module depends on the other, and nothing
 * reads it when the picker is not installed.
 */
registry.category("icon_sets").add("material_symbols", {
    label: _t("Material Symbols"),
    sequence: 10,
    // Drawn filled with the oi-filled class.
    fill: true,
    async load() {
        const symbols = await loadMaterialSymbols();
        return symbols.map(({name, aliases}) => ({
            value: name,
            name,
            aliases: aliases || [],
        }));
    },
});
