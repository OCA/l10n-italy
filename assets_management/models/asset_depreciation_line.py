# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AssetDepreciationLine(models.Model):
    _name = 'asset.depreciation.line'
    _description = "Assets Depreciations Lines"
    _order = 'date asc, name asc'

    amount = fields.Monetary(
        string="Amount",
    )

    asset_accounting_info_ids = fields.One2many(
        'asset.accounting.info',
        'dep_line_id',
        string="Accounting Info"
    )

    asset_id = fields.Many2one(
        'asset.asset',
        readonly=True,
        related='depreciation_id.asset_id',
        store=True,
        string="Asset"
    )

    balance = fields.Monetary(
        compute='_compute_balance',
        store=True,
        string="Balance",
    )

    base = fields.Float(
        string="Base",
    )

    company_id = fields.Many2one(
        'res.company',
        readonly=True,
        related='depreciation_id.company_id',
    )

    currency_id = fields.Many2one(
        'res.currency',
        readonly=True,
        related='depreciation_id.currency_id',
    )

    date = fields.Date(
        required=True,
        string="Date",
    )

    depreciation_id = fields.Many2one(
        'asset.depreciation',
        ondelete='cascade',
        readonly=True,
        required=True,
        string="Asset depreciation",
    )

    depreciation_line_type_id = fields.Many2one(
        'asset.depreciation.line.type',
        string="Depreciation Type"
    )

    depreciation_nr = fields.Integer(
        string="Dep. Num",
    )

    depreciation_type_id = fields.Many2one(
        'asset.depreciation.type',
        readonly=True,
        related='depreciation_id.type_id',
        store=True,
        string="Asset depreciation type",
    )

    force_dep_nr = fields.Boolean(
        readonly=True,
        related='depreciation_id.force_all_dep_nr',
        string="Force Dep. Num",
    )

    move_id = fields.Many2one(
        'account.move',
        string="Move"
    )

    move_type = fields.Selection(
        [('depreciated', 'Depreciation'),
         ('historical', 'Historical'),
         ('in', 'In'),
         ('out', 'Out'),
         ('loss', 'Capital Loss'),
         ('gain', 'Capital Gain')],
        string="Type",
        required=True
    )

    name = fields.Char(
        required=True,
        string="Name",
    )

    partial_dismissal = fields.Boolean(
        string="Partial Dismissal"
    )

    percentage = fields.Float(
        string="%"
    )

    requires_account_move = fields.Boolean(
        readonly=True,
        related='depreciation_id.type_id.requires_account_move',
        string="Required Account Move",
    )

    requires_depreciation_nr = fields.Boolean(
        compute='_compute_requires_depreciation_nr',
        search='_search_requires_depreciation_nr_lines',
        string="Requires Dep Num"
    )

    # Non-default parameter: set which `move_types` require numeration
    _numbered_move_types = ('depreciated', 'historical')
    # Non-default parameter: set which `move_types` do not concur to
    # asset.depreciation's `amount_residual` field compute
    _non_residual_move_types = ('gain',)
    # Non-default parameter: set which `move_types` get to update the
    # depreciable amount
    _update_move_types = ('in', 'out')

    @api.model
    def create(self, vals):
        line = super().create(vals)
        if line.need_normalize_depreciation_nr():
            line.normalize_depreciation_nr(force=True)
        return line

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        for line in self:
            if line.need_normalize_depreciation_nr():
                line.normalize_depreciation_nr(force=True)
        return res

    @api.multi
    def unlink(self):
        if self.mapped('asset_accounting_info_ids'):
            lines = self.filtered('asset_accounting_info_ids')
            name_list = "\n".join([l[-1] for l in lines.name_get()])
            raise ValidationError(
                _("The lines you you are trying to delete are currently"
                  " linked to accounting info. Please remove them if"
                  " necessary before removing these lines:\n") + name_list
            )
        if any([m.state != 'draft' for m in self.mapped('move_id')]):
            lines = self.filtered(
                lambda l: l.move_id and l.move_id.state != 'draft'
            )
            name_list = "\n".join([l[-1] for l in lines.name_get()])
            raise ValidationError(
                _("Following lines are linked to posted account moves, and"
                  " cannot be deleted:\n") + name_list
            )
        self.mapped('move_id').unlink()
        return super().unlink()

    @api.multi
    def name_get(self):
        return [(line.id, line.make_name()) for line in self]

    @api.constrains('company_id')
    def check_company(self):
        for dep_line in self:
            comp = dep_line.get_linked_aa_info_records().mapped('company_id')
            if len(comp) > 1 or (comp and comp != dep_line.company_id):
                raise ValidationError(
                    _("`{}`: cannot change depreciation line's company once"
                      " it's already related to an asset.")
                    .format(dep_line.make_name())
                )

    @api.constrains('depreciation_nr')
    def check_depreciation_nr_coherence(self):
        for dep in self.mapped('depreciation_id'):
            # Check if any number is negative
            num_lines = dep.line_ids.filtered('requires_depreciation_nr')
            nums = num_lines.mapped('depreciation_nr')
            if nums and min(nums) < 0:
                raise ValidationError(
                    _("Depreciation number can't be a negative number.")
                )

    @api.multi
    @api.depends('amount', 'move_type')
    def _compute_balance(self):
        for line in self:
            if line.move_type in ['out', 'depreciated', 'historical', 'loss']:
                line.balance = - line.amount
            else:
                line.balance = line.amount

    @api.multi
    def _compute_requires_depreciation_nr(self):
        for line in self:
            line.requires_depreciation_nr = line.is_depreciation_nr_required()

    @api.multi
    def _search_requires_depreciation_nr_lines(self, operator, value):
        if operator not in ('=', '!='):
            raise ValidationError(
                _("Invalid search operator!")
            )

        if (operator == '=' and value) or (operator == '!=' and not value):
            return [('move_type', 'in', self.get_numbered_move_types())]
        else:
            return [('move_type', 'not in', self.get_numbered_move_types())]

    @api.onchange('move_type')
    def onchange_move_type(self):
        if self.move_type not in ('in', 'out'):
            self.depreciation_line_type_id = False

    def get_linked_aa_info_records(self):
        self.ensure_one()
        return self.asset_accounting_info_ids

    def get_balances_grouped(self):
        """ Groups balances of line in `self` by line.move_type """
        balances_grouped = {}
        for line in self:
            if line.move_type not in balances_grouped:
                balances_grouped[line.move_type] = 0
            balances_grouped[line.move_type] += line.balance
        return balances_grouped

    def get_depreciation_nr_dict(self):
        """ Returns dict {line: new number} """
        dep = self.mapped('depreciation_id')
        dep.ensure_one()
        lines = dep.line_ids.filtered('requires_depreciation_nr').sorted()
        if not lines:
            return {}

        first_num = 1
        if dep.force_first_dep_nr and dep.first_dep_nr > 0:
            first_num = dep.first_dep_nr

        return {
            line: nr + first_num
            for nr, line in enumerate(lines)
        }

    def get_non_residual_move_types(self):
        """
        Returns list of `move_type` vals that do not concur to
        asset.depreciation's `amount_residual` field compute
        """
        return self._non_residual_move_types

    def get_numbered_move_types(self):
        """ Returns list of `move_type` vals that require numeration """
        return self._numbered_move_types

    def get_update_move_types(self):
        """
        Returns list of `move_type` that concur to update asset.depreciation's
        `amount_depreciable_updated` field
        """
        return self._update_move_types

    def is_depreciation_nr_required(self):
        """ Defines if a line requires to be numbered """
        self.ensure_one()
        return self.move_type in self.get_numbered_move_types() \
            and not self.partial_dismissal

    def make_name(self):
        self.ensure_one()
        return "{} ({})".format(self.name, self.depreciation_id.make_name())

    def need_normalize_depreciation_nr(self):
        """ Check if numbers need to be normalized """
        dep = self.mapped('depreciation_id')
        dep.ensure_one()

        if dep.force_all_dep_nr:
            return False

        lines = dep.line_ids.filtered('requires_depreciation_nr').sorted()
        if not lines:
            return False

        first_line = lines[0]

        if dep.force_first_dep_nr and dep.first_dep_nr:
            if first_line.depreciation_nr != dep.first_dep_nr:
                return True

        if not dep.force_first_dep_nr:
            if first_line.depreciation_nr != 1:
                return True

        nrs = tuple(lines.mapped('depreciation_nr') or [0])
        if min(nrs) <= 0:
            return True

        expected_nrs = tuple([x for x in range(min(nrs), max(nrs) + 1)])
        if nrs != expected_nrs:
            return True

        return False

    def normalize_depreciation_nr(self, force=False):
        """
        Normalize depreciation numbers to be consecutive for depreciation
        and historical lines within the same depreciation set; force to 0
        every non-depreciation line.
        :param force: force normalization for every depreciations' lines
        """
        for dep in self.mapped('depreciation_id'):

            # Avoid if user chooses to use custom numbers
            if dep.force_all_dep_nr:
                continue

            num_lines = dep.line_ids.filtered('requires_depreciation_nr')
            if force or num_lines.need_normalize_depreciation_nr():
                nr_dict = num_lines.get_depreciation_nr_dict()
                for num_line, nr in nr_dict.items():
                    if num_line.depreciation_nr != nr:
                        num_line.depreciation_nr = nr
            (dep.line_ids - num_lines).update({'depreciation_nr': 0})

    ##########################################################################
    #                                                                        #
    #                      ACCOUNT MOVE CREATING METHODS                     #
    #                                                                        #
    ##########################################################################

    @api.multi
    def button_generate_account_move(self):
        self.generate_account_move()

    @api.multi
    def button_regenerate_account_move(self):
        self.button_remove_account_move()
        self.generate_account_move()

    @api.multi
    def button_remove_account_move(self):
        self.mapped('move_id').unlink()

    def generate_account_move(self):
        for line in self.filtered(lambda l: l.needs_account_move()):
            line.generate_account_move_single()

    def generate_account_move_single(self):
        self.ensure_one()
        am_obj = self.env['account.move']

        vals = self.get_account_move_vals()
        if 'line_ids' not in vals:
            vals['line_ids'] = []

        line_vals = self.get_account_move_line_vals()
        for v in line_vals:
            vals['line_ids'].append((0, 0, v))

        self.move_id = am_obj.create(vals)

    def get_account_move_vals(self):
        self.ensure_one()
        return {
            'company_id': self.company_id.id,
            'date': self.date,
            'journal_id': self.asset_id.category_id.journal_id.id,
            'line_ids': [],
            'ref': _("Asset: ") + self.asset_id.make_name(),
        }

    def get_account_move_line_vals(self):
        """ Switcher between methods """
        method = self.get_account_move_line_vals_methods().get(self.move_type)
        if not method:
            raise NotImplementedError(
                _("Cannot create account move lines: no method is specified.")
            )

        return method()

    def get_account_move_line_vals_methods(self):
        """
        Maps line `move_type` to its own method for generating move lines.
        """
        return {
            t: getattr(self, 'get_{}_account_move_line_vals'.format(t), False)
            for t in dict(self._fields['move_type'].selection).keys()
        }

    def get_depreciated_account_move_line_vals(self):
        self.ensure_one()

        # Asset depreciation
        if not self.partial_dismissal:
            credit_account_id = self.asset_id.category_id.fund_account_id.id
            debit_account_id = self.asset_id.category_id \
                .depreciation_account_id.id

        # Asset partial dismissal
        else:
            debit_account_id = self.asset_id.category_id.fund_account_id.id
            credit_account_id = self.asset_id.category_id\
                .asset_account_id.id

        amt = abs(self.amount)
        credit_line_vals = {
            'account_id': credit_account_id,
            'credit': amt,
            'debit': 0.0,
            'currency_id': self.currency_id.id,
            'name': " - ".join((self.asset_id.make_name(), self.name)),
        }
        debit_line_vals = {
            'account_id': debit_account_id,
            'credit': 0.0,
            'debit': amt,
            'currency_id': self.currency_id.id,
            'name': " - ".join((self.asset_id.make_name(), self.name)),
        }
        return [credit_line_vals, debit_line_vals]

    def get_gain_account_move_line_vals(self):
        self.ensure_one()
        credit_line_vals = {
            'account_id': self.asset_id.category_id.gain_account_id.id,
            'credit': self.amount,
            'debit': 0.0,
            'currency_id': self.currency_id.id,
            'name': " - ".join((self.asset_id.make_name(), self.name)),
        }
        debit_line_vals = {
            'account_id': self.asset_id.category_id.asset_account_id.id,
            'credit': 0.0,
            'debit': self.amount,
            'currency_id': self.currency_id.id,
            'name': " - ".join((self.asset_id.make_name(), self.name)),
        }
        return [credit_line_vals, debit_line_vals]

    def get_historical_account_move_line_vals(self):
        raise NotImplementedError(
            _("Cannot create account move lines for lines of type"
              " `Historical`")
        )

    def get_in_account_move_line_vals(self):
        raise NotImplementedError(
            _("Cannot create account move lines for lines of type `In`")
        )

    def get_loss_account_move_line_vals(self):
        self.ensure_one()
        credit_line_vals = {
            'account_id': self.asset_id.category_id.asset_account_id.id,
            'credit': self.amount,
            'debit': 0.0,
            'currency_id': self.currency_id.id,
            'name': " - ".join((self.asset_id.make_name(), self.name)),
        }
        debit_line_vals = {
            'account_id': self.asset_id.category_id.loss_account_id.id,
            'credit': 0.0,
            'debit': self.amount,
            'currency_id': self.currency_id.id,
            'name': " - ".join((self.asset_id.make_name(), self.name)),
        }
        return [credit_line_vals, debit_line_vals]

    def get_out_account_move_line_vals(self):
        raise NotImplementedError(
            _("Cannot create account move lines for lines of type `Out`")
        )

    def needs_account_move(self):
        self.ensure_one()
        return self.requires_account_move and not self.move_id and self.amount

    def post_dismiss_asset(self):
        dep = self.mapped('depreciation_id')
        dep.ensure_one()
        types = ('gain', 'loss')
        gain_or_loss = self.filtered(
            lambda l: l.needs_account_move() and l.move_type in types
        )
        if gain_or_loss:
            gain_or_loss.generate_account_move_single()
            dep.generate_dismiss_account_move()

    def post_partial_dismiss_asset(self):
        dep = self.mapped('depreciation_id')
        dep.ensure_one()
        types = ('depreciated', 'gain', 'loss')
        to_create_move = self.filtered(
            lambda l: l.needs_account_move() and l.move_type in types
        )
        if to_create_move:
            to_create_move.generate_account_move()
