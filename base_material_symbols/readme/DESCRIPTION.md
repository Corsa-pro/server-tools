Adds Google's complete **Material Symbols** icon set to Odoo: about 4,000
icons, against the 482 that Odoo 20 ships and none in Odoo 19.

Icons are written the way Odoo 20 writes them:

```xml
<i class="oi" data-icon="sports_motorsports"/>
<i class="oi oi-filled oi-lg" data-icon="flag"/>
```

- **On Odoo 19** this markup works as it will on 20, so modules written now
  keep working after the upgrade. Odoo 19's own icons (`oi oi-search`, Font
  Awesome) are untouched.
- **On Odoo 20** the complete font takes the place of Odoo's 482-icon subset
  under the same name, so every Material Symbol works everywhere Odoo 20
  draws icons, including `icon="..."` on buttons.

The font comes in Google's three styles, **Outlined, Rounded and Sharp**,
at weight 400, grade 0 and 24 px optical size as in Odoo 20, with their fill
axis (`oi-filled`). Each company chooses its style; with
`website_material_symbols`, each website can choose its own. A browser only
downloads the style in use (440 to 540 KB in WOFF2), once, and only on pages
that draw a symbol.

For other modules the module also provides:

- the list of icon names with their aliases
  (`static/lib/material_symbols/symbols.json`);
- in Python, `is_material_symbol(name)` and `symbol_names()` from
  `odoo.addons.base_material_symbols.tools`, to validate a name;
- in JavaScript, `loadMaterialSymbols()` from
  `@base_material_symbols/js/material_symbols.esm`;
- a "Material Symbols" tab in the icon picker of `web_widget_icon_picker`,
  when that module is installed (neither module depends on the other);
- a PNG of any symbol, for places that cannot load the font, such as
  emails: `/base_material_symbols/icon/<style>/<fill>/<name>/<color>/<background>/<width>x<height>`,
  colors URL-encoded (`rgb(113%2C%2075%2C%20103)`, `rgba(...)` or a hex code).

**HTML fields.** Odoo 19's HTML sanitizer drops the attributes it does not
know, `data-icon` among them, so Material Symbols vanished from HTML fields
and chatter messages when saved. The module allows `data-icon`, as Odoo 20
does.

**Companion modules**, each installed automatically with its apps:

- `website_material_symbols`: a style per website;
- `html_editor_material_symbols`: Material Symbols in the editor's Icons tab
  (website builder, HTML fields);
- `mail_material_symbols`: symbols sent as images in emails;
- `mass_mailing_material_symbols`: the same in Email Marketing.
