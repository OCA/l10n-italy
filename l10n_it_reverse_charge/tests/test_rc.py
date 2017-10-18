# -*- coding: utf-8 -*-
# © 2016 Davide Corio (Abstract)
# Copyright 2017 Alex Comba - Agile Business Group
# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2017 Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import time
from odoo.tests.common import TransactionCase


class ReverseChargeCase(TransactionCase):

    def setUp(self):
        super(ReverseChargeCase, self).setUp()
        tax_model = self.env['account.tax']
        fp_model = self.env['account.fiscal.position']
        fp_tax_model = self.env['account.fiscal.position.tax']
        invoice_model = self.env['account.invoice']
        account_model = self.env['account.account']
        rc_fp = self.env.ref('l10n_it_reverse_charge.rc_fp_0')
        tax_22a = tax_model.create({
            'name': "Tax 22% Purchase",
            'type_tax_use': 'purchase',
            'amount': '22.00'
            })

        tax_22aieu = tax_model.create({
            'name': "Tax 22% Purchases I-EU",
            'type_tax_use': 'purchase',
            'amount': '22.00'
            })

        tax_22vieu = tax_model.create({
            'name': "Tax 22% Sales I-EU",
            'type_tax_use': 'purchase',
            'amount': '-22.00'
            })

        tax_22ieu = tax_model.create({
            'name': "Tax 22% I-EU",
            'type_tax_use': 'purchase',
            'amount_type': 'group',
            'amount': 0,
            'children_tax_ids': [(6, 0, [tax_22aieu.id, tax_22vieu.id])],
            })

        # adding Intra-EU fiscal position
        rc_fp = fp_model.create({
            'name': 'Intra-EU Purchases',
            'rc_type_id': self.env.ref(
                'l10n_it_reverse_charge.account_rc_type_1').id,
            })
        # adding tax mapping
        fp_tax_model.create({
            'position_id': rc_fp.id,
            'tax_src_id': tax_22a.id,
            'tax_dest_id': tax_22ieu.id
            })

        # adding a new vendor bill
        account = account_model.search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_expenses').id)], limit=1)
        rc_bill_data = {
            'company_id': self.env.ref('base.main_company').id,
            'fiscal_position_id': rc_fp.id,
            'partner_id': self.env.ref('base.res_partner_2').id,
            'user_id': self.env.ref('base.user_demo').id,
            'type': 'in_invoice',
            'date_invoice': time.strftime('%Y-%m')+'-01',
            'invoice_line_ids': [(0, 0, {
                'account_id': account.id,
                'quantity': 1,
                'price_unit': 100.0,
                'product_id': self.env.ref('product.product_order_01').id,
                'name': self.env.ref('product.product_order_01').name,
                'uom_id': self.env.ref('product.product_uom_unit').id,
                'invoice_line_tax_ids': [(6, 0, [tax_22ieu.id])]
                })]
            }
        self.rc_bill = invoice_model.create(rc_bill_data)

    def test_intraue_rc(self):
        self.rc_bill.action_invoice_open()
        tax_1_amount = self.rc_bill.tax_line_ids[0].amount
        tax_2_amount = self.rc_bill.tax_line_ids[1].amount
        self.assertTrue((tax_1_amount + tax_2_amount == 0), "Wrong VAT amount")
