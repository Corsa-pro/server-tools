// Copyright 2026 CORSA.pro (https://www.corsa.pro)
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import {
    SYMBOLS_URL,
    clearMaterialSymbolsCache,
    loadMaterialSymbols,
} from "@base_material_symbols/js/material_symbols.esm";
import {afterEach, describe, expect, getFixture, test} from "@odoo/hoot";
import {applyMaterialSymbolsStyle} from "@base_material_symbols/js/material_symbols_style.esm";
import {browser} from "@web/core/browser/browser";
import {patchWithCleanup} from "@web/../tests/web_test_helpers";
import {registry} from "@web/core/registry";

const SYMBOLS = [
    {name: "directions_car", codepoint: "e531"},
    {name: "emoji_flags", codepoint: "ea1a"},
    {name: "ev_station", codepoint: "e56d"},
    {name: "flag", codepoint: "e153"},
    {name: "flag_circle", codepoint: "eaf8"},
    {name: "local_gas_station", codepoint: "e546"},
    {name: "local_shipping", codepoint: "e558", aliases: ["lorry"]},
];

function names(symbols) {
    return symbols.map(({name}) => name);
}

describe("markup", () => {
    test("data-icon draws a Material Symbol; Odoo 19's own icons keep their font", () => {
        const fixture = getFixture();
        fixture.innerHTML = `
            <i class="oi" data-icon="flag"></i>
            <i class="oi oi-search"></i>
            <i class="oi oi-filled" data-icon="star"></i>`;
        const [symbol, odooIcon, filled] = fixture.querySelectorAll("i");
        expect(getComputedStyle(symbol).fontFamily).toInclude(
            "Material Symbols Outlined"
        );
        expect(getComputedStyle(symbol, "::before").content).toBe('"flag"');
        expect(getComputedStyle(odooIcon).fontFamily).toInclude("odoo_ui_icons");
        expect(getComputedStyle(odooIcon).fontFamily).not.toInclude("Material Symbols");
        expect(getComputedStyle(filled).fontVariationSettings).toInclude("FILL");
    });

    test("a symbol is 1em wide even before the font has loaded", () => {
        const fixture = getFixture();
        fixture.innerHTML = `<i class="oi" data-icon="sports_motorsports"></i>`;
        const before = getComputedStyle(fixture.querySelector("i"), "::before");
        expect(before.width).toBe(before.fontSize);
        expect(before.overflow).toBe("hidden");
    });

    test("Odoo 20's size helpers exist", () => {
        const fixture = getFixture();
        fixture.innerHTML = `<div style="font-size: 10px"><i class="oi oi-2x" data-icon="flag"></i></div>`;
        expect(getComputedStyle(fixture.querySelector("i")).fontSize).toBe("20px");
    });
});

describe("style", () => {
    afterEach(() => {
        delete document.documentElement.dataset.materialSymbols;
    });

    test("the active company's style is set on the page", () => {
        applyMaterialSymbolsStyle({3: "rounded", 4: "sharp"}, 4);
        expect(document.documentElement).toHaveAttribute(
            "data-material-symbols",
            "sharp"
        );
        // Outlined, the default, is not sent: nothing is set.
        applyMaterialSymbolsStyle({3: "rounded"}, 4);
        expect(document.documentElement).not.toHaveAttribute("data-material-symbols");
    });

    test("the page's style picks the font", () => {
        const fixture = getFixture();
        fixture.innerHTML = `<i class="oi" data-icon="flag"></i>`;
        const icon = fixture.querySelector("i");
        for (const style of ["Rounded", "Sharp"]) {
            document.documentElement.dataset.materialSymbols = style.toLowerCase();
            expect(getComputedStyle(icon).fontFamily).toInclude(
                `Material Symbols ${style}`
            );
        }
    });
});

describe("loading", () => {
    afterEach(clearMaterialSymbolsCache);

    test("the list is fetched once per page", async () => {
        patchWithCleanup(browser, {
            fetch: async (url) => {
                expect.step(url);
                return new Response(JSON.stringify({symbols: SYMBOLS}));
            },
        });
        expect(names(await loadMaterialSymbols())).toEqual(names(SYMBOLS));
        await loadMaterialSymbols();
        expect.verifySteps([SYMBOLS_URL]);
    });

    test("a failed load is retried on the next call", async () => {
        let fail = true;
        patchWithCleanup(browser, {
            fetch: async () => {
                if (fail) {
                    return new Response("", {status: 500});
                }
                return new Response(JSON.stringify({symbols: SYMBOLS}));
            },
        });
        await expect(loadMaterialSymbols()).rejects.toThrow(/500/);
        fail = false;
        expect(await loadMaterialSymbols()).toHaveLength(SYMBOLS.length);
    });

    test("the icon picker gets a Material Symbols set, which can be filled", async () => {
        patchWithCleanup(browser, {
            fetch: async () => new Response(JSON.stringify({symbols: SYMBOLS})),
        });
        const set = registry.category("icon_sets").get("material_symbols");
        expect(set.fill).toBe(true);
        const icons = await set.load();
        expect(icons.find(({value}) => value === "local_shipping")).toEqual({
            value: "local_shipping",
            name: "local_shipping",
            aliases: ["lorry"],
        });
        expect(icons).toHaveLength(SYMBOLS.length);
    });
});
