# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.osv import fields, orm


class res_partner(orm.Model):
    _inherit = "res.partner"

    _columns = {
        'eori_code': fields.char('EORI Code', size=20),
        'license_number': fields.char('License Code', size=20),
        # 1.2.6 RiferimentoAmministrazione
        'pa_partner_code': fields.char('PA Code for partner', size=20),
        # 1.2.1.4
        'register': fields.char('Professional Register', size=60),
        # 1.2.1.5
        'register_province': fields.many2one(
            'res.country.state', string='Register Province'),
        # 1.2.1.6
        'register_code': fields.char('Register Code', size=60),
        # 1.2.1.7
        'register_regdate': fields.date('Register Registration Date'),
        # 1.2.1.8
        'register_fiscalpos': fields.many2one(
            'fatturapa.fiscal_position',
            string="Register Fiscal Position"),
    }
