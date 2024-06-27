# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    intrastat_uom_kg_id = fields.Many2one(
        comodel_name="uom.uom", string="Unit of Measure for Kg"
    )
    intrastat_additional_unit_from = fields.Selection(
        selection=[("quantity", "Quantity"), ("weight", "Weight"), ("none", "None")],
        string="Additional Unit from",
        default="weight",
    )
    intrastat_exclude_free_line = fields.Boolean(string="Exclude Free lines")
    intrastat_ua_code = fields.Char(string="User ID (UA Code)")
    intrastat_delegated_vat = fields.Char(string="Delegate VAT number")
    intrastat_delegated_name = fields.Char(string="Delegate")
    intrastat_export_file_name = fields.Char(string="File name for export")

    # default values sale section
    intrastat_sale_statistic_amount = fields.Boolean(
        string="Sales Statistic Value in Euro"
    )
    intrastat_sale_transaction_nature_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature",
        string="Sales Transaction Nature",
    )
    intrastat_sale_transaction_nature_b_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature.b",
        string="Sales Transaction Nature B",
    )
    intrastat_sale_delivery_code_id = fields.Many2one(
        comodel_name="account.incoterms", string="Sales Delivery Terms"
    )
    intrastat_sale_transport_code_id = fields.Many2one(
        comodel_name="account.intrastat.transport", string="Sales Transport Mode"
    )
    intrastat_sale_province_origin_id = fields.Many2one(
        comodel_name="res.country.state", string="Origin Province"
    )
    intrastat_sale_country_origin_id = fields.Many2one(
        comodel_name="res.country", string="Origin Country"
    )

    # default values purchase section
    intrastat_purchase_statistic_amount = fields.Boolean(
        string="Purchases Statistic Value in Euro"
    )
    intrastat_purchase_transaction_nature_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature",
        string="Purchases Transaction Nature",
    )
    intrastat_purchase_transaction_nature_b_id = fields.Many2one(
        comodel_name="account.intrastat.transaction.nature.b",
        string="Purchases Transaction Nature B",
    )
    intrastat_purchase_delivery_code_id = fields.Many2one(
        comodel_name="account.incoterms", string="Purchases Delivery Terms"
    )
    intrastat_purchase_transport_code_id = fields.Many2one(
        comodel_name="account.intrastat.transport", string="Purchases Transport Mode"
    )
    intrastat_purchase_province_destination_id = fields.Many2one(
        comodel_name="res.country.state", string="Destination Province"
    )

    intrastat_min_amount = fields.Float(
        string="Min amount",
        help="In case of invoices < 'Min amount', "
        "use min amount in Intrastat statement",
        default=1.0,
    )
    # modifiche per PR soglie_intrastat
    # soglie intrastat
    intrastat_goods_sale_threshold = fields.Monetary(
        string="Soglia Cessioni Intra-UE (beni)"
    )
    intrastat_goods_purchase_threshold = fields.Monetary(
        string="Soglia Acquisti Intra-UE (beni)"
    )
    intrastat_service_sale_threshold = fields.Monetary(
        string="Soglia Prestazioni Rese a soggetti UE (servizi)"
    )
    intrastat_service_purchase_threshold = fields.Monetary(
        string="Soglia Prestazioni Ricevute da soggetti UE (servizi)"
    )
    intrastat_email_recipients = fields.Char(string="Destinatari Email Intrastat")
    # posizioni fiscali intrastat
    fiscal_position_goods_sale_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Vendite Beni"
    )
    fiscal_position_goods_purchase_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Acquisti Beni"
    )
    fiscal_position_service_sale_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Vendite Servizi"
    )
    fiscal_position_service_purchase_id = fields.Many2one(
        "account.fiscal.position", string="Posizione Fiscale Acquisti Servizi"
    )

    # enable email notification
    intrastat_email_enabled = fields.Boolean(
        string="Enable Intrastat Email Notification",
        default=False,
        help="Enable email notification when Intrastat threshold is exceeded.",
    )
