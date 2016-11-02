# -*- coding: utf-8 -*-
# © 2015 Alex Comba - Agile Business Group
# © 2016 Andrea Cometa - Apulia Software
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from itertools import groupby
from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def grouped_lines_by_ddt(self):
        """
        Returns invoice lines from a specified invoice grouped by ddt

        :Parameters:
            -'invoice_id' (int): specify the concerned invoice.
        """
        all_lines = self.invoice_line_ids
        ddt_lines_dict = []
        for line in all_lines:
            ddt_lines = line.get_ddt_lines()
            for ddt_line in ddt_lines:
                ddt_lines_dict.append(
                    {'ddt': ddt_line.package_preparation_id.ddt_number,
                     'line': line})
            if not ddt_lines:
                ddt_lines_dict.append({'ddt': '', 'line': line})

        lines = sorted(ddt_lines_dict, key=lambda x: x['ddt'])
        for key, valuesiter in groupby(lines, key=lambda x: x['ddt']):
            group = {}
            group[key] = list(v['line'] for v in valuesiter)

        return group


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def get_ddt_lines(self):
        self.ensure_one()
        ddt_lines = self.env['stock.picking.package.preparation.line'].search(
            [('move_id', 'in', [i.id for i in self.move_line_ids])])
        return ddt_lines