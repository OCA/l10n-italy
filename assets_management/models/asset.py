# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Asset(models.Model):
    _name = 'asset.asset'
    _description = "Assets"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'purchase_date desc, name asc'

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    asset_accounting_info_ids = fields.One2many(
        'asset.accounting.info',
        'asset_id',
        string="Accounting Info"
    )

    category_id = fields.Many2one(
        'asset.category',
        required=True,
        string="Category",
    )

    code = fields.Char(
        default="",
        string="Code",
    )

    company_id = fields.Many2one(
        'res.company',
        default=get_default_company_id,
        required=True,
        string="Company",
        track_visibility='onchange',
    )

    currency_id = fields.Many2one(
        'res.currency',
        required=True,
        string="Currency",
    )

    customer_id = fields.Many2one(
        'res.partner',
        string="Customer"
    )

    depreciation_ids = fields.One2many(
        'asset.depreciation',
        'asset_id',
        string="Depreciations",
    )

    name = fields.Char(
        required=True,
        string="Name",
        track_visibility='onchange',
    )

    purchase_amount = fields.Monetary(
        string="Purchase Value",
        track_visibility='onchange',
    )

    purchase_date = fields.Date(
        default=fields.Date.today(),
        string="Purchase Date",
        track_visibility='onchange',
    )

    purchase_invoice_id = fields.Many2one(
        'account.invoice',
        string="Purchase Invoice"
    )

    purchase_move_id = fields.Many2one(
        'account.move',
        string="Purchase Move"
    )

    sale_amount = fields.Monetary(
        string="Sale Value",
    )

    sale_date = fields.Date(
        string="Sale Date"
    )

    sale_invoice_id = fields.Many2one(
        'account.invoice',
        string="Sale Invoice"
    )

    sale_move_id = fields.Many2one(
        'account.move',
        string="Sale Move"
    )

    sold = fields.Boolean(
        string="Sold"
    )

    state = fields.Selection(
        [('non_depreciated', "Non Depreciated"),
         ('partially_depreciated', "Partially Depreciated"),
         ('totally_depreciated', "Depreciated")],
        compute='_compute_state',
        default='non_depreciated',
        store=True,
        string="State"
    )

    supplier_id = fields.Many2one(
        'res.partner',
        string="Supplier"
    )

    supplier_ref = fields.Char(
        string="Supplier Ref."
    )

    used = fields.Boolean(
        string="Used",
    )

    @api.model
    def create(self, vals):
        # Add depreciation if it's missing while category is set
        create_deps_from_categ = False
        if vals.get('category_id') and not vals.get('depreciation_ids'):
            create_deps_from_categ = True
        if vals.get('code'):
            vals['code'] = ' '.join(vals.get('code').split())
        asset = super().create(vals)
        if create_deps_from_categ:
            asset.onchange_category_id()
        return asset

    @api.multi
    def write(self, vals):
        if vals.get('code'):
            vals['code'] = ' '.join(vals.get('code').split())
        return super().write(vals)

    @api.multi
    def unlink(self):
        if self.mapped('asset_accounting_info_ids'):
            assets = self.filtered('asset_accounting_info_ids')
            name_list = "\n".join([a[-1] for a in assets.name_get()])
            raise ValidationError(
                _("The assets you are trying to delete are currently linked"
                  " to accounting info. Please remove them if necessary"
                  " before removing these assets:\n") + name_list
            )
        self.mapped('depreciation_ids').unlink()
        return super().unlink()

    @api.multi
    def name_get(self):
        return [(asset.id, asset.make_name()) for asset in self]

    @api.constrains('company_id')
    def check_company(self):
        for asset in self:
            comp = asset.get_linked_aa_info_records().mapped('company_id')
            if len(comp) > 1 or (comp and comp != asset.company_id):
                raise ValidationError(
                    _("`{}`: cannot change asset's company once it's already"
                      " related to accounting info.")
                    .format(asset.make_name())
                )

    @api.multi
    @api.depends('depreciation_ids', 'depreciation_ids.state')
    def _compute_state(self):
        for asset in self:
            asset.state = asset.get_asset_state()

    @api.onchange('category_id')
    def onchange_category_id(self):
        # Do not allow category changes if any depreciation line is already
        # linked to an account move
        if any(self.depreciation_ids.mapped('line_ids.move_id')):
            raise ValidationError(
                _("Cannot change category for an asset that's already been"
                  " depreciated.")
            )

        if self.category_id:

            # Remove depreciation lines
            self.depreciation_ids = False

            # Set new lines
            vals = self.category_id.get_depreciation_vals(self.purchase_amount)
            self.depreciation_ids = [(0, 0, v) for v in vals]
            self.onchange_purchase_amount()
            self.onchange_purchase_date()

    @api.onchange('company_id')
    def onchange_company_currency(self):
        if self.company_id:
            self.currency_id = self.company_id.currency_id

    @api.onchange('purchase_amount')
    def onchange_purchase_amount(self):
        if self.purchase_amount:
            for dep in self.depreciation_ids:
                dep.amount_depreciable = self.purchase_amount * dep.base_coeff
            if self.depreciation_ids.mapped('line_ids').filtered(
                lambda l: l.move_type == 'depreciated'
            ):
                title = _("Warning!")
                msg = _(
                    "Current asset has already been depreciated. Changes upon"
                    " its purchase value will not be automatically reflected"
                    " upon depreciation lines, which will have to be updated"
                    " manually."
                )
                return {'warning': {'title': title, 'message': msg}}

    @api.onchange('purchase_date')
    def onchange_purchase_date(self):
        if self.purchase_date:
            for dep in self.depreciation_ids:
                dep.date_start = self.purchase_date

    @api.multi
    def launch_wizard_generate_depreciations(self):
        self.ensure_one()
        xmlid = 'assets_management.action_wizard_asset_generate_depreciation'
        [act] = self.env.ref(xmlid).read()
        ctx = dict(self._context)
        ctx.update({
            'default_asset_ids': [(6, 0, self.ids)],
            'default_category_ids': [(6, 0, self.category_id.ids)],
            'default_company_id': self.company_id.id,
            'default_date': fields.Date.today(),
            'default_type_ids': [
                (6, 0, self.depreciation_ids.mapped('type_id').ids)
            ],
        })
        act['context'] = ctx
        return act

    def get_asset_state(self):
        self.ensure_one()
        if not self.depreciation_ids:
            return 'non_depreciated'

        states = tuple(set(self.depreciation_ids.mapped('state')))

        if not states:
            return 'non_depreciated'
        elif len(states) == 1:
            return states[0]
        else:
            return 'partially_depreciated'

    def get_linked_aa_info_records(self):
        self.ensure_one()
        return self.env['asset.accounting.info'].search([
            '|',
            ('asset_id', '=', self.id),
            ('dep_line_id.asset_id', '=', self.id),
        ])

    def make_name(self):
        self.ensure_one()
        name = self.name.strip()
        if self.code:
            return "[{}] {}".format(self.code.strip(), name)
        return name
