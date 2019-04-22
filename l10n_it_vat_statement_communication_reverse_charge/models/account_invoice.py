# -*- coding: utf-8 -*-

from odoo import models, api


class Invoice(models.Model):
    _inherit = 'account.invoice'

    def generate_self_invoice(self):
        return super(Invoice, self.with_context(
            exclude_from_vat_statement_amount=True)).generate_self_invoice()

    @api.model
    def invoice_line_move_line_get(self):
        # solamente l'imponibile non deve essere incluso nella comunicazione
        # (VP2); l'imposta va inclusa.
        # Quindi modifichiamo solo la move.line dell'imponibile
        res = super(Invoice, self).invoice_line_move_line_get()
        if self.env.context.get('exclude_from_vat_statement_amount'):
            for move_line_dict in res:
                move_line_dict['exclude_from_vat_statement_amount'] = True
        return res

    @api.model
    def line_get_convert(self, line, part):
        res = super(Invoice, self).line_get_convert(line, part)
        if 'exclude_from_vat_statement_amount' in line:
            res['exclude_from_vat_statement_amount'] = line[
                'exclude_from_vat_statement_amount']
        return res
