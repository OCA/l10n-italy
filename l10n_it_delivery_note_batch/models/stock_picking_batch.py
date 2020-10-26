# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    delivery_note_ids = fields.One2many(
        'stock.delivery.note', 'stock_picking_batch_id',
        string='Delivery Notes', copy=False)

    delivery_note_count = \
        fields.Integer(compute='_compute_delivery_note_count')

    @api.multi
    def _compute_delivery_note_count(self):
        for rec in self:
            rec.delivery_note_count = len(rec.delivery_note_ids)

    @api.multi
    def create_delivery_notes(self, **kwargs):
        for rec in self:
            if rec.state != 'done':
                # TODO check state - when are we allowed to
                # create draft delivery notes?
                pass

            # select only pickings that don't already have a delivery note
            # TODO state check on individual pickings?
            pickings = rec.mapped('picking_ids').search(
                [('delivery_note_id', '=', False), ('batch_id', '=', rec.id)])

            # poor man's group by - group by homogeneous pickings
            todo_list = {}
            for p in pickings:
                key = tuple(p.id for p in p.get_partners())
                todo_list[key] = todo_list.get(key,
                                               self.env['stock.picking']) | p
            type_id = self.env['stock.delivery.note.type'].search([
                ('code', '=', rec.picking_type_id.code)
            ], limit=1)

            for partner_ids, pickings in todo_list.items():
                dn = self.env['stock.delivery.note'].create({
                    'partner_sender_id': partner_ids[0],
                    'partner_id': partner_ids[1],
                    'partner_shipping_id': partner_ids[1],
                    'stock_picking_batch_id': rec.id,
                    'type_id': type_id.id,
                })
                pickings.write({'delivery_note_id': dn.id})

        return self.goto_delivery_notes(**kwargs)

    @api.multi
    def goto_delivery_notes(self, **kwargs):
        delivery_notes = self.mapped('delivery_note_ids')
        action = self.env.ref(
            'l10n_it_delivery_note.stock_delivery_note_action').read()[0]
        action.update(kwargs)

        if len(delivery_notes) > 1:
            action['domain'] = [('id', 'in', delivery_notes.ids)]

        elif len(delivery_notes) == 1:
            action['views'] = [(
                self.env.ref(
                    'l10n_it_delivery_note.stock_delivery_note_form_view'
                ).id, 'form'
            )]
            action['res_id'] = delivery_notes.id

        else:
            action = {'type': 'ir.actions.act_window_close'}

        return action
