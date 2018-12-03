# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    eori_code = fields.Char('EORI Code', size=20)
    license_number = fields.Char('License Code', size=20)
    # 1.2.6 RiferimentoAmministrazione
    pa_partner_code = fields.Char('PA Code for partner', size=20)
    # 1.2.1.4
    register = fields.Char('Professional Register', size=60)
    # 1.2.1.5
    register_province = fields.Many2one(
        'res.country.state', string='Register Province')
    # 1.2.1.6
    register_code = fields.Char('Register Code', size=60)
    # 1.2.1.7
    register_regdate = fields.Date('Register Registration Date')
    # 1.2.1.8
    register_fiscalpos = fields.Many2one(
        'fatturapa.fiscal_position',
        string="Register Fiscal Position")
    # 1.1.4
    codice_destinatario = fields.Char(
        "Codice Destinatario",
        help="Il codice, di 7 caratteri, assegnato dal Sdi ai soggetti che "
             "hanno accreditato un canale; qualora il destinatario non abbia "
             "accreditato un canale presso Sdi e riceva via PEC le fatture, "
             "l'elemento deve essere valorizzato con tutti zeri ('0000000'). ",
        default='0000000')
    # 1.1.6
    pec_destinatario = fields.Char(
        "PEC destinatario",
        help="Indirizzo PEC al quale inviare la fattura elettronica. "
             "Da valorizzare "
             "SOLO nei casi in cui l'elemento informativo "
             "<CodiceDestinatario> vale '0000000'"
    )
    electronic_invoice_subjected = fields.Boolean(
        "Subjected to electronic invoice")

    @api.multi
    @api.constrains(
        'is_pa', 'ipa_code', 'codice_destinatario', 'is_company',
        'electronic_invoice_subjected', 'vat', 'fiscalcode', 'lastname',
        'firstname', 'customer', 'street', 'zip', 'city', 'state_id',
        'country_id'
    )
    def _check_ftpa_partner_data(self):
        for partner in self:
            if partner.electronic_invoice_subjected and partner.customer:
                # These checks must be done for customers only, as only
                # needed for XML generation
                if partner.is_pa and \
                        (not partner.ipa_code or len(partner.ipa_code) != 6):
                    raise ValidationError(_(
                        "As a Public Administration, partner %s IPA Code "
                        "must be 6 characters long"
                    ) % partner.name)
                if not partner.is_company and \
                        (not partner.lastname or not partner.firstname):
                    raise ValidationError(_(
                        "As a natural person, partner %s "
                        "must have Name and Surname"
                    ) % partner.name)
                if not partner.is_pa and (
                    not partner.codice_destinatario or
                        len(partner.codice_destinatario) != 7):
                    raise ValidationError(_("Partner %s Addressee Code"
                                            " must be 7 characters long")
                                          % partner.name)
                if not partner.vat and not partner.fiscalcode:
                    raise ValidationError(_(
                        "Partner %s, must have VAT Number or Fiscal Code"
                    ) % partner.name)
                if not partner.street:
                    raise ValidationError(_(
                        'Customer %s: street is needed for XML generation.'
                    ) % partner.name)
                if not partner.zip:
                    raise ValidationError(_(
                        'Customer %s: ZIP is needed for XML generation.'
                    ) % partner.name)
                if not partner.city:
                    raise ValidationError(_(
                        'Customer %s: city is needed for XML generation.'
                    ) % partner.name)
                if not partner.state_id:
                    raise ValidationError(_(
                        'Customer %s: province is needed for XML '
                        'generation.'
                    ) % partner.name)
                if not partner.country_id:
                    raise ValidationError(_(
                        'Customer %s: country is needed for XML'
                        ' generation.'
                    ) % partner.name)
