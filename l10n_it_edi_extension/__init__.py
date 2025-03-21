# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import controllers
from . import models
from . import wizards

import os
import base64
from odoo.tools import config

from openupgradelib import openupgrade
from psycopg2 import sql

from odoo.addons.base.models.ir_qweb_fields import Markup, nl2br, nl2br_enclose

OLD_MODULES = [
    "l10n_it_fatturapa",
    "l10n_it_fatturapa_in",
    "l10n_it_fiscalcode",
    "l10n_it_ipa",
    "l10n_it_pec",
    "l10n_it_rea",
]


def rename_fields(env, table, field_updates, condition=None):
    """Generic function to rename fields."""
    set_clauses = sql.SQL(", ").join(
        sql.SQL("{} = {}").format(sql.Identifier(target), sql.Identifier(source))
        for target, source in field_updates.items()
    )
    query = sql.SQL("""
        UPDATE {table}
        SET {set_clauses}
    """).format(table=sql.Identifier(table), set_clauses=set_clauses)
    if condition:
        query += sql.SQL(" WHERE {} ").format(sql.SQL(condition))
    openupgrade.logged_query(env.cr, query)


def update_table(env, target_table, source_table, field_updates, condition):
    """Generic function to update fields in a table based on a join."""
    set_clauses = sql.SQL(", ").join(
        sql.SQL("{} = {}.{}").format(
            sql.Identifier(target), sql.Identifier(source_table), sql.Identifier(source)
        )
        for target, source in field_updates.items()
    )
    query = sql.SQL("""
        UPDATE {target_table}
        SET {set_clauses}
        FROM {source_table}
    """).format(
        target_table=sql.Identifier(target_table),
        set_clauses=set_clauses,
        source_table=sql.Identifier(source_table),
    )
    if condition:
        query += sql.SQL(" WHERE {} ").format(sql.SQL(condition))
    openupgrade.logged_query(env.cr, query)


def _l10n_it_fatturapa_pre_migration(env):
    RENAMED_MODELS = [
        ("fatturapa.activity.progress", "l10n_it_edi.activity_progress"),
        ("fatturapa.summary.data", "l10n_it_edi.summary_data"),
    ]
    RENAMED_TABLES = [
        ("fatturapa_activity_progress", "l10n_it_edi_activity_progress"),
        ("fatturapa_summary_data", "l10n_it_edi_summary_data"),
    ]
    RENAMED_FIELDS = [
        [
            (
                "l10n_it_edi.activity_progress",
                "fatturapa_activity_progress",
            ),
            (
                "l10n_it_edi.activity_progress",
                "activity_progress",
            ),
        ],
        [
            (
                "account.move",
                "protocol_number",
            ),
            (
                "account.move",
                "l10n_it_edi_protocol_number",
            ),
        ],
        [
            (
                "account.move",
                "tax_representative_id",
            ),
            (
                "account.move",
                "l10n_it_edi_tax_representative_id",
            ),
        ],
        [
            (
                "account.move",
                "intermediary",
            ),
            (
                "account.move",
                "l10n_it_edi_intermediary_id",
            ),
        ],
        [
            (
                "account.move",
                "sender",
            ),
            (
                "account.move",
                "l10n_it_edi_sender",
            ),
        ],
        [
            (
                "account.move",
                "fatturapa_summary_ids",
            ),
            (
                "account.move",
                "l10n_it_edi_summary_ids",
            ),
        ],
        [
            (
                "account.move",
                "activity_progress_ids",
            ),
            (
                "account.move",
                "l10n_it_edi_activity_progress_ids",
            ),
        ],
        [
            (
                "account.move",
                "efatt_rounding",
            ),
            (
                "account.move",
                "l10n_it_edi_rounding",
            ),
        ],
        [
            (
                "account.move",
                "art73",
            ),
            (
                "account.move",
                "l10n_it_edi_art73",
            ),
        ],
        [
            (
                "account.move",
                "related_invoice_code",
            ),
            (
                "account.move",
                "l10n_it_edi_related_invoice_code",
            ),
        ],
        [
            (
                "account.move",
                "related_invoice_code",
            ),
            (
                "account.move",
                "l10n_it_edi_related_invoice_code",
            ),
        ],
        [
            (
                "account.move",
                "related_invoice_date",
            ),
            (
                "account.move",
                "l10n_it_edi_related_invoice_date",
            ),
        ],
        [
            (
                "account.move",
                "efatt_stabile_organizzazione_indirizzo",
            ),
            (
                "account.move",
                "l10n_it_edi_stabile_organizzazione_indirizzo",
            ),
        ],
        [
            (
                "account.move",
                "efatt_stabile_organizzazione_civico",
            ),
            (
                "account.move",
                "l10n_it_edi_stabile_organizzazione_civico",
            ),
        ],
        [
            (
                "account.move",
                "efatt_stabile_organizzazione_cap",
            ),
            (
                "account.move",
                "l10n_it_edi_stabile_organizzazione_cap",
            ),
        ],
        [
            (
                "account.move",
                "efatt_stabile_organizzazione_comune",
            ),
            (
                "account.move",
                "l10n_it_edi_stabile_organizzazione_comune",
            ),
        ],
        [
            (
                "account.move",
                "efatt_stabile_organizzazione_provincia",
            ),
            (
                "account.move",
                "l10n_it_edi_stabile_organizzazione_provincia",
            ),
        ],
        [
            (
                "account.move",
                "efatt_stabile_organizzazione_nazione",
            ),
            (
                "account.move",
                "l10n_it_edi_stabile_organizzazione_nazione",
            ),
        ],
        [
            (
                "account.move",
                "efatt_stabile_organizzazione_nazione",
            ),
            (
                "account.move",
                "l10n_it_edi_stabile_organizzazione_nazione",
            ),
        ],
        [
            (
                "account.move.line",
                "admin_ref",
            ),
            (
                "account.move.line",
                "l10n_it_edi_admin_ref",
            ),
        ],
    ]

    openupgrade.rename_models(
        env.cr,
        RENAMED_MODELS,
    )
    openupgrade.rename_tables(
        env.cr,
        RENAMED_TABLES,
    )
    field_spec = []
    for renamed_field in RENAMED_FIELDS:
        (old_model, old_field), (new_model, new_field) = renamed_field
        field_spec.append(
            (
                old_model,
                new_model.replace(".", "_"),
                old_field,
                new_field,
            )
        )
    openupgrade.rename_fields(
        env,
        field_spec,
    )


def _l10n_it_fatturapa_post_migration(env):
    table = "res_partner"
    rename_fields(
        env,
        table,
        {
            "l10n_it_pa_index": "codice_destinatario",
            "l10n_it_pec_email": "pec_destinatario",
        },
    )

    table = "res_company"
    rename_fields(
        env,
        table,
        {"l10n_it_tax_representative_partner_id": "fatturapa_tax_representative"},
    )

    table = "account_move_line"
    rename_fields(
        env,
        table,
        {"sequence": "ftpa_line_number"},
    )

    query = """
        UPDATE res_company
        SET l10n_it_tax_system = fp.code
        FROM res_partner rp
        JOIN fatturapa_fiscal_position fp ON rp.register_fiscalpos = fp.id
        WHERE res_company.partner_id = rp.id AND rp.register_fiscalpos IS NOT NULL
    """
    openupgrade.logged_query(env.cr, query)

    env.cr.execute("""
        UPDATE ir_attachment
        SET res_model = 'account.move', res_id = fa.invoice_id
        FROM fatturapa_attachments fa
        WHERE ir_attachment.id = fa.ir_attachment_id
    """)

    env.cr.execute("""
        SELECT invoice_id, invoice_line_id, name, date, lineRef
        FROM fatturapa_related_ddt
        WHERE invoice_id IS NOT NULL OR invoice_line_id IS NOT NULL
    """)
    rows = env.cr.fetchall()
    invoice_map = {}
    for row in rows:
        invoice_id, invoice_line_id, name, date, lineRef = row
        move_id = (
            invoice_id or env["account.move.line"].browse(invoice_line_id).move_id.id
        )
        if move_id:
            invoice_map.setdefault(move_id, []).append((name, date, lineRef))

    moves = env["account.move"].browse(invoice_map.keys())
    for move in moves:
        for name, date, lineRef in invoice_map[move.id]:
            document_type_tags = Markup('<ul class="mb-0">{}</ul>').format(
                Markup().join(
                    nl2br_enclose(" ".join(tag.split()), "li")
                    for tag in [
                        f"NumeroDDT: {name}",
                        f'DataDDT: {date or "N/A"}',
                        f'LineRef: {lineRef or "N/A"}',
                    ]
                )
            )
            message = Markup("{} {}<br/>{}").format(
                "DatiDDT", env._("from XML file:"), document_type_tags
            )
            move.sudo().message_post(body=message)

    env.cr.execute("""
        SELECT invoice_id, invoice_line_id, type, name, date, code, cig, cup
        FROM fatturapa_related_document_type
        WHERE invoice_id IS NOT NULL OR invoice_line_id IS NOT NULL
    """)
    rows = env.cr.fetchall()
    invoice_map = {}
    for row in rows:
        invoice_id, invoice_line_id, document_type, name, date, code, cig, cup = row
        move_id = (
            invoice_id or env["account.move.line"].browse(invoice_line_id).move_id.id
        )
        if move_id:
            invoice_map.setdefault(move_id, []).append(
                (document_type, name, date, code, cig, cup)
            )

    moves = env["account.move"].browse(invoice_map.keys())
    for move in moves:
        for document_type, name, date, code, cig, cup in invoice_map[move.id]:
            document_type_tags = Markup('<ul class="mb-0">{}</ul>').format(
                Markup().join(
                    nl2br_enclose(" ".join(tag.split()), "li")
                    for tag in [
                        f"IdDocumento: {name}",
                        f'Data: {date or "N/A"}',
                        f'CodiceCommessaConvenzione: {code or "N/A"}',
                        f'CodiceCIG: {cig or "N/A"}',
                        f'CodiceCUP: {cup or "N/A"}',
                    ]
                )
            )
            message = Markup("{} {}<br/>{}").format(
                document_type, env._("from XML file:"), document_type_tags
            )
            move.sudo().message_post(body=message)


def _l10n_it_fatturapa_in_pre_migration(env):
    RENAMED_MODELS = [
        ("einvoice.line", "l10n_it_edi.line"),
        ("fatturapa.article.code", "l10n_it_edi.article_code"),
        ("discount.rise.price", "l10n_it_edi.discount_rise_price"),
        ("einvoice.line.other.data", "l10n_it_edi.line_other_data"),
    ]
    RENAMED_TABLES = [
        ("einvoice_line", "l10n_it_edi_line"),
        ("fatturapa_article_code", "l10n_it_edi_article_code"),
        ("discount_rise_price", "l10n_it_edi_discount_rise_price"),
        ("einvoice_line_other_data", "l10n_it_edi_line_other_data"),
    ]
    RENAMED_FIELDS = [
        [
            (
                "l10n_it_edi.article_code",
                "e_invoice_line_id",
            ),
            (
                "l10n_it_edi.article_code",
                "l10n_it_edi_line_id",
            ),
        ],
        [
            (
                "l10n_it_edi.discount_rise_price",
                "e_invoice_line_id",
            ),
            (
                "l10n_it_edi.discount_rise_price",
                "l10n_it_edi_line_id",
            ),
        ],
        [
            (
                "l10n_it_edi.line_other_data",
                "e_invoice_line_id",
            ),
            (
                "l10n_it_edi.line_other_data",
                "l10n_it_edi_line_id",
            ),
        ],
        [
            (
                "l10n_it_edi.line",
                "cod_article_ids",
            ),
            (
                "l10n_it_edi.line",
                "l10n_it_edi_article_code_ids",
            ),
        ],
        [
            (
                "l10n_it_edi.line",
                "discount_rise_price_ids",
            ),
            (
                "l10n_it_edi.line",
                "l10n_it_edi_discount_rise_price_ids",
            ),
        ],
        [
            (
                "l10n_it_edi.line",
                "other_data_ids",
            ),
            (
                "l10n_it_edi.line",
                "l10n_it_edi_line_other_data_ids",
            ),
        ],
        [
            (
                "account.move",
                "e_invoice_line_ids",
            ),
            (
                "account.move",
                "l10n_it_edi_line_ids",
            ),
        ],
        [
            (
                "account.move",
                "e_invoice_amount_untaxed",
            ),
            (
                "account.move",
                "l10n_it_edi_amount_untaxed",
            ),
        ],
        [
            (
                "account.move",
                "e_invoice_amount_tax",
            ),
            (
                "account.move",
                "l10n_it_edi_amount_tax",
            ),
        ],
        [
            (
                "account.move",
                "e_invoice_amount_total",
            ),
            (
                "account.move",
                "l10n_it_edi_amount_total",
            ),
        ],
    ]

    openupgrade.rename_models(
        env.cr,
        RENAMED_MODELS,
    )
    openupgrade.rename_tables(
        env.cr,
        RENAMED_TABLES,
    )
    field_spec = []
    for renamed_field in RENAMED_FIELDS:
        (old_model, old_field), (new_model, new_field) = renamed_field
        field_spec.append(
            (
                old_model,
                new_model.replace(".", "_"),
                old_field,
                new_field,
            )
        )
    openupgrade.rename_fields(
        env,
        field_spec,
    )


def _l10n_it_fatturapa_in_post_migration(env):
    env.cr.execute("""
        SELECT
            am.id,
            fai.ir_attachment_id AS attachment_id
        FROM account_move am
        JOIN fatturapa_attachment_in fai ON fai.id = am.fatturapa_attachment_in_id
        WHERE am.fatturapa_attachment_in_id IS NOT NULL
    """)
    rows = env.cr.fetchall()
    for row in rows:
        invoice_id, attachment_id = row
        move = env["account.move"].browse(invoice_id)
        attachment = env["ir.attachment"].browse(attachment_id)
        filestore_path = os.path.join(
            config.filestore(env.cr.dbname), attachment.store_fname
        )
        if os.path.exists(filestore_path):
            with open(filestore_path, "rb") as f:
                file_data = base64.b64encode(f.read())
                move.l10n_it_edi_attachment_file = file_data


def _l10n_it_fiscalcode_post_migration(env):
    table = "res_partner"
    condition = "fiscalcode IS NOT NULL"
    condition += " AND LENGTH(TRIM(fiscalcode)) >= 11"
    rename_fields(
        env, table, {"l10n_it_codice_fiscale": "fiscalcode"}, condition=condition
    )


def _l10n_it_ipa_post_migration(env):
    table = "res_partner"
    condition = "ipa_code IS NOT NULL"
    rename_fields(env, table, {"l10n_it_pa_index": "ipa_code"}, condition=condition)


def _l10n_it_pec_post_migration(env):
    table = "res_partner"
    condition = "pec_mail IS NOT NULL"
    rename_fields(env, table, {"l10n_it_pec_email": "pec_mail"}, condition=condition)


def _l10n_it_rea_post_migration(env):
    table = "res_company"
    condition = "res_company.partner_id = res_partner.id"
    condition += " AND res_partner.rea_office IS NOT NULL"
    update_table(
        env,
        table,
        "res_partner",
        {
            "l10n_it_eco_index_office": "rea_office",
            "l10n_it_eco_index_number": "rea_code",
            "l10n_it_eco_index_share_capital": "rea_capital",
            "l10n_it_eco_index_sole_shareholder": "rea_member_type",
            "l10n_it_eco_index_liquidation_state": "rea_liquidation_state",
        },
        condition,
    )


def _l10n_it_edi_extension_pre_init_hook(env):
    for module in OLD_MODULES:
        migration_function = globals().get(f"_{module}_pre_migration")
        if openupgrade.is_module_installed(env.cr, module) and migration_function:
            migration_function(env)


def _l10n_it_edi_extension_post_init_hook(env):
    for module in OLD_MODULES:
        migration_function = globals().get(f"_{module}_post_migration")
        if openupgrade.is_module_installed(env.cr, module) and migration_function:
            migration_function(env)
