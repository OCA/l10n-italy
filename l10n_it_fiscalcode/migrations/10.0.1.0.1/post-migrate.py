# -*- coding: utf-8 -*-
# Copyright 2018 Alex Comba - Agile Business Group
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """ Sync of fiscalcode field to descendants """
    if not version:
        return
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        partners = env['res.partner'].search(
            [('is_company', '=', True)])
        for partner in partners:
            partner._commercial_sync_to_children()
