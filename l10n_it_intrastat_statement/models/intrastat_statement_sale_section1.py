#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models

from .intrastat_statement import format_9, format_x


class IntrastatStatementSaleSection1(models.Model):
    _inherit = "account.intrastat.statement.sale.section"
    _name = "account.intrastat.statement.sale.section1"
    _description = "Intrastat Statement - Sales Section 1"

    transaction_nature_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature",
        string="Transaction Nature",
        default=lambda m: m._default_transaction_nature_id(),
    )
    weight_kg = fields.Integer(string="Net Mass (kg)")
    additional_units = fields.Integer()
    additional_units_required = fields.Boolean(
        string="Additional Unit Required",
        store=True,
        related="intrastat_code_id.additional_unit_required",
    )
    additional_units_uom = fields.Char(
        string="Additional Unit of Measure",
        readonly=True,
        related="intrastat_code_id.additional_unit_uom_id.name",
    )
    statistic_amount_euro = fields.Integer(string="Statistic Value in Euro")
    delivery_code_id = fields.Many2one(
        comodel_name="account.incoterms", string="Delivery Terms"
    )
    transport_code_id = fields.Many2one(
        comodel_name="account.intrastat.transport", string="Transport Mode"
    )
    country_destination_id = fields.Many2one(
        comodel_name="res.country", string="Destination Country"
    )
    province_origin_id = fields.Many2one(
        comodel_name="res.country.state", string="Origin Province"
    )
    transaction_nature_b_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature.b",
        string="Transaction Nature B",
    )
    country_origin_id = fields.Many2one(
        comodel_name="res.country", string="Origin Country"
    )
    triangulation = fields.Boolean(
        default=False,
    )

    @api.model
    def get_section_number(self):
        return 1

    def apply_partner_data(self, partner_data):
        res = super().apply_partner_data(partner_data)
        if "country_destination_id" in partner_data:
            self.country_destination_id = partner_data["country_destination_id"]
        return res

    @api.onchange("weight_kg")
    def change_weight_kg(self):
        if self.statement_id.company_id.intrastat_additional_unit_from == "weight":
            self.additional_units = self.weight_kg

    @api.onchange("transaction_nature_id")
    def _onchange_transaction_nature_id(self):
        domain = [("nature_parent_id", "=", self.transaction_nature_id.id)]
        recs = self.env["account.intrastat.transaction.nature.b"].search(domain)
        return {"domain": {"transaction_nature_b_id": [("id", "in", recs.ids)]}}

    @api.model
    def _prepare_statement_line(self, inv_intra_line, statement_id=None):
        res = super()._prepare_statement_line(inv_intra_line, statement_id)
        company_id = self.env.company

        # Company defaults
        delivery_code_id = (
            inv_intra_line.delivery_code_id
            or company_id.intrastat_sale_delivery_code_id
        )
        province_origin_id = (
            inv_intra_line.province_origin_id
            or company_id.intrastat_sale_province_origin_id
        )
        statistic_amount = (
            inv_intra_line.statistic_amount_euro
            or company_id.intrastat_sale_statistic_amount
        )
        transaction_nature_id = (
            inv_intra_line.transaction_nature_id
            or company_id.intrastat_sale_transaction_nature_id
        )
        transport_code_id = (
            inv_intra_line.transport_code_id
            or company_id.intrastat_sale_transport_code_id
        )

        # Amounts
        statistic_amount = statement_id.round_min_amount(
            statistic_amount, statement_id.company_id or company_id, 0
        )

        # not setting default yet
        nature_b_model = self.env["account.intrastat.transaction.nature.b"]

        if inv_intra_line.transaction_nature_b_id:
            transaction_nature_b_id = inv_intra_line.transaction_nature_b_id
        else:
            transaction_nature_b_id = nature_b_model

        triangulation = inv_intra_line.triangulation
        country_good_origin_id = inv_intra_line.country_good_origin_id

        res.update(
            {
                "transaction_nature_id": transaction_nature_id.id,
                "weight_kg": (round(inv_intra_line.weight_kg) or 1)
                if inv_intra_line.show_weight
                else None,
                "additional_units": round(inv_intra_line.additional_units) or 1,
                "statistic_amount_euro": statistic_amount,
                "delivery_code_id": delivery_code_id.id,
                "transport_code_id": transport_code_id.id,
                "country_destination_id": inv_intra_line.country_destination_id.id,
                "province_origin_id": province_origin_id.id,
                "transaction_nature_b_id": transaction_nature_b_id.id,
                "triangulation": triangulation,
                "country_origin_id": country_good_origin_id.id,
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
        #  Codice IVA dell’acquirente
        rcd += format_x(self.vat_code.replace(" ", ""), 12)
        # Ammontare delle operazioni in euro
        rcd += format_9(self.amount_euro, 13)
        # Codice della natura della transazione
        if self.triangulation:  # in caso triangolazione
            rcd += format_x(self.transaction_nature_id.triangulation, 1)
        else:
            rcd += format_x(self.transaction_nature_id.code, 1)

        # Codice della nomenclatura combinata della merce
        rcd += format_9(self.intrastat_code_id.name, 8)
        if self.statement_id.period_type == "M":
            #  Massa netta in chilogrammi
            rcd += format_9(self.weight_kg, 10)
            #  Quantità espressa nell'unità di misura supplementare
            rcd += format_9(self.additional_units, 10)
            #  Valore statistico in euro
            rcd += format_9(self.statistic_amount_euro, 13)
            #  Codice delle condizioni di consegna
            delivery_code = self.delivery_code_id.code or ""
            rcd += format_x(delivery_code[:1], 1)
            #  Codice del modo di trasporto
            transport_code = self.transport_code_id.code
            rcd += format_9(transport_code, 1)
            #  Codice del paese di destinazione
            rcd += format_x(self.country_destination_id.code, 2)
            #  Codice della provincia di origine della merce
            rcd += format_x(self.province_origin_id.code, 2)
            # new fields
            if self.triangulation:
                nb_code = ""
            else:
                nb_code = self.transaction_nature_b_id.code
            rcd += format_x(nb_code, 1)

            rcd += format_x(self.country_origin_id.code, 2)

        rcd += "\r\n"
        return rcd
