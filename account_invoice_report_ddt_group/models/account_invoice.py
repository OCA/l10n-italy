# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields, _
import collections


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    has_ddt = fields.Boolean("Has TD", compute="_compute_has_ddt")

    @api.multi
    def group_lines_by_ddt(self):
        self.ensure_one()
        self.invoice_line_ids.filtered(lambda r: r.display_type).unlink()
        grouped_lines = self.grouped_lines_by_ddt()
        line_number = 0
        for ddt in grouped_lines:
            new_line = self.env['account.invoice.line'].create({
                'sequence': line_number,
                'name': ddt or _('No TD'),
                'display_type': 'line_section',
                'invoice_id': self.id
            })
            if grouped_lines[ddt]['shipping_address']:
                new_line.name = "%s\n%s" % (
                    new_line.name, grouped_lines[ddt]['shipping_address'])
            line_number += 1
            for line in grouped_lines[ddt]['lines']:
                line.sequence = line_number
                line_number += 1

    @api.multi
    def grouped_lines_by_ddt(self):
        """
        Returns invoice lines from a specified invoice grouped by ddt
        """
        all_lines = self.invoice_line_ids
        ddt_dict = {}
        # do not consider Sections and Notes: they will be overwritten
        for line in all_lines.filtered(lambda r: not r.display_type):
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
                        ddt_key = '%s - %s' % (
                            ddt.ddt_number, '%s/%s/%s' % (
                                ddt.date.day, ddt.date.month, ddt.date.year)
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
                if (
                    string_key and
                    ddt.partner_shipping_id.commercial_partner_id.
                    ddt_invoice_print_shipping_address
                ):
                    group[string_key]['shipping_address'] =\
                        self._prepare_ddt_shipping_address(
                            ddt.partner_shipping_id)
            else:
                group[string_key]['lines'].extend(ddt_dict[key])
        # Order dict by ddt number
        if group:
            group_ordered = collections.OrderedDict()
            keys_ordered = sorted(group.keys())
            for key in keys_ordered:
                group_ordered[key] = group[key]
            group = group_ordered
        return group

    @api.multi
    def _compute_has_ddt(self):
        for invoice in self:
            invoice.has_ddt = False
            for line in invoice.invoice_line_ids:
                if line.ddt_line_id:
                    invoice.has_ddt = True
                    break

    @api.multi
    def has_serial_number(self):
        self.ensure_one()
        for line in self.invoice_line_ids:
            if line.ddt_line_id.lot_ids:
                return True
        return False

    @api.multi
    def _prepare_ddt_shipping_address(self, partner_shipping_id):
        shipping_address = '{} - {}'.format(partner_shipping_id.display_name,
                                            partner_shipping_id.city or '')
        return shipping_address
