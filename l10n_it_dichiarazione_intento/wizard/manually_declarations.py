# Copyright 2019 Francesco Apruzzese <francescoapruzzese@openforce.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from lxml import etree
from odoo import models, fields, api


class SelectManuallyDeclarations(models.TransientModel):

    _name = 'select.manually.declarations'
    _description = 'Set declaration of intent manually on invoice'

    def fields_view_get(self, view_id=None, view_type='form', context=None,
                        toolbar=False, submenu=False):
        res = super(SelectManuallyDeclarations, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=False)
        # Show only valid documents for the invoice
        invoice_id = self.env.context.get('active_id', False)
        if not invoice_id:
            return res
        invoice = self.env['account.invoice'].browse(invoice_id)
        declarations = self.env['dichiarazione.intento'].get_valid(
            invoice.type.split('_')[0],
            invoice.partner_id.commercial_partner_id.id,
            invoice.date_invoice)
        if declarations:
            declarations_ids = [d.id for d in declarations]
        else:
            declarations_ids = []
        form_arch = etree.XML(res['arch'])
        nodes = form_arch.xpath("//field[@name='declaration_ids']")
        for node in nodes:
            node.set(
                'domain',
                '[("id", "in", {ids})]'.format(ids=declarations_ids)
                )
            res['arch'] = etree.tostring(form_arch)
        return res

    declaration_ids = fields.Many2many(
        'dichiarazione.intento',
        string='Declarations of Intent',
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
