# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: ElvenStudio
#    Copyright 2015 elvenstudio.it
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
#
##############################################################################

from . import models


def pre_init_hook(cr):
    cr.execute("SELECT state from ir_module_module where name = "
               "'l10n_it_fatturapa' and state in ('installed', 'to upgrade')")
    l10n_it_fatturapa_is_installed = cr.fetchone()
    if l10n_it_fatturapa_is_installed:
        cr.execute(
            "UPDATE ir_model_data SET module = 'l10n_it_fiscal_payment_mode' "
            "WHERE model = 'fatturapa.payment_method'")
