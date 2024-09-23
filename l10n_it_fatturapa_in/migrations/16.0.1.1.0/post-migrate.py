#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    e_invoices_in = env["fatturapa.attachment.in"].search([])
    e_invoices_in._l10n_it_link_attachments()
