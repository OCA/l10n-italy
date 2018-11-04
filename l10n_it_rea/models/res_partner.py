# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp.osv import fields, orm


sel_member_type = [
    ('SU', 'Unique Member'), ('SM', 'Multiple Members')]
sel_liquidation_state = [
    ('LS', 'In liquidation'),
    ('LN', 'Not in liquidation')]


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'rea_office': fields.many2one(
            'res.country.state', string='Office Province'),
        'rea_code': fields.char('REA Code', size=20),
        'rea_capital': fields.float('Capital'),
        'rea_member_type': fields.selection(
            sel_member_type, 'Member Type'),
        'rea_liquidation_state': fields.selection(
            sel_liquidation_state, 'Liquidation State')
    }
    _sql_constraints = [
        ('rea_code_uniq', 'unique (rea_code, company_id)',
         'The rea code code must be unique per company !'),
    ]

