import base64

from odoo.addons.l10n_it_fatturapa_out.tests.fatturapa_common import FatturaPACommon


class TestInvoiceWT(FatturaPACommon):
    def setUp(self):
        super().setUp()

        ###
        # XXX this should really be in FatturaPACommon
        # tested 2021/08/06 @TheMule71

        # XXX - a company named "YourCompany" alread exists
        # we move it out of the way but we should do better here
        self.env.company.sudo().search([("name", "=", "YourCompany")]).write(
            {"name": "YourCompany_"}
        )
        self.env.company.name = "YourCompany"
        self.env.company.vat = "IT06363391001"
        self.env.company.fatturapa_art73 = True
        self.env.company.partner_id.street = "Via Milano, 1"
        self.env.company.partner_id.city = "Roma"
        self.env.company.partner_id.state_id = self.env.ref("base.state_us_2").id
        self.env.company.partner_id.country_id = self.env.ref("base.it").id
        self.env.company.partner_id.zip = "00100"
        self.env.company.partner_id.phone = "06543534343"
        self.env.company.email = "info@yourcompany.example.com"
        self.env.company.fatturapa_fiscal_position_id = self.env.ref(
            "l10n_it_fatturapa.fatturapa_RF01"
        ).id
        self.env["decimal.precision"].search(
            [("name", "=", "Product Unit of Measure")]
        ).digits = 3
        self.env["uom.uom"].search([("name", "=", "Units")]).name = "Unit(s)"
        ###

        type_payable = self.env.ref("account.data_account_type_payable")
        type_receivable = self.env.ref("account.data_account_type_receivable")
        self.tax_0 = (
            self.env.ref("l10n_it_fatturapa.tax_00_enas")
            .sudo()
            .copy({"company_id": self.env.company.id})
        )
        self.wt_account_payable = self.env["account.account"].create(
            {
                "name": "Debiti per ritenute da versare",
                "code": "WT_001",
                "user_type_id": type_payable.id,
                "reconcile": True,
            }
        )
        self.wt_account_receivable = self.env["account.account"].create(
            {
                "name": "Crediti per ritenute subite",
                "code": "WT_002",
                "user_type_id": type_receivable.id,
                "reconcile": True,
            }
        )
        self.journal_misc = self.env["account.journal"].search(
            [("type", "=", "general")]
        )[0]
        vals_payment = {
            "name": "",
            "line_ids": [(0, 0, {"value": "balance", "days": 15})],
        }
        self.payment_term_15 = self.env["account.payment.term"].create(vals_payment)
        wt_vals = {
            "name": "Code 1040",
            "code": "1040",
            "certification": True,
            "account_receivable_id": self.wt_account_receivable.id,
            "account_payable_id": self.wt_account_payable.id,
            "journal_id": self.journal_misc.id,
            "payment_term": self.payment_term_15.id,
            "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            "rate_ids": [
                (
                    0,
                    0,
                    {
                        "tax": 20,
                        "base": 1,
                    },
                )
            ],
        }
        self.wt1040 = self.env["withholding.tax"].create(wt_vals)
        wt_vals = {
            "name": "Enasarco",
            "code": "Enasarco",
            "account_receivable_id": self.wt_account_receivable.id,
            "account_payable_id": self.wt_account_payable.id,
            "journal_id": self.journal_misc.id,
            "wt_types": "enasarco",
            "payment_term": self.payment_term_15.id,
            "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            "rate_ids": [
                (
                    0,
                    0,
                    {
                        "tax": 8.25,
                        "base": 1,
                    },
                )
            ],
        }
        self.enasarco = self.env["withholding.tax"].create(wt_vals)
        wt_vals = {
            "name": "INPS",
            "code": "INPS",
            "account_receivable_id": self.wt_account_receivable.id,
            "account_payable_id": self.wt_account_payable.id,
            "journal_id": self.journal_misc.id,
            "wt_types": "enasarco",
            "payment_term": self.payment_term_15.id,
            "payment_reason_id": self.env.ref("l10n_it_payment_reason.a").id,
            "rate_ids": [
                (
                    0,
                    0,
                    {
                        "tax": 5.25,
                        "base": 1,
                    },
                )
            ],
        }
        self.inps = self.env["withholding.tax"].create(wt_vals)

    def test_e_invoice_wt(self):
        self.set_sequences(13, "2019-01-07")

        invoice = self.invoice_model.create(
            {
                "name": "INV/2019/0013",
                "invoice_date": "2019-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "name": "Service",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, [self.tax_22.id])],
                            "invoice_line_tax_wt_ids": [(6, 0, [self.wt1040.id])],
                        },
                    ),
                ],
            }
        )
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_post()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00011.xml")

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content,
            "IT06363391001_00011.xml",
            module_name="l10n_it_fatturapa_out_wt",
        )

    def test_e_invoice_wt_enas_0(self):
        self.set_sequences(14, "2019-01-07")
        invoice = self.invoice_model.create(
            {
                "name": "INV/2019/0014",
                "invoice_date": "2019-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "name": "Service",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, [self.tax_22.id])],
                            "invoice_line_tax_wt_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        self.wt1040.id,
                                        self.enasarco.id,
                                    ],
                                )
                            ],
                        },
                    ),
                ],
            }
        )
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_post()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00014.xml")

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content,
            "IT06363391001_00014.xml",
            module_name="l10n_it_fatturapa_out_wt",
        )

    def test_e_invoice_wt_enas_1(self):
        """
        Fill DatiCassaPrevidenziale with Enasarco data
        """
        self.set_sequences(15, "2019-01-07")
        self.enasarco.use_daticassaprev = True
        self.enasarco.daticassprev_tax_id = self.tax_0
        invoice = self.invoice_model.create(
            {
                "name": "INV/2019/0015",
                "invoice_date": "2019-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "name": "Service",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, [self.tax_22.id])],
                            "invoice_line_tax_wt_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        self.wt1040.id,
                                        self.enasarco.id,
                                    ],
                                )
                            ],
                        },
                    ),
                ],
            }
        )
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_post()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00015.xml")

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content,
            "IT06363391001_00015.xml",
            module_name="l10n_it_fatturapa_out_wt",
        )

    def test_e_invoice_wt_enas_2(self):
        """
        Fill DatiCassaPrevidenziale with Enasarco data,
        when DatiRiepilogo already has 0 VAT
        """
        self.set_sequences(16, "2019-01-07")
        self.enasarco.use_daticassaprev = True
        self.enasarco.daticassprev_tax_id = self.tax_0
        invoice = self.invoice_model.create(
            {
                "name": "INV/2019/0016",
                "invoice_date": "2019-01-07",
                "partner_id": self.res_partner_fatturapa_2.id,
                "journal_id": self.sales_journal.id,
                "invoice_payment_term_id": self.account_payment_term.id,
                "user_id": self.user_demo.id,
                "move_type": "out_invoice",
                "currency_id": self.EUR.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "account_id": self.a_sale.id,
                            "name": "Service",
                            "quantity": 1,
                            "product_uom_id": self.product_uom_unit.id,
                            "price_unit": 10,
                            "tax_ids": [(6, 0, [self.tax_0.id])],
                            "invoice_line_tax_wt_ids": [
                                (
                                    6,
                                    0,
                                    [
                                        self.wt1040.id,
                                        self.enasarco.id,
                                    ],
                                )
                            ],
                        },
                    ),
                ],
            }
        )
        invoice._onchange_invoice_line_wt_ids()
        invoice.action_post()
        res = self.run_wizard(invoice.id)

        attachment = self.attach_model.browse(res["res_id"])
        self.set_e_invoice_file_id(attachment, "IT06363391001_00016.xml")

        # XML doc to be validated
        xml_content = base64.decodebytes(attachment.datas)
        self.check_content(
            xml_content,
            "IT06363391001_00016.xml",
            module_name="l10n_it_fatturapa_out_wt",
        )


def test_e_invoice_wt_inps_0(self):
    self.set_sequences(17, "2019-01-07")
    invoice = self.invoice_model.create(
        {
            "invoice_date": "2019-01-07",
            "partner_id": self.res_partner_fatturapa_2.id,
            "journal_id": self.sales_journal.id,
            "invoice_payment_term_id": self.account_payment_term.id,
            "user_id": self.user_demo.id,
            "move_type": "out_invoice",
            "currency_id": self.EUR.id,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "account_id": self.a_sale.id,
                        "name": "Service",
                        "quantity": 1,
                        "product_uom_id": self.product_uom_unit.id,
                        "price_unit": 10,
                        "tax_ids": [(6, 0, [self.tax_22.id])],
                        "invoice_line_tax_wt_ids": [
                            (
                                6,
                                0,
                                [
                                    self.wt1040.id,
                                    self.inps.id,
                                ],
                            )
                        ],
                    },
                ),
            ],
        }
    )
    invoice._onchange_invoice_line_wt_ids()
    invoice.action_post()
    res = self.run_wizard(invoice.id)

    attachment = self.attach_model.browse(res["res_id"])
    self.set_e_invoice_file_id(attachment, "IT06363391001_00017.xml")

    # XML doc to be validated
    xml_content = base64.decodebytes(attachment.datas)
    self.check_content(
        xml_content, "IT06363391001_00017.xml", module_name="l10n_it_fatturapa_out_wt"
    )


def test_e_invoice_wt_inps_1(self):
    """
    Fill DatiCassaPrevidenziale with INPS data
    """
    self.set_sequences(18, "2019-01-07")
    self.inps.use_daticassaprev = True
    self.inps.daticassprev_tax_id = self.tax_0
    invoice = self.invoice_model.create(
        {
            "invoice_date": "2019-01-07",
            "partner_id": self.res_partner_fatturapa_2.id,
            "journal_id": self.sales_journal.id,
            "invoice_payment_term_id": self.account_payment_term.id,
            "user_id": self.user_demo.id,
            "move_type": "out_invoice",
            "currency_id": self.EUR.id,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "account_id": self.a_sale.id,
                        "name": "Service",
                        "quantity": 1,
                        "product_uom_id": self.product_uom_unit.id,
                        "price_unit": 10,
                        "tax_ids": [(6, 0, [self.tax_22.id])],
                        "invoice_line_tax_wt_ids": [
                            (
                                6,
                                0,
                                [
                                    self.wt1040.id,
                                    self.inps.id,
                                ],
                            )
                        ],
                    },
                ),
            ],
        }
    )
    invoice._onchange_invoice_line_wt_ids()
    invoice.action_post()
    res = self.run_wizard(invoice.id)

    attachment = self.attach_model.browse(res["res_id"])
    self.set_e_invoice_file_id(attachment, "IT06363391001_00018.xml")

    # XML doc to be validated
    xml_content = base64.decodebytes(attachment.datas)
    self.check_content(
        xml_content, "IT06363391001_00018.xml", module_name="l10n_it_fatturapa_out_wt"
    )


def test_e_invoice_wt_inps_2(self):
    """
    Fill DatiCassaPrevidenziale with INPS data,
    when DatiRiepilogo already has 0 VAT
    """
    self.set_sequences(19, "2019-01-07")
    self.inps.use_daticassaprev = True
    self.inps.daticassprev_tax_id = self.tax_0
    invoice = self.invoice_model.create(
        {
            "invoice_date": "2019-01-07",
            "partner_id": self.res_partner_fatturapa_2.id,
            "journal_id": self.sales_journal.id,
            "invoice_payment_term_id": self.account_payment_term.id,
            "user_id": self.user_demo.id,
            "move_type": "out_invoice",
            "currency_id": self.EUR.id,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "account_id": self.a_sale.id,
                        "name": "Service",
                        "quantity": 1,
                        "product_uom_id": self.product_uom_unit.id,
                        "price_unit": 10,
                        "tax_ids": [(6, 0, [self.tax_0.id])],
                        "invoice_line_tax_wt_ids": [
                            (
                                6,
                                0,
                                [
                                    self.wt1040.id,
                                    self.inps.id,
                                ],
                            )
                        ],
                    },
                ),
            ],
        }
    )
    invoice._onchange_invoice_line_wt_ids()
    invoice.action_post()
    res = self.run_wizard(invoice.id)

    attachment = self.attach_model.browse(res["res_id"])
    self.set_e_invoice_file_id(attachment, "IT06363391001_00019.xml")

    # XML doc to be validated
    xml_content = base64.decodebytes(attachment.datas)
    self.check_content(
        xml_content, "IT06363391001_00019.xml", module_name="l10n_it_fatturapa_out_wt"
    )
