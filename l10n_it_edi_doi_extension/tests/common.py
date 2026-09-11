# Copyright 2025 Nextev
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta

from odoo import fields
from odoo.tests import Form

from odoo.addons.base.tests.common import BaseCommon


class Common(BaseCommon):
    @classmethod
    def _create_declaration(cls, type_doi, protocol_part1=None, protocol_part2=None):
        """Create a declaration with unique protocol numbers."""
        if protocol_part1 is None:
            # Generate unique protocol numbers based on sequence
            if not hasattr(cls, "_protocol_counter"):
                cls._protocol_counter = 0
            cls._protocol_counter += 1
            protocol_part1 = str(1000 + cls._protocol_counter)
            protocol_part2 = str(2000 + cls._protocol_counter)

        return cls.env["l10n_it_edi_doi.declaration_of_intent"].create(
            {
                "partner_id": cls.partner.id,
                "company_id": cls.company.id,
                "state": "active",
                "type": type_doi,
                "plafond_id": cls.plafond.id if type_doi == "in" else False,
                "currency_id": cls.company.currency_id.id,
                "issue_date": fields.Date.today(),
                "start_date": fields.Date.today(),
                "end_date": fields.Date.today() + relativedelta(months=2),
                "threshold": 5000,
                "protocol_number_part1": protocol_part1,
                "protocol_number_part2": protocol_part2,
            }
        )

    @classmethod
    def _create_invoice(cls, name, partner, taxes=False, date=False, in_type=False):
        invoice_form = Form(
            cls.env["account.move"].with_context(
                default_move_type="in_invoice" if in_type else "out_invoice",
                default_partner_id=partner.id,
            )
        )
        invoice_form.invoice_date = date if date else fields.Date.today()
        invoice_form.invoice_payment_term_id = cls.env.ref(
            "account.account_payment_term_advance"
        )
        cls._add_invoice_line_id(invoice_form, taxes=taxes, in_type=in_type)
        invoice = invoice_form.save()
        return invoice

    @classmethod
    def _add_invoice_line_id(cls, invoice_form, taxes=False, in_type=False):
        with invoice_form.invoice_line_ids.new() as invoice_line:
            invoice_line.product_id = cls.env.ref("product.product_product_5")
            invoice_line.quantity = 10.00
            invoice_line.name = "test line"
            invoice_line.price_unit = 90.00
            if taxes:
                invoice_line.tax_ids.clear()
                for tax in taxes:
                    invoice_line.tax_ids.add(tax)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.ref("base.main_company")
        cls.company.country_id = cls.env.ref("base.it")
        cls.company.account_fiscal_country_id = cls.env.ref("base.it")
        cls.tax_model = cls.env["account.tax"]
        cls.partner = cls.env.ref("base.res_partner_2")
        cls.partner.country_id = cls.env.ref("base.it")
        cls.partner.company_id = cls.company
        cls.current_year = fields.Date.today().year

        cls.plafond = cls.env["l10n_it_edi_doi_extension.plafond.year"].create(
            {
                "year": cls.current_year,
                "company_id": cls.company.id,
                "plafond_total": 100000.0,
            }
        )
        cls.doi_in = cls._create_declaration("in")
        cls.tax_group = cls.env["account.tax.group"].create(
            {"name": "Vat Free", "sequence": 1}
        )
        cls.tax = cls.tax_model.create(
            {
                "l10n_it_exempt_reason": "N3.5",
                "l10n_it_law_reference": "Art. 8, comma 1, lett. a) DPR 633/72",
                "type_tax_use": "purchase",
                "name": "0% declaration tax3",
                "amount": 0,
                "tax_group_id": cls.tax_group.id,
            }
        )
        cls.env.company.l10n_it_edi_doi_bill_tax_id = cls.tax
