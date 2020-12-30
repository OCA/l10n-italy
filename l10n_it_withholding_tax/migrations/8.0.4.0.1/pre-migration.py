# -*- coding: utf-8 -*-
# Copyright (C) 2020 Ciro Urselli (<http://www.apuliasoftware.it>).
# Copyright 2020 Vincenzo Terzulli <v.terzulli@elvenstudio.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(cr, version):
    if not version:
        return

    # backup existing 'withholding_tax' field values
    openupgrade.copy_columns(cr, {
        'account_invoice': [
            ('withholding_tax', 'withholding_tax_backup', None),
        ]
    })
