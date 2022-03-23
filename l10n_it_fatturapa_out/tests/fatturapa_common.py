import base64
import tempfile

from lxml import etree

from odoo.modules.module import get_module_resource

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.mail.tests.common import mail_new_test_user


class FatturaPACommon(AccountTestInvoicingCommon):
    def setUp(self):
        super(FatturaPACommon, self).setUp()
        # used to be in AccountTestUsers
        self.account_model = self.env["account.account"]

        # self.company = self.env.ref("base.main_company")
        # self.company = self.env["res.company"].browse(self.env.companies.ids[0])
        self.account_manager = mail_new_test_user(
            self.env,
            name="Adviser",
            login="fm",
            email="accountmanager@yourcompany.com",
            groups="account.group_account_manager,base.group_partner_manager",
            company_ids=[(6, 0, [self.env.company.id])],
        )
        self.env.user = self.account_manager
        self.company = self.env.company
        self.company.e_invoice_transmitter_id = self.company.partner_id.id

        self.wizard_model = self.env["wizard.export.fatturapa"]
        self.data_model = self.env["ir.model.data"]
        self.attach_model = self.env["fatturapa.attachment.out"]
        self.invoice_model = self.env["account.move"]
        self.fatturapa_attach = self.env["fatturapa.attachments"]
        self.context = {}
        self.maxDiff = None
        self.sales_journal = self.env["account.journal"].search(
            [("type", "=", "sale"), ("company_id", "=", self.env.company.id)]
        )[0]
        account_user_type = self.env.ref("account.data_account_type_receivable")
        self.a_recv = self.account_model.with_user(self.account_manager.id).create(
            dict(
                code="cust_acc",
                name="customer account",
                user_type_id=account_user_type.id,
                reconcile=True,
            )
        )
        self.a_sale = self.env["account.account"].search(
            [
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_revenue").id,
                )
            ],
            limit=1,
        )
        self.account_payment_term = self.env.ref(
            "account.account_payment_term_end_following_month"
        )
        self.account_payment_term.fatturapa_pt_id = self.env.ref(
            "l10n_it_fiscal_payment_term.fatturapa_tp02"
        )
        self.account_payment_term.fatturapa_pm_id = self.env.ref(
            "l10n_it_fiscal_payment_term.fatturapa_mp05"
        )
        self.user_demo = self.env.ref("base.user_demo")
        self.product_uom_unit = self.env.ref("uom.product_uom_unit")
        self.product_product_10 = self.env.ref("product.product_product_10")
        self.product_order_01 = self.env.ref("product.product_order_01")
        self.product_product_10.default_code = False
        self.product_product_10.barcode = False
        self.product_order_01.default_code = False
        self.product_order_01.barcode = False

        # XXX l10n_it_fatturapa.tax_* should be either fixed or removed
        # here we need to copy the values to be able to use them
        # as company (in the accounts) is different
        def _tax_vals(ref):
            # if the repartition_lines have an account set, we replace it
            tax = self.env.ref(ref).sudo()
            invoice_rpls = [
                (
                    0,
                    0,
                    {
                        "factor_percent": rpl.factor_percent,
                        "repartition_type": rpl.repartition_type,
                        "account_id": self.company_data["default_account_tax_sale"].id
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
                        "account_id": self.company_data["default_account_tax_sale"].id
                        if rpl.account_id
                        else None,
                    },
                )
                for rpl in tax.refund_repartition_line_ids
            ]
            tax_values = tax.copy_data()[0]
            tax_values.update(
                {
                    "company_id": self.env.company.id,
                    "invoice_repartition_line_ids": invoice_rpls,
                    "refund_repartition_line_ids": refund_rpls,
                }
            )
            return tax_values

        tax_model = self.env["account.tax"]
        self.tax_22 = tax_model.create(_tax_vals("l10n_it_fatturapa.tax_22"))
        self.tax_10 = tax_model.create(_tax_vals("l10n_it_fatturapa.tax_10"))
        self.tax_22_SP = tax_model.create(_tax_vals("l10n_it_fatturapa.tax_22_SP"))
        self.tax_00_ns = tax_model.create(_tax_vals("l10n_it_fatturapa.tax_00_ns"))

        self.res_partner_fatturapa_0 = self.env.ref(
            "l10n_it_fatturapa.res_partner_fatturapa_0"
        )
        # B2B Customer
        self.res_partner_fatturapa_2 = self.env.ref(
            "l10n_it_fatturapa.res_partner_fatturapa_2"
        )
        # INTRA Customer
        self.res_partner_fatturapa_5 = self.env.ref(
            "l10n_it_fatturapa.res_partner_fatturapa_5"
        )
        self.intermediario = self.env.ref("l10n_it_fatturapa.res_partner_fatturapa_1")
        self.stabile_organizzazione = self.env.ref(
            "l10n_it_fatturapa.res_partner_fatturapa_3"
        )
        self.res_partner_fatturapa_4 = self.env.ref(
            "l10n_it_fatturapa.res_partner_fatturapa_4"
        )
        self.EUR = self.env.ref("base.EUR")
        # United Arab Emirates currency
        self.AED = self.env.ref("base.AED")
        self.cr.execute(
            "UPDATE res_company SET currency_id = %s WHERE id = %s",
            [self.EUR.id, self.company.id],
        )
        self.trasmittente = self.env.ref("l10n_it_fatturapa.res_partner_fatturapa_1")
        # Otherwise self.company in cache could keep the old wrong value USD
        self.company.refresh()

    def AttachFileToInvoice(self, InvoiceId, filename):
        self.fatturapa_attach.create(
            {
                "name": filename,
                "invoice_id": InvoiceId,
                "datas": self.getAttachment(filename)[1],
            }
        )

    def set_sequences(
        self,
        invoice_number,
        dt,
        sequence_name="Customer Invoices : Check Number Sequence",
    ):
        seq_pool = self.env["ir.sequence"]
        inv_seq = seq_pool.search([("name", "=", sequence_name)], limit=1)
        seq_date = self.env["ir.sequence.date_range"].search(
            [
                ("sequence_id", "=", inv_seq.id),
                ("date_from", "<=", dt),
                ("date_to", ">=", dt),
            ],
            limit=1,
        )
        if not seq_date:
            seq_date = inv_seq._create_date_range_seq(dt)
        seq_date.number_next_actual = invoice_number

    def run_wizard(self, invoice_id):
        wizard = self.wizard_model.create({})
        return wizard.with_context({"active_ids": [invoice_id]}).exportFatturaPA()

    def set_e_invoice_file_id(self, e_invoice, file_name):
        # We need this because file name is random and we can't predict it
        partial_file_name = file_name.replace(".xml", "")
        test_file_id = partial_file_name.split("_")[1]
        xml_content = base64.decodebytes(e_invoice.datas)
        parser = etree.XMLParser(remove_blank_text=True)
        xml = etree.fromstring(xml_content, parser)
        file_id = xml.findall(".//ProgressivoInvio")
        file_id[0].text = test_file_id
        e_invoice.datas = base64.encodebytes(etree.tostring(xml))
        e_invoice.name = file_name

    def check_content(self, xml_content, file_name, module_name=None):
        parser = etree.XMLParser(remove_blank_text=True)
        test_fatt_data = self.getFile(file_name, module_name=module_name)[1]
        test_fatt_content = base64.decodebytes(test_fatt_data)
        test_fatt = etree.fromstring(test_fatt_content, parser)
        xml = etree.fromstring(xml_content, parser)
        self.assertEqual(etree.tostring(test_fatt), etree.tostring(xml))

    def getFilePath(self, filepath):
        with open(filepath, "rb") as test_data:
            with tempfile.TemporaryFile() as out:
                base64.encode(test_data, out)
                out.seek(0)
                return filepath, out.read()

    def getAttachment(self, name, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_out"
        return self.getFilePath(
            get_module_resource(module_name, "tests", "data", "attah_base.pdf")
        )

    def getFile(self, filename, module_name=None):
        if module_name is None:
            module_name = "l10n_it_fatturapa_out"
        path = get_module_resource(module_name, "tests", "data", filename)
        return self.getFilePath(path)

    def _create_invoice(self):
        return self.invoice_model.create(
            {
                "name": "Test Invoice",
                "journal_id": self.sales_journal.id,
                "partner_id": self.res_partner_fatturapa_0.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "product_id": self.product_product_10.id,
                            "name": self.product_product_10.name,
                            "quantity": 1,
                            "price_unit": 1,
                            "tax_ids": [(6, 0, {self.tax_22.id})],
                        },
                    ),
                ],
            }
        )

    def _create_e_invoice(self):
        invoice = self._create_invoice()
        invoice._post()
        action = self.run_wizard(invoice.id)
        return self.env[action["res_model"]].browse(action["res_id"])
