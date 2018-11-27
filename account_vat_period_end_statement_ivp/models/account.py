# flake8: noqa
# -*- coding: utf-8 -*-
#    Copyright (C) 2011-12 Domsense s.r.l. <http://www.domsense.com>.
#    Copyright (C) 2012-15 Agile Business Group sagl <http://www.agilebg.com>
#    Copyright (C) 2013-15 LinkIt Spa <http://http://www.linkgroup.it>
#    Copyright (C) 2013-17 Associazione Odoo Italia
#                          <http://www.odoo-italia.org>
#    Copyright (C) 2017    Didotech srl <http://www.didotech.com>
#    Copyright (C) 2017    SHS-AV s.r.l. <https://www.zeroincombenze.it>
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#
from openerp.osv import orm, fields
from openerp.tools.translate import _
import logging
try:
    import codicefiscale
except ImportError as err:
    logging.debug(err)


class AccountVatPeriodEndStatement(orm.Model):
    _inherit = "account.vat.period.end.statement"

    _columns = {
        'vat_settlement_attachment_id': fields.many2one(
            'account.vat.settlement.attachment',
            'VAT Settlement Export File',
            readonly=True),
        'show_zero': fields.boolean('Show zero amount lines'),
        'soggetto_codice_fiscale': fields.char(
            'Codice fiscale dichiarante',
            size=16, required=True,
            help="CF del soggetto che presenta la comunicazione "
            "se PF o DI o con la specifica carica"),
        'codice_carica': fields.selection([
            ('0', 'Azienda PF (Ditta indivisuale/Professionista/eccetera)'),
            ('1', 'Legale rappresentante, socio amministratore'),
            ('2', 'Rappresentante di minore,interdetto,eccetera'),
            ('3', 'Curatore fallimentare'),
            ('4', 'Commissario liquidatore'),
            ('5', 'Custode giudiziario'),
            ('6', 'Rappresentante fiscale di soggetto non residente'),
            ('7', 'Erede'),
            ('8', 'Liquidatore'),
            ('9', 'Obbligato di soggetto estinto'),
            ('10', 'Rappresentante fiscale art. 44c3 DLgs 331/93'),
            ('11', 'Tutore di minore'),
            ('12', 'Liquidatore di DI'),
            ('13', 'Amministratore di condominio'),
            ('14', 'Pubblica Amministrazione'),
            ('15', 'Commissario PA') ,],
            'Codice carica' ,),
        'progressivo_telematico':
        fields.integer('Progressivo telematico', readonly=True),
        'incaricato_trasmissione_codice_fiscale':
        fields.char('Codice Fiscale Incaricato',
                    size=16,
                    help="CF intermediario "
                         "che effettua la trasmissione telematica"),
        'incaricato_trasmissione_numero_CAF':
        fields.integer('Numero CAF intermediario',
                       size=5,
                       help="Eventuale numero iscrizione albo del C.A.F."),
        'incaricato_trasmissione_data_impegno':
        fields.date('Data data impegno')
    }

    def copy(self, cr, uid, ids, defaults, context=None):
        if context is None:
            context = self.pool['res.users'].context_get(cr, uid)
        defaults['vat_settlement_attachment_id'] = False
        return super(AccountVatPeriodEndStatement, self).copy(
            cr, uid, ids, defaults, context)

    def action_cancel(self, cr, uid, ids, context=None):
        for vat_statement in self.browse(cr, uid, ids, context):
            if vat_statement:
                raise orm.except_orm(
                    _('Error!'),
                    _('You should delete VAT Settlement before'
                      ' deleting Vat Period End Statement')
                )
        return super(AccountVatPeriodEndStatement, self).action_cancel(
            cr, uid, ids, context)

    def onchange_fiscalcode(self, cr, uid, ids, fiscalcode, name,
                            context=None):
        if fiscalcode:
            if len(fiscalcode) != 16:
                if len(fiscalcode) == 11:
                    res_partner_pool = self.pool.get('res.partner')
                    chk = res_partner_pool.simple_vat_check(
                        cr, uid, 'it', fiscalcode)
                    if not chk:
                        return {'value': {name: False},
                                'warning': {
                                   'title': 'Invalid fiscalcode!',
                                   'message': 'Invalid vat number'}
                        }
                else:
                    return {'value': {name: False},
                            'warning': {
                                'title': 'Invalid len!',
                                'message': 'Fiscal code len must be 11 or 16'}
                        }
            else:
                chk = codicefiscale.control_code(fiscalcode[0:15])
                if chk != fiscalcode[15]:
                    value = fiscalcode[0:15] + chk
                    return {'value': {name: value},
                            'warning': {'title': 'Invalid fiscalcode!',
                                        'message':
                                        'Fiscal code could be %s' % value}
                            }
            return {'value': {name: fiscalcode}}
        return {}


class AccountVatSettlementAttachment(orm.Model):
    _name = "account.vat.settlement.attachment"
    _description = "Vat Settlement Export File"
    _inherits = {'ir.attachment': 'ir_attachment_id'}
    _inherit = ['mail.thread']

    _columns = {
        'ir_attachment_id': fields.many2one(
            'ir.attachment', 'Attachment', required=True, ondelete="cascade"),
        'vat_statement_ids': fields.one2many(
            'account.vat.period.end.statement', 'vat_settlement_attachment_id',
            string="VAT Statements", readonly=True),
    }
