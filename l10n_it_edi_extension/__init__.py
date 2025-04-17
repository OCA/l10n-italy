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
    "l10n_it_fatturapa_out",
    "l10n_it_fatturapa_sale",
    "l10n_it_fiscal_payment_term",
    "l10n_it_fiscalcode",
    "l10n_it_ipa",
    "l10n_it_pec",
    "l10n_it_rea",
    "l10n_it_vat_payability",
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


def add_field_if_not_exists(env, table, field_name, field_type, module):
    """Helper function to add fields if they do not exist."""
    if not openupgrade.column_exists(env.cr, table, field_name):
        sql_type_mapping = {
            "binary": "bytea",
            "boolean": "bool",
            "char": "varchar",
            "date": "date",
            "datetime": "timestamp",
            "float": "numeric",
            "html": "text",
            "integer": "int4",
            "many2many": False,
            "many2one": "int4",
            "many2one_reference": "int4",
            "monetary": "numeric",
            "one2many": False,
            "reference": "varchar",
            "selection": "varchar",
            "text": "text",
            "serialized": "text",
        }
        openupgrade.add_fields(
            env,
            [
                (
                    field_name,
                    table.replace("_", "."),
                    table,
                    field_type,
                    sql_type_mapping[field_type],
                    module,
                )
            ],
        )


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
                "l10n_edi_it_art73",
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
        [
            (
                "res.partner",
                "eori_code",
            ),
            (
                "res.partner",
                "l10n_edi_it_eori_code",
            ),
        ],
        [
            (
                "res.partner",
                "electronic_invoice_no_contact_update",
            ),
            (
                "res.partner",
                "l10n_edi_it_electronic_invoice_no_contact_update",
            ),
        ],
        [
            (
                "res.partner",
                "register",
            ),
            (
                "res.partner",
                "l10n_edi_it_register",
            ),
        ],
        [
            (
                "res.partner",
                "register_province",
            ),
            (
                "res.partner",
                "l10n_edi_it_register_province",
            ),
        ],
        [
            (
                "res.partner",
                "register_code",
            ),
            (
                "res.partner",
                "l10n_edi_it_register_code",
            ),
        ],
        [
            (
                "res.partner",
                "register_regdate",
            ),
            (
                "res.partner",
                "l10n_edi_it_register_regdate",
            ),
        ],
        [
            (
                "res.company",
                "fatturapa_art73",
            ),
            (
                "res.company",
                "l10n_edi_it_art73",
            ),
        ],
        [
            (
                "res.company",
                "fatturapa_pub_administration_ref",
            ),
            (
                "res.company",
                "l10n_edi_it_admin_ref",
            ),
        ],
        [
            (
                "res.company",
                "fatturapa_sender_partner",
            ),
            (
                "res.company",
                "l10n_edi_it_sender_partner",
            ),
        ],
        [
            (
                "res.company",
                "fatturapa_stabile_organizzazione",
            ),
            (
                "res.company",
                "l10n_edi_it_stable_organization",
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


def _l10n_it_fatturapa_post_migration_related_ddt(env):
    env.cr.execute("""
        SELECT invoice_id, invoice_line_id, name, date
        FROM fatturapa_related_ddt
        WHERE invoice_id IS NOT NULL OR invoice_line_id IS NOT NULL
    """)
    rows = env.cr.fetchall()
    invoice_map = {}
    for row in rows:
        invoice_id, invoice_line_id, name, date = row
        move_id = (
            invoice_id or env["account.move.line"].browse(invoice_line_id).move_id.id
        )
        if move_id:
            invoice_map.setdefault(move_id, []).append((name, date))

    moves = env["account.move"].browse(invoice_map.keys())
    for move in moves:
        for name, date in invoice_map[move.id]:
            ddt_tags = Markup('<ul class="mb-0">{}</ul>').format(
                Markup().join(
                    nl2br_enclose(" ".join(tag.split()), "li")
                    for tag in [
                        f"NumeroDDT: {name}",
                        f'DataDDT: {date or "N/A"}',
                    ]
                )
            )
            message = Markup("{} {}<br/>{}").format(
                "DatiDDT", env._("from XML file:"), ddt_tags
            )
            move.sudo().message_post(body=message)


def _l10n_it_fatturapa_post_migration_delivery_data(env):
    env.cr.execute("""
        SELECT
            am.id AS move_id,
            rp.name AS carrier_name,
            rp.license_number AS license_number,
            am.transport_vehicle,
            am.transport_reason,
            am.number_items,
            am.description,
            am.unit_weight,
            am.gross_weight,
            am.net_weight,
            am.pickup_datetime,
            am.transport_date,
            am.delivery_address,
            am.delivery_datetime,
            am.ftpa_incoterms
        FROM account_move am
        LEFT JOIN res_partner rp ON am.carrier_id = rp.id
    """)
    rows = env.cr.fetchall()
    invoice_map = {}
    for row in rows:
        move_id, *delivery_data = row
        invoice_map.setdefault(move_id, []).append(tuple(delivery_data))

    moves = env["account.move"].browse(invoice_map.keys())
    for move in moves:
        for delivery_data in invoice_map[move.id]:
            (
                carrier_name,
                license_number,
                transport_vehicle,
                transport_reason,
                number_items,
                description,
                unit_weight,
                gross_weight,
                net_weight,
                pickup_datetime,
                transport_date,
                delivery_address,
                delivery_datetime,
                ftpa_incoterms,
            ) = delivery_data
            delivery_tags = Markup('<ul class="mb-0">{}</ul>').format(
                Markup().join(
                    nl2br_enclose(" ".join(tag.split()), "li")
                    for tag in [
                        f'Carrier: {carrier_name or "N/A"}',
                        f'NumeroLicenzaGuida: {license_number or "N/A"}',
                        f'MezzoTrasporto: {transport_vehicle or "N/A"}',
                        f'CausaleTrasporto: {transport_reason or "N/A"}',
                        f'NumeroColli: {number_items or "N/A"}',
                        f'Descrizione: {description or "N/A"}',
                        f'UnitaMisuraPeso: {unit_weight or "N/A"}',
                        f'PesoLordo: {gross_weight or "N/A"}',
                        f'PesoNetto: {net_weight or "N/A"}',
                        f'DataOraRitiro: {pickup_datetime or "N/A"}',
                        f'DataInizioTrasporto: {transport_date or "N/A"}',
                        f'IndirizzoResa: {delivery_address or "N/A"}',
                        f'DataOraConsegna: {delivery_datetime or "N/A"}',
                        f'TipoResa: {ftpa_incoterms or "N/A"}',
                    ]
                )
            )
            message = Markup("{} {}<br/>{}").format(
                "DatiTrasporto", env._("from XML file:"), delivery_tags
            )
            move.sudo().message_post(body=message)


def _l10n_it_fatturapa_post_migration_vehicle_data(env):
    env.cr.execute("""
        SELECT
            id AS move_id,
            vehicle_registration,
            total_travel
        FROM account_move
        WHERE
            vehicle_registration IS NOT NULL
            OR total_travel IS NOT NULL
    """)
    rows = env.cr.fetchall()
    invoice_map = {}
    for row in rows:
        move_id, *vehicle_data = row
        invoice_map.setdefault(move_id, []).append(tuple(vehicle_data))

    moves = env["account.move"].browse(invoice_map.keys())
    for move in moves:
        for vehicle_data in invoice_map[move.id]:
            vehicle_registration, total_travel = vehicle_data
            vehicle_tags = Markup('<ul class="mb-0">{}</ul>').format(
                Markup().join(
                    nl2br_enclose(" ".join(tag.split()), "li")
                    for tag in [
                        f'Data: {vehicle_registration or "N/A"}',
                        f'TotalePercorso: {total_travel or "N/A"}',
                    ]
                )
            )
            message = Markup("{} {}<br/>{}").format(
                "DatiVeicoli", env._("from XML file:"), vehicle_tags
            )
            move.sudo().message_post(body=message)


def _l10n_it_fatturapa_post_migration_payment_data(env):
    env.cr.execute("""
        SELECT
            fpd.invoice_id,
            fpt.code AS term_code,
            fpdl.recipient,
            fpm.code AS method_code,
            fpdl.payment_term_start,
            fpdl.payment_days,
            fpdl.payment_due_date,
            fpdl.payment_amount,
            fpdl.post_office_code,
            fpdl.recepit_surname,
            fpdl.recepit_name,
            fpdl.recepit_cf,
            fpdl.recepit_title,
            fpdl.payment_bank_name,
            fpdl.payment_bank_iban,
            fpdl.payment_bank_abi,
            fpdl.payment_bank_cab,
            fpdl.payment_bank_bic,
            fpdl.prepayment_discount,
            fpdl.max_payment_date,
            fpdl.penalty_amount,
            fpdl.penalty_date,
            fpdl.payment_code
        FROM fatturapa_payment_data fpd
        LEFT JOIN fatturapa_payment_term fpt ON fpd.payment_terms = fpt.id
        LEFT JOIN fatturapa_payment_detail fpdl ON fpd.id = fpdl.payment_data_id
        LEFT JOIN fatturapa_payment_method fpm ON fpdl.fatturapa_pm_id = fpm.id
    """)
    rows = env.cr.fetchall()
    invoice_map = {}
    for row in rows:
        invoice_id, *payment_data = row
        invoice_map.setdefault(invoice_id, []).append(tuple(payment_data))

    moves = env["account.move"].browse(invoice_map.keys())
    for move in moves:
        for payment_data in invoice_map[move.id]:
            (
                term_code,
                recipient,
                method_code,
                payment_term_start,
                payment_days,
                payment_due_date,
                payment_amount,
                post_office_code,
                recepit_surname,
                recepit_name,
                recepit_cf,
                recepit_title,
                payment_bank_name,
                payment_bank_iban,
                payment_bank_abi,
                payment_bank_cab,
                payment_bank_bic,
                prepayment_discount,
                max_payment_date,
                penalty_amount,
                penalty_date,
                payment_code,
            ) = payment_data
            payment_tags = Markup('<ul class="mb-0">{}</ul>').format(
                Markup().join(
                    nl2br_enclose(" ".join(tag.split()), "li")
                    for tag in [
                        f'CondizioniPagamento: {term_code or "N/A"}',
                        f'Beneficiario: {recipient or "N/A"}',
                        f'ModalitaPagamento: {method_code or "N/A"}',
                        f'DataRiferimentoTerminiPagamento: {payment_term_start or "N/A"}',  # noqa: E501
                        f'GiorniTerminiPagamento: {payment_days or "N/A"}',
                        f'DataScadenzaPagamento: {payment_due_date or "N/A"}',
                        f'ImportoPagamento: {payment_amount or "N/A"}',
                        f'CodUfficioPostale: {post_office_code or "N/A"}',
                        f'CognomeQuietanzante: {recepit_surname or "N/A"}',
                        f'NomeQuietanzante: {recepit_name or "N/A"}',
                        f'CFQuietanzante: {recepit_cf or "N/A"}',
                        f'TitoloQuietanzante: {recepit_title or "N/A"}',
                        f'IstitutoFinanziario: {payment_bank_name or "N/A"}',
                        f'IBAN: {payment_bank_iban or "N/A"}',
                        f'ABI: {payment_bank_abi or "N/A"}',
                        f'CAB: {payment_bank_cab or "N/A"}',
                        f'BIC: {payment_bank_bic or "N/A"}',
                        f'ScontoPagamentoAnticipato: {prepayment_discount or "N/A"}',
                        f'DataLimitePagamentoAnticipato: {max_payment_date or "N/A"}',
                        f'PenalitaPagamentiRitardati: {penalty_amount or "N/A"}',
                        f'DataDecorrenzaPenale: {penalty_date or "N/A"}',
                        f'CodicePagamento: {payment_code or "N/A"}',
                    ]
                )
            )
            message = Markup("{} {}<br/>{}").format(
                "DatiPagamento", env._("from XML file:"), payment_tags
            )
            move.sudo().message_post(body=message)


def _l10n_it_fatturapa_post_migration_related_document_type(env):
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
    out_moves = moves.filtered(lambda m: m.is_sale_document())
    for move in out_moves:
        for index, (document_type, name, date, code, cig, cup) in enumerate(
            invoice_map[move.id], start=1
        ):
            if index == 1:
                if document_type == "order":
                    document_type = "purchase_order"
                elif document_type not in ["contract", "agreement"]:
                    document_type = ""
                move.l10n_it_origin_document_type = document_type
                move.l10n_it_origin_document_name = name
                move.l10n_it_origin_document_date = date
                move.l10n_it_cig = cig
                move.l10n_it_cup = cup
            else:
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
    for move in moves - out_moves:
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
        LEFT JOIN fatturapa_fiscal_position fp ON rp.register_fiscalpos = fp.id
        WHERE res_company.partner_id = rp.id AND rp.register_fiscalpos IS NOT NULL
    """
    openupgrade.logged_query(env.cr, query)

    query = """
        UPDATE ir_attachment
        SET res_model = 'account.move', res_id = fa.invoice_id
        FROM fatturapa_attachments fa
        WHERE ir_attachment.id = fa.ir_attachment_id
    """
    openupgrade.logged_query(env.cr, query)

    _l10n_it_fatturapa_post_migration_related_ddt(env)
    _l10n_it_fatturapa_post_migration_delivery_data(env)
    _l10n_it_fatturapa_post_migration_vehicle_data(env)
    _l10n_it_fatturapa_post_migration_payment_data(env)
    _l10n_it_fatturapa_post_migration_related_document_type(env)


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
    table = "account_move"
    condition = "e_invoice_reference IS NOT NULL"
    rename_fields(env, table, {"ref": "e_invoice_reference"}, condition=condition)

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
        attachment.res_model = "account.move"
        attachment.res_id = move.id
        attachment.res_field = "l10n_it_edi_attachment_file"
        if not attachment.raw:
            filestore_path = os.path.join(
                config.filestore(env.cr.dbname), attachment.store_fname
            )
            if os.path.exists(filestore_path):
                with open(filestore_path, "rb") as f:
                    file_raw = base64.encodebytes(f.read())
                    attachment.raw = file_raw


def _l10n_it_fatturapa_out_post_migration(env):
    updates = {
        "ready": "being_sent",
        "sent": "processing",
        "delivered": "forwarded",
        "accepted": "accepted_by_pa_partner",
        "error": "forward_failed",
    }

    for fatturapa_state, l10n_it_edi_state in updates.items():
        query = f"""
            UPDATE account_move
            SET l10n_it_edi_state = '{l10n_it_edi_state}'
            WHERE fatturapa_state = '{fatturapa_state}'
        """
        openupgrade.logged_query(env.cr, query)

    env.cr.execute("""
        SELECT
            am.id,
            fao.ir_attachment_id AS attachment_id
        FROM account_move am
        JOIN fatturapa_attachment_out fao ON fao.id = am.fatturapa_attachment_out_id
        WHERE am.fatturapa_attachment_out_id IS NOT NULL
    """)
    rows = env.cr.fetchall()
    for row in rows:
        invoice_id, attachment_id = row
        move = env["account.move"].browse(invoice_id)
        attachment = env["ir.attachment"].browse(attachment_id)
        attachment.res_model = "account.move"
        attachment.res_id = move.id
        attachment.res_field = "l10n_it_edi_attachment_file"
        if not attachment.raw:
            filestore_path = os.path.join(
                config.filestore(env.cr.dbname), attachment.store_fname
            )
            if os.path.exists(filestore_path):
                with open(filestore_path, "rb") as f:
                    file_raw = base64.encodebytes(f.read())
                    attachment.raw = file_raw


def _l10n_it_fatturapa_sale_post_migration(env):
    add_field_if_not_exists(
        env,
        "sale_order",
        "l10n_it_origin_document_type",
        "selection",
        "l10n_it_edi_sale",
    )
    add_field_if_not_exists(
        env, "sale_order", "l10n_it_origin_document_name", "char", "l10n_it_edi_sale"
    )
    add_field_if_not_exists(
        env, "sale_order", "l10n_it_origin_document_date", "date", "l10n_it_edi_sale"
    )
    add_field_if_not_exists(
        env, "sale_order", "l10n_it_cig", "char", "l10n_it_edi_sale"
    )
    add_field_if_not_exists(
        env, "sale_order", "l10n_it_cup", "char", "l10n_it_edi_sale"
    )

    env.cr.execute("""
        SELECT sale_order_id, sale_order_line_id, type, name, date, code, cig, cup
        FROM fatturapa_related_document_type
        WHERE sale_order_id IS NOT NULL OR sale_order_line_id IS NOT NULL
    """)
    rows = env.cr.fetchall()
    sale_map = {}
    for row in rows:
        sale_order_id, sale_order_line_id, document_type, name, date, code, cig, cup = (
            row
        )
        sale_id = (
            sale_order_id
            or env["sale.order.line"].browse(sale_order_line_id).order_id.id
        )
        if sale_id:
            sale_map.setdefault(sale_id, []).append(
                (document_type, name, date, code, cig, cup)
            )

    sales = env["sale.order"].browse(sale_map.keys())
    for sale in sales:
        for index, (document_type, name, date, code, cig, cup) in enumerate(
            sale_map[sale.id], start=1
        ):
            if index == 1:
                if document_type == "order":
                    document_type = "purchase_order"
                elif document_type not in ["contract", "agreement"]:
                    document_type = ""
                query = f"""
                    UPDATE sale_order
                    SET
                        l10n_it_origin_document_type = '{document_type or ''}',
                        l10n_it_origin_document_name = '{name or ''}',
                        l10n_it_cig = '{cig or ''}',
                        l10n_it_cup = '{cup or ''}'
                    WHERE id = {sale.id}
                """
                openupgrade.logged_query(env.cr, query)
                if date:
                    query = f"""
                        UPDATE sale_order
                        SET l10n_it_origin_document_date = '{date.strftime('%Y-%m-%d')}'
                        WHERE id = {sale.id}
                    """
                    openupgrade.logged_query(env.cr, query)
            else:
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
                sale.sudo().message_post(body=message)


def _l10n_it_fiscal_payment_term_post_migration(env):
    add_field_if_not_exists(
        env, "account_move", "l10n_it_payment_method", "selection", "l10n_it_edi_ndd"
    )

    query = """
        UPDATE account_move
        SET l10n_it_payment_method = fpm.code
        FROM account_payment_term apt
        LEFT JOIN fatturapa_payment_method fpm ON apt.fatturapa_pm_id = fpm.id
        WHERE account_move.invoice_payment_term_id = apt.id
    """
    openupgrade.logged_query(env.cr, query)


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


def _l10n_it_vat_payability_pre_migration(env):
    updates = {
        "D": "on_payment",
        "I": "on_invoice",
        "S": "on_invoice",
    }

    for payability, tax_exigibility in updates.items():
        query = f"""
            UPDATE account_tax
            SET tax_exigibility = '{tax_exigibility}'
            WHERE payability = '{payability}'
        """
        openupgrade.logged_query(env.cr, query)


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
