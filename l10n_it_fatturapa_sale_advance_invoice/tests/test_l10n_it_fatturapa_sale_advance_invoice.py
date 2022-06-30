# Copyright 2022 Sergio Corato <https://github.com/sergiocorato>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import SavepointCase
from odoo.tools import mute_logger, safe_eval


class TestL10nItFatturapaSaleAdvanceInvoice(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.product_id = cls.env.ref('product.product_product_1')
        cls.product_id.invoice_policy = 'order'
        cls.journal_model = cls.env['account.journal']
        sale_journals = cls.journal_model.search([
            ('type', '=', 'sale')
        ])
        for sale_journal in sale_journals:
            sale_journal.advance_fiscal_document_type_id = \
                cls.env.ref('l10n_it_fiscal_document_type.9').id

    def _create_order(self):
        sale_order = self.env['sale.order'].create({
            'partner_id': self.env.ref('base.res_partner_3').id,
            'order_line': [
                (0, 0, {
                    'product_id': self.product_id.id,
                    'product_uom_qty': 5,
                }),
            ]
        })
        sale_order.action_confirm()
        return sale_order

    @mute_logger(
        'odoo.models', 'odoo.models.unlink', 'odoo.addons.base.ir.ir_model'
    )
    def test_create_advance_invoice(self):
        sale_order = self._create_order()
        wizard_obj = self.env['sale.advance.payment.inv']
        wizard_vals = wizard_obj.default_get(
            ['advance_payment_method']
        )
        wizard_vals.update({
            'advance_payment_method': 'percentage',
            'amount': 10.0})
        context = {"active_model": 'sale.order',
                   "active_ids": [sale_order.id],
                   "active_id": sale_order.id}
        wizard = wizard_obj.with_context(context).create(wizard_vals)
        res = wizard.with_context(open_invoices=True).create_invoices()
        domain = safe_eval(res.get('domain'))
        model = res.get('res_model')
        res_id = res.get('res_id')
        domain.append(('id', '=', res_id))
        invoices = self.env[model].search(domain)
        self.assertTrue(len(invoices), 1)
        invoice = invoices[0]
        self.assertEqual(invoice.fiscal_document_type_id,
                         invoice.journal_id.advance_fiscal_document_type_id)

    @mute_logger(
        'odoo.models', 'odoo.models.unlink', 'odoo.addons.base.ir.ir_model'
    )
    def test_create_invoice(self):
        sale_order = self._create_order()
        wizard_obj = self.env['sale.advance.payment.inv']
        wizard_vals = wizard_obj.default_get(
            ['advance_payment_method']
        )
        wizard_vals.update({
            'advance_payment_method': 'all'
        })
        context = {"active_model": 'sale.order',
                   "active_ids": [sale_order.id],
                   "active_id": sale_order.id}
        wizard = wizard_obj.with_context(context).create(wizard_vals)
        res = wizard.with_context(open_invoices=True).create_invoices()
        domain = safe_eval(res.get('domain'))
        model = res.get('res_model')
        res_id = res.get('res_id')
        domain.append(('id', '=', res_id))
        invoices = self.env[model].search(domain)
        self.assertTrue(len(invoices), 1)
        invoice = invoices[0]
        self.assertNotEqual(invoice.fiscal_document_type_id,
                            invoice.journal_id.advance_fiscal_document_type_id)
