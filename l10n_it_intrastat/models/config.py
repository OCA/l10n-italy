from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    intrastat_uom_kg_id = fields.Many2one(
        'product.uom', string="Unit of Measure for Kg",
    )
    intrastat_additional_unit_from = fields.Selection(
        [('quantity', 'Quantity'), ('weight', 'Weight'), ('none', 'None')],
        string='Additional Unit from', default='weight')
    intrastat_exclude_free_line = fields.Boolean(string='Exclude Free lines')
    intrastat_ua_code = fields.Char(string="User ID (UA Code)", size=4)
    intrastat_delegated_vat = fields.Char(string="Delegate VAT number",
                                          size=16)
    intrastat_delegated_name = fields.Char(string="Delegate", size=255)
    intrastat_export_file_name = fields.Char(string="File name for export")

    # default values sale section
    intrastat_sale_statistic_amount = fields.Boolean(
        string='Force Statistic Value in Euro')
    intrastat_sale_transaction_nature_id = fields.Many2one(
        'account.intrastat.transaction.nature', string='Transaction Nature')
    intrastat_sale_delivery_code_id = fields.Many2one(
        'stock.incoterms', string='Delivery Terms')
    intrastat_sale_transport_code_id = fields.Many2one(
        'account.intrastat.transport', string='Transport Mode')
    intrastat_sale_province_origin_id = fields.Many2one(
        'res.country.state', string='Origin Province')

    # default values purchase section
    intrastat_purchase_statistic_amount = fields.Boolean(
        string='Force Statistic Value in Euro')
    intrastat_purchase_transaction_nature_id = fields.Many2one(
        'account.intrastat.transaction.nature', string='Transaction Nature')
    intrastat_purchase_delivery_code_id = fields.Many2one(
        'stock.incoterms', string='Delivery Terms')
    intrastat_purchase_transport_code_id = fields.Many2one(
        'account.intrastat.transport', string='Transport Mode')
    intrastat_purchase_province_destination_id = fields.Many2one(
        'res.country.state', string='Destination Province')
    intrastat_min_amount = fields.Float(
        string="Min amount", help="In case of invoices < 'Min amount', use min"
                                  " amount in Intrastat statement",
        default=1
    )
