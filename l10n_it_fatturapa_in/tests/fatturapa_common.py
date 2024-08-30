#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64
import operator
import tempfile
from functools import reduce

from odoo import fields
from odoo.modules import get_module_resource
from odoo.tests import Form
from odoo.tests.common import SingleTransactionCase

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.mail.tests.common import mail_new_test_user


class FatturapaCommon(SingleTransactionCase):
    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_in"
        path = get_module_resource(module_name, "tests", "data", filename)
        with open(path, "rb") as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return path, out.read()

    @classmethod
    def create_wt(cls):
        return cls.env["withholding.tax"].create(
            {
                "name": "1040",
                "code": "1040",
                "account_receivable_id": cls.receivable_account.id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 20.0})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.a").id,
            }
        )

    @classmethod
    def create_wt_23_20(cls):
        return cls.env["withholding.tax"].create(
            {
                "name": "2320",
                "code": "2320",
                "account_receivable_id": cls.receivable_account.id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 23.0, "base": 0.2})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.a").id,
            }
        )

    @classmethod
    def create_wt_23_50(cls):
        return cls.env["withholding.tax"].create(
            {
                "name": "2320",
                "code": "2320",
                "account_receivable_id": cls.receivable_account.id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 23.0, "base": 0.5})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.a").id,
            }
        )

    @classmethod
    def create_wt_26_20q(cls):
        return cls.env["withholding.tax"].create(
            {
                "name": "2620q",
                "code": "2620q",
                "account_receivable_id": cls.receivable_account.id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 26.0, "base": 0.2})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    @classmethod
    def create_wt_26_40q(cls):
        return cls.env["withholding.tax"].create(
            {
                "name": "2640q",
                "code": "2640q",
                "account_receivable_id": cls.receivable_account.id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 26.0, "base": 0.4})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    @classmethod
    def create_wt_27_20q(cls):
        return cls.env["withholding.tax"].create(
            {
                "name": "2720q",
                "code": "2720q",
                "account_receivable_id": cls.receivable_account.id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 27.0, "base": 0.2})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    @classmethod
    def create_wt_4q(cls):
        return cls.env["withholding.tax"].create(
            {
                "name": "4q",
                "code": "4q",
                "wt_types": "enasarco",
                "account_receivable_id": cls.receivable_account.id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 4.0, "base": 1.0})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    @classmethod
    def create_misc_journal(cls):
        return cls.env["account.journal"].create(
            {
                "name": "Test Miscellaneous Journal",
                "code": "TMJ",
                "type": "general",
            }
        )

    def create_wt_115_r(self):
        return self.env["withholding.tax"].create(
            {
                "name": "1040 R",
                "code": "1040R",
                "account_receivable_id": self.receivable_account.id,
                "account_payable_id": self.payable_account.id,
                "journal_id": self.misc_journal.id,
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

    def create_wt_enasarco_115_a(self):
        return self.env["withholding.tax"].create(
            {
                "name": "1040/3",
                "code": "1040",
                "account_receivable_id": self.receivable_account.id,
                "account_payable_id": self.payable_account.id,
                "journal_id": self.misc_journal.id,
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

    def create_wt_enasarco_85_r(self):
        return self.env["withholding.tax"].create(
            {
                "name": "Enasarco 8,50",
                "code": "TC07",
                "account_receivable_id": self.receivable_account.id,
                "account_payable_id": self.payable_account.id,
                "journal_id": self.misc_journal.id,
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

    def create_wt_enasarco_157_r(self):
        return self.env["withholding.tax"].create(
            {
                "name": "Enasarco",
                "code": "TC07",
                "account_receivable_id": self.receivable_account.id,
                "account_payable_id": self.payable_account.id,
                "journal_id": self.misc_journal.id,
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

    @classmethod
    def create_receivable_account(cls):
        return cls.env["account.account"].create(
            {
                "name": "Test WH tax",
                "code": "whtaxrec2",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )

    @classmethod
    def create_payable_account(cls):
        return cls.env["account.account"].create(
            {
                "name": "Test WH tax",
                "code": "whtaxpay2",
                "account_type": "liability_payable",
                "reconcile": True,
            }
        )

    def create_res_bank(self):
        return self.env["res.bank"].create(
            {
                "name": "Banca generica",
                "bic": "BCITITMM",
            }
        )

    def create_attachment(self, name, file_name, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_in"
        attach = self.env["fatturapa.attachment.in"].create(
            {"name": name, "datas": self.getFile(file_name, module_name=module_name)[1]}
        )
        return attach

    def run_wizard(
        self, name, file_name, mode="import", wiz_values=None, module_name=None
    ):
        if module_name is None:
            module_name = "l10n_it_fatturapa_in"
        attach = self.create_attachment(name, file_name, module_name=module_name)
        attach.e_invoice_received_date = fields.Datetime.now()
        attach_id = attach.id
        if mode == "import":
            wizard_form = Form(
                self.wizard_model.with_context(
                    active_ids=[attach_id], active_model="fatturapa.attachment.in"
                )
            )
            wizard = wizard_form.save()
            return wizard.importFatturaPA()
        if mode == "link":
            wizard_form = Form(
                self.wizard_link_model.with_context(
                    active_ids=[attach_id], active_model="fatturapa.attachment.in"
                )
            )
            wizard = wizard_form.save()
            if wiz_values:
                wiz_values.wizard_id = wizard
            return wizard.link()
        if not mode:
            # return created fatturapa.attachment.in record in case no mode provided
            return attach

    def run_wizard_multi(self, file_name_list, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_in"

        attachments = self.attach_model.create(
            [
                {
                    "name": file_name,
                    "datas": self.getFile(file_name, module_name=module_name)[1],
                }
                for file_name in file_name_list
            ]
        )

        wizard = self.wizard_model.with_context(
            active_model=attachments._name,
            active_ids=attachments.ids,
        ).create({})

        return wizard.importFatturaPA()

    @classmethod
    def _setup_journals(cls):
        cls.misc_journal = cls.create_misc_journal()

    @classmethod
    def _setup_taxes(cls):
        company = cls.env.company
        cls._copy_taxes_to_company(company)
        cls.env.company.arrotondamenti_tax_id = cls.env["account.tax"].search(
            [
                ("type_tax_use", "=", "purchase"),
                ("amount", "=", 0.0),
            ],
            order="sequence",
            limit=1,
        )

    @classmethod
    def _copy_taxes_to_company(cls, company):
        """Copy specific taxes to `company`."""
        # Demo taxes have been created for another company,
        # copy them in current company
        external_ids = [
            "l10n_it_fatturapa.tax_22_acq",
            "l10n_it_fatturapa.tax_00_minimi_acq",
        ]
        taxes_list = [cls.env.ref(external_id) for external_id in external_ids]
        taxes = reduce(
            operator.ior,
            taxes_list,
        )
        sudo_taxes = taxes.sudo()
        taxes_values = []
        for tax in sudo_taxes:
            tax_data = tax.copy_data()[0]
            invoice_rpls = [
                (
                    0,
                    0,
                    {
                        "factor_percent": rpl.factor_percent,
                        "repartition_type": rpl.repartition_type,
                        "account_id": cls.tax_receivable_account.id
                        if rpl.account_id
                        else None,
                    },
                )
                for rpl in tax.invoice_repartition_line_ids
            ]
            refund_rpls = [
                (
                    0,
                    0,
                    {
                        "factor_percent": rpl.factor_percent,
                        "repartition_type": rpl.repartition_type,
                        "account_id": cls.tax_receivable_account.id
                        if rpl.account_id
                        else None,
                    },
                )
                for rpl in tax.refund_repartition_line_ids
            ]
            tax_data.update(
                {
                    "country_id": company.country_id.id,
                    "company_id": company.id,
                    "invoice_repartition_line_ids": invoice_rpls,
                    "refund_repartition_line_ids": refund_rpls,
                }
            )
            taxes_values.append(tax_data)
        return cls.env["account.tax"].create(taxes_values)

    @classmethod
    def _setup_accounts(cls):
        # round up accounts
        arrotondamenti_attivi_account_id = (
            cls.env["account.account"]
            .search(
                [("account_type", "=", "income_other")],
                limit=1,
            )
            .id
        )
        arrotondamenti_passivi_account_id = (
            cls.env["account.account"]
            .search(
                [
                    (
                        "account_type",
                        "=",
                        "expense_direct_cost",
                    )
                ],
                limit=1,
            )
            .id
        )
        cls.env.company.arrotondamenti_attivi_account_id = (
            arrotondamenti_attivi_account_id
        )
        cls.env.company.arrotondamenti_passivi_account_id = (
            arrotondamenti_passivi_account_id
        )
        cls.payable_account = cls.create_payable_account()
        cls.payable_account_id = cls.payable_account.id
        cls.receivable_account = cls.create_receivable_account()
        cls.tax_receivable_account = cls.env["account.account"].search(
            [
                ("code", "=", "251000"),  # Tax receivable
            ]
        )

    @classmethod
    def _set_it_user(cls):
        """Create and set an Italian Account Manager as current user."""
        groups = cls.env.user.groups_id | cls.env.ref("account.group_account_manager")
        groups_xml_id_dict = groups.get_external_id()
        user = mail_new_test_user(
            cls.env,
            login="it_account_manager",
            groups=",".join(groups_xml_id_dict.values()),
        )

        cls.env = cls.env(user=user)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls._set_it_user()

        # create IT company
        # (borrowing setup_company_data from AccountTestInvoicingCommon)
        AccountTestInvoicingCommon.env = cls.env
        cls.company_data_it = AccountTestInvoicingCommon.setup_company_data(
            "La tua società",
            chart_template=cls.env.company.chart_template_id,
            currency_id=cls.env.ref("base.EUR").id,
            country_id=cls.env.ref("base.it").id,
        )
        it_company = cls.company_data_it["company"]
        cls.env.user.company_id = it_company
        cls.env.user.company_ids = it_company
        cls.env["res.lang"]._activate_lang("it_IT")

        # we need a fiscal position in the current country
        cls.fiscal_pos_it1 = cls.env["account.fiscal.position"].create(
            {
                "name": "fiscal_pos_it1",
                "country_id": cls.env.company.country_id.id,
                "auto_apply": True,
            }
        )

        cls._setup_accounts()
        cls._setup_journals()
        cls._setup_taxes()

        cls.wizard_model = cls.env["wizard.import.fatturapa"]
        cls.wizard_link_model = cls.env["wizard.link.to.invoice"]
        cls.wizard_link_inv_line_model = cls.env["wizard.link.to.invoice.line"]
        cls.attach_model = cls.env["fatturapa.attachment.in"]
        cls.invoice_model = cls.env["account.move"]
        cls.headphones = cls.env.ref("product.product_product_7_product_template")
        cls.imac = cls.env.ref("product.product_product_8_product_template")
        cls.service = cls.env.ref("product.product_product_1")
        cls.wt = cls.create_wt_4q()
        cls.wtq = cls.create_wt_27_20q()
        cls.wt4q = cls.create_wt_26_40q()
        cls.wt2q = cls.create_wt_26_20q()
