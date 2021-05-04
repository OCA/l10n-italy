import base64
import tempfile

from odoo.modules import get_module_resource
from odoo.tests import Form
from odoo.tests.common import SingleTransactionCase


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

    def create_wt(self):
        return self.env["withholding.tax"].create(
            {
                "name": "1040",
                "code": "1040",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 20.0})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            }
        )

    def create_wt_23_20(self):
        return self.env["withholding.tax"].create(
            {
                "name": "2320",
                "code": "2320",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 23.0, "base": 0.2})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            }
        )

    def create_wt_23_50(self):
        return self.env["withholding.tax"].create(
            {
                "name": "2320",
                "code": "2320",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 23.0, "base": 0.5})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            }
        )

    def create_wt_26_20q(self):
        return self.env["withholding.tax"].create(
            {
                "name": "2620q",
                "code": "2620q",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 26.0, "base": 0.2})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    def create_wt_26_40q(self):
        return self.env["withholding.tax"].create(
            {
                "name": "2640q",
                "code": "2640q",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 26.0, "base": 0.4})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    def create_wt_27_20q(self):
        return self.env["withholding.tax"].create(
            {
                "name": "2720q",
                "code": "2720q",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 27.0, "base": 0.2})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    def create_wt_4q(self):
        return self.env["withholding.tax"].create(
            {
                "name": "4q",
                "code": "4q",
                "wt_types": "enasarco",
                "account_receivable_id": self.payable_account_id,
                "account_payable_id": self.payable_account_id,
                "payment_term": self.env.ref(
                    "account.account_payment_term_immediate"
                ).id,
                "rate_ids": [(0, 0, {"tax": 4.0, "base": 1.0})],
                "payment_reason_id": self.env.ref("l10n_it_payment_reason.q").id,
            }
        )

    def create_res_bank(self):
        return self.env["res.bank"].create(
            {
                "name": "Banca generica",
                "bic": "BCITITMM",
            }
        )

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
        attach_form = Form(self.attach_model)
        attach_form.name = name
        attach_form.datas = self.getFile(file_name, module_name=module_name)[1]
        attach_id = attach_form.save().id
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

    def setUp(self):
        super(FatturapaCommon, self).setUp()
        self.wizard_model = self.env["wizard.import.fatturapa"]
        self.wizard_link_model = self.env["wizard.link.to.invoice"]
        self.data_model = self.env["ir.model.data"]
        self.attach_model = self.env["fatturapa.attachment.in"]
        self.invoice_model = self.env["account.move"]
        self.payable_account_id = (
            self.env["account.account"]
            .search(
                [
                    (
                        "user_type_id",
                        "=",
                        self.env.ref("account.data_account_type_payable").id,
                    )
                ],
                limit=1,
            )
            .id
        )
        self.headphones = self.env.ref("product.product_product_7_product_template")
        self.imac = self.env.ref("product.product_product_8_product_template")
        self.service = self.env.ref("product.product_product_1")
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
        self.env["res.lang"]._activate_lang("it_IT")
