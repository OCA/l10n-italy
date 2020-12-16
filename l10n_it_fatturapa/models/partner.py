# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, orm
from openerp.osv.osv import except_osv
STANDARD_ADDRESSEE_CODE = '0000000'
from openerp.tools.translate import _


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
            "Codice Destinatario",
            help="Il codice, di 7 caratteri, assegnato dal Sdi ai soggetti che "
             "hanno accreditato un canale; qualora il destinatario non abbia "
             "accreditato un canale presso Sdi e riceva via PEC le fatture, "
             "l'elemento deve essere valorizzato con tutti zeri ('0000000'). "),
        # 1.1.6
        'pec_destinatario': fields.char(
            "PEC destinatario",
            help="Indirizzo PEC al quale inviare la fattura elettronica. "
                 "Da valorizzare "
                 "SOLO nei casi in cui l'elemento informativo "
                 "<CodiceDestinatario> vale '0000000'"),
        'electronic_invoice_subjected': fields.boolean(
            "Subjected to electronic invoice"),
    


    'electronic_invoice_subjected': fields.boolean(
        "Enable electronic invoicing"),
    'electronic_invoice_obliged_subject': fields.boolean(
        "Obliged Subject"),
    'electronic_invoice_data_complete': fields.boolean(
        compute="_compute_electronic_invoice_data_complete"),

    'electronic_invoice_no_contact_update': fields.boolean(
        "Do not update the contact from Electronic Invoice Details"),

    'electronic_invoice_use_this_address': fields.boolean(
        "Use this e-invoicing data when invoicing to this address",
        help="Set this when the main company has got several Addressee Codes or PEC"
    ),
}
    
    _defaults = {
        'codice_destinatario': STANDARD_ADDRESSEE_CODE,
        }

    def _compute_electronic_invoice_data_complete(self, cr, uid, ids, context={}):
        check_fatturapa_fields = self._check_ftpa_partner_data._constrains
        for partner in self.browse(cr, uid, ids, context=context):
            partner.electronic_invoice_data_complete = True
            partner_values = partner.read(check_fatturapa_fields)[0]
            partner_values['electronic_invoice_subjected'] = True
            partner_dummy = self.new(partner_values)
            try:
                partner_dummy._check_ftpa_partner_data()
            except Exception:
                partner.electronic_invoice_data_complete = False

    def _check_ftpa_partner_data(self, cr, uid, ids, context={}):
        for partner in self.browse(cr, uid, ids):
            if partner.electronic_invoice_subjected and partner.customer:
                if partner.is_pa and (
                    not partner.ipa_code or len(partner.ipa_code) != 6
                ):
                    raise except_osv(_('Error' ),
                             _(
                        "Il partner %s, essendo una pubblica amministrazione "
                        "deve avere il codice IPA lungo 6 caratteri"
                    ) % partner.name)
                if not partner.is_company and (
                    not partner.lastname or not partner.firstname
                ):
                    raise except_osv(_('Error' ),_(
                        "Il partner %s, essendo persona "
                        "deve avere Nome e Cognome"
                    ) % partner.name)
                if (
                    not partner.is_pa
                    and not partner.codice_destinatario
                ):
                    raise except_osv(_('Error' ),_(
                        "Partner %s must have Addresse Code. Use %s if unknown"
                    ) % (partner.name, STANDARD_ADDRESSEE_CODE))
                if (
                    not partner.is_pa
                    and partner.codice_destinatario
                    and len(partner.codice_destinatario) != 7
                ):
                    raise except_osv(_('Error' ),_(
                        "Partner %s Addressee Code "
                        "must be 7 characters long."
                    ) % partner.name)
                if partner.pec_destinatario:
                    if partner.codice_destinatario != STANDARD_ADDRESSEE_CODE:
                        raise except_osv(_('Error' ),_(
                            "Partner %s has Addressee PEC %s, "
                            "the Addresse Code must be %s."
                        ) % (partner.name,
                             partner.pec_destinatario,
                             STANDARD_ADDRESSEE_CODE))
                if (
                    not partner.vat and not partner.fiscalcode and
                    partner.country_id.code == 'IT'
                ):
                    raise except_osv(_('Error' ),_(
                        "Italian partner %s must "
                        "have VAT Number or Fiscal Code."
                    ) % partner.name)
                if partner.customer:
                    if not partner.street:
                        raise except_osv(_('Error' ),_(
                            'Customer %s: street is needed for XML generation.'
                        ) % partner.name)
                    if not partner.zip and partner.country_id.code == 'IT':
                        raise except_osv(_('Error' ),_(
                            'Italian partner %s: ZIP is needed for XML generation.'
                        ) % partner.name)
                    if not partner.city:
                        raise except_osv(_('Error' ),_(
                            'Customer %s: city is needed for XML generation.'
                        ) % partner.name)
                    if not partner.country_id:
                        raise except_osv(_('Error' ),_(
                            'Customer %s: country is needed for XML'
                            ' generation.'
                        ) % partner.name)
        return True

    def onchange_country_id_e_inv(self, cr, uid, ids, country_id, context=None):
        out = {'value': {}}
        out['value']['country_id'] = country_id
        if not country_id:
            out['value']['codice_destinatario'] = 'XXXXXXX'
        else:
            countryBrws = self.pool.get('res.country').browse(cr, uid, country_id)
            if countryBrws.code == 'IT':
                out['value']['codice_destinatario'] = STANDARD_ADDRESSEE_CODE
            else:
                out['value']['codice_destinatario'] = 'XXXXXXX'
        return out

    def onchange_electronic_invoice_subjected(self, cr, uid, ids, electronic_invoice_subjected, electronic_invoice_obliged_subject, country_id, context={}):
        out = {'value': {'electronic_invoice_subjected': electronic_invoice_subjected}}
        for partner in self.browse(cr, uid, ids, context):
            if not electronic_invoice_subjected:
                out['value']['electronic_invoice_obliged_subject'] = False
            else:
                if partner.supplier:
                    out.update(self.onchange_country_id_e_inv(cr, uid, ids, electronic_invoice_obliged_subject, country_id))
                    out['value']['electronic_invoice_obliged_subject'] = True
        return out

    def onchange_e_inv_obliged_subject(self, cr, uid, ids, electronic_invoice_obliged_subject, country_id, context={}):
        out = {'value': {'electronic_invoice_obliged_subject': electronic_invoice_obliged_subject}}
        if not electronic_invoice_obliged_subject:
            out.update(self.onchange_country_id_e_inv(cr, uid, ids, country_id))
            out['value']['self.pec_destinatario'] = ''
            out['value']['self.eori_code'] = ''
        return out

    _constraints = [
        (_check_ftpa_partner_data, 'Some customer infos are needed.', [
            'is_pa', 'ipa_code', 'codice_destinatario', 'company_type',
            'electronic_invoice_subjected', 'vat', 'fiscalcode', 'lastname',
            'firstname', 'customer', 'street', 'zip', 'city',
            'country_id']),
    ]

