import base64
import tempfile

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
                "account_receivable_id": cls.payable_account_id,
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
                "account_receivable_id": cls.payable_account_id,
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
                "account_receivable_id": cls.payable_account_id,
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
                "account_receivable_id": cls.payable_account_id,
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
                "account_receivable_id": cls.payable_account_id,
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
                "account_receivable_id": cls.payable_account_id,
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
                "account_receivable_id": cls.payable_account_id,
                "account_payable_id": cls.payable_account_id,
                "payment_term": cls.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 4.0, "base": 1.0})],
                "payment_reason_id": cls.env.ref("l10n_it_payment_reason.q").id,
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
        attach = self.attach_model.create(
            {"name": name, "datas": self.getFile(file_name, module_name=module_name)[1]}
        )
        return attach

    def run_wizard(
        self,
        name,
        file_name,
        mode="import",
        wiz_values=None,
        module_name=None,
    ):
        if module_name is None:
            module_name = "l10n_it_fatturapa_in"

        attach = self.create_attachment(name, file_name, module_name=module_name)
        attach_id = attach.id
        if mode == "import":
            wizard_form = Form(
                self.wizard_model.with_context(
                    active_ids=[attach_id], active_model="fatturapa.attachment.in"
                ).with_company(self.env.company)
            )
            wizard = wizard_form.save()
            return wizard.importFatturaPA()
        if mode == "link":
            wizard_form = Form(
                self.wizard_link_model.with_context(
                    active_ids=[attach_id], active_model="fatturapa.attachment.in"
                ).with_company(self.env.company)
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
        active_ids = []
        for file_name in file_name_list:
            active_ids.append(
                self.attach_model.create(
                    {
                        "name": file_name,
                        "datas": self.getFile(file_name, module_name)[1],
                    }
                ).id
            )
        wizard = self.wizard_model.with_context(active_ids=active_ids).create({})
        return wizard.importFatturaPA()

    @classmethod
    def _setup_taxes(cls):
        # duplicate US purchase taxes in our current country
        for tax in cls.env["account.tax"].search(
            [
                ("country_id", "=", cls.env.ref("base.us").id),
                ("type_tax_use", "=", "purchase"),
            ]
        ):
            tax_data = tax.sudo().copy_data()[0]
            default_account_tax_purchase = cls.env["account.account"].search(
                [
                    ("company_id", "=", cls.env.company.id),
                    ("code", "=", "251000"),  # Tax receivable
                ]
            )
            invoice_rpls = [
                (
                    0,
                    0,
                    {
                        "factor_percent": rpl.factor_percent,
                        "repartition_type": rpl.repartition_type,
                        "account_id": default_account_tax_purchase.id
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
                        "account_id": default_account_tax_purchase.id
                        if rpl.account_id
                        else None,
                    },
                )
                for rpl in tax.refund_repartition_line_ids
            ]
            tax_data.update(
                {
                    "country_id": cls.env.company.country_id.id,
                    "company_id": cls.env.company.id,
                    "invoice_repartition_line_ids": invoice_rpls,
                    "refund_repartition_line_ids": refund_rpls,
                }
            )
            tax.create(tax_data)

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
        cls.env.company.arrotondamenti_tax_id = cls.env["account.tax"].search(
            [
                ("type_tax_use", "=", "purchase"),
                ("amount", "=", 0.0),
                ("company_id", "=", cls.env.company.id),
            ],
            order="sequence",
            limit=1,
        )
        cls.env.company.arrotondamenti_attivi_account_id = (
            arrotondamenti_attivi_account_id
        )
        cls.env.company.arrotondamenti_passivi_account_id = (
            arrotondamenti_passivi_account_id
        )
        cls.payable_account_id = (
            cls.env["account.account"]
            .search(
                [
                    (
                        "account_type",
                        "=",
                        "liability_payable",
                    )
                ],
                limit=1,
            )
            .id
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
        cls.env.user.company_ids |= cls.company_data_it["company"]
        cls.env.company = cls.company_data_it["company"]
        cls.env["res.lang"]._activate_lang("it_IT")

        # we need a fiscal position in the current country
        cls.fiscal_pos_it1 = cls.env["account.fiscal.position"].create(
            {
                "name": "fiscal_pos_it1",
                "country_id": cls.env.company.country_id.id,
                "auto_apply": True,
            }
        )

        cls._setup_taxes()
        cls._setup_accounts()

        cls.wizard_model = cls.env["wizard.import.fatturapa"].with_company(
            cls.env.company
        )
        cls.wizard_link_model = cls.env["wizard.link.to.invoice"].with_company(
            cls.env.company
        )
        cls.wizard_link_inv_line_model = cls.env[
            "wizard.link.to.invoice.line"
        ].with_company(cls.env.company)
        cls.attach_model = cls.env["fatturapa.attachment.in"].with_company(
            cls.env.company
        )
        cls.invoice_model = cls.env["account.move"].with_company(cls.env.company)
        cls.headphones = cls.env.ref("product.product_product_7_product_template")
        cls.imac = cls.env.ref("product.product_product_8_product_template")
        cls.service = cls.env.ref("product.product_product_1")
        cls.wt = cls.create_wt_4q()
        cls.wtq = cls.create_wt_27_20q()
        cls.wt4q = cls.create_wt_26_40q()
        cls.wt2q = cls.create_wt_26_20q()
