# Author(s): Silvio Gregorini (silviogregorini@openforce.it)
# Copyright 2019 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from collections import OrderedDict

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.misc import format_amount


def format_date(rec, field_name, fmt):
    """Formats record's field value according to given format `fmt`"""
    if not rec[field_name]:
        return ""
    return rec._fields[field_name].from_string(rec[field_name]).strftime(fmt)


class Report(models.TransientModel):
    """
    This report has the following structure:
        * Report (which is just a data container)
        ** Category
        *** Asset
        **** Depreciation
        ***** Depreciation Line by Year
    Each class is set to be linked via a M2O to its parent class, and via
    a O2M to its child class.
    Each class is linked to Report via `report_id` field.
    Asset and Depreciation Line by Year both have a relation to the section
    Accounting Data which stores sale/purchase data.
    """

    _name = "report_asset_journal"
    _description = "Report Asset Journal"
    _inherit = "report.account_financial_report.abstract_report"

    # Data fields
    asset_ids = fields.Many2many(
        "asset.asset",
    )

    asset_order_fname = fields.Char()

    category_ids = fields.Many2many(
        "asset.category",
    )

    company_id = fields.Many2one(
        "res.company",
    )

    date = fields.Date()

    show_totals = fields.Boolean()

    show_category_totals = fields.Boolean()
    show_sold_assets = fields.Boolean()
    type_ids = fields.Many2many(
        "asset.depreciation.type",
    )

    # Report structure fields
    report_category_ids = fields.One2many("report_asset_journal_category", "report_id")

    report_asset_ids = fields.One2many("report_asset_journal_asset", "report_id")

    report_depreciation_ids = fields.One2many(
        "report_asset_journal_depreciation", "report_id"
    )

    report_depreciation_line_year_ids = fields.One2many(
        "report_asset_journal_depreciation_line_year", "report_id"
    )

    report_total_ids = fields.One2many("report_asset_journal_totals", "report_id")

    # Fields to be printed
    report_footer_year = fields.Char()
    report_name = fields.Char()

    ############################
    #                          #
    # REPORT RENDERING METHODS #
    #                          #
    ############################

    def print_report(self, report_type=None):
        """
        This method is called from the JS widget buttons 'Print'
        and 'Export' in the HTML view.
        Prints PDF and XLSX reports.
        :param report_type: string that represents the report type
        """
        self.ensure_one()
        report_type = report_type or "qweb-pdf"
        if report_type in ("qweb-pdf", "xlsx", "qweb-html"):
            res = self.do_print(report_type)
        elif report_type:
            raise ValidationError(
                _("No report has been defined for type `{}`.").format(report_type)
            )
        else:
            raise ValidationError(
                _("No report type has been declared for current print.")
            )
        return res

    def do_print(self, report_type):
        self.ensure_one()
        if report_type == "qweb-pdf":
            xml_id = "l10n_it_asset_management.report_asset_journal_pdf"
        elif report_type == "qweb-html":
            xml_id = "l10n_it_asset_management.report_asset_journal_html"
        else:
            xml_id = "l10n_it_asset_management.report_asset_journal_xlsx"
        report = self.env.ref(xml_id)
        return report.report_action(self)

    @api.model
    def get_html(self, given_context=None):
        """Method needed from JavaScript widget to render HTML view"""
        context = dict(self.env.context)
        context.update(given_context or {})
        report = self or self.browse(context.get("active_id"))
        xml_id = "l10n_it_asset_management.template_asset_journal_report"

        result = {}
        if report:
            context["o"] = report
            result["html"] = self.env.ref(xml_id).render(context)
        return result

    ###########################
    #                         #
    # REPORT CREATION METHODS #
    #                         #
    ###########################

    def compute_data_for_report(self):
        """Compute data to be printed"""
        self.set_report_name()
        self.generate_structure()
        self.generate_data()

    def generate_data(self):
        self.report_category_ids.generate_data()
        self.report_asset_ids.generate_data()
        self.report_depreciation_ids.generate_data()
        self.report_depreciation_line_year_ids.generate_data()
        self.report_category_ids.generate_totals()
        self.generate_totals()

    def generate_structure(self):
        deps = self.get_depreciations()
        dep_lines = deps.mapped("line_ids")
        assets = deps.mapped("asset_id")
        if self.date:
            assets = assets.filtered(
                lambda a: not a.purchase_date or a.purchase_date <= self.date
            )
            dep_lines = dep_lines.filtered(lambda dl: dl.date <= self.date)
        categories = assets.mapped("category_id")

        if not (categories and assets and deps and dep_lines):
            raise ValidationError(
                _("There is nothing to print according to current settings!")
            )

        dep_lines_grouped = OrderedDict()
        fiscal_year = self.env["account.fiscal.year"]
        for dep_line in dep_lines.sorted("date"):
            dep = dep_line.depreciation_id
            fyear = fiscal_year.get_fiscal_year_by_date(
                dep_line.date, company=dep_line.company_id
            )
            key = (dep, fyear)
            if key not in dep_lines_grouped:
                dep_lines_grouped[key] = self.env["asset.depreciation.line"]
            dep_lines_grouped[key] += dep_line

        self.write(
            {
                "report_category_ids": [
                    (0, 0, {"category_id": c.id, "report_id": self.id})
                    for c in categories.sorted("name")
                ]
            }
        )
        for report_categ in self.report_category_ids:
            report_categ.write(
                {
                    "report_asset_ids": [
                        (0, 0, {"asset_id": a.id, "report_id": self.id})
                        for a in self.sort_assets(assets)
                        if a.category_id == report_categ.category_id
                    ]
                }
            )
        for report_asset in self.report_asset_ids:
            report_asset.write(
                {
                    "report_depreciation_ids": [
                        (0, 0, {"depreciation_id": d.id, "report_id": self.id})
                        for d in deps
                        if d.asset_id == report_asset.asset_id
                    ]
                }
            )
        for report_dep in self.report_depreciation_ids:
            sequence = 0
            for (dep, fyear), lines in dep_lines_grouped.items():
                if dep == report_dep.depreciation_id:
                    sequence += 1
                    report_dep.write(
                        {
                            "report_depreciation_year_line_ids": [
                                (
                                    0,
                                    0,
                                    {
                                        "dep_line_ids": [(6, 0, lines.ids)],
                                        "fiscal_year_id": fyear.id,
                                        "report_id": self.id,
                                        "sequence": sequence,
                                    },
                                )
                            ]
                        }
                    )

    def generate_totals(self):
        curr = self.company_id.currency_id
        categ_totals = self.report_category_ids.mapped("report_total_ids")
        fnames = self.env["report_asset_journal_totals"]._total_fnames
        totals_by_dep_type = {
            t: {fname: 0 for fname in fnames} for t in categ_totals.mapped("type_id")
        }
        for total in categ_totals:
            total_curr = total.get_currency()
            total_type = total.type_id
            for fname in fnames:
                totals_by_dep_type[total_type][fname] += total_curr._convert(
                    total[fname], curr, self.company_id, self.date
                )
        self.write(
            {
                "report_total_ids": [
                    (
                        0,
                        0,
                        dict(
                            v,
                            name=_("General Total"),
                            type_name=t.name_get()[0][-1],
                            type_id=t.id,
                        ),
                    )
                    for t, v in totals_by_dep_type.items()
                ]
            }
        )

    def get_depreciations(self):
        domain = []
        if self.asset_ids:
            domain += [("asset_id", "in", self.asset_ids.ids)]
        if self.category_ids:
            domain += [("asset_id.category_id", "in", self.category_ids.ids)]
        if self.company_id:
            domain += [("company_id", "=", self.company_id.id)]
        if self.date:
            domain += [("date_start", "<=", self.date)]
        if self.type_ids:
            domain += [("type_id", "in", self.type_ids.ids)]
        if not self.show_sold_assets:
            domain += [
                "|",
                ("asset_id.sale_date", "=", False),
                ("asset_id.sale_date", ">=", self.date.replace(month=1, day=1)),
            ]
        return self.env["asset.depreciation"].search(domain)

    def set_report_name(self):
        report_name = _("Assets Depreciations ")
        if self.date:
            report_name += _("to date {}").format(format_date(self, "date", "%d-%m-%Y"))
        self.report_name = report_name.strip()

    def sort_assets(self, assets):
        sortable_assets = assets.filtered(self.asset_order_fname)
        sorted_assets = (
            sortable_assets.sorted(self.asset_order_fname)
            + (assets - sortable_assets).sorted()
        )
        return sorted_assets


class ReportCategory(models.TransientModel):
    _name = "report_asset_journal_category"
    _description = "Report Asset Journal Category"
    _inherit = "report.account_financial_report.abstract_report"

    # Data fields
    category_id = fields.Many2one("asset.category", ondelete="cascade", required=True)

    # Report structure fields
    report_id = fields.Many2one(
        "report_asset_journal",
    )

    report_asset_ids = fields.One2many(
        "report_asset_journal_asset", "report_category_id"
    )

    report_total_ids = fields.One2many(
        "report_asset_journal_totals", "report_category_id"
    )

    # Fields to be printed
    category_name = fields.Char()

    def generate_data(self):
        for report_categ in self:
            report_categ.write(report_categ.get_report_categ_data())

    def get_report_categ_data(self):
        self.ensure_one()
        return {"category_name": self.category_id.name}

    def generate_totals(self):
        for categ in self:
            curr = categ.report_id.company_id.currency_id
            report_date = categ.report_id.date
            report_deps = categ.report_asset_ids.mapped("report_depreciation_ids")
            fnames = categ.env["report_asset_journal_totals"]._total_fnames
            totals_by_dep_type = {
                t: {fname: 0 for fname in fnames}
                for t in report_deps.mapped("depreciation_id.type_id")
            }
            for report_dep in report_deps.filtered("report_depreciation_year_line_ids"):
                dep_type = report_dep.depreciation_id.type_id
                last_line = report_dep.report_depreciation_year_line_ids[-1]
                line_curr = last_line.get_currency()
                fy_start = last_line.fiscal_year_id.date_from
                fy_end = last_line.fiscal_year_id.date_to
                for fname in fnames:
                    if fname == "amount_depreciation_fund_prev_year":
                        if fy_start <= report_date <= fy_end:
                            totals_by_dep_type[dep_type][fname] += line_curr._convert(
                                last_line[fname],
                                curr,
                                categ.report_id.company_id,
                                report_date,
                            )
                    elif fname in (
                        "amount_in_total",
                        "amount_out_total",
                        "gain_loss_total",
                    ):
                        if fy_start <= report_date <= fy_end:
                            totals_by_dep_type[dep_type][fname] += line_curr._convert(
                                last_line[fname],
                                curr,
                                categ.report_id.company_id,
                                report_date,
                            )
                        elif report_date < fy_start:
                            totals_by_dep_type[dep_type][fname] = 0
                    elif fname == "amount_depreciated":
                        if fy_start <= report_date <= fy_end:
                            totals_by_dep_type[dep_type][fname] += line_curr._convert(
                                last_line[fname],
                                curr,
                                categ.report_id.company_id,
                                report_date,
                            )
                    else:
                        totals_by_dep_type[dep_type][fname] += line_curr._convert(
                            last_line[fname],
                            curr,
                            categ.report_id.company_id,
                            report_date,
                        )
            categ.write(
                {
                    "report_total_ids": [
                        (
                            0,
                            0,
                            dict(
                                v,
                                name=categ.category_id.name_get()[0][-1],
                                type_name=t.name_get()[0][-1],
                                type_id=t.id,
                            ),
                        )
                        for t, v in totals_by_dep_type.items()
                    ]
                }
            )


class ReportAsset(models.TransientModel):
    _name = "report_asset_journal_asset"
    _description = "Report Asset Journal Asset"
    _inherit = "report.account_financial_report.abstract_report"

    # Data fields
    asset_id = fields.Many2one("asset.asset", ondelete="cascade", required=True)

    # Report structure fields
    report_id = fields.Many2one(
        "report_asset_journal",
    )

    report_category_id = fields.Many2one("report_asset_journal_category")

    report_depreciation_ids = fields.One2many(
        "report_asset_journal_depreciation", "report_asset_id"
    )

    report_purchase_doc_id = fields.Many2one(
        "report_asset_journal_accounting_doc",
    )

    report_sale_doc_id = fields.Many2one(
        "report_asset_journal_accounting_doc",
    )

    # Fields to be printed
    asset_code = fields.Char()
    asset_name = fields.Char()
    asset_purchase_amount = fields.Float()
    asset_state = fields.Char()
    asset_used = fields.Char()

    def format_amount(self, amount, currency=None):
        self.ensure_one()
        currency = currency or self.get_currency()
        return format_amount(self.env, amount, currency)

    def generate_data(self):
        for report_asset in self:
            report_asset.write(report_asset.get_report_asset_data())

    def get_currency(self):
        self.ensure_one()
        return self.asset_id.currency_id

    def get_report_asset_data(self):
        self.ensure_one()
        asset = self.asset_id
        states_dict = dict(asset._fields["state"].selection)

        vals = {
            "asset_code": asset.code or "/",
            "asset_name": asset.name,
            "asset_purchase_amount": asset.purchase_amount,
            "asset_state": states_dict.get(asset.state) or _("Unknown"),
            "asset_used": _("Used") if asset.used else _("New"),
        }

        acc_doc = self.env["report_asset_journal_accounting_doc"]
        purchase_vals = self.get_purchase_vals()
        if purchase_vals:
            vals.update(
                {
                    "report_purchase_doc_id": acc_doc.create(purchase_vals).id,
                }
            )

        sale_vals = self.get_sale_vals()
        if sale_vals:
            vals.update(
                {
                    "report_sale_doc_id": acc_doc.create(sale_vals).id,
                }
            )

        return vals

    def get_purchase_vals(self):
        asset = self.asset_id
        purchase_vals = {
            "partner_name": asset.supplier_id.name or "/",
            "partner_vat": asset.supplier_id.vat or "/",
        }

        if asset.purchase_date:
            purchase_vals["document_date"] = format_date(
                asset, "purchase_date", "%d-%m-%Y"
            )

        if asset.supplier_ref:
            purchase_vals["partner_ref"] = asset.supplier_ref
        elif asset.purchase_move_id.payment_reference:
            purchase_vals["partner_ref"] = asset.purchase_move_id.payment_reference
        elif asset.purchase_move_id.ref:
            purchase_vals["partner_ref"] = asset.purchase_move_id.ref
        else:
            purchase_vals["partner_ref"] = "/"

        if asset.purchase_move_id:
            purchase_vals.update(
                {
                    "document_nr": asset.purchase_move_id.name or "/",
                    "res_id": asset.purchase_move_id.id,
                    "res_model": "account.move",
                }
            )
        else:
            purchase_vals.update(
                {
                    "document_nr": "/",
                    "res_id": asset.id,
                    "res_model": "asset.asset",
                }
            )

        return purchase_vals

    def get_sale_vals(self):
        asset = self.asset_id
        if not asset.sale_date or asset.sale_date > self.report_id.date:
            return {}

        sale_vals = {
            "document_date": format_date(asset, "sale_date", "%d-%m-%Y"),
            "partner_name": asset.customer_id.name,
            "partner_vat": asset.customer_id.vat or "/",
        }

        if asset.sale_move_id:
            sale_vals.update(
                {
                    "document_nr": asset.sale_move_id.name or "/",
                    "res_id": asset.sale_move_id.id,
                    "res_model": "account.move",
                }
            )
        else:
            sale_vals.update(
                {
                    "document_nr": "/",
                    "res_id": asset.id,
                    "res_model": "asset.asset",
                }
            )
        return sale_vals


class ReportDepreciation(models.TransientModel):
    _name = "report_asset_journal_depreciation"
    _description = "Report Asset Journal Depreciation"
    _inherit = "report.account_financial_report.abstract_report"
    _order = "type_name asc"

    # Data fields
    depreciation_id = fields.Many2one(
        "asset.depreciation", ondelete="cascade", required=True
    )

    # Report structure fields
    report_id = fields.Many2one(
        "report_asset_journal",
    )

    report_asset_id = fields.Many2one("report_asset_journal_asset")

    report_depreciation_year_line_ids = fields.One2many(
        "report_asset_journal_depreciation_line_year", "report_depreciation_id"
    )

    # Fields to be printed
    dep_amount_depreciable = fields.Float()
    dep_date_start = fields.Char()
    dep_percentage = fields.Float()
    dep_pro_rata_temporis = fields.Char()
    mode_name = fields.Char()
    type_name = fields.Char()

    def format_amount(self, amount, currency=None):
        self.ensure_one()
        currency = currency or self.get_currency()
        return format_amount(self.env, amount, currency)

    def generate_data(self):
        for report_dep in self:
            report_dep.write(report_dep.get_report_dep_data())

    def get_currency(self):
        self.ensure_one()
        return self.depreciation_id.currency_id

    def get_report_dep_data(self):
        self.ensure_one()
        dep = self.depreciation_id
        if dep.pro_rata_temporis:
            dep_pro_rata_temporis = "\u2612"  # checked ballot box -> ☒
        else:
            dep_pro_rata_temporis = "\u2610"  # empty ballot box -> ☐

        return {
            "dep_amount_depreciable": dep.amount_depreciable,
            "dep_date_start": format_date(dep, "date_start", "%d-%m-%Y"),
            "dep_percentage": dep.percentage,
            "dep_pro_rata_temporis": dep_pro_rata_temporis,
            "mode_name": dep.mode_id.name_get()[0][-1] if dep.mode_id else "",
            "type_name": dep.type_id.name_get()[0][-1] if dep.type_id else "",
        }


class ReportDepreciationLineByYear(models.TransientModel):
    _name = "report_asset_journal_depreciation_line_year"
    _description = "Report Asset Journal Depreciation Line Year"
    _inherit = "report.account_financial_report.abstract_report"
    _order = "sequence asc"

    # Data fields
    dep_line_ids = fields.Many2many(
        "asset.depreciation.line", relation="report_journal_line_year_dep_line"
    )

    fiscal_year_id = fields.Many2one("account.fiscal.year")

    # Report structure fields
    report_id = fields.Many2one(
        "report_asset_journal",
    )

    report_depreciation_id = fields.Many2one("report_asset_journal_depreciation")

    report_accounting_doc_ids = fields.Many2many(
        "report_asset_journal_accounting_doc",
        relation="year_dep_line_accounting_doc_rel",
    )

    sequence = fields.Integer()

    # Fields to be printed
    amount_depreciable = fields.Float()
    amount_depreciable_updated = fields.Float()
    amount_depreciated = fields.Float()
    amount_depreciation_fund_curr_year = fields.Float()
    amount_depreciation_fund_prev_year = fields.Float()
    amount_gain = fields.Float()
    amount_gain_total = fields.Float()
    amount_historical = fields.Float()
    amount_in = fields.Float()
    amount_in_detail = fields.Char()
    amount_in_total = fields.Float()
    amount_loss = fields.Float()
    amount_loss_total = fields.Float()
    amount_out = fields.Float()
    amount_out_detail = fields.Char()
    amount_out_total = fields.Float()
    amount_residual = fields.Float()
    date_start = fields.Char()
    gain_loss = fields.Float()  # Needed for the .xls report
    gain_loss_total = fields.Float()  # Needed for the .xls report
    has_amount_detail = fields.Boolean()
    percentage = fields.Float()
    year = fields.Char()
    type_name = fields.Char()

    def format_amount(self, amount, currency=None):
        self.ensure_one()
        currency = currency or self.get_currency()
        return format_amount(self.env, amount, currency)

    def generate_data(self):
        for report_dep_line_year in self.sorted():  # Force sorting by _order
            report_dep_line_year.write(
                report_dep_line_year.get_report_dep_line_year_data()
            )

    def get_currency(self):
        self.ensure_one()
        return self.report_depreciation_id.depreciation_id.currency_id

    def get_report_dep_line_year_data(self):
        self.ensure_one()
        report_dep = self.report_depreciation_id
        grouped_amounts = self.dep_line_ids.get_balances_grouped()

        amount_depreciable = report_dep.dep_amount_depreciable
        amount_gain = grouped_amounts.get("gain") or 0.0
        amount_gain_total = amount_gain
        amount_historical = abs(grouped_amounts.get("historical") or 0.0)
        amount_in = abs(grouped_amounts.get("in") or 0.0)
        amount_in_total = amount_in
        amount_loss = grouped_amounts.get("loss") or 0.0
        amount_loss_total = amount_loss
        amount_out = abs(grouped_amounts.get("out") or 0.0)
        amount_out_total = amount_out
        gain_loss = amount_gain + amount_loss
        gain_loss_total = gain_loss

        amount_depreciated = sum(
            [
                line.amount
                for line in self.dep_line_ids.filtered(
                    lambda l: l.move_type == "depreciated" and not l.partial_dismissal
                )
            ]
        )
        amount_dismissal = sum(
            [
                line.amount
                for line in self.dep_line_ids.filtered(
                    lambda l: l.move_type == "depreciated" and l.partial_dismissal
                )
            ]
        )

        prev_year_line = report_dep.report_depreciation_year_line_ids.filtered(
            lambda l: l.sequence == self.sequence - 1
        )
        asset = self.report_depreciation_id.report_asset_id.asset_id
        fy_start = self.fiscal_year_id.date_from
        fy_end = self.fiscal_year_id.date_to
        if asset.sold and asset.sale_date and fy_start <= asset.sale_date <= fy_end:
            amount_depreciable_upd = 0.0
            depreciation_fund_curr_year = 0.0
            amount_residual = 0.0
            if prev_year_line:
                depreciation_fund_prev_year = (
                    prev_year_line.amount_depreciation_fund_curr_year
                )
                amount_in_total += prev_year_line.amount_in_total
                amount_out_total += prev_year_line.amount_out_total
            else:
                depreciation_fund_prev_year = 0.0
        else:
            if prev_year_line:
                depreciation_fund_prev_year = (
                    prev_year_line.amount_depreciation_fund_curr_year
                )
                prev_year_resid = prev_year_line.amount_residual
                amount_depreciable_upd = (
                    prev_year_line.amount_depreciable_updated + amount_in - amount_out
                )
                amount_in_total += prev_year_line.amount_in_total
                amount_out_total += prev_year_line.amount_out_total
            else:
                depreciation_fund_prev_year = 0.0
                prev_year_resid = amount_depreciable
                amount_depreciable_upd = amount_depreciable + amount_in - amount_out

            depreciation_fund_curr_year = (
                depreciation_fund_prev_year + amount_depreciated + amount_dismissal
            )
            amount_residual = (
                prev_year_resid
                + amount_in
                - amount_out
                - amount_depreciated
                - amount_dismissal
            )
        if prev_year_line:
            amount_gain_total += prev_year_line.amount_gain_total
            amount_loss_total += prev_year_line.amount_loss_total
            gain_loss_total += prev_year_line.gain_loss_total

        type_mapping = {"in": {}, "out": {}}
        for dep_line in self.dep_line_ids.filtered(
            lambda l: l.move_type in ("in", "out") and l.depreciation_line_type_id
        ):
            dep_type = dep_line.depreciation_line_type_id
            if dep_type not in type_mapping[dep_line.move_type]:
                type_mapping[dep_line.move_type][dep_type] = 0
            type_mapping[dep_line.move_type][dep_type] += dep_line.amount

        amount_in_detail = amount_out_detail = ""
        has_amount_detail = False
        if type_mapping["in"]:
            amount_in_detail = "; ".join(
                [
                    "{}: {}".format(dep_type.name, self.format_amount(amount))
                    for dep_type, amount in sorted(list(type_mapping["in"].items()))
                ]
            )
            has_amount_detail = True
        if type_mapping["out"]:
            amount_out_detail = "; ".join(
                [
                    "{}: {}".format(dep_type.name, self.format_amount(amount))
                    for dep_type, amount in sorted(list(type_mapping["out"].items()))
                ]
            )
            has_amount_detail = True

        accounting_doc_vals = []
        for dep_line in self.dep_line_ids.filtered(
            lambda l: l.move_type in ("in", "out")
        ):
            for num, aa_info in enumerate(dep_line.asset_accounting_info_ids):
                vals = {
                    "document_date": format_date(dep_line, "date", "%d-%m-%Y"),
                    "document_nr": aa_info.move_id.name or "/",
                    "partner_name": aa_info.move_id.partner_id.name or "/",
                    "partner_ref": aa_info.move_id.ref or "/",
                    "partner_vat": aa_info.move_id.partner_id.vat or "/",
                    "res_id": aa_info.move_id.id,
                    "res_model": "account.move",
                    "sequence": num + 1,
                }
                accounting_doc_vals.append((0, 0, vals))

        start = fields.Date.from_string(self.fiscal_year_id.date_from).year
        end = fields.Date.from_string(self.fiscal_year_id.date_to).year
        if start == end:
            year = str(start)
        else:
            year = "{} - {}".format(start, end)

        return {
            "amount_depreciable": amount_depreciable,
            "amount_depreciable_updated": amount_depreciable_upd,
            "amount_depreciated": amount_depreciated,
            "amount_depreciation_fund_curr_year": depreciation_fund_curr_year,
            "amount_depreciation_fund_prev_year": depreciation_fund_prev_year,
            "amount_gain": amount_gain,
            "amount_historical": amount_historical,
            "amount_in": amount_in,
            "amount_in_detail": amount_in_detail,
            "amount_in_total": amount_in_total,
            "amount_loss": amount_loss,
            "amount_out": amount_out,
            "amount_out_detail": amount_out_detail,
            "amount_out_total": amount_out_total,
            "amount_residual": amount_residual,
            "date_start": report_dep.dep_date_start,
            "gain_loss": gain_loss,
            "gain_loss_total": gain_loss_total,
            "has_amount_detail": has_amount_detail,
            "percentage": report_dep.dep_percentage,
            "report_accounting_doc_ids": accounting_doc_vals,
            "type_name": report_dep.type_name,
            "year": year,
        }


class ReportAccountingDoc(models.TransientModel):
    _name = "report_asset_journal_accounting_doc"
    _description = "Report Asset Journal Accounting Doc"
    _inherit = "report.account_financial_report.abstract_report"
    _order = "sequence asc"

    # Report structure fields
    report_id = fields.Many2one(
        "report_asset_journal",
    )

    # Fields to be printed
    document_date = fields.Char()
    document_nr = fields.Char()
    partner_name = fields.Char()
    partner_ref = fields.Char()
    partner_vat = fields.Char()
    res_id = fields.Integer()
    res_model = fields.Char()
    sequence = fields.Integer()


class ReportTotals(models.TransientModel):
    _name = "report_asset_journal_totals"
    _description = "Report Asset Journal Totals"
    _inherit = "report.account_financial_report.abstract_report"
    _total_fnames = [
        "amount_depreciable_updated",
        "amount_depreciated",
        "amount_depreciation_fund_curr_year",
        "amount_depreciation_fund_prev_year",
        "amount_gain",
        "amount_in_total",
        "amount_loss",
        "amount_out_total",
        "amount_residual",
        "gain_loss_total",
    ]

    # Data fields
    type_id = fields.Many2one(
        "asset.depreciation.type",
    )

    # Report structure fields
    report_id = fields.Many2one(
        "report_asset_journal",
    )

    report_category_id = fields.Many2one("report_asset_journal_category")

    # Fields to be printed
    amount_depreciable_updated = fields.Float()
    amount_depreciated = fields.Float()
    amount_depreciation_fund_curr_year = fields.Float()
    amount_depreciation_fund_prev_year = fields.Float()
    amount_gain = fields.Float()
    amount_in_total = fields.Float()
    amount_loss = fields.Float()
    amount_out_total = fields.Float()
    amount_residual = fields.Float()
    gain_loss = fields.Float()  # Needed for the .xls report
    gain_loss_total = fields.Float()  # Needed for the .xls report
    name = fields.Char()  # Needed for the .xls report
    type_name = fields.Char()

    def format_amount(self, amount, currency=None):
        self.ensure_one()
        currency = currency or self.get_currency()
        return format_amount(self.env, amount, currency)

    def get_currency(self):
        self.ensure_one()
        report = self.report_id or self.report_category_id.report_id
        return report.company_id.currency_id
