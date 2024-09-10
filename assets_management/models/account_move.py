# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    asset_accounting_info_ids = fields.One2many(
        "asset.accounting.info", "move_id", string="Assets Accounting Info"
    )

    asset_ids = fields.Many2many(
        "asset.asset", compute="_compute_asset_data", store=True, string="Assets"
    )

    dep_line_ids = fields.Many2many(
        "asset.depreciation.line",
        compute="_compute_asset_data",
        store=True,
        string="Depreciation Lines",
    )

    hide_link_asset_button = fields.Boolean(
        compute="_compute_hide_link_asset_button",
        compute_sudo=True,
        default=True,
        string="Hide Asset Button",
    )

    @api.constrains("company_id")
    def check_company(self):
        for move in self:
            comp = move.get_linked_aa_info_records().mapped("company_id")
            if len(comp) > 1 or (comp and comp != move.company_id):
                raise ValidationError(
                    _(
                        "`{}`: cannot change move's company once it's already"
                        " related to an asset."
                    ).format(move.name_get()[0][-1])
                )

    def button_cancel(self):
        res = super().button_cancel()
        if self:
            # Remove every a.a.info related to current moves, and delete
            # related depreciation lines
            aa_infos = self.mapped(lambda m: m.get_linked_aa_info_records())
            dep_lines = aa_infos.mapped("dep_line_id")
            aa_infos.unlink()
            # Filtering needed: cannot delete dep lines with a.a.info
            dep_lines.filtered(lambda l: not l.asset_accounting_info_ids).unlink()
        return res

    @api.depends(
        "asset_accounting_info_ids",
        "asset_accounting_info_ids.asset_id",
        "asset_accounting_info_ids.dep_line_id",
    )
    def _compute_asset_data(self):
        for move in self:
            aa_info = move.get_linked_aa_info_records()
            assets = aa_info.mapped("asset_id")
            dep_lines = aa_info.mapped("dep_line_id")
            if dep_lines:
                assets += dep_lines.mapped("asset_id")
            move.update(
                {
                    "asset_ids": [(6, 0, assets.ids)],
                    "dep_line_ids": [(6, 0, dep_lines.ids)],
                }
            )

    def _compute_hide_link_asset_button(self):
        valid_account_ids = self.get_valid_accounts()
        if not valid_account_ids:
            self.update({"hide_link_asset_button": True})
        else:
            for move in self:
                move.hide_link_asset_button = (
                    not any(
                        [
                            line.account_id.id in valid_account_ids.ids
                            for line in move.invoice_line_ids
                        ]
                    )
                    or move.state != "posted"
                )

    def open_wizard_manage_asset(self):
        self.ensure_one()
        # do not use invoice_line_ids as it will ignore possible extra lines for not
        # deductible VAT
        lines = self.line_ids.filtered(lambda line: not line.asset_accounting_info_ids)
        if not lines:
            raise ValidationError(_("Every line is already linked to an asset."))

        xmlid = "assets_management.action_wizard_account_move_manage_asset"
        act = self.env["ir.actions.act_window"]._for_xml_id(xmlid)
        ctx = dict(self._context)
        ctx.update(
            {
                "default_company_id": self.company_id.id,
                "default_dismiss_date": self.invoice_date or self.invoice_date_due,
                "default_move_ids": [(6, 0, self.ids)],
                "default_move_line_ids": [(6, 0, lines.ids)],
                "default_purchase_date": self.invoice_date or self.invoice_date_due,
                "move_ids": self.ids,
            }
        )
        act.update({"context": ctx})
        return act

    def get_linked_aa_info_records(self):
        self.ensure_one()
        return self.env["asset.accounting.info"].search(
            [
                "|",
                ("move_id", "=", self.id),
                ("move_line_id.move_id", "=", self.id),
            ]
        )

    def get_valid_accounts(self):
        return self.env["asset.category"].search([]).mapped("asset_account_id")
