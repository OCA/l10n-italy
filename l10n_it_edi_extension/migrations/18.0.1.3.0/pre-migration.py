#  Copyright 2026 Nextev Srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE l10n_it_edi_line_other_data
        ALTER COLUMN date_ref TYPE date
        USING date_ref::date
        """,
    )
