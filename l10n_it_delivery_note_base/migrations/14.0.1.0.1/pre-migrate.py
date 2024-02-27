# Copyright 2023 Nextev Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # delete ir.sequence model data due to change
    # into via code creation for every company
    deleted_dn_seq_data = (
        "l10n_it_delivery_note_base.delivery_note_sequence_ddt_incoming",
        "l10n_it_delivery_note_base.delivery_note_sequence_ddt",
        "l10n_it_delivery_note_base.delivery_note_sequence_ddt_internal",
    )
    openupgrade.delete_records_safely_by_xml_id(env, deleted_dn_seq_data)

    # delete stock.delivery.note.type model data due to change
    # into via code creation for every company
    deleted_dn_type_data = (
        "l10n_it_delivery_note_base.delivery_note_type_incoming_ddt",
        "l10n_it_delivery_note_base.delivery_note_type_ddt",
        "l10n_it_delivery_note_base.delivery_note_type_priced_ddt",
        "l10n_it_delivery_note_base.delivery_note_type_internal_ddt",
    )
    openupgrade.delete_records_safely_by_xml_id(env, deleted_dn_type_data)
