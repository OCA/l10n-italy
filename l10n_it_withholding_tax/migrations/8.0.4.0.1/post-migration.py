# -*- coding: utf-8 -*-
# Copyright (C) 2020 Ciro Urselli (<http://www.apuliasoftware.it>).
# Copyright 2020 Vincenzo Terzulli <v.terzulli@elvenstudio.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import SUPERUSER_ID, api
from openupgradelib import openupgrade
import time
import logging
_log = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        _log.info('Recomputing WT on existing invoices...')

        counter = 0
        start_time = time.time()
        block_time = start_time

        invoice_model = env['account.invoice']
        domain = [('withholding_tax_backup', '=', True)]
        ids_invoices = invoice_model.search_read(domain=domain, fields=['id'])
        ids_invoices = [v['id'] for v in ids_invoices]

        items = 20
        while ids_invoices:
            ids = ids_invoices[:items]
            del ids_invoices[:items]
            invoice_ids = invoice_model.browse(ids)

            # dalla posizione fiscale
            # for invoice_id in invoice_ids:
            #     wt_ids = invoice_id.fiscal_position.withholding_tax_ids
            #     for line_id in invoice_id.invoice_line:
            #         if not line_id.withholding_tax_exclude:
            #             line_id.invoice_line_tax_wt_ids = [(6, 0, wt_ids.ids)]
            #     invoice_id.button_reset_taxes()

            # dal castelletto delle ritenute
            # si è scelto di adottare questo approccio per considerare i casi in cui
            # le ritenute applicate alla fattura siano stato modificate manualmente
            # nel castelletto.
            for invoice_id in invoice_ids:
                wt_ids = invoice_id.withholding_tax_line.mapped('withholding_tax_id')
                for line_id in invoice_id.invoice_line:
                    if not line_id.withholding_tax_exclude:
                        line_id.invoice_line_tax_wt_ids = [(6, 0, wt_ids.ids)]
                invoice_id.button_reset_taxes()

            counter += len(ids)
            duration = time.time() - block_time
            _log.info('   Done: %d invoices - Avg single duration: %fs' %
                      (counter, duration/items))

        _log.info('Completed in %fs' % (time.time() - start_time))

        # remove field withholding_tax_backup
        openupgrade.drop_columns(cr, {
            ('account_invoice', 'withholding_tax_backup'),
        })

    return True
