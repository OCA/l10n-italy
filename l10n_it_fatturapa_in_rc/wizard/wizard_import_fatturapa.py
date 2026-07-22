from odoo import models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def _prepare_generic_line_data(self, line):
        retLine = {}
        account_tax_model = self.env['account.tax']
        if float(line.AliquotaIVA) == 0.0 and (
            line.Natura.startswith("N6") or line.Natura == "N2.1"
        ):
            # search reversed tax
            account_rc_type_tax = self.env['account.rc.type.tax'].search([
                ('rc_type_id.e_invoice_suppliers', '=', True)
            ])
            if not account_rc_type_tax:
                account_rc_type_tax = self.env[
                    'account.rc.type.tax'].search([])
            reversed_acc_tax_ids = account_rc_type_tax.mapped(
                'purchase_tax_id.id')
            account_taxes = account_tax_model.search([
                ('type_tax_use', '=', 'purchase'),
                ('kind_id.code', '=', line.Natura),
                ('id', 'in', reversed_acc_tax_ids),
            ])
            retLine['rc'] = True
            if account_taxes:
                retLine['invoice_line_tax_ids'] = [
                    (6, 0, [account_taxes[0].id])]
            return retLine
        else:
            return super(WizardImportFatturapa, self).\
                _prepare_generic_line_data(line)

    def set_invoice_line_ids(
        self, FatturaBody, credit_account_id, partner, wt_found, invoice_data
    ):
        res = super(WizardImportFatturapa, self).set_invoice_line_ids(
            FatturaBody, credit_account_id, partner, wt_found, invoice_data)
        if not invoice_data.get('invoice_line_ids'):
            return
        # set RC fiscal position
        inv_line_ids = invoice_data['invoice_line_ids'][0][2]
        inv_lines = self.env['account.invoice.line'].browse(inv_line_ids)
        fp_obj = self.env['account.fiscal.position']
        inv_fp = fp_obj.browse(
            invoice_data.get("fiscal_position_id", 0)
        ).exists()
        rc_inv_lines = inv_lines.filtered("rc")
        if not inv_fp and rc_inv_lines:
            fp_domain = [
                ('rc_type_id.e_invoice_suppliers', '=', True)
            ]
            inv_fp_src_taxes = rc_inv_lines.mapped("invoice_line_tax_ids")
            if inv_fp_src_taxes:
                fp_domain.append(
                    ("tax_ids.tax_src_id", "in", inv_fp_src_taxes.ids)
                )
            inv_rc_fp = self.env['account.fiscal.position'].search(
                fp_domain,
                limit=1
            )
            if inv_rc_fp:
                invoice_data['fiscal_position_id'] = inv_rc_fp.id
        return res
