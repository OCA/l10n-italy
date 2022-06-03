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
        if any(inv_lines.mapped('rc')):
            rc_ita_fp = self.env['account.fiscal.position'].search([
                ('rc_type_id.e_invoice_suppliers', '=', True)
            ])
            if rc_ita_fp:
                invoice_data['fiscal_position_id'] = rc_ita_fp.id
        return res
