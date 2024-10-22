# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

from odoo.tools import DotDict

OLD_MODULE_NAME = "l10n_it_ricevute_bancarie"
NEW_MODULE_NAME = "l10n_it_riba"
RENAMED_MODELS = [
    ("riba.distinta", "riba.slip"),
    ("riba.distinta.line", "riba.slip.line"),
    ("riba.distinta.move.line", "riba.slip.move.line"),
    (
        "report.l10n_it_ricevute_bancarie.distinta_qweb",
        "report.l10n_it_riba.slip_qweb",
    ),  # abstract
    ("riba.accreditation", "riba.credit"),
    ("riba.unsolved", "riba.past_due"),
]
RENAMED_TABLES = [
    ("riba_distinta", "riba_slip"),
    ("riba_distinta_line", "riba_slip_line"),
    ("riba_distinta_move_line", "riba_slip_move_line"),
    ("riba_accreditation", "riba_credit"),
    ("riba_unsolved", "riba_past_due"),
]
RENAMED_FIELDS = [
    [
        (
            "account.move",
            "riba_credited_ids",
        ),
        (
            "account.move",
            "riba_accredited_ids",
        ),
    ],
    [
        (
            "account.move",
            "riba_unsolved_ids",
        ),
        (
            "account.move",
            "riba_past_due_ids",
        ),
    ],
    [
        (
            "account.move",
            "unsolved_move_line_ids",  # is m2m, with table invoice_unsolved_line_rel
        ),
        (
            "account.move",
            "past_due_move_line_ids",  # is m2m, with table invoice_past_due_line_rel
        ),
    ],
    [
        (
            "account.move",
            "is_unsolved",
        ),
        (
            "account.move",
            "is_past_due",
        ),
    ],
    [
        (
            "account.move.line",
            "distinta_line_ids",
        ),
        (
            "account.move.line",
            "slip_line_ids",
        ),
    ],
    [
        (
            "account.move.line",
            "unsolved_invoice_ids",  # is m2m with table invoice_unsolved_line_rel
        ),
        (
            "account.move.line",
            "past_due_invoice_ids",  # is m2m with table invoice_past_due_line_rel
        ),
    ],
    [
        (
            "riba.distinta",
            "date_accreditation",
        ),
        (
            "riba.slip",
            "date_credited",
        ),
    ],
    [
        (
            "riba.distinta",
            "date_unsolved",
        ),
        (
            "riba.slip",
            "date_past_due",
        ),
    ],
    [
        (
            "riba.distinta",
            "accreditation_move_id",
        ),
        (
            "riba.slip",
            "credit_move_id",
        ),
    ],
    [
        (
            "riba.distinta",
            "unsolved_move_ids",  # is m2m table name computed
        ),
        (
            "riba.slip",
            "past_due_move_ids",  # is m2m table name computed
        ),
    ],
    [
        (
            "riba.distinta.line",
            "unsolved_move_id",
        ),
        (
            "riba.slip.line",
            "past_due_move_id",
        ),
    ],
    [
        (
            "riba.distinta.line",
            "distinta_id",
        ),
        (
            "riba.slip.line",
            "slip_id",
        ),
    ],
    [
        (
            "riba.configuration",
            "accreditation_journal_id",
        ),
        (
            "riba.configuration",
            "credit_journal_id",
        ),
    ],
    [
        (
            "riba.configuration",
            "accreditation_account_id",
        ),
        (
            "riba.configuration",
            "credit_account_id",
        ),
    ],
    [
        (
            "riba.configuration",
            "unsolved_journal_id",
        ),
        (
            "riba.configuration",
            "past_due_journal_id",
        ),
    ],
    [
        (
            "riba.accreditation",
            "accreditation_journal_id",
        ),
        (
            "riba.credit",
            "credit_journal_id",
        ),
    ],
    [
        (
            "riba.accreditation",
            "accreditation_account_id",
        ),
        (
            "riba.credit",
            "credit_account_id",
        ),
    ],
    [
        (
            "riba.accreditation",
            "accreditation_amount",
        ),
        (
            "riba.credit",
            "credit_amount",
        ),
    ],
    [
        (
            "riba.unsolved",
            "unsolved_journal_id",
        ),
        (
            "riba.past_due",
            "past_due_journal_id",
        ),
    ],
]
RENAMED_XMLIDS = [
    ("seq_riba_distinta", "seq_riba_slip"),
    ("print_distinta_qweb", "print_slip_qweb"),
    ("access_riba_distinta_uinvoice", "access_riba_slip_uinvoice"),
    ("access_riba_distinta_group_invoice", "access_riba_slip_group_invoice"),
    ("access_riba_distinta_user", "access_riba_slip_user"),
    ("access_riba_distinta_accountant", "access_riba_slip_accountant"),
    ("access_riba_distinta_line_uinvoice", "access_riba_slip_line_uinvoice"),
    ("access_riba_distinta_line_group_invoice", "access_riba_slip_line_group_invoice"),
    ("access_riba_distinta_line_user", "access_riba_slip_line_user"),
    ("access_riba_distinta_line_accountant", "access_riba_slip_line_accountant"),
    ("access_riba_distinta_move_line_uinvoice", "access_riba_slip_move_line_uinvoice"),
    (
        "access_riba_distinta_move_line_group_invoice",
        "access_riba_slip_move_line_group_invoice",
    ),
    ("access_riba_distinta_move_line_user", "access_riba_slip_move_line_user"),
    (
        "access_riba_distinta_move_line_accountant",
        "access_riba_slip_move_line_accountant",
    ),
    ("access_riba_unsolved", "access_riba_past_due"),
    ("access_riba_accreditation", "access_riba_credit"),
    ("riba_distinta_company_rule", "riba_slip_company_rule"),
    ("riba_distinta_line_company_rule", "riba_slip_line_company_rule"),
    ("view_riba_da_emettere_tree", "view_riba_to_issue_tree"),
    ("action_riba_da_emettere", "action_riba_to_issue"),
    ("menu_riba_da_emettere", "menu_riba_to_issue"),
    ("view_distinta_riba_filtri", "view_slip_riba_filter"),
    ("view_distinta_riba_tree", "view_slip_riba_tree"),
    ("view_riba_distinta_line_form", "view_riba_slip_line_form"),
    ("distinta_riba_action", "slip_riba_action"),
    ("distinta_layout", "slip_layout"),
    ("distinta_qweb", "slip_qweb"),
    ("riba_accreditation", "riba_credit"),
    ("riba_accreditation_action", "riba_credit_action"),
    ("riba_unsolved", "riba_past_due"),
    ("riba_unsolved_action", "riba_past_due_action"),
]


def migrate_old_module(cr):
    openupgrade.rename_models(
        cr,
        RENAMED_MODELS,
    )
    openupgrade.rename_tables(
        cr,
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
        # The method only needs the cursor, not the whole Environment
        DotDict(
            cr=cr,
        ),
        field_spec,
        # Prevent Environment usage
        # whenever it will be implemented.
        no_deep=True,
    )
    full_renamed_xmlids = [
        (
            ".".join((OLD_MODULE_NAME, old_xmlid)),
            ".".join((NEW_MODULE_NAME, new_xmlid)),
        )
        for old_xmlid, new_xmlid in RENAMED_XMLIDS
    ]
    openupgrade.rename_xmlids(
        cr,
        full_renamed_xmlids,
    )


def pre_absorb_old_module(cr):
    if openupgrade.is_module_installed(cr, "l10n_it_ricevute_bancarie"):
        openupgrade.update_module_names(
            cr,
            [
                ("l10n_it_ricevute_bancarie", "l10n_it_riba"),
            ],
            merge_modules=True,
        )
        migrate_old_module(cr)
