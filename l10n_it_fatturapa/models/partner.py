# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


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
             "l'elemento deve essere valorizzato con tutti zeri ('0000000'). ")
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
        'is_pa', 'ipa_code', 'codice_destinatario', 'company_type',
        'electronic_invoice_subjected', 'vat', 'fiscalcode', 'lastname',
        'firstname'
    )
    def _check_ftpa_partner_data(self):
        for partner in self:
            if partner.electronic_invoice_subjected:
                if partner.is_pa and (
                    not partner.ipa_code or len(partner.ipa_code) != 6
                ):
                    raise ValidationError(_(
                        "Il partner %s, essendo una pubblica amministrazione "
                        "deve avere il codice IPA lungo 6 caratteri"
                    ) % partner.name)
                if not partner.is_pa and (
                    not partner.codice_destinatario or
                    len(partner.codice_destinatario) != 7
                ):
                    raise ValidationError(_(
                        "Il partner %s "
                        "deve avere il Codice Destinatario lungo 7 caratteri"
                    ) % partner.name)
                if partner.company_type == 'person' and (
                    not partner.lastname or not partner.firstname
                ):
                    raise ValidationError(_(
                        "Il partner %s, essendo persona "
                        "deve avere Nome e Cognome"
                    ) % partner.name)
                if (
                    not partner.is_pa and
                    partner.codice_destinatario == '0000000'
                ):
                    if not partner.vat and not partner.fiscalcode:
                        raise ValidationError(_(
                            "Il partner %s, con Codice Destinatario '0000000',"
                            " deve avere o P.IVA o codice fiscale"
                        ) % partner.name)
