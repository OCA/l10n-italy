# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ddt_invoice_exclude = fields.Boolean(
        string='Exclude from DDT invoicing',
        default=True,
        help="If flagged this service will not be automatically "
             "invoiced from DDT.")
