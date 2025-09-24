# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class EInvoiceLine(models.Model):
    _name = "l10n_it_edi.line"
    _description = "E-invoice Line"

    invoice_id = fields.Many2one(
        "account.move", string="Invoice", readonly=True, ondelete="cascade"
    )
    invoice_line_id = fields.Many2one(
        "account.move.line", string="Invoice Line", readonly=True, ondelete="cascade"
    )
    line_number = fields.Integer(readonly=True)
    service_type = fields.Char(string="Sale Provision Type", readonly=True)
    l10n_it_edi_article_code_ids = fields.One2many(
        "l10n_it_edi.article_code",
        "l10n_it_edi_line_id",
        string="Articles Code",
        readonly=True,
    )
    name = fields.Char(string="Description", readonly=True)
    qty = fields.Float(
        string="Quantity", readonly=True, digits="Product Unit of Measure"
    )
    uom = fields.Char(string="Unit of measure", readonly=True)
    period_start_date = fields.Date(readonly=True)
    period_end_date = fields.Date(readonly=True)
    unit_price = fields.Float(readonly=True, digits="Product Price")
    l10n_it_edi_discount_rise_price_ids = fields.One2many(
        "l10n_it_edi.discount_rise_price",
        "l10n_it_edi_line_id",
        string="Discount and Supplement Details",
        readonly=True,
    )
    total_price = fields.Float(readonly=True)
    tax_amount = fields.Float(string="VAT Rate", readonly=True)
    wt_amount = fields.Char(string="Tax Withholding", readonly=True)
    tax_kind = fields.Char(string="Nature", readonly=True)
    l10n_it_edi_line_other_data_ids = fields.One2many(
        "l10n_it_edi.line_other_data",
        "l10n_it_edi_line_id",
        string="Other Administrative Data",
        readonly=True,
    )
