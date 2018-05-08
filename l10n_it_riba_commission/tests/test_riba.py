# -*- coding: utf-8 -*-
# Copyright 2018 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import dateutil
from odoo import fields
from odoo.addons.l10n_it_ricevute_bancarie.tests.riba_common import (
    TestRibaCommon
)


class TestRiBa(TestRibaCommon):

    def setUp(self):
        super(TestRiBa, self).setUp()
        self.sale_order_model = self.env['sale.order']
        self.account_model = self.env['account.account']
        self.advance_inv_model = self.env['sale.advance.payment.inv']
        self.commission_model = self.env['sale.commission']
        self.settle_model = self.env['sale.commission.settlement']
        self.make_settle_model = self.env['sale.commission.make.settle']

        self.product = self.env['product.product'].search([], limit=1)
        self.riba_payment_term = self.env['account.payment.term'].create({
            'name': 'Ri.Ba. Immediate',
            'riba': True,
            'riba_payment_cost': 5.00,
            'line_ids': [
                (0, 0,
                 {'value': 'balance', 'option': 'day_after_invoice_date'})]
        })

        partners = self.env['res.partner'].search([], limit=3)
        self.partner = partners[0]

        paid_riba_commission = self.commission_model.create({
            'name': 'Only paid RiBa commission',
            'fix_qty': 20,
            'invoice_state': 'paid',
            'only_paid_riba': True
        })

        partners[1].write({
            'agent': True,
            'commission': paid_riba_commission.id
        })
        self.paid_riba_agent = partners[1]

        all_riba_commission = self.commission_model.create({
            'name': 'All RiBa commission',
            'fix_qty': 20,
            'invoice_state': 'paid',
            'only_paid_riba': False
        })
        partners[2].write({
            'agent': True,
            'commission': all_riba_commission.id
        })
        self.all_riba_agent = partners[2]
        self.account_user_type = self.env.ref(
            'account.data_account_type_receivable')

    def test_only_paid_riba(self):
        # Create and confirm sale order
        sale_order = self.sale_order_model.create({
            'partner_id': self.partner.id,
            'payment_term_id': self.riba_payment_term.id,
            'order_line': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 8.0,
                'qty_delivered': 1.0,
                'product_uom': self.product.uom_id.id,
                'price_unit': 100.0,
                'agents': [(0, 0, {
                    'agent': self.paid_riba_agent.id,
                    'commission': self.paid_riba_agent.commission.id
                })]
            })]
        })
        sale_order.action_confirm()

        # Generate the invoices
        payment = self.advance_inv_model.create({
            'advance_payment_method': 'all',
        })
        context = {"active_model": 'sale.order',
                   "active_ids": [sale_order.id],
                   "active_id": sale_order.id}
        payment.with_context(context).create_invoices()

        # Validate generated invoices
        for invoice in sale_order.invoice_ids:
            invoice.company_id.due_cost_service_id = self.service_due_cost.id
            invoice.action_invoice_open()

            # Issue the RiBa and confirm it, it will mark the invoice as paid
            riba_move_line_id = False
            for move_line in invoice.move_id.line_ids:
                if move_line.account_id.id == \
                        self.env.ref('l10n_generic_coa.1_conf_a_recv').id:
                    riba_move_line_id = move_line.id

            wizard_riba_issue = self.env['riba.issue'].create({
                'configuration_id': self.riba_config.id
            })
            action = wizard_riba_issue.with_context(
                {'active_ids': [riba_move_line_id]}
            ).create_list()
            riba_list_id = action and action['res_id'] or False
            riba_list = self.distinta_model.browse(riba_list_id)
            riba_list.confirm()
            self.assertEqual(riba_list.state, 'accepted')
            self.assertEqual(invoice.state, 'paid')

            # Generate settlements for agent, the settlement is not created
            wizard = self.make_settle_model.create(
                {'date_to':
                 (fields.Datetime.from_string(fields.Datetime.now()) +
                  dateutil.relativedelta.relativedelta(months=1))})
            wizard.action_settle()
            settlements = self.settle_model.search([('state', '=', 'settled')])
            self.assertEquals(len(settlements), 0)

            # Validate the RiBa
            amount = sum(line.amount for line in riba_list.line_ids)
            wiz_accreditation = self.env['riba.accreditation'].with_context({
                "active_model": "riba.distinta",
                "active_ids": [riba_list_id],
                "active_id": riba_list_id,
            }).create({
                'bank_amount': amount,
            })
            wiz_accreditation.create_move()
            self.assertEqual(riba_list.state, 'accredited')
            # bank notifies cash in
            bank_move = self.move_model.create({
                'journal_id': self.bank_journal.id,
                'line_ids': [
                    (0, 0, {
                        'partner_id': self.partner.id,
                        'account_id': self.sbf_effects.id,
                        'credit': amount,
                        'debit': 0,
                        'name': 'sbf effects',
                    }),
                    (0, 0, {
                        'partner_id': self.partner.id,
                        'account_id': self.riba_account.id,
                        'credit': 0,
                        'debit': amount,
                        'name': 'Banca conto ricevute bancarie',
                    }),
                ]
            })
            to_reconcile = self.env['account.move.line']
            line_set = (bank_move.line_ids | riba_list.acceptance_move_ids[
                0].line_ids)
            for line in line_set:
                if line.account_id.id == self.sbf_effects.id:
                    to_reconcile |= line
            self.assertEqual(len(to_reconcile), 2)
            to_reconcile.reconcile()
            # refresh otherwise riba_list.payment_ids is not recomputed
            riba_list.refresh()
            self.assertEqual(riba_list.state, 'paid')

            # Generate settlements for agent, the settlement is created
            wizard = self.make_settle_model.create(
                {'date_to': (
                    fields.Datetime.from_string(fields.Datetime.now()) +
                    dateutil.relativedelta.relativedelta(months=1))})
            wizard.action_settle()
            settlements = self.settle_model.search([('state', '=', 'settled')])
            self.assertEquals(len(settlements), 1)
