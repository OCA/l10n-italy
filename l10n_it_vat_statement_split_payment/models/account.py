# Copyright 2018 Silvio Gregorini (silviogregorini@openforce.it)
# Copyright (c) 2018 Openforce Srls Unipersonale (www.openforce.it)
# Copyright (c) 2019 Matteo Bilotta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def group_by_account_and_tax(self):
        grouped_lines = {}

        for line in self:
            group_key = (line.account_id, line.tax_line_id)
            if group_key not in grouped_lines:
                grouped_lines.update({group_key: []})

            grouped_lines[group_key].append(line)

        return grouped_lines
