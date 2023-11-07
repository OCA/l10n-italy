# Copyright 2023 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    view_refs = [
        "l10n_it_sdi_channel.view_fatturapa_out_attachment_form",
        "l10n_it_sdi_channel.view_invoice_form_fatturapa",
    ]
    for view in view_refs:
        env.ref(view).unlink()
