#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .intrastat_statement import format_9, format_x


class IntrastatStatementSaleSection4(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section4"
    _description = "Intrastat Statement - Sales Section 4"

    intrastat_custom_id = fields.Many2one(
        comodel_name="account.intrastat.custom", string="Customs Section"
    )
    month = fields.Integer(string="Ref. Month")
    quarterly = fields.Integer(string="Ref. Quarter")
    year_id = fields.Integer(string="Ref. Year")
    protocol = fields.Integer(string="Protocol Number")
    progressive_to_modify = fields.Integer(string="Progressive to Adjust")
    invoice_number = fields.Char(string="Invoice Number")
    invoice_date = fields.Date(string="Invoice Date")
    supply_method = fields.Selection(
        selection=[("I", "Instant"), ("R", "Repeated")], string="Supply Method"
    )
    payment_method = fields.Selection(
        selection=[("B", "Bank Transfer"), ("A", "Credit"), ("X", "Other")],
        string="Payment Method",
    )
    country_payment_id = fields.Many2one(
        comodel_name="res.country", string="Payment Country"
    )
    cancellation = fields.Boolean(
        string="Cancellation",
        help="The Adjustment is intended for cancellation",
    )

    @api.model
    def get_section_number(self):
        return 4

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super(IntrastatStatementSaleSection4, self)._prepare_statement_line(
            inv_intra_line, statement_id
        )

        # Period Ref
        ref_period = statement_id._get_period_ref()

        res.update(
            {
                "month": ref_period.get("month"),
                "quarterly": ref_period.get("quarterly"),
                "year_id": ref_period.get("year_id"),
                "invoice_number": inv_intra_line.invoice_number,
                "invoice_date": inv_intra_line.invoice_date,
                "supply_method": inv_intra_line.supply_method,
                "payment_method": inv_intra_line.payment_method,
                "country_payment_id": inv_intra_line.country_payment_id.id,
                "intrastat_custom_id": statement_id.intrastat_custom_id.id,
            }
        )
        return res

    def _export_line_checks(self, section_label, section_number):
        super(IntrastatStatementSaleSection4, self)._export_line_checks(
            section_label, section_number
        )
        if not self.year_id:
            raise ValidationError(_("Missing reference year on 'Sales - Section 4'"))
        if not self.intrastat_custom_id:
            raise ValidationError(_("Missing customs section on 'Sales - Section 4'"))
        if not self.protocol:
            raise ValidationError(_("Missing protocol number on 'Sales - Section 4'"))
        if not self.progressive_to_modify:
            raise ValidationError(
                _("Missing progressive to adjust on 'Sales - Section 4'")
            )
        if not self.country_payment_id and not self.cancellation:
            raise ValidationError(_("Missing payment country on 'Sales - Section 4'"))

    @api.model
    def _prepare_export_line(self):
        self._export_line_checks(_("Sales"), self.get_section_number())
        modifying = not self.cancellation

        rcd = ""
        # Codice della sezione doganale in cui è stato registrata la
        # dichiarazione da rettificare
        rcd += format_9(self.intrastat_custom_id.code, 6)
        # Anno di registrazione della dichiarazione da rettificare
        year = (self.year_id or 0) % 100
        rcd += format_9(year, 2)
        # Protocollo della dichiarazione da rettificare
        rcd += format_9(self.protocol, 6)
        # Progressivo della sezione 3 da rettificare
        rcd += format_9(self.progressive_to_modify, 5)
        # Codice dello Stato membro dell’acquirente
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(modifying and country_id.code, 2)
        #  Codice IVA dell’acquirente
        rcd += format_x(modifying and self.vat_code.replace(" ", ""), 12)
        # Ammontare delle operazioni in euro
        rcd += format_9(modifying and self.amount_euro, 13)
        # Numero Fattura
        rcd += format_x(modifying and self.invoice_number, 15)
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            invoice_date_ddmmyy = self.invoice_date.strftime("%d%m%y")
        rcd += format_x(modifying and invoice_date_ddmmyy, 6)
        # Codice del servizio
        rcd += format_9(modifying and self.intrastat_code_id.name, 6)
        # Modalità di erogazione
        rcd += format_x(modifying and self.supply_method, 1)
        # Modalità di incasso
        rcd += format_x(modifying and self.payment_method, 1)
        # Codice del paese di pagamento
        rcd += format_x(modifying and self.country_payment_id.code, 2)

        rcd += "\r\n"
        return rcd
