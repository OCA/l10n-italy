# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio <davide.corio@abstract.it>
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Gianmarco Conte - Dinamiche Aziendali srl
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from . import models


def pre_init_hook(cr):
    cr.execute("SELECT state from ir_module_module where name = "
               "'l10n_it_fatturapa' and state in ('installed', 'to upgrade')")
    l10n_it_fatturapa_is_installed = cr.fetchone()
    if l10n_it_fatturapa_is_installed:
        cr.execute(
            "UPDATE ir_model_data SET module = 'l10n_it_fiscal_payment_term' "
            "WHERE model = 'fatturapa.payment_term'")
        cr.execute(
            "UPDATE ir_model_data SET module = 'l10n_it_fiscal_payment_term' "
            "WHERE model = 'fatturapa.payment_method'")
