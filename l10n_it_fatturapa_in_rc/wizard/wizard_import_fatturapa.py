# -*- coding: utf-8 -*-

from odoo import models


class WizardImportFatturapa(models.TransientModel):
    _inherit = "wizard.import.fatturapa"

    def _prepare_generic_line_data(self, line):
        retLine = {}
        account_tax_model = self.env['account.tax']
        if float(line.AliquotaIVA) == 0.0 and line.Natura == 'N6':
            # search reversed tax
            account_rc_types = self.env['account.rc.type.tax'].search([])
            reversed_acc_tax_ids = account_rc_types.mapped(
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
