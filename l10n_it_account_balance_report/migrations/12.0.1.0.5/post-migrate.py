#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    unaffected_type = env.ref('account.data_unaffected_earnings')
    unaffected_type.update({
        'account_balance_report_section': 'liabilities',
    })
