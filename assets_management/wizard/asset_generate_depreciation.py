# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


class WizardAssetsGenerateDepreciations(models.TransientModel):
    _name = 'wizard.asset.generate.depreciation'
    _description = "Generate Asset Depreciations"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    @api.model
    def get_default_date_dep(self):
        fiscal_year = self.env['account.fiscal.year'].get_fiscal_year_by_date(
            fields.Date.today(),
            company=self.env.user.company_id,
            miss_raise=False
        )
        if fiscal_year:
            return fiscal_year.date_to
        return fields.Date.today()

    @api.model
    def get_default_type_ids(self):
        return [(6, 0, self.env['asset.depreciation.type'].search([]).ids)]

    asset_ids = fields.Many2many(
        'asset.asset',
        string="Assets",
    )

    category_ids = fields.Many2many(
        'asset.category',
        string="Categories",
    )

    company_id = fields.Many2one(
        'res.company',
        default=get_default_company_id,
        string="Company",
    )

    date_dep = fields.Date(
        default=get_default_date_dep,
        required=True,
        string="Depreciation Date",
    )

    type_ids = fields.Many2many(
        'asset.depreciation.type',
        default=get_default_type_ids,
        required=True,
        string="Depreciation Types"
    )

    final = fields.Boolean(
        string='Final',
        default=False,
    )

    @api.multi
    def do_generate(self):
        """
        Launches the generation of new depreciation lines for the retrieved
        assets.
        Reloads the current window if necessary.
        """
        self.ensure_one()

        # Add depreciation date in context just in case
        deps = self.get_depreciations().with_context(dep_date=self.date_dep,
                                                     final=self.final)
        for dep in deps:
            # no depreciation
            if dep.state == 'non_depreciated':
                continue

            # already closed
            if dep.state == 'totally_depreciated':
                raise UserError(
                    'Non si può effettuare l\'ammortamento {} poichè il bene '
                    'risulta già ammortizzato '.format(dep.display_name)
                )

            # existenz of lines beyond
            lines = dep.line_ids
            # final is True
            confirmed_lines = lines.filtered(
                lambda l: l.move_type == 'depreciated' and not
                l.partial_dismissal and l.date >= self.date_dep
                and l.final is True
            )

            if confirmed_lines:
                raise UserError(
                    'Non si può effettuare l\'ammortamento del bene '
                    'poichè per {} esistono ammortamenti consolidati alla '
                    'data impostata '
                    .format(dep.display_name)
                )
            else:
                newer_lines = lines.filtered(
                    lambda l: l.move_type == 'depreciated' and not
                    l.partial_dismissal and l.date >= self.date_dep
                )

                if newer_lines:
                    newer_lines.button_remove_account_move()
                    newer_lines.unlink()
            # end if

        dep_lines = deps.generate_depreciation_lines(self.date_dep)
        deps.post_generate_depreciation_lines(dep_lines)
        if self._context.get('reload_window'):
            return {
                'type': 'ir.actions.client',
                'tag': 'reload'
            }

    def get_depreciations(self):
        self.ensure_one()
        domain = self.get_depreciations_domain()
        return self.env['asset.depreciation'].search(domain)

    def get_depreciations_domain(self):
        domain = [
            ('amount_residual', '>', 0),
            ('date_start', '!=', False),
            ('date_start', '<', self.date_dep),
            ('type_id', 'in', self.type_ids.ids),
        ]
        if self.asset_ids:
            domain += [('asset_id', 'in', self.asset_ids.ids)]
        if self.category_ids:
            domain += [('asset_id.category_id', 'in', self.category_ids.ids)]
        if self.company_id:
            domain += [('company_id', '=', self.company_id.id)]
        return domain

    @api.multi
    def do_warning(self):
        self.ensure_one()
        wizard = self

        if self.final:
            lines = list()
            # mapping  warnings
            # default
            lines.append((0, 0, {
                'reason': 'Attenzione: l\'operazione è irreversibile!'}))

            year = datetime.date.today().year
            end_year = datetime.date(year, 12, 31)

            # check date
            if self.date_dep < end_year:
                lines.append((0, 0, {
                    'reason': 'Attenzione: la data inserita per l\'ammortamento'
                              ' è fuori esercizio (inferiore a quella '
                              'dell\'anno in corso).'}))

            if self.date_dep > end_year:
                lines.append((0, 0, {
                    'reason': 'Attenzione: la data inserita per l\'ammortamento'
                              ' è fuori esercizio (superiore a quella '
                              'dell\'anno in corso).'}))

            wz_id = self.env['asset.generate.warning'].create({
                'wizard_id': wizard.id,
                'reason_lines': lines,
            })

            model = 'assets_management'
            wiz_view = self.env.ref(
                model + '.asset_generate_warning'
            )
            return {
                'type': 'ir.actions.act_window',
                'name': 'Richiesta conferma',
                'res_model': 'asset.generate.warning',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': wiz_view.id,
                'target': 'new',
                'res_id': wz_id.id,
                'context': {'active_id': wizard},
            }

        self.do_generate()

