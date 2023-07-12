#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade
from openupgradelib.openupgrade import logged_query

from odoo.tools import DotDict

NEW_MODULE_NAME = "l10n_it_financial_statements_report"
OLD_MODULE_NAME = "l10n_it_account_balance_report"

REMOVED_MODELS = [
    "report_trial_balance_account",
    "account_balance_report_partner",
    "account_balance_report_account",
]

RENAMED_MODELS = [
    (
        "account_balance_report",
        "report.l10n_it_financial_statements_report.report",
    ),
    (
        "report.l10n_it_a_b_r.account_balance_report_xlsx",
        "report.l10n_it_financial_statements_report.report_xlsx",
    ),
]

RENAMED_FIELDS = [
    (
        "account.account.type",
        "account_account_type",
        "account_balance_report_section",
        "financial_statements_report_section",
    ),
]

RENAMED_XMLIDS = [
    (
        "template_account_balance_report",
        "template_financial_statements_report",
    ),
    (
        "account_balance_report",
        "report",
    ),
    (
        "account_balance_report_base",
        "financial_statements_report_base",
    ),
    (
        "account_balance_report_title",
        "financial_statements_report_title",
    ),
    (
        "account_balance_report_filters",
        "financial_statements_report_filters",
    ),
    (
        "account_balance_report_split_columns",
        "financial_statements_report_split_columns",
    ),
    (
        "account_balance_report_lines_header",
        "financial_statements_report_lines_header",
    ),
    (
        "account_balance_report_lines",
        "financial_statements_report_lines",
    ),
    (
        "account_balance_report_partners",
        "financial_statements_report_partners",
    ),
    (
        "account_balance_report_totals",
        "financial_statements_report_totals",
    ),
]


def remove_models(cr, model_spec):
    for name in model_spec:
        logged_query(
            cr,
            "DELETE FROM ir_model WHERE model = %s",
            (name,),
        )


def migrate_old_module(cr):
    remove_models(
        cr,
        REMOVED_MODELS,
    )
    openupgrade.rename_models(
        cr,
        RENAMED_MODELS,
    )
    openupgrade.rename_fields(
        # The method only needs the cursor, not the whole Environment
        DotDict(
            cr=cr,
        ),
        RENAMED_FIELDS,
        # Prevent Environment usage
        # whenever it will be implemented.
        no_deep=True,
    )
    full_renamed_xmlids = [
        (
            ".".join((NEW_MODULE_NAME, old_xmlid)),
            ".".join((NEW_MODULE_NAME, new_xmlid)),
        )
        for old_xmlid, new_xmlid in RENAMED_XMLIDS
    ]
    openupgrade.rename_xmlids(
        cr,
        full_renamed_xmlids,
    )


def pre_absorb_old_module(cr):
    if openupgrade.is_module_installed(cr, OLD_MODULE_NAME):
        openupgrade.update_module_names(
            cr,
            [
                (OLD_MODULE_NAME, NEW_MODULE_NAME),
            ],
            merge_modules=True,
        )
        migrate_old_module(cr)
