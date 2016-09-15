# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class AccountFiscalyearClosingConfig(models.Model):
    _name = "account.fiscalyear.closing.config"
    _description = "Fiscal year closing move config"
    _order = "sequence asc, id asc"

    name = fields.Char(string="Description", required=True)
    sequence = fields.Integer(string="Sequence", index=True, default=1)
    code = fields.Char(string="Unique code", required=True)
    inverse = fields.Char(
        string="Inverse config",
        help="Configuration code to inverse its move")
    reconcile = fields.Boolean(
        string="Reconcile",
        help="Reconcile inverse move")
    fyc_id = fields.Many2one(
        comodel_name='account.fiscalyear.closing', index=True, readonly=True,
        string="Fiscal Year Closing", required=True, ondelete='cascade')
    move_type = fields.Selection(selection=[
        ('closing', 'Closing'),
        ('opening', 'Opening'),
    ], string="Move type", readonly=True, default='closing')
    enable = fields.Boolean(string="Enable", default=True)
    date = fields.Date(
        string="Move date", compute='_compute_date', readonly=True)
    journal_id = fields.Many2one(
        comodel_name="account.journal", string="Journal", required=True)
    move_id = fields.Many2one(
        comodel_name="account.move", string="Move")
    mapping_ids = fields.One2many(
        comodel_name='account.fiscalyear.closing.mapping',
        inverse_name='fyc_config_id', string="Account mappings")
    closing_type_default = fields.Selection(selection=[
        ('balance', 'Balance'),
        ('unreconciled', 'Un-reconciled'),
    ], string="Default closing type", required=True, default='balance')
    closing_type_ids = fields.One2many(
        comodel_name='account.fiscalyear.closing.type',
        inverse_name='fyc_config_id', string="Closing types")

    _sql_constraints = [
        ('code_uniq', 'unique(code, fyc_id)',
         _('Code must be unique per fiscal year closing!')),
    ]

    @api.multi
    @api.depends('move_type', 'fyc_id.date_end', 'fyc_id.date_opening')
    def _compute_date(self):
        for config in self:
            if config.move_type == 'closing':
                config.date = config.fyc_id.date_end
            else:
                config.date = config.fyc_id.date_opening

    @api.multi
    def config_inverse_get(self):
        configs = self.env['account.fiscalyear.closing.config']
        for config in self:
            code = config.inverse and config.inverse.strip()
            if code:
                configs |= self.search([
                    ('fyc_id', '=', config.fyc_id.id),
                    ('code', '=', code),
                ])
        return configs

    @api.multi
    def closing_type_get(self, account):
        self.ensure_one()
        closing_type = self.closing_type_default
        closing_types = self.closing_type_ids.filtered(
            lambda r: r.account_type_id == account.user_type_id)
        if closing_types:
            closing_type = closing_types[0].closing_type
        return closing_type

    @api.multi
    def move_prepare(self, move_lines):
        self.ensure_one()
        move = {}
        description = self.name
        journal_id = self.journal_id.id
        date = self.fyc_id.date_end
        if self.move_type == 'opening':
            date = self.fyc_id.date_opening
        if move_lines:
            move = {
                'ref': description,
                'date': date,
                'fyc_id': self.fyc_id.id,
                'journal_id': journal_id,
                'line_ids': [(0, 0, m) for m in move_lines],
            }
        return move

    def _mapping_move_lines_get(self):
        move_lines = []
        dst_totals = {}
        # Add balance/unreconciled move lines
        for account_map in self.mapping_ids:
            # Init destination account totals
            dst_id = account_map.dst_account_id.id
            if dst_id and dst_totals.get(dst_id) is None:
                dst_totals[dst_id] = 0
            for account in account_map.src_account_ids:
                move_line = False
                closing_type = self.closing_type_get(account)
                if closing_type == 'balance':
                    # Get all lines
                    lines = account_map.account_lines_get(account)
                    balance, move_line = account_map.move_line_prepare(
                        account, lines)
                    if move_line:
                        move_lines.append(move_line)
                elif closing_type == 'unreconciled':
                    # Get credit and debit grouping by partner
                    partners = account_map.account_partners_get(account)
                    for partner in partners:
                        balance, move_line = account_map.\
                            move_line_partner_prepare(account, partner)
                        if move_line:
                            move_lines.append(move_line)
                else:
                    # Account type has unsupported closing method
                    continue
                if dst_id and balance:
                    dst_totals[dst_id] -= balance
        # Add destination move lines, if any
        for account_map in self.mapping_ids.filtered('dst_account_id'):
            dst_id = account_map.dst_account_id.id
            balance = dst_totals.get(dst_id, 0)
            if balance:
                dst_totals[dst_id] = 0
                move_line = account_map.dst_move_line_prepare(dst_id, balance)
                if move_line:
                    move_lines.append(move_line)
        return move_lines

    @api.multi
    def inverse_move_prepare(self):
        self.ensure_one()
        move = False
        date = self.fyc_id.date_end
        if self.move_type == 'opening':
            date = self.fyc_id.date_opening
        config = self.config_inverse_get()
        if config.move_id:
            move = config.move_id._move_reverse_prepare(
                date=date, journal=self.journal_id)
            move['line_ids'] = config.move_id._move_lines_reverse_prepare(
                move.get('line_ids', []), date=date, journal=self.journal_id)
            move['ref'] = self.name
        return move

    @api.multi
    def moves_create(self):
        moves = self.env['account.move']
        for config in self:
            # Prepare one move per configuration
            data = False
            if config.mapping_ids:
                move_lines = self._mapping_move_lines_get()
                data = config.move_prepare(move_lines)
            elif config.inverse:
                data = self.inverse_move_prepare()
            # Create move
            if data:
                move = moves.create(data)
                config.move_id = move.id
                moves |= move
        return moves
