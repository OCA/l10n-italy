#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from .intrastat_statement import format_9, format_x


class IntrastatStatementSaleSection3(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section3"
    _description = "Intrastat Statement - Sales Section 3"

    invoice_number = fields.Char()
    invoice_date = fields.Date()
    supply_method = fields.Selection(
        selection=[("I", "Instant"), ("R", "Repeated")],
    )
    payment_method = fields.Selection(
        selection=[("B", "Bank Transfer"), ("A", "Credit"), ("X", "Other")],
    )
    country_payment_id = fields.Many2one(
        comodel_name="res.country", string="Payment Country"
    )

    def get_supply_method_key(self):
        self.ensure_one()
        return self.supply_method

    def get_payment_method_key(self):
        self.ensure_one()
        return self.payment_method

    @api.model
    def get_section_number(self):
        return 3

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super()._prepare_statement_line(inv_intra_line, statement_id)
        res.update(
            {
                "invoice_number": inv_intra_line.invoice_number,
                "invoice_date": inv_intra_line.invoice_date,
                "supply_method": inv_intra_line.supply_method,
                "payment_method": inv_intra_line.payment_method,
                "country_payment_id": inv_intra_line.country_payment_id.id,
            }
        )
        return res

    @api.model
    def _prepare_export_line(self):
        self.ensure_one()
        self._export_line_checks(_("Sales"), self.get_section_number())

        rcd = ""
        # Codice dello Stato membro dell’acquirente
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(country_id.code, 2)
        #  Codice IVA del fornitore
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Numero Fattura
        rcd += format_x(self.invoice_number, 15)
        # Data Fattura
        invoice_date_ddmmyy = False
        if self.invoice_date:
            invoice_date_ddmmyy = self.invoice_date.strftime("%d%m%y")
        rcd += format_x(invoice_date_ddmmyy, 6)
        # Codice del servizio
        rcd += format_9(self.intrastat_code_id.name, 6)
        # Modalità di erogazione
        rcd += format_x(self.supply_method, 1)
        # Modalità di incasso
        rcd += format_x(self.payment_method, 1)
        # Codice del paese di pagamento
        rcd += format_x(self.country_payment_id.code, 2)

        rcd += "\r\n"
        return rcd
