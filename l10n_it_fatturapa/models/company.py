# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    fatturapa_fiscal_position_id = fields.Many2one(
        'fatturapa.fiscal_position', 'Fiscal Position',
        help="Fiscal position used by FatturaPA",
        )
    fatturapa_sequence_id = fields.Many2one(
        'ir.sequence', 'Sequence',
        help="il progressivo univoco del file è rappresentato da una "
             "stringa alfanumerica di lunghezza massima di 5 caratteri "
             "e con valori ammessi da “A” a “Z” e da “0” a “9”.",
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
        'res.partner', 'Third Party/Sender'
        )


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    fatturapa_fiscal_position_id = fields.Many2one(
        related='company_id.fatturapa_fiscal_position_id',
        string="Fiscal Position",
        help='Fiscal position used by FatturaPA'
        )
    fatturapa_sequence_id = fields.Many2one(
        related='company_id.fatturapa_sequence_id',
        string="Sequence",
        help="il progressivo univoco del file è rappresentato da una "
             "stringa alfanumerica di lunghezza massima di 5 caratteri "
             "e con valori ammessi da “A” a “Z” e da “0” a “9”.",
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
        help="Used when a foreign company needs to send invoices to an"
             "Italian PA and has a tax representative in Italy"
        )
    fatturapa_sender_partner = fields.Many2one(
        related='company_id.fatturapa_sender_partner',
        string="Third Party/Sender",
        help="Used when company sends invoices to a third party and they "
             "send invoices to SDI"
        )

    @api.onchange('company_id')
    def onchange_company_id(self):
        res = super(AccountConfigSettings, self).onchange_company_id()
        if self.company_id:
            company = self.company_id
            self.fatturapa_fiscal_position_id = (
                company.fatturapa_fiscal_position_id and
                company.fatturapa_fiscal_position_id.id or False
                )
            self.fatturapa_sequence_id = (
                company.fatturapa_sequence_id and
                company.fatturapa_sequence_id.id or False
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
        return res
