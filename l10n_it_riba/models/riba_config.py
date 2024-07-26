# Copyright (C) 2012 Andrea Cometa.
# Email: info@andreacometa.it
# Web site: http://www.andreacometa.it
# Copyright (C) 2012 Associazione OpenERP Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2012-2017 Lorenzo Battistini - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class RibaConfiguration(models.Model):
    _name = "riba.configuration"
    _description = "Configuration parameters for RiBa"
    _check_company_auto = True

    name = fields.Char("Description", size=64, required=True)
    type = fields.Selection(
        [("sbf", "Subject To Collection"), ("incasso", "After Collection")],
        "Issue Mode",
        required=True,
    )
    sbf_collection_type = fields.Selection(
        [("immediate", "Immediate"), ("maturation", "At currency maturation")],
        "Collection Type",
    )
    bank_id = fields.Many2one(
        "res.partner.bank",
        "Bank Account",
        required=True,
        check_company=True,
        help="Bank account used for RiBa issuing.",
    )
    acceptance_journal_id = fields.Many2one(
        "account.journal",
        "Acceptance Journal",
        check_company=True,
        domain="[('company_id', '=', company_id), ('type', '=', 'bank')]",
        help="Journal used when RiBa is accepted by the bank.",
    )
    acceptance_account_id = fields.Many2one(
        "account.account",
        "Acceptance Account",
        check_company=True,
        help="Account used when RiBa is accepted by the bank.",
    )
    company_id = fields.Many2one(
        "res.company",
        "Company",
        required=True,
        default=lambda self: self.env.company,
    )
    credit_journal_id = fields.Many2one(
        "account.journal",
        "Credit Journal",
        check_company=True,
        domain="[('company_id', '=', company_id), ('type', '=', 'bank')]",
        help="Journal used when RiBa amount is credited by the bank.",
    )
    credit_account_id = fields.Many2one(
        "account.account",
        "RiBa Account",
        check_company=True,
        help="Account used when RiBa amount is credited by the bank.",
        domain="["
        "('company_id', '=', company_id), "
        "('account_type', '!=', 'liability_credit_card'), "
        "]",
    )
    bank_account_id = fields.Many2one(
        "account.account",
        "A/C Bank Account",
        check_company=True,
    )
    bank_expense_account_id = fields.Many2one("account.account", "Bank Fees Account")
    past_due_journal_id = fields.Many2one(
        "account.journal",
        "Past Due Journal",
        check_company=True,
        domain="[('company_id', '=', company_id), ('type', '=', 'bank')]",
        help="Journal used when RiBa is past due.",
    )
    overdue_effects_account_id = fields.Many2one(
        "account.account",
        "Past Due Bills Account",
        check_company=True,
    )
    protest_charge_account_id = fields.Many2one(
        "account.account",
        "Protest Fee Account",
        check_company=True,
    )
    settlement_journal_id = fields.Many2one(
        "account.journal",
        "Settlement Journal",
        check_company=True,
        help="Journal used when customers finally pay the invoice to bank.",
    )

    def get_default_value_by_list(self, field_name):
        if not self.env.context.get("active_id", False):
            return False
        ribalist_model = self.env["riba.slip"]
        ribalist = ribalist_model.browse(self.env.context["active_id"])
        return (
            ribalist.config_id[field_name]
            and ribalist.config_id[field_name].id
            or False
        )

    def get_default_value_by_list_line(self, field_name):
        if not self.env.context.get("active_id", False):
            return False
        ribalist_line = self.env["riba.slip.line"].browse(self.env.context["active_id"])
        return (
            ribalist_line.slip_id.config_id[field_name]
            and ribalist_line.slip_id.config_id[field_name].id
            or False
        )
