from odoo import _, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        statement_obj = self.env["account.intrastat.statement"]
        for invoice in self:
            if invoice.move_type.startswith("out"):
                domain = [
                    ("date_start", "<=", invoice.invoice_date),
                    ("date_stop", ">=", invoice.invoice_date),
                    ("sale", "=", True),
                ]
            else:
                domain = [
                    ("date_start", "<=", invoice.date),
                    ("date_stop", ">=", invoice.date),
                    ("purchase", "=", True),
                ]
            statements = statement_obj.search(domain)
            sections = {
                "out": [
                    "sale_section1_ids",
                    "sale_section2_ids",
                    "sale_section3_ids",
                    "sale_section4_ids",
                ],
                "in": [
                    "purchase_section1_ids",
                    "purchase_section2_ids",
                    "purchase_section3_ids",
                    "purchase_section4_ids",
                ],
            }
            if invoice.intrastat and statements:
                for section in sections[
                    "out" if invoice.move_type.startswith("out") else "in"
                ]:
                    if invoice in statements[section].invoice_id:
                        break
                else:
                    raise ValidationError(
                        _(
                            "Intrastat statement already exists for the date range "
                            "of the invoice %s you are trying to post! Post it in "
                            "another date or delete the intrastat statement to "
                            "proceed."
                        )
                        % (
                            invoice.name
                            if invoice.name != "/"
                            else invoice.partner_id.name
                        )
                    )
        return super().action_post()
