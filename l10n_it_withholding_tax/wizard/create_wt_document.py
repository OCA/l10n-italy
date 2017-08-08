# -*- coding: utf-8 -*-
# Copyright © 2015 Alessandro Camilli (<http://www.openforce.it>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models, fields, api, _
from openerp.exceptions import Warning, ValidationError


class wizard_create_wt_document(models.TransientModel):
    _name = "withholding.tax.wizard.create.document"

    def _default_lines(self):
        # Any account move must exists in the statements
        move_ids = self._context.get('active_ids', False)
        domain = [('move_id', 'in', move_ids)]
        statements = self.env['withholding.tax.statement'].search(domain)
        if statements:
            raise ValidationError(
                _('Error! Wt statement already exists for this move'))
        # move lines
        lines = []
        move_ids = self._context.get('active_ids', False)
        if move_ids:
            domain = [('move_id', 'in', move_ids),
                      ('account_id.type', 'in', ['payable', 'receivable'])]
            move_lines = self.env['account.move.line'].search(domain)
            if move_lines:
                for ml in move_lines:
                    val = {
                        'account_line_id': ml.id,
                        'account_line_credit': ml.credit,
                        'account_line_debit': ml.debit,
                    }
                lines.append((0, 0, val))
        return lines

    def _default_partner(self):
        partner_id = False
        move_ids = self._context.get('active_ids', False)
        if move_ids:
            domain = [('move_id', 'in', move_ids),
                      ('account_id.type', 'in', ['payable', 'receivable'])]
            move_line = self.env['account.move.line'].search(domain, limit=1)
            if move_line:
                partner_id = move_line.partner_id.id
        return partner_id

    def _default_date(self):
        date = False
        move_ids = self._context.get('active_ids', False)
        if move_ids:
            domain = [('id', 'in', move_ids)]
            move = self.env['account.move'].search(domain, limit=1)
            if move:
                date = move.date
        return date

    date = fields.Date(string='Date', required=True, default=_default_date)
    partner_id = fields.Many2one(
        'res.partner', string="Partner", required=True,
        default=_default_partner)
    line_ids = fields.One2many(
        'withholding.tax.wizard.create.document.line', 'wiz_id',
        string="Partner", required=True, default=_default_lines)

    @api.multi
    def create_wt_document(self):
        statement_ids = []
        for wiz in self:
            for line in wiz.line_ids:

                if line.wt_type:
                    # Statement
                    val = {
                        'move_id': line.account_line_id.move_id.id,
                        'date': wiz.date,
                        'partner_id': wiz.partner_id.id,
                        'withholding_tax_id': line.wt_type.id,
                        'base': line.wt_base,
                        'tax': line.wt_amount,
                    }
                    statement = self.env[
                        'withholding.tax.statement'].create(val)
                    statement_ids.append(statement.id)
                    # Update account move line
                    line.account_line_id.withholding_tax_amount =\
                        line.wt_amount
                    line.account_line_id.withholding_tax_id =\
                        line.wt_type.id
                    line.account_line_id.withholding_tax_base =\
                        line.wt_base

        view_ref = self.env['ir.model.data'].get_object_reference(
            'l10n_it_withholding_tax', 'view_withholding_statement_tree')
        return {
            'name': _('Withholding Tax Statement'),
            'domain': "[('id','in', [" + ','.join(map(str, statement_ids)) + "])]",
            'view_mode': 'tree',
            'view_id': view_ref[1] or False,
            'res_model': 'withholding.tax.statement',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
        }


class wizard_create_wt_document_line(models.TransientModel):
    _name = "withholding.tax.wizard.create.document.line"

    wiz_id = fields.Many2one(
        'withholding.tax.wizard.create.document', string="Wizard Document",
        readonly=True, required=True)
    account_line_id = fields.Many2one(
        'account.move.line', string="Move Line", required=True, readonly=True)
    account_line_credit = fields.Float(string="Credit", readonly=True)
    account_line_debit = fields.Float(string="Debit", readonly=True)
    wt_type = fields.Many2one('withholding.tax', string="WT type")
    wt_base = fields.Float(string="WT base")
    wt_amount = fields.Float(string="WT amount")

    @api.onchange('wt_type')
    def onchange_wt_type(self):
        dp_obj = self.env['decimal.precision']
        self.wt_base = 0
        self.wt_amount = 0
        if self.wt_type:
            if self.account_line_credit:
                base = self.account_line_credit
            else:
                base = self.account_line_debit
            self.wt_base = round(base * self.wt_type.base,
                                 dp_obj.precision_get('Account'))
