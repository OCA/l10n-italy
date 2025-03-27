from odoo import _, api, fields, models
from odoo.exceptions import UserError


class L10nItDeclarationOfIntent(models.Model):
    _inherit = "l10n_it_edi_doi.declaration_of_intent"

    purchase_order_ids = fields.One2many(
        "purchase.order",
        "l10n_it_edi_doi_id",
        string="Purchase / Rfq Orders",
        copy=False,
        readonly=True,
    )

    type = fields.Selection(
        [("in", "Issued from company"), ("out", "Received from customers")],
        required=True,
        default="out",
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

    @api.ondelete(at_uninstall=False)
    def _unlink_except_linked_to_purchase_document(self):
        if self.purchase_order_ids:
            raise UserError(
                _(
                    "You cannot delete Declarations of Intents that "
                    "are already used on at least one Purchase Order."
                )
            )
