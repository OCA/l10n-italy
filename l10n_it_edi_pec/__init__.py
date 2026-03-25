# Copyright 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2018 Sergio Corato (https://efatto.it)
# Copyright 2018 Lorenzo Battistini <https://github.com/eLBati>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from . import models

from openupgradelib import openupgrade, openupgrade_tools


def _l10n_it_edi_pec_pre_init_hook(env):
    if not openupgrade.is_module_installed(env.cr, "l10n_it_fatturapa_pec"):
        return
    openupgrade.rename_fields(
        env,
        [
            (
                "fetchmail.server",
                "fetchmail_server",
                "is_fatturapa_pec",
                "is_l10n_it_edi_pec",
            ),
            (
                "ir.mail_server",
                "ir_mail_server",
                "is_fatturapa_pec",
                "is_l10n_it_edi_pec",
            ),
            (
                "ir.mail_server",
                "ir_mail_server",
                "email_from_for_fatturaPA",
                "l10n_it_edi_pec_email_from",
            ),
        ],
    )
    # Update ir_model_data for the fetchmail.pec.max.retry parameter
    # so that the new module doesn't create a duplicate
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_model_data
        SET module = 'l10n_it_edi_pec'
        WHERE module = 'l10n_it_fatturapa_pec'
        AND name = 'fetchmail_pec_max_retry'
        """,
    )


def _l10n_it_edi_pec_post_init_hook(env):
    if not openupgrade.is_module_installed(env.cr, "l10n_it_fatturapa_pec"):
        return
    # Migrate PEC settings from sdi.channel to res.company.
    # In v16, PEC settings were stored on sdi.channel records linked
    # to companies via res_company.sdi_channel_id. In v18, they are stored
    # directly on res.company.
    if not openupgrade_tools.table_exists(env.cr, "sdi_channel"):
        return
    if not openupgrade.column_exists(env.cr, "res_company", "sdi_channel_id"):
        return
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_company
        SET
            l10n_it_edi_use_pec = True,
            l10n_it_edi_pec_server_id = sc.pec_server_id,
            l10n_it_edi_pec_fetch_server_id = sc.fetch_pec_server_id,
            l10n_it_edi_pec_email_exchange_system = sc.email_exchange_system
        FROM sdi_channel sc
        WHERE res_company.sdi_channel_id = sc.id
            AND sc.channel_type = 'pec'
        """,
    )
