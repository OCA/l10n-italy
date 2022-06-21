#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def migrate(cr, version):
    # Move the group and its view from l10n_it_fatturapa_pec
    openupgrade.rename_xmlids(
        cr,
        [
            (
                'l10n_it_fatturapa_pec.group_force_e_inv_export_state',
                'l10n_it_fatturapa_out.group_force_e_inv_export_state',
            ),
            (
                'l10n_it_fatturapa_pec'
                '.view_fatturapa_out_pec_attachment_form_statusbar',
                'l10n_it_fatturapa_out.fatturapa_attachment_out_form_statusbar',
            ),
        ],
    )
