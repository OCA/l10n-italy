# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, api, _
from openerp.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    fatturapa_fiscal_position_id = fields.Many2one(
        'fatturapa.fiscal_position', 'Fiscal Position',
        help="Fiscal position used by Fattura Elettronica",
        )
    fatturapa_sequence_id = fields.Many2one(
        'ir.sequence', 'Sequence',
        help="The univocal progressive of the file is represented by "
             "an alphanumeric sequence of maximum length 5, "
             "its values are included in 'A'-'Z' and '0'-'9'"
        )
    fatturapa_art73 = fields.Boolean('Art73')
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
        help="Dati relativi al soggetto terzo che emette fattura per conto "
             "del cedente / prestatore"
        )
    fatturapa_stabile_organizzazione = fields.Many2one(
        'res.partner', 'Stabile Organizzazione',
        help='Blocco da valorizzare nei casi di cedente / prestatore non '
             'residente, con stabile organizzazione in Italia'
        )

    @api.multi
    @api.constrains(
        'fatturapa_sequence_id'
    )
    def _check_fatturapa_sequence_id(self):
        for company in self:
            if company.fatturapa_sequence_id:
                journal = self.env['account.journal'].search([
                    ('sequence_id', '=', company.fatturapa_sequence_id.id)
                ], limit=1)
                if journal:
                    raise ValidationError(_(
                        "Sequence %s already used by journal %s. Please select"
                        " another one"
                    ) % (company.fatturapa_sequence_id.name, journal.name))


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    fatturapa_fiscal_position_id = fields.Many2one(
        related='company_id.fatturapa_fiscal_position_id',
        string="Fiscal Position",
        help='Fiscal position used by Fattura Elettronica'
        )
    fatturapa_sequence_id = fields.Many2one(
        related='company_id.fatturapa_sequence_id',
        string="Sequence",
        help="The univocal progressive of the file is represented by "
             "an alphanumeric sequence of maximum length 5, "
             "its values are included in 'A'-'Z' and '0'-'9'"
        )
    fatturapa_art73 = fields.Boolean(
        related='company_id.fatturapa_art73',
        string="Art73",
        help="indicates whether the document has been issued in accordance"
             " with the terms and conditions established by ministerial "
             "decree in accordance with Article 73 of Presidential Decree"
             ""
             "633/72 (this allows the company to issue the same"
             " year more documents with the same number)"
        )
    fatturapa_pub_administration_ref = fields.Char(
        related='company_id.fatturapa_pub_administration_ref',
        string="Public Administration Reference Code"
        )
    fatturapa_rea_office = fields.Many2one(
        related='company_id.fatturapa_rea_office',
        string="Rea Office"
        )
    fatturapa_rea_number = fields.Char(
        related='company_id.fatturapa_rea_number',
        string="Rea Number"
        )
    fatturapa_rea_capital = fields.Float(
        related='company_id.fatturapa_rea_capital',
        string="Rea Capital"
        )
    fatturapa_rea_partner = fields.Selection(
        related='company_id.fatturapa_rea_partner',
        string="Rea Copartner"
        )
    fatturapa_rea_liquidation = fields.Selection(
        related='company_id.fatturapa_rea_liquidation',
        string="Rea Liquidation"
        )
    fatturapa_tax_representative = fields.Many2one(
        related='company_id.fatturapa_tax_representative',
        string="Legal Tax Representative",
        help="Blocco da valorizzare nei casi in cui il cedente / prestatore "
             "si avvalga di un rappresentante fiscale in Italia"
        )
    fatturapa_sender_partner = fields.Many2one(
        related='company_id.fatturapa_sender_partner',
        string="Third Party/Sender",
        help="Dati relativi al soggetto terzo che emette fattura per conto "
             "del cedente / prestatore"
        )
    fatturapa_stabile_organizzazione = fields.Many2one(
        related='company_id.fatturapa_stabile_organizzazione',
        string="Stabile Organizzazione",
        help="Blocco da valorizzare nei casi di cedente / prestatore non "
             "residente, con stabile organizzazione in Italia"
        )

    @api.v7
    def onchange_company_id(self, cr, uid, ids, company_id, context=None):
        res = super(AccountConfigSettings, self).onchange_company_id(
            cr, uid, ids, company_id, context=context)
        if company_id:
            company = self.pool.get('res.company').browse(
                cr, uid, company_id, context=context)
            default_sequence = self.pool.get('ir.sequence').search(cr, uid, [
                ('code', '=', 'account.invoice.fatturapa')
            ])
            default_sequence = (
                default_sequence[0] if default_sequence else False
                )
            res['value'].update({
                'fatturapa_fiscal_position_id': (
                    company.fatturapa_fiscal_position_id and
                    company.fatturapa_fiscal_position_id.id or False
                    ),
                'fatturapa_sequence_id': (
                    company.fatturapa_sequence_id and
                    company.fatturapa_sequence_id.id or default_sequence
                    ),
                'fatturapa_art73': (
                    company.fatturapa_art73 or False
                    ),
                'fatturapa_pub_administration_ref': (
                    company.fatturapa_pub_administration_ref or False
                    ),
                'fatturapa_rea_office': (
                    company.fatturapa_rea_office and
                    company.fatturapa_rea_office.id or False
                    ),
                'fatturapa_rea_number': (
                    company.fatturapa_rea_number or False
                    ),
                'fatturapa_rea_capital': (
                    company.fatturapa_rea_capital or False
                    ),
                'fatturapa_rea_partner': (
                    company.fatturapa_rea_partner or False
                    ),
                'fatturapa_rea_liquidation': (
                    company.fatturapa_rea_liquidation or False
                    ),
                'fatturapa_tax_representative': (
                    company.fatturapa_tax_representative and
                    company.fatturapa_tax_representative.id or False
                    ),
                'fatturapa_sender_partner': (
                    company.fatturapa_sender_partner and
                    company.fatturapa_sender_partner.id or False
                    ),
                'fatturapa_stabile_organizzazione': (
                    company.fatturapa_stabile_organizzazione and
                    company.fatturapa_stabile_organizzazione.id or False
                    ),
                })
        else:
            res['value'].update({
                'fatturapa_fiscal_position_id': False,
                'fatturapa_sequence_id': False,
                'fatturapa_art73': False,
                'fatturapa_pub_administration_ref': False,
                'fatturapa_rea_office': False,
                'fatturapa_rea_number': False,
                'fatturapa_rea_capital': False,
                'fatturapa_rea_partner': False,
                'fatturapa_rea_liquidation': False,
                'fatturapa_tax_representative': False,
                'fatturapa_sender_partner': False,
                'fatturapa_stabile_organizzazione': False,
                })
        return res
