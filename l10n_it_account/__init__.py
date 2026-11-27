# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from . import models
from . import wizards


def _l10n_it_account_post_init(env):
    lang = env["res.lang"]
    if lang._lang_get("it_IT"):
        lang.update_menu_finance_it_translation()
