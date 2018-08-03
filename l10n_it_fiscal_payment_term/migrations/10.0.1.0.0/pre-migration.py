# -*- coding: utf-8 -*-
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2017-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    if not version:
        return
    try:
        from openupgradelib import openupgrade
        openupgrade.rename_xmlids(
            cr, [
                ('l10n_it_fatturapa.fatturapa_TP01',
                 'l10n_it_fiscal_payment_term.fatturapa_TP01',),
                ('l10n_it_fatturapa.fatturapa_tp02',
                 'l10n_it_fiscal_payment_term.fatturapa_tp02',),
                ('l10n_it_fatturapa.fatturapa_tp03',
                 'l10n_it_fiscal_payment_term.fatturapa_tp03', ),
                ('l10n_it_fatturapa.fatturapa_tp04',
                 'l10n_it_fiscal_payment_term.fatturapa_tp04', ),
                ('l10n_it_fatturapa.fatturapa_mp01',
                 'l10n_it_fiscal_payment_term.fatturapa_mp01',),
                ('l10n_it_fatturapa.fatturapa_mp02',
                 'l10n_it_fiscal_payment_term.fatturapa_mp02',),
                ('l10n_it_fatturapa.fatturapa_mp03',
                 'l10n_it_fiscal_payment_term.fatturapa_mp03',),
                ('l10n_it_fatturapa.fatturapa_mp04',
                 'l10n_it_fiscal_payment_term.fatturapa_mp04',),
                ('l10n_it_fatturapa.fatturapa_mp05',
                 'l10n_it_fiscal_payment_term.fatturapa_mp05',),
                ('l10n_it_fatturapa.fatturapa_mp06',
                 'l10n_it_fiscal_payment_term.fatturapa_mp06',),
                ('l10n_it_fatturapa.fatturapa_mp07',
                 'l10n_it_fiscal_payment_term.fatturapa_mp07',),
                ('l10n_it_fatturapa.fatturapa_mp08',
                 'l10n_it_fiscal_payment_term.fatturapa_mp08',),
                ('l10n_it_fatturapa.fatturapa_mp09',
                 'l10n_it_fiscal_payment_term.fatturapa_mp09',),
                ('l10n_it_fatturapa.fatturapa_mp10',
                 'l10n_it_fiscal_payment_term.fatturapa_mp10',),
                ('l10n_it_fatturapa.fatturapa_mp11',
                 'l10n_it_fiscal_payment_term.fatturapa_mp11',),
                ('l10n_it_fatturapa.fatturapa_mp12',
                 'l10n_it_fiscal_payment_term.fatturapa_mp12',),
                ('l10n_it_fatturapa.fatturapa_mp13',
                 'l10n_it_fiscal_payment_term.fatturapa_mp13',),
                ('l10n_it_fatturapa.fatturapa_mp14',
                 'l10n_it_fiscal_payment_term.fatturapa_mp14',),
                ('l10n_it_fatturapa.fatturapa_mp15',
                 'l10n_it_fiscal_payment_term.fatturapa_mp15',),
                ('l10n_it_fatturapa.fatturapa_mp16',
                 'l10n_it_fiscal_payment_term.fatturapa_mp16',),
                ('l10n_it_fatturapa.fatturapa_mp17',
                 'l10n_it_fiscal_payment_term.fatturapa_mp17',),
                ('l10n_it_fatturapa.fatturapa_mp18',
                 'l10n_it_fiscal_payment_term.fatturapa_mp18',),
                ('l10n_it_fatturapa.fatturapa_mp19',
                 'l10n_it_fiscal_payment_term.fatturapa_mp19',),
                ('l10n_it_fatturapa.fatturapa_mp20',
                 'l10n_it_fiscal_payment_term.fatturapa_mp20',),
                ('l10n_it_fatturapa.fatturapa_mp21',
                 'l10n_it_fiscal_payment_term.fatturapa_mp21',),
                ('l10n_it_fatturapa.fatturapa_mp22',
                 'l10n_it_fiscal_payment_term.fatturapa_mp22',),
            ],
        )
    except ImportError:
        raise Exception("You need openupgradelib for performing the migration")
