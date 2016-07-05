# -*- coding: utf-8 -*-
# © 2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    corrispettivo = fields.Boolean(string='Corrispettivo')

    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(SaleOrder, self)._prepare_invoice(order, lines)
        domain = []
        if order.corrispettivo:
            domain = [
                ('type', '=', 'sale'),
                ('corrispettivi', '=', True)]
        else:
            domain = [
                ('type', '=', 'sale'),
                ('corrispettivi', '=', False)]
        journals = self.env['account.journal'].search(domain)
        if not journals:
            raise UserError(_("Can't find a correct journal"))
        res['journal_id'] = journals[0].id
        res['corrispettivo'] = True
        return res
