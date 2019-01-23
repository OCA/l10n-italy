# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2018 Andrea Cometa <a.cometa@apuliasoftware.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.osv import fields, orm
from openerp.osv.osv import except_osv
from openerp.tools.translate import _


class ResPartner(orm.Model):
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
            'res.province', string='Register Province'),
        # 1.2.1.6
        'register_code': fields.char('Register Code', size=60),
        # 1.2.1.7
        'register_regdate': fields.date('Register Registration Date'),
        # 1.2.1.8
        'register_fiscalpos': fields.many2one(
            'fatturapa.fiscal_position',
            string="Register Fiscal Position"),
        # 1.1.4
        'codice_destinatario': fields.char(
            "Codice Destinatario", size=7,
            help="Il codice, di 7 caratteri, assegnato dal Sdi ai soggetti che "
             "hanno accreditato un canale; qualora il destinatario non abbia "
             "accreditato un canale presso Sdi e riceva via PEC le fatture, "
             "l'elemento deve essere valorizzato con tutti zeri ('0000000'). "),
        # 1.1.6
        'pec_destinatario': fields.char(
            "PEC destinatario", size=64,
            help="Indirizzo PEC al quale inviare la fattura elettronica. "
                 "Da valorizzare "
                 "SOLO nei casi in cui l'elemento informativo "
                 "<CodiceDestinatario> vale '0000000'"),
        'electronic_invoice_subjected': fields.boolean(
            "Subjected to electronic invoice"),
    }
    
    _defaults = {
        'codice_destinatario': '0000000',
        }

    def _check_ftpa_partner_data(self, cr, uid, ids, context={}):
        for partner in self.browse(cr, uid, ids):
            if partner.electronic_invoice_subjected:
                if partner.is_pa and (
                    not partner.ipa_code or len(partner.ipa_code) != 6
                ):
                    raise except_osv(_('Error' ),
                             _(
                        "Il partner %s, essendo una pubblica amministrazione "
                        "deve avere il codice IPA lungo 6 caratteri"
                    ) % partner.name)
                if not partner.is_pa and (
                    not partner.codice_destinatario or
                    len(partner.codice_destinatario) != 7
                ):
                    raise except_osv(_('Error' ),_(
                        "Il partner %s "
                        "deve avere il Codice Destinatario lungo 7 caratteri"
                    ) % partner.name)
                if (
                    not partner.is_pa and
                    partner.codice_destinatario == '0000000'
                ):
                    if not partner.vat and not partner.fiscalcode:
                        raise except_osv(_('Error' ),_(
                            "Il partner %s, con Codice Destinatario '0000000',"
                            " deve avere o P.IVA o codice fiscale"
                        ) % partner.name)
                if partner.customer:
                    address = partner.address and partner.address[0] or False
                    if not address or not address.street:
                        raise except_osv(_('Error' ),_(
                            'Customer %s: street is needed for XML generation.'
                        ) % partner.name)
                    if not address or not address.zip:
                        raise except_osv(_('Error' ),_(
                            'Customer %s: ZIP is needed for XML generation.'
                        ) % partner.name)
                    if not address or not address.city:
                        raise except_osv(_('Error' ),_(
                            'Customer %s: city is needed for XML generation.'
                        ) % partner.name)
                    if not address or not address.country_id:
                        raise except_osv(_('Error' ),_(
                            'Customer %s: country is needed for XML'
                            ' generation.'
                        ) % partner.name)
        return True

    _constraints = [
        (_check_ftpa_partner_data, 'Some customer infos are needed.', [
            'is_pa', 'ipa_code', 'codice_destinatario', 'company_type',
            'electronic_invoice_subjected', 'vat', 'fiscalcode',
            'customer', 'street', 'zip', 'city', 'country_id']),
    ]

