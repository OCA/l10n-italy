# Copyright 2025 Nextev Srl

import re

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class L10nItDeclarationOfIntent(models.Model):
    _inherit = "l10n_it_edi_doi.declaration_of_intent"

    number = fields.Char(
        help="Sequential number for internal reference",
        copy=False,
    )

    purchase_order_ids = fields.One2many(
        "purchase.order",
        "l10n_it_edi_doi_id",
        string="Purchase / Rfq Orders",
        copy=False,
        readonly=True,
    )

    move_doi_ids = fields.One2many(
        "account.move.doi",
        "declaration_id",
        string="Invoice Declaration Lines",
        copy=False,
        readonly=True,
        help="Links to invoices using this declaration with specific amounts.",
    )

    type = fields.Selection(
        [("in", "Issued from company"), ("out", "Received from customers")],
        required=True,
        default="out",
    )

    @api.constrains("protocol_number_part1", "protocol_number_part2", "type")
    def _check_protocol_format(self):
        """
        Validate AdE protocol format for issued declarations.

        The full protocol (part1 + part2) should be 17 characters:
        - AAAA: Year (4 digits)
        - NNNNNNNN: Sequential number (8 digits)
        - CCCCC: Last 5 chars of company fiscal code (5 alphanumeric)

        Format: AAAANNNNNNNNCCCCC (17 characters total)
        """
        # Format RegEx: 4 digits + 8 digits + 5 alphanumeric
        pattern = r"^(\d{4})(\d{8})([A-Z0-9]{5})$"
        format_explanation = self.env._(
            "Format: AAAANNNNNNNNCCCCC\n"
            "- AAAA: Year (4 digits)\n"
            "- NNNNNNNN: Sequential (8 digits)\n"
            "- CCCCC: Last 5 chars of fiscal code\n"
            "Example: 20250000123456789"
        )
        for doi in self:
            if doi.type != "in":
                # Skip validation for received declarations
                continue

            part1 = (doi.protocol_number_part1 or "").strip()
            part2 = (doi.protocol_number_part2 or "").strip()

            if not part1 or not part2:
                continue

            full_protocol = part1 + part2
            if len(full_protocol) != 17:
                raise ValidationError(
                    doi.env._(
                        "The protocol number must be exactly 17 characters.\n"
                        "Current: %(current)s (%(length)s characters)\n\n",
                        current=full_protocol,
                        length=len(full_protocol),
                    )
                    + format_explanation
                )

            match = re.match(pattern, full_protocol.upper())
            if not match:
                raise ValidationError(
                    doi.env._(
                        "The protocol '%(protocol)s' does not match AdE format.\n\n",
                        protocol=full_protocol,
                    )
                    + format_explanation
                )

    def _fetch_valid_declaration_of_intent(
        self, company, partner, currency, date, doi_type="out"
    ):
        res = super()._fetch_valid_declaration_of_intent(
            company, partner, currency, date
        )
        if not res or res.type == doi_type:
            return res
        # Same domain as in the original, with the addition of 'type'
        domain = [
            ("state", "=", "active"),
            ("company_id", "=", company.id),
            ("currency_id", "=", currency.id),
            ("partner_id", "=", partner.commercial_partner_id.id),
            ("start_date", "<=", date),
            ("end_date", ">=", date),
            ("remaining", ">", 0),
            ("type", "=", doi_type),
        ]
        return self.search(domain, limit=1)

    @api.depends(
        "invoice_ids",
        "invoice_ids.state",
        "invoice_ids.l10n_it_edi_doi_amount",
        "invoice_ids.move_type",
        "move_doi_ids",
        "move_doi_ids.amount",
        "move_doi_ids.move_id.state",
        "move_doi_ids.move_id.move_type",
    )
    def _compute_invoiced(self):
        """Override to use bridge model amounts when available.

        For invoices with bridge records (multiple declarations), use the specific
        amounts from the bridge model. For invoices without bridge records (single
        declaration via l10n_it_edi_doi_id), use the standard l10n_it_edi_doi_amount.

        Refunds (in_refund, out_refund) reduce the invoiced amount.
        """
        for declaration in self:
            total_invoiced = 0

            # Get all posted invoices and draft with name linked through the bridge
            # model
            posted_doi_links = declaration.move_doi_ids.filtered(
                lambda doi: doi.move_id.state == "posted"
                or (doi.move_id.state == "draft" and doi.move_id.name)
            )
            bridge_moves = posted_doi_links.mapped("move_id")

            # Sum amounts from bridge records for multi-declaration invoices
            # Refunds reduce the total (negative contribution)
            for doi_link in posted_doi_links:
                amount = doi_link.amount
                if doi_link.move_id.move_type in ("in_refund", "out_refund"):
                    amount = -amount
                total_invoiced += amount

            # For single-declaration invoices (not using bridge model),
            # use the standard field
            posted_invoices = declaration.invoice_ids.filtered(
                lambda invoice: invoice.state == "posted"
            )
            single_declaration_invoices = posted_invoices - bridge_moves
            for invoice in single_declaration_invoices:
                amount = invoice.l10n_it_edi_doi_amount
                if invoice.move_type in ("in_refund", "out_refund"):
                    amount = -amount
                total_invoiced += amount

            declaration.invoiced = total_invoiced

    @api.depends(
        "purchase_order_ids",
        "purchase_order_ids.state",
        "purchase_order_ids.l10n_it_edi_doi_not_yet_invoiced",
    )
    def _compute_not_yet_invoiced(self):
        received_doi = self.filtered(lambda r: r.type == "out")
        issued_doi = self - received_doi
        super(L10nItDeclarationOfIntent, received_doi)._compute_not_yet_invoiced()
        for declaration in issued_doi:
            relevant_orders = declaration.purchase_order_ids.filtered(
                lambda order: order.state == "purchase"
            )
            declaration.not_yet_invoiced = sum(
                relevant_orders.mapped("l10n_it_edi_doi_not_yet_invoiced")
            )
        return  # W8110

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if not values.get("number"):
                values["number"] = self.env["ir.sequence"].next_by_code(
                    "l10n_it_edi_doi.declaration_of_intent"
                )
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_except_linked_to_purchase_document(self):
        if self.purchase_order_ids:
            raise UserError(
                _(
                    "You cannot delete Declarations of Intents that "
                    "are already used on at least one Purchase Order."
                )
            )
