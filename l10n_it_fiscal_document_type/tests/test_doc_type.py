# Copyright 2017 Lorenzo Battistini
# Copyright 2023 Simone Rubino - TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.test_mail.tests.common import mail_new_test_user
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase, users


class TestDocType(TransactionCase):

    def setUp(self):
        super(TestDocType, self).setUp()
        self.journalrec = self.env['account.journal'].search(
            [('type', '=', 'sale')])[0]
        self.doc_type_model = self.env['fiscal.document.type']
        self.TD01 = self.doc_type_model.search(
            [('code', '=', 'TD01')], limit=1)
        self.TD04 = self.doc_type_model.search(
            [('code', '=', 'TD04')], limit=1)
        self.inv_model = self.env['account.invoice']
        self.partner3 = self.env.ref('base.res_partner_3')
        self.fp = self.env["account.fiscal.position"].create({
            "name": "FP",
            "fiscal_document_type_id": self.TD01.id,
        })
        self.adviser = mail_new_test_user(
            self.env,
            login="Adviser",
            groups='account.group_account_manager',
        )

    def test_doc_type(self):
        self.TD01.journal_ids = [self.journalrec.id]
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        invoice._set_document_fiscal_type()
        self.assertEqual(invoice.fiscal_document_type_id.id, self.TD01.id)

        invoice2 = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        self.assertEqual(invoice2.fiscal_document_type_id.id, self.TD01.id)

    def test_doc_type_update(self):
        """Check that document type is updated when updating invoice type."""
        revenue_account_type = \
            self.env.ref('account.data_account_type_revenue')
        revenue_account = self.env['account.account'].search(
            [('user_type_id', '=', revenue_account_type.id)], limit=1)
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.env.ref('product.product_product_5').id,
                'quantity': 10.0,
                'account_id': revenue_account.id,
                'name': 'product test 5',
                'price_unit': 100.00,
            })]})
        self.assertEqual(invoice.fiscal_document_type_id, self.TD01)

        invoice.type = 'out_refund'
        self.assertEqual(invoice.fiscal_document_type_id, self.TD04)

    def test_doc_type_refund(self):
        self.TD01.journal_ids = [self.journalrec.id]
        invoice = self.inv_model.create({
            'partner_id': self.partner3.id
        })
        invoice._set_document_fiscal_type()
        refund = invoice.refund(
            invoice.date_invoice,
            invoice.date,
            'refund test',
            invoice.journal_id.id
        )
        self.assertEqual(refund.fiscal_document_type_id.id, self.TD04.id)

        invoice = self.inv_model.create({
            'partner_id': self.partner3.id,
            "fiscal_position_id": self.fp.id,
        })
        invoice._set_document_fiscal_type()
        refund = invoice.refund(
            invoice.date_invoice,
            invoice.date,
            'refund test',
            invoice.journal_id.id
        )
        self.assertEqual(refund.fiscal_document_type_id.id, self.TD04.id)

    @users("Adviser", "admin")
    def test_access(self):
        """Users can only read fiscal documents,
        Users can't create/update/delete fiscal documents."""
        # Arrange
        user = self.env.user
        doc_type_model = self.doc_type_model
        doc_type = self.TD01
        user_doc_type_model = doc_type_model.sudo(user=user.id)
        user_doc_type = user_doc_type_model.browse(doc_type.id)
        # pre-condition: user_* objects are linked to current user
        root_user = self.env.ref("base.user_root")
        self.assertEqual(doc_type_model.env.uid, root_user.id)
        self.assertEqual(doc_type.env.uid, root_user.id)
        self.assertEqual(user_doc_type.env.uid, user.id)
        self.assertEqual(user_doc_type_model.env.uid, user.id)

        # Act: Read
        code = user_doc_type.code

        # Assert: Read
        self.assertEqual(code, "TD01")

        # Act: Create
        with self.assertRaises(AccessError) as ae, self.env.cr.savepoint():
            user_doc_type_model.create({
                "code": "TC04",
                "name": "Test Code",
            })

        # Assert: Create
        exc_message = ae.exception.args[0]
        self.assertIn("not allowed", exc_message)
        self.assertIn("Operation: create", exc_message)
        self.assertIn("Document model: " + user_doc_type_model._name, exc_message)

        # Act: Update
        with self.assertRaises(AccessError) as ae, self.env.cr.savepoint():
            user_doc_type.name = "Update is forbidden"

        # Assert: Update
        exc_message = ae.exception.args[0]
        self.assertIn("not allowed", exc_message)
        self.assertIn("Operation: write", exc_message)
        self.assertIn("Document model: " + user_doc_type_model._name, exc_message)

        # Act: Delete
        with self.assertRaises(AccessError) as ae, self.env.cr.savepoint():
            user_doc_type.unlink()

        # Assert: Delete
        exc_message = ae.exception.args[0]
        self.assertIn("not allowed", exc_message)
        self.assertIn("Operation: unlink", exc_message)
        self.assertIn("Document model: " + user_doc_type_model._name, exc_message)
