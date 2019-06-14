# Copyright (c) 2019 Matteo Bilotta
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ReportVatRegistry(models.AbstractModel):
    _inherit = 'report.l10n_it_vat_registries.report_registro_iva'

    @api.model
    def _compute_totals_tax(self, tax, data):
        res = super()._compute_totals_tax(tax, data)

        if tax.is_split_payment:
            # res = (tax_name, base, tax, deductible, undeductible)
            #
            # In case of SP tax, SP VAT must not appear as deductible.
            #
            return (res[0], res[1], res[2], 0.0, res[4])

        return res
