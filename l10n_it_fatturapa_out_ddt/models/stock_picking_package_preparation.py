# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Francesco Apruzzese
#    Copyright 2015 Apulia Software srl
#    Copyright 2015 Lorenzo Battistini - Agile Business Group
#    Copyright 2018 Giuseppe Stoduto
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, exceptions, _
import openerp.addons.decimal_precision as dp
from openerp.report import report_sxw

class StockPickingPackagePreparationLine(models.Model):

    _inherit = 'stock.picking.package.preparation.line'

    sale_line_id = fields.Many2one(
        related='move_id.procurement_id.sale_line_id',
        string='Sale order line',
        store=True, readonly=True)
    price_unit = fields.Float('Unit Price', digits=dp.get_precision(
        'Product Price'), default=0.0)
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    discount = fields.Float(
        string='Discount (%)', digits=dp.get_precision('Discount'),
        default=0.0)

    def _prepare_lines_from_pickings(self, picking_ids):
        """
        Add values used for invoice creation
        """
        lines = super(StockPickingPackagePreparationLine, self).\
            _prepare_lines_from_pickings(picking_ids)
        for line in lines:
            sale_line = False
            if line['move_id']:
                move = self.env['stock.move'].browse(line['move_id'])
                sale_line = move.procurement_id.sale_line_id or False
            if sale_line:
                line['price_unit'] = sale_line.price_unit or 0
                line['discount'] = sale_line.discount or 0
                line['tax_ids'] = [(6, 0, [x.id]) for x in sale_line.tax_id]

        return lines

    def quantity_by_lot(self):
        rml_parser = report_sxw.rml_parse(self.env.cr,self.env.uid, 'reconciliation_widget_asl', context=self._context)
        res = {}
        for quant in self.move_id.quant_ids:
            if quant.lot_id:
                if quant.location_id.id == self.move_id.location_dest_id.id:
                    if quant.lot_id not in res:
                        res[quant.lot_id] = quant.qty
                    else:
                        res[quant.lot_id] += quant.qty
        for lot in res:
            if lot.product_id.track_all and lot.product_id.track_outgoing:
                res[lot] = rml_parser.formatLang(self.env, res[lot])
            else:
                # If not tracking by lots, quantity is not relevant
                res[lot] = False
        return res


class StockPickingPackagePreparation(models.Model):

    _inherit = 'stock.picking.package.preparation'

    @api.multi
    @api.depends('picking_ids.invoice_state')
    def _compute_to_be_invoiced(self):
        for ddt in self:
            for picking in ddt.picking_ids:
                if picking.invoice_state == 'none' or picking.invoice_state == 'invoiced':
                    ddt.to_be_invoiced = False
                    break
                else:
                    ddt.to_be_invoiced = True

    show_price = fields.Boolean(string='Show prices on report')
    to_be_invoiced = fields.Boolean(
        string='To be Invoiced', store=True, compute="_compute_to_be_invoiced",
        help="It depends on the 'invoice control' field in picking. "
              "True if 'To Be Invoice' is set."
              "Save to see the changes")

    def _compute_weight(self):
        res = super(StockPickingPackagePreparation, self)._compute_weight()
        package = self.package_id
        package_model = self.env['stock.quant.package']
        quant_model = self.env['stock.quant']
        quants = quant_model.browse(package.get_content())
        child_packages = package_model.search([('id', 'child_of', package.id)])
        tare_weight = sum(child_packages.mapped('ul_id.weight'))
        if not tare_weight:
            net_weight = sum(l.product_id.weight_net * l.qty for l in quants)
            self.net_weight = net_weight
        return res

    @api.onchange('partner_id', 'ddt_type_id')
    def on_change_partner(self):
        res = super(StockPickingPackagePreparation, self).on_change_partner()
        self.show_price = self.partner_id.ddt_show_price
        return res

    @api.multi
    def action_put_in_pack(self):
        for package in self:
            for picking in package.picking_ids:
                if picking.invoice_state == 'none':
                    raise exceptions.Warning(
                        _('The movement "%s" are not billable') % picking.name)
        return super(StockPickingPackagePreparation, self).action_put_in_pack()

    # Uncomment to activate the manual movements
    # @api.multi
    # def action_done(self):
    #     for picking in self.picking_ids:
    #         if picking.state != 'done':
    #             raise exceptions.Warning(
    #                 _("Not every picking is in done status"))
    #     for package in self:
    #         if not package.ddt_number:
    #             package.ddt_number = (
    #                 package.ddt_type_id.sequence_id.next_by_id(
    #                     package.ddt_type_id.sequence_id.id)
    #             )
    #     self.write({'state': 'done', 'date_done': fields.Datetime.now()})
    #     return True


    @api.multi
    def action_send_ddt_mail(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.\
                get_object_reference('l10n_it_fatturapa_out_ddt',
                                     'email_template_edi_ddt')[1]
        except ValueError:
            template_id = False

        try:
            compose_form_id = ir_model_data.\
                get_object_reference('mail',
                                     'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        ctx = {
            'default_model': 'stock.picking.package.preparation',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'mark_so_as_sent': True,
            'custom_layout':
                "l10n_it_fatturapa_out_ddt.mail_template_data_notification_email_ddt"
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
