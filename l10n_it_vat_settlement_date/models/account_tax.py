# Copyright (c) 2021 Marco Colombo (https://github/TheMule71)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class AccountTax(models.Model):
    _inherit = "account.tax"


    def _account_tax_ids_with_moves(self):
        """ Return all account.tax ids for which there is at least
        one account.move.line in the context period
        for the user company.

        Caveat: this ignores record rules and ACL but it is good
        enough for filtering taxes with activity during the period.
        """
        req = """
            SELECT id
            FROM account_tax at
            WHERE
            company_id = %s AND
            EXISTS (
              SELECT 1 FROM account_move_line aml
              WHERE
                COALESCE(date_vat_settlement, date) >= %s AND
                COALESCE(date_vat_settlement, date) <= %s AND
                company_id = %s AND (
                  tax_line_id = at.id OR
                  EXISTS (
                    SELECT 1 FROM account_move_line_account_tax_rel
                    WHERE account_move_line_id = aml.id AND
                      account_tax_id = at.id
                  )
                )
            )
        """
        from_date, to_date, company_id, target_move = self.get_context_values()
        self.env.cr.execute(
            req, (company_id, from_date, to_date, company_id))
        return [r[0] for r in self.env.cr.fetchall()]


    def get_move_line_partial_domain(self, from_date, to_date, company_id):
        return [
            '|', '&', ('date_vat_settlement', '>=', from_date), ('date_vat_settlement', '<=', to_date),
                 '&', ('date_vat_settlement', '=', None), '&', ('date', '<=', to_date), ('date', '>=', from_date),
            ('company_id', '=', company_id),
        ]
