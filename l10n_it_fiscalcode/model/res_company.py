# -*- coding: utf-8 -*-
# Copyright 2016 Giuliano Lotta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResCompany(models.Model):
    """ Extends res.company to add Italian Fiscal Code
    """
    # Private attributes
    _inherit = 'res.company'

    # Fields declaration
    fiscalcode = fields.Char(related='partner_id.fiscalcode')
    is_soletrader = fields.Boolean(related='partner_id.is_soletrader')
