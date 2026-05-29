#  Copyright 2026 Nextev Srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Reset the sequence after data migrated from einvoice_line with explicit IDs
    openupgrade.logged_query(
        env.cr,
        """
        SELECT setval(
            'l10n_it_edi_line_id_seq',
            (SELECT MAX(id) FROM l10n_it_edi_line)
        )
        """,
    )
