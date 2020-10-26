# Copyright 2014-2019 Dinamiche Aziendali srl
# (http://www.dinamicheaziendali.it/)
# @author: Marco Calcagni <mcalcagni@dinamicheaziendali.it>
# @author: Gianmarco Conte <gconte@dinamicheaziendali.it>
# Copyright (c) 2019, Link IT Europe Srl
# @author: Matteo Bilotta <mbilotta@linkeurope.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from .stock_delivery_note import DATE_FORMAT


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    delivery_note_ids = \
        fields.Many2many('stock.delivery.note',
                         'stock_delivery_note_account_invoice_rel',
                         'invoice_id',
                         'delivery_note_id',
                         string="Delivery Notes", copy=False)

    delivery_note_count = \
        fields.Integer(compute='_compute_delivery_note_count')

    @api.multi
    def _compute_delivery_note_count(self):
        for invoice in self:
            invoice.delivery_note_count = len(invoice.delivery_note_ids)

    @api.multi
    def goto_delivery_notes(self, **kwargs):
        delivery_notes = self.mapped('delivery_note_ids')
        action = self.env.ref('l10n_it_delivery_note.'
                              'stock_delivery_note_action').read()[0]
        action.update(kwargs)

        if len(delivery_notes) > 1:
            action['domain'] = [('id', 'in', delivery_notes.ids)]

        elif len(delivery_notes) == 1:
            action['views'] = \
                [(self.env.ref('l10n_it_delivery_note.'
                               'stock_delivery_note_form_view').id, 'form')]
            action['res_id'] = delivery_notes.id

        else:
            action = {'type': 'ir.actions.act_window_close'}

        return action

    def goto_invoice(self, **kwargs):
        self.ensure_one()

        if self.type.startswith('out_'):
            view_id = self.env.ref('account.invoice_form').id

        else:
            view_id = False

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'res_id': self.id,
            'views': [(view_id, 'form')],
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            **kwargs
        }

    @api.multi
    def update_delivery_note_lines(self):
        context = {}

        for invoice in self.filtered(lambda i: i.delivery_note_ids):
            new_lines = []
            old_lines = \
                invoice.invoice_line_ids.filtered(lambda l: l.delivery_note_id)
            old_lines.unlink()

            #
            # TODO: Come bisogna comportarsi nel caso in
            #        cui il DdT non sia un DdT "valido"?
            #       Al momento, potrebbe essere possibile avere
            #       sia sei DdT senza numero (non ancora confermati)
            #       così come è possibile avere dei DdT senza, necessariamente,
            #       data di trasporto (non è un campo obbligatorio).
            #

            #
            # THIS ALLOWS TO CHANGE TRANSLATION LANGUAGE FOR EVERY INVOICE!
            #
            #   See: odoo/tools/translate.py -> 'def _get_lang(self, frame):'
            #
            context['lang'] = invoice.partner_id.lang

            for note in invoice.delivery_note_ids:
                new_lines.append((0, False, {
                    'sequence': 99, 'display_type': 'line_note',
                    'name':
                        _("""Delivery Note "{}" of {}""").
                        format(note.name, note.date.strftime(DATE_FORMAT)),
                    'delivery_note_id': note.id
                }))

            invoice.write({'invoice_line_ids': new_lines})


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    delivery_note_id = fields.Many2one('stock.delivery.note',
                                       string="Delivery Note",
                                       readonly=True, copy=False)
