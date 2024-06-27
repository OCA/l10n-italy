#  Copyright 2023 MKT SRL
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

NEW_MODULE_NAME = "l10n_it_financial_statement_eu"
OLD_MODULE_NAME = "l10n_it_account_balance_eu"
RENAMED_MODELS = [
    (
        "account.balance.eu",
        "financial.statement.eu",
    ),
    (
        "account.balance.eu.log",
        "financial.statement.eu.log",
    ),
    (
        "account.balance.eu.wizard",
        "financial.statement.eu.wizard",
    ),
    (
        "report.l10n_it_account_balance_eu.balance_eu_xlsx_report",
        "report.l10n_it_financial_statement_eu.fseu_xlsx_report",
    ),
    (
        "report.l10n_it_account_balance_eu.balance_eu_xbrl_report",
        "report.l10n_it_financial_statement_eu.fseu_xbrl_report",
    ),
    (
        "report.l10n_it_account_balance_eu.balance_eu_html_report",
        "report.l10n_it_financial_statement_eu.fseu_html_report",
    ),
]

RENAMED_FIELDS = [
    [
        (
            "account.account",
            "account_balance_eu_debit_id",
        ),
        (
            "account.account",
            "financial_statement_eu_debit_id",
        ),
    ],
    [
        (
            "account.account",
            "account_balance_eu_credit_id",
        ),
        (
            "account.account",
            "financial_statement_eu_credit_id",
        ),
    ],
    [
        (
            "financial.statement.eu.log",
            "balance_id",
        ),
        (
            "financial.statement.eu.log",
            "financial_statement_id",
        ),
    ],
]
RENAMED_XMLIDS = [
    (
        "view_account_form_balance_ue",
        "view_form_account_financial_statement_eu",
    ),
    (
        "template_account_balance_report",
        "fseu_html_report",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    old_view = env["ir.ui.view"].search(
        [
            ("name", "=", "view.account.form.balance.ue"),
            ("model", "=", "account.account"),
        ]
    )
    if old_view:
        old_view.sudo().unlink()

    openupgrade.rename_models(
        env.cr,
        RENAMED_MODELS,
    )
    field_spec = []
    for renamed_field in RENAMED_FIELDS:
        (old_model, old_field), (new_model, new_field) = renamed_field
        field_spec.append(
            (
                old_model,
                old_model.replace(".", "_"),
                old_field,
                new_field,
            )
        )
    openupgrade.rename_fields(
        env,
        field_spec,
    )

    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                ".".join((OLD_MODULE_NAME, old_xml_id)),
                ".".join((NEW_MODULE_NAME, new_xml_id)),
            )
            for old_xml_id, new_xml_id in RENAMED_XMLIDS
        ],
    )

    openupgrade.rename_tables(
        env.cr, [("account_balance_eu", "financial_statement_eu")]
    )
    openupgrade.rename_tables(
        env.cr, [("account_balance_eu_log", "financial_statement_eu_log")]
    )
    openupgrade.rename_tables(
        env.cr, [("account_balance_eu_wizard", "financial_statement_eu_wizard")]
    )
