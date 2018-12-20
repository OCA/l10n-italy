# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2018 Giuseppe Stoduto
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from openerp import fields, models, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    incoterm = fields.Many2one('stock.incoterms', 'Incoterm', help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    volume = fields.Float('Volume')

    @api.multi
    def set_so_state(self, invoices, state):
        so_obj = self.env['sale.order']
        for invoice in invoices:
            so_ids = so_obj.search([('invoice_ids', '=', invoice.id)])
            for so_id in so_ids:
                if so_id.ddt_ids and so_id.state == 'done':
                    for line in so_id.order_line:
                        if line.state == 'done':
                            line.write({'state': 'confirmed'})
                    so_id.state = state

    @api.multi
    def unlink(self):
        self.set_so_state(self, 'manual')
        return super(AccountInvoice, self).unlink()
