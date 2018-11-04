# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp.osv import fields, orm
from tools.translate import _
from res_partner import sel_liquidation_state, sel_member_type


class Company(orm.Model):
    _inherit = 'res.company'

    _columns = {
        'rea_office': fields.related(
            'partner_id', 'rea_office', type='many2one',
            relation='res.country.state', string='Office Province'),
        'rea_code': fields.related(
            'partner_id', 'rea_code', string='REA Code', type='char'),
        'rea_capital': fields.related(
            'partner_id', 'rea_capital', string='Capital', type='char'),
        'rea_member_type': fields.related(
            'partner_id', 'rea_member_type', string='Member Type',
            type='selection', selection=sel_member_type),
        'rea_liquidation_state': fields.related(
            'partner_id', 'rea_liquidation_state',
            string='Liquidation State', type='selection',
            selection=sel_liquidation_state),
    }

    def onchange_rea_data(self, cr, uid, ids, rea_office, rea_code, rea_capital,
            rea_member_type, rea_liquidation_state):
        company_registry = ''
        member_type = ''
        if (
            rea_office or rea_code or rea_capital or
            rea_member_type or rea_liquidation_state
        ):
            if rea_member_type:
                member_type = dict(sel_member_type)[rea_member_type]
            liquidation_state = ''
            if rea_liquidation_state:
                liquidation_state = dict(sel_liquidation_state)[
                    rea_liquidation_state]
            # using always €, as this is a registry of Italian companies
            rea_office_code = self.pool['res.country.state'].read(
                cr, uid, rea_office, ['code'])
            company_registry = _("%s %s Share Cap. %s € %s %s") % (
                rea_office_code['code'] or '', rea_code or '',
                _(rea_capital), member_type, liquidation_state
            )
        return {'value': {'company_registry': company_registry}}
