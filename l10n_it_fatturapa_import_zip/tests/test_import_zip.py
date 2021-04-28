import base64
import tempfile
from datetime import datetime

from odoo.modules import get_module_resource
from odoo.tests.common import TransactionCase


class TestImportZIP(TransactionCase):
    def setUp(self):
        super(TestImportZIP, self).setUp()
        self.attach_model = self.env["fatturapa.attachment.import.zip"]
        self.cleanPartners()
        arrotondamenti_attivi_account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_other_income").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        arrotondamenti_passivi_account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_direct_costs").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        arrotondamenti_tax_id = self.env["account.tax"].search(
            [("type_tax_use", "=", "purchase"), ("amount", "=", 0.0)],
            order="sequence",
            limit=1,
        )
        self.env.company.arrotondamenti_attivi_account_id = (
            arrotondamenti_attivi_account_id
        )
        self.env.company.arrotondamenti_passivi_account_id = (
            arrotondamenti_passivi_account_id
        )
        self.env.company.arrotondamenti_tax_id = arrotondamenti_tax_id
        account_payable = self.env["account.account"].create(
            {
                "name": "Test WH tax",
                "code": "whtaxpay2",
                "user_type_id": self.env.ref("account.data_account_type_payable").id,
                "reconcile": True,
            }
        )
        account_receivable = self.env["account.account"].create(
            {
                "name": "Test WH tax",
                "code": "whtaxrec2",
                "user_type_id": self.env.ref("account.data_account_type_receivable").id,
                "reconcile": True,
            }
        )
        self.env["withholding.tax"].create(
            {
                "name": "1040",
                "code": "1040",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 20.0})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            }
        )
        self.env["withholding.tax"].create(
            {
                "name": "Enasarco",
                "code": "TC07",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref("account.account_payment_term_advance").id,
                "wt_types": "enasarco",
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.r").id,
                "rate_ids": [
                    (
                        0,
                        0,
                        {
                            "tax": 1.57,
                            "base": 1.0,
                        },
                    )
                ],
            }
        )
        self.env["withholding.tax"].create(
            {
                "name": "Enasarco 8,50",
                "code": "TC07",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref("account.account_payment_term_advance").id,
                "wt_types": "enasarco",
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.r").id,
                "rate_ids": [
                    (
                        0,
                        0,
                        {
                            "tax": 8.5,
                            "base": 1.0,
                        },
                    )
                ],
            }
        )
        self.env["withholding.tax"].create(
            {
                "name": "1040/3",
                "code": "1040",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref("account.account_payment_term_advance").id,
                "wt_types": "ritenuta",
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
                "rate_ids": [
                    (
                        0,
                        0,
                        {
                            "tax": 11.50,
                            "base": 1.0,
                        },
                    )
                ],
            }
        )
        self.env["withholding.tax"].create(
            {
                "name": "1040 R",
                "code": "1040R",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref("account.account_payment_term_advance").id,
                "wt_types": "ritenuta",
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.r").id,
                "rate_ids": [
                    (
                        0,
                        0,
                        {
                            "tax": 11.50,
                            "base": 1.0,
                        },
                    )
                ],
            }
        )

        self.env["withholding.tax"].create(
            {
                "name": "2320",
                "code": "2320",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 23.0, "base": 0.2})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            }
        )

        self.env["withholding.tax"].create(
            {
                "name": "2320",
                "code": "2320",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 23.0, "base": 0.5})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            }
        )

        self.env["withholding.tax"].create(
            {
                "name": "2620q",
                "code": "2620q",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 26.0, "base": 0.2})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

        self.env["withholding.tax"].create(
            {
                "name": "2640q",
                "code": "2640q",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 26.0, "base": 0.4})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

        self.env["withholding.tax"].create(
            {
                "name": "2720q",
                "code": "2720q",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 27.0, "base": 0.2})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

        self.env["withholding.tax"].create(
            {
                "name": "4q",
                "code": "4q",
                "wt_types": "enasarco",
                "account_receivable_id": account_receivable.id,
                "account_payable_id": account_payable.id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 4.0, "base": 1.0})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

        AED = self.env.ref("base.AED")
        AED.active = True

    def cleanPartners(self):
        # VAT number used in tests, assigned to other partners by demo data, probably
        main_company = self.env.ref("base.main_company")
        partners = self.env["res.partner"].search([("vat", "=", "IT06363391001")])
        for partner in partners:
            if partner.id != main_company.partner_id.id:
                partner.vat = ""

    def getFile(self, filename):
        module_name = "l10n_it_fatturapa_import_zip"
        path = get_module_resource(module_name, "tests", "data", filename)
        with open(path, "rb") as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    def test_import_zip(self):
        attachment = self.attach_model.create(
            {
                "name": "xml_import.zip",
                "datas": self.getFile("xml_import.zip")[1],
            }
        )
        attachment.action_import()
        self.assertEqual(len(attachment.invoice_out_ids), 6)
        self.assertEqual(len(attachment.invoice_in_ids), 37)
        checked = False
        for att in attachment.attachment_out_ids:
            if att.name == "IT06363391001_00012.xml":
                checked = True
                self.assertEqual(
                    att.out_invoice_ids.invoice_date, datetime(2020, 1, 7).date()
                )
                self.assertEqual(
                    att.out_invoice_ids.invoice_date_due, datetime(2020, 2, 29).date()
                )
        self.assertTrue(checked)
