from odoo.tests.common import TransactionCase


class ReverseChargeCommon(TransactionCase):

    def setUp(self):
        super(ReverseChargeCommon, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.invoice_line_model = self.env['account.invoice.line']
        self.partner_model = self.env['res.partner']

        self._create_account()
        self._create_taxes()
        self._create_journals()
        self._create_rc_types()
        self._create_rc_type_taxes()
        self._create_fiscal_position()

        self.sample_product = self.env.ref("product.product_product_4d")
        self.supplier_extraEU = self.partner_model.create({
            'name': 'Extra EU supplier',
            'customer': False,
            'supplier': True,
            'property_account_position_id': self.fiscal_position_extra.id
        })
        self.supplier_intraEU = self.partner_model.create({
            'name': 'Intra EU supplier',
            'customer': False,
            'supplier': True,
            'property_account_position_id': self.fiscal_position_intra.id
        })
        self.supplier_intraEU_exempt = self.partner_model.create({
            'name': 'Intra EU supplier exempt',
            'customer': False,
            'supplier': True,
            'property_account_position_id': self.fiscal_position_exempt.id
        })
        self.invoice_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_payable').id)], limit=1).id
        self.invoice_line_account = self.env['account.account'].search(
            [('user_type_id', '=', self.env.ref(
                'account.data_account_type_expenses').id)], limit=1).id
        self.term_15_30 = self.env['account.payment.term'].create({
            'name': '15 30',
            'line_ids': [
                (0, 0, {
                    'value': 'percent',
                    'value_amount': 50,
                    'days': 15,
                    'sequence': 1,
                }),
                (0, 0, {
                    'value': 'balance',
                    'days': 30,
                    'sequence': 2,
                })]})
        self.env['account.journal'].search(
            [('name', '=', 'Customer Invoices')]).update_posted = True

    def _create_account(self):
        account_model = self.env['account.account']
        self.account_selfinvoice = account_model.create({
            'code': '295000',
            'name': 'selfinvoice temporary',
            'user_type_id': self.env.ref(
                'account.data_account_type_current_liabilities').id
        })

    def _create_taxes(self):
        tax_model = self.env['account.tax']
        self.tax_22ae = tax_model.create({
            'name': "Tax 22% Purchase Extra-EU",
            'type_tax_use': 'purchase',
            'amount': 22
        })
        self.tax_22ai = tax_model.create({
            'name': "Tax 22% Purchases Intra-EU",
            'type_tax_use': 'purchase',
            'amount': 22
        })
        self.tax_22vi = tax_model.create({
            'name': "Tax 22% Sales Intra-EU",
            'type_tax_use': 'sale',
            'amount': 22
        })
        self.tax_22ve = tax_model.create({
            'name': "Tax 22% Sales Extra-EU",
            'type_tax_use': 'sale',
            'amount': 22
        })
        self.tax_22 = tax_model.create({
            'name': "Tax 22%",
            'type_tax_use': 'purchase',
            'amount': 22
        })
        self.tax_0_pur = tax_model.create({
            'name': "Tax 0%",
            'type_tax_use': 'purchase',
            'amount': 0
        })
        self.tax_0_sal = tax_model.create({
            'name': "Tax 0%",
            'type_tax_use': 'sale',
            'amount': 0
        })

    def _create_journals(self):
        journal_model = self.env['account.journal']
        self.journal_selfinvoice = journal_model.create({
            'name': 'selfinvoice',
            'type': 'sale',
            'code': 'SLF',
            'update_posted': True
        })

        self.journal_reconciliation = journal_model.create({
            'name': 'RC reconciliation',
            'type': 'bank',
            'code': 'SLFRC',
            'default_credit_account_id': self.account_selfinvoice.id,
            'default_debit_account_id': self.account_selfinvoice.id,
            'update_posted': True
        })

        self.journal_selfinvoice_extra = journal_model.create({
            'name': 'Extra Selfinvoice',
            'type': 'sale',
            'code': 'SLFEX',
            'update_posted': True
        })

        self.journal_cee_extra = journal_model.create({
            'name': 'Extra CEE',
            'type': 'purchase',
            'code': 'EXCEE',
            'update_posted': True
        })

    def _create_rc_types(self):
        rc_type_model = self.env['account.rc.type']
        self.rc_type_ieu = rc_type_model.create({
            'name': 'Intra EU (selfinvoice)',
            'method': 'selfinvoice',
            'partner_type': 'supplier',
            'journal_id': self.journal_selfinvoice.id,
            'payment_journal_id': self.journal_reconciliation.id,
            'transitory_account_id': self.account_selfinvoice.id
        })

        self.rc_type_eeu = rc_type_model.create({
            'name': 'Extra EU (selfinvoice)',
            'method': 'selfinvoice',
            'partner_type': 'other',
            'with_supplier_self_invoice': True,
            'partner_id': self.env.ref('base.main_partner').id,
            'journal_id': self.journal_selfinvoice_extra.id,
            'supplier_journal_id': self.journal_cee_extra.id,
            'payment_journal_id': self.journal_reconciliation.id,
            'transitory_account_id': self.account_selfinvoice.id
        })

        self.rc_type_exempt = rc_type_model.create({
            'name': 'Intra EU (exempt)',
            'method': 'selfinvoice',
            'partner_type': 'supplier',
            'journal_id': self.journal_selfinvoice.id,
            'payment_journal_id': self.journal_reconciliation.id,
            'transitory_account_id': self.account_selfinvoice.id
        })

    def _create_rc_type_taxes(self):
        rc_type_tax_model = self.env['account.rc.type.tax']
        self.rc_type_tax_ieu = rc_type_tax_model.create({
            'rc_type_id': self.rc_type_ieu.id,
            'purchase_tax_id': self.tax_22ai.id,
            'sale_tax_id': self.tax_22vi.id
        })

        self.rc_type_tax_eeu = rc_type_tax_model.create({
            'rc_type_id': self.rc_type_eeu.id,
            'original_purchase_tax_id': self.tax_0_pur.id,
            'purchase_tax_id': self.tax_22ae.id,
            'sale_tax_id': self.tax_22ve.id
        })

        self.rc_type_tax_exempt = rc_type_tax_model.create({
            'rc_type_id': self.rc_type_exempt.id,
            'purchase_tax_id': self.tax_0_pur.id,
            'sale_tax_id': self.tax_0_sal.id
        })

    def _create_fiscal_position(self):
        model_fiscal_position = self.env['account.fiscal.position']
        self.fiscal_position_intra = model_fiscal_position.create({
            'name': 'Intra EU',
            'rc_type_id': self.rc_type_ieu.id
        })

        self.fiscal_position_extra = model_fiscal_position.create({
            'name': 'Extra EU',
            'rc_type_id': self.rc_type_eeu.id
        })

        self.fiscal_position_exempt = model_fiscal_position.create({
            'name': 'Intra EU exempt',
            'rc_type_id': self.rc_type_exempt.id
        })
