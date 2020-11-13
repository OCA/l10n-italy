# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models
from . import tools
from odoo import api, SUPERUSER_ID


def _l10n_it_account_post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["account.account.type"].set_account_types_negative_sign()
