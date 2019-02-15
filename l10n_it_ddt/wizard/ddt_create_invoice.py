# Copyright 2014 Abstract (http://www.abstract.it)
# Copyright Davide Corio <davide.corio@abstract.it>
# Copyright 2014-2018 Agile Business Group (http://www.agilebg.com)
# Copyright 2015 Apulia Software s.r.l. (http://www.apuliasoftware.it)
# Copyright Francesco Apruzzese <f.apruzzese@apuliasoftware.it>
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _


class DdtCreateInvoice(models.TransientModel):
    _name = "ddt.create.invoice"
    _description = "Create invoice from TD"

    def _get_ddt_ids(self):
        return self.env['stock.picking.package.preparation'].browse(
            self.env.context['active_ids'])

    ddt_ids = fields.Many2many(
        'stock.picking.package.preparation', default=_get_ddt_ids)

    @api.multi
    def create_invoice(self):
        if self.ddt_ids:
            invoice_ids = self.ddt_ids.action_invoice_create()
            # ----- Show new invoices
            if invoice_ids:
                ir_model_data = self.env['ir.model.data']
                form_res = ir_model_data.get_object_reference(
                    'account', 'invoice_form')
                form_id = form_res and form_res[1] or False
                tree_res = ir_model_data.get_object_reference(
                    'account', 'invoice_tree')
                tree_id = tree_res and tree_res[1] or False
                return {
                    'name': _('Invoices from TD'),
                    'view_type': 'form',
                    'view_mode': 'form,tree',
                    'res_model': 'account.invoice',
                    'domain': [('id', 'in', invoice_ids)],
                    # 'res_id': ddt.id,
                    'view_id': False,
                    'views': [(tree_id, 'tree'), (form_id, 'form')],
                    'type': 'ir.actions.act_window',
                }
