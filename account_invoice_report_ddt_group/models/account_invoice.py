# -*- coding: utf-8 -*-
# Copyright 2015 Alex Comba - Agile Business Group
# Copyright 2016 Andrea Cometa - Apulia Software
# Copyright 2016-2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, api, fields


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
            ddts = line.mapped('ddt_line_id.package_preparation_id')
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
                    if ddt.ddt_number and ddt.date:
                        ddt_date = fields.Date.from_string(ddt.date)
                        ddt_key = '%s - %s' % (
                            ddt.ddt_number, '%s/%s/%s' % (
                                ddt_date.day, ddt_date.month, ddt_date.year)
                        )
                        if string_key:
                            string_key += ', %s' % ddt_key
                        else:
                            string_key = ddt_key
            # group dict can be different from ddt_dict,
            # e.g. when DDT does not have a number yet
            if string_key not in group:
                group[string_key] = ddt_dict[key]
            else:
                group[string_key].append(ddt_dict[key])
        return group

    @api.multi
    def has_serial_number(self):
        self.ensure_one()
        for line in self.invoice_line_ids:
            if line.ddt_line_id.lot_ids:
                return True
        return False
