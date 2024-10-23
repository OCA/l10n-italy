# Copyright 2023 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade

from odoo.addons.l10n_it_delivery_note_base import post_init_hook


@openupgrade.migrate()
def migrate(env, version):
    # delete only xml ir.sequence reference in model data due to change
    # into via code creation for every company
    deleted_dn_seq_data = (
        "delivery_note_sequence_ddt_incoming",
        "delivery_note_sequence_ddt",
        "delivery_note_sequence_ddt_internal",
    )
    openupgrade.logged_query(
        env.cr,
        f"""
            DELETE FROM ir_model_data
            WHERE module='l10n_it_delivery_note_base'
            AND model='ir.sequence'
            AND name IN {deleted_dn_seq_data}
        """,
    )

    # delete only stock.delivery.note.type xml in model data due to change
    # into via code creation for every company
    deleted_dn_type_data = (
        "delivery_note_type_incoming_ddt",
        "delivery_note_type_ddt",
        "delivery_note_type_priced_ddt",
        "delivery_note_type_internal_ddt",
    )
    openupgrade.logged_query(
        env.cr,
        f"""
            DELETE FROM ir_model_data
            WHERE module='l10n_it_delivery_note_base'
            AND model='stock.delivery.note.type'
            AND name IN {deleted_dn_type_data}
        """,
    )
    post_init_hook(env.cr, env)
