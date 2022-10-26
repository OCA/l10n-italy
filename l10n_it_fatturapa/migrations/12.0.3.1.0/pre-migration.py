#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def migrate(cr, installed_version):
    openupgrade.rename_columns(
        cr,
        {
            'res_company': [
                ('phone_electronic_invoice', None),
            ],
        },
    )
