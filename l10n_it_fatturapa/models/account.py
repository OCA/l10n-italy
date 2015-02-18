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
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields

AVAILABLE_STATES = [
    ('draft', 'Draft'),
    ('sent', 'Sent'),
    ('rejected', 'Rejected'),
    ('accepted', 'Accepted')]


class fatturapa_document_type(models.Model):
    _name = "fatturapa.document_type"
    _description = 'FatturaPA Document Type'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class fatturapa_payment_term(models.Model):
    _name = "fatturapa.payment_term"
    _description = 'FatturaPA Payment Term'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class fatturapa_payment_method(models.Model):
    _name = "fatturapa.payment_method"
    _description = 'FatturaPA Payment Method'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class fatturapa_fiscal_position(models.Model):
    _name = "fatturapa.fiscal_position"
    _description = 'FatturaPA Fiscal Position'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class fatturapa_format(models.Model):
    _name = "fatturapa.format"
    _description = 'FatturaPA Format'

    name = fields.Char('Description', size=128)
    code = fields.Char('Code', size=4)


class account_payment_term(models.Model):
    _inherit = 'account.payment.term'

    fatturapa_pt_id = fields.Many2one(
        'fatturapa.payment_term',
        string="FatturaPA Payment Term")
    fatturapa_pm_id = fields.Many2one(
        'fatturapa.payment_method',
        string="FatturaPA Payment Method")


class account_invoice(models.Model):
    _inherit = "account.invoice"

    fatturapa_po_enable = fields.Boolean('FatturaPA Purchase Order')
    fatturapa_po = fields.Char('FatturaPA Purchase Order Number', size=64)
    fatturapa_po_line_no = fields.Integer('FatturaPA PO Line No')
    fatturapa_po_cup = fields.Char('FatturaPA PO CUP', size=64)
    fatturapa_po_cig = fields.Char('FatturaPA PO CIG', size=64)
    fatturapa_contract_enable = fields.Boolean('FatturaPA Contract')
    fatturapa_contract = fields.Char('FatturaPA Contract Number', size=64)
    fatturapa_contract_line_no = fields.Char(
        'FatturaPA Contract Line No', size=12)
    fatturapa_contract_date = fields.Date('FatturaPA Contract Date')
    fatturapa_contract_numitem = fields.Char(
        'FatturaPA Contract NumItem', size=64)
    fatturapa_contract_cup = fields.Char(
        'FatturaPA Contract CUP', size=64)
    fatturapa_contract_cig = fields.Char(
        'FatturaPA Contract CIG', size=64)
    fatturapa_agreement_enable = fields.Boolean('FatturaPA Agreement')
    fatturapa_agreement = fields.Char('FatturaPA Agreement Number', size=64)
    fatturapa_agreement_line_no = fields.Char(
        'FatturaPA Agreement Line No', size=12)
    fatturapa_agreement_date = fields.Date('FatturaPA Agreement Date')
    fatturapa_agreement_numitem = fields.Char(
        'FatturaPA Agreement NumItem', size=64)
    fatturapa_agreement_cup = fields.Char(
        'FatturaPA Agreement CUP', size=64)
    fatturapa_agreement_cig = fields.Char(
        'FatturaPA Agreement CIG', size=64)
    fatturapa_reception_enable = fields.Boolean('FatturaPA Reception')
    fatturapa_reception = fields.Char(
        'FatturaPA Reception Number', size=64)
    fatturapa_reception_line_no = fields.Char(
        'FatturaPA Reception Line No', size=12)
    fatturapa_reception_date = fields.Date('FatturaPA Reception Date')
    fatturapa_reception_numitem = fields.Char(
        'FatturaPA Reception NumItem', size=64)
    fatturapa_reception_cup = fields.Char(
        'FatturaPA Reception CUP', size=64)
    fatturapa_reception_cig = fields.Char(
        'FatturaPA Reception CIG', size=64)
    fatturapa_attachment_id = fields.Many2one(
        'fatturapa.attachment', 'FatturaPA Export File')
    fatturapa_attachment_state = fields.Selection(
        related='fatturapa_attachment_id.state', type='selection', store=True,
        selection=AVAILABLE_STATES, readonly=True, select=True,
        string='FatturaPA Export State')
