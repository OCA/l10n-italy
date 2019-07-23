#  Copyright 2019 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def write_sudo_inv_subj(self, inv_subj):
        """
        Method called from frontend.
        Write field `electronic_invoice_subjected` in self using sudo.

        :param inv_subj: value of field `electronic_invoice_subjected`
        :return: The id of updated partner,
        or False if the write operation did not succeed
        """
        self.ensure_one()

        try:
            return self.sudo().write({
                'electronic_invoice_subjected': inv_subj,
            })
        except ValidationError:
            return False
