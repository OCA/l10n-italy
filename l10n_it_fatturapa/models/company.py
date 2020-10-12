# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    fatturapa_fiscal_position_id = fields.Many2one(
        'fatturapa.fiscal_position', 'Fiscal Position',
        help="Fiscal position used by electronic invoice",
        )
    fatturapa_sequence_id = fields.Many2one(
        'ir.sequence', 'E-invoice Sequence',
        help="The univocal progressive of the file is represented by "
             "an alphanumeric sequence of maximum length 5, "
             "its values are included in 'A'-'Z' and '0'-'9'"
        )
    fatturapa_art73 = fields.Boolean('Art. 73')
    fatturapa_pub_administration_ref = fields.Char(
        'Public Administration Reference Code', size=20,
        )
    fatturapa_rea_office = fields.Many2one(
        related="partner_id.rea_office", string='REA office')
    fatturapa_rea_number = fields.Char(
        related="partner_id.rea_code", string='Rea Number')
    fatturapa_rea_capital = fields.Float(
        related='partner_id.rea_capital',
        string='Rea Capital')
    fatturapa_rea_partner = fields.Selection(
        related='partner_id.rea_member_type',
        string='Member Type')
    fatturapa_rea_liquidation = fields.Selection(
        related='partner_id.rea_liquidation_state',
        string='Liquidation State')
    fatturapa_tax_representative = fields.Many2one(
        'res.partner', 'Legal Tax Representative'
        )
    fatturapa_sender_partner = fields.Many2one(
        'res.partner', 'Third Party/Sender',
        help="Data of Third-Party Issuer Intermediary who emits the "
             "invoice on behalf of the seller/provider"
        )
    fatturapa_stabile_organizzazione = fields.Many2one(
        'res.partner', 'Stable Organization',
        help='The fields must be entered only when the seller/provider is '
             'non-resident, with a stable organization in Italy'
        )
    fatturapa_preview_style = fields.Selection([
        ('fatturaordinaria_v1.2.1.xsl', 'FatturaOrdinaria v1.2.1'),
        ('FoglioStileAssoSoftware_v1.1.xsl', 'AssoSoftware v1.1')],
        string='Preview Format Style', required=True,
        default='fatturaordinaria_v1.2.1.xsl')

    @api.multi
    @api.constrains(
        'fatturapa_sequence_id'
    )
    def _check_fatturapa_sequence_id(self):
        for company in self:
            if company.fatturapa_sequence_id:
                if company.fatturapa_sequence_id.use_date_range:
                    raise ValidationError(_(
                        "Sequence %s can't use subsequences."
                    ) % company.fatturapa_sequence_id.name)
                journal = self.env['account.journal'].search([
                    ('sequence_id', '=', company.fatturapa_sequence_id.id)
                ], limit=1)
                if journal:
                    raise ValidationError(_(
                        "Sequence %s already used by journal %s. Please select"
                        " another one."
                    ) % (company.fatturapa_sequence_id.name, journal.name))


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    fatturapa_fiscal_position_id = fields.Many2one(
        related='company_id.fatturapa_fiscal_position_id',
        string="Fiscal Position",
        help='Fiscal position used by electronic invoice',
        readonly=False,
        )
    fatturapa_sequence_id = fields.Many2one(
        related='company_id.fatturapa_sequence_id',
        string="Sequence",
        help="The univocal progressive of the file is represented by "
             "an alphanumeric sequence of maximum length 5, "
             "its values are included in 'A'-'Z' and '0'-'9'",
        readonly=False
        )
    fatturapa_art73 = fields.Boolean(
        related='company_id.fatturapa_art73',
        string="Art. 73",
        help="Indicates whether the document has been issued according to "
             "methods and terms laid down in a ministerial decree under "
             "the terms of Article 73 of Italian Presidential Decree "
             "633/72 (this enables the company to issue in the same "
             "year several documents with same number)",
        readonly=False
        )
    fatturapa_pub_administration_ref = fields.Char(
        related='company_id.fatturapa_pub_administration_ref',
        string="Public Administration Reference Code",
        readonly=False
        )
    fatturapa_rea_office = fields.Many2one(
        related='company_id.rea_office',
        string="REA Office",
        readonly=False
        )
    fatturapa_rea_number = fields.Char(
        related='company_id.rea_code',
        string="REA Number",
        readonly=False
        )
    fatturapa_rea_capital = fields.Float(
        related='company_id.rea_capital',
        string="REA Capital",
        readonly=False
        )
    fatturapa_rea_partner = fields.Selection(
        related='company_id.rea_member_type',
        string="REA Copartner",
        readonly=False
        )
    fatturapa_rea_liquidation = fields.Selection(
        related='company_id.rea_liquidation_state',
        string="REA Liquidation",
        readonly=False
        )
    fatturapa_tax_representative = fields.Many2one(
        related='company_id.fatturapa_tax_representative',
        string="Legal Tax Representative",
        help='The fields must be entered only when the seller/provider makes '
             'use of a tax representative in Italy',
        readonly=False
        )
    fatturapa_sender_partner = fields.Many2one(
        related='company_id.fatturapa_sender_partner',
        string="Third Party/Sender",
        help="Data of Third-Party Issuer Intermediary who emits the "
             "invoice on behalf of the seller/provider",
        readonly=False
        )
    fatturapa_stabile_organizzazione = fields.Many2one(
        related='company_id.fatturapa_stabile_organizzazione',
        string="Stable Organization",
        help="The fields must be entered only when the seller/provider is "
             "non-resident, with a stable organization in Italy",
        readonly=False
        )
    fatturapa_preview_style = fields.Selection(
        related='company_id.fatturapa_preview_style',
        string="Preview Format Style", required=True,
        default='fatturaordinaria_v1.2.1.xsl',
        readonly=False
        )

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            company = self.company_id
            default_sequence = self.env['ir.sequence'].search([
                ('code', '=', 'account.invoice.fatturapa')
            ])
            default_sequence = (
                default_sequence[0].id if default_sequence else False)
            self.fatturapa_fiscal_position_id = (
                company.fatturapa_fiscal_position_id and
                company.fatturapa_fiscal_position_id.id or False
                )
            self.fatturapa_sequence_id = (
                company.fatturapa_sequence_id and
                company.fatturapa_sequence_id.id or default_sequence
                )
            self.fatturapa_art73 = (
                company.fatturapa_art73 or False
                )
            self.fatturapa_pub_administration_ref = (
                company.fatturapa_pub_administration_ref or False
                )
            self.fatturapa_rea_office = (
                company.fatturapa_rea_office and
                company.fatturapa_rea_office.id or False
                )
            self.fatturapa_rea_number = (
                company.fatturapa_rea_number or False
                )
            self.fatturapa_rea_capital = (
                company.fatturapa_rea_capital or False
                )
            self.fatturapa_rea_partner = (
                company.fatturapa_rea_partner or False
                )
            self.fatturapa_rea_liquidation = (
                company.fatturapa_rea_liquidation or False
                )
            self.fatturapa_tax_representative = (
                company.fatturapa_tax_representative and
                company.fatturapa_tax_representative.id or False
                )
            self.fatturapa_sender_partner = (
                company.fatturapa_sender_partner and
                company.fatturapa_sender_partner.id or False
                )
            self.fatturapa_stabile_organizzazione = (
                company.fatturapa_stabile_organizzazione and
                company.fatturapa_stabile_organizzazione.id or False
                )
            self.fatturapa_preview_style = (
                company.fatturapa_preview_style or False
            )
        else:
            self.fatturapa_fiscal_position_id = False
            self.fatturapa_sequence_id = False
            self.fatturapa_art73 = False
            self.fatturapa_pub_administration_ref = False
            self.fatturapa_rea_office = False
            self.fatturapa_rea_number = False
            self.fatturapa_rea_capital = False
            self.fatturapa_rea_partner = False
            self.fatturapa_rea_liquidation = False
            self.fatturapa_tax_representative = False
            self.fatturapa_sender_partner = False
            self.fatturapa_stabile_organizzazione = False
            self.fatturapa_preview_style = 'fatturaordinaria_v1.2.1.xsl'
