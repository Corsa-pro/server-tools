* PDF reports: wkhtmltopdf does not apply font ligatures, so
  `data-icon` markup does not draw in reports yet. The PNG route draws any
  symbol; turning report markup into those images is not done yet.
* Odoo 20's `oi_*` icon names (Odoo UI Icons) are not mapped on Odoo 19.
* Weight, grade and optical size are fixed (400, 0, 24 px), as in Odoo 20.

**Updating the font.** `scripts/build_font.py` downloads Google's three fonts
at a pinned commit of https://github.com/google/material-design-icons, fixes
their axes and rewrites `static/lib/material_symbols/`. It needs `fonttools` and
`brotli`, which are not Odoo dependencies; see the script's docstring. Bump
the commit in the script, run it, and review `SOURCE.md` and the size of the
files in the diff.
