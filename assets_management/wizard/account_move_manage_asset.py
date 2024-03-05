# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# Copyright 2024 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class WizardAccountMoveManageAsset(models.TransientModel):
    _name = "wizard.account.move.manage.asset"
    _description = "Manage Assets from Account Moves"
    _check_company_auto = True

    @api.model
    def get_default_company_id(self):
        return self.env.company

    @api.model
    def get_default_move_ids(self):
        return self._context.get("move_ids")

    asset_id = fields.Many2one(
        "asset.asset",
        string="Asset",
        check_company=True,
    )

    asset_purchase_amount = fields.Monetary(string="Purchase Amount")

    category_id = fields.Many2one(
        "asset.category",
        string="Category",
        check_company=True,
    )

    code = fields.Char(
        default="",
        string="Code",
    )

    company_id = fields.Many2one(
        "res.company",
        readonly=True,
        default=get_default_company_id,
        string="Company",
    )

    currency_id = fields.Many2one(
        "res.currency",
        readonly=True,
        related="company_id.currency_id",
        string="Currency",
    )

    depreciated_fund_amount = fields.Monetary(string="Depreciated Fund Amount")

    depreciation_type_ids = fields.Many2many(
        "asset.depreciation.type",
        string="Depreciation Types",
        check_company=True,
    )

    dismiss_date = fields.Date(
        default=fields.Date.today(),
        string="Dismiss Date",
    )

    is_move_state_ok = fields.Boolean(
        string="Move State",
    )

    dismiss_asset_without_sale = fields.Boolean()

    management_type = fields.Selection(
        [
            ("create", "Create New"),
            ("update", "Update Existing"),
            ("partial_dismiss", "Partial Dismiss"),
            ("dismiss", "Dismiss Asset"),
        ],
        string="Management Type",
    )

    move_ids = fields.Many2many(
        "account.move",
        default=get_default_move_ids,
        string="Moves",
        check_company=True,
    )

    move_line_ids = fields.Many2many(
        "account.move.line",
        string="Move Lines",
        check_company=True,
    )

    move_type = fields.Selection(
        [
            ("sale", "Sale"),
            ("purchase", "Purchase"),
            ("general", "Miscellaneous"),
            ("out_invoice", "Customer Invoice"),
            ("in_invoice", "Vendor Bill"),
            ("out_refund", "Customer Credit Note"),
            ("in_refund", "Vendor Credit Note"),
            ("wrong", "Wrong"),
        ],
        string="Move Type",
    )

    name = fields.Char(
        string="Name",
    )

    purchase_date = fields.Date(
        default=fields.Date.today(),
        string="Purchase Date",
    )

    used = fields.Boolean(
        string="Used",
    )

    # Mapping between move journal type and depreciation line type
    _move_journal_type_2_dep_line_type = {
        "purchase": "in",
        "sale": "out",
        "in_invoice": "in",
        "out_invoice": "out",
        "in_refund": "out",
        "out_refund": "in",
    }

    # Every method used in here must return an asset
    _management_type_2_method = {
        "create": lambda w: w.create_asset(),
        "dismiss": lambda w: w.dismiss_asset(),
        "partial_dismiss": lambda w: w.partial_dismiss_asset(),
        "update": lambda w: w.update_asset(),
    }

    @api.onchange("asset_id", "management_type")
    def onchange_depreciation_type_ids(self):
        if self.management_type == "update":
            if self.asset_id:
                self.depreciation_type_ids = self.asset_id.mapped(
                    "depreciation_ids.type_id"
                )
            else:
                self.depreciation_type_ids = False
        else:
            self.depreciation_type_ids = False
        if self.asset_id:
            self.move_line_ids = self.move_ids.mapped("line_ids").filtered(
                lambda line: not line.asset_accounting_info_ids
                and line.account_id == self.asset_id.category_id.asset_account_id
            )

    @api.onchange("category_id")
    def onchange_category_id(self):
        if self.category_id:
            self.move_line_ids = self.move_ids.mapped("line_ids").filtered(
                lambda line: not line.asset_accounting_info_ids
                and line.account_id == self.category_id.asset_account_id
            )

    @api.onchange("move_ids")
    def onchange_moves(self):
        if self.move_ids:
            moves = self.move_ids
            move_types = set(moves.mapped("journal_id.type"))

            self.is_move_state_ok = all([m.state == "posted" for m in moves])
            self.move_line_ids = moves.mapped("line_ids").filtered(
                lambda line: not line.asset_accounting_info_ids
            )
            move_type = moves[0].move_type

            if any([move.move_type != move_type for move in moves]):
                move_type = "wrong"
            if move_type == "entry":
                move_type = "general"
            self.move_type = move_type

            if move_type in ("in_invoice", "out_refund"):
                self.management_type = "create"
            elif move_type in ("in_refund", "out_invoice"):
                self.management_type = "dismiss"
            else:
                self.management_type = False
            if "purchase" in move_types and "sale" in move_types:
                self.move_type = "wrong"
            elif "purchase" in move_types:
                self.move_type = "purchase"
                self.management_type = "create"
            elif "sale" in move_types:
                self.move_type = "sale"
                self.management_type = "dismiss"
            else:
                self.move_type = "general"
                self.management_type = "update"
        else:
            if self._context.get("remove_asset_without_sale"):
                self.dismiss_asset_without_sale = True
                self.management_type = "dismiss"
                self.asset_id = self._context.get("asset_ids")[0]

    def link_asset(self):
        self.ensure_one()
        self.check_pre_link_asset()

        method = self.get_management_type_2_method().get(self.management_type)
        if not method:
            raise ValidationError(
                _(
                    "Could not determine how to link move lines to asset"
                    " in mode `{}`."
                ).format(self.management_type)
            )
        # As written above: method defined in here must return an asset
        asset = method(self)

        if self._context.get("show_asset"):
            act_xmlid = "assets_management.action_asset"
            act = self.env.ref(act_xmlid).read()[0]
            form_xmlid = "assets_management.asset_form_view"
            form = self.env.ref(form_xmlid)
            act.update(
                {
                    "res_id": asset.id,
                    "view_id": form.id,
                    "view_mode": "form",
                    "view_type": "form",
                    "views": [(form.id, "form")],
                }
            )
            return act

        return asset

    def check_pre_create_asset(self):
        self.ensure_one()
        if not self.move_line_ids:
            raise ValidationError(
                _("At least one move line is mandatory to create a new asset!")
            )

        if not len(self.move_line_ids.mapped("move_id")) == 1:
            raise ValidationError(
                _(
                    "Cannot create asset if move lines come from different"
                    " account moves!"
                )
            )

        if not all(
            [
                line.account_id == self.category_id.asset_account_id
                for line in self.move_line_ids
            ]
        ):
            categ_name = self.category_id.name_get()[0][-1]
            acc_name = self.category_id.asset_account_id.name_get()[0][-1]
            raise ValidationError(
                _(
                    "You need to choose move lines with account `{}`"
                    " if you need them to create an asset for"
                    " category `{}`!"
                ).format(acc_name, categ_name)
            )

    def check_pre_dismiss_asset(self):
        self.ensure_one()
        if not self.asset_id:
            raise ValidationError(_("Please choose an asset before continuing!"))

        if not self.move_line_ids and not self.dismiss_asset_without_sale:
            raise ValidationError(
                _("At least one move line is mandatory to dismiss" " an asset!")
            )

        if (
            not len(self.move_line_ids.mapped("move_id")) == 1
            and not self.dismiss_asset_without_sale
        ):
            raise ValidationError(
                _(
                    "Cannot dismiss asset if move lines come from different"
                    " account moves!"
                )
            )

        if (
            not all(
                [
                    line.account_id == self.asset_id.category_id.asset_account_id
                    for line in self.move_line_ids
                ]
            )
            and not self.dismiss_asset_without_sale
        ):
            ass_name = self.asset_id.make_name()
            ass_acc = self.asset_id.category_id.asset_account_id.name_get()[0][-1]
            raise ValidationError(
                _(
                    "You need to choose move lines with account `{}`"
                    " if you need them to dismiss asset `{}`!"
                ).format(ass_acc, ass_name)
            )

    def check_pre_link_asset(self):
        self.ensure_one()
        if len(self.move_line_ids.mapped("account_id")) > 1:
            raise ValidationError(_("Every move line must share the same account!"))

        if not self.management_type:
            raise ValidationError(_("Couldn't determine which action should be done."))

    def check_pre_update_asset(self):
        self.ensure_one()
        if not self.asset_id:
            raise ValidationError(_("Please choose an asset before continuing!"))

        if not self.depreciation_type_ids:
            raise ValidationError(_("Please choose at least one depreciation type!"))

        if not self.move_line_ids:
            raise ValidationError(
                _("At least one move line is mandatory to update" " an asset!")
            )

        if not all(
            [
                line.account_id == self.asset_id.category_id.asset_account_id
                for line in self.move_line_ids
            ]
        ):
            ass_name = self.asset_id.make_name()
            ass_acc = self.asset_id.category_id.asset_account_id.name_get()[0][-1]
            raise ValidationError(
                _(
                    "You need to choose move lines with account `{}`"
                    " if you need them to update asset `{}`!"
                ).format(ass_acc, ass_name)
            )

    def create_asset(self):
        """Creates asset and returns it"""
        self.ensure_one()
        self.check_pre_create_asset()
        return self.env["asset.asset"].create(self.get_create_asset_vals())

    def dismiss_asset(self):
        """Dismisses asset and returns it"""
        self.ensure_one()
        self.check_pre_dismiss_asset()
        old_dep_lines = self.asset_id.mapped("depreciation_ids.line_ids")
        self.asset_id.write(self.get_dismiss_asset_vals())

        for dep in self.asset_id.depreciation_ids:
            (dep.line_ids - old_dep_lines).with_context(
                {"dismiss_date": self.dismiss_date}
            ).post_dismiss_asset()

        return self.asset_id

    def get_create_asset_vals(self):
        self.ensure_one()
        purchase_amount = self.move_line_ids.get_asset_purchase_amount(
            currency=self.currency_id
        )
        if len(self.move_line_ids.mapped("partner_id")) == 1:
            supplier = self.move_line_ids.mapped("partner_id")
        else:
            raise ValidationError(_("Multiple partners found in move lines!"))
        move = self.move_line_ids.mapped("move_id")
        return {
            "asset_accounting_info_ids": [
                (0, 0, {"move_line_id": line.id, "relation_type": self.management_type})
                for line in self.move_line_ids
            ],
            "category_id": self.category_id.id,
            "code": self.code,
            "company_id": self.company_id.id,
            "currency_id": self.currency_id.id,
            "dismiss_date": False,
            "name": self.name,
            "purchase_amount": purchase_amount,
            "purchase_date": self.purchase_date,
            "purchase_move_id": move.id,
            "supplier_id": supplier.id,
            "supplier_ref": move.payment_reference or move.ref or "",
            "used": self.used,
        }

    def get_dismiss_asset_vals(self):
        self.ensure_one()
        asset = self.asset_id
        currency = self.asset_id.currency_id
        dismiss_date = self.dismiss_date
        digits = self.env["decimal.precision"].precision_get("Account")

        last_depreciation_dates = asset.depreciation_ids.filtered(
            "last_depreciation_date"
        ).mapped("last_depreciation_date")
        if last_depreciation_dates:
            max_date = max(last_depreciation_dates)
            if max_date > dismiss_date:
                raise ValidationError(
                    _(
                        "Cannot dismiss an asset earlier than the last depreciation"
                        " date.\n"
                        "(Dismiss date: {}, last depreciation date: {})."
                    ).format(dismiss_date, max_date)
                )

        if self.dismiss_asset_without_sale:
            move_nums = _("Dismiss Asset without Sale")
            writeoff = 0
            vals = {
                "depreciation_ids": [],
                "sale_amount": writeoff,
                "dismiss_date": self.dismiss_date,
                "dismissed": True,
            }
        else:
            move = self.move_line_ids.mapped("move_id")
            move_nums = move.name

            writeoff = 0
            for line in self.move_line_ids:
                writeoff += line.currency_id._convert(
                    line.credit - line.debit, currency, line.company_id, line.date
                )
            writeoff = round(writeoff, digits)

            vals = {
                "customer_id": move.partner_id.id,
                "depreciation_ids": [],
                "sale_amount": writeoff,
                "sale_date": move.invoice_date or move.date,
                "sale_move_id": move.id,
                "sold": True,
            }
        for dep in asset.depreciation_ids:
            residual = dep.amount_residual
            dep_vals = {"line_ids": []}
            dep_writeoff = writeoff

            if self.dismiss_asset_without_sale and not self.move_line_ids:
                asset_accounting_info_ids = [
                    (
                        0,
                        0,
                        {
                            "relation_type": self.management_type,
                        },
                    )
                ]
                dep_name = _("Direct dismiss")
            else:
                asset_accounting_info_ids = [
                    (
                        0,
                        0,
                        {
                            "move_line_id": line.id,
                            "relation_type": self.management_type,
                        },
                    )
                    for line in self.move_line_ids
                ]
                dep_name = _("From move(s) ") + move_nums
            dep_line_vals = {
                "asset_accounting_info_ids": asset_accounting_info_ids,
                "amount": min(residual, dep_writeoff),
                "date": dismiss_date,
                "move_type": "out",
                "name": dep_name,
            }
            dep_vals["line_ids"].append((0, 0, dep_line_vals))

            balance = dep_writeoff - residual
            if not float_is_zero(balance, digits):
                balance = round(balance, digits)
                move_type = "gain" if balance > 0 else "loss"
                dep_balance_vals = {
                    "asset_accounting_info_ids": [
                        (
                            0,
                            0,
                            {
                                "move_line_id": line.id,
                                "relation_type": self.management_type,
                            },
                        )
                        for line in self.move_line_ids
                    ],
                    "amount": abs(balance),
                    "date": dismiss_date,
                    "move_type": move_type,
                    "name": _("From move(s) ") + move_nums,
                }
                dep_vals["line_ids"].append((0, 0, dep_balance_vals))

            vals["depreciation_ids"].append((1, dep.id, dep_vals))

        return vals

    def get_move_journal_type_2_dep_line_type(self):
        self.ensure_one()
        return self._move_journal_type_2_dep_line_type

    def get_management_type_2_method(self):
        self.ensure_one()
        return self._management_type_2_method

    def get_partial_dismiss_asset_vals(self):
        self.ensure_one()
        asset = self.asset_id
        currency = self.asset_id.currency_id
        dismiss_date = self.dismiss_date
        digits = self.env["decimal.precision"].precision_get("Account")
        fund_amt = self.depreciated_fund_amount
        purchase_amt = self.asset_purchase_amount

        last_depreciation_dates = asset.depreciation_ids.filtered(
            "last_depreciation_date"
        ).mapped("last_depreciation_date")
        if last_depreciation_dates:
            max_date = max(last_depreciation_dates)
            if max_date > dismiss_date:
                raise ValidationError(
                    _(
                        "Cannot dismiss an asset earlier than the last depreciation"
                        " date.\n"
                        "(Dismiss date: {}, last depreciation date: {})."
                    ).format(dismiss_date, max_date)
                )

        move = self.move_line_ids.mapped("move_id")
        move_nums = move.name

        writeoff = 0
        for line in self.move_line_ids:
            writeoff += line.currency_id._convert(
                line.credit - line.debit, currency, line.company_id, line.date
            )
        writeoff = round(writeoff, digits)

        vals = {"depreciation_ids": []}
        for dep in asset.depreciation_ids:
            if dep.pro_rata_temporis:
                dep_writeoff = writeoff * dep.get_pro_rata_temporis_multiplier(
                    dismiss_date, "std"
                )
            else:
                dep_writeoff = writeoff

            name = _("Partial dismissal from move(s) {}").format(move_nums)

            out_line_vals = {
                "asset_accounting_info_ids": [
                    (
                        0,
                        0,
                        {
                            "move_line_id": line.id,
                            "relation_type": self.management_type,
                        },
                    )
                    for line in self.move_line_ids
                ],
                "amount": purchase_amt,
                "date": dismiss_date,
                "move_type": "out",
                "name": name,
                "partial_dismissal": True,
            }
            dep_line_vals = {
                "asset_accounting_info_ids": [
                    (
                        0,
                        0,
                        {
                            "move_line_id": line.id,
                            "relation_type": self.management_type,
                        },
                    )
                    for line in self.move_line_ids
                ],
                "amount": -fund_amt,
                "date": dismiss_date,
                "move_type": "depreciated",
                "name": name,
                "partial_dismissal": True,
            }

            dep_vals = {"line_ids": [(0, 0, out_line_vals), (0, 0, dep_line_vals)]}

            balance = (fund_amt + dep_writeoff) - purchase_amt
            if not float_is_zero(balance, digits):
                loss_gain_vals = {
                    "asset_accounting_info_ids": [
                        (
                            0,
                            0,
                            {
                                "move_line_id": line.id,
                                "relation_type": self.management_type,
                            },
                        )
                        for line in self.move_line_ids
                    ],
                    "amount": abs(balance),
                    "date": dismiss_date,
                    "move_type": "gain" if balance > 0 else "loss",
                    "name": name,
                    "partial_dismissal": True,
                }
                dep_vals["line_ids"].append((0, 0, loss_gain_vals))

            vals["depreciation_ids"].append((1, dep.id, dep_vals))

        return vals

    def get_update_asset_vals(self):
        self.ensure_one()
        asset = self.asset_id
        asset_name = asset.make_name()
        digits = self.env["decimal.precision"].precision_get("Account")

        grouped_move_lines = {}
        for line in self.move_line_ids:
            move = line.move_id
            if move not in grouped_move_lines:
                grouped_move_lines[move] = self.env["account.move.line"]
            grouped_move_lines[move] |= line

        vals = {"depreciation_ids": []}
        for dep in asset.depreciation_ids.filtered(
            lambda d: d.type_id in self.depreciation_type_ids
        ):
            residual = dep.amount_residual
            balances = 0

            dep_vals = {"line_ids": []}
            for move, lines in grouped_move_lines.items():
                move_num = move.name

                # Compute amount and sign to preview how much the line
                # balance will be: if it's going to write off the
                # whole residual amount and more, making it become lower
                # than zero, raise error
                # todo probabilmente si può evitare questo calcolo
                amount = 0
                if lines:
                    amount = sum(
                        line.currency_id._convert(
                            line.debit - line.credit,
                            dep.currency_id,
                            line.company_id,
                            line.date,
                        )
                        for line in lines
                    )
                sign = 1 if float_compare(amount, 0, digits) > 0 else -1
                # Block updates if the amount to be written off is higher than
                # the residual amount
                if sign < 0 and float_compare(residual, abs(amount), digits) < 0:
                    raise ValidationError(
                        _(
                            "Could not update `{}`: not enough residual amount"
                            " to write off move `{}`.\n"
                            "(Amount to write off: {}; residual amount: {}.)\n"
                            "Maybe you should try to dismiss this asset"
                            " instead?"
                        ).format(asset_name, move_num, -amount, residual)
                    )
                balances += amount
                # end todo

                dep_type = "in" if sign > 0 else "out"
                dep_line_vals = {
                    "asset_accounting_info_ids": [
                        (
                            0,
                            0,
                            {
                                "move_line_id": line.id,
                                "relation_type": self.management_type,
                            },
                        )
                        for line in lines
                    ],
                    "amount": abs(amount),
                    "date": move.date,
                    "move_type": dep_type,
                    "name": _("From move(s) ") + move_num,
                }
                dep_vals["line_ids"].append((0, 0, dep_line_vals))

            if balances < 0 and residual + balances < 0:
                raise ValidationError(
                    _(
                        "Could not update `{}`: not enough residual amount to"
                        " write off.\n"
                        "(Amount to write off: {}; residual amount: {}.)\n"
                        "Maybe you should try to dismiss this asset instead?"
                    ).format(asset_name, balances, residual)
                )

            vals["depreciation_ids"].append((1, dep.id, dep_vals))

        return vals

    def partial_dismiss_asset(self):
        """Dismisses asset partially and returns it"""
        self.ensure_one()
        self.check_pre_dismiss_asset()
        old_dep_lines = self.asset_id.mapped("depreciation_ids.line_ids")
        self.asset_id.write(self.get_partial_dismiss_asset_vals())

        for dep in self.asset_id.depreciation_ids:
            (dep.line_ids - old_dep_lines).post_partial_dismiss_asset()

        return self.asset_id

    def update_asset(self):
        """Updates asset and returns it"""
        self.ensure_one()
        self.check_pre_update_asset()
        self.asset_id.write(self.get_update_asset_vals())
        return self.asset_id
