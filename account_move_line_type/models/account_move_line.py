#
# Copyright 2020-22 SHS-AV s.r.l. <https://www.zeroincombenze.it>
# Copyright 2020-22 powERP enterprise network <https://www.powerp.it>
# Copyright 2020-22 Didotech s.r.l. <https://www.didotech.com>
#

import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def get_line_type(self, vals=None, duedate_mode=None):
        """
        Get line type in order to manage invoice moves; type 'lp' and 'tax' can
        be found only in invoices moves. Generic account move can contains
        'receivable', 'payable' an 'other' type line.
        :return:
        'receivable': line is a customer line and can be reconciled
        'payable': line is a supplier line and can be reconciled
        'liquidity': line with bank or cash account
        'lp': line is a loss / profit line with tax code (only invoices)
        'tax': tax line of previous 'lp' line (only invoices)
        'other': any line not in previous list
        """
        def get_line_type_from_dict(vals=None, duedate_mode=None):
            line_type = 'other'
            if vals.get('account_id'):
                acc = self.env['account.account'].search(
                    [('id', '=', vals['account_id'])])
                line_type = acc.user_type_id.type
            if (duedate_mode and line_type in ('receivable', 'payable') and
                    (not vals.get('date_maturity') or
                     vals.get('tax_ids') or vals.get('tax_line_id'))):
                line_type = 'other'
            if line_type == 'other' and vals.get('journal_id'):
                journal = self.env['account.journal'].browse(
                    vals['journal_id'])
                if journal.type in ('purchase', 'sale'):
                    if vals.get('tax_ids'):
                        line_type = 'lp'
                    elif vals.get('tax_line_id'):
                        line_type = 'tax'
            return line_type

        if vals:
            return get_line_type_from_dict(vals, duedate_mode=duedate_mode)
        line_type = (self.account_id.user_type_id.type
                     if self.account_id else 'other')
        if (duedate_mode and line_type in ('receivable', 'payable') and
                (not self.date_maturity or self.tax_ids or self.tax_line_id)):
            line_type = 'other'
        if (line_type == 'other' and self.journal_id and
                self.journal_id.type in ('purchase', 'sale')):
            if self.tax_ids:
                line_type = 'lp'
            elif self.tax_line_id:
                line_type = 'tax'
        return line_type

    @api.multi
    @api.depends('account_id', 'tax_ids', 'tax_line_id')
    def _compute_line_type(self):
        for line in self:
            line.line_type = 'other'
            if line.account_id:
                account_type = self.env['account.account.type'].search(
                    [('id', '=', line.account_id.user_type_id.id)])
                if account_type:
                    if account_type.type == 'payable' and \
                            not line.tax_ids and not line.tax_line_id \
                            and line.journal_id.type == 'purchase':
                        line.line_type = 'debit'
                    elif account_type.type == 'receivable' and \
                            not line.tax_ids and not line.tax_line_id \
                            and line.journal_id.type == 'sale':
                        line.line_type = 'credit'
                    elif line.tax_ids and line.journal_id.type in \
                            ('purchase', 'sale'):
                        line.line_type = 'lp'
                    elif line.tax_line_id.id and line.journal_id.type in \
                            ('purchase', 'sale'):
                        line.line_type = 'tax'
    # TODO selection?
    line_type = fields.Char(
        string="Tipo di riga",
        compute='_compute_line_type',
        store=True
        # required=True,
    )
