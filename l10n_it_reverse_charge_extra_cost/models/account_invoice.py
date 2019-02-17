# -*- coding: utf-8 -*-
# Copyright 2019 Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models
from odoo.exceptions import Warning as UserError
from odoo.tools.translate import _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    extra_self_invoice_cost = fields.Float('Extra cost on self invoice',
                                           default=0, digits=(16, 2),
                                           copy=False)
    extra_cost_desc = fields.Char('Description for extra cost on self invoice',
                                  copy=False)

    def generate_extra_line(self, invoice_id, extra_cost, account_id, desc):
        model_invoice_line = self.env['account.invoice.line']
        model_invoice_line.create({
            'invoice_id': invoice_id,
            'name': desc,
            'account_id': account_id,
            'price_unit': extra_cost,
            'quantity': 1,
            'discount': 0,
            'rc': True
            # 'invoice_line_tax_ids': tax_id, is set up later in code
        })

    def generate_supplier_self_invoice(self):
        rc_type = self.fiscal_position_id.rc_type_id
        if not len(rc_type.tax_ids) == 1:
            raise UserError(_(
                "Can't find 1 tax mapping for %s" % rc_type.name))
        if not self.rc_self_purchase_invoice_id:
            supplier_invoice = self.copy()
        else:
            supplier_invoice_vals = self.copy_data()
            supplier_invoice = self.rc_self_purchase_invoice_id
            supplier_invoice.invoice_line_ids.unlink()
            supplier_invoice.write(supplier_invoice_vals[0])
        if self.extra_self_invoice_cost:
            self.generate_extra_line(supplier_invoice.id,
                                     self.extra_self_invoice_cost,
                                     rc_type.transitory_account_id.id,
                                     self.extra_cost_desc)
        # because this field has copy=False
        supplier_invoice.date = self.date
        supplier_invoice.date_invoice = self.date
        supplier_invoice.date_due = self.date
        supplier_invoice.partner_id = rc_type.partner_id.id
        supplier_invoice.journal_id = rc_type.supplier_journal_id.id
        for inv_line in supplier_invoice.invoice_line_ids:
            inv_line.invoice_line_tax_ids = [
                (6, 0, [rc_type.tax_ids[0].purchase_tax_id.id])]
            inv_line.account_id = rc_type.transitory_account_id.id
        self.rc_self_purchase_invoice_id = supplier_invoice.id

        # temporary disabling self invoice automations
        supplier_invoice.fiscal_position_id = None
        supplier_invoice.compute_taxes()
        supplier_invoice.check_total = supplier_invoice.amount_total
        supplier_invoice.action_invoice_open()
        supplier_invoice.fiscal_position_id = self.fiscal_position_id.id
