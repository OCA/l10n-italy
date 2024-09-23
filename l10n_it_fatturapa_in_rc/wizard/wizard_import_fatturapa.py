from odoo import models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def _is_in_reverse_charge_line(self, line):
        """The e-invoice line `line` should be imported as reverse charge."""
        return float(line.AliquotaIVA) == 0.0 and line.Natura.startswith("N6")

    def _prepare_generic_line_data(self, line):
        retLine = {}
        account_tax_model = self.env["account.tax"]
        if self._is_in_reverse_charge_line(line):
            # search reversed tax
            account_rc_type_tax = self.env["account.rc.type.tax"].search(
                [("rc_type_id.e_invoice_suppliers", "=", True)]
            )
            if not account_rc_type_tax:
                account_rc_type_tax = self.env["account.rc.type.tax"].search([])
            reversed_acc_tax_ids = account_rc_type_tax.mapped("purchase_tax_id.id")
            account_taxes = account_tax_model.search(
                [
                    ("type_tax_use", "=", "purchase"),
                    ("kind_id.code", "=", line.Natura),
                    ("id", "in", reversed_acc_tax_ids),
                ]
            )
            retLine["rc"] = True
            if account_taxes:
                retLine["tax_ids"] = [(6, 0, [account_taxes[0].id])]
            return retLine
        else:
            return super()._prepare_generic_line_data(line)

    def set_invoice_line_ids(
        self, FatturaBody, credit_account_id, partner, wt_found, invoice
    ):
        res = super().set_invoice_line_ids(
            FatturaBody, credit_account_id, partner, wt_found, invoice
        )
        if not invoice.invoice_line_ids:
            return res
        # set RC fiscal position
        inv_lines = invoice.invoice_line_ids
        if any(inv_lines.mapped("rc")):
            rc_ita_fp = self.env["account.fiscal.position"].search(
                [("rc_type_id.e_invoice_suppliers", "=", True)]
            )
            if rc_ita_fp:
                invoice.fiscal_position_id = rc_ita_fp
        return res
