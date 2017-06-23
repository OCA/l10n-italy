# -*- coding: utf-8 -*-
# Copyright 2015 Alex Comba - Agile Business Group
# Copyright 2016 Andrea Cometa - Apulia Software
# Copyright 2016-2017 Lorenzo Battistini - Agile Business Group
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from openerp import models, api, fields
import collections


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
                        if 'DDT' not in ddt_key.upper():
                            ddt_key = 'DDT %s' % (ddt_key)
                        if string_key:
                            string_key += ', %s' % ddt_key
                        else:
                            string_key = ddt_key
            # group dict can be different from ddt_dict,
            # e.g. when DDT does not have a number yet
            if string_key not in group:
                group[string_key] = {'lines': ddt_dict[key]}
                group[string_key]['shipping_address'] = ''
                if string_key and ddt.partner_shipping_id.parent_id.\
                        ddt_invoice_print_shipping_address:
                    group[string_key]['shipping_address'] =\
                        self._prepare_ddt_shipping_address(
                            ddt.partner_shipping_id)
            else:
                group[string_key]['lines'].append(ddt_dict[key])
        # Order dict by ddt number
        if group:
            group_ordered = collections.OrderedDict()
            keys_ordered = sorted(group.keys())
            for key in keys_ordered:
                group_ordered[key] = group[key]
            group = group_ordered
        return group

    @api.multi
    def has_serial_number(self):
        self.ensure_one()
        for line in self.invoice_line_ids:
            if line.ddt_line_id.lot_ids:
                return True
        return False

    @api.multi
    def _prepare_ddt_shipping_address(self, partner_shipping_id):
        shipping_address = '{} - {}'.format(partner_shipping_id.name,
                                            partner_shipping_id.city)
        return shipping_address
