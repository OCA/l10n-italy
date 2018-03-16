# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api


class MakeSettle(models.TransientModel):
    _inherit = 'sale.commission.make.settle'

    @api.multi
    def action_settle(self):
        self.ensure_one()
        res = super(MakeSettle, self).action_settle()
        settlement_obj = self.env['sale.commission.settlement']
        riba_line_model = self.env['riba.distinta.line']
        if 'type' in res and res['type'] != 'ir.actions.act_window_close':
            settlements = settlement_obj.browse(res['domain'][0][2])
            for settlement in settlements:
                # Check the configuration of the commission type and all
                # settlement lines of this settlement
                commission = settlement.agent.commission
                self.unlink_settlement_lines_by_commission(
                    commission, riba_line_model, settlement)
                if not settlement.lines:
                    settlement.unlink()
            # Refresh settlements list to be shown,
            # just close if there isn't any left
            settlements = settlements.exists()
            if settlements:
                res['domain'][0][2] = settlements.ids
            else:
                res = {'type': 'ir.actions.act_window_close'}
        return res

    @staticmethod
    def unlink_settlement_lines_by_commission(
            commission, riba_line_model, settlement):
        for settlement_line in settlement.lines:
            if commission.invoice_state == 'paid' \
                    and commission.only_paid_riba:
                # Check if invoice has RiBa payment method
                invoice = settlement_line.invoice
                if invoice.payment_term_id and invoice.payment_term_id.riba:
                    # Get Account moves of the payment for this invoice
                    payments = invoice.payment_move_line_ids
                    for payment in payments.mapped('move_id'):
                        # Check if linked RiBa line has been paid
                        riba_line = riba_line_model.search([
                            ('acceptance_move_id', '=', payment.id)])
                        if riba_line.state != 'paid':
                            # If RiBa hasn't been paid, delete current
                            # settlement line from settlement
                            settlement_line.unlink()
