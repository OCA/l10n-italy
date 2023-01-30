# Copyright 2019-2023 Openforce Srls Unipersonale (www.openforce.it)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from . import models
from . import wizards


CODED_MODELS = (
    'asset.asset',
    'asset.category',
    'asset.depreciation.mode',
    'asset.depreciation.type'
)


def set_import_codes(cr, registry):
    from odoo import SUPERUSER_ID
    from odoo.api import Environment
    env = Environment(cr, SUPERUSER_ID, {})

    for model in CODED_MODELS:
        for rec in env[model].sudo().search([]):
            rec.assign_import_code()
