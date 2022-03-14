# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WizardAssetsGenerateDepreciations(models.TransientModel):
    _name = "wizard.asset.generate.depreciation"
    _description = "Generate Asset Depreciations"

    @api.model
    def get_default_company_id(self):
        return self.env.user.company_id

    @api.model
    def get_default_date_dep(self):
        query = (
            "SELECT MAX(date) FROM asset_depreciation_line WHERE "
            "final='true' and move_type = 'depreciated'"
        )
        self._cr.execute(query)
        date = self._cr.fetchone()
        # has depreciation
        if date[0]:
            last_date = date[0]
            last_date += datetime.timedelta(days=1)
        else:
            last_date = fields.Date.today()
        # end if

        # search for end of fiscal year if is set according
        # with the year of last date
        fiscal_year = self.env["account.fiscal.year"].get_fiscal_year_by_date(
            last_date, company=self.env.user.company_id, miss_raise=False
        )
        if fiscal_year:
            return fiscal_year.date_to
        # end if

        return fields.Date.today()

    @api.model
    def get_default_type_ids(self):
        return [(6, 0, self.env["asset.depreciation.type"].search([]).ids)]

    @api.depends("asset_ids")
    def _compute_asset_ids(self):
        for r in self:
            r.has_asset_ids = len(r.asset_ids) > 0
        # end for

    asset_ids = fields.Many2many(
        "asset.asset",
        string="Assets",
    )

    category_ids = fields.Many2many(
        "asset.category",
        string="Categories",
    )

    company_id = fields.Many2one(
        "res.company",
        default=get_default_company_id,
        string="Company",
    )

    date_dep = fields.Date(
        default=get_default_date_dep,
        required=True,
        string="Depreciation Date",
    )

    type_ids = fields.Many2many(
        "asset.depreciation.type",
        default=get_default_type_ids,
        required=True,
        string="Depreciation Types",
    )

    final = fields.Boolean(
        string="Final",
        default=False,
    )

    has_asset_ids = fields.Boolean(string="Has asset ids", compute="_compute_asset_ids")

    def do_generate(self):
        """
        Launches the generation of new depreciation lines for the retrieved
        assets.
        Reloads the current window if necessary.
        """
        self.ensure_one()

        # assets
        # assets = list()
        # Add depreciation date in context just in case
        deps = self.get_depreciations().with_context(
            dep_date=self.date_dep, final=self.final
        )
        for dep in deps:
            # no depreciation
            # if dep.asset_id not in assets:
            #     assets.append(dep.asset_id)
            # # end if

            # already closed
            if dep.state == "totally_depreciated":
                raise UserError(
                    _(
                        "Non si può effettuare l'ammortamento {} poichè il bene "
                        "risulta già ammortizzato ".format(dep.display_name)
                    )
                )

            # existenz of lines beyond
            lines = dep.line_ids

            # not depreciated type
            extra = lines.filtered(
                lambda line: line.move_type != "depreciated" and line.final is False
            )

            # start
            year = self.date_dep.year
            start_year = datetime.date(year, 1, 1)
            datetime.date(year, 12, 31)

            # final is True
            confirmed_lines = lines.filtered(
                lambda l: l.move_type == "depreciated"
                and not l.partial_dismissal
                and start_year <= l.date <= self.date_dep
                and l.final is True
            )

            if confirmed_lines:
                raise UserError(
                    _(
                        "Non si può effettuare l'ammortamento del bene "
                        "poichè per {} esistono ammortamenti consolidati entro la "
                        "data impostata ".format(dep.display_name)
                    )
                )
            else:
                newer_lines = lines.filtered(
                    lambda l: l.move_type == "depreciated"
                    and not l.partial_dismissal
                    and start_year <= l.date
                    and l.final is False
                )

                if newer_lines:
                    newer_lines.button_remove_account_move()
                    newer_lines.unlink()
            # end if

            if extra and self.final:
                for ln in extra:
                    if ln.move_id and ln.move_id.state == "draft":
                        ln.move_id.post()
                        ln.final = True
                    # end if
                # end for
            # end if

        dep_lines = deps.generate_depreciation_lines(self.date_dep)
        deps.post_generate_depreciation_lines(dep_lines)

        # for asset in assets:
        #     asset.compute_last_depreciation_date()
        # # end if

        # if self._context.get('reload_window'):
        return {"type": "ir.actions.client", "tag": "reload"}

    def get_depreciations(self):
        self.ensure_one()
        domain = self.get_depreciations_domain()
        return self.env["asset.depreciation"].search(domain)

    def get_depreciations_domain(self):
        domain = [
            ("amount_residual", ">", 0),
            ("date_start", "!=", False),
            ("date_start", "<", self.date_dep),
            ("type_id", "in", self.type_ids.ids),
        ]
        if self.asset_ids:
            domain += [("asset_id", "in", self.asset_ids.ids)]
        if self.category_ids:
            domain += [("asset_id.category_id", "in", self.category_ids.ids)]
        if self.company_id:
            domain += [("company_id", "=", self.company_id.id)]
        return domain

    def do_warning(self):
        self.ensure_one()
        wizard = self

        if self.final:
            lines = list()
            # mapping  warnings
            # default
            lines.append(
                (0, 0, {"reason": "ATTENZIONE: l'operazione è irreversibile!"})
            )

            datetime.date.today().year
            year = self.date_dep.year
            end_year = datetime.date(year, 12, 31)
            current_date_str = self.date_dep.strftime("%d-%m-%Y")
            end_year_str = end_year.strftime("%d-%m-%Y")

            # check date
            if self.date_dep < end_year:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "reason": "ATTENZIONE: la data inserita per "
                            "l'ammortamento {curr}"
                            " è fuori esercizio (inferiore a quella usuale "
                            "per l'anno indicato {endy} ).".format(
                                curr=current_date_str, endy=end_year_str
                            )
                        },
                    )
                )

            if self.date_dep > end_year:
                lines.append(
                    (
                        0,
                        0,
                        {
                            "reason": "ATTENZIONE: la data inserita per l'ammortamento"
                            " {curr} è fuori esercizio (superiore a quella "
                            "usuale per l'anno indicato {endy}).".format(
                                curr=current_date_str, endy=end_year_str
                            )
                        },
                    )
                )

            # get assets
            deps = self.get_depreciations().with_context(
                dep_date=self.date_dep, final=self.final
            )
            for dep in deps:
                extra = dep.line_ids.filtered(
                    lambda l: l.move_type != "depreciated" and l.final is False
                )
                if extra:
                    for ln in extra:
                        tipo = ln.depreciation_line_type_id.display_name
                        asset = ln.depreciation_id.display_name
                        lines.append(
                            (
                                0,
                                0,
                                {
                                    "reason": 'ATTENZIONE: il movimento "{movimento}" '
                                    'di tipo {tipo} per il bene "{asset}" '
                                    "risulta non consolidato".format(
                                        movimento=ln.name, asset=asset, tipo=tipo
                                    )
                                },
                            )
                        )

            wz_id = self.env["asset.generate.warning"].create(
                {
                    "wizard_id": wizard.id,
                    "reason_lines": lines,
                }
            )

            model = "assets_management"
            wiz_view = self.env.ref(model + ".asset_generate_warning")

            model = "assets_management"
            wiz_view = self.env.ref(model + ".asset_generate_warning")
            return {
                "type": "ir.actions.act_window",
                "name": "Richiesta conferma",
                "res_model": "asset.generate.warning",
                "view_type": "form",
                "view_mode": "form",
                "view_id": wiz_view.id,
                "target": "new",
                "res_id": wz_id.id,
                "context": {"active_id": wizard},
            }

        if self._context.get("depreciated"):
            return self.do_generate().with_context(depreciated=True)
        else:
            return self.do_generate()
