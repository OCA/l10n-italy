# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

STANDARD_ADDRESSEE_CODE = '0000000'


class ResPartner(models.Model):
    _inherit = "res.partner"

    eori_code = fields.Char('EORI Code', size=20)
    license_number = fields.Char('License Code', size=20)
    # 1.2.6 RiferimentoAmministrazione
    pa_partner_code = fields.Char('PA Code for Partner', size=20)
    # 1.2.1.4
    register = fields.Char('Professional Register', size=60)
    # 1.2.1.5
    register_province = fields.Many2one(
        'res.country.state', string='Register Province')
    # 1.2.1.6
    register_code = fields.Char('Register Registration Number', size=60)
    # 1.2.1.7
    register_regdate = fields.Date('Register Registration Date')
    # 1.2.1.8
    register_fiscalpos = fields.Many2one(
        'fatturapa.fiscal_position',
        string="Register Fiscal Position")
    # 1.1.4
    codice_destinatario = fields.Char(
        "Addressee Code",
        help="The code, 7 characters long, assigned by ES to subjects with an "
             "accredited channel; if the addressee didn't accredit a channel "
             "to ES and invoices are received by PEC, the field must be "
             "the standard value ('%s')." % STANDARD_ADDRESSEE_CODE,
        default=STANDARD_ADDRESSEE_CODE)
    # 1.1.6
    pec_destinatario = fields.Char(
        "Addressee PEC",
        help="PEC to which the electronic invoice will be sent. "
             "Must be filled "
             "ONLY when the information element "
             "<CodiceDestinatario> is '%s'" % STANDARD_ADDRESSEE_CODE
    )
    electronic_invoice_subjected = fields.Boolean(
        "Enable electronic invoicing")

    @api.multi
    @api.constrains(
        'is_pa', 'ipa_code', 'codice_destinatario', 'company_type',
        'electronic_invoice_subjected', 'vat', 'fiscalcode', 'lastname',
        'firstname', 'customer', 'street', 'zip', 'city', 'state_id',
        'country_id'
    )
    def _check_ftpa_partner_data(self):
        for partner in self:
            if partner.electronic_invoice_subjected and partner.customer:
                # These checks must be done for customers only, as only
                # needed for XML generation
                if partner.is_pa and (
                    not partner.ipa_code or len(partner.ipa_code) != 6
                ):
                    raise ValidationError(_(
                        "As a Public Administration, partner %s IPA Code "
                        "must be 6 characters long."
                    ) % partner.name)
                if (
                    partner.company_type == 'person' and not
                    partner.company_name and (
                        not partner.lastname or not partner.firstname
                    )
                ):
                    raise ValidationError(_(
                        "As a natural person, partner %s "
                        "must have Name and Surname."
                    ) % partner.name)
                if (
                    not partner.is_pa
                    and not partner.codice_destinatario
                ):
                    raise ValidationError(_(
                        "Partner %s must have Addresse Code. Use %s if unknown"
                    ) % (partner.name, STANDARD_ADDRESSEE_CODE))
                if (
                    not partner.is_pa
                    and partner.codice_destinatario
                    and len(partner.codice_destinatario) != 7
                ):
                    raise ValidationError(_(
                        "Partner %s Addressee Code "
                        "must be 7 characters long."
                    ) % partner.name)
                if partner.pec_destinatario:
                    if partner.codice_destinatario != STANDARD_ADDRESSEE_CODE:
                        raise ValidationError(_(
                            "Partner %s has Addressee PEC %s, "
                            "the Addresse Code must be %s."
                        ) % (partner.name,
                             partner.pec_destinatario,
                             STANDARD_ADDRESSEE_CODE))
                if (
                    not partner.vat and not partner.fiscalcode and
                    partner.country_id.code == 'IT'
                ):
                    raise ValidationError(_(
                        "Italian partner %s must "
                        "have VAT Number or Fiscal Code."
                    ) % partner.name)
                if not partner.street:
                    raise ValidationError(_(
                        'Customer %s: street is needed for XML generation.'
                    ) % partner.name)
                if not partner.zip and partner.country_id.code == 'IT':
                    raise ValidationError(_(
                        'Italian partner %s: ZIP is needed for XML generation.'
                    ) % partner.name)
                if not partner.city:
                    raise ValidationError(_(
                        'Customer %s: city is needed for XML generation.'
                    ) % partner.name)
                if not partner.country_id:
                    raise ValidationError(_(
                        'Customer %s: country is needed for XML'
                        ' generation.'
                    ) % partner.name)

    @api.onchange('country_id')
    def onchange_country_id_e_inv(self):
        if self.country_id.code == 'IT':
            self.codice_destinatario = STANDARD_ADDRESSEE_CODE
        else:
            self.codice_destinatario = 'XXXXXXX'
