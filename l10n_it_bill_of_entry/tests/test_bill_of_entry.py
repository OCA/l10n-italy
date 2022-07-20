# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2017 CQ Creativi Quadrati (http://www.creativiquadrati.it)
#    @author Diego Bruselli <d.bruselli@creativiquadrati.it>
#
#    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################

from odoo.tests.common import TransactionCase


class TestBillOfEntry(TransactionCase):

    def _get_invline_vals(self, product, quantity=1., price_unit=1.):
        vals = {
            'product_id': product.id,
            'quantity': quantity,
            'price_unit': price_unit,
        }
        return vals

    def _create_invoice(self, partner, customs_doc_type, journal):
        vals = {
            'type': 'in_invoice',
            'partner_id': partner.id,
        }
        if customs_doc_type:
            vals['customs_doc_type'] = customs_doc_type
        if journal:
            vals['journal_id'] = journal.id
        invoice = self.env['account.invoice'].create(vals)
        invoice._onchange_partner_id()
        invoice._onchange_journal_id()
        invoice._convert_to_write(invoice._cache)
        return invoice

    def _create_invoice_line(self, invoice, vals):
        new_vals = {
            'invoice_id': invoice.id,
            'account_id': self.account_revenue.id,
            'name': 'something in',
        }
        vals.update(new_vals)
        line = self.env['account.invoice.line'].create(vals)
        line._onchange_product_id()
        line._convert_to_write(line._cache)
        return line

    def setUp(self):
        super(TestBillOfEntry, self).setUp()

        self.account_model = self.env['account.account']
        self.tax_model = self.env['account.tax']
        self.journal_model = self.env['account.journal']
        self.invoice_model = self.env['account.invoice']
        self.inv_line_model = self.env['account.invoice.line']
        self.move_line_model = self.env['account.move.line']
        self.fp_model = self.env['account.fiscal.position']
        self.fp_tax_model = self.env['account.fiscal.position.tax']

        # Default accounts for invoice line account_id
        revenue_acctype_id = self.env.ref(
            'account.data_account_type_revenue'
        ).id
        self.account_revenue = self.account_model.search(
            [('user_type_id', '=', revenue_acctype_id)], limit=1
        )
        # Default purchase journal
        self.journal = self.journal_model.search(
            [('type', '=', 'purchase')], limit=1
        )
        self.journal.update_posted = True
        # Extra EU purchase journal for differentiate
        # extra EU purchase invoices from ordinary ones
        self.extra_journal = self.env.ref(
            'l10n_it_bill_of_entry.account_journal_purchase_extraEU'
        )
        # Bill of entry storno journal
        self.company = self.env.ref('base.main_company')
        self.bill_of_entry_journal = self.journal_model.create({
            'name': 'bill_of_entry_journal',
            'type': 'general',
            'code': 'BOE',
            'update_posted': True
        })
        self.company.bill_of_entry_journal_id = self.bill_of_entry_journal.id

        # Extra EU fiscal position tax correspondence
        self.tax22 = self.tax_model.create({
            'name': '22%',
            'amount': 22,
            'amount_type': 'percent',
            'type_tax_use': 'purchase',
            'tax_group_id': self.env.ref('account.tax_group_taxes').id
        })
        self.fiscpos_extra = self.env.ref(
            'l10n_it_bill_of_entry.fiscal_position_extraEU'
        )
        self.fp_tax_model.create({
            'position_id': self.fiscpos_extra.id,
            'tax_src_id': self.tax22.id,
        })

        # Delivery Expense account
        self.account_delivery_expense = \
            self.env.ref('l10n_it_bill_of_entry.account_account_delivery_expense')

        # Extra EU purchase journal
        self.journal_extra = \
            self.env.ref('l10n_it_bill_of_entry.account_journal_purchase_extraEU')

        # Products
        self.product1 = self.env.ref('product.product_delivery_01')
        self.product1.write({
            'supplier_taxes_id': [(6, 0, [self.tax22.id])],
        })
        self.tax_22extraUE = self.env.ref('l10n_it_bill_of_entry.tax_22extraUE')
        self.product_extra = \
            self.env.ref('l10n_it_bill_of_entry.product_product_extraEU_purchase')
        self.product_extra.supplier_taxes_id = [(6, 0, self.tax_22extraUE.ids)]
        self.adv_customs_expense = \
            self.env.ref('l10n_it_bill_of_entry.product_product_adv_customs_expense')
        self.customs_expense = \
            self.env.ref('l10n_it_bill_of_entry.product_product_customs_expense')
        self.product_delivery = \
            self.env.ref('l10n_it_bill_of_entry.product_product_delivery')
        self.product_delivery.supplier_taxes_id = [(6, 0, [self.tax22.id])]
        self.product_stamp = \
            self.env.ref('l10n_it_bill_of_entry.product_product_stamp_duties')

        # Partners
        self.customs = self.env.ref('l10n_it_bill_of_entry.partner_customs')
        self.supplier = self.env.ref('base.res_partner_1')
        self.supplier.property_account_position_id = \
            self.fiscpos_extra.id
        self.forwarder = self.env.ref('base.res_partner_12')

        # Extra EU supplier invoice - draft state
        self.supplier_invoice = self._create_invoice(
            self.supplier, 'supplier_invoice', self.journal_extra
        )
        line_vals = self._get_invline_vals(self.product1, 1, 2500)
        self._create_invoice_line(self.supplier_invoice, line_vals)
        self.supplier_invoice.compute_taxes()
        # self.supplier_invoice.action_invoice_open()

        # Bill of Entry - draft state
        self.bill_of_entry = self._create_invoice(
            self.customs, 'bill_of_entry', self.journal
        )
        line_vals = self._get_invline_vals(self.product_extra, 1, 2500)
        self._create_invoice_line(self.bill_of_entry, line_vals)
        self.bill_of_entry.compute_taxes()
        self.bill_of_entry.write({
            'supplier_invoice_ids': [(6, 0, [self.supplier_invoice.id])]
        })
        # self.bill_of_entry.action_invoice_open()

        # Forwarder Invoice - draft state
        self.forwarder_invoice = self._create_invoice(
            self.forwarder, 'forwarder_invoice', self.journal
        )
        line_vals = self._get_invline_vals(self.product_delivery, 1, 300)
        self._create_invoice_line(self.forwarder_invoice, line_vals)
        line_vals = self._get_invline_vals(
            self.adv_customs_expense, 1, 550
        )
        self.adv_customs_expense_line = self._create_invoice_line(
            self.forwarder_invoice, line_vals
        )
        self.adv_customs_expense_line.advance_customs_vat = True
        self.adv_customs_expense_line.invoice_line_tax_ids = [(6, 0, [])]
        self.forwarder_invoice.compute_taxes()
        self.forwarder_invoice.write({
            'forwarder_bill_of_entry_ids': [(4, self.bill_of_entry.id)],
        })

    def test_storno_create(self):

        # Validate bill of entry
        self.bill_of_entry.action_invoice_open()

        # Validate forwarder invoice
        self.forwarder_invoice.action_invoice_open()

        # Storno Bill of Entry account.move
        storno = self.forwarder_invoice.bill_of_entry_storno_id
        self.assertTrue(storno)
        self.assertEqual(storno.date, self.forwarder_invoice.date_invoice)

        # Advance Customs Expense account.move.line
        move_line_domain = [
            ('account_id', '=', self.adv_customs_expense_line.account_id.id),
            ('debit', '=', 0.),
            ('credit', '=', self.adv_customs_expense_line.price_subtotal),
            ('partner_id', '=', self.adv_customs_expense_line.partner_id.id),
            ('product_id', '=', self.adv_customs_expense_line.product_id.id)
        ]
        adv_customs_expense_moveline = \
            self.move_line_model.search(move_line_domain)
        self.assertEqual(len(adv_customs_expense_moveline), 1)

        # Customs Expense account.move.lines
        move_line_domain = [
            ('account_id', '=', self.bill_of_entry.account_id.id),
            ('debit', '=', self.bill_of_entry.amount_total),
            ('credit', '=', 0.),
            ('partner_id', '=', self.bill_of_entry.partner_id.id)
        ]
        customs_expense_moveline = \
            self.move_line_model.search(move_line_domain)
        self.assertEqual(len(customs_expense_moveline), 1)

        # Extra EU goods purchase account.move.lines
        for boe_line in self.bill_of_entry.invoice_line_ids:
            move_line_domain = [
                ('account_id', '=', boe_line.account_id.id),
                ('debit', '=', 0.),
                ('credit', '=', boe_line.price_subtotal),
                ('partner_id', '=', boe_line.partner_id.id),
                ('product_id', '=', boe_line.product_id.id)
            ]
            extraeu_expense_moveline = \
                self.move_line_model.search(move_line_domain)
            self.assertEqual(len(extraeu_expense_moveline), 1)

        # Storno - BoE reconciliation (supplier debit account)
        storno_reconcile_ids = storno.line_ids.filtered(
            lambda l: l.full_reconcile_id
        ).mapped('full_reconcile_id').ids
        boe_reconcile_ids = self.bill_of_entry.move_id.line_ids.filtered(
            lambda l: l.full_reconcile_id
        ).mapped('full_reconcile_id').ids
        self.assertEqual(
            sorted(storno_reconcile_ids),
            sorted(boe_reconcile_ids)
        )
