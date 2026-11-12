# Copyright 2024-2026 Innovyou srl <http://www.innovyou.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

OLD_MODULE = "l10n_it_fatturapa_out_rf11"
NEW_MODULE = "l10n_it_edi_rf11"


def pre_absorb_old_module(env):
    """Absorb the Odoo 16 module ``l10n_it_fatturapa_out_rf11`` into this one.

    On a v16->v18 upgrade the customer DB still carries the old module and its
    data. Every 74-ter field kept by this module lives on core models under an
    identical column name in both versions:

        res.partner  : is_74ter_agent, agent_74ter_id, invoices_paid_by_agent
        res.company  : payments_74ter_journal_id
        account.move : agent_74ter_id, to_be_paid_by_agent_74ter

    so renaming the module (rather than letting the orphaned v16 module be
    uninstalled/purged, which would DROP those columns) preserves every value
    untouched and merely re-parents the old ``ir_model_data`` to us.

    Runs as ``pre_init_hook`` so it fires *before* our tables/columns are
    touched, on the fresh-install path (``-i``/``-u`` while the old module is
    still present). The twin ``migrations/18.0.1.0.0/pre-migrate.py`` re-calls
    this same function to cover the OpenUpgrade ``apriori.renamed_modules``
    path, where the module record is renamed early and appears as an upgrade
    rather than a fresh install (so the pre_init_hook would not fire).

    NOTE: the company RF11 ``RegimeFiscale`` is intentionally NOT migrated
    here. Core's ``res.company.l10n_it_tax_system`` is already populated from
    the v16 ``fatturapa_fiscal_position.code`` by
    ``l10n_it_edi_extension._l10n_it_fatturapa_post_migration``, which runs
    ahead of us via the dependency chain
    l10n_it_edi_rf11 -> l10n_it_edi_sender_partner -> l10n_it_edi_extension.
    """
    if openupgrade.is_module_installed(env.cr, OLD_MODULE):
        openupgrade.update_module_names(
            env.cr,
            [(OLD_MODULE, NEW_MODULE)],
            merge_modules=True,
        )
