Write an icon in a view, a QWeb template or an Owl component:

```xml
<i class="oi" data-icon="local_gas_station" title="Fuel"/>
```

Helper classes, as in Odoo 20:

- `oi-filled`: the filled version of the icon;
- sizes `oi-sm`, `oi-lg`, `oi-2x` to `oi-10x`;
- `oi-rotate-90`, `oi-rotate-180`, `oi-rotate-270`, `oi-flip-horizontal`,
  `oi-flip-vertical`;
- `oi-stack`, `oi-stack-1x`, `oi-stack-2x` to stack two icons.

Odoo 19's `oi-fw`, `oi-spin` and `oi-pulse` work on these icons too.

Browse the names at https://fonts.google.com/icons (Material Symbols).
Use the icon's name with underscores, e.g. `directions_car`. The style
(Outlined, Rounded or Sharp) is not part of the markup: it is chosen per
company, and per website.

To validate a name in Python:

```python
from odoo.addons.base_material_symbols.tools import is_material_symbol

if not is_material_symbol(record.icon):
    raise ValidationError(...)
```
