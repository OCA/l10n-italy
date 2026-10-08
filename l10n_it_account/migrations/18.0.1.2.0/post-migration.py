# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo.addons.l10n_it_account.migration_tools import rename_oca_module

# OCA modules renamed with the ``_oca`` suffix
# because Odoo Enterprise provides a module named ``l10n_it_intrastat``.
RENAMED_MODULES = [
    ("l10n_it_intrastat", "l10n_it_intrastat_oca"),
    ("l10n_it_intrastat_statement", "l10n_it_intrastat_statement_oca"),
]


@openupgrade.migrate()
def migrate(env, version):
    for old_module, new_module in RENAMED_MODULES:
        rename_oca_module(env, old_module, new_module)
