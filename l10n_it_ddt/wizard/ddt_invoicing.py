# -*- coding: utf-8 -*-
# Copyright 2017 Alessandro Camilli - Openforce
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError


class DdtInvoicing(models.TransientModel):
    _name = "ddt.invoicing"

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)

    @api.multi
    def create_invoices(self):
        for wizard in self:
            domain = [('to_be_invoiced', '=', True),
                      ('invoice_id', '=', False),
                      ('date', '>=', wizard.date_from),
                      ('date', '<=', wizard.date_to)]
            ddts = self.env['stock.picking.package.preparation'].search(domain)

            if not ddts:
                raise UserError(
                    _('Nothing to invoice'))

            view = self.env['ir.model.data'].get_object_reference(
                'l10n_it_ddt', 'view_ddt_create_invoice')

            self = self.with_context(active_ids=ddts.ids,
                                     ddt_date_from=wizard.date_from,
                                     ddt_date_to=wizard.date_to)
            return {
                'name': _('DDT Invoicing'),
                'context': self._context,
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_id': view[1],
                'res_model': 'ddt.create.invoice',
                'target': 'new'}
