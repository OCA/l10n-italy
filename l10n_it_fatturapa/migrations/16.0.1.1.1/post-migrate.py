#  Copyright 2024 Michele Di Croce - Stesi Consulting srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    fatturapa_attachments = env["fatturapa.attachments"].search([])
    fatturapa_attachments._l10n_it_link_attachments()
