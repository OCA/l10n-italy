# -*- coding: utf-8 -*-
# © 2015 Alex Comba - Agile Business Group
# © 2016 Andrea Cometa - Apulia Software
# © 2016-2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def grouped_lines_by_ddt(self):
        """
        Returns invoice lines from a specified invoice grouped by ddt
        """
        all_lines = self.invoice_line_ids
        ddt_dict = {}
        for line in all_lines:
            # group by recordset (that can be empty or bigger then 1)
            ddt_lines = line.get_ddt_lines()
            ddts = ddt_lines.mapped('package_preparation_id')
            if ddts not in ddt_dict:
                ddt_dict[ddts] = [line]
            else:
                ddt_dict[ddts].append(line)
        # convert recordset to string.
        group = {}
        for key in ddt_dict:
            if not key:
                # empty recordset
                string_key = ''
            else:
                string_key = ''
                for ddt in key:
                    if ddt.ddt_number:
                        if string_key:
                            string_key += ', %s' % ddt.ddt_number
                        else:
                            string_key = ddt.ddt_number
            # group dict can be different from ddt_dict,
            # e.g. when DDT does not have a number yet
            if string_key not in group:
                group[string_key] = ddt_dict[key]
            else:
                group[string_key].append(ddt_dict[key])
        return group


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def get_ddt_lines(self):
        self.ensure_one()
        return self.ddt_line_id
