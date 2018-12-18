# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp.osv import fields, osv, orm

from openerp.addons.l10n_it_sdi_channel.models.sdi import SDI_CHANNELS


class ResCompany(orm.Model):
    _inherit = 'res.company'

    _columns = {
        'sdi_channel_id': fields.many2one('sdi.channel', string='SdI channel'),
        'sdi_channel_type': fields.related(
            'sdi_channel_id', 'channel_type', type='selection',
            selection=SDI_CHANNELS,
            string='SdI channel type', readonly=True),
        'email_from_for_fatturaPA': fields.related(
            'sdi_channel_id', 'pec_server_id', 'email_from_for_fatturaPA',
            type='char', string='Sender Email Address', readonly=True),
        'email_exchange_system': fields.related(
            'sdi_channel_id', 'email_exchange_system', type='char',
            string='Exchange System Email Address', readonly=True),
    }


class AccountConfigSettings(orm.TransientModel):
    _inherit = 'account.config.settings'

    _columns = {
        'sdi_channel_id': fields.related(
            'company_id', 'sdi_channel_id', type='many2one',
            relation='sdi.channel', string='SdI channel'),
        'sdi_channel_type': fields.related(
            'sdi_channel_id', 'channel_type', type='selection',
            selection=SDI_CHANNELS, string='SdI channel type', readonly=True),
        'email_from_for_fatturaPA': fields.related(
            'sdi_channel_id', 'pec_server_id', 'email_from_for_fatturaPA',
            type='char', string='Sender Email Address', readonly=True),
        'email_exchange_system': fields.related(
            'sdi_channel_id', 'email_exchange_system', type='char',
            string='Exchange System Email Address', readonly=True),
    }

    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            res['value'].update({
                'sdi_channel_id': (company.sdi_channel_id
                                   and company.sdi_channel_id.id or False),
                'sdi_channel_type': (company.sdi_channel_type
                                     and company.sdi_channel_type or False),
                'email_from_for_fatturaPA': (
                    company.email_from_for_fatturaPA
                    and company.email_from_for_fatturaPA or False),
                'email_exchange_system': (
                    company.email_exchange_system
                    and company.email_exchange_system or False),
                })
        else:
            res['value'].update({
                'sdi_channel_id': False,
                'sdi_channel_type': False,
                'email_from_for_fatturaPA': False,
                'email_exchange_system': False,
            })
        res.setdefault('domain', {}).update({
            'sdi_channel_id': [('company_id', '=', company_id)],
            'sdi_channel_type': [('company_id', '=', company_id)],
            'email_from_for_fatturaPA': [('company_id', '=', company_id)],
            'email_exchange_system':  [('company_id', '=', company_id)],
        })
        return res
