#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .intrastat_statement import format_9, format_x


class IntrastatStatementSaleSection2(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section2"
    _description = "Intrastat Statement - Sales Section 2"

    month = fields.Integer(string="Ref. Month")
    quarterly = fields.Integer(string="Ref. Quarter")
    year_id = fields.Integer(string="Ref. Year")
    sign_variation = fields.Selection(
        selection=[("+", "+"), ("-", "-")], string="Adjustment Sign"
    )
    transaction_nature_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature",
        string="Transaction Nature",
        default=lambda m: m._default_transaction_nature_id(),
    )
    statistic_amount_euro = fields.Integer(string="Statistic Value in Euro")

    @api.model
    def get_section_number(self):
        return 2

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super()._prepare_statement_line(inv_intra_line, statement_id)
        company_id = self._context.get("company_id", self.env.company)

        # Company defaults
        transaction_nature_id = (
            inv_intra_line.transaction_nature_id
            or company_id.intrastat_sale_transaction_nature_id
        )
        statistic_amount = (
            inv_intra_line.statistic_amount_euro
            or company_id.intrastat_sale_statistic_amount
        )

        # Amounts
        statistic_amount = statement_id.round_min_amount(
            statistic_amount, statement_id.company_id or company_id, 0
        )

        # Period Ref
        ref_period = statement_id._get_period_ref()

        # Sign variation
        sign_variation = False
        if inv_intra_line.invoice_id.move_type == "out_refund":
            sign_variation = "-"
        res.update(
            {
                "month": ref_period.get("month"),
                "quarterly": ref_period.get("quarterly"),
                "year_id": ref_period.get("year_id"),
                "sign_variation": sign_variation,
                "transaction_nature_id": transaction_nature_id.id,
                "statistic_amount_euro": statistic_amount,
            }
        )
        return res

    def _export_line_checks(self, section_label, section_number):
        res = super()._export_line_checks(section_label, section_number)
        if not self.year_id:
            raise ValidationError(_("Missing reference year on 'Sales - Section 2'"))
        if not self.sign_variation:
            raise ValidationError(_("Missing adjustment sign on 'Sales - Section 2'"))
        if self.statement_id.period_type == "M":
            if not self.month:
                raise ValidationError(
                    _("Missing reference month on 'Sales - Section 2' adjustment")
                )
        elif self.statement_id.period_type == "T":
            if not self.quarterly:
                raise ValidationError(
                    _("Missing reference quarter on 'Sales - Section 2' adjustment")
                )
        return res

    @api.model
    def _prepare_export_line(self):
        self.ensure_one()
        self._export_line_checks(_("Sales"), self.get_section_number())

        rcd = ""
        # Mese di riferimento del riepilogo da rettificare
        rcd += format_9(self.month, 2)
        #  Trimestre di riferimento del riepilogo da rettificare
        rcd += format_9(self.quarterly, 1)
        # Anno periodo di ref da modificare
        year = (self.year_id or 0) % 100
        rcd += format_9(year, 2)
        # Codice dello Stato membro dell’acquirente
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(country_id.code, 2)
        #  Codice IVA dell’acquirente
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        #  Segno da attribuire alle variazioni da X(1) apportare
        rcd += format_x(self.sign_variation, 1)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Codice della natura della transazione
        rcd += format_x(self.transaction_nature_id.code, 1)
        # Codice della nomenclatura combinata della merce
        rcd += format_9(self.intrastat_code_id.name, 8)
        if self.statement_id.period_type == "M":
            #  Valore statistico in euro
            rcd += format_9(self.statistic_amount_euro, 13)

        rcd += "\r\n"
        return rcd

    def get_amount_euro(self):
        amount = 0
        for section in self:
            if section.sign_variation == "-":
                amount -= section.amount_euro
            else:
                amount += section.amount_euro
        return amount
