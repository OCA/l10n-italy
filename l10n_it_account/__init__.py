# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models
from . import wizards
from . import tools
from odoo import api, SUPERUSER_ID


def _l10n_it_account_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["account.account"].set_account_types_negative_sign()

    lang = env["res.lang"]
    if lang._lang_get("it_IT"):
        lang.update_menu_finance_it_translation()
