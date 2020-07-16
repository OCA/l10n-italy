# Copyright 2019 Francesco Apruzzese <francescoapruzzese@openforce.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models, fields, api


class SelectManuallyDeclarations(models.TransientModel):

    _name = 'select.manually.declarations'
    _description = 'Set declaration of intent manually on invoice'

    def _default_declaration(self):
        invoice_id = self._context.get('active_id', False)
        if not invoice_id:
            return []
        invoice = self.env['account.invoice'].browse(invoice_id)
        domain = [('partner_id', '=', invoice.partner_id.commercial_partner_id.id),
                  ('type', '=', invoice.type.split('_')[0]),
                  ('date_start', '<=', invoice.date_invoice),
                  ('date_end', '>=', invoice.date_invoice)
                  ]
        return self.env['dichiarazione.intento'].search(domain)

    declaration_ids = fields.Many2many(
        'dichiarazione.intento',
        string='Declarations of Intent',
        default=_default_declaration
    )

    @api.multi
    def confirm(self):
        self.ensure_one()
        res = True
        # ----- Link dichiarazione to invoice
        invoice_id = self.env.context.get('active_id', False)
        if not invoice_id:
            return res
        invoice = self.env['account.invoice'].browse(invoice_id)
        for declaration in self.declaration_ids:
            invoice.dichiarazione_intento_ids = [
                (4, declaration.id)]
        return True
