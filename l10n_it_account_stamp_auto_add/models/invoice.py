# -*- coding: utf-8 -*-
##############################################################################
#
#    Italian Localization - Account Stamp
#    See __openerp__.py file for copyright and licensing details.
#
##############################################################################

from openerp.osv.orm import Model


class account_invoice(Model):
    _inherit = 'account.invoice'

    def button_reset_taxes(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        line_obj = self.pool.get('account.invoice.line')
        for invoice in self.browse(cr, uid, ids, context):
            stamp_line_id = self.is_tax_stamp_line_present(cr, uid, invoice, context=context)
            if stamp_line_id:
                line_obj.unlink(cr, uid, stamp_line_id, context)
            if not invoice.tax_stamp:
                continue
            if invoice.type in ('out_invoice',  'out_refund'):
                if invoice.company_id.automatic_tax_stamp_on_customer_invoices:
                    self.add_tax_stamp_line(cr, uid, invoice.id, context=context)
            else:
                if invoice.company_id.automatic_tax_stamp_on_supplier_invoices:
                    self.add_tax_stamp_line(cr, uid, invoice.id, context=context)
        res = super(account_invoice, self).button_reset_taxes(
            cr, uid, ids, context=context)
        return res
