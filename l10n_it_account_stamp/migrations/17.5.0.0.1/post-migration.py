#  Copyright 2024 Sergio Zanchetta
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.load_data(env.cr, "l10n_it_account_stamp", "17.5.0.0.1/noupdate_changes.xml")
    openupgrade.delete_record_translations(env.cr, "l10n_it_account_stamp", ["l10n_it_account_stamp_2_euro"])
