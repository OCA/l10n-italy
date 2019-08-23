# Copyright 2019 Simone Rubino - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    intrastat_uom_kg_id = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of measure for Kg")
    intrastat_additional_unit_from = fields.Selection(
        selection=[
            ('quantity', 'Quantity'),
            ('weight', 'Weight'),
            ('none', 'None')],
        string='Additional Unit of Measure FROM',
        default='weight')
    intrastat_exclude_free_line = fields.Boolean(
        string='Exclude Free lines')
    intrastat_ua_code = fields.Char(
        string="User ID (UA Code)",
        size=4)
    intrastat_delegated_vat = fields.Char(
        string="Delegated person VAT",
        size=16)
    intrastat_delegated_name = fields.Char(
        string="Delegated person",
        size=255)
    intrastat_export_file_name = fields.Char(
        string="File name for export")

    # default values sale section
    intrastat_sale_statistic_amount = fields.Boolean(
        string="Intrastat Sale: Statistic amount")
    intrastat_sale_transation_nature_id = fields.Many2one(
        string="Intrastat Sale: Transation nature",
        comodel_name='account.intrastat.transation.nature')
    intrastat_sale_delivery_code_id = fields.Many2one(
        string="Intrastat Sale: Delivery code",
        comodel_name='account.incoterms')
    intrastat_sale_transport_code_id = fields.Many2one(
        string="Intrastat Sale: Transport code",
        comodel_name='account.intrastat.transport')
    intrastat_sale_province_origin_id = fields.Many2one(
        string="Intrastat Sale: Province origin",
        comodel_name='res.country.state')

    # default values purchase section
    intrastat_purchase_statistic_amount = fields.Boolean(
        string="Intrastat Purchase: Statistic amount")
    intrastat_purchase_transation_nature_id = fields.Many2one(
        string="Intrastat Purchase: Transation nature",
        comodel_name='account.intrastat.transation.nature')
    intrastat_purchase_delivery_code_id = fields.Many2one(
        string="Intrastat Purchase: Delivery code",
        comodel_name='account.incoterms')
    intrastat_purchase_transport_code_id = fields.Many2one(
        string="Intrastat Purchase: Transport code",
        comodel_name='account.intrastat.transport')
    intrastat_purchase_province_destination_id = fields.Many2one(
        string="Intrastat Purchase: Province destination",
        comodel_name='res.country.state')

    intrastat_min_amount = fields.Float(
        string="Min amount",
        help="In case of invoices < 'min amount', "
             "use min amount in intrastat statement",
        default=1.0
    )
