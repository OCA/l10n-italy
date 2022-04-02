#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .intrastat_statement import format_9, format_x


class IntrastatStatementPurchaseSection2(models.Model):
    _inherit = "account.intrastat.statement.purchase.section"
    _name = "account.intrastat.statement.purchase.section2"
    _description = "Intrastat Statement - Purchases Section 2"

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
        res = super(IntrastatStatementPurchaseSection2, self)._prepare_statement_line(
            inv_intra_line, statement_id
        )
        company_id = self._context.get("company_id", self.env.company)

        # Company defaults
        statistic_amount = (
            inv_intra_line.statistic_amount_euro
            or company_id.intrastat_purchase_statistic_amount
        )
        transaction_nature_id = (
            inv_intra_line.transaction_nature_id
            or company_id.intrastat_purchase_transaction_nature_id
        )

        # Amounts
        dp_model = self.env["decimal.precision"]
        statistic_amount = statement_id.round_min_amount(
            statistic_amount,
            statement_id.company_id or company_id,
            dp_model.precision_get("Account"),
        )

        # Period Ref
        ref_period = statement_id._get_period_ref()

        # Sign variation
        sign_variation = False
        if inv_intra_line.invoice_id.move_type == "in_refund":
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
        super(IntrastatStatementPurchaseSection2, self)._export_line_checks(
            section_label, section_number
        )
        if not self.year_id:
            raise ValidationError(
                _("Missing reference year on 'Purchases - Section 2'")
            )
        if not self.sign_variation:
            raise ValidationError(
                _("Missing adjustment sign on 'Purchases - Section 2'")
            )
        if self.statement_id.period_type == "M":
            if not self.month:
                raise ValidationError(
                    _(
                        "Missing reference month "
                        "on 'Purchases - Section 2' adjustment"
                    )
                )
        elif self.statement_id.period_type == "T":
            if not self.quarterly:
                raise ValidationError(
                    _(
                        "Missing reference quarter "
                        "on 'Purchases - Section 2' adjustment"
                    )
                )

    def _prepare_export_line(self):
        self._export_line_checks(_("Purchase"), self.get_section_number())

        rcd = ""
        # Mese di riferimento del riepilogo da rettificare
        rcd += format_9(self.month, 2)
        #  Trimestre di riferimento del riepilogo da rettificare
        rcd += format_9(self.quarterly, 1)
        # Anno periodo di ref da modificare
        year = (self.year_id or 0) % 100
        rcd += format_9(year, 2)
        # Codice dello Stato membro del fornitore
        country_id = self.country_partner_id or self.partner_id.country_id
        rcd += format_x(country_id.code, 2)
        #  Codice IVA del fornitore
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        #  Segno da attribuire alle variazioni da X(1) apportare
        rcd += format_x(self.sign_variation, 1)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Ammontare delle operazioni in valuta
        # >> da valorizzare solo per operazione Paesi non Euro
        amount_currency = 0
        if not (
            self.invoice_id.company_id.currency_id.id == self.invoice_id.currency_id.id
        ):
            amount_currency = self.amount_currency
        rcd += format_9(amount_currency, 13)
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
