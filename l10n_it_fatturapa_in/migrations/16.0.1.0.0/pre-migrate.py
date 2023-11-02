#  Copyright 2023 Nextev Srl
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    view = env.ref("l10n_it_fatturapa_in.view_fatturapa_in_attachment_form")
    view.inherit_id = False
