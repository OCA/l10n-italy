##############################################################################
#
#    Author(s): Andrea Colangelo (andreacolangelo@openforce.it)
#
#    Copyright © 2017 Openforce di Camilli Alessandro (www.openforce.it)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see:
#    http://www.gnu.org/licenses/agpl-3.0.txt.
#
##############################################################################

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    enasarco_account_id = fields.Many2one(
        'account.account', 'Enasarco Account')
    enasarco_journal_id = fields.Many2one(
        'account.journal', 'Enasarco Journal')


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = "res.config.settings"

    enasarco_account_id = fields.Many2one(
        'account.account', string="Enasarco Account *",
        related='company_id.enasarco_account_id')
    enasarco_journal_id = fields.Many2one(
        'account.journal', string="Enasarco Journal *",
        related='company_id.enasarco_journal_id')

