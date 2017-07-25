# -*- coding: utf-8 -*-
# Copyright 2017 Davide Corio
# Copyright 2017 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    rc_type_id = fields.Many2one('account.rc.type', 'RC Type')
