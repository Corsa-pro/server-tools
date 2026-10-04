# Copyright 2026 CORSA.pro (https://www.corsa.pro)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tools import mail

from . import controllers
from . import models
from . import tools

# Keep <i class="oi" data-icon="flag"/> through the HTML sanitizer, as Odoo
# 20 does: most HTML fields drop attributes that are not on this list.
mail.safe_attrs |= {"data-icon"}
