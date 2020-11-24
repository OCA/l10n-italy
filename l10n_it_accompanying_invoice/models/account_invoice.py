# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2020 Simone Vanin - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'
    # we need this to be able to call l10n_it_ddt.delivery_data
    note = fields.Text('Notes', readonly=True, related="comment")
    date_done = fields.Datetime(string='Shipping Date')
