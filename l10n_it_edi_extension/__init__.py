# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from . import controllers
from . import models
from . import wizards

from odoo.tools import config

from openupgradelib import openupgrade, openupgrade_tools

from odoo.addons.base.models.ir_qweb_fields import Markup, nl2br, nl2br_enclose

OLD_MODULES = [
    "l10n_it_fatturapa",
    "l10n_it_fatturapa_in",
    "l10n_it_fatturapa_out",
    "l10n_it_fiscal_payment_term",
    "l10n_it_fiscalcode",
    "l10n_it_ipa",
    "l10n_it_pec",
    "l10n_it_rea",
    "l10n_it_vat_payability",
]


def _l10n_it_fatturapa_pre_migration(env):
    RENAMED_FIELDS = [
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
                "l10n_edi_it_register_province_id",
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
                "fatturapa_stabile_organizzazione",
            ),
            (
                "res.company",
                "l10n_edi_it_stable_organization",
            ),
        ],
    ]
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


def _l10n_it_fatturapa_post_migration(env):
    query = """
        UPDATE res_partner
        SET
            l10n_it_pa_index = codice_destinatario,
            l10n_it_pec_email = pec_destinatario
    """
    openupgrade.logged_query(env.cr, query)

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

    query = """
        UPDATE account_move_line
        SET sequence = ftpa_line_number
    """
    openupgrade.logged_query(env.cr, query)

    query = """
        UPDATE res_company
        SET l10n_it_tax_representative_partner_id = fatturapa_tax_representative
    """
    openupgrade.logged_query(env.cr, query)

    if openupgrade_tools.table_exists(env.cr, "fatturapa_activity_progress"):
        env.cr.execute("SELECT * FROM fatturapa_activity_progress LIMIT 1")
        if env.cr.fetchone():
            openupgrade.logged_query(
                env.cr,
                """
                INSERT INTO
                    l10n_it_edi_activity_progress (activity_progress, invoice_id)
                SELECT
                    fatturapa_activity_progress, invoice_id
                FROM
                    fatturapa_activity_progress
                """,
            )

    if openupgrade_tools.table_exists(env.cr, "fatturapa_summary_data"):
        env.cr.execute("SELECT * FROM fatturapa_summary_data LIMIT 1")
        if env.cr.fetchone():
            openupgrade.logged_query(
                env.cr,
                """
                INSERT INTO
                    l10n_it_edi_summary_data (
                        tax_rate, non_taxable_nature, incidental_charges, rounding,
                        amount_untaxed, amount_tax, payability, law_reference,
                        invoice_id
                    )
                SELECT
                    tax_rate, non_taxable_nature, incidental_charges, rounding,
                    amount_untaxed, amount_tax, payability, law_reference,
                    invoice_id
                FROM
                    fatturapa_summary_data
                """,
            )

    _l10n_it_fatturapa_post_migration_related_ddt(env)
    _l10n_it_fatturapa_post_migration_delivery_data(env)
    _l10n_it_fatturapa_post_migration_vehicle_data(env)
    _l10n_it_fatturapa_post_migration_payment_data(env)


def _l10n_it_fatturapa_in_pre_migration(env):
    RENAMED_FIELDS = [
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
    query = """
        UPDATE account_move
        SET ref = e_invoice_reference
        WHERE e_invoice_reference IS NOT NULL
    """
    openupgrade.logged_query(env.cr, query)

    if openupgrade_tools.table_exists(env.cr, "einvoice_line"):
        env.cr.execute("SELECT * FROM einvoice_line LIMIT 1")
        if env.cr.fetchone():
            openupgrade.logged_query(
                env.cr,
                """
                INSERT INTO
                    l10n_it_edi_line (
                        id, invoice_id, line_number, service_type, name, qty, uom,
                        period_start_date, period_end_date, unit_price,
                        total_price, tax_amount, wt_amount, tax_kind
                    )
                SELECT
                    id, invoice_id, line_number, service_type, name, qty, uom,
                    period_start_date, period_end_date, unit_price,
                    total_price, tax_amount, wt_amount, tax_kind
                FROM
                    einvoice_line
                """,
            )

    if openupgrade_tools.table_exists(env.cr, "fatturapa_article_code"):
        env.cr.execute("SELECT * FROM fatturapa_article_code LIMIT 1")
        if env.cr.fetchone():
            openupgrade.logged_query(
                env.cr,
                """
                INSERT INTO
                    l10n_it_edi_article_code (name, code_val, l10n_it_edi_line_id)
                SELECT
                    name, code_val, e_invoice_line_id
                FROM
                    fatturapa_article_code
                """,
            )

    if openupgrade_tools.table_exists(env.cr, "discount_rise_price"):
        env.cr.execute("SELECT * FROM discount_rise_price LIMIT 1")
        if env.cr.fetchone():
            openupgrade.logged_query(
                env.cr,
                """
                INSERT INTO
                    l10n_it_edi_discount_rise_price (
                        name, percentage, amount, invoice_line_id, invoice_id,
                        l10n_it_edi_line_id
                    )
                SELECT
                    name, percentage, amount, invoice_line_id, invoice_id,
                    e_invoice_line_id
                FROM
                    discount_rise_price
                """,
            )

    if openupgrade_tools.table_exists(env.cr, "einvoice_line_other_data"):
        env.cr.execute("SELECT * FROM einvoice_line_other_data LIMIT 1")
        if env.cr.fetchone():
            openupgrade.logged_query(
                env.cr,
                """
                INSERT INTO
                    l10n_it_edi_line_other_data (
                        l10n_it_edi_line_id, name, text_ref, num_ref, date_ref
                    )
                SELECT
                    e_invoice_line_id, name, text_ref, num_ref, date_ref
                FROM
                    einvoice_line_other_data
                """,
            )

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


def _l10n_it_fiscal_payment_term_post_migration(env):
    if not openupgrade.column_exists(env.cr, "account_move", "l10n_it_payment_method"):
        field_spec = [
            (
                "l10n_it_payment_method",
                "account.move",
                "account_move",
                "selection",
                "selection",
                "l10n_it_edi_ndd",
                False,
            )
        ]
        openupgrade.add_fields(env, field_spec)

    query = """
        UPDATE account_move
        SET l10n_it_payment_method = fpm.code
        FROM account_payment_term apt
        LEFT JOIN fatturapa_payment_method fpm ON apt.fatturapa_pm_id = fpm.id
        WHERE account_move.invoice_payment_term_id = apt.id
    """
    openupgrade.logged_query(env.cr, query)


def _l10n_it_fiscalcode_post_migration(env):
    query = """
        UPDATE res_partner
        SET l10n_it_codice_fiscale = fiscalcode
        WHERE
            fiscalcode IS NOT NULL
            AND LENGTH(TRIM(fiscalcode)) >= 11
    """
    openupgrade.logged_query(env.cr, query)

    query = """
        UPDATE res_company
        SET l10n_it_codice_fiscale = fiscalcode
        WHERE
            fiscalcode IS NOT NULL
            AND LENGTH(TRIM(fiscalcode)) >= 11
    """
    openupgrade.logged_query(env.cr, query)


def _l10n_it_ipa_post_migration(env):
    query = """
        UPDATE res_partner
        SET l10n_it_pa_index = ipa_code
        WHERE ipa_code IS NOT NULL
    """
    openupgrade.logged_query(env.cr, query)


def _l10n_it_pec_post_migration(env):
    query = """
        UPDATE res_partner
        SET l10n_it_pec_email = pec_mail
        WHERE pec_mail IS NOT NULL
    """
    openupgrade.logged_query(env.cr, query)


def _l10n_it_rea_post_migration(env):
    query = """
        UPDATE
            res_company
        SET
            l10n_it_eco_index_office = res_partner.rea_office,
            l10n_it_eco_index_number = res_partner.rea_code,
            l10n_it_eco_index_share_capital = res_partner.rea_capital,
            l10n_it_eco_index_sole_shareholder = res_partner.rea_member_type,
            l10n_it_eco_index_liquidation_state = res_partner.rea_liquidation_state
        FROM
            res_partner
        WHERE
            res_company.partner_id = res_partner.id
            AND res_partner.rea_office IS NOT NULL
    """
    openupgrade.logged_query(env.cr, query)

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE res_company
        SET l10n_it_has_eco_index = 't'
        WHERE l10n_it_eco_index_number IS NOT NULL
        """,
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
