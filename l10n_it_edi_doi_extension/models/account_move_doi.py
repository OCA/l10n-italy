# Copyright 2025 Nextev Srl

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMoveDoi(models.Model):
    """Bridge model to allow multiple Declarations of Intent per invoice.

    This model allows linking an invoice to multiple declarations of intent,
    specifying the amount covered by each declaration.
    """

    _name = "account.move.doi"
    _description = "Invoice Declaration of Intent"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    move_id = fields.Many2one(
        "account.move",
        string="Invoice",
        required=True,
        ondelete="cascade",
        index=True,
    )
    declaration_id = fields.Many2one(
        "l10n_it_edi_doi.declaration_of_intent",
        string="Declaration of Intent",
        required=True,
        ondelete="restrict",
    )
    amount = fields.Monetary(
        currency_field="currency_id",
        help="Amount of the invoice covered by this declaration of intent. "
        "If zero, the full remaining amount will be used.",
    )
    currency_id = fields.Many2one(
        related="move_id.currency_id",
        store=True,
    )
    company_id = fields.Many2one(
        related="move_id.company_id",
        store=True,
    )

    # Related fields for display
    protocol_number_part1 = fields.Char(
        related="declaration_id.protocol_number_part1",
        string="Protocol 1",
    )
    protocol_number_part2 = fields.Char(
        related="declaration_id.protocol_number_part2",
        string="Protocol 2",
    )
    declaration_issue_date = fields.Date(
        related="declaration_id.issue_date",
        string="Issue Date",
    )
    declaration_start_date = fields.Date(
        related="declaration_id.start_date",
        string="Start Date",
    )
    declaration_end_date = fields.Date(
        related="declaration_id.end_date",
        string="End Date",
    )
    declaration_threshold = fields.Monetary(
        related="declaration_id.threshold",
        string="Threshold",
    )
    declaration_invoiced = fields.Monetary(
        related="declaration_id.invoiced",
        string="Already Invoiced",
    )
    declaration_available = fields.Monetary(
        compute="_compute_declaration_available",
        string="Available",
    )

    @api.depends(
        "declaration_id", "declaration_id.threshold", "declaration_id.invoiced"
    )
    def _compute_declaration_available(self):
        for record in self:
            if record.declaration_id:
                record.declaration_available = (
                    record.declaration_id.threshold - record.declaration_id.invoiced
                )
            else:
                record.declaration_available = 0

    @api.constrains("declaration_id", "move_id")
    def _check_declaration_validity(self):
        for record in self:
            if not record.declaration_id or not record.move_id:
                continue
            move = record.move_id
            declaration = record.declaration_id
            validity_errors = declaration._get_validity_errors(
                move.company_id,
                move.partner_id.commercial_partner_id,
                move.currency_id,
            )
            if validity_errors:
                raise ValidationError("\n".join(validity_errors))

    @api.constrains("amount")
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError(
                    _("The amount covered by a declaration cannot be negative.")
                )

    def _compute_display_name(self):
        for record in self:
            if record.declaration_id:
                amount_str = f"{record.amount:.2f}" if record.amount else "0.00"
                record.display_name = (
                    f"{record.declaration_id.display_name} - "
                    f"{amount_str} {record.currency_id.symbol}"
                )
            else:
                record.display_name = _("New")
