#  Copyright 2021 Simone Vanin - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


def migrate(cr, installed_version):

    openupgrade.logged_query(
        cr,
        """
update account_move
set
    fiscal_document_type_id = inv.fiscal_document_type_id
from account_invoice inv
where
    account_move.id = inv.move_id;
    """,
    )
