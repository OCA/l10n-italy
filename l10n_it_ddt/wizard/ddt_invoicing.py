# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import Warning as UserError


class DdtInvoicing(models.TransientModel):
    _name = "ddt.invoicing"

    @api.model
    def _default_journal(self):
        return self.env['account.journal'].search([('type', '=', 'sale')],
                                                  order='id', limit=1)
    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    journal_id = fields.Many2one('account.journal', string='Journal',
                                 default=_default_journal,
                                 domain=[('type', '=', 'sale')])
    date_invoice = fields.Date(string='Invoice Date')

    @api.multi
    def create_invoices(self):
        for wizard in self:
            domain = [('to_be_invoiced', '=', True),
                      ('invoice_id', '=', False),
                      ('state', '=', 'done'),
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
                                     ddt_date_to=wizard.date_to,
                                     invoice_date=wizard.date_invoice,
                                     invoice_journal_id=wizard.journal_id.id,
                                     )
            return {
                'name': _('DDT Invoicing'),
                'context': self._context,
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_id': view[1],
                'res_model': 'ddt.create.invoice',
                'target': 'new'}
