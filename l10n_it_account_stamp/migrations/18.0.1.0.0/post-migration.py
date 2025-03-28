#  Copyright 2024 Sergio Zanchetta
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    openupgrade.load_data(
        env, "l10n_it_account_stamp", "migrations/18.0.1.0.0/noupdate_changes.xml"
    )
    openupgrade.delete_record_translations(
        cr, "l10n_it_account_stamp", ["l10n_it_account_stamp_2_euro"]
    )
